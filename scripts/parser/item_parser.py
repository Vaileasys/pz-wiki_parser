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

# Parse fluid container
def parse_fluid_container(lines, start_index):
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
            property_value = property_value.rstrip(',').strip()
            
            if property_key == 'DisplayName':
                display_name = translate.get_translation(item_id, 'DisplayName', 'en')
                if display_name == item_id:
                    display_name = property_value
                property_value = display_name


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
                        print(f"Warning: Skipping invalid key-value pair in line: {line}")

            # Handle multiple values (separated by ';')
            elif ';' in property_value:
                property_value = [v.strip() for v in property_value.split(';') if v.strip()]
            
            # Add property and value to dictionary
            item_dict[property_key] = property_value

        i += 1
    
    return None, None, i


# Parse the module and its items
def parse_module(lines):
    global item_counter
    combined_dict = {}
    module_name = None
    block_level = 0

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
            parts = line.split(' ')
            if len(parts) == 2:
                item_name, item_data, end_index = parse_item(lines, i, module_name)
                if item_name and module_name and not is_blacklisted(item_name, item_data):
                    item_id = f"{module_name}.{item_name}"
                    combined_dict[item_id] = item_data
                    item_counter += 1
                else:
                    item_id = f"{module_name}.{item_name}"
                i = end_index
#            else:
#                print(f"Warning: Skipping item line: {line}")
        
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
