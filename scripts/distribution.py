import json
import os
import re
import math
import tqdm
import scripts.parser.distribution_parser as distribution_parser
import scripts.core.utility as utility
from scripts.core.constants import DATA_PATH

cache_path = os.path.join(DATA_PATH, "distributions")

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
                    # Skip lines that don't fit the format
                    pass

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
    """
    item_list = set()
    item_counts = {}

    for file_key, fp in file_paths.items():
        data = utility.load_cache(fp, suppress=False)
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
                    original_item = item
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

    os.makedirs("output/distributions", exist_ok=True)
    with open("output/distributions/Item_list.txt", "w") as output_file:
        for item in sorted(item_list):
            output_file.write(item + "\n")

    utility.save_cache(item_name_changes, "item_name_changes.json", cache_path)

    return item_list


def build_item_json(item_list, procedural_data, distribution_data, vehicle_data, foraging_data, attached_weapons_data,
                    clothing_data, stories_data):
    def get_container_info(item_name):
        containers_info = []
        unique_entries = set()

        def process_nested_object(obj, room_name, container_name=None):
            if "items" in obj:
                items = obj["items"]
                rolls = obj.get("rolls", 0)
                for entry in items:
                    if entry["name"] == item_name:
                        chance = entry["chance"]
                        entry_tuple = (room_name, container_name, chance, rolls)
                        if entry_tuple not in unique_entries:
                            containers_info.append({
                                "Room": room_name,
                                "Container": container_name,
                                "Chance": chance,
                                "Rolls": rolls
                            })
                            unique_entries.add(entry_tuple)
            else:
                for sub_key, sub_value in obj.items():
                    if isinstance(sub_value, dict):
                        process_nested_object(sub_value, room_name, sub_key)

        for proclist, content in procedural_data.items():
            # Process primary items
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
                                    entry_tuple = (room, container, proclist, chance, rolls)
                                    if entry_tuple not in unique_entries:
                                        containers_info.append({
                                            "Room": room,
                                            "Container": container,
                                            "Proclist": proclist,
                                            "Chance": chance,
                                            "Rolls": rolls
                                        })
                                        unique_entries.add(entry_tuple)
            # Process junk items
            junk = content.get("junk", {})
            junk_items = junk.get("items", [])
            junk_rolls = junk.get("rolls", 0)
            for entry in junk_items:
                if entry["name"] == item_name:
                    chance = entry["chance"]
                    for room, room_content in distribution_data.items():
                        for container, container_content in room_content.items():
                            proc_lists = container_content.get("procList", [])
                            for proc_entry in proc_lists:
                                if proc_entry.get("name") == proclist:
                                    entry_tuple = (room, container, proclist, chance, junk_rolls)
                                    if entry_tuple not in unique_entries:
                                        containers_info.append({
                                            "Room": room,
                                            "Container": container,
                                            "Proclist": proclist,
                                            "Chance": chance,
                                            "Rolls": junk_rolls
                                        })
                                        unique_entries.add(entry_tuple)
            # If neither primary items nor junk exist, check nested objects
            if not items and not junk:
                process_nested_object(content, room_name=proclist)
        return containers_info

    def get_vehicle_info(item_name):
        vehicles_info = []
        unique_entries = set()

        for label, details in vehicle_data.items():
            type_parts = re.findall(r'[A-Z][^A-Z]*', label)

            # Various parsing conditions
            if type_parts and type_parts[0] == "Mc" and len(type_parts) > 1:
                vehicle_type = type_parts[0] + type_parts[1]
                container = ' '.join(type_parts[2:])
            elif len(type_parts) > 2 and ' '.join(type_parts[:2]) == "Metal Welder":
                vehicle_type = ' '.join(type_parts[:2])
                container = ' '.join(type_parts[2:])
            elif len(type_parts) > 3 and ' '.join(type_parts[:3]) == "Mass Gen Fac":
                vehicle_type = ' '.join(type_parts[:3])
                container = ' '.join(type_parts[3:])
            elif len(type_parts) > 2 and ' '.join(type_parts[:2]) == "Construction Worker":
                vehicle_type = ' '.join(type_parts[:2])
                container = ' '.join(type_parts[2:])
            elif type_parts and (type_parts[0] == "Glove" or ' '.join(type_parts[:2]) == "Glove box"):
                vehicle_type = "All"
                container = ' '.join(type_parts)
            elif type_parts and type_parts[0] == "Trunk":
                vehicle_type = ' '.join(type_parts[1:])
                container = type_parts[0]
            else:
                vehicle_type = type_parts[0] if type_parts else "Unknown"
                container = ' '.join(type_parts[1:]) if len(type_parts) > 1 else "Unknown"

            # Adjust container and type per rules
            if container.lower() == "glovebox":
                container = "Glove Box"

            if vehicle_type == "Pick" and container.startswith("Up Truck Lights_ Airport"):
                vehicle_type = "Pick Up Truck Lights Airport"
            elif vehicle_type == "Pick":
                vehicle_type = "Pick Up Truck"

            if container.startswith("Up Truck Lights_ Airport"):
                container = container.replace("Up Truck Lights_ Airport", "", 1).strip()
            elif container.startswith("Up Truck"):
                container = container.replace("Up Truck", "", 1).strip()

            rolls = details.get("rolls", 0)
            items = details.get("items", {})

            if item_name in items:
                chance = items[item_name]
                entry_tuple = (vehicle_type, container, chance, rolls)
                if entry_tuple not in unique_entries:
                    vehicles_info.append({
                        "Type": vehicle_type,
                        "Container": container,
                        "Chance": chance,
                        "Rolls": rolls
                    })
                    unique_entries.add(entry_tuple)

            junk_items = details.get("junk", {}).get("items", {})
            if item_name in junk_items:
                chance = junk_items[item_name]
                entry_tuple = (vehicle_type, container, chance, rolls)
                if entry_tuple not in unique_entries:
                    vehicles_info.append({
                        "Type": vehicle_type,
                        "Container": container,
                        "Chance": chance,
                        "Rolls": rolls
                    })
                    unique_entries.add(entry_tuple)

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
            weapons = details.get("weapons", [])
            if item_name in weapons:
                outfits = details.get("outfit", "Any")
                day_survived = details.get("daySurvived", 0)
                chance = details.get("chance", 0)

                if not isinstance(outfits, list):
                    outfits = [outfits]

                for outfit in outfits:
                    attached_weapon_matches.append({
                        "outfit": outfit,
                        "daySurvived": day_survived,
                        "chance": chance
                    })

        return attached_weapon_matches

    def get_clothing_info(item_name, clothing_data):
        clothing_matches = []

        for gender_outfits in ["FemaleOutfits", "MaleOutfits"]:
            gender_outfits_data = clothing_data.get(gender_outfits, {})
            gender = "Female" if gender_outfits == "FemaleOutfits" else "Male"

            for outfit_name, outfit_details in gender_outfits_data.items():
                items = outfit_details.get("Items", {})

                outfit_name_original = outfit_name
                outfit_name = outfit_name.replace("_", "")
                outfit_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', outfit_name)

                if item_name in items:
                    formatted_outfit_name = f"[[{outfit_name} ({gender.lower()} outfit)|{outfit_name} ({gender.lower()})]]"
                    clothing_matches.append({
                        "GUID": outfit_details.get("GUID", ""),
                        "outfit_name": formatted_outfit_name,
                        "Chance": items[item_name],
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
        item_name = item_name_changes.get(item, item)
        all_items[item_name] = {
            "name": item_name,
            "Containers": get_container_info(item_name),
            "Vehicles": get_vehicle_info(item_name),
            "Foraging": get_foraging_info(item_name),
            "AttachedWeapon": get_attached_weapon_info(item_name),
            "Clothing": get_clothing_info(item_name, clothing_data),
            "Stories": get_story_info(item_name)
        }

    utility.save_cache(all_items, "all_items.json", cache_path)


def build_tables():
    json_path = os.path.join(DATA_PATH, "distributions", "all_items.json")
    all_items = utility.load_cache(json_path)

    output_dir = "output/distributions/complete"
    os.makedirs(output_dir, exist_ok=True)

    def process_containers(containers_list):
        container_lines = []
        unique_output_lines = set()

        for container in containers_list:
            room = container["Room"]
            container_name = container["Container"]
            chance = container["Chance"]
            rolls = container["Rolls"]
            loot_rarity = 0.4  # 0.6 B41
            luck_multiplier = 1  # Luck no longer changes, but still calculated
            density = 0.06280941113673441  # 5.2 B41 average

            effective_chance = round((1 - (1 - (math.floor(
                (1 + (100 * chance * loot_rarity * luck_multiplier) + (10 * density))) / 10000)) ** rolls) * 100, 2)

            container_line = f"{{{{!}}}} {room} {{{{!}}}}{{{{!}}}} {{{{ll|{container_name}}}}} {{{{!}}}}{{{{!}}}} {effective_chance}%"

            if container_line not in unique_output_lines:
                container_lines.append((room, container_name, effective_chance, container_line))
                unique_output_lines.add(container_line)

        container_lines.sort(key=lambda x: (x[0].lower(), x[1].lower(), -x[2]))
        content = "\n{{!}}-\n".join(line[3] for line in container_lines)
        return f"|container=\n{content}"

    def process_vehicles(vehicles_list):
        vehicle_lines = []
        unique_output_lines = set()

        for vehicle in vehicles_list:
            type_ = vehicle["Type"]
            container = vehicle["Container"]
            chance = vehicle["Chance"]
            rolls = vehicle["Rolls"]
            loot_rarity = 0.4 #0.6 B41
            luck_multiplier = 1 #Luck no longer changes, but still calculated
            density = 0.06280941113673441 #5.2 B41

            effective_chance = round((1 - (1 - (math.floor(
                (1 + (100 * chance * loot_rarity * luck_multiplier) + (10 * density))) / 10000)) ** rolls) * 100, 2)

            vehicle_line = f"{{{{!}}}} {type_} {{{{!}}}}{{{{!}}}} {{{{ll|{container}}}}} {{{{!}}}}{{{{!}}}} {effective_chance}%"

            if vehicle_line not in unique_output_lines:
                vehicle_lines.append((type_, container, effective_chance, vehicle_line))
                unique_output_lines.add(vehicle_line)

        vehicle_lines.sort(key=lambda x: (x[0].lower(), x[1].lower(), -x[2]))
        content = "\n{{!}}-\n".join(line[3] for line in vehicle_lines)
        return f"|vehicle=\n{content}"

    def process_attached_weapon(attached_weapon_list):
        attached_weapon_lines = []
        for weapon in attached_weapon_list:
            outfit = weapon["outfit"]
            day_survived = weapon.get("daySurvived", 0)
            chance = weapon.get("chance", 0)
            body_line = f"{{{{!}}}} {outfit} {{{{!}}}}{{{{!}}}} {day_survived} {{{{!}}}}{{{{!}}}} {chance}"
            attached_weapon_lines.append((outfit, day_survived, chance, body_line))

        attached_weapon_lines.sort(key=lambda x: (x[0].lower(), x[1], -x[2]))
        content = "\n{{!}}-\n".join(line[3] for line in attached_weapon_lines)
        return f"|zombie=\n{content}"

    def process_clothing(clothing_list):
        clothing_lines = []

        for clothing in clothing_list:
            guid = clothing["GUID"]
            outfit_name = clothing["outfit_name"]
            chance = clothing["Chance"]
            container_line = f"{{{{!}}}} {outfit_name} {{{{!}}}}{{{{!}}}} {chance}% {{{{!}}}}{{{{!}}}} {guid}"
            clothing_lines.append((outfit_name, guid, chance, container_line))

        clothing_lines.sort(key=lambda x: (x[0].lower(), x[1].lower(), -x[2]))
        content = "\n{{!}}-\n".join(line[3] for line in clothing_lines)
        return f"|outfit=\n{content}"

    def process_stories(stories_list):
        story_lines = []
        for story in stories_list:
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

            story_line = f"{{{{!}}}} {story} {{{{!}}}}{{{{!}}}} {{{{ll|{link}}}}}"
            story_lines.append((story, link, story_line))

        story_lines.sort(key=lambda x: (x[0].lower(), x[1].lower()))
        content = "\n{{!}}-\n".join(line[2] for line in story_lines)
        return f"|stories=\n{content}"

    def process_foraging(foraging_data):
        def format_months(month_obj):
            month_names = ["January", "February", "March", "April", "May", "June",
                           "July", "August", "September", "October", "November", "December"]
            sorted_keys = sorted(map(int, month_obj.keys()))
            if not sorted_keys:
                return "-"
            start_month = month_names[sorted_keys[0] - 1]
            end_month = month_names[sorted_keys[-1] - 1]
            return f"{start_month} to {end_month}" if start_month != end_month else start_month

        min_count = foraging_data.get("minCount")
        max_count = foraging_data.get("maxCount")
        amount = f"{min_count}-{max_count}" if min_count is not None and max_count is not None else "-"
        if amount == "---" or amount == "-":
            amount = "1"

        skill_level = foraging_data.get("skill", "-")
        zones = foraging_data.get("zones", {})
        sorted_zones = "<br>".join([f"{zone}: {value}" for zone, value in sorted(zones.items())]) if zones else "-"
        snow = foraging_data.get("snowChance", "-")
        rain = foraging_data.get("rainChance", "-")
        day = foraging_data.get("dayChance", "-")
        night = foraging_data.get("nightChance", "-")

        months_available = format_months(foraging_data.get("months", {}))
        bonus_months = format_months(foraging_data.get("bonusMonths", {}))
        malus_months = format_months(foraging_data.get("malusMonths", {}))

        foraging_info = (
            f"|foraging=\n{{{{!}}}} "
            f"{amount} {{{{!}}}}{{{{!}}}}"
            f"{skill_level} {{{{!}}}}{{{{!}}}}"
            f"{sorted_zones} {{{{!}}}}{{{{!}}}}"
            f"{snow} {{{{!}}}}{{{{!}}}}"
            f"{rain} {{{{!}}}}{{{{!}}}}"
            f"{day} {{{{!}}}}{{{{!}}}}"
            f"{night} {{{{!}}}}{{{{!}}}}"
            f"{months_available} {{{{!}}}}{{{{!}}}}"
            f"{bonus_months} {{{{!}}}}{{{{!}}}}"
            f"{malus_months}"
        )

        return foraging_info

    for item_id, item_data in tqdm.tqdm(all_items.items(), desc="Processing items"):
        table = f"{{{{Location table|item_id={item_id}"

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

        table += "\n}}"
        output_path = f"{output_dir}/{item_id}.txt"
        with open(output_path, "w") as output_file:
            output_file.write(table)


def calculate_missing_items(itemname_path, itemlist_path, missing_items_path):
    with open(itemname_path, 'r') as file:
        item_dict = {}
        for line in file:
            if '.' in line and '=' in line:
                key = line.split('.')[1].split('=')[0].strip()
                value = line.split('=')[1].strip().strip('"').strip(',')
                item_dict[key] = value

    with open(itemlist_path, 'r') as key_file:
        keys_to_remove = {line.strip() for line in key_file}

    filtered_dict = {k: v for k, v in item_dict.items() if k not in keys_to_remove}

    with open(missing_items_path, 'w') as output_file:
        for key in filtered_dict.keys():
            output_file.write(f"{key}\n")


def main():
    file_paths = {
        "proceduraldistributions": DATA_PATH + "/distributions/proceduraldistributions.json",
        "foraging": DATA_PATH + "/distributions/foraging.json",
        "vehicle_distributions": DATA_PATH + "/distributions/vehicle_distributions.json",
        "clothing": DATA_PATH + "/distributions/clothing.json",
        "attached_weapons": DATA_PATH + "/distributions/attached_weapons.json",
        "stories": DATA_PATH + "/distributions/stories.json",
        "distributions": DATA_PATH + "/distributions/distributions.json"
    }

    distribution_parser.main()
    item_list = process_json(file_paths)

    procedural_data = utility.load_cache(file_paths["proceduraldistributions"])

    distribution_data = utility.load_cache(file_paths["distributions"])

    vehicle_data = utility.load_cache(file_paths["vehicle_distributions"])

    foraging_data = utility.load_cache(file_paths["foraging"])

    attached_weapons_data = utility.load_cache(file_paths["attached_weapons"])

    clothing_data = utility.load_cache(file_paths["clothing"])

    stories_data = utility.load_cache(file_paths["stories"])

    build_item_json(item_list, procedural_data, distribution_data, vehicle_data, foraging_data, attached_weapons_data, clothing_data, stories_data)
    build_tables()

    itemname_path = "resources/Translate/EN/ItemName_EN.txt"
    itemlist_path = "output/distributions/Item_list.txt"
    missing_items_path = "output/distributions/missing_items.txt"

    calculate_missing_items(itemname_path, itemlist_path, missing_items_path)
    print("Script completed successfully.")


if __name__ == "__main__":
    main()
