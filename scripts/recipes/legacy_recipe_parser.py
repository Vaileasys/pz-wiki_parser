#!/usr/bin/env python3
"""
Project Zomboid Wiki Legacy Recipe Parser

This script parses legacy recipe definitions from Project Zomboid's script files.
It handles the complex task of parsing various recipe formats, including crafting
recipes, fluid recipes, and construction recipes, converting them into a structured
format for wiki documentation.

The script handles:
- Parsing recipe blocks from multiple source files
- Processing nested recipe definitions
- Handling item mappers and substitutions
- Processing fluid and energy recipes
- Managing construction and crafting recipes
- Cache management for parsed data
"""

import os, re
from scripts.core.version import Version
from scripts.core.constants import DATA_DIR
from scripts.core.cache import save_cache, load_cache

RECIPES_DIR = os.path.join("resources", "scripts")
CACHE_JSON = "recipes_data.json"

# Global dictionary to store the parsed recipe data
parsed_data = {}


def remove_comments(text):
    """
    Removes block comments from text.

    Args:
        text (str): Text containing block comments.

    Returns:
        str: Text with all block comments removed.

    Comments start with /* and end with */.
    Supports nested comments and preserves non-comment text.
    """
    result = []
    current_line = 0
    length = len(text)
    while current_line < length:
        # If we find a comment start, enter comment mode
        if text[current_line:current_line+2] == "/*":
            current_line += 2
            nest = 1
            # Skip characters until we find the matching closing comment
            while current_line < length and nest > 0:
                if text[current_line:current_line+2] == "/*":
                    nest += 1
                    current_line += 2
                elif text[current_line:current_line+2] == "*/":
                    nest -= 1
                    current_line += 2
                else:
                    current_line += 1
        else:
            result.append(text[current_line])
            current_line += 1
    return "".join(result)


def get_recipe_data():
    """
    Returns the parsed recipe data.

    Returns:
        dict: Parsed recipe data, initializing it if empty.

    This function serves as the main interface to access the parsed recipe data,
    ensuring the data is loaded before being accessed.
    """
    global parsed_data
    if not parsed_data:
        main()
    return parsed_data


def gather_recipe_lines(directory: str):
    """
    Gathers recipe definitions from all relevant files in the directory.

    Args:
        directory (str): Root directory to search for recipe files.

    Returns:
        list: All lines from valid recipe files.

    Searches for files that:
    - Start with 'recipes', 'entity', or 'craftrecipe'
    - End with '.txt'
    - Don't contain 'test' or 'dbg' in the name
    """
    all_lines = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if (
                (filename.lower().startswith("recipes") or
                 filename.lower().startswith("entity") or
                 filename.lower().startswith("craftrecipe"))
                and filename.lower().endswith(".txt")
                and "test" not in filename.lower()
                and "dbg" not in filename.lower()
            ):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    all_lines.extend(f.readlines())
    return all_lines


def extract_recipe_blocks(lines):
    """
    Extracts individual recipe blocks from a list of lines.

    Args:
        lines (list): List of text lines to process.

    Returns:
        list: List of tuples containing (recipe_name, recipe_text).

    Handles:
    - Recipe block detection and extraction
    - Proper bracket matching
    - Comment removal
    - Recipe name extraction
    """
    blocks = []
    in_recipe = False
    bracket_level = 0
    current_lines = []
    current_name = None
    craft_recipe_pattern = re.compile(r'^\s*craftRecipe\s+(\S+)', re.IGNORECASE)
    comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)

    for line in lines:
        if not in_recipe:
            match = craft_recipe_pattern.search(line)
            if match:
                in_recipe = True
                current_name = match.group(1).strip()
                bracket_level = line.count('{') - line.count('}')
                current_lines = [line]
        else:
            current_lines.append(line)
            bracket_level += line.count('{')
            bracket_level -= line.count('}')
            if bracket_level <= 0:
                recipe_text = "".join(current_lines)
                # Remove any block comments from the recipe text
                recipe_text = re.sub(comment_pattern, "", recipe_text)
                blocks.append((current_name, recipe_text))

                # Reset state for next recipe block
                in_recipe = False
                bracket_level = 0
                current_lines = []
                current_name = None
    return blocks


def parse_recipe_block(recipe_name, recipe_text):
    """
    Parses a recipe block into a structured dictionary.

    Args:
        recipe_name (str): Name of the recipe.
        recipe_text (str): Raw text of the recipe block.

    Returns:
        dict: Structured recipe data including:
            - name: Recipe name
            - inputs: List of input items
            - outputs: List of output items
            - itemMappers: Dictionary of item mappings
            - Additional properties like category

    Handles:
    - Item mapper definitions
    - Input and output blocks
    - Property parsing
    - Comment removal
    """
    recipe_text = remove_comments(recipe_text)
    recipe_dict = {"name": recipe_name, "inputs": [], "outputs": []}
    mapper_pattern = re.compile(r'itemMapper\s+(\S+)\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    mappers = {}

    def mapper_replacer(match):
        mapper_name = match.group(1).strip()
        body = match.group(2).strip()
        body = remove_comments(body)
        mapper_dict = {}
        for ln in body.splitlines():
            ln = re.sub(r'/\*.*?\*/', '', ln.strip().rstrip(','))
            if not ln or ln.startswith('//'):
                continue
            if '=' in ln:
                left, right = ln.split('=', 1)
                mapper_dict[left.strip()] = right.strip().rstrip(',')
        mappers[mapper_name] = mapper_dict
        return ""

    recipe_text = mapper_pattern.sub(mapper_replacer, recipe_text)
    if mappers:
        recipe_dict["itemMappers"] = mappers

    inputs_pattern = re.compile(r'inputs\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    outputs_pattern = re.compile(r'outputs\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)

    # Parse inputs block
    m = inputs_pattern.search(recipe_text)
    if m:
        block_text = m.group(1)
        recipe_dict["inputs"] = parse_items_block(block_text, is_output=False, recipe_dict=recipe_dict)
        s, e = m.span()
        recipe_text = recipe_text[:s] + recipe_text[e:]

    # Parse outputs block
    m = outputs_pattern.search(recipe_text)
    if m:
        block_text = m.group(1)
        new_outputs = parse_items_block(block_text, is_output=True, recipe_dict=recipe_dict)

        existing_outputs = recipe_dict.get("outputs", [])
        recipe_dict["outputs"] = existing_outputs + new_outputs

        s, e = m.span()
        recipe_text = recipe_text[:s] + recipe_text[e:]

    # Parse remaining lines in the recipe text
    leftover = []
    for ln in recipe_text.splitlines():
        ln = re.sub(r'/\*.*?\*/', '', ln.strip().rstrip(','))
        if ln and not ln.startswith('//'):
            leftover.append(ln)

        # Handle leftover key-value pairs
        pair_pattern = re.compile(r'^\s*(\w+)\s*=\s*(.*?)\s*$', re.IGNORECASE)
        for ln in leftover:
            m2 = pair_pattern.match(ln)
            if not m2:
                continue
            k, v = m2.group(1), m2.group(2)
            if k.lower() == "category":
                recipe_dict["category"] = v.rstrip(',').strip()
            elif ";" in v:
                recipe_dict[k] = [x.strip() for x in v.split(";") if x.strip()]
            else:
                recipe_dict[k] = v

    return recipe_dict


def parse_items_block(block_text, is_output=False, recipe_dict=None):
    """
    Parses a block of item definitions within a recipe.

    Args:
        block_text (str): Text containing item definitions.
        is_output (bool): Whether this is an output block.
        recipe_dict (dict): Parent recipe dictionary for context.

    Returns:
        list: List of parsed item definitions.

    Handles:
    - Fluid items and modifiers
    - Energy items
    - Regular items
    - Item properties and amounts
    """
    if recipe_dict is None:
        recipe_dict = {}
    # Remove block comments from the entire block
    block_text = remove_comments(block_text)
    results = []
    lines = re.split(r'[\r\n]+', block_text)
    last_item = None
    for line in lines:
        # Remove block comments from each line
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)
        line = line.strip().rstrip(',')
        if not line or line.startswith('//'):
            continue

        # Handle fluid lines:
        if line.lower().startswith('-fluid') or line.lower().startswith('+fluid'):
            fl = parse_fluid_line(line)
            if not fl:
                continue

            # If it's a '-' fluid line
            if fl["sign"] == '-':
                if last_item:
                    if is_any_fluid_container(last_item):
                        last_item["items"] = ["Any fluid container"]
                    last_item["fluidModifier"] = {
                        "fluidType": fl["items"],
                        "amount": fl["amount"]
                    }
                else:
                    results.append({
                        "fluid": True,
                        "amount": fl["amount"],
                        "items": fl["items"]
                    })

            # If it's a '+' fluid line
            else:
                if last_item:
                    copy_item = dict(last_item)
                    copy_item["fluidModifier"] = {
                        "fluidType": fl["items"],
                        "amount": fl["amount"]
                    }
                    if not is_output:
                        outputs = recipe_dict.setdefault("outputs", [])
                        outputs.append(copy_item)
                    else:
                        results.append(copy_item)

            continue

        # Handle energy lines
        if line.lower().startswith('energy'):
            ei = parse_energy_line(line)
            if ei:
                results.append(ei)
                last_item = None
            continue

        # Handle item lines
        elif line.lower().startswith('item'):
            it = parse_item_line(line)
            if it:
                results.append(it)
                last_item = it
            continue

    return results


def is_any_fluid_container(item_obj):
    """
    Checks if an item object represents any fluid container.

    Args:
        item_obj (dict): Item object to check.

    Returns:
        bool: True if the item is any fluid container, False otherwise.
    """
    if (item_obj.get("index") == 1 and item_obj.get("items") and
        len(item_obj["items"]) == 1 and item_obj["items"][0] == "Base.*"):
        return True
    return False


def parse_fluid_line(line):
    """
    Parses a fluid line definition.

    Args:
        line (str): Line containing fluid definition.

    Returns:
        dict: Parsed fluid information including:
            - sign: '+' or '-' for fluid addition/removal
            - items: List of fluid types
            - amount: Fluid amount
        Returns None if parsing fails.
    """
    pattern = re.compile(r'^([+-])fluid\s+([\d\.]+)\s+(?:\[(.*?)\]|(\S+))', re.IGNORECASE)
    m = pattern.match(line)
    if not m:
        return None
    sign = m.group(1)
    amount = float(m.group(2))
    bracket = m.group(3)
    single = m.group(4)
    items = []
    if bracket:
        items = [x.strip() for x in re.split(r'[;,]', bracket) if x.strip()]
    elif single:
        items = [single.strip()]
    return {"sign": sign, "amount": amount, "items": items}


def parse_energy_line(line):
    """
    Parses an energy line definition.

    Args:
        line (str): Line containing energy definition.

    Returns:
        dict: Parsed energy information including:
            - energy: True flag
            - amount: Energy amount
        Returns None if parsing fails.
    """
    pattern = re.compile(r'^energy\s+([\d\.]+)\s+(\S+)\s*(.*)$', re.IGNORECASE)
    m = pattern.match(line)
    if not m:
        return None
    amt = float(m.group(1).strip())
    t = m.group(2).strip()
    mod = m.group(3).strip() if m.group(3) else None
    r = {"energy": True, "amount": amt, "type": t}
    if mod:
        r["modifiers"] = mod
    return r


def parse_item_line(line):
    """
    Parses an item line definition.

    Args:
        line (str): Line containing item definition.

    Returns:
        dict: Parsed item information including:
            - items: List of item types
            - amount: Item amount
            - index: Item index
            - Additional properties
        Returns None if parsing fails.
    """
    pattern = re.compile(r'^item\s+(\d+)\s+(.*)$', re.IGNORECASE)
    m = pattern.match(line)
    if not m:
        return None

    index = int(m.group(1))
    rest = m.group(2).strip()
    rest = re.sub(r'/\*.*?\*/', '', rest, flags=re.DOTALL)
    result = {"index": index}

    mpsec = re.compile(r'mappers?\[.*?\]', re.IGNORECASE)
    rest = mpsec.sub("", rest).strip()

    tags_pat = re.compile(r'tags\[(.*?)\]', re.IGNORECASE)
    flags_pat = re.compile(r'flags\[(.*?)\]', re.IGNORECASE)
    br_items = re.compile(r'\[(.*?)\]')
    mode_pat = re.compile(r'mode\s*:\s*(\S+)', re.IGNORECASE)
    mapr_pat = re.compile(r'mapper\s*:\s*(\S+)', re.IGNORECASE)

    # Extract mapper
    mp = mapr_pat.search(rest)
    if mp:
        result["mapper"] = mp.group(1)
        rest = mapr_pat.sub("", rest)

    # Extract mode
    mo = mode_pat.search(rest)
    if mo:
        result["mode"] = mo.group(1).capitalize()  # e.g., "Destroy"
        rest = mode_pat.sub("", rest)

    # Extract tags
    tg = tags_pat.search(rest)
    if tg:
        tstr = tg.group(1)
        spl = [x.strip() for x in re.split(r'[;,]', tstr) if x.strip()]
        result["tags"] = spl
        rest = tags_pat.sub("", rest)

    flags_found = []
    while True:
        fl = flags_pat.search(rest)
        if not fl:
            break
        spl = [x.strip() for x in re.split(r'[;,]', fl.group(1)) if x.strip()]
        flags_found.extend(spl)
        rest = flags_pat.sub("", rest, count=1)
    if flags_found:
        result["flags"] = flags_found

    if re.search(r'\bitemcount\b', rest, re.IGNORECASE):
        flags_list = result.setdefault("flags", [])
        flags_list.append("itemcount")
        rest = re.sub(r'(?i)\bitemcount\b', '', rest).strip()

    items_found = []
    while True:
        br = br_items.search(rest)
        if not br:
            break
        inside = br.group(1).strip()
        spl = [x.strip() for x in re.split(r'[;,]', inside) if x.strip()]
        pref = [f"Base.{x}" if not x.startswith("Base.") else x for x in spl]
        items_found.extend(pref)
        rest = br_items.sub("", rest, count=1)

    if items_found:
        result["items"] = items_found
    else:
        lf = rest.strip()
        if lf:
            spl = [x.strip() for x in re.split(r'[;,]', lf) if x.strip()]
            pref = [f"Base.{x}" if not x.startswith("Base.") else x for x in spl]
            if pref:
                result["items"] = pref

    return result


def extract_block(text, start_index):
    """
    Extracts a complete block of text between braces.

    Args:
        text (str): Text to extract block from.
        start_index (int): Starting position for extraction.

    Returns:
        tuple: (block_text, end_index) where:
            - block_text: Extracted block content
            - end_index: Index after the closing brace
    """
    bracket_level = 0
    end_index = start_index
    while end_index < len(text):
        char = text[end_index]
        if char == '{':
            bracket_level += 1
        elif char == '}':
            bracket_level -= 1
            if bracket_level == 0:
                return text[start_index:end_index + 1], end_index + 1
        end_index += 1
    return text[start_index:], end_index


def parse_module_block(text):
    """
    Parses a module block definition.

    Args:
        text (str): Text containing module definition.

    Returns:
        tuple: (skin_mapping, entity_blocks) where:
            - skin_mapping: Dictionary of skin mappings
            - entity_blocks: List of entity block definitions
    """
    modules = []
    module_pattern = re.compile(r'module\s+(\w+)\s*\{', re.IGNORECASE)
    pos = 0
    while True:
        m = module_pattern.search(text, pos)
        if not m:
            break
        module_name = m.group(1)
        block, new_pos = extract_block(text, m.end() - 1)
        modules.append({"name": module_name, "block": block})
        pos = new_pos
    return modules


def parse_module_skin_mapping(module_block):
    """
    Parses skin mappings from a module block.

    Args:
        module_block (str): Module block text.

    Returns:
        dict: Dictionary of skin mappings.
    """
    mapping = {}
    skin_pattern = re.compile(r'xuiSkin\s+(\w+)\s*\{', re.IGNORECASE)
    m = skin_pattern.search(module_block)
    if m:
        skin_name = m.group(1)
        skin_block, _ = extract_block(module_block, m.end() - 1)
        entity_pattern = re.compile(r'entity\s+(\S+)\s*\{', re.IGNORECASE)
        pos = 0
        while True:
            m_entity = entity_pattern.search(skin_block, pos)
            if not m_entity:
                break
            entity_name = m_entity.group(1)
            ent_block, new_pos = extract_block(skin_block, m_entity.end() - 1)
            dn_match = re.search(r'DisplayName\s*=\s*([^,\n]+)', ent_block, re.IGNORECASE)
            icon_match = re.search(r'Icon\s*=\s*([^,\n]+)', ent_block, re.IGNORECASE)
            displayName = dn_match.group(1).strip() if dn_match else None
            icon = icon_match.group(1).strip() if icon_match else None
            mapping[entity_name] = {"DisplayName": displayName, "Icon": icon}
            pos = new_pos
    return mapping


def parse_entity_blocks(module_block, skin_mapping):
    """
    Parses entity blocks from a module block.

    Args:
        module_block (str): Module block text.
        skin_mapping (dict): Dictionary of skin mappings.

    Returns:
        list: List of parsed entity blocks.
    """
    entities = []
    entity_pattern = re.compile(r'entity\s+(\S+)\s*\{', re.IGNORECASE)
    pos = 0
    while True:
        m = entity_pattern.search(module_block, pos)
        if not m:
            break
        entity_name = m.group(1)
        entity_block, new_pos = extract_block(module_block, m.end() - 1)
        entity_data = {"name": entity_name, "components": {}}
        # Extract component blocks within the entity
        component_pattern = re.compile(r'component\s+(\S+)\s*\{', re.IGNORECASE)
        comp_pos = 0
        while True:
            m_comp = component_pattern.search(entity_block, comp_pos)
            if not m_comp:
                break
            comp_name = m_comp.group(1)
            comp_block, comp_new_pos = extract_block(entity_block, m_comp.end() - 1)
            entity_data["components"][comp_name] = comp_block
            comp_pos = comp_new_pos
        # From UiConfig, try to extract entityStyle
        if "UiConfig" in entity_data["components"]:
            ui_config_block = entity_data["components"]["UiConfig"]
            m_es = re.search(r'entityStyle\s*=\s*(\S+)', ui_config_block, re.IGNORECASE)
            if m_es:
                entity_data["entityStyle"] = m_es.group(1).strip().rstrip(',')
        entities.append(entity_data)
        pos = new_pos
    return entities


def parse_sprite_config(block_text):
    """
    Parses sprite configuration from a block.

    Args:
        block_text (str): Block containing sprite configuration.

    Returns:
        dict: Parsed sprite configuration.
    """
    sprites_by_face = {}
    skillBaseHealth = None
    m_health = re.search(r'skillBaseHealth\s*=\s*([\d\.]+)', block_text, re.IGNORECASE)
    if m_health:
        try:
            skillBaseHealth = float(m_health.group(1))
        except ValueError:
            skillBaseHealth = None

    # Find each face block
    face_pattern = re.compile(r'face\s+(\S+)\s*\{', re.IGNORECASE)
    pos = 0
    while True:
        m_face = face_pattern.search(block_text, pos)
        if not m_face:
            break
        face_direction = m_face.group(1).strip()
        face_block, new_pos = extract_block(block_text, m_face.end() - 1)
        # Find all row assignments inside this face block.
        row_matches = re.findall(r'row\s*=\s*([^,}\n]+)', face_block, re.IGNORECASE)
        sprites = []
        for row_text in row_matches:
            row_text = row_text.strip().rstrip(',')
            # Split on whitespace to separate multiple sprites in one row
            entries = row_text.split()
            for entry in entries:
                entry = entry.strip()
                if entry:
                    sprites.append(entry)
        sprites_by_face[face_direction] = sprites
        pos = new_pos

    return sprites_by_face, skillBaseHealth


def parse_construction_recipe(text):
    """
    Parses a construction recipe definition.

    Args:
        text (str): Text containing construction recipe.

    Returns:
        dict: Parsed construction recipe data.
    """
    # Remove block comments from the full text first.
    text = remove_comments(text)
    recipes = []
    modules = parse_module_block(text)
    for module in modules:
        skin_mapping = parse_module_skin_mapping(module["block"])
        entities = parse_entity_blocks(module["block"], skin_mapping)
        for entity in entities:
            if "CraftRecipe" in entity["components"]:
                recipe = {}
                recipe["name"] = entity["name"]
                # Parse the CraftRecipe component using the existing parser logic.
                craft_recipe_text = entity["components"]["CraftRecipe"]
                craft_recipe_parsed = parse_recipe_block(entity["name"], craft_recipe_text)
                recipe.update(craft_recipe_parsed)
                # Add outputs from xuiSkin using the entityStyle defined in UiConfig.
                entityStyle = entity.get("entityStyle")
                if entityStyle and entityStyle in skin_mapping:
                    mapping = skin_mapping[entityStyle]
                    recipe.setdefault("outputs", []).append({
                        "displayName": mapping.get("DisplayName"),
                        "icon": mapping.get("Icon")
                    })
                # Parse the SpriteConfig component, if it exists.
                if "SpriteConfig" in entity["components"]:
                    sprite_text = entity["components"]["SpriteConfig"]
                    face_sprites, health = parse_sprite_config(sprite_text)
                    # Instead of a flat list, store sprite outputs nested by face.
                    recipe["spriteOutputs"] = face_sprites
                    if health is not None:
                        recipe["skillBaseHealth"] = health
                # Mark this recipe as a construction recipe.
                recipe["construction"] = True
                recipes.append(recipe)
    return recipes


def main():
    """
    Main execution function for legacy recipe parsing.

    This function:
    1. Checks for existing cache
    2. If needed, parses all recipe files
    3. Processes recipe blocks and definitions
    4. Saves parsed data to cache
    5. Returns the parsed recipe data
    """
    global parsed_data

    cache_file = os.path.join(DATA_DIR, CACHE_JSON)
    # Try to get cache from json file
    parsed_data, cache_version = load_cache(cache_file, get_version=True)

    # Parse recipes if there is no cache, or it's outdated.
    if cache_version != Version.get():
        # Gather raw lines and join into one text block.
        lines = gather_recipe_lines(RECIPES_DIR)
        file_text = "".join(lines)
        # Remove all block comments from the complete text.
        file_text = remove_comments(file_text)
        # Re-split the text into lines for further processing.
        lines = file_text.splitlines(keepends=True)
        recipes = []

        # Process normal recipe blocks from the comment-free text.
        normal_recipe_blocks = extract_recipe_blocks(lines)
        for recipe_name, recipe_text in normal_recipe_blocks:
            parsed = parse_recipe_block(recipe_name, recipe_text)
            recipes.append(parsed)

        # Process construction recipes if module blocks exist.
        if "module" in file_text:
            construction_recipes = parse_construction_recipe(file_text)
            recipes.extend(construction_recipes)

        parsed_data = {"recipes": recipes}
        save_cache(parsed_data, CACHE_JSON)

    print(f'Number of recipes found: {len(parsed_data["recipes"])}')


if __name__ == "__main__":
    main()
