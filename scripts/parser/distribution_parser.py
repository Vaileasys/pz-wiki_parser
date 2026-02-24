import os
import re
import lupa
from lupa import LuaRuntime
import xml.etree.ElementTree as ET
from scripts.core.constants import CACHE_DIR, OUTPUT_DIR
from scripts.core.cache import save_cache
from scripts.core import config_manager as cfg
from scripts.core.file_loading import (
    get_lua_path,
    get_lua_dir,
    get_clothing_dir,
    get_media_dir,
)
from scripts.utils import lua_helper, echo

cache_path = os.path.join(CACHE_DIR, "distributions")


def parse_container_files(
    distributions_lua_path, procedural_distributions_path, output_path
):
    """
    Parses Lua container files to extract distribution data and convert it to JSON format.
    Includes debug statements at each step for troubleshooting.
    """

    def lua_table_to_python(obj):
        if isinstance(obj, dict):
            return {k: lua_table_to_python(v) for k, v in obj.items()}
        elif hasattr(obj, "items"):
            return {k: lua_table_to_python(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [lua_table_to_python(item) for item in obj]
        return obj

    def read_and_modify_lua_file(filename, table_name):
        with open(filename, "r", encoding="utf-8") as file:
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
            "Distribution_SideTableJunk.lua",
        ]

        for cf in clutter_files:
            cf_path = os.path.join(distributions_dir, cf)
            if os.path.exists(cf_path):
                with open(cf_path, "r", encoding="utf-8") as cff:
                    lua_code_clutter = cff.read()
                    lua.execute(lua_code_clutter)

        lua.execute('function pz_is_table(x) return type(x) == "table" end')
        lua.execute(lua_code)

        distribution_table = lua.globals().distributionTable

        def remove_prefixes(name):
            prefixes = ["Base."]
            for prefix in prefixes:
                if name.startswith(prefix):
                    return name[len(prefix) :]
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
                    if (
                        "procedural" in container_content
                        and container_content["procedural"]
                    ):
                        container_details["procedural"] = True
                        if "procList" in container_content:
                            container_details["procList"] = []
                            for i in range(1, len(container_content["procList"]) + 1):
                                item = container_content["procList"][i]
                                if isinstance(item, dict):
                                    # item is already Python dict, safe to use .get()
                                    container_details["procList"].append(
                                        {
                                            "name": remove_prefixes(
                                                item.get("name", "")
                                            ),
                                            "min": item.get("min", 0),
                                            "max": item.get("max", 0),
                                            "weightChance": item.get(
                                                "weightChance", None
                                            ),
                                        }
                                    )
                        containers[container_name] = container_details
                    else:
                        non_procedural_details = {}
                        if "rolls" in container_content:
                            non_procedural_details["rolls"] = container_content["rolls"]

                        if "items" in container_content and isinstance(
                            container_content["items"], list
                        ):
                            items_list = container_content["items"]
                            non_procedural_details["items"] = []
                            for i in range(1, len(items_list), 2):
                                item_name = remove_prefixes(items_list[i])
                                item_chance = items_list[i + 1]
                                non_procedural_details["items"].append(
                                    {"name": item_name, "chance": item_chance}
                                )

                        if (
                            "junk" in container_content
                            and "items" in container_content["junk"]
                            and isinstance(container_content["junk"]["items"], list)
                        ):
                            junk_items_list = container_content["junk"]["items"]
                            non_procedural_details["junk"] = {
                                "rolls": container_content["junk"]["rolls"],
                                "items": [],
                            }
                            for i in range(1, len(junk_items_list), 2):
                                item_name = remove_prefixes(junk_items_list[i])
                                item_chance = junk_items_list[i + 1]
                                non_procedural_details["junk"]["items"].append(
                                    {"name": item_name, "chance": item_chance}
                                )

                        # Append non-procedural tables to procedural_memory
                        procedural_memory[room_name] = procedural_memory.get(
                            room_name, {}
                        )
                        procedural_memory[room_name][container_name] = (
                            non_procedural_details
                        )

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
            "Distribution_SideTableJunk.lua",
        ]

        for cf in clutter_files:
            cf_path = os.path.join(distributions_dir, cf)
            if os.path.exists(cf_path):
                with open(cf_path, "r", encoding="utf-8") as cff:
                    lua_code_clutter = cff.read()
                    lua.execute(lua_code_clutter)

        # Define pz_is_table after clutter tables are loaded
        lua.execute('function pz_is_table(x) return type(x) == "table" end')

        lua.execute(lua_code)
        distribution_table = lua.globals().ProceduralDistributions.list

        def remove_prefixes(name):
            if not isinstance(name, str):
                name = str(name)

            prefixes = [
                "Base.",
                "Farming.",
                "Radio.",
                "Camping.",
                "farming.",
                "radio.",
                "camping.",
            ]
            for prefix in prefixes:
                if name.startswith(prefix):
                    return name[len(prefix) :]
            return name

        pz_is_table = lua.globals().pz_is_table
        output_json = {}

        for table_name, table_content in distribution_table.items():
            if not pz_is_table(table_content):
                continue

            table_details = {}

            if "rolls" in table_content:
                table_details["rolls"] = table_content["rolls"]

            if "items" in table_content and pz_is_table(table_content["items"]):
                items_list = table_content["items"]
                table_details["items"] = []
                for i in range(1, len(items_list), 2):
                    item_name = remove_prefixes(items_list[i])
                    item_chance = items_list[i + 1]
                    table_details["items"].append(
                        {"name": item_name, "chance": item_chance}
                    )

            if (
                "junk" in table_content
                and "items" in table_content["junk"]
                and pz_is_table(table_content["junk"]["items"])
            ):
                junk_items_list = table_content["junk"]["items"]
                table_details["junk"] = {
                    "rolls": table_content["junk"]["rolls"],
                    "items": [],
                }
                for i in range(1, len(junk_items_list), 2):
                    item_name = remove_prefixes(junk_items_list[i])
                    item_chance = junk_items_list[i + 1]
                    table_details["junk"]["items"].append(
                        {"name": item_name, "chance": item_chance}
                    )

            output_json[table_name] = table_details

        for table_name, table_content in procedural_memory.items():
            if table_name not in output_json:
                output_json[table_name] = table_content
            else:
                output_json[table_name].update(table_content)

        return lua_table_to_python(output_json)

    def main():
        lua_code_distributions = read_and_modify_lua_file(
            distributions_lua_path, "distributionTable"
        )
        lua_code_procedural = read_and_modify_lua_file(
            procedural_distributions_path, "ProceduralDistributions"
        )

        procedural_memory = {}
        room_data = distributions_parser(lua_code_distributions, procedural_memory)
        save_cache(room_data, "distributions.json", output_path)

        procedural_data = procedural_distributions_parser(
            lua_code_procedural, procedural_memory
        )
        save_cache(procedural_data, "proceduraldistributions.json", output_path)

    main()


def parse_foraging(output_path):
    """
    Parses foraging-related Lua files and combines their data into a single JSON output.

    This function reads the main forageDefinitions.lua and other foraging-related Lua files, extracts
    relevant data, and augments the extracted data with additional information like item chances. The
    results are then saved into a JSON file.

    Args:
        output_path (str): Directory where the final foraging JSON will be saved.
    """
    # Get the foraging directory from lua_dir + shared/Foraging
    foraging_dir = os.path.join(get_lua_dir(), "shared", "Foraging")
    forage_definitions_path = os.path.join(foraging_dir, "forageDefinitions.lua")

    # Get all .lua files from the Categories subdirectory
    categories_dir = os.path.join(foraging_dir, "Categories")
    additional_files = []

    if os.path.exists(categories_dir):
        for filename in os.listdir(categories_dir):
            if filename.endswith(".lua"):
                # Remove .lua extension to match previous behavior
                additional_files.append(os.path.splitext(filename)[0])
    else:
        echo.warning(f"Categories directory not found at {categories_dir}")

    def preprocess_lua_code(lua_code):
        """
        Removes or comments out the `require` statements from Lua code.
        """
        pattern = r'require\s*["\']Foraging/[^"\']*["\']\s*;'
        return re.sub(pattern, "-- [REMOVED] \\g<0>", lua_code)

    def parse_lua_file(file_path):
        """
        Reads and processes a Lua file to extract relevant data.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lua_code = f.read()

            # Preprocess the Lua code to handle `require` statements
            lua_code = preprocess_lua_code(lua_code)

            # Execute the Lua code in the Lua runtime
            lua = LuaRuntime(unpack_returned_tuples=True)

            # Inject global tables and dummy functions to prevent runtime errors
            lua.execute("forageDefs = {}")
            lua.execute("forageSystem = {}")
            lua.execute(
                'forageSystem.worldSprites = { berryBushes = "dummy_texture_path" }'
            )
            lua.execute("function getTexture(path) return path end")

            lua.execute("""
                worldSprites = {
                    add = function() end,
                    remove = function() end,
                    update = function() end
                }
            """)
            lua.execute(
                "forageSystem.addForageDef = function(itemName, itemDef) forageDefs[itemName] = itemDef end"
            )

            # Execute the Lua script
            lua.execute(lua_code)
            forage_defs = lua.globals().forageDefs
            return lua_table_to_python(forage_defs)
        except Exception as e:
            echo.error(f"Error processing Lua file {file_path}: {e}")
            return {}

    def lua_table_to_python(obj):
        """
        Converts a Lua table to a Python dictionary or list.
        """
        if lupa.lua_type(obj) == "table":
            py_dict = {}
            for key in obj:
                py_key = key
                py_value = obj[key]
                if lupa.lua_type(py_key) in ("table", "function"):
                    py_key = str(py_key)
                else:
                    py_key = lua_table_to_python(py_key)

                if lupa.lua_type(py_value) == "table":
                    py_value = lua_table_to_python(py_value)
                elif lupa.lua_type(py_value) == "function":
                    py_value = str(py_value)
                else:
                    py_value = py_value
                py_dict[py_key] = py_value
            return py_dict
        elif lupa.lua_type(obj) == "function":
            return str(obj)
        else:
            return obj

    # Parse the main forageDefinitions.lua file
    forage_data = parse_lua_file(forage_definitions_path)

    # Process each additional Lua file and merge its data
    for file_name in additional_files:
        file_path = os.path.join(categories_dir, f"{file_name}.lua")
        if os.path.exists(file_path):
            additional_data = parse_lua_file(file_path)
            if additional_data:
                for key, value in additional_data.items():
                    if key in forage_data:
                        forage_data[key].update(value)
                    else:
                        forage_data[key] = value

    # Save the combined data to a JSON file
    save_cache(forage_data, "foraging.json", output_path)


def parse_vehicles(vehicle_distributions_path, output_path):
    """
    Parse the Lua vehicle distribution file and convert it into JSON format.

    Parameters:
        vehicle_distributions_path (str): Path to the Lua file to parse.
        output_path (str): Path where the output JSON file will be written.
    """

    def parse_lua_table(lua_content):
        key_pattern = re.compile(r"VehicleDistributions\.(\w+)\s*=\s*{")
        rolls_pattern = re.compile(r"rolls\s*=\s*(\d+),")
        item_pattern = re.compile(r'"(\w+)"\s*,\s*(\d+\.?\d*),')
        junk_pattern = re.compile(r"junk\s*=\s*{")
        junk_rolls_pattern = re.compile(r"rolls\s*=\s*(\d+),")
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

                distribution_dict[current_key] = {"rolls": 1, "items": {}, "junk": {}}
                inside_junk = False
                continue
            rolls_match = rolls_pattern.search(line)
            if rolls_match and current_key:
                distribution_dict[current_key]["rolls"] = int(rolls_match.group(1))
            item_match = item_pattern.findall(line)
            if item_match and current_key and not inside_junk:
                for item, weight in item_match:
                    distribution_dict[current_key]["items"][item] = distribution_dict[
                        current_key
                    ]["items"].get(item, 0) + float(weight)
            junk_match = junk_pattern.search(line)
            if junk_match and current_key:
                inside_junk = True
                junk_items = []
            junk_rolls_match = junk_rolls_pattern.search(line)
            if junk_rolls_match and inside_junk and current_key:
                distribution_dict[current_key]["junk"]["rolls"] = int(
                    junk_rolls_match.group(1)
                )
            junk_item_match = junk_item_pattern.findall(line)
            if junk_item_match and inside_junk and current_key:
                for item, weight in junk_item_match:
                    junk_items.append((item, float(weight)))
            if inside_junk and "}" in line:
                distribution_dict[current_key]["junk"]["items"] = {
                    item: weight for item, weight in junk_items
                }
                inside_junk = False
        return distribution_dict

    try:
        with open(vehicle_distributions_path, "r", encoding="utf-8") as lua_file:
            lua_content = lua_file.read()
    except FileNotFoundError:
        echo.error(f"Error: The file {vehicle_distributions_path} does not exist.")
        return
    except Exception as e:
        echo.error(f"Error reading {vehicle_distributions_path}: {e}")
        return

    try:
        vehicle_distributions = parse_lua_table(lua_content)
    except Exception as e:
        echo.error(f"Error parsing Lua content: {e}")
        return

    save_cache(vehicle_distributions, "vehicle_distributions.json", output_path)


def parse_clothing(clothing_file_path, guid_table_path, output_file):
    """
    Parse the clothing XML file and generate a JSON file containing outfit data with item probabilities.

    :param clothing_file_path: The path to the clothing XML file
    :param guid_table_path: The path to the GUID table XML file
    :return: None
    """

    def guid_item_mapping(guid_table):
        guid_mapping = {}
        try:
            tree = ET.parse(guid_table)
            root = tree.getroot()
            for file_entry in root.findall("files"):
                path = file_entry.find("path").text
                guid = file_entry.find("guid").text
                filename = os.path.splitext(os.path.basename(path))[0]
                guid_mapping[guid] = filename
        except ET.ParseError as e:
            echo.error(f"Error parsing GUID table XML: {e}")
        return guid_mapping

    def get_outfits(xml_file, guid_mapping):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except ET.ParseError as e:
            echo.error(f"Error parsing clothing XML: {e}")
            return {}

        output_json = {"FemaleOutfits": {}, "MaleOutfits": {}}

        for outfit in root.findall(".//m_FemaleOutfits") + root.findall(
            ".//m_MaleOutfits"
        ):
            outfit_type = (
                "FemaleOutfits" if outfit.tag == "m_FemaleOutfits" else "MaleOutfits"
            )
            outfit_name = (
                outfit.find("m_Name").text
                if outfit.find("m_Name") is not None
                else "Unknown Outfit"
            )
            outfit_guid = (
                outfit.find("m_Guid").text
                if outfit.find("m_Guid") is not None
                else "No GUID"
            )
            items_with_probabilities = {}

            for item_block in outfit.findall("m_items"):
                probability_tag = item_block.find("probability")
                probability = (
                    float(probability_tag.text) * 100
                    if probability_tag is not None
                    else 100
                )
                probability = int(probability)

                item_guid = (
                    item_block.find("itemGUID").text
                    if item_block.find("itemGUID") is not None
                    else None
                )
                if item_guid:
                    item_name = guid_mapping.get(item_guid, item_guid)
                    items_with_probabilities[item_name] = probability

                for subitem in item_block.findall(".//subItems/itemGUID"):
                    subitem_guid = subitem.text
                    subitem_name = guid_mapping.get(subitem_guid, subitem_guid)
                    items_with_probabilities[subitem_name] = (
                        probability  # Apply the same probability for sub-items
                    )

            if outfit_name:
                output_json[outfit_type][outfit_name] = {
                    "GUID": outfit_guid,
                    "Items": items_with_probabilities,
                }

        return output_json

    guid_mapping = guid_item_mapping(guid_table_path)
    outfits_data = get_outfits(clothing_file_path, guid_mapping)

    save_cache(outfits_data, output_file, cache_path)


def check_decompiler_output():
    """
    Check if the ZomboidDecompiler output directory exists.

    Returns:
        bool: True if decompiler output exists, False otherwise
    """
    decompiler_output = os.path.join(OUTPUT_DIR, "ZomboidDecompiler")
    return os.path.exists(decompiler_output) and os.path.isdir(decompiler_output)


def ensure_decompiler_run():
    """
    Ensure the ZomboidDecompiler has been run.
    If not, run it now.

    Returns:
        bool: True if decompiler output exists or was successfully created, False otherwise
    """
    if check_decompiler_output():
        echo.success("ZomboidDecompiler output found. Skipping decompilation.")
        return True

    echo.info("ZomboidDecompiler output not found. Running decompiler...")

    # Check if Java is installed
    import subprocess
    import platform

    try:
        # Check for Java installation
        if platform.system() == "Windows":
            result = subprocess.run(
                ["java", "-version"],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            result = subprocess.run(
                ["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

        if result.returncode != 0:
            echo.error(
                "Error: Java is not installed or not in PATH. Cannot run decompiler."
            )
            return False
    except Exception as e:
        echo.error(f"Error checking Java installation: {e}")
        return False

    # Run the decompiler
    from scripts.core import runner

    result = runner.run_zomboid_decompiler()

    if result:
        echo.warning("Warning: Decompiler may not have completed successfully.")
        return False
    else:
        echo.success("Decompiler completed successfully.")
        return True


def parse_stories(output_file):
    """
    Parses story-related files from the game directory and decompiled Java files.

    This function orchestrates parsing of:
    - Story clutter definitions from Lua files
    - Various story types from decompiled Java files (building, table, survivor, vehicle, zone)

    The parsing process:
    1. Extracts all strings containing "Base." from Java files and removes the prefix
    2. Checks if story clutter category names appear in each Java file
    3. If found, includes all items from that clutter category in the story's item list

    Args:
        output_file (str): Name of the output JSON file (will be saved in cache/distributions/)
    """

    def get_story_files():
        """
        Scans the decompiled Java directory and categorizes story files by prefix.

        Returns:
            dict: Dictionary mapping story types to lists of file paths
        """
        base_path = os.path.join(
            OUTPUT_DIR, "ZomboidDecompiler", "source", "zombie", "randomizedWorld"
        )

        if not os.path.exists(base_path):
            echo.info(f"Warning: Decompiler output directory not found at {base_path}")
            return {}

        # Define file categorization based on prefixes
        # Map file prefixes to story type keys
        prefix_mapping = {
            "RBTS": "random_table",  # Must check RBTS before RB (more specific)
            "RB": "random_building",
            "RDS": "random_survivor",
            "RVS": "random_vehicle",
            "RZS": "random_zone",
        }

        story_files = {
            "random_building": [],
            "random_table": [],
            "random_survivor": [],
            "random_vehicle": [],
            "random_zone": [],
        }

        # Scan all subdirectories for Java files
        for root, dirs, files in os.walk(base_path):
            for filename in files:
                if not filename.endswith(".java"):
                    continue

                # Skip base classes
                if filename.endswith("Base.java"):
                    continue

                # Check prefixes in order (most specific first)
                for prefix, story_type in prefix_mapping.items():
                    if filename.startswith(prefix):
                        file_path = os.path.join(root, filename)
                        story_files[story_type].append(file_path)
                        break

        # Print summary
        total_files = sum(len(files) for files in story_files.values())
        echo.info(f"Found {total_files} story files:")
        for story_type, files in story_files.items():
            if files:
                echo.info(f"  - {story_type}: {len(files)} files")

        return story_files

    def parse_java_story_file(file_path, story_clutter_data):
        """
        Parse a single Java story file and extract item spawn data.

        This function:
        1. Extracts all strings containing "Base." and adds items to the list
        2. Checks if any story clutter category names appear in the file
        3. If found, adds all items from that clutter category to the spawn list

        Args:
            file_path (str): Path to the Java file
            story_clutter_data (dict): Story clutter categories and their items

        Returns:
            dict: Parsed story data with possible item spawns
        """
        filename = os.path.basename(file_path)
        story_id = os.path.splitext(filename)[0]

        try:
            # Read the Java file content
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        except Exception as e:
            echo.error(f"Error reading {filename}: {e}")
            return {"id": story_id, "file": filename, "items": [], "error": str(e)}

        items = []

        # Step 1: Extract all strings containing "Base." between quotes
        # Pattern matches: "Base.ItemName" or 'Base.ItemName'
        # Only captures valid item names (alphanumeric + underscores)
        base_item_pattern = r'["\'](Base\.([A-Za-z0-9_]+))["\']'
        matches = re.findall(base_item_pattern, file_content)

        for match in matches:
            # match is a tuple: (full_string_with_base, item_name_without_base)
            # We want the second element (item name without "Base." prefix)
            item_name = match[1] if isinstance(match, tuple) else match
            if item_name and item_name not in items:
                items.append(item_name)

        # Step 2: Check for story clutter category names in the file
        # and add their items if found
        if story_clutter_data:
            for clutter_category, clutter_items in story_clutter_data.items():
                # Check if this clutter category name appears in the file
                if clutter_category in file_content:
                    # Add all items from this clutter category
                    for clutter_item in clutter_items:
                        if clutter_item not in items:
                            items.append(clutter_item)

        return {
            "id": story_id,
            "file": filename,
            "items": sorted(items),  # Sort for consistent output
            "item_count": len(items),
        }

    def parse_story_clutter():
        """
        Parses StoryClutter_Definitions.lua and extracts all story clutter item definitions.

        Returns:
            dict: Dictionary of story clutter categories and their items
        """
        # Get the game directory from config
        game_directory = cfg.get_game_directory()

        # Construct path to StoryClutter_Definitions.lua
        story_clutter_path = os.path.join(
            game_directory,
            "media",
            "lua",
            "server",
            "RandomizedWorldContent",
            "StoryClutter",
            "StoryClutter_Definitions.lua",
        )

        if not os.path.exists(story_clutter_path):
            echo.warning(
                f"StoryClutter_Definitions.lua not found at {story_clutter_path}"
            )
            echo.info("Skipping story clutter parsing.")
            return {}

        echo.info(f"Parsing StoryClutter_Definitions.lua from {story_clutter_path}")

        try:
            # Read and execute the Lua file using lua_helper
            with open(story_clutter_path, "r", encoding="utf-8") as f:
                lua_code = f.read()

            # Create Lua runtime and execute the code
            lua_runtime = LuaRuntime(unpack_returned_tuples=True)
            lua_runtime.execute(lua_code)

            # Parse the StoryClutter table
            parsed_data = lua_helper.parse_lua_tables(
                lua_runtime, tables=["StoryClutter"]
            )

            if "StoryClutter" not in parsed_data:
                echo.warning("StoryClutter table not found in parsed data")
                return {}

            # Extract and clean the story clutter data
            story_clutter_table = parsed_data["StoryClutter"]
            story_data = {}

            # Process each category in the StoryClutter table
            for category_name, items in story_clutter_table.items():
                if isinstance(items, list):
                    # Clean item names
                    cleaned_items = []
                    for item_name in items:
                        if isinstance(item_name, str):
                            # Remove module prefix
                            clean_name = item_name
                            for prefix in ["Base."]:
                                if clean_name.startswith(prefix):
                                    clean_name = clean_name[len(prefix) :]
                                    break
                            cleaned_items.append(clean_name)

                    story_data[category_name] = cleaned_items

            echo.info(f"Parsed {len(story_data)} story clutter categories")
            return story_data

        except Exception as e:
            echo.error(f"Error parsing StoryClutter_Definitions.lua: {e}")
            import traceback

            traceback.print_exc()
            return {}

    def parse_story_types(story_files, story_clutter_data):
        """
        Parses various story type definitions from decompiled Java classes.

        Args:
            story_files (dict): Dictionary mapping story types to file paths
            story_clutter_data (dict): Story clutter categories and their items

        Returns:
            dict: Dictionary of story types and their parsed data
        """
        story_types = {}

        for story_type, file_paths in story_files.items():
            if not file_paths:
                continue

            echo.info(f"Processing {story_type} stories ({len(file_paths)} files)...")

            story_type_data = {}
            for file_path in file_paths:
                try:
                    parsed_data = parse_java_story_file(file_path, story_clutter_data)
                    story_id = parsed_data.get("id")
                    if story_id:
                        story_type_data[story_id] = parsed_data
                except Exception as e:
                    echo.error(f"Error parsing {file_path}: {e}")
                    continue

            if story_type_data:
                story_types[story_type] = story_type_data

        return story_types

    # Main execution
    all_story_data = {}

    # Parse story clutter from Lua files first (needed for story type parsing)
    story_clutter = parse_story_clutter()
    if story_clutter:
        all_story_data["story_clutter"] = story_clutter

    # Get categorized story files from decompiled Java
    story_files = get_story_files()

    # Parse story types from Java files (pass story_clutter for item resolution)
    if story_files:
        story_types = parse_story_types(story_files, story_clutter)
        if story_types:
            all_story_data["story_types"] = story_types

            # Statistics
            total_stories = sum(len(stories) for stories in story_types.values())
            total_items = 0
            for story_type_data in story_types.values():
                for story_data in story_type_data.values():
                    total_items += story_data.get("item_count", 0)

    # Save to cache/distributions directory
    distributions_cache = os.path.join(CACHE_DIR, "distributions")
    os.makedirs(distributions_cache, exist_ok=True)

    if all_story_data:
        save_cache(all_story_data, output_file, distributions_cache)
        output_path = os.path.join(distributions_cache, output_file)
    else:
        echo.warning("No story data was parsed")


def parse_container_contents(output_path):
    """
    Parse container contents using distribution_container_parser and save to cache.
    This generates the same data as item_container_contents.py but saves it to cache.
    """
    from scripts.parser import distribution_container_parser
    from scripts.objects.item import Item
    from tqdm import tqdm

    def get_probabilities(container_data):
        """
        Calculate probabilities for container contents.
        This matches the calculation from item_container_contents.py
        """

        def calculate_probabilities(items_list, total_rolls, only_one=False):
            """Calculates the probability of each item appearing at least once."""
            item_weights = {}
            total_weight = 0

            # Combine duplicate items, adding weights
            for i in range(0, len(items_list), 2):
                item_name = items_list[i]
                item_weight = items_list[i + 1]

                if item_name in item_weights:
                    item_weights[item_name] += item_weight
                else:
                    item_weights[item_name] = item_weight

                total_weight += item_weight

            # Calculate probability
            probabilities = {}
            for item_name, item_weight in item_weights.items():
                if total_weight > 0:
                    if only_one:
                        # onlyOne = true
                        probability = (item_weight / total_weight) * 100
                        probability = round(probability, 2)
                    else:
                        # Normal calculation
                        single_roll_prob = item_weight / total_weight
                        probability = 1 - (1 - single_roll_prob) ** total_rolls
                        probability = round(probability * 100, 2)
                else:
                    probability = 0

                probabilities[item_name] = probability

            return probabilities

        # Extract item content data
        rolls = container_data.get("rolls", 1)
        junk_data = container_data.get("junk", {})
        junk_rolls = junk_data.get("rolls", 0)
        junk_items = junk_data.get("items", [])
        item_list = container_data.get("items", [])
        only_one = container_data.get("onlyOne", False)

        normal_items = calculate_probabilities(item_list, rolls, only_one)
        junk_items_dict = calculate_probabilities(
            junk_items, junk_rolls, only_one=False
        )

        combined_probabilities = {}
        all_items = set(normal_items.keys()).union(set(junk_items_dict.keys()))

        for item in all_items:
            normal_prob = normal_items.get(item, 0) / 100
            junk_prob = junk_items_dict.get(item, 0) / 100

            combined_prob = normal_prob + junk_prob - (normal_prob * junk_prob)
            combined_prob = round(combined_prob * 100, 2)
            combined_prob = min(combined_prob, 100)

            combined_probabilities[item] = combined_prob

        return {"items": combined_probabilities}

    def find_distro_key(search_dict, search_key):
        """Find which distribution contains the search key."""
        for parent, sub_dict in search_dict.items():
            if isinstance(sub_dict, dict) and search_key in sub_dict:
                return parent
        return None

    def process_item(id_type, distribution_data):
        """Process a single container item and return its contents."""
        has_distro = False
        item_probabilities = {}

        distro_key = find_distro_key(distribution_data, id_type)
        if distro_key:
            has_distro = True
            dist_group = distribution_data[distro_key]
            if isinstance(dist_group, dict):
                container_contents = dist_group.get(id_type)
                if container_contents and isinstance(container_contents, dict):
                    item_probabilities = get_probabilities(container_contents)

        return has_distro, item_probabilities

    # Get distribution data
    distribution_data = distribution_container_parser.get_distribution_data()
    container_dict = {}

    echo.info("Processing container contents...")

    # Get all container items
    try:
        total_items = Item.count()
    except AttributeError:
        # Fallback if Item.count() doesn't work
        total_items = len(list(Item.all()))

    with tqdm(
        total=total_items, desc="Processing container items", unit=" items"
    ) as pbar:
        for item_id in Item.all():
            try:
                item = Item(item_id)
                pbar.set_postfix_str(f"Processing: {item_id[:30]}")

                if item.item_type == "container":
                    has_distro, item_contents = process_item(
                        item.id_type, distribution_data
                    )

                    if has_distro and item_contents.get("items"):
                        container_dict[item_id] = item_contents

            except Exception:
                pass

            pbar.update(1)

    # Save to cache
    save_cache(container_dict, "container_contents.json", output_path)
    echo.info(f"Container contents data saved with {len(container_dict)} containers")


def main():
    """
    Main function to process all distribution data.

    Returns:
        bool: True if processing was successful, False if decompiler check failed
    """
    # Ensure decompiler has been run before proceeding
    if not ensure_decompiler_run():
        echo.error("Cannot continue without decompiler output.")
        echo.error("Please ensure Java is installed and the decompiler can run.")
        return False

    # File paths
    distributions_lua_path = get_lua_path("Distributions")
    procedural_distributions_path = get_lua_path("ProceduralDistributions")
    vehicle_distributions_path = get_lua_path("VehicleDistributions")
    clothing_file_path = os.path.join(get_clothing_dir(), "clothing.xml")
    guid_table_path = os.path.join(get_media_dir(), "fileGuidTable.xml")

    # Foraging path for init check
    foraging_dir = os.path.join(get_lua_dir(), "shared", "Foraging")
    forage_definitions_path = os.path.join(foraging_dir, "forageDefinitions.lua")

    # Call the init function to check if all files exist
    init(
        distributions_lua_path,
        forage_definitions_path,
        procedural_distributions_path,
        vehicle_distributions_path,
        clothing_file_path,
        guid_table_path,
    )

    # Parse files into json
    parse_container_files(
        distributions_lua_path, procedural_distributions_path, cache_path
    )
    parse_foraging(cache_path)
    parse_vehicles(vehicle_distributions_path, cache_path)

    parse_clothing(clothing_file_path, guid_table_path, "clothing.json")
    parse_stories("stories.json")

    # Parse container contents
    parse_container_contents(cache_path)
    return True


# Function to check if all resources are found
def init(*file_paths):
    missing_files = []

    for path in file_paths:
        if not os.path.exists(path):
            missing_files.append(path)

    if not missing_files:
        echo.success("All resources are found.")
    else:
        for missing in missing_files:
            echo.warning(f"Resource missing: {missing}")


if __name__ == "__main__":
    main()
