import os
import re
from scripts.core.language import Language, Translate
from scripts.core.version import Version
from scripts.core.constants import DATA_DIR
from scripts.utils.echo import echo_info, echo_warning
from scripts.core.cache import save_cache, load_cache
from scripts.core.file_loading import get_script_files

RESOURCE_PATH = os.path.join("resources", "scripts")
CACHE_JSON = 'item_data.json'

# Blacklisted item name prefixes
blacklist_prefix = ["MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_"]
# Blacklisted item property-value pairs
blacklist_property = {
    "OBSOLETE": ['true'] # Multiple values can be defined for a single property
}

parsed_data = {}


def get_item_data():
    global parsed_data
    if parsed_data == {}:
        init()
    return parsed_data


def is_blacklisted(item_name, item_data):
    """Check if item is blacklisted"""
    # Check if item name has a blacklisted prefix
    if any(item_name.startswith(prefix) for prefix in blacklist_prefix):
        return True

    # Check if a property and value is blacklisted
    for prop, blacklisted_values in blacklist_property.items():
        for item_prop, value in item_data.items():
            if item_prop.lower() == prop.lower():
                prop = value.rstrip(',').lower()
                if prop in blacklisted_values:
                    return True
    
    return False


def parse_fluid_container(lines, start_index):
    """Parse fluid container"""
    properties = {}
    fluid_list = []
    block_level = 1  # Entering FluidContainer block
    i = start_index

    # Regex for key-value pairs
    key_value_pattern = re.compile(r'^\s*(\w+)\s*=\s*(.+?),?\s*$')

    while i < len(lines):
        line = lines[i].strip()

        # End of current block
        if line == '}':
            block_level -= 1
            if block_level == 0:
                break
            i += 1
            continue

        # Start Fluids block
        if re.match(r'^\s*Fluids\b', line):
            block_level += 1
            i += 1
            # Stay in the Fluids block
            while block_level >= 2:
                line = lines[i].strip()
                if line == '}':
                    block_level -= 1
                    i += 1
                    continue

                # Parse fluid entries
                fluid_match = key_value_pattern.match(line)
                if fluid_match and fluid_match.group(1) == "fluid":
                    fluid_value = fluid_match.group(2).strip()

                    # Split fluid into components
                    fluid_parts = fluid_value.split(':', 2)  # Split into up to 3 parts
                    fluid_data = {
                        'FluidID': fluid_parts[0],                      # First part: FluidID
                        'LiquidCount': float(fluid_parts[1]),           # Second part: LiquidCount
                    }
                    if len(fluid_parts) == 3:  # Third part: Optional Color
                        color_part = fluid_parts[2]
                        if all(c.replace('.', '', 1).isdigit() for c in color_part.split(':')):  
                            # Check if the Color part contains numbers (RGB float)
                            fluid_data['Color'] = [float(c) for c in color_part.split(':')]
                        else:
                            # Otherwise, store it as a name
                            fluid_data['Color'] = color_part

                    fluid_list.append(fluid_data)
                i += 1
            continue

        # Parse other key-value pairs in FluidContainer
        key_value_match = key_value_pattern.match(line)
        if key_value_match:
            key, value = key_value_match.groups()
            properties[key.strip()] = value.strip()

        i += 1

    # Add fluids list to properties
    if fluid_list:
        properties['fluids'] = fluid_list

    return properties, i


def parse_item(lines, start_index, module_name):
    """Parse an item and its properties"""
    item_dict = {}
    item_name = None
    i = start_index

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty line
        if not line:
            i += 1
            continue

        # Skip block comments (/* */) and inline comments (/** **/)
        if '/*' in line:
            # Inline comments
            if '*/' in line:
                line = re.sub(r'/\*.*?\*/', '', line).strip()
            else:
                # Multi-line block comments
                while '*/' not in line and i < len(lines) - 1:
                    i += 1
                    line = lines[i].strip()
                # Remove the remaining part of the block comment
                if '*/' in line:
                    line = re.sub(r'.*\*/', '', line).strip()
                else:
                    # If no closing comment, skip the entire line
                    i += 1
                    continue
        
        # Start FluidCOntainer block
        if re.match(r'^component\sFluidContainer\b', line):
            fluid_properties = {}
            fluid_properties, i = parse_fluid_container(lines, i + 1)
            item_dict.update(fluid_properties)
            continue

        # Start item block
        if re.match(r'^item(\s)', line):
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                item_name = parts[1]
                item_id = f"{module_name}.{item_name}"
            else:
                echo_warning(f"Couldn't parse item line: {line}")
                i += 1
                continue
        
        # Close current item block
        elif line == '}':
            return item_name, item_dict, i
        
        # Get the item's properties
        elif '=' in line:
            property_key, property_value = line.split('=', 1)
            property_key = property_key.strip()
            property_value = property_value.rstrip(',').strip()

            blacklist_keys = ['DisplayName', 'DummyProperty']
            # Handle properties (separated by ';') with key-value pairs (separated by ':')
            if ':' in property_value:
                # Skip blacklisted keys
                if property_key in blacklist_keys:
                    pass
                else:
                    try:
                        property_value = {
                            k.strip(): v.strip().split('|') if '|' in v else v.strip()
                            for pair in property_value.split(';')
                            if ':' in pair
                            for k, v in [pair.split(':', 1)]
                        }
                    except ValueError:
                        echo_warning(f"Skipping invalid key-value pair in line: {line}")

            # Handle multiple values (separated by ';')
            elif ';' in property_value:
                property_value = [v.strip() for v in property_value.split(';') if v.strip()]
            
            # Add property and value to dictionary
            item_dict[property_key] = property_value

        i += 1
    
    return None, None, i


def parse_module(lines):
    """Parse the module and its items"""
    combined_dict = {}
    module_name = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect the start of a module block
        if re.match(r'^module(\s)', line):
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                module_name = parts[1]
            else:
                echo_warning(f"Couldn't parse module line: {line}")
        
        # Detect the start of an item block
        elif re.match(r'^item(\s)', line): # regex to return 'item' and not any suffixes
            parts = re.split(r'\s+', line)
            if len(parts) == 2:
                item_name, item_data, end_index = parse_item(lines, i, module_name)
                if item_name and module_name and not is_blacklisted(item_name, item_data):
                    item_id = f"{module_name}.{item_name}"
                    combined_dict[item_id] = item_data
                else:
                    item_id = f"{module_name}.{item_name}"
                i = end_index
                
#            else:
#                echo_warning(f"Skipping item line: {line}")
        i += 1

    return combined_dict


def parse_files(file_paths: list[str]) -> dict:
    """
    Parses a list of .txt files and updates the global parsed_data.

    Args:
        file_paths (list[str]): List of absolute file paths to parse.

    Returns:
        dict: Parsed item data.
    """
    global parsed_data

    for file_path in file_paths:
        if file_path.endswith('.txt') and os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                parsed_data.update(parse_module(lines))

    # Update DisplayName with translated values
    for item_id, item_data in parsed_data.items():
        display_name = item_data.get("DisplayName")

        # Fix for DisplayName being a list (e.g., multiple DisplayName lines)
        if isinstance(display_name, list):
            display_name = ", ".join(display_name)

        display_name = Translate.get(item_id, "DisplayName", "en", display_name)
        parsed_data[item_id]["DisplayName"] = display_name

    # Sort parsed data by Type
    parsed_data = dict(sorted(parsed_data.items(), key=lambda x: x[1]["Type"]))

    save_cache(parsed_data, CACHE_JSON)

    return parsed_data


def get_new_items(old_dict, new_dict):
    """Compares the new dict with the old dict and returns a dict of new items and another for changed properties."""
    new_keys_dict = {}
    changed_values_dict = {}

    for key in new_dict:
        if key not in old_dict:
            new_keys_dict[key] = new_dict[key]

    def compare_dicts(old, new):
        changes = {}
        for key, value in new.items():
            if key in old:
                if isinstance(value, dict) and isinstance(old[key], dict):
                    nested_changes = compare_dicts(old[key], value)
                    if nested_changes:
                        changes[key] = nested_changes
                elif old[key] != value:
                    changes[key] = value
        return changes

    changed_values_dict = compare_dicts(old_dict, new_dict)

    return new_keys_dict, changed_values_dict


def init():
    """Initialise parser"""
    global parsed_data
    Language.get() # Initialise so we don't interrupt progress bars

    cache_file = os.path.join(DATA_DIR, CACHE_JSON)
    # Try to get cache from json file
    cached_data, cache_version = load_cache(cache_file, "item", get_version=True, backup_old=True)
    game_version = Version.get()

    # Parse items if there is no cache, or it's outdated.
    if cache_version != game_version:
        script_files = get_script_files()
        parsed_data = parse_files(script_files)
    else:
        parsed_data = cached_data.copy()

    # Compare parsed_data with cached data.
    if cached_data and cached_data != parsed_data and cache_version != game_version:
        new_items, modified_items = get_new_items(cached_data, parsed_data)
        save_cache(new_items, CACHE_JSON.replace(".json", "") + "_new.json")
        save_cache(modified_items, CACHE_JSON.replace(".json", "") + "_changes.json")

    echo_info(f"Number of items found: {len(parsed_data)}")

if __name__ == "__main__":
    init()
