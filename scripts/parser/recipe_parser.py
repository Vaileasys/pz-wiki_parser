import json
import os
import re

RECIPES_DIR = "resources/scripts/recipes"
OUTPUT_JSON = "output/recipes/recipes.json"
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)


def gather_recipe_lines(directory: str):
    all_lines = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().startswith("recipes") and filename.lower().endswith(".txt"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    all_lines.extend(f.readlines())
    return all_lines


def extract_recipe_blocks(lines):
    blocks = []
    in_recipe = False
    bracket_level = 0
    current_lines = []
    current_name = None

    # Regex to detect 'craftRecipe SomeName' on a single line
    craft_recipe_pattern = re.compile(r'^\s*craftRecipe\s+(\S+)', re.IGNORECASE)

    for line in lines:
        # If we are NOT currently in a recipe, look for a new 'craftRecipe <Name>'
        if not in_recipe:
            match = craft_recipe_pattern.search(line)
            if match:
                in_recipe = True
                current_name = match.group(1).strip()
                bracket_level = 0
                current_lines = [line]

                if '{' in line:
                    bracket_level += line.count('{')
                    bracket_level -= line.count('}')
        else:
            current_lines.append(line)
            open_count = line.count('{')
            close_count = line.count('}')
            bracket_level += open_count
            bracket_level -= close_count

            if bracket_level <= 0:
                recipe_text = "".join(current_lines)
                blocks.append((current_name, recipe_text))
                in_recipe = False
                bracket_level = 0
                current_lines = []
                current_name = None

    return blocks


def parse_recipe_block(recipe_name, recipe_text):
    recipe_dict = {
        "name": recipe_name,
        "inputs": [],
        "outputs": []
    }

    mapper_pattern = re.compile(r'itemMapper\s+(\S+)\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    mappers = {}

    def mapper_replacer(match):
        mapper_name = match.group(1).strip()
        body = match.group(2).strip()
        mapper_dict = {}
        for line in body.splitlines():
            line = line.strip().rstrip(',')
            # strip out inline comments /* ... */
            line = re.sub(r'/\*.*?\*/', '', line).strip()
            if not line or line.startswith('//'):
                continue
            if '=' in line:
                left, right = line.split('=', 1)
                left = left.strip()
                right = right.strip().rstrip(',')
                mapper_dict[left] = right
        mappers[mapper_name] = mapper_dict
        return ""

    recipe_text = mapper_pattern.sub(mapper_replacer, recipe_text)

    if mappers:
        recipe_dict["itemMappers"] = mappers

    inputs_pattern = re.compile(r'inputs\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    m = inputs_pattern.search(recipe_text)
    if m:
        block_text = m.group(1)
        recipe_dict["inputs"] = parse_items_block(block_text, is_output=False)
        # remove from recipe_text
        start, end = m.span()
        recipe_text = recipe_text[:start] + recipe_text[end:]

    outputs_pattern = re.compile(r'outputs\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    m = outputs_pattern.search(recipe_text)
    if m:
        block_text = m.group(1)
        recipe_dict["outputs"] = parse_items_block(block_text, is_output=True)
        # remove from recipe_text
        start, end = m.span()
        recipe_text = recipe_text[:start] + recipe_text[end:]

    leftover_lines = recipe_text.splitlines()
    pair_pattern = re.compile(r'^\s*([\w]+)\s*=\s*(.*?)\s*$', re.IGNORECASE)
    for line in leftover_lines:
        line = re.sub(r'/\*.*?\*/', '', line).strip().rstrip(',')
        if not line or line.startswith('//'):
            continue
        m2 = pair_pattern.match(line)
        if not m2:
            continue
        key, val = m2.group(1), m2.group(2)

        # If val has semicolons => treat as list
        if ";" in val:
            splitted = [x.strip() for x in val.split(";") if x.strip()]
            recipe_dict[key] = splitted
        else:
            recipe_dict[key] = val

    return recipe_dict


def parse_items_block(block_text, is_output=False):
    results = []
    lines = re.split(r'[\r\n]+', block_text)
    for line in lines:
        line = line.strip().rstrip(',')
        if not line or line.startswith('//'):
            continue
        # fluid or item line?
        if line.lower().startswith('-fluid'):
            fluid_info = parse_fluid_line(line)
            if fluid_info:
                results.append(fluid_info)
        elif line.lower().startswith('item'):
            item_info = parse_item_line(line)
            if item_info:
                results.append(item_info)
        # else skip unknown lines
    return results

def parse_fluid_line(line):
    fluid_pattern = re.compile(r'^-fluid\s+([\d\.]+)\s+\[(.*?)\]', re.IGNORECASE)
    m = fluid_pattern.match(line)
    if not m:
        return None
    amount_str = m.group(1).strip()
    items_str = m.group(2).strip()
    splitted = re.split(r'[;,]', items_str)
    splitted = [x.strip() for x in splitted if x.strip()]
    return {
        "fluid": True,
        "amount": float(amount_str),
        "items": splitted
    }

def parse_item_line(line):
    item_pattern = re.compile(r'^item\s+(\d+)\s+(.*)$', re.IGNORECASE)
    m = item_pattern.match(line)
    if not m:
        return None
    index = int(m.group(1))
    rest = m.group(2).strip()
    result = {"index": index}

    tags_pattern   = re.compile(r'tags\[(.*?)\]', re.IGNORECASE)
    flags_pattern  = re.compile(r'flags\[(.*?)\]', re.IGNORECASE)
    bracket_items  = re.compile(r'\[(.*?)\]')
    mode_pattern   = re.compile(r'mode\s*:\s*(\S+)', re.IGNORECASE)
    mapper_pattern = re.compile(r'mapper\s*:\s*(\S+)', re.IGNORECASE)

    # mapper
    mp = mapper_pattern.search(rest)
    if mp:
        result["mapper"] = mp.group(1)
        rest = mapper_pattern.sub("", rest)

    # mode
    mo = mode_pattern.search(rest)
    if mo:
        result["mode"] = mo.group(1).capitalize()
        rest = mode_pattern.sub("", rest)

    # tags
    tg = tags_pattern.search(rest)
    if tg:
        tag_str = tg.group(1)
        splitted = re.split(r'[;,]', tag_str)
        splitted = [x.strip() for x in splitted if x.strip()]
        result["tags"] = splitted
        rest = tags_pattern.sub("", rest)

    fl = flags_pattern.search(rest)
    flags_found = []
    while True:
        fl = flags_pattern.search(rest)
        if not fl:
            break
        f_str = fl.group(1)
        splitted = re.split(r'[;,]', f_str)
        splitted = [x.strip() for x in splitted if x.strip()]
        flags_found.extend(splitted)
        # remove that occurrence
        rest = flags_pattern.sub("", rest, count=1)
    if flags_found:
        result["flags"] = flags_found

    items_found = []
    while True:
        br = bracket_items.search(rest)
        if not br:
            break
        inside = br.group(1).strip()
        splitted = re.split(r'[;,]', inside)
        splitted = [x.strip() for x in splitted if x.strip()]
        items_found.extend(splitted)
        rest = bracket_items.sub("", rest, count=1)
    if items_found:
        result["items"] = items_found
    else:
        leftover = rest.strip()
        if leftover:
            splitted = re.split(r'[;,]', leftover)
            splitted = [x.strip() for x in splitted if x.strip()]
            if splitted:
                result["items"] = splitted

    # Check for "itemcount" leftover
    if "itemcount" in rest.lower():
        flags_list = result.setdefault("flags", [])
        flags_list.append("itemcount")
        rest = re.sub(r'itemcount', '', rest, flags=re.IGNORECASE).strip()

    return result


def main():
    lines = gather_recipe_lines(RECIPES_DIR)
    recipe_blocks = extract_recipe_blocks(lines)

    recipes = []
    for recipe_name, recipe_text in recipe_blocks:
        parsed = parse_recipe_block(recipe_name, recipe_text)
        recipes.append(parsed)

    output_data = {"recipes": recipes}
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)

    print(f"{len(recipes)} recipes written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
