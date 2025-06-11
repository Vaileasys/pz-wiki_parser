import re
import copy
from tqdm import tqdm
from pathlib import Path
from scripts.core.file_loading import get_script_files, read_file
from scripts.core.language import Translate
from scripts.core.cache import save_cache, load_cache
from scripts.utils import echo
from scripts.parser.recipe_parser import parse_recipe_block, parse_construction_recipe
from scripts.core.constants import PBAR_FORMAT
from scripts.core.version import Version
from scripts.core import config_manager as config

PREFIX_BLACKLIST = {
    "item": ["MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_"]
}

COLON_SEPARATOR = ["fixing", "evolvedrecipe"]

# Available configs:
# list_keys              = Store multiple identical keys as a list. Always treated as a list.
# list_keys_semicolon    = Split the value by semicolons (`;`) into a list. Always treated as a list.
# list_keys_slash        = Split the value by slashes (`/`) into a list. Always treated as a list.
# list_keys_pipe         = Split the value by pipes (`|`) into a list. Always treated as a list.
# list_keys_space        = Split the value by spaces into a list. Always treated as a list.
# list_keys_colon        = Split the value by colons (`:`) into a list. Always treated as a list.
# dict_keys              = Store multiple identical keys as counts in a dict. Always treated as a dict.
# dict_keys_colon        = Split each entry by colon (`:`) and store as key-value pairs in a dict. Always treated as a dict.
# dict_keys_equal        = Split each entry by equals sign (`=`) and store as key-value pairs in a dict. Always treated as a dict.
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
        "list_keys_semicolon": ["specialKeyRing", "leftCol", "rightCol", "zombieType", "itemType"],
        "dict_keys_colon": ["skills"],
        "list_keys_space": ["offset", "rotate", "extents", "extentsOffset", "centerOfMassOffset", "shadowExtents", "shadowOffset", "physicsChassisShape", "xywh"]
    },
    "template": {
        "list_keys": ["template"],
        "list_keys_semicolon": ["requireInstalled", "leftCol", "rightCol", "itemType"],
        "list_keys_space": ["offset", "rotate", "extents", "extentsOffset", "centerOfMassOffset", "shadowOffset", "physicsChassisShape", "xywh", "angle"],
        "dict_keys_colon": ["skills"],
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
        # Handled through recipe_parser
        "list_keys": ["inputs"],
        "dict_keys_colon": ["AutoLearnAll", "AutoLearnAny", "xpAward", "SkillRequired"],
        "list_keys_semicolon": ["tags", "Tags", "AutoLearnAll", "AutoLearnAny"],
        "file_blacklist": [
            "dbg_entity_turbo",
            "dbg_entity_test_new_components",
            "dbg_example_recipes",
            "dbg_entity_test_resources",
            "recipes_blacksmith_TEST_RECIPES",
            "craftrecipe_testing",
            "TESTING_CapGuns",
            "entity_channels_test",
            "TESTING_items_food_fluids",
            "TESTING_Misc",
            "items_testing",
            "dbg_entity_test_new_components",
            "dbg_entity_test_resources",
            "x_entity_channels_test",
            "x_entity_test",
            "items_debug"
        ],
        "folder_blacklist": [
            "tempNotWorking"
        ]
    },
    "entity": {
        "file_blacklist": [
            "dbg_entity_turbo",
            "dbg_entity_test_new_components",
            "dbg_example_recipes",
            "dbg_entity_test_resources",
            "recipes_blacksmith_TEST_RECIPES",
            "craftrecipe_testing",
            "TESTING_CapGuns",
            "entity_channels_test",
            "TESTING_items_food_fluids",
            "TESTING_Misc",
            "items_testing",
            "dbg_entity_test_new_components",
            "dbg_entity_test_resources",
            "x_entity_channels_test",
            "x_entity_test",
            "items_debug"
        ],
        "folder_blacklist": [
            "tempNotWorking"
        ],
        # Handled through recipe_parser
        "list_keys": ["row"],
        "list_keys_space": ["row"],
        "dict_keys_colon": ["SkillRequired", "xpAward"],
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

# Cached scripts
script_cache = {}

## ------------------------- Post Processing ------------------------- ##

def inject_templates(script_dict: dict, script_type: str, template_dict: dict) -> dict:
    """Injects and merges template! and template entries into each script definition."""
    def recursive_merge(destination: dict, source: dict):
        """Recursively adds values from source into destination, without overwriting existing ones."""
        for key, value in source.items():
            if key not in destination:
                destination[key] = copy.deepcopy(value)
            elif isinstance(destination[key], dict) and isinstance(value, dict):
                recursive_merge(destination[key], value)
            else:
                dst_val = destination[key]
                if isinstance(dst_val, dict) and isinstance(value, dict):
                    recursive_merge(dst_val, value)
                else:
                    # Existing non-dict value, don't overwrite
                    pass

    def merge_template(script_data: dict, template_path: str, script_id: str, script_type: str, template_dict: dict) -> dict:
        """Merges a template into the script data."""
        module = script_id.split(".", 1)[0]

        # Handle nested paths
        if "/" in template_path:
            parts = template_path.split("/")
            base_template_id = f"{module}.{script_type}_{parts[0]}"
            base_template = template_dict.get(base_template_id)
            if not base_template:
                echo.warning(f"[{script_id}] base template '{base_template_id}' not found.")
                return script_data

            # Walk through nested templates
            current_template = base_template
            for key in parts[1:]:
                if current_template is None:
                    echo.warning(f"[{script_id}] template path '{template_path}' is incomplete at '{key}'.")
                    return script_data
                current_template = current_template.get(key)

            if current_template is None:
                echo.warning(f"[{script_id}] could not fully walk path '{template_path}'.")
                return script_data

            # Build path inside script_data
            dest = script_data
            for key in parts[1:-1]:
                if key not in dest:
                    dest[key] = {}
                elif not isinstance(dest[key], dict):
                    echo.warning(f"[{script_id}] expected dict at '{key}' but found {type(dest[key])}.")
                    return script_data
                dest = dest[key]

            # Add or merge final key
            final_key = parts[-1]
            if final_key not in dest:
                dest[final_key] = copy.deepcopy(current_template)
            else:
                if isinstance(dest[final_key], dict) and isinstance(current_template, dict):
                    recursive_merge(dest[final_key], current_template)
            
            # Handle wildcard inheritance, e.g., Seat* → SeatFrontLeft
            if len(parts) >= 2 and parts[1] == "part":
                part_name = final_key
                template_group = parts[0]
                base_template_id = f"{module}.{script_type}_{template_group}"
                base_template = template_dict.get(base_template_id)

                if base_template:
                    part_block = base_template.get("part", {})
                    for wildcard, wildcard_data in part_block.items():
                        if "*" in wildcard and isinstance(wildcard_data, dict):
                            prefix = wildcard.rstrip("*")
                            if part_name.startswith(prefix):
                                if isinstance(dest[part_name], dict):
                                    recursive_merge(dest[part_name], wildcard_data)

        else:
            # Merge full template
            template_id = f"{module}.{script_type}_{template_path}"
            template = template_dict.get(template_id)
            if not template:
                echo.warning(f"[{script_id}] template '{template_id}' not found.")
                return script_data

            # Merge sub-templates recursively
            sub_template_list = template.get("template")
            if sub_template_list:
                for sub_temp in sub_template_list:
                    script_data = merge_template(script_data, sub_temp, script_id, script_type, template_dict)

            # Merge fields into script_data
            for key, value in template.items():
                if key in ("ScriptType", "SourceFile", "template"):
                    continue
                if key not in script_data:
                    script_data[key] = copy.deepcopy(value)
                else:
                    if isinstance(script_data[key], list) and isinstance(value, list):
                        script_data[key] = list(dict.fromkeys(script_data[key] + value))
                    elif isinstance(script_data[key], dict) and isinstance(value, dict):
                        recursive_merge(script_data[key], value)

        return script_data

    updated_dict = {}

    for script_id, script_data in script_dict.items():
        # Inject and merge template! into vehicle data
        template_name = script_data.get("template!")
        if template_name:
            script_data = merge_template(script_data, template_name, script_id, script_type, template_dict)

        # Inject and merge 'template'
        template_list = list(script_data.get("template", []))
        for temp in template_list:
            script_data = merge_template(script_data, temp, script_id, script_type, template_dict)

        # Remove templates
        script_data.pop("template!", None)
        script_data.pop("template", None)

        updated_dict[script_id] = script_data

    return updated_dict

def post_process(script_dict: dict, script_type: str):
    """Applies post-processing logic based on script type."""
    # Inject template! into data
    if script_type == "vehicle":
        template_dict = extract_script_data("template")
        script_dict = inject_templates(script_dict, script_type, template_dict)

    return script_dict

## ------------------------- Split Handlers ------------------------- ##
def split_list(value: str, character: str) -> list:
    """Splits by a specific character and normalises as a list"""
    return [normalise(v) for v in value.strip().split(character) if v.strip()]

def split_dict(value: list[str], character: str) -> dict:
    """Splits at a specific character and normalises as a dict."""
    result = {}
    for entry in value:
        entry = entry.strip()
        if not entry:
            continue
        if character in entry:
            key, val = entry.split(character, 1)
            key = normalise(key)
            if key == "":
                continue
            result[key] = normalise(val)
        else:
            key = normalise(entry)
            if key == "":
                continue
            result[key] = True
    return result

def split_pipe_list(value: str) -> list:
    """Splits at pipes `|` and normalises as a list."""
    return split_list(value, "|")

def split_slash_list(value: str) -> list:
    """Splits at slashes `/` and normalises as a list."""
    return split_list(value, "/")

def split_space_list(value: str) -> list:
    """Splits at spaces ` ` and normalises as a list."""
    return split_list(value, " ")

def split_semicolon_list(value: str) -> list:
    """Splits at semicolons `;` and normalises as a list."""
    return split_list(value, ";")

def split_colon_list(value: str) -> list:
    """Splits at colons `:` and normalises as a list."""
    return split_list(value, ":")

def split_colon_dict(value: list[str]) -> dict:
    """Splits at colons `:` and normalises as a dict."""
    return split_dict(value, ":")

def split_equal_dict(value: list[str]) -> dict:
    """Splits at equals `=` and normalises as a dict."""
    return split_dict(value, "=")

def split_space_dict(value: list[str]) -> dict:
    """Splits at spaces ` ` and normalises as a dict."""
    return split_dict(value, " ")


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
            echo.warning(f"[{block_id}] No ':' in 'EvolvedRecipe' value: {value}")
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
            echo.warning(f"[{block_id}] Invalid skill entry in Fixer: '{entry}'")

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
            echo.warning(f"[{block_id}] Malformed itemMapper line: '{line}'")
            continue

        output, input_ = match.groups()
        input_ = normalise(input_)
        output = normalise(output)

        # Reverse the key-value to be: 'input: output'
        if input_ in mapper:
            echo.warning(f"[{block_id}] Duplicate input '{input_}' in itemMapper: already mapped to '{mapper[input_]}'")
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

    # Ensure we return as a list when required
    list_keys_combined = (
        list_keys
        | list_keys_semicolon
        | list_keys_pipe
        | list_keys_space
        | list_keys_slash
        | list_keys_colon
    )
    if key_lower in list_keys_combined:
        return parts

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
    Strip // single‑line comments and nested /* … */ block comments.

    Parameters:
    lines : list[str]
        Raw lines read from a text file.

    Returns
    list[str]
        Lines with comments removed; blank lines are dropped.
    """
    cleaned_lines: list[str] = []
    block_depth = 0

    for raw_line in lines:
        char_pos = 0
        output_chars: list[str] = []

        while char_pos < len(raw_line):
            # Single line comments
            if block_depth == 0 and raw_line[char_pos : char_pos + 2] == "//":
                break

            # Multi line comments (nesting supported)
            if raw_line[char_pos : char_pos + 2] == "/*":
                block_depth += 1
                char_pos += 2
                continue
            if block_depth and raw_line[char_pos : char_pos + 2] == "*/":
                block_depth -= 1
                char_pos += 2
                continue

            if block_depth == 0:
                output_chars.append(raw_line[char_pos])

            char_pos += 1

        stripped_line = "".join(output_chars).strip()
        if stripped_line and block_depth == 0:
            cleaned_lines.append(stripped_line)

    return cleaned_lines


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
    match = re.match(r'^([^\s:=]+)\s*[:=]\s*(.+)', line)
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
                    echo.warning(f"[{block_id}] Duplicate subkey '{k}' in '{key}' with different value: '{v}' – existing: '{existing[k]}'")

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
            echo.warning(f"[{block_id}] Duplicate key '{key}'. Replacing '{existing}' with '{processed}'")
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

            # Assign a separator based on the script type
            separator = r':' if script_type in COLON_SEPARATOR else r'='

            # Special case for 'itemMapper' block type
            if block_type == "itemMapper":
                block_data = parse_item_mapper(stripped_block_lines, block_id)
            # Determine whether to parse this block recursively (nested structure or key-value pairs)
            elif has_nested_block or any(re.search(separator, ln) for ln in stripped_block_lines):
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


def is_blacklisted(filepath: str, script_type: str) -> bool:
    """
    Check if a file should be blacklisted based on file and folder blacklists.
    
    Args:
        filepath (str): Path to the file to check
        script_type (str): Type of script being parsed
        
    Returns:
        bool: True if file should be blacklisted, False otherwise
    """
    path = Path(filepath)
    config = SCRIPT_CONFIGS.get(script_type, {})
    
    # Check file blacklist
    if path.stem in config.get("file_blacklist", []):
        echo.info(f"Skipping blacklisted file: '{path.stem}'")
        return True
        
    # Check folder blacklist
    for folder in config.get("folder_blacklist", []):
        if folder in str(path):
            echo.info(f"Skipping file in blacklisted folder '{folder}': '{path.stem}'")
            return True
            
    return False


def check_cache_version(script_type: str):
    cached_data, cached_version = load_cache(f"parsed_{script_type}_data.json", f"{script_type}", get_version=True)
    if cached_version == Version.get():
        return cached_data
    return {}


def extract_script_data(script_type: str, do_post_processing: bool = True, cache_result: bool = True, use_cache = True) -> dict[str, dict]:
    """
    Parses all script files of a given script type, extracting blocks into dictionaries keyed by FullType (i.e. [Module].[Type])

    Args:
        script_type (str): Type of script to extract (e.g., "item", "vehicle").
        prefix (str): Required prefix of the block type (e.g., "vehicle_").

    Returns:
        dict[str, dict]: A dictionary of parsed script blocks keyed by full ID (FullType).
    """
    global script_cache

    # Clear memory cache
    if not use_cache or config.get_debug_mode():
        script_cache = {}
    
    # Get script_type from cache if it's already been parsed.
    if script_type in script_cache:
        return script_cache[script_type]
    
    # Try load from disk cache if not debug mode
    if use_cache and not config.get_debug_mode():
        # Try to load cache from local storage
        saved_cache_data = check_cache_version(script_type)
        if saved_cache_data:
            script_cache[script_type] = saved_cache_data # Cache in memory for next run
            return saved_cache_data

    script_dict = {}
    entity_dict = {} # special case for entity
    script_files = get_script_files()

    if not script_files:
        echo.warning("No script files found.")

    with tqdm(total=len(script_files), desc=f"Parsing {script_type} files", unit=" files", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        for filepath in script_files:
            pbar.set_postfix_str(f"Parsing: '{Path(filepath).stem[:30]}'")

            # Check if file should be blacklisted
            if is_blacklisted(filepath, script_type):
                continue

            content = read_file(filepath)
            if not content:
                echo.warning(f"File is empty or unreadable: {filepath}")
                continue

            if script_type == "entity":
                file_texts: dict[str, str] = {}
                for filepath in script_files:
                    # Check if file should be blacklisted
                    if is_blacklisted(filepath, script_type):
                        continue

                    text = read_file(filepath)
                    if not text:
                        echo.warning(f"File is empty or unreadable: {filepath}")
                        continue

                    file_texts[filepath] = text

                if not file_texts:
                    echo.warning("No entity files found.")
                    return {}

                full_text = "\n".join(file_texts.values())
                recipes = parse_construction_recipe(full_text)

                entity_dict = {}
                for recipe in recipes:
                    name = recipe.get("name")
                    if not name:
                        continue

                    # Best‑effort: find which file contains the entity definition
                    source_file = next(
                        (Path(p).stem for p, t in file_texts.items()
                        if re.search(rf'\bentity\s+{re.escape(name)}\b', t)),
                        "unknown"
                    )

                    recipe["ScriptType"] = script_type
                    recipe["SourceFile"] = source_file
                    entity_dict[name] = recipe

                save_cache(entity_dict, "parsed_entity_data.json")
                script_cache[script_type] = entity_dict
                echo.success(f"Parsed {len(entity_dict)} entity entries.")
                return dict(sorted(entity_dict.items()))

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

                        if script_type == "craftRecipe":
                            current_id = block_name

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

                        # Recursively parse the block and attach data, handle custom if required
                        cleaned = remove_comments(block_lines)
                        if script_type == "craftRecipe":
                            block_data = parse_recipe_block(cleaned, current_id)
                        else:
                            block_data = parse_block(cleaned, current_id, script_type)

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
            
            pbar.update(1)
    
    if do_post_processing:
        script_dict = post_process(script_dict, script_type)

    if not script_dict:
        echo.warning("No valid script entries were found.")
    else:
        echo.success(f"Parsed {len(script_dict)} {script_type} entries.")

    if cache_result:
        # Cache dict in memory
        script_cache[script_type] = script_dict

        # Special case for storing both types of entity data
        if script_type == "entity":
            save_cache(entity_dict, f"parsed_{script_type}_data.json")
            save_cache(script_dict, f"parsed_{script_type}_old_data.json")
        else:
            save_cache(script_dict, f"parsed_{script_type}_data.json")

    return dict(sorted(script_dict.items()))


def main():
    menu = {
        "1": {"script_type": "item", "desc": "Game items like tools, food, and materials."},
        "2": {"script_type": "fluid", "desc": "Liquids, like water or fuel."},
        "3": {"script_type": "vehicle", "desc": "Vehicles and their properties."},
        "4": {"script_type": "template", "desc": "Vehicles and their properties."},
        "5": {"script_type": "evolvedrecipe", "desc": "Recipes that enhance food items with optional ingredients."},
        "6": {"script_type": "uniquerecipe", "desc": "Special one-off recipes with fixed inputs and results."},
        "7": {"script_type": "craftRecipe", "desc": "Standard crafting recipes for items and upgrades. [uses recipe_parser]"},
        "8": {"script_type": "entity", "desc": "World objects with buildable or interactive components. [uses recipe_parser]"},
        "9": {"script_type": "energy", "desc": "Energy effects like visual charges or particle trails."},
        "10": {"script_type": "multistagebuild", "desc": "Construction stages for buildable structures."},
        "11": {"script_type": "model", "desc": "3D model definitions for in-game rendering."},
        "12": {"script_type": "animation", "desc": "Animation sequences and frame data for characters or items."},
        "13": {"script_type": "animationsMesh", "desc": "Mesh overlays tied to animations, such as effects or shadows."},
        "14": {"script_type": "mannequin", "desc": "Definitions for mannequin poses and appearances."},
        "15": {"script_type": "timedAction", "desc": "Timed gameplay actions like crafting or using items."},
        "16": {"script_type": "physicsHitReaction", "desc": "Physical reactions to hits."},
        "17": {"script_type": "ragdoll", "desc": "Physics constraints for ragdoll body parts."},
        "18": {"script_type": "sound", "desc": "Sound event triggers and configurations."},
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

        echo.info(f"Processing '{script_type}'...")

        extract_script_data(script_type)

if __name__ == "__main__":
    main()
