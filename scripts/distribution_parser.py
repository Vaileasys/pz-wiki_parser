import os
import json
import re
import struct
import lupa
from lupa import LuaRuntime
import xml.etree.ElementTree as ET


def parse_container_files(distributions_lua_path, procedural_distributions_path, output_path):
    """
    Parses Lua container files to extract distribution data and convert it to JSON format.
    Includes debug statements at each step for troubleshooting.
    """
    os.makedirs(output_path, exist_ok=True)

    def lua_table_to_python(obj):
        if isinstance(obj, dict):
            return {k: lua_table_to_python(v) for k, v in obj.items()}
        elif hasattr(obj, 'items'):
            return {k: lua_table_to_python(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [lua_table_to_python(item) for item in obj]
        return obj

    def read_and_modify_lua_file(filename, table_name):
        with open(filename, 'r', encoding='utf-8') as file:
            lua_content = file.read()
        # Make local table global if needed
        if f"local {table_name}" in lua_content:
            lua_content = lua_content.replace(f"local {table_name}", table_name)
        return lua_content

    def distributions_parser(lua_code, procedural_memory):
        lua = LuaRuntime(unpack_returned_tuples=True)

        # Load clutter tables first
        distributions_dir = os.path.dirname(distributions_lua_path)
        clutter_files = [
            "Distribution_BinJunk.lua",
            "Distribution_ShelfJunk.lua",
            "Distribution_BagsAndContainers.lua",
            "Distribution_ClosetJunk.lua",
            "Distribution_CounterJunk.lua",
            "Distribution_DeskJunk.lua",
            "Distribution_SideTableJunk.lua"
        ]

        for cf in clutter_files:
            cf_path = os.path.join(distributions_dir, cf)
            if os.path.exists(cf_path):
                with open(cf_path, 'r', encoding='utf-8') as cff:
                    lua_code_clutter = cff.read()
                    lua.execute(lua_code_clutter)

        lua.execute('function pz_is_table(x) return type(x) == "table" end')
        lua.execute(lua_code)

        distribution_table = lua.globals().distributionTable

        def remove_prefixes(name):
            prefixes = ["Base.", "Farming.", "Radio.", "Camping.", "farming.", "radio.", "camping."]
            for prefix in prefixes:
                if name.startswith(prefix):
                    return name[len(prefix):]
            return name

        output_json = {}
        pz_is_table = lua.globals().pz_is_table

        for room_name, room_content in distribution_table.items():
            containers = {}
            if pz_is_table(room_content):
                # Convert room_content to Python before processing
                python_room_content = lua_table_to_python(room_content)
                for container_name, container_content in python_room_content.items():
                    if not isinstance(container_content, dict):
                        continue
                    container_details = {}
                    if 'procedural' in container_content and container_content['procedural']:
                        container_details['procedural'] = True
                        if 'procList' in container_content:
                            container_details['procList'] = []
                            for i in range(1, len(container_content['procList']) + 1):
                                item = container_content['procList'][i]
                                if isinstance(item, dict):
                                    # item is already Python dict, safe to use .get()
                                    container_details['procList'].append({
                                        'name': remove_prefixes(item.get('name', '')),
                                        'min': item.get('min', 0),
                                        'max': item.get('max', 0),
                                        'weightChance': item.get('weightChance', None)
                                    })
                        containers[container_name] = container_details
                    else:
                        non_procedural_details = {}
                        if 'rolls' in container_content:
                            non_procedural_details['rolls'] = container_content['rolls']

                        if 'items' in container_content and isinstance(container_content['items'], list):
                            items_list = container_content['items']
                            non_procedural_details['items'] = []
                            for i in range(1, len(items_list), 2):
                                item_name = remove_prefixes(items_list[i])
                                item_chance = items_list[i + 1]
                                non_procedural_details['items'].append({
                                    'name': item_name,
                                    'chance': item_chance
                                })

                        if 'junk' in container_content and 'items' in container_content['junk'] and isinstance(container_content['junk']['items'], list):
                            junk_items_list = container_content['junk']['items']
                            non_procedural_details['junk'] = {
                                'rolls': container_content['junk']['rolls'],
                                'items': []
                            }
                            for i in range(1, len(junk_items_list), 2):
                                item_name = remove_prefixes(junk_items_list[i])
                                item_chance = junk_items_list[i + 1]
                                non_procedural_details['junk']['items'].append({
                                    'name': item_name,
                                    'chance': item_chance
                                })

                        # Append non-procedural tables to procedural_memory
                        procedural_memory[room_name] = procedural_memory.get(room_name, {})
                        procedural_memory[room_name][container_name] = non_procedural_details

            if containers:
                output_json[room_name] = containers

        return lua_table_to_python(output_json)

    def procedural_distributions_parser(lua_code, procedural_memory):
        lua = LuaRuntime(unpack_returned_tuples=True)

        # Just like in distributions_parser, load clutter tables here
        distributions_dir = os.path.dirname(distributions_lua_path)
        clutter_files = [
            "Distribution_BinJunk.lua",
            "Distribution_ShelfJunk.lua",
            "Distribution_BagsAndContainers.lua",
            "Distribution_ClosetJunk.lua",
            "Distribution_CounterJunk.lua",
            "Distribution_DeskJunk.lua",
            "Distribution_SideTableJunk.lua"
        ]

        for cf in clutter_files:
            cf_path = os.path.join(distributions_dir, cf)
            if os.path.exists(cf_path):
                with open(cf_path, 'r', encoding='utf-8') as cff:
                    lua_code_clutter = cff.read()
                    lua.execute(lua_code_clutter)

        # Define pz_is_table after clutter tables are loaded
        lua.execute('function pz_is_table(x) return type(x) == "table" end')

        lua.execute(lua_code)
        distribution_table = lua.globals().ProceduralDistributions.list

        def remove_prefixes(name):
            if not isinstance(name, str):
                name = str(name)

            prefixes = ["Base.", "Farming.", "Radio.", "Camping.", "farming.", "radio.", "camping."]
            for prefix in prefixes:
                if name.startswith(prefix):
                    return name[len(prefix):]
            return name

        pz_is_table = lua.globals().pz_is_table
        output_json = {}

        for table_name, table_content in distribution_table.items():
            if not pz_is_table(table_content):
                continue

            table_details = {}

            if 'rolls' in table_content:
                table_details['rolls'] = table_content['rolls']

            if 'items' in table_content and pz_is_table(table_content['items']):
                items_list = table_content['items']
                table_details['items'] = []
                for i in range(1, len(items_list), 2):
                    item_name = remove_prefixes(items_list[i])
                    item_chance = items_list[i + 1]
                    table_details['items'].append({
                        'name': item_name,
                        'chance': item_chance
                    })

            if 'junk' in table_content and 'items' in table_content['junk'] and pz_is_table(table_content['junk']['items']):
                junk_items_list = table_content['junk']['items']
                table_details['junk'] = {
                    'rolls': table_content['junk']['rolls'],
                    'items': []
                }
                for i in range(1, len(junk_items_list), 2):
                    item_name = remove_prefixes(junk_items_list[i])
                    item_chance = junk_items_list[i + 1]
                    table_details['junk']['items'].append({
                        'name': item_name,
                        'chance': item_chance
                    })

            output_json[table_name] = table_details

        for table_name, table_content in procedural_memory.items():
            if table_name not in output_json:
                output_json[table_name] = table_content
            else:
                output_json[table_name].update(table_content)

        return lua_table_to_python(output_json)

    # Function to save JSON to file
    def save_to_json(data, filename):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    def main():
        lua_code_distributions = read_and_modify_lua_file(distributions_lua_path, 'distributionTable')
        lua_code_procedural = read_and_modify_lua_file(procedural_distributions_path, 'ProceduralDistributions')

        procedural_memory = {}
        room_data = distributions_parser(lua_code_distributions, procedural_memory)
        save_to_json(room_data, os.path.join(output_path, 'distributions.json'))

        procedural_data = procedural_distributions_parser(lua_code_procedural, procedural_memory)
        save_to_json(procedural_data, os.path.join(output_path, 'proceduraldistributions.json'))

    main()


def parse_foraging(forage_definitions_path, output_path):
    """
    Parses foraging-related Lua files and combines their data into a single JSON output.

    This function reads the main forageDefinitions.lua and other foraging-related Lua files, extracts
    relevant data, and augments the extracted data with additional information like item chances. The
    results are then saved into a JSON file.

    Args:
        forage_definitions_path (str): Path to the primary forageDefinitions.lua file.
        output_path (str): Directory where the final foraging JSON will be saved.
    """

    additional_files = [
        "Ammo", "Animals", "Berries", "Clothing", "DeadAnimals", "ForestGoods",
        "ForestRarities", "Fruits", "Herbs", "Insects", "Junk", "Medical",
        "MedicinalPlants", "Mushrooms", "Stones", "Vegetables", "WildPlants"
    ]

    def preprocess_lua_code(lua_code):
        """
        Removes or comments out the `require` statements from Lua code.
        """
        pattern = r'require\s*["\']Foraging/[^"\']*["\']\s*;'
        return re.sub(pattern, '-- [REMOVED] \\g<0>', lua_code)

    def parse_lua_file(file_path):
        """
        Reads and processes a Lua file to extract relevant data.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lua_code = f.read()

            # Preprocess the Lua code to handle `require` statements
            lua_code = preprocess_lua_code(lua_code)

            # Execute the Lua code in the Lua runtime
            lua = LuaRuntime(unpack_returned_tuples=True)

            # Inject global tables and dummy functions to prevent runtime errors
            lua.execute('forageDefs = {}')
            lua.execute('forageSystem = {}')
            lua.execute('forageSystem.worldSprites = { berryBushes = "dummy_texture_path" }')
            lua.execute('function getTexture(path) return path end')

            lua.execute('''
                worldSprites = {
                    add = function() end,
                    remove = function() end,
                    update = function() end
                }
            ''')

            # Execute the Lua script
            lua.execute(lua_code)
            forage_defs = lua.globals().forageDefs
            return lua_table_to_python(forage_defs)
        except Exception as e:
            print(f"Error processing Lua file {file_path}: {e}")
            return {}

    def lua_table_to_python(obj):
        """
        Converts a Lua table to a Python dictionary or list.
        """
        if lupa.lua_type(obj) == 'table':
            py_dict = {}
            for key in obj:
                py_key = key
                py_value = obj[key]
                if lupa.lua_type(py_key) in ('table', 'function'):
                    py_key = str(py_key)
                else:
                    py_key = lua_table_to_python(py_key)

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

    # Parse the main forageDefinitions.lua file
    forage_data = parse_lua_file(forage_definitions_path)

    # Process each additional Lua file and merge its data
    for file_name in additional_files:
        file_path = os.path.join(os.path.dirname(forage_definitions_path), f"{file_name}.lua")
        if os.path.exists(file_path):
            additional_data = parse_lua_file(file_path)
            if additional_data:
                for key, value in additional_data.items():
                    if key in forage_data:
                        forage_data[key].update(value)
                    else:
                        forage_data[key] = value

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Save the combined data to a JSON file
    output_file_path = os.path.join(output_path, 'foraging.json')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(forage_data, f, ensure_ascii=False, indent=4)


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

                if current_key.startswith("Up Truck") and "Pick" in current_key:
                    current_key = current_key.replace("Up Truck", "").strip()
                    current_key = "Pick Up Truck" + current_key

                distribution_dict[current_key] = {'rolls': 1, 'items': {}, 'junk': {}}
                inside_junk = False
                continue
            rolls_match = rolls_pattern.search(line)
            if rolls_match and current_key:
                distribution_dict[current_key]['rolls'] = int(rolls_match.group(1))
            item_match = item_pattern.findall(line)
            if item_match and current_key and not inside_junk:
                for item, weight in item_match:
                    distribution_dict[current_key]['items'][item] = distribution_dict[current_key]['items'].get(item,
                                                                                                                0) + float(
                        weight)
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
        # Skip the first 8 bytes (magic number and minor/major version)
        initial_bytes = file.read(8)
        if len(initial_bytes) < 8:
            return []

        # Read the constant pool count
        count_bytes = file.read(2)
        if len(count_bytes) < 2:
            return []
        constant_pool_count = struct.unpack(">H", count_bytes)[0] - 1

        constants = []
        i = 0
        while i < constant_pool_count:
            # Attempt to read the tag byte
            tag_byte = file.read(1)
            if len(tag_byte) < 1:
                break  # Stop processing as we've hit EOF prematurely

            tag = struct.unpack("B", tag_byte)[0]

            if tag == 1:  # CONSTANT_Utf8
                length_bytes = file.read(2)
                if len(length_bytes) < 2:
                    break
                length = struct.unpack(">H", length_bytes)[0]
                value = file.read(length)
                if len(value) < length:
                    break
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
                    # Skip non-UTF-8 constants
                    pass
            elif tag in {7, 8}:
                # Skip over 2 bytes (index reference)
                skip_bytes = file.read(2)
                if len(skip_bytes) < 2:
                    break
            elif tag in {3, 4}:
                # Skip over 4 bytes
                skip_bytes = file.read(4)
                if len(skip_bytes) < 4:
                    break
            elif tag in {5, 6}:
                # Skip over 8 bytes
                skip_bytes = file.read(8)
                if len(skip_bytes) < 8:
                    break
                i += 1  # Long/double take two entries
            elif tag in {9, 10, 11, 12, 15, 16, 18}:
                # Skip over 4 bytes
                skip_bytes = file.read(4)
                if len(skip_bytes) < 4:
                    break

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
    clothing_file_path = "resources/clothing/clothing.xml"
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
