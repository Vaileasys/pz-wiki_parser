import json
import os
import re
import tqdm
import scripts.distribution_parser as distribution_parser

# Dictionary to store changes for reference across the script
item_name_changes = {}

def load_item_dictionary(item_name):
    """Load and search for a modified item name based on a dictionary in itemname_en.txt."""
    file_path = "resources/itemname_en.txt"  # Assuming the file path

    if not os.path.exists(file_path):
        return item_name  # If the file doesn't exist, return the original item name

    # Manually parse the dictionary file
    item_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("ItemName_Base"):
                # Extract key and value from lines formatted as `ItemName_Base.something = "Something",`
                try:
                    key, value = line.split(" = ")
                    key = key.strip()  # The full key e.g., ItemName_Base.223Box
                    value = value.strip().strip('",')  # Strip quotes and trailing comma

                    item_dict[key] = value
                except ValueError:
                    continue  # Skip lines that don't fit the format

    # Format item name for comparison: remove spaces and surround with double quotes
    formatted_item_name = f'"{item_name.replace(" ", "")}"'

    # Search values for a match
    for key, value in item_dict.items():
        if formatted_item_name == f'"{value.replace(" ", "")}"':
            # Match found; extract new item ID from the key
            new_item_id = key.split(".", 1)[1]
            item_name_changes[item_name] = new_item_id  # Store original and new item name
            return new_item_id

    # If no match is found, return the original item name
    return item_name


def process_json(file_paths):
    """
    Process JSON files and gather a list of unique items and their counts.

    Parameters
    ----------
    file_paths : dict
        A dictionary mapping file keys to file paths. The supported file keys are:
            - "proceduraldistributions" : A JSON file containing procedural distribution data.
            - "foraging" : A JSON file containing foraging data.
            - "vehicle_distributions" : A JSON file containing vehicle distribution data.
            - "clothing" : A JSON file containing clothing data.
            - "attached_weapons" : A JSON file containing attached weapon data.
            - "stories" : A JSON file containing story data.

    Returns
    -------
    item_list : set
        A set of unique items found in the input JSON files.

    Notes
    -----
    This function processes the input JSON files and stores the results in a dictionary.
    The dictionary is then saved to a file named "item_list.txt" in the "output/distributions" directory.
    The function also saves the changes dictionary to a file named "item_name_changes.json" in the same directory.
    """
    item_list = set()
    item_counts = {}

    for file_key, file_path in file_paths.items():
        with open(file_path, "r") as file:
            data = json.load(file)
            count = 0

            if file_key == "proceduraldistributions":
                for distribution, content in data.items():
                    items = content.get("items", [])
                    for entry in items:
                        item_list.add(entry["name"])
                        count += 1
                    junk_items = content.get("junk", {}).get("items", [])
                    for entry in junk_items:
                        item_list.add(entry["name"])
                        count += 1

            elif file_key == "foraging":
                for key, entry in data.items():
                    item_type = entry.get("type", "")
                    item_type = re.sub(r"^(Base\.|Radio\.|Farming\.)", "", item_type)
                    item_list.add(item_type)
                    count += 1

            elif file_key == "vehicle_distributions":
                for zone, details in data.items():
                    items = details.get("items", {})
                    item_list.update(items.keys())
                    count += len(items)
                    if "junk" in details:
                        junk_items = details["junk"].get("items", {})
                        item_list.update(junk_items.keys())
                        count += len(junk_items)

            elif file_key == "clothing":
                for outfit, details in data.items():
                    for outfit_details in details.values():
                        items = outfit_details.get("Items", [])
                        item_list.update(items)
                        count += len(items)

            elif file_key == "attached_weapons":
                for weapon_config, details in data.items():
                    weapons = details.get("weapons", [])
                    for weapon in weapons:
                        weapon = re.sub(r"^Base\.", "", weapon)
                        item_list.add(weapon)
                        count += 1

            elif file_key == "stories":
                for story_key, items in data.items():
                    for item in items:
                        # Update item name if found in the dictionary
                        item = load_item_dictionary(item)
                        item_list.add(item)
                        count += 1

            cleaned_item_list = set()

            for item in item_list:
                if '.' in item:
                    item = item.split('.', 1)[1]
                cleaned_item_list.add(item)

            item_list = cleaned_item_list

            item_counts[file_key] = count

    print(f"Unique items found: {len(item_list)}")
    for file_key, count in item_counts.items():
        print(f"Total items found in {file_key}: {count}")

    os.makedirs("output", exist_ok=True)
    with open("output/distributions/Item_list.txt", "w") as output_file:
        for item in sorted(item_list):
            output_file.write(item + "\n")

    # Save the changes dictionary for reference
    with open("output/distributions/json/item_name_changes.json", "w") as changes_file:
        json.dump(item_name_changes, changes_file, indent=4)

    return item_list


def build_item_json(item_list, procedural_data, distribution_data, vehicle_data, foraging_data, attached_weapons_data,
                    clothing_data, stories_data):
    """
    Build a JSON file containing item data.

    Parameters
    ----------
    item_list : list
        A list of unique items found in the input JSON files.
    procedural_data : dict
        A dictionary containing procedural distribution data.
    distribution_data : dict
        A dictionary containing distribution data.
    vehicle_data : dict
        A dictionary containing vehicle distribution data.
    foraging_data : dict
        A dictionary containing foraging data.
    attached_weapons_data : dict
        A dictionary containing attached weapon data.
    clothing_data : dict
        A dictionary containing clothing data.
    stories_data : dict
        A dictionary containing story data.

    Notes
    -----
    This function processes the input data and stores the results in a dictionary.
    The dictionary is then saved to a file named "all_items.json" in the "output/distributions/json" directory.
    """
    def get_container_info(item_name):
        containers_info = []
        for proclist, content in procedural_data.items():
            items = content.get("items", [])
            rolls = content.get("rolls", 0)
            for entry in items:
                if entry["name"] == item_name:
                    chance = entry["chance"]
                    for room, room_content in distribution_data.items():
                        for container, container_content in room_content.items():
                            proc_lists = container_content.get("procList", [])
                            for proc_entry in proc_lists:
                                if proc_entry.get("name") == proclist:
                                    containers_info.append({
                                        "Room": room,
                                        "Container": container,
                                        "Proclist": proclist,
                                        "Chance": chance,
                                        "Rolls": rolls
                                    })
        return containers_info

    def get_vehicle_info(item_name):
        vehicles_info = []
        for label, details in vehicle_data.items():
            # Split the label using camel case
            type_parts = re.findall(r'[A-Z][^A-Z]*', label)

            # Apply specific rules to determine vehicle_type and container
            if type_parts[0] == "Mc" and len(type_parts) > 1:
                vehicle_type = type_parts[0] + type_parts[1]
                container = ' '.join(type_parts[2:])
            elif ' '.join(type_parts[:2]) == "Metal Welder" and len(type_parts) > 2:
                vehicle_type = ' '.join(type_parts[:2])
                container = ' '.join(type_parts[2:])
            elif ' '.join(type_parts[:3]) == "Mass Gen Fac" and len(type_parts) > 3:
                vehicle_type = ' '.join(type_parts[:3])
                container = ' '.join(type_parts[3:])
            elif ' '.join(type_parts[:2]) == "Construction Worker" and len(type_parts) > 2:
                vehicle_type = ' '.join(type_parts[:2])
                container = ' '.join(type_parts[2:])
            elif type_parts[0] == "Glove" or ' '.join(type_parts[:2]) == "Glove box":
                vehicle_type = "All"
                container = ' '.join(type_parts)
            elif type_parts[0] == "Trunk":
                vehicle_type = ' '.join(type_parts[1:])
                container = type_parts[0]
            else:
                vehicle_type = type_parts[0]
                container = ' '.join(type_parts[1:])

            # Normalize container name for "Glovebox"
            if container.lower() == "glovebox":
                container = "Glove Box"

            # Process item details
            rolls = details.get("rolls", 0)
            items = details.get("items", {})
            if item_name in items:
                chance = items[item_name]
                vehicles_info.append({
                    "Type": vehicle_type,
                    "Container": container,
                    "Chance": chance,
                    "Rolls": rolls
                })
            junk_items = details.get("junk", {}).get("items", {})
            if item_name in junk_items:
                chance = junk_items[item_name]
                vehicles_info.append({
                    "Type": vehicle_type,
                    "Container": container,
                    "Chance": chance,
                    "Rolls": rolls
                })

        return vehicles_info

    def get_foraging_info(item_name):
        item_info = foraging_data.get(item_name, {})
        relevant_data = {}

        parameters = [
            "skill", "chance", "zones", "categories", "xp", "minCount",
            "maxCount", "months", "bonusMonths", "malusMonths",
            "snowChance", "rainChance", "dayChance", "nightChance"
        ]

        for param in parameters:
            if param in item_info:
                relevant_data[param] = item_info[param]

        return relevant_data

    def get_attached_weapon_info(item_name):
        attached_weapon_matches = []

        for weapon_config, details in attached_weapons_data.items():
            # Check if the item_name exists in the list of weapons
            weapons = details.get("weapons", [])
            if item_name in weapons:
                # Assign "Any" to outfit if it isn't specified in the details
                outfits = details.get("outfit", "Any")
                day_survived = details.get("daySurvived", 0)
                chance = details.get("chance", 0)

                # Ensure `outfits` is a list even if set to "Any"
                if not isinstance(outfits, list):
                    outfits = [outfits]

                # Append each configuration to the matches list
                for outfit in outfits:
                    attached_weapon_matches.append({
                        "outfit": outfit,
                        "daySurvived": day_survived,
                        "chance": chance
                    })

        return attached_weapon_matches

    def get_clothing_info(item_name):
        clothing_matches = []

        for gender_outfits in ["FemaleOutfits", "MaleOutfits"]:
            if gender_outfits in clothing_data:
                for outfit_name, outfit_details in clothing_data[gender_outfits].items():
                    items = outfit_details.get("Items", {})
                    if item_name in items:
                        guid = outfit_details.get("GUID", "")
                        chance = items[item_name]
                        clothing_matches.append({
                            "GUID": guid,
                            "Outfit": outfit_name,
                            "Chance": chance
                        })

        return clothing_matches

    def get_story_info(item_name):
        matching_stories = []
        for story_category, items in stories_data.items():
            if item_name in items:
                matching_stories.append(story_category)
        return matching_stories

    all_items = {}

    for item in tqdm.tqdm(item_list, desc="Building item data"):
        item_name = item_name_changes.get(item, item)  # Apply any saved name changes
        all_items[item_name] = {
            "name": item_name,
            "Containers": get_container_info(item_name),
            "Vehicles": get_vehicle_info(item_name),
            "Foraging": get_foraging_info(item_name),
            "AttachedWeapon": get_attached_weapon_info(item_name),  # Assign attached weapon info
            "Clothing": get_clothing_info(item_name),
            "Stories": get_story_info(item_name)
        }

        # Output to JSON file
    os.makedirs("output", exist_ok=True)
    with open("output/distributions/json/all_items.json", "w") as json_file:
        json.dump(all_items, json_file, indent=4)
    print("Completed building JSON file")


def build_tables():
    # Load the JSON data
    """
    Builds distribution tables for all items.

    Reads the JSON data file created by `build_json`, processes each item, and creates a table
    containing all the relevant distribution information. The table is then written to a file
    in the specified output directory.

    The output directory is created if it does not exist. The file name is in the format
    `<item_id>.txt`, where `<item_id>` is the ID of the item.
    """
    with open("output/distributions/json/all_items.json", "r") as file:
        all_items = json.load(file)

    # Create the output directory if it doesn't exist
    output_dir = "output/distributions/complete"
    os.makedirs(output_dir, exist_ok=True)


    # Helper functions to process each type
    def process_containers(containers_list):
        container_lines = []

        for container in containers_list:
            room = container["Room"]
            container_name = container["Container"]
            chance = container["Chance"]
            rolls = container["Rolls"]

            # Calculate effective_chance
            effective_chance = round((1 - (1 - ((1 + ((100 * chance * 0.6) + (10 * rolls))) / 10000)) ** rolls) * 100,
                                     2)

            # Format each line with the specified format
            container_line = f"{{{{!}}}} {room} {{{{!}}}}{{{{!}}}} {{{{ll|{container_name}}}}} {{{{!}}}}{{{{!}}}} {effective_chance}%"
            container_lines.append(container_line)

        # Join lines with `{{!}}-` only if there are two or more entries
        if len(container_lines) > 1:
            content = "\n{{!}}-\n".join(container_lines)
        else:
            content = "\n".join(container_lines)

        # Prepend "|Containers=" to the final content
        return f"|container=\n{content}"


    def process_vehicles(vehicles_list):
        vehicle_lines = []

        for vehicle in vehicles_list:
            type_ = vehicle["Type"]
            container = vehicle["Container"]
            chance = vehicle["Chance"]
            rolls = vehicle["Rolls"]

            # Calculate effective chance
            effective_chance = round((1 - (1 - ((1 + ((100 * chance * 0.6) + (10 * rolls))) / 10000)) ** rolls) * 100,
                                     2)

            # Format each line with the specified format
            vehicle_line = f"{{{{!}}}} {type_} {{{{!}}}}{{{{!}}}} {{{{ll|{container}}}}} {{{{!}}}}{{{{!}}}} {effective_chance}%"
            vehicle_lines.append(vehicle_line)

        # Join lines with `{{!}}-` only if there are two or more entries
        if len(vehicle_lines) > 1:
            content = "\n{{!}}-\n".join(vehicle_lines)
        else:
            content = "\n".join(vehicle_lines)

        # Prepend "|vehicle=" to the final content
        return f"|vehicle=\n{content}"


    def process_attached_weapon(attached_weapon_list):
        attached_weapon_lines = []

        for weapon in attached_weapon_list:
            outfit = weapon["outfit"]
            day_survived = weapon.get("daySurvived", 0)
            chance = weapon.get("chance", 0)

            # Format the line using the provided template
            body_line = f"{{{{!}}}} {outfit} {{{{!}}}}{{{{!}}}} {day_survived} {{{{!}}}}{{{{!}}}} {chance}"
            attached_weapon_lines.append(body_line)

        # Join lines with `{{!}}-` only if there are two or more entries
        if len(attached_weapon_lines) > 1:
            content = "\n{{!}}-\n".join(attached_weapon_lines)
        else:
            content = "\n".join(attached_weapon_lines)

        # Prepend "|zombie=" to the final content
        return f"|zombie=\n{content}"


    def process_clothing(clothing_list):
        clothing_lines = []

        for clothing in clothing_list:
            guid = clothing["GUID"]
            outfit = clothing["Outfit"]
            chance = clothing["Chance"]

            # Format each line using the specified template
            container_line = f"{{{{!}}}} {outfit} {{{{!}}}}{{{{!}}}} {chance} {{{{!}}}}{{{{!}}}} {guid}"
            clothing_lines.append(container_line)

        # Join lines with `{{!}}-` only if there are two or more entries
        if len(clothing_lines) > 1:
            content = "\n{{!}}-\n".join(clothing_lines)
        else:
            content = "\n".join(clothing_lines)

        # Prepend "|clothing=" to the final content
        return f"|outfit=\n{content}"


    def process_stories(stories_list):
        story_lines = []

        for story in stories_list:
            # Determine the link based on the prefix of the story
            if story.startswith("RZS"):
                link = "Zone stories"
            elif story.startswith("RBTS"):
                link = "Table stories"
            elif story.startswith("RB") and not story.startswith("RBTS"):
                link = "Building stories"
            elif story.startswith("RVS"):
                link = "Vehicle stories"
            else:
                link = "Randomized stories"

            # Format each story line with the specified template
            story_line = f"{{{{!}}}} {story} {{{{!}}}}{{{{!}}}} {{{{ll|{link}}}}}"
            story_lines.append(story_line)

        # Join all story lines with `{{!}}-` if there are multiple entries
        if len(story_lines) > 1:
            content = "\n{{!}}-\n".join(story_lines)
        else:
            content = "\n".join(story_lines)

        # Prepend "|story=" to the final content
        return f"|stories=\n{content}"


    def process_foraging(foraging_data):
        # Helper function to convert month indexes to readable month names
        def format_months(month_obj):
            month_names = ["January", "February", "March", "April", "May", "June",
                           "July", "August", "September", "October", "November", "December"]

            sorted_keys = sorted(map(int, month_obj.keys()))

            if not sorted_keys:
                return "-"

            # Get the first and last month indices
            start_month = month_names[sorted_keys[0] - 1]
            end_month = month_names[sorted_keys[-1] - 1]

            # Return "X to Y" or just "X" if only one month
            return f"{start_month} to {end_month}" if start_month != end_month else start_month

        # Extract and format each component
        min_count = foraging_data.get("minCount")
        max_count = foraging_data.get("maxCount")
        amount = f"{min_count}-{max_count}" if min_count is not None and max_count is not None else "-"

        if amount == "---" or amount == "-":
            amount = "1"

        skill_level = foraging_data.get("skill", "-")

        # Formatting Biomes with line breaks if multiple zones exist
        zones = foraging_data.get("zones", {})
        biomes = "<br>".join([f"{zone}: {value}" for zone, value in zones.items()]) if zones else "-"

        snow = foraging_data.get("snowChance", "-")
        rain = foraging_data.get("rainChance", "-")
        day = foraging_data.get("dayChance", "-")
        night = foraging_data.get("nightChance", "-")

        # Formatting months available, bonus months, and malus months
        months_available = format_months(foraging_data.get("months", {}))
        bonus_months = format_months(foraging_data.get("bonusMonths", {}))
        malus_months = format_months(foraging_data.get("malusMonths", {}))

        # Constructing the formatted string in a single line
        foraging_info = (
            f"|foraging=\n{{{{!}}}} "
            f"{amount} {{{{!}}}}{{{{!}}}}"
            f"{skill_level} {{{{!}}}}{{{{!}}}}"
            f"{biomes} {{{{!}}}}{{{{!}}}}"
            f"{snow} {{{{!}}}}{{{{!}}}}"
            f"{rain} {{{{!}}}}{{{{!}}}}"
            f"{day} {{{{!}}}}{{{{!}}}}"
            f"{night} {{{{!}}}}{{{{!}}}}"
            f"{months_available} {{{{!}}}}{{{{!}}}}"
            f"{bonus_months} {{{{!}}}}{{{{!}}}}"
            f"{malus_months}"
        )

        return foraging_info

    # Process each item and create a table
    for item_id, item_data in tqdm.tqdm(all_items.items(), desc="Processing items"):
        table = f"{{{{Location table|item_id={item_id}"

        # Process each section if it has values
        if item_data.get("Containers"):
            table += "\n" + process_containers(item_data["Containers"])
        if item_data.get("Vehicles"):
            table += "\n" + process_vehicles(item_data["Vehicles"])
        if item_data.get("AttachedWeapon"):
            table += "\n" + process_attached_weapon(item_data["AttachedWeapon"])
        if item_data.get("Stories"):
            table += "\n" + process_stories(item_data["Stories"])
        if item_data.get("Clothing"):
            table += "\n" + process_clothing(item_data["Clothing"])
        if item_data.get("Foraging"):
            table += "\n" + process_foraging(item_data["Foraging"])

        # Close the table format
        table += "\n}}"

        # Write the table to a file
        with open(f"{output_dir}/{item_id}.txt", "w") as output_file:
            output_file.write(table)


def calculate_missing_items(itemname_path, itemlist_path, missing_items_path):
    """
    Calculate and output the missing items between ItemName_EN.txt and Item_list.txt.

    This function takes three parameters: the path to the ItemName_EN.txt file, the path to the Item_list.txt file,
    and the path to the output file that will contain only the keys of the items that are missing.

    The function creates a dictionary from the ItemName_EN.txt file, loads the keys to remove from the Item_list.txt
    file, removes any matching keys from the dictionary, and then outputs only the keys of the filtered dictionary to
    the output file.

    The output file will contain one key per line.
    """
    with open(itemname_path, 'r') as file:
        item_dict = {}

        # Process each line in the file
        for line in file:
            # Check for lines that contain both '.' and '='
            if '.' in line and '=' in line:
                # Remove the part before and including the first period, then split by '='
                key = line.split('.')[1].split('=')[0].strip()
                value = line.split('=')[1].strip().strip('"').strip(',')

                # Add to dictionary
                item_dict[key] = value

    # Load the list of keys to remove from Item_list.txt
    with open(itemlist_path, 'r') as key_file:
        keys_to_remove = {line.strip() for line in key_file}

    # Remove any matching keys from the dictionary
    filtered_dict = {k: v for k, v in item_dict.items() if k not in keys_to_remove}

    # Output only the keys of the filtered dictionary to missing_items.txt
    with open(missing_items_path, 'w') as output_file:
        for key in filtered_dict.keys():
            output_file.write(f"{key}\n")


def main():
    file_paths = {
        "proceduraldistributions": "output/distributions/json/proceduraldistributions.json",
        "foraging": "output/distributions/json/foraging.json",
        "vehicle_distributions": "output/distributions/json/vehicle_distributions.json",
        "clothing": "output/distributions/json/clothing.json",
        "attached_weapons": "output/distributions/json/attached_weapons.json",
        "stories": "output/distributions/json/stories.json",
        "distributions": "output/distributions/json/distributions.json"
    }

    distribution_parser.main()
    item_list = process_json(file_paths)

    with open(file_paths["proceduraldistributions"], "r") as proc_file:
        procedural_data = json.load(proc_file)

    with open(file_paths["distributions"], "r") as dist_file:
        distribution_data = json.load(dist_file)

    with open(file_paths["vehicle_distributions"], "r") as vehicle_file:
        vehicle_data = json.load(vehicle_file)

    with open(file_paths["foraging"], "r") as foraging_file:
        foraging_data = json.load(foraging_file)

    with open(file_paths["attached_weapons"], "r") as attached_weapons_file:
        attached_weapons_data = json.load(attached_weapons_file)

    with open(file_paths["clothing"], "r") as clothing_file:
        clothing_data = json.load(clothing_file)

    with open(file_paths["stories"], "r") as stories_file:
        stories_data = json.load(stories_file)

    build_item_json(item_list, procedural_data, distribution_data, vehicle_data, foraging_data, attached_weapons_data,
                    clothing_data, stories_data)

    build_tables()

    itemname_path = "resources/Translate/EN/ItemName_EN.txt"
    itemlist_path = "output/distributions/Item_list.txt"
    missing_items_path = "output/distributions/missing_items.txt"

    calculate_missing_items(itemname_path, itemlist_path, missing_items_path)


if __name__ == "__main__":
    main()
