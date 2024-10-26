import os
import json
import re
import struct
import lupa
from lupa import LuaRuntime
from slpp import slpp as lua_parser
import xml.etree.ElementTree as ET


def parse_container_files(distributions_lua_path, procedural_distributions_path, output_path):
    # Ensure output directory exists
    """
    Parses Lua container files to extract distribution data and convert it to JSON format.

    This function processes two Lua files: one containing general distribution data and the
    other containing procedural distribution data. It modifies the Lua code to make tables
    global, executes the Lua code using a Lua runtime, and extracts data from the tables.
    The data is then converted to Python dictionaries and saved as JSON files.

    Args:
        distributions_lua_path (str): The file path to the Lua file containing distribution data.
        procedural_distributions_path (str): The file path to the Lua file containing procedural
            distribution data.
        output_path (str): The directory where the output JSON files ('distributions.json' and
            'proceduraldistributions.json') will be saved.

    Raises:
        Exception: If there is an error executing Lua code or processing the tables.
    """
    os.makedirs(output_path, exist_ok=True)

    # Helper function to convert Lua tables into Python-friendly structures
    def lua_table_to_python(obj):
        if isinstance(obj, dict):  # Lua table as a dict
            return {k: lua_table_to_python(v) for k, v in obj.items()}
        elif hasattr(obj, 'items'):  # _LuaTable, convert to Python dict
            return {k: lua_table_to_python(v) for k, v in obj.items()}
        elif isinstance(obj, list):  # Already a Python list
            return [lua_table_to_python(item) for item in obj]
        return obj  # Return the object if it's not a table

    # Function to read and modify Lua file content
    def read_and_modify_lua_file(filename, table_name):
        # Read the Lua file into memory
        with open(filename, 'r') as file:
            lua_content = file.read()

        # Modify the content: change `local` to make it global
        lua_content = lua_content.replace(f"local {table_name}", table_name)

        return lua_content

    # Parser for `distributions.lua` (modified to append non-procedural tables to procedural memory)
    def distributions_parser(lua_code, procedural_memory):
        # Initialize the Lua runtime
        lua = LuaRuntime(unpack_returned_tuples=True)

        # Define the `is_table` helper function in Lua
        lua.execute('function is_table(x) return type(x) == "table" end')

        # Execute the modified Lua code in memory
        lua.execute(lua_code)

        # Access the global distributionTable from Lua
        distribution_table = lua.globals().distributionTable

        # Helper function to remove unwanted prefixes in both cases
        def remove_prefixes(name):
            prefixes = ["Base.", "Farming.", "Radio.", "Camping.", "farming.", "radio.", "camping."]
            for prefix in prefixes:
                if name.startswith(prefix):
                    return name[len(prefix):]
            return name

        # Create the final nested dictionary for the procedural-only containers
        output_json = {}

        # Process the content of the distribution table
        for room_name, room_content in distribution_table.items():
            containers = {}
            if lua.globals().is_table(room_content):
                for container_name, container_content in room_content.items():
                    if not lua.globals().is_table(container_content):
                        continue

                    container_details = {}
                    if 'procedural' in container_content and container_content['procedural']:
                        container_details['procedural'] = True
                        if 'procList' in container_content:
                            container_details['procList'] = []
                            for i in range(1, len(container_content['procList']) + 1):
                                item = container_content['procList'][i]
                                if lua.globals().is_table(item):
                                    container_details['procList'].append({
                                        'name': remove_prefixes(item['name']),  # Remove prefixes here
                                        'min': item['min'] if 'min' in item else 0,
                                        'max': item['max'] if 'max' in item else 0,
                                        'weightChance': item['weightChance'] if 'weightChance' in item else None
                                    })
                        containers[container_name] = container_details
                    else:
                        # Process non-procedural items (convert to list of {"name": <item_name>, "chance": <item_chance>})
                        non_procedural_details = {}
                        if 'rolls' in container_content:
                            non_procedural_details['rolls'] = container_content['rolls']

                        if 'items' in container_content and lua.globals().is_table(container_content['items']):
                            items_list = container_content['items']
                            non_procedural_details['items'] = []
                            for i in range(1, len(items_list), 2):
                                item_name = remove_prefixes(items_list[i])  # Apply prefix removal here
                                item_chance = items_list[i + 1]
                                non_procedural_details['items'].append({
                                    'name': item_name,
                                    'chance': item_chance
                                })

                        if 'junk' in container_content and lua.globals().is_table(container_content['junk']['items']):
                            junk_items_list = container_content['junk']['items']
                            non_procedural_details['junk'] = {
                                'rolls': container_content['junk']['rolls'],
                                'items': []
                            }
                            for i in range(1, len(junk_items_list), 2):
                                item_name = remove_prefixes(junk_items_list[i])  # Apply prefix removal here as well
                                item_chance = junk_items_list[i + 1]
                                non_procedural_details['junk']['items'].append({
                                    'name': item_name,
                                    'chance': item_chance
                                })

                        # Append non-procedural tables to the procedural memory
                        procedural_memory[room_name] = procedural_memory.get(room_name, {})
                        procedural_memory[room_name][container_name] = non_procedural_details

            if containers:  # Only add procedural rooms to the output
                output_json[room_name] = containers

        return lua_table_to_python(output_json)

    # Parser for `proceduraldistributions.lua` (modified for new `items` output format)
    def procedural_distributions_parser(lua_code, procedural_memory):
        # Initialize the Lua runtime
        lua = LuaRuntime(unpack_returned_tuples=True)

        # Define the `is_table` helper function in Lua
        lua.execute('function is_table(x) return type(x) == "table" end')

        # Execute the modified Lua code in memory
        lua.execute(lua_code)

        # Access the ProceduralDistributions.list from Lua
        distribution_table = lua.globals().ProceduralDistributions.list

        # Create the final nested dictionary that will be converted to JSON
        output_json = {}

        # Helper function to remove unwanted prefixes in both cases
        def remove_prefixes(name):
            prefixes = ["Base.", "Farming.", "Radio.", "Camping.", "farming.", "radio.", "camping."]

            for prefix in prefixes:
                if name.startswith(prefix):
                    return name[len(prefix):]
            return name

        # Process the content of the procedural distribution table
        for table_name, table_content in distribution_table.items():
            if not lua.globals().is_table(table_content):
                continue

            table_details = {}

            if 'rolls' in table_content:
                table_details['rolls'] = table_content['rolls']

            if 'items' in table_content and lua.globals().is_table(table_content['items']):
                items_list = table_content['items']
                table_details['items'] = []
                for i in range(1, len(items_list), 2):
                    item_name = remove_prefixes(items_list[i])  # Apply prefix removal here
                    item_chance = items_list[i + 1]
                    table_details['items'].append({
                        'name': item_name,
                        'chance': item_chance
                    })

            if 'junk' in table_content and lua.globals().is_table(table_content['junk']['items']):
                junk_items_list = table_content['junk']['items']
                table_details['junk'] = {
                    'rolls': table_content['junk']['rolls'],
                    'items': []
                }
                for i in range(1, len(junk_items_list), 2):
                    item_name = remove_prefixes(junk_items_list[i])  # Apply prefix removal here as well
                    item_chance = junk_items_list[i + 1]
                    table_details['junk']['items'].append({
                        'name': item_name,
                        'chance': item_chance
                    })

            output_json[table_name] = table_details

        # Now, append the non-procedural data that was passed from distributions_parser
        for table_name, table_content in procedural_memory.items():
            if table_name not in output_json:
                output_json[table_name] = table_content
            else:
                output_json[table_name].update(table_content)

        return lua_table_to_python(output_json)

    # Function to save JSON to file
    def save_to_json(data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def main():
        # Read both Lua files into memory
        lua_code_distributions = read_and_modify_lua_file(distributions_lua_path, 'distributionTable')
        lua_code_procedural = read_and_modify_lua_file(procedural_distributions_path, 'ProceduralDistributions')

        # Initialize an empty dict to store the non-procedural containers from distributions
        procedural_memory = {}

        # First, process 'distributions.lua', appending non-procedural tables to procedural_memory
        room_data = distributions_parser(lua_code_distributions, procedural_memory)
        save_to_json(room_data, os.path.join(output_path, 'distributions.json'))

        # Then, process 'proceduraldistributions.lua', incorporating the appended non-procedural tables
        procedural_data = procedural_distributions_parser(lua_code_procedural, procedural_memory)
        save_to_json(procedural_data, os.path.join(output_path, 'proceduraldistributions.json'))

    # Run the main function
    main()


def parse_foraging(forage_definitions_path, output_path):
    """
    Parses a Lua file containing foraging definitions and extracts item data
    to generate a JSON file with item chances.

    This function reads a Lua file from the specified path, executes the Lua
    code to access the 'forageDefs' table, and extracts item information. It
    then augments the item data with chance values extracted from specified
    Lua table names. The resulting data is saved as a JSON file in the
    specified output directory.

    Args:
        forage_definitions_path (str): The file path to the Lua file containing
            foraging definitions.
        output_path (str): The directory where the output JSON file
            ('foraging.json') will be saved.

    Raises:
        Exception: If there is an error parsing any of the Lua tables.
    """
    with open(forage_definitions_path, 'r', encoding='utf-8') as f:
        lua_code = f.read()

    # Function to extract a Lua table given its name
    def extract_lua_table(lua_code, table_name):
        pattern = r'local\s+' + re.escape(table_name) + r'\s*=\s*\{'
        match = re.search(pattern, lua_code)
        if not match:
            return None
        start = match.end() - 1  # Position of the opening brace
        brace_level = 1
        end = start + 1
        while end < len(lua_code):
            char = lua_code[end]
            if char == '{':
                brace_level += 1
            elif char == '}':
                brace_level -= 1
                if brace_level == 0:
                    # Found the matching closing brace
                    break
            end += 1
        table_str = lua_code[start:end+1]
        return table_str

    # List of table names to extract
    table_names = [
        'ammunition',
        'clothing',
        'medical',
        'junkWeapons',
        'junkItems',
        'trashItems',
        # Add other tables if needed
    ]

    # Extract tables
    tables = {}
    for table_name in table_names:
        table_str = extract_lua_table(lua_code, table_name)
        if table_str:
            tables[table_name] = table_str

    # Build a mapping from item names to chance values
    item_chance_mapping = {}

    for table_name, table_str in tables.items():
        try:
            table_dict = lua_parser.decode(table_str)
        except Exception as e:
            print(f"Error parsing table {table_name}: {e}")
            continue
        # Handle different structures based on table content
        if 'items' in table_dict and 'chance' in table_dict:
            # Single-level table
            chance = table_dict['chance']
            items = table_dict['items']
            for item_name, item_full_name in items.items():
                item_chance_mapping[item_name] = chance
        else:
            # Multi-level table (e.g., with rarity levels)
            for rarity_level, data in table_dict.items():
                if isinstance(data, dict):
                    chance = data.get('chance')
                    items = data.get('items')
                    if chance and items:
                        for item_name, item_full_name in items.items():
                            item_chance_mapping[item_name] = chance
                    else:
                        # Some tables may have items directly under rarity levels
                        for sub_rarity, sub_data in data.items():
                            if isinstance(sub_data, dict):
                                chance = sub_data.get('chance')
                                items = sub_data.get('items')
                                if chance and items:
                                    for item_name, item_full_name in items.items():
                                        item_chance_mapping[item_name] = chance

    # Now execute the Lua code
    # Create Lua runtime
    lua = LuaRuntime(unpack_returned_tuples=True)

    # Lua code to define missing functions and variables
    prelude = '''
    -- Define empty functions to prevent errors during execution
    doWildFoodSpawn = function() end
    doRandomAgeSpawn = function() end
    doWildCropSpawn = function() end
    doPoisonItemSpawn = function() end
    doDeadTrapAnimalSpawn = function() end
    doClothingItemSpawn = function() end
    doJunkWeaponSpawn = function() end
    doGenericItemSpawn = function() end
    doWildMushroomSpawn = function() end
    doForageItemIcon = function() end
    doItemSize = function() end
    doWeight = function() end

    -- Define worldSprites table with necessary keys
    worldSprites = {
        shrubs = {},
        wildPlants = {},
        vines = {},
        smallTrees = {},
        berryBushes = {},
    }
    -- Define getTexture function
    getTexture = function(path) return path end
    '''

    # Combine prelude and Lua code
    full_lua_code = prelude + lua_code

    # Execute the modified Lua code
    lua.execute(full_lua_code)

    # Get the forageDefs table
    forageDefs = lua.globals().forageDefs

    # Function to convert Lua table to Python dict
    def lua_table_to_python(obj):
        if lupa.lua_type(obj) == 'table':
            py_dict = {}
            for key in obj:
                py_key = key
                py_value = obj[key]
                # Convert key
                if lupa.lua_type(py_key) in ('table', 'function'):
                    py_key = str(py_key)
                else:
                    py_key = lua_table_to_python(py_key)
                # Convert value
                if lupa.lua_type(py_value) == 'table':
                    py_value = lua_table_to_python(py_value)
                elif lupa.lua_type(py_value) == 'function':
                    py_value = str(py_value)
                else:
                    py_value = py_value
                py_dict[py_key] = py_value
            return py_dict
        elif lupa.lua_type(obj) == 'function':
            return str(obj)
        else:
            return obj

    # Convert the forageDefs table to a Python dictionary
    forage_defs_dict = lua_table_to_python(forageDefs)

    # Now, augment each item with its chance value
    for item_name, item_data in forage_defs_dict.items():
        chance = item_chance_mapping.get(item_name)
        if chance is not None:
            item_data['chance'] = chance

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Write the dictionary to a JSON file
    with open(os.path.join(output_path, 'foraging.json'), 'w', encoding='utf-8') as f:
        json.dump(forage_defs_dict, f, ensure_ascii=False, indent=4)


def parse_vehicles(vehicle_distributions_path, output_path):
    """
    Parse the Lua vehicle distribution file and convert it into JSON format.

    Parameters:
        vehicle_distributions_path (str): Path to the Lua file to parse.
        output_path (str): Path where the output JSON file will be written.
    """
    def parse_lua_table(lua_content):
        key_pattern = re.compile(r'VehicleDistributions\.(\w+)\s*=\s*{')
        rolls_pattern = re.compile(r'rolls\s*=\s*(\d+),')
        item_pattern = re.compile(r'"(\w+)"\s*,\s*(\d+\.?\d*),')
        junk_pattern = re.compile(r'junk\s*=\s*{')
        junk_rolls_pattern = re.compile(r'rolls\s*=\s*(\d+),')
        junk_item_pattern = re.compile(r'"(\w+)"\s*,\s*(\d+\.?\d*),')

        distribution_dict = {}
        current_key = None
        inside_junk = False
        junk_items = []
        lines = lua_content.splitlines()

        for line in lines:
            key_match = key_pattern.search(line)
            if key_match:
                current_key = key_match.group(1)
                distribution_dict[current_key] = {'rolls': 1, 'items': {}, 'junk': {}}
                inside_junk = False
                continue
            rolls_match = rolls_pattern.search(line)
            if rolls_match and current_key:
                distribution_dict[current_key]['rolls'] = int(rolls_match.group(1))
            item_match = item_pattern.findall(line)
            if item_match and current_key and not inside_junk:
                for item, weight in item_match:
                    distribution_dict[current_key]['items'][item] = distribution_dict[current_key]['items'].get(item, 0) + float(weight)
            junk_match = junk_pattern.search(line)
            if junk_match and current_key:
                inside_junk = True
                junk_items = []
            junk_rolls_match = junk_rolls_pattern.search(line)
            if junk_rolls_match and inside_junk and current_key:
                distribution_dict[current_key]['junk']['rolls'] = int(junk_rolls_match.group(1))
            junk_item_match = junk_item_pattern.findall(line)
            if junk_item_match and inside_junk and current_key:
                for item, weight in junk_item_match:
                    junk_items.append((item, float(weight)))
            if inside_junk and '}' in line:
                distribution_dict[current_key]['junk']['items'] = {item: weight for item, weight in junk_items}
                inside_junk = False
        return distribution_dict

    try:
        with open(vehicle_distributions_path, 'r', encoding='utf-8') as lua_file:
            lua_content = lua_file.read()
    except FileNotFoundError:
        print(f"Error: The file {vehicle_distributions_path} does not exist.")
        return
    except Exception as e:
        print(f"Error reading {vehicle_distributions_path}: {e}")
        return
    try:
        vehicle_distributions = parse_lua_table(lua_content)
    except Exception as e:
        print(f"Error parsing Lua content: {e}")
        return
    try:
        os.makedirs(output_path, exist_ok=True)
        output_file_path = os.path.join(output_path, 'vehicle_distributions.json')
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(vehicle_distributions, json_file, indent=4)
    except Exception as e:
        print(f"Error writing JSON file: {e}")


def parse_attachedweapons(attached_weapon_path, output_path):
    """
    Parses a Lua file containing attached weapon definitions and converts it into a JSON format.

    This function reads a Lua file specified by the `attached_weapon_path`, executes the Lua code
    within a Lua runtime to retrieve the 'AttachedWeaponDefinitions' table, and converts this table
    into a Python dictionary. It specifically extracts entries that contain a 'chance' field,
    which are considered weapon definitions. The resulting dictionary is then written to a JSON
    file at the specified `output_path`.

    Args:
        attached_weapon_path (str): The file path to the Lua file containing attached weapon definitions.
        output_path (str): The directory where the output JSON file ('attached_weapons.json') will be saved.

    Raises:
        Exception: If there is an error executing Lua code or processing the Lua tables.
    """
    with open(attached_weapon_path, 'r') as file:
        lua_code = file.read()

    # Prepare the Lua environment
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('AttachedWeaponDefinitions = AttachedWeaponDefinitions or {}')
    lua.execute(lua_code)
    attached_weapon_definitions = lua.eval('AttachedWeaponDefinitions')

    # Function to convert Lua table to Python dictionary or list
    def lua_table_to_python(obj):
        if lupa.lua_type(obj) == 'table':
            # Get all keys in the Lua table
            keys = list(obj.keys())
            # Check if all keys are consecutive integers starting from 1
            if all(isinstance(key, int) for key in keys):
                min_key = min(keys)
                max_key = max(keys)
                expected_keys = list(range(1, max_key + 1))
                # If the keys are consecutive integers, treat the table as a list
                if sorted(keys) == expected_keys:
                    return [lua_table_to_python(obj[i]) for i in expected_keys]
            # Otherwise, treat it as a dictionary
            return {str(k): lua_table_to_python(v) for k, v in obj.items()}
        elif isinstance(obj, (str, int, float, bool)):
            return obj
        else:
            return str(obj)

    # Function to remove specified prefixes
    def remove_prefixes(name):
        prefixes = ["Base.", "Radio.", "Farming."]
        for prefix in prefixes:
            if name.startswith(prefix):
                return name[len(prefix):]
        return name

    # Convert the Lua table to a Python dictionary
    attached_weapon_definitions_dict = lua_table_to_python(attached_weapon_definitions)

    # Extract weapon definitions (entries with a 'chance' field) and remove prefixes
    weapon_definitions = {}
    for key, value in attached_weapon_definitions_dict.items():
        if isinstance(value, dict) and 'chance' in value:
            # Remove prefixes from the main key
            cleaned_key = remove_prefixes(key)
            # If the entry has a 'weapons' list, clean each entry within that list
            if 'weapons' in value and isinstance(value['weapons'], list):
                value['weapons'] = [remove_prefixes(weapon) for weapon in value['weapons']]
            # Add to the final dictionary
            weapon_definitions[cleaned_key] = value

    # Write the weapon definitions to the JSON file
    try:
        # Ensure output directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_file_path = os.path.join(output_path, 'attached_weapons.json')
        with open(output_file_path, 'w') as json_file:
            json.dump(weapon_definitions, json_file, indent=4)

    except IOError as e:
        print(f"Error writing to file {output_file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def parse_clothing(clothing_file_path, guid_table_path, output_file_path):
    """
    Parse the clothing XML file and generate a JSON file containing outfit data with item probabilities.

    :param clothing_file_path: The path to the clothing XML file
    :param guid_table_path: The path to the GUID table XML file
    :param output_file_path: The path to the output JSON file
    :return: None
    """
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    def guid_item_mapping(guid_table):
        guid_mapping = {}
        try:
            tree = ET.parse(guid_table)
            root = tree.getroot()
            for file_entry in root.findall('files'):
                path = file_entry.find('path').text
                guid = file_entry.find('guid').text
                filename = os.path.splitext(os.path.basename(path))[0]
                guid_mapping[guid] = filename
        except ET.ParseError as e:
            print(f"Error parsing GUID table XML: {e}")
        return guid_mapping

    def get_outfits(xml_file, guid_mapping):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing clothing XML: {e}")
            return {}

        output_json = {
            "FemaleOutfits": {},
            "MaleOutfits": {}
        }

        for outfit in root.findall('.//m_FemaleOutfits') + root.findall('.//m_MaleOutfits'):
            outfit_type = "FemaleOutfits" if outfit.tag == 'm_FemaleOutfits' else "MaleOutfits"
            outfit_name = outfit.find('m_Name').text if outfit.find('m_Name') is not None else "Unknown Outfit"
            outfit_guid = outfit.find('m_Guid').text if outfit.find('m_Guid') is not None else "No GUID"
            items_with_probabilities = {}

            for item_block in outfit.findall('m_items'):
                probability_tag = item_block.find('probability')
                probability = float(probability_tag.text)*100 if probability_tag is not None else 100
                probability = int(probability)

                item_guid = item_block.find('itemGUID').text if item_block.find('itemGUID') is not None else None
                if item_guid:
                    item_name = guid_mapping.get(item_guid, item_guid)
                    items_with_probabilities[item_name] = probability

                for subitem in item_block.findall('.//subItems/itemGUID'):
                    subitem_guid = subitem.text
                    subitem_name = guid_mapping.get(subitem_guid, subitem_guid)
                    items_with_probabilities[subitem_name] = probability  # Apply the same probability for sub-items

            if outfit_name:
                output_json[outfit_type][outfit_name] = {
                    "GUID": outfit_guid,
                    "Items": items_with_probabilities
                }

        return output_json

    guid_mapping = guid_item_mapping(guid_table_path)
    outfits_data = get_outfits(clothing_file_path, guid_mapping)

    with open(output_file_path, "w") as f_out:
        json.dump(outfits_data, f_out, indent=4)


def parse_stories(class_files_directory, output_path):

    """
    Processes all .class files in the given directory and collects their relevant string constants.

    This function takes two parameters: the path to the directory containing the .class files
    and the path to the output JSON file.

    It first processes each .class file in the given directory and collects their relevant string
    constants. It then saves the collected constants to a JSON file at the specified output path.

    :param class_files_directory: The path to the directory containing the .class files
    :param output_path: The path to the output JSON file
    :return: None
    """

    def read_constant_pool(file):
        """
        Reads the constant pool of a .class file and extracts relevant string constants.

        This function takes a binary file object as input and reads the constant pool
        section of the .class file. It then extracts any relevant string constants
        and returns them as a list. The constants that are extracted are those that
        contain a period and start with "Base.", "Farming.", or "Radio.".

        :param file: A binary file object
        :return: A list of relevant string constants
        """
        # Skip the first 8 bytes (magic number and minor/major version)
        file.read(8)

        # Read the constant pool count
        constant_pool_count = struct.unpack(">H", file.read(2))[0] - 1

        constants = []

        # Loop through the constant pool
        i = 0
        while i < constant_pool_count:
            # Each entry starts with a 1-byte tag
            tag = struct.unpack("B", file.read(1))[0]

            if tag == 1:  # CONSTANT_Utf8
                length = struct.unpack(">H", file.read(2))[0]
                value = file.read(length)
                try:
                    decoded_value = value.decode("utf-8")
                    # Only add constants that contain a period and start with specified prefixes
                    if '.' in decoded_value and decoded_value.startswith(("Base.", "Farming.", "Radio.")):
                        # Remove the prefix before appending
                        if decoded_value.startswith("Base."):
                            constants.append(decoded_value[5:])
                        elif decoded_value.startswith("Farming."):
                            constants.append(decoded_value[8:])
                        elif decoded_value.startswith("Radio."):
                            constants.append(decoded_value[6:])
                        else:
                            constants.append(decoded_value)
                except UnicodeDecodeError:
                    pass  # Skip non-UTF-8 constants
            elif tag in {7, 8}:  # CONSTANT_Class or CONSTANT_String
                file.read(2)  # Skip over 2 bytes (index reference)
            elif tag in {3, 4}:  # CONSTANT_Integer or CONSTANT_Float
                file.read(4)  # Skip over 4 bytes
            elif tag in {5, 6}:  # CONSTANT_Long or CONSTANT_Double (take two entries)
                file.read(8)  # Skip over 8 bytes
                i += 1  # These take up two entries in the constant pool
            elif tag in {9, 10, 11, 12, 15, 16, 18}:  # Other reference types
                file.read(4)  # Skip over 4 bytes
            i += 1

        return constants

    def process_class_files(directory):
        """Processes all .class files in the given directory and collects their relevant constants."""
        constants_by_file = {}

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".class"):
                    class_file_path = os.path.join(root, file)
                    with open(class_file_path, "rb") as class_file:
                        constants = read_constant_pool(class_file)
                        if constants:
                            # Use the filename without extension as the key
                            file_name_without_ext = os.path.splitext(file)[0]
                            constants_by_file[file_name_without_ext] = constants

        return constants_by_file

    def save_to_json(data, output_path):
        """Saves the data to a JSON file at the specified output path."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # Execute the process
    constants_by_file = process_class_files(class_files_directory)
    save_to_json(constants_by_file, output_path)


def main():
    # File paths
    attached_weapon_path = "resources/lua/AttachedWeaponDefinitions.lua"
    distributions_lua_path = "resources/lua/Distributions.lua"
    forage_definitions_path = "resources/lua/forageDefinitions.lua"
    procedural_distributions_path = "resources/lua/ProceduralDistributions.lua"
    vehicle_distributions_path = "resources/lua/VehicleDistributions.lua"
    clothing_file_path = "resources/clothing.xml"
    guid_table_path = "resources/fileGuidTable.xml"
    class_files_directory = "resources/Java"

    # Call the init function to check if all files exist
    init(attached_weapon_path, distributions_lua_path, forage_definitions_path,
         procedural_distributions_path, vehicle_distributions_path, clothing_file_path, guid_table_path)

    # Parse files into json
    parse_container_files(distributions_lua_path, procedural_distributions_path, "output/distributions/json/")
    parse_foraging(forage_definitions_path, "output/distributions/json/")
    parse_vehicles(vehicle_distributions_path, "output/distributions/json/")
    parse_attachedweapons(attached_weapon_path, "output/distributions/json/")
    parse_clothing(clothing_file_path, guid_table_path, "output/distributions/json/clothing.json")
    parse_stories(class_files_directory, "output/distributions/json/stories.json")


# Function to check if all resources are found
def init(*file_paths):
    missing_files = []

    for path in file_paths:
        if not os.path.exists(path):
            missing_files.append(path)

    if not missing_files:
        print("All resources are found.")
    else:
        for missing in missing_files:
            print(f"Resource missing: {missing}")


if __name__ == "__main__":
    main()
