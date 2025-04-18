import re
from pathlib import Path
from core.file_loading import get_script_files, read_file
from scripts.core.language import Translate
from scripts.core.cache import save_cache
from scripts.utils.echo import echo, echo_info, echo_warning, echo_error, echo_success

PREFIX_BLACKLIST = {
    "item": ["MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_"]
}

# Available configs:
# list_keys              = Store multiple identical keys as a list. Always treated as a list.
# list_keys_semicolon    = Split the value by semicolons (;) into a list. Always treated as a list.
# list_keys_slash        = Split the value by slashes (/) into a list. Always treated as a list.
# list_keys_pipe         = Split the value by pipes (|) into a list. Always treated as a list.
# list_keys_space        = Split the value by spaces into a list. Always treated as a list.
# list_keys_colon        = Split the value by colons (:) into a list. Always treated as a list.
# dict_keys              = Store multiple identical keys as counts in a dict. Always treated as a dict.
# dict_keys_colon        = Split each entry by colon (:) and store as key-value pairs in a dict. Always treated as a dict.
# dict_keys_equal        = Split each entry by equals sign (=) and store as key-value pairs in a dict. Always treated as a dict.
# dict_keys_space        = Split each entry by the first space and store as key-value pairs in a dict. Always treated as a dict.
SCRIPT_CONFIGS = {
    "item": {
        "list_keys": [
            "SoundMap", "fluid", "ModelWeaponPart", "Tags", "Categories", "ClothingItemExtra", "ClothingItemExtraOption", "ResearchableRecipes",
            "StaticModelsByIndex", "WorldStaticModelsByIndex", "WeaponSpritesByIndex", "MountOn", "AttachmentsProvided"
        ],
        "list_keys_semicolon": ["Tags", "ResearchableRecipes", "IconsForTexture", "StaticModelsByIndex", "WorldStaticModelsByIndex", "ClothingItemExtra",
            "ClothingItemExtraOption", "BloodLocation", "AttachmentsProvided", "TeachedRecipes", "Categories", "StaticModel", "WeaponSpritesByIndex","MountOn"
        ],
        "list_keys_slash": ["RequireInHandOrInventory", "FireModePossibilities"],
        "dict_keys_space": ["SoundMap"]
    },
    "vehicle": {
        "list_keys": ["template"],
        "list_keys_semicolon": ["specialKeyRing", "leftCol", "rightCol", "zombieType"],
        "dict_keys_colon": ["skills"],
        "list_keys_space": ["offset", "rotate", "extents", "extentsOffset", "centerOfMassOffset", "shadowExtents", "shadowOffset", "physicsChassisShape", "xywh"]
    },
    "template": {
        "list_keys_semicolon": ["requireInstalled", "leftCol", "rightCol", "itemType"],
        "list_keys_space": ["offset", "rotate", "extents", "centerOfMassOffset", "shadowOffset", "physicsChassisShape", "xywh"],
        "dict_keys_colon": ["skills"],
    },
    "entity": {
        # Not fully supported
        "list_keys": ["row"],
        "list_keys_space": ["row"],
        "dict_keys_colon": ["SkillRequired", "xpAward"],
    },
    "model": {
        "list_keys": [],
        "list_keys_space": ["offset", "rotate"]
    },
    "fixing": {
        "list_keys_semicolon": ["Require"],
        "dict_keys_equal": ["GlobalItem"],
    },
    "craftRecipe": {
        # Not fully supported
        "dict_keys_colon": ["AutoLearnAll", "AutoLearnAny", "xpAward", "SkillRequired"],
        "list_keys_semicolon": ["tags", "Tags", "AutoLearnAll", "AutoLearnAny"]
    },
    "uniquerecipe": {
        "dict_keys": ["Item"],
    },
    "energy": {
        "list_keys_colon": ["Color"],
    },
    "multistagebuild": {
        "dict_keys_equal": ["ItemsRequired", "SkillRequired", "XP"],
        "list_keys_semicolon": ["ItemsRequired", "PreviousStage"],
    },
    "animationsMesh": {
        "list_keys": ["animationDirectory"]
    },
    "timedAction": {
        "list_keys_semicolon": ["muscleStrainParts"]
    },
    "ragdoll": {
        "list_keys_space": ["constraintAxisA", "constraintAxisB", "constraintPositionOffsetA", "constraintPositionOffsetB", "constraintLimit"]
    }
}


## ------------------------- Split Handlers ------------------------- ##
def split_pipe_list(value: str) -> list:
    """Splits at pipes '|' and normalises as a list."""
    return [normalise(v) for v in value.split('|') if v.strip()]

def split_slash_list(value: str) -> list:
    """Splits at slashes '/' and normalises as a list."""
    return [normalise(v) for v in value.split('/') if v.strip()]

def split_space_list(value: str) -> list:
    """Splits at spaces ' ' and normalises as a list."""
    return [normalise(v) for v in value.strip().split() if v.strip()]

def split_semicolon_list(value: str) -> list:
    """Splits at semicolons ';' and normalises as a list."""
    return [normalise(v) for v in value.split(';') if v.strip()]

def split_colon_list(value: str) -> list:
    """Splits at colons ':' and normalises as a list."""
    return [normalise(v) for v in value.split(':') if v.strip()]

def split_colon_dict(value: list[str]) -> dict:
    """Splits at colons ':' and normalises as a dict."""
    result = {}
    for entry in value:
        if ':' in entry:
            key, val = entry.split(':', 1)
            result[normalise(key)] = normalise(val)
        else:
            result[normalise(entry)] = True
    return result

def split_equal_dict(value: list[str]) -> dict:
    """Splits at equals '=' and normalises as a dict."""
    result = {}
    for entry in value:
        if '=' in entry:
            key, val = entry.split('=', 1)
            result[normalise(key)] = normalise(val)
        else:
            result[normalise(entry)] = True
    return result

def split_space_dict(value: list[str]) -> dict:
    """Splits at spaces ' ' and normalises as a dict."""
    result = {}
    for entry in value:
        if ' ' in entry:
            key, val = entry.split(' ', 1)
            result[normalise(key)] = normalise(val)
        else:
            result[normalise(entry)] = True
    return result


## ------------------------- Special Cases ------------------------- ##

def parse_evolved_recipe(value: str, block_id: str = "Unknown") -> dict:
    """Special case for processing values of 'EvolvedRecipe'."""
    result = {}
    entries = value.split(';')

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        is_cooked = False
        if '|' in entry:
            entry, modifier = entry.split('|', 1)
            if modifier.strip().lower() == "cooked":
                is_cooked = True

        if ':' not in entry:
            echo_warning(f"[{block_id}] No ':' in 'EvolvedRecipe' value: {value}")
            continue

        name, amount = entry.split(':', 1)
        result[normalise(name)] = [normalise(amount), is_cooked]

    return result

def parse_fluid(value: str, block_id: str = "Unknown") -> list[list]:
    """Special case for processing values of 'fluid'."""
    result = []
    entries = split_semicolon_list(value)

    for entry in entries:
        if not entry:
            continue
        parts = [normalise(p) for p in entry.split(':') if p.strip()]
        if len(parts) >= 2:
            result.append(parts)
        else:
            result.append([entry])
    return result

def parse_fixer(value: str, block_id: str = "Unknown") -> dict:
    """Special case for processing values of 'fixer'."""
    fixer_data = {}

    entries = split_semicolon_list(value)
    if not entries:
        return fixer_data

    item_entry = entries[0]
    if '=' in item_entry:
        item_name, item_amount = item_entry.split('=', 1)
        item_name = normalise(item_name)
        item_amount = normalise(item_amount)
    else:
        item_name = normalise(item_entry)
        item_amount = 1

    skill_dict = {}
    for entry in entries[1:]:
        if '=' in entry:
            skill, level = entry.split('=', 1)
            skill_dict[normalise(skill)] = normalise(level)
        else:
            echo_warning(f"[{block_id}] Invalid skill entry in Fixer: '{entry}'")

    fixer_data[item_name] = {
        "Amount": item_amount,
        "Skill": skill_dict
    }

    return fixer_data

def parse_item_mapper(lines: list[str], block_id: str = "Unknown") -> dict:
    """Special case for processing values of 'itemMapper'."""
    mapper = {}

    for line in lines:
        line = line.strip().rstrip(',')
        if not line or line == "}":
            continue

        match = re.match(r'^([\w\.]+)\s*=\s*([\w\.]+)', line)
        if not match:
            echo_warning(f"[{block_id}] Malformed itemMapper line: '{line}'")
            continue

        output, input_ = match.groups()
        input_ = normalise(input_)
        output = normalise(output)

        # Reverse the key-value to be: 'input: output'
        if input_ in mapper:
            echo_warning(f"[{block_id}] Duplicate input '{input_}' in itemMapper: already mapped to '{mapper[input_]}'")
        mapper[input_] = output

    return mapper


## ------------------------- Process Values ------------------------- ##

def process_value(key: str, value: str, block_id: str = "Unknown", script_type: str = "") -> str | list | dict:
    """
    Processes a raw value string into its appropriate type based on key and script type rules.
    Applies special handling for known keys and uses config-based rules to convert values into lists or dictionaries based on separators.

    Args:
        key (str): The key associated with the value (e.g., "Tags", "EvolvedRecipe").
        value (str): The raw string value to be processed.
        block_id (str, optional): Identifier for the current script block, used in warnings. Defaults to "Unknown".
        script_type (str, optional): Type of script being parsed (e.g., "item", "fixing"). Determines which rules apply.

    Returns:
        str | list | dict: The processed value, cast into a normalised format (e.g., list, dict, or scalar).
    """
    config = SCRIPT_CONFIGS.get(script_type, {})

    key_lower = key.lower()

    # Initialise configs
    list_keys = {k.lower() for k in config.get("list_keys", [])}
    list_keys_semicolon = {k.lower() for k in config.get("list_keys_semicolon", [])}
    list_keys_colon = {k.lower() for k in config.get("list_keys_colon", [])}
    list_keys_pipe = {k.lower() for k in config.get("list_keys_pipe", [])}
    list_keys_space = {k.lower() for k in config.get("list_keys_space", [])}
    list_keys_slash = {k.lower() for k in config.get("list_keys_slash", [])}
    dict_keys = {k.lower() for k in config.get("dict_keys", [])}
    dict_keys_colon = {k.lower() for k in config.get("dict_keys_colon", [])}
    dict_keys_equal = {k.lower() for k in config.get("dict_keys_equal", [])}
    dict_keys_space = {k.lower() for k in config.get("dict_keys_space", [])}

    parts = [value]

    # Process values based on configs and special cases
    if key_lower == "evolvedrecipe" and script_type == "item":
        return parse_evolved_recipe(value, block_id)
    elif key_lower == "displayname" and script_type == "item":
        value = Translate.get(block_id, "DisplayName", "en", value)
        return value
    elif key_lower == "fluid" and script_type in ("item", "entity"):
        return parse_fluid(value, block_id)
    elif key_lower == "fixer" and script_type == "fixing":
        return parse_fixer(value, block_id)
    elif key_lower in list_keys_semicolon:
        parts = split_semicolon_list(value)
    elif key_lower in list_keys_colon:
        parts = split_colon_list(value)
    elif key_lower in list_keys_pipe:
        parts = split_pipe_list(value)
    elif key_lower in list_keys_slash:
        parts = split_slash_list(value)
    elif key_lower in list_keys_space:
        parts = split_space_list(value)
    else:
        parts = [normalise(value)]

    # If it should be a dict (e.g., colon-separated pairs)
    if key_lower in dict_keys_colon:
        return split_colon_dict(parts)
    if key_lower in dict_keys_equal:
        return split_equal_dict(parts)
    if key_lower in dict_keys_space:
        return split_space_dict(parts)

    # Ensure list if required
    if key_lower in list_keys:
        return parts
    # Ensure dict if required, adding duplicates
    if key_lower in dict_keys:
        count_dict = {}
        for entry in parts:
            count_dict[entry] = count_dict.get(entry, 0) + 1
        return count_dict

    # Fallback
    return parts[0] if len(parts) == 1 else parts


def normalise(value: str) -> str | int | float | bool:
    """
    Convert a string to its type: int, float, bool, or str.

    Args:
        value (str): The input string to normalise.

    Returns:
        str | int | float | bool: The value converted to its appropriate type.
    """
    value = value.strip().rstrip(',')
    lower = value.lower()

    if lower in ("true", "false"):
        return lower == "true"

    # Java-style float suffix
    if value.lower().endswith('f'):
        stripped = value[:-1]
        try:
            return float(stripped)
        except ValueError:
            pass

    try:
        return float(value) if '.' in value else int(value)
    except ValueError:
        return value


## ------------------------- Core Parser ------------------------- ##

def remove_comments(lines: list[str]) -> list[str]:
    """
    Remove single-line and multi-line comments from a list of lines.

    Args:
        lines (list[str]): Raw lines from a script file.

    Returns:
        list[str]: Cleaned lines with comments removed.
    """
    clean_lines = []
    in_multiline_comment = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Handle multi-line comments
        if in_multiline_comment:
            if "*/" in line:
                _, after = line.split("*/", 1)
                line = after.strip()
                in_multiline_comment = False
            else:
                continue

        # Inline block comments
        while "/*" in line and "*/" in line:
            pre, rest = line.split("/*", 1)
            _, post = rest.split("*/", 1)
            line = (pre + post).strip()

        # Start multi-line comment
        if "/*" in line:
            line, _ = line.split("/*", 1)
            line = line.strip()
            in_multiline_comment = True

        # Inline line comments
        if "//" in line:
            line, _ = line.split("//", 1)
            line = line.strip()

        if line:
            clean_lines.append(line)

    return clean_lines
        

def parse_key_value_line(line: str, data: dict, block_id: str = "Unknown", script_type: str = "") -> None:
    """
    Parses a single key-value line and inserts or merges it into the provided data dictionary.
    Supports both '=' and ':' as separators, applies script-type-specific processing rules, and handles merging of values, lists, and nested dictionaries.

    Args:
        line (str): The script line containing a key-value pair.
        data (dict): The dictionary to update with the parsed key and value.
        block_id (str, optional): Identifier for the current script block, used for warnings. Defaults to "Unknown".
        script_type (str, optional): Type of script being parsed (e.g., "item", "vehicle"). Used to apply config rules.

    Returns:
        None
    """
    match = re.match(r'^(\w+)\s*[:=]\s*(.+)', line)
    if not match:
        return

    key, value = match.groups()
    key = key.strip()
    value = value.strip().rstrip(',')

    # Always process the value using the config rules
    processed = process_value(key, value, block_id, script_type)

    if key in data:
        existing = data[key]

        # Merge if this key is defined as a dict accumulator (e.g., for counts)
        if key in SCRIPT_CONFIGS.get(script_type, {}).get("dict_keys", []):
            if isinstance(existing, dict) and isinstance(processed, dict):
                for k, v in processed.items():
                    existing[k] = existing.get(k, 0) + v
            return

        # Merge if both existing and new value are dicts (e.g., SoundMap)
        if isinstance(existing, dict) and isinstance(processed, dict):
            for k, v in processed.items():
                if k not in existing:
                    existing[k] = v
                elif existing[k] != v:
                    echo_warning(f"[{block_id}] Duplicate subkey '{k}' in '{key}' with different value: '{v}' – existing: '{existing[k]}'")

        # Merge list-style values
        elif isinstance(existing, list):
            if isinstance(processed, list):
                for v in processed:
                    if v not in existing:
                        existing.append(v)
            else:
                if processed not in existing:
                    existing.append(processed)

        # Conflict between single values
        elif existing != processed:
            echo_warning(f"[{block_id}] Duplicate key '{key}'. Replacing '{existing}' with '{processed}'")
            data[key] = processed

    else:
        data[key] = processed


def parse_block(lines: list[str], block_id: str = "Unknown", script_type: str = "") -> dict:
    """
    Parse a block of script lines into a nested dictionary.

    Args:
        lines (list[str]): Block of script lines.
        block_id (str, optional): Identifier for this block. Defaults to "Unknown".
        script_type (str, optional): Script type to apply correct parsing rules. Defaults to "".

    Returns:
        dict: Parsed block as a structured dictionary.
    """
    def is_nested_block_start(lines: list[str]) -> bool:
        """Checks if any line is followed by '{', indicating a nested block."""
        for i in range(len(lines) - 1):
            line = lines[i].strip()
            next_line = lines[i + 1].strip()
            if re.match(r'^\w+(?:\s+[\w*/@]+)?$', line) and next_line == "{":
                return True
        return False

    data = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        block_match = re.match(r'^(\w+)(?:\s+([\w*/]+))?$', line)
        # Check if this line starts a new nested block
        if block_match and i + 1 < len(lines) and lines[i + 1].strip() == "{":
            block_type, block_name = block_match.groups()
            i += 2
            block_lines = []
            block_depth = 1

            while i < len(lines):
                next_line = lines[i].strip()
                block_depth += next_line.count("{")
                block_depth -= next_line.count("}")
                block_lines.append(next_line)
                i += 1
                if block_depth <= 0:
                    break

            stripped_block_lines = remove_comments(block_lines)

            has_nested_block = is_nested_block_start(stripped_block_lines)

            # Special case for 'itemMapper' block type
            if block_type == "itemMapper":
                block_data = parse_item_mapper(stripped_block_lines, block_id)
            # Determine whether to parse this block recursively (nested structure or key-value pairs)
            elif has_nested_block or any(re.search(r'[:=]', ln) for ln in stripped_block_lines):
                block_data = parse_block(stripped_block_lines, block_id, script_type)
            else:
                block_data = [normalise(ln) for ln in stripped_block_lines if ln != "}"]

            if block_name:
                data.setdefault(block_type, {})[block_name] = block_data
            else:
                data[block_type] = block_data
        else:
            parse_key_value_line(line, data, block_id, script_type)
            i += 1

    return data


def extract_script_data(script_type: str) -> dict[str, dict]:
    """
    Parses all script files of a given script type, extracting blocks into dictionaries keyed by FullType (i.e. [Module].[Type])

    Args:
        script_type (str): Type of script to extract (e.g., "item", "vehicle").
        prefix (str): Required prefix of the block type (e.g., "vehicle_").

    Returns:
        dict[str, dict]: A dictionary of parsed script blocks keyed by full ID (FullType).
    """
    script_dict = {}
    script_files = get_script_files()

    if not script_files:
        echo_warning("No script files found.")

    for filepath in script_files:
        content = read_file(filepath)
        if not content:
            echo_warning(f"File is empty or unreadable: {filepath}")
            continue
        
        # Clean up comments and prep for parsing
        lines = remove_comments(content.splitlines())
        module = None
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Get the module name (e.g., 'module Base')
            if match := re.match(r'^module\s+(\w+)', line):
                module = match.group(1)
                i += 1
                continue

            # Detect block start (e.g., 'item Axe {')
            block_match = re.match(r'^(\w+)\s+(.+)', line)
            if block_match and i + 1 < len(lines) and lines[i + 1].strip() == "{":
                block_type, block_name = block_match.groups()
                if block_name is not None:
                    block_name = block_name.replace(" ", "_")

                # Skip blacklisted prefixes (e.g., 'MakeUp_' for items)
                blacklist = PREFIX_BLACKLIST.get(script_type, [])
                if block_type == script_type and module and not any(block_name.startswith(prefix) for prefix in blacklist):
                    current_id = f"{module}.{block_name}"
#                    echo_info(f"Parsing {script_type}: {current_id}")

                    # Extract lines inside this block, between curly brackets
                    i += 2
                    block_lines = []
                    block_depth = 1

                    while i < len(lines):
                        next_line = lines[i].strip()
                        block_depth += next_line.count("{")
                        block_depth -= next_line.count("}")
                        block_lines.append(next_line)
                        i += 1
                        if block_depth <= 0:
                            break
                    
                    # Recursively parse the block and attach data
                    block_data = parse_block(remove_comments(block_lines), current_id, script_type)
#                    block_data = post_process_data(block_data, script_type)
                    block_data["ScriptType"] = script_type
                    block_data["SourceFile"] = Path(filepath).stem
                    script_dict[current_id] = block_data
                else:
                    # Skip unknown or irrelevant blocks
                    i += 2
                    skip_depth = 1
                    while i < len(lines) and skip_depth > 0:
                        next_line = lines[i].strip()
                        skip_depth += next_line.count("{")
                        skip_depth -= next_line.count("}")
                        i += 1
                continue

            i += 1

    if not script_dict:
        echo_warning("No valid script entries were found.")
    else:
        echo_success(f"Parsed {len(script_dict)} {script_type} entries.")

    save_cache(script_dict, f"{script_type}_data.json")
    return dict(sorted(script_dict.items()))


def main():
    menu = {
        "1": {"script_type": "item", "desc": "Game items like tools, food, and materials."},
        "2": {"script_type": "fluid", "desc": "Liquids, like water or fuel."},
        "3": {"script_type": "vehicle", "desc": "Vehicles and their properties."},
        "4": {"script_type": "evolvedrecipe", "desc": "Recipes that enhance food items with optional ingredients."},
        "5": {"script_type": "uniquerecipe", "desc": "Special one-off recipes with fixed inputs and results."},
        "6": {"script_type": "craftRecipe", "desc": "Standard crafting recipes for items and upgrades. [not fully supported]"},
        "7": {"script_type": "entity", "desc": "World objects with buildable or interactive components. [not fully supported]"},
        "8": {"script_type": "energy", "desc": "Energy effects like visual charges or particle trails."},
        "9": {"script_type": "multistagebuild", "desc": "Construction stages for buildable structures."},
        "10": {"script_type": "model", "desc": "3D model definitions for in-game rendering."},
        "11": {"script_type": "animation", "desc": "Animation sequences and frame data for characters or items."},
        "12": {"script_type": "animationsMesh", "desc": "Mesh overlays tied to animations, such as effects or shadows."},
        "13": {"script_type": "mannequin", "desc": "Definitions for mannequin poses and appearances."},
        "14": {"script_type": "timedAction", "desc": "Timed gameplay actions like crafting or using items."},
        "15": {"script_type": "physicsHitReaction", "desc": "Physical reactions to hits."},
        "16": {"script_type": "ragdoll", "desc": "Physics constraints for ragdoll body parts."},
        "17": {"script_type": "sound", "desc": "Sound event triggers and configurations."},
    }

    while True:
        for key, value in menu.items():
            print(f"{key}: {value.get('script_type')} - {value.get('desc')}")
        print("Q: Quit")
        option = input("Enter a script type or select an option.\n> ")

        if option in menu:
            script_type = menu[option]["script_type"]
        elif option.lower() == "q":
            break
        else:
            script_type = option

        print(f"Processing '{script_type}'...")

        extract_script_data(script_type)

if __name__ == "__main__":
    main()
