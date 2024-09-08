import os
import re
import json
from scripts.core import translate

# Blacklisted item name prefixes
blacklist_prefix = ["MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_"]
# Blacklisted item property-value pairs
blacklist_property = {
    "OBSOLETE": ['true'] # Multiple values can be defined for a single property
}

item_counter = 0
parsed_data = {}


def get_item_data():
    global parsed_data
    if parsed_data == {}:
        init()
    return parsed_data


# Check if item is blacklisted
def is_blacklisted(item_name, item_data):
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


# Parse an item and its properties
def parse_item(lines, start_index, module_name):
    global item_counter
    item_dict = {}
    item_name = None
    i = start_index
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty line
        if not line:
            i += 1
            continue

        # Skip comments (/* */)
        if '/*' in line:
            while '*/' not in line and i < len(lines):
                i += 1
                line = lines[i].strip()
            i += 1
            continue

        # Start item block
        if re.match(r'^item(\s)', line):
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                item_name = parts[1]
                item_id = f"{module_name}.{item_name}"
            else:
                print(f"Warning: Couldn't parse item line: {line}")
                i += 1
                continue
        
        # Close current item block
        elif line == '}':
            return item_name, item_dict, i
        
        # Get the item's properties
        elif '=' in line:
            property_key, property_value = line.split('=', 1)
            property_key = property_key.strip()
            property_value = property_value.strip().rstrip(',')
            
            if property_key == 'DisplayName':
                display_name = translate.get_translation(item_id, 'DisplayName', 'en')
                if display_name == item_id:
                    display_name = property_value
                property_value = display_name
        
            # Handle properties (separated by ';') with key-value pairs (separated by ':')
            if ':' in property_value:
                property_value = {k.strip(): v.strip().split('|') if '|' in v else v.strip()
                    for k, v in (pair.split(':') for pair in property_value.split(';'))}

            # Handle multiple values (separated by ';')
            elif ';' in property_value:
                property_value = [v.strip() for v in property_value.split(';')]
            
            # Add property and value to dictionary
            item_dict[property_key] = property_value

        i += 1
    
    return None, None, i


# Parse the module and its items
def parse_module(lines):
    global item_counter
    combined_dict = {}
    module_name = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect the start of a module block
        if re.match(r'^module(\s)', line):
            parts = line.split(' ')
            if len(parts) >= 2:
                module_name = parts[1]
            else:
                print(f"Warning: Couldn't parse module line: {line}")
        
        # Detect the start of an item block
        elif re.match(r'^item(\s)', line): # regex to return 'item' and not any suffixes
            item_name, item_data, end_index = parse_item(lines, i, module_name)
            if item_name and module_name and not is_blacklisted(item_name, item_data):
                item_id = f"{module_name}.{item_name}"
                combined_dict[item_id] = item_data
                item_counter += 1
            else:
                item_id = f"{module_name}.{item_name}"
            i = end_index
        
        i += 1

    return combined_dict


# Parse all files in a folder
def parse_files(directory):
    global parsed_data

    # Traverse the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    parsed_data.update(parse_module(lines))
    
    return parsed_data


# Save parsed data to json file
def save_to_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Initialise parser
def init():
    global parsed_data
    resources_path = 'resources/scripts/'
    output_file = 'output/logging/parsed_item_data.json'
    parsed_data = parse_files(resources_path)
    save_to_json(parsed_data, output_file)
    print(f"Total number of items parsed: {item_counter}")

if __name__ == "__main__":
    init()
