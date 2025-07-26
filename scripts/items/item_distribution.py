import json
import os
import re
import math
import tqdm
import scripts.parser.distribution_parser as distribution_parser
from scripts.core.constants import DATA_DIR
from scripts.core.cache import save_cache, load_cache
from scripts.utils.categories import find_all_categories
from scripts.utils import lua_helper
from scripts.objects.item import Item
from scripts.objects.fish import Fish

cache_path = os.path.join(DATA_DIR, "distributions")

# Dictionary to store changes for reference across the script
item_name_changes = {}


def load_item_dictionary(item_name):
    """Load and search for a modified item name based on a dictionary in itemname_en.txt."""
    file_path = os.path.join("resources", "itemname_en.txt")

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
        data = load_cache(fp, suppress=False)
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

        elif file_key == "stories":
            for story_key, items in data.items():
                for item in items:
                    # Update item name if found in the dictionary
                    original_item = item
                    item = load_item_dictionary(item)
                    item_list.add(item)
                    count += 1

        elif file_key == "fishing":
            for fish_item_id, fish_data in data.items():
                # Skip non-item entries like "version"
                if fish_item_id == "version" or not isinstance(fish_data, dict):
                    continue
                # Only process items that have fishing-related data structure
                if not ("lure" in fish_data or "isRiver" in fish_data or "isLake" in fish_data):
                    continue
                # Remove "Base." prefix if present to match other item processing
                item_name = fish_item_id.replace("Base.", "") if fish_item_id.startswith("Base.") else fish_item_id
                item_list.add(item_name)
                count += 1

        elif file_key == "butchering":
            # Process butchering data from AnimalPartsDefinitions
            animals_data = data.get("AnimalPartsDefinitions", {}).get("animals", {})
            for animal_name, animal_data in animals_data.items():
                # Process head item
                if "head" in animal_data:
                    head_item = animal_data["head"]
                    head_item = head_item.replace("Base.", "") if head_item.startswith("Base.") else head_item
                    item_list.add(head_item)
                    count += 1
                
                # Process skull item
                if "skull" in animal_data:
                    skull_item = animal_data["skull"]
                    skull_item = skull_item.replace("Base.", "") if skull_item.startswith("Base.") else skull_item
                    item_list.add(skull_item)
                    count += 1
                
                # Process feather item
                if "feather" in animal_data:
                    feather_item = animal_data["feather"]
                    feather_item = feather_item.replace("Base.", "") if feather_item.startswith("Base.") else feather_item
                    item_list.add(feather_item)
                    count += 1
                
                # Process leather item
                if "leather" in animal_data:
                    leather_item = animal_data["leather"]
                    leather_item = leather_item.replace("Base.", "") if leather_item.startswith("Base.") else leather_item
                    item_list.add(leather_item)
                    count += 1
                
                # Process parts items
                if "parts" in animal_data:
                    for part in animal_data["parts"]:
                        part_item = part.get("item", "")
                        part_item = part_item.replace("Base.", "") if part_item.startswith("Base.") else part_item
                        item_list.add(part_item)
                        count += 1
                
                # Process bones items
                if "bones" in animal_data:
                    for bone in animal_data["bones"]:
                        bone_item = bone.get("item", "")
                        bone_item = bone_item.replace("Base.", "") if bone_item.startswith("Base.") else bone_item
                        item_list.add(bone_item)
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

    os.makedirs(os.path.join("output", "distributions"), exist_ok=True)
    with open(os.path.join("output", "distributions", "Item_list.txt"), "w") as output_file:
        for item in sorted(item_list):
            output_file.write(item + "\n")

    save_cache(item_name_changes, "item_name_changes.json", cache_path)

    return item_list


def build_item_json(item_list, procedural_data, distribution_data, vehicle_data, foraging_data,
                    clothing_data, stories_data, fishing_data, butchering_data, attached_weapons_data):
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
        
        # Define known container types to look for at the end of strings
        container_types_suffix = [
            "GloveBox", "TruckBed", 
            "SeatFront", "SeatRear", "Seat",
            "EmptySeat", "DriverSeat"
        ]
        
        # Define container types that appear at the beginning
        container_types_prefix = [
            "Trunk"
        ]
        
        # Define special vehicle prefixes that should be kept together as a unit
        # but will still need proper word splitting for display
        special_vehicles = [
            "PrisonGuard", "PoliceState", "PoliceSheriff", "PoliceDetective", "PoliceSWAT",
            "ArmyLight", "ArmyHeavy", "BadTeens", "PackRat",
            "StepVan_Plonkies", "StepVan_AirportCatering", "VanSeats_AirportShuttle",
            "StepVan_MarineBites", "StepVan_Zippee", "StepVan_Soda", "StepVan_Beer",
            "StepVan_Chips", "StepVan_Windows", "Van_Beer", "StepVan_Genuine_Beer",
            "StepVan_Cereal", "Van_Locksmith", "StepVan_Florist", "Van_CraftSupplies",
            "MobileLibrary", "PickUpTruckLights_Airport", "MetalWelder", "MassGenFac",
            "ConstructionWorker", "KnoxDistillery"
        ]
        
        # Special case abbreviations that should be kept as-is
        abbreviations = ["SWAT", "NNN"]
        
        # Helper function to split camel case strings
        def split_camel_case(name):
            # Special cases
            if name == "PoliceSWAT":
                return "Police SWAT"
            elif name == "Mass Gen Fac":
                return "Mass-Genfac"
                
            # Handle abbreviations first
            for abbr in abbreviations:
                if abbr in name:
                    # Replace abbreviation with a placeholder that won't be split
                    placeholder = f"___{abbr}___"
                    name = name.replace(abbr, placeholder)
            
            # Split camel case
            result = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
            
            # Restore abbreviations
            for abbr in abbreviations:
                placeholder = f"___{abbr}___"
                result = result.replace(placeholder, abbr)
                
            return result
        
        # Helper function to format names with proper spacing
        def format_name(name, is_special_with_underscore=False):
            # Special handling for underscore-containing special vehicles
            if is_special_with_underscore and "_" in name:
                parts = name.split("_")
                # Put words after underscore first, then the part before underscore
                name = parts[1] + " " + parts[0]
            
            # Replace underscores with spaces
            name = name.replace("_", " ")
            
            # Split camel case
            name = split_camel_case(name)
            
            # Ensure abbreviations have spaces after them
            for abbr in abbreviations:
                # Replace abbreviation followed by a letter with abbreviation + space + letter
                name = re.sub(f'({abbr})([a-zA-Z])', r'\1 \2', name)
            
            # Trim any excess whitespace and return
            return name.strip()
        
        for label, details in vehicle_data.items():
            # Skip the "version" entry which isn't a vehicle
            if label == "version":
                continue
                
            # Default values
            vehicle_type = label
            container = "Unknown"
            is_special_with_underscore = False
            
            # First check for container types at the end
            suffix_match = False
            for suffix in container_types_suffix:
                if label.endswith(suffix):
                    container = suffix
                    # Vehicle type is everything before the container suffix
                    vehicle_type = label[:-len(suffix)]
                    suffix_match = True
                    break
            
            # If found a suffix, now check if the vehicle type is a special vehicle
            if suffix_match:
                special_vehicle_match = False
                for special in special_vehicles:
                    if vehicle_type == special:
                        is_special_with_underscore = "_" in special
                        special_vehicle_match = True
                        break
            # If no suffix found, check for container types at the beginning
            else:
                prefix_match = False
                for prefix in container_types_prefix:
                    if label.startswith(prefix):
                        container = prefix
                        # Vehicle type is everything after the container prefix
                        vehicle_type = label[len(prefix):]
                        prefix_match = True
                        break
                
                # If no container type found, check if this is a special vehicle
                if not prefix_match:
                    special_vehicle_match = False
                    for special in special_vehicles:
                        if label == special:
                            vehicle_type = special
                            is_special_with_underscore = "_" in special
                            container = "Base"  # Marking as base entry
                            special_vehicle_match = True
                            break
                    
                    # If not a special vehicle and no container, this might be a base vehicle type
                    if not special_vehicle_match:
                        # Check if this is a base entry (like "Police", "Nurse", etc.)
                        # by looking for corresponding entries with containers
                        is_base_entry = any(entry.startswith(label) and entry != label for entry in vehicle_data.keys())
                        if is_base_entry:
                            vehicle_type = label
                            container = "Base"  # Marking as base entry
            
            # Format the vehicle type and container names for readability
            vehicle_type = format_name(vehicle_type, is_special_with_underscore)
            
            # Format the container name to be more readable
            if container == "GloveBox":
                container = "Glove Box"
            elif container == "TruckBed":
                container = "Truck Bed"
            elif container == "SeatFront":
                container = "Front Seat"
            elif container == "SeatRear":
                container = "Rear Seat"
            elif container == "Trunk":
                container = "Trunk"
            else:
                container = format_name(container)
            
            # Process items in this vehicle container
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
            
            # Process junk items
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
                    clothing_matches.append({
                        "GUID": outfit_details.get("GUID", ""),
                        "outfit_name": f"{outfit_name} ({gender.lower()})",
                        "Chance": items[item_name],
                    })

        return clothing_matches

    def get_story_info(item_name):
        matching_stories = []
        for story_category, items in stories_data.items():
            if item_name in items:
                matching_stories.append({
                    "id": story_category,
                    "link": get_story_link(story_category)
                })
        return matching_stories
    
    def get_story_link(story_category):
        if story_category.startswith("RZS"):
            return "Zone stories"
        elif story_category.startswith("RBTS"):
            return "Table stories"
        elif story_category.startswith("RB") and not story_category.startswith("RBTS"):
            return "Building stories"
        elif story_category.startswith("RVS"):
            return "Vehicle stories"
        else:
            return "Randomized stories"

    def get_fishing_info(item_name):
        fishing_info = {}

        fish_data = None
        if item_name in fishing_data:
            fish_data = fishing_data[item_name]
        elif f"Base.{item_name}" in fishing_data:
            fish_data = fishing_data[f"Base.{item_name}"]
        
        if fish_data:
            # Extract lure information
            lures = []
            if "lure" in fish_data:
                for lure_name, chance in fish_data["lure"].items():
                    lures.append({
                        "name": lure_name,
                        "chance": chance
                    })
            
            # Extract isRiver and isLake booleans
            is_river = fish_data.get("isRiver", False)
            is_lake = fish_data.get("isLake", False)
            
            fishing_info = {
                "lures": lures,
                "isRiver": is_river,
                "isLake": is_lake
            }
        
        return fishing_info

    def get_butchering_info(item_name):
        """
        Get butchering information for an item by finding which animals produce it.
        Returns a list of animals and amounts that produce this item.
        """
        butchering_matches = []
        
        # Process the butchering data to find items
        animals_data = butchering_data.get("AnimalPartsDefinitions", {}).get("animals", {})
        
        for animal_name, animal_data in animals_data.items():
            # Helper function to calculate amount string
            def get_amount_string(item_data):
                if "nb" in item_data:
                    return str(item_data["nb"])
                elif "minNb" in item_data and "maxNb" in item_data:
                    return f"{item_data['minNb']}-{item_data['maxNb']}"
                elif "maxNb" in item_data:
                    return str(item_data["maxNb"])
                elif "minNb" in item_data:
                    return str(item_data["minNb"])
                else:
                    return "1"  # Default amount
            
            # Check head item
            if "head" in animal_data:
                head_item = animal_data["head"]
                head_item_clean = head_item.replace("Base.", "") if head_item.startswith("Base.") else head_item
                if head_item_clean == item_name:
                    butchering_matches.append({
                        "animal": animal_name,
                        "amount": "1",
                        "type": "head"
                    })
            
            # Check skull item
            if "skull" in animal_data:
                skull_item = animal_data["skull"]
                skull_item_clean = skull_item.replace("Base.", "") if skull_item.startswith("Base.") else skull_item
                if skull_item_clean == item_name:
                    butchering_matches.append({
                        "animal": animal_name,
                        "amount": "1",
                        "type": "skull"
                    })
            
            # Check feather item
            if "feather" in animal_data:
                feather_item = animal_data["feather"]
                feather_item_clean = feather_item.replace("Base.", "") if feather_item.startswith("Base.") else feather_item
                if feather_item_clean == item_name:
                    butchering_matches.append({
                        "animal": animal_name,
                        "amount": "1",
                        "type": "feather"
                    })
            
            # Check leather item
            if "leather" in animal_data:
                leather_item = animal_data["leather"]
                leather_item_clean = leather_item.replace("Base.", "") if leather_item.startswith("Base.") else leather_item
                if leather_item_clean == item_name:
                    butchering_matches.append({
                        "animal": animal_name,
                        "amount": "1",
                        "type": "leather"
                    })
            
            # Check parts items
            if "parts" in animal_data:
                for part in animal_data["parts"]:
                    part_item = part.get("item", "")
                    part_item_clean = part_item.replace("Base.", "") if part_item.startswith("Base.") else part_item
                    if part_item_clean == item_name:
                        amount = get_amount_string(part)
                        butchering_matches.append({
                            "animal": animal_name,
                            "amount": amount,
                            "type": "parts"
                        })
            
            # Check bones items
            if "bones" in animal_data:
                for bone in animal_data["bones"]:
                    bone_item = bone.get("item", "")
                    bone_item_clean = bone_item.replace("Base.", "") if bone_item.startswith("Base.") else bone_item
                    if bone_item_clean == item_name:
                        amount = get_amount_string(bone)
                        butchering_matches.append({
                            "animal": animal_name,
                            "amount": amount,
                            "type": "bones"
                        })
        
        return butchering_matches

    def get_attached_weapon_info(item_name, attached_weapons_data):
        """
        Calculate effective spawn chances for attached weapons based on the Java implementation.
        
        This function processes both global definitions and outfit-specific definitions,
        applying the weighted selection algorithm to calculate accurate spawn probabilities.
        
        Returns a list of dictionaries with outfit, definition_id, effective_chance, and days_required.
        """
        attached_weapon_matches = []
        
        # Remove "Base." prefix if it exists for comparison
        item_name_no_prefix = item_name.replace("Base.", "") if item_name.startswith("Base.") else item_name
        full_item_name = f"Base.{item_name_no_prefix}"
        
        # Extract definitions from the parsed data
        definitions_data = attached_weapons_data.get("AttachedWeaponDefinitions", {})
        outfit_definitions_data = definitions_data.get("attachedWeaponCustomOutfit", {})
        
        # Load outfit data for link generation
        from scripts.parser.outfit_parser import get_outfits
        outfits_data = get_outfits()

        def get_days_from_outfit_name(outfit_name):
            """Helper function to determine days required based on outfit name"""
            if "Early" in outfit_name:
                return 10
            elif "Mid" in outfit_name:
                return 30
            elif "Late" in outfit_name:
                return 90
            return 0  # Default if no time period found
        
        # Global definitions (not outfit-specific)
        global_definitions = {}
        for def_name, def_data in definitions_data.items():
            if def_name != "attachedWeaponCustomOutfit" and isinstance(def_data, dict):
                if "weapons" in def_data:
                    global_definitions[def_name] = def_data
        
        # Process global definitions for "Any" outfit
        global_applicable_defs = []
        for def_name, def_data in global_definitions.items():
            weapons = def_data.get("weapons", [])
            # Check if this definition contains our target item
            if any(weapon == full_item_name or weapon == item_name_no_prefix for weapon in weapons):
                # Check if definition name contains time period
                days_required = get_days_from_outfit_name(def_name)
                if days_required == 0:  # If no time period in name, use original value
                    days_required = def_data.get("daySurvived", 0)
                
                global_applicable_defs.append({
                    "name": def_name,
                    "chance": def_data.get("chance", 0),
                    "weapons": weapons,
                    "days_required": days_required,
                    "id": def_data.get("id", def_name),
                    "outfit_filter": def_data.get("outfit", [])
                })
        
        # Calculate global "Any" chances
        if global_applicable_defs:
            # Filter out definitions that require specific outfits for global calculation
            truly_global_defs = [d for d in global_applicable_defs if not d["outfit_filter"]]
            
            if truly_global_defs:
                # Variables for global calculation
                global_base_chance = 0.06  # 6% default sandbox setting
                total_global_weight = sum(d["chance"] for d in truly_global_defs)
                
                for definition in truly_global_defs:
                    definition_selection_weight = definition["chance"] / total_global_weight if total_global_weight > 0 else 0
                    item_selection_weight = 1.0 / len(definition["weapons"])
                    effective_chance_percentage = global_base_chance * definition_selection_weight * item_selection_weight * 100
                    
                    attached_weapon_matches.append({
                        "outfit": "Any",  # Keep "Any" as is - no link needed
                        "definition_id": definition["id"],
                        "effective_chance": round(effective_chance_percentage, 2),
                        "days_required": definition["days_required"]
                    })
        
        # Process outfit-specific definitions
        for outfit_name, outfit_config in outfit_definitions_data.items():
            outfit_base_chance = outfit_config.get("chance", 0) / 100.0
            outfit_weapons = outfit_config.get("weapons", [])
            
            # Check outfit name for time period
            outfit_days_required = get_days_from_outfit_name(outfit_name)
            if outfit_days_required == 0:  # If no time period in name, use original value
                outfit_days_required = outfit_config.get("daySurvived", 0)
            
            # Find applicable weapon definitions for this outfit
            outfit_applicable_defs = []
            for weapon_def in outfit_weapons:
                if isinstance(weapon_def, dict) and "weapons" in weapon_def:
                    weapons = weapon_def.get("weapons", [])
                    # Check if this definition contains our target item
                    if any(weapon == full_item_name or weapon == item_name_no_prefix for weapon in weapons):
                        # Check weapon definition name for time period
                        weapon_days = get_days_from_outfit_name(weapon_def.get("id", ""))
                        if weapon_days == 0:  # If no time period in name, use original value
                            weapon_days = weapon_def.get("daySurvived", 0)
                        
                        # Use the higher value between outfit and weapon definition days required
                        days_required = max(weapon_days, outfit_days_required)
                        
                        outfit_applicable_defs.append({
                            "name": weapon_def.get("id", f"outfit_{outfit_name}"),
                            "chance": weapon_def.get("chance", 0),
                            "weapons": weapons,
                            "days_required": days_required,  # Store the higher value
                            "id": weapon_def.get("id", f"outfit_{outfit_name}")
                        })
            
            # Calculate outfit-specific chances
            if outfit_applicable_defs:
                total_outfit_weight = sum(d["chance"] for d in outfit_applicable_defs)
                
                for definition in outfit_applicable_defs:
                    definition_selection_weight = definition["chance"] / total_outfit_weight if total_outfit_weight > 0 else 0
                    item_selection_weight = 1.0 / len(definition["weapons"])
                    effective_chance_percentage = outfit_base_chance * definition_selection_weight * item_selection_weight * 100
                    
                    attached_weapon_matches.append({
                        "outfit": get_outfit_link(outfit_name, outfits_data),  # Convert outfit name to link
                        "definition_id": definition["id"],
                        "effective_chance": round(effective_chance_percentage, 2),
                        "days_required": definition["days_required"]  # Using the higher value we stored earlier
                    })
        
        # Process global definitions that have outfit filters but can also apply to those specific outfits
        # Collect all unique outfits mentioned in global definitions
        all_mentioned_outfits = set(outfit_definitions_data.keys())
        for definition in global_applicable_defs:
            all_mentioned_outfits.update(definition["outfit_filter"])
        
        for outfit_name in all_mentioned_outfits:
            # Check outfit name for time period
            outfit_days_required = get_days_from_outfit_name(outfit_name)
            if outfit_days_required == 0:  # If no time period in name, use original value
                outfit_days_required = outfit_definitions_data.get(outfit_name, {}).get("daySurvived", 0)
            
            # Check global definitions that specify this outfit
            global_for_outfit = [d for d in global_applicable_defs if outfit_name in d["outfit_filter"]]
            
            if global_for_outfit:
                # Check if this outfit has custom definitions
                if outfit_name in outfit_definitions_data:
                    # This outfit has custom definitions, skip global processing for it
                    # (it was already handled in the outfit-specific section above)
                    continue
                else:
                    # This outfit doesn't have custom definitions, use global 6% chance
                    global_base_chance = 0.06
                    total_weight = sum(d["chance"] for d in global_for_outfit)
                    
                    for definition in global_for_outfit:
                        definition_selection_weight = definition["chance"] / total_weight if total_weight > 0 else 0
                        item_selection_weight = 1.0 / len(definition["weapons"])
                        effective_chance_percentage = global_base_chance * definition_selection_weight * item_selection_weight * 100
                        
                        # Check definition name for time period
                        def_days = get_days_from_outfit_name(definition["id"])
                        if def_days == 0:  # If no time period in name, use original value
                            def_days = definition["days_required"]
                        
                        # Use the higher value between outfit and definition days required
                        days_required = max(def_days, outfit_days_required)
                        
                        attached_weapon_matches.append({
                            "outfit": get_outfit_link(outfit_name, outfits_data),  # Convert outfit name to link
                            "definition_id": definition["id"],
                            "effective_chance": round(effective_chance_percentage, 2),
                            "days_required": days_required
                        })
        
        return attached_weapon_matches

    all_items = {}
    for item in tqdm.tqdm(item_list, desc="Building item data"):
        item_name = item_name_changes.get(item, item)
        all_items[item_name] = {
            "name": item_name,
            "Containers": get_container_info(item_name),
            "Vehicles": get_vehicle_info(item_name),
            "Foraging": get_foraging_info(item_name),
            "Clothing": get_clothing_info(item_name, clothing_data),
            "Stories": get_story_info(item_name),
            "Fishing": get_fishing_info(item_name),
            "Butchering": get_butchering_info(item_name),
            "AttachedWeapons": get_attached_weapon_info(item_name, attached_weapons_data)
        }

    save_cache(all_items, "all_items.json", cache_path)


def build_tables(category_items, index):
    """
    Build Lua tables from pre-categorized item data, organizing items by category.
    Split files that would exceed 2500 lines into multiple numbered files.
    
    Args:
        category_items (dict): Dictionary of items organized by category
        index (dict): Dictionary of item IDs organized by category
        
    Output files to data_files directory with category-based filenames.
    """
    output_dir = os.path.join("output", "distributions", "data_files")
    os.makedirs(output_dir, exist_ok=True)
    
    # Animal data mapping for butchering information
    animal_data = {
        "henleghorn": {"name": "Leghorn Hen", "type": "Chicken"},
        "rabkittencottontail": {"name": "Cottontail Rabbit Kitten", "type": "Rabbit"},
        "mousepupsgolden": {"name": "Golden Mouse Pups", "type": "Mouse"},
        "raccoonkitgrey": {"name": "Grey Raccoon Kit", "type": "Raccoon"},
        "rabdoeswamp": {"name": "Swamp Rabbit Doe", "type": "Rabbit"},
        "ramrambouillet": {"name": "Rambouillet Ram", "type": "Sheep"},
        "ratfemalegrey": {"name": "Grey Female Rat", "type": "Rat"},
        "chickrhodeisland": {"name": "Rhode Island Chick", "type": "Chicken"},
        "raccoonboargrey": {"name": "Grey Raccoon Boar", "type": "Raccoon"},
        "chickleghorn": {"name": "Leghorn Chick", "type": "Chicken"},
        "turkeypoultmeleagris": {"name": "Meleagris Turkey Poult", "type": "Turkey"},
        "raccoonsowgrey": {"name": "Grey Raccoon Sow", "type": "Raccoon"},
        "lambfriesian": {"name": "Friesian Lamb", "type": "Sheep"},
        "mousefemalewhite": {"name": "White Female Mouse", "type": "Mouse"},
        "pigletlargeblack": {"name": "Large Black Piglet", "type": "Pig"},
        "gobblersmeleagris": {"name": "Meleagris Turkey Gobbler", "type": "Turkey"},
        "mousepupswhite": {"name": "White Mouse Pups", "type": "Mouse"},
        "cowcalfholstein": {"name": "Holstein Cow Calf", "type": "Cow"},
        "henrhodeisland": {"name": "Rhode Island Hen", "type": "Chicken"},
        "mousewhite": {"name": "White Mouse", "type": "Mouse"},
        "cowholstein": {"name": "Holstein Cow", "type": "Cow"},
        "mousegolden": {"name": "Golden Mouse", "type": "Mouse"},
        "cowangus": {"name": "Angus Cow", "type": "Cow"},
        "cowcalfangus": {"name": "Angus Cow Calf", "type": "Cow"},
        "sowlandrace": {"name": "Landrace Sow", "type": "Pig"},
        "sowlargeblack": {"name": "Large Black Sow", "type": "Pig"},
        "mousefemaledeer": {"name": "Female Deer Mouse", "type": "Mouse"},
        "cockerelleghorn": {"name": "Leghorn Cockerel", "type": "Chicken"},
        "ewerambouillet": {"name": "Rambouillet Ewe", "type": "Sheep"},
        "rabkittenappalachian": {"name": "Appalachian Rabbit Kitten", "type": "Rabbit"},
        "cockerelrhodeisland": {"name": "Rhode Island Cockerel", "type": "Chicken"},
        "rabbuckcottontail": {"name": "Cottontail Rabbit Buck", "type": "Rabbit"},
        "ramfriesian": {"name": "Friesian Ram", "type": "Sheep"},
        "cowcalfsimmental": {"name": "Simmental Cow Calf", "type": "Cow"},
        "mousefemalegolden": {"name": "Golden Female Mouse", "type": "Mouse"},
        "ewesuffolk": {"name": "Suffolk Ewe", "type": "Sheep"},
        "ratbabywhite": {"name": "White Rat Baby", "type": "Rat"},
        "ramsuffolk": {"name": "Suffolk Ram", "type": "Sheep"},
        "fawnwhitetailed": {"name": "White-tailed Deer Fawn", "type": "Deer"},
        "mousedeer": {"name": "Deer Mouse", "type": "Mouse"},
        "ratgrey": {"name": "Grey Rat", "type": "Rat"},
        "turkeyhenmeleagris": {"name": "Meleagris Turkey Hen", "type": "Turkey"},
        "rabdoecottontail": {"name": "Cottontail Rabbit Doe", "type": "Rabbit"},
        "boarlandrace": {"name": "Landrace Boar", "type": "Pig"},
        "rabdoeappalachian": {"name": "Appalachian Rabbit Doe", "type": "Rabbit"},
        "rabbuckswamp": {"name": "Swamp Rabbit Buck", "type": "Rabbit"},
        "lambsuffolk": {"name": "Suffolk Lamb", "type": "Sheep"},
        "lambrambouillet": {"name": "Rambouillet Lamb", "type": "Sheep"},
        "ratwhite": {"name": "White Rat", "type": "Rat"},
        "ewefriesian": {"name": "Friesian Ewe", "type": "Sheep"},
        "doewhitetailed": {"name": "White-tailed Deer Doe", "type": "Deer"},
        "cowsimmental": {"name": "Simmental Cow", "type": "Cow"},
        "buckwhitetailed": {"name": "White-tailed Deer Buck", "type": "Deer"},
        "boarlargeblack": {"name": "Large Black Boar", "type": "Pig"},
        "ratfemalewhite": {"name": "White Female Rat", "type": "Rat"},
        "bullangus": {"name": "Angus Bull", "type": "Cow"},
        "mousepupsdeer": {"name": "Deer Mouse Pups", "type": "Mouse"},
        "bullholstein": {"name": "Holstein Bull", "type": "Cow"},
        "rabbuckappalachian": {"name": "Appalachian Rabbit Buck", "type": "Rabbit"},
        "bullsimmental": {"name": "Simmental Bull", "type": "Cow"},
        "pigletlandrace": {"name": "Landrace Piglet", "type": "Pig"},
        "ratbabygrey": {"name": "Grey Rat Baby", "type": "Rat"},
        "rabkittenswamp": {"name": "Swamp Rabbit Kitten", "type": "Rabbit"}
    }
    
    # Function to write file header
    def write_header(f, category, part_number=None):
        f.write("--[[\n")
        if part_number:
            f.write(f"Distribution data for {category} items (Part {part_number})\n")
        else:
            f.write(f"Distribution data for {category} items\n")
        f.write("\nData structure:\n")
        f.write("container = {room, container_name, effective_chance}\n")
        f.write("vehicle = {type, container_name, effective_chance}\n")
        f.write("stories = {id, link}\n")
        f.write("outfit = {outfit_name, probability, guid}\n")
        f.write("foraging = {amount, level, snow, rain, day, night, biome_table, months_table, bonus_table, malus_table}\n")
        f.write("fishing = {lure_link, chance}\n")
        f.write("butchering = {animal_name, amount}\n")
        f.write("attachedWeapons = {outfit, definition_id, days_required, effective_chance}\n")
        f.write("--]]\n\n")
        f.write("local data = {\n")


    def effective_chance_calc(rolls, chance):
        """
        Calculate the overall spawn chance (%) over `rolls` attempts,
        given per‐roll `chance`, a loot rarity modifier, luck multiplier,
        raw zombie density, zombie population loot effect, and a global loot multiplier.
        """
        loot_rarity = 0.6  # apocalypse default
        luck_multiplier = 1  # apocalypse default
        density = 0.1536470651626587  # median of various locations, mostly towns and residential sections
        pop_loot_effect = 10  # apocalypse default
        global_multiplier = 1  # apocalypse default

        density_factor = density * pop_loot_effect
        threshold = (chance * 100 * loot_rarity * luck_multiplier + density_factor) * global_multiplier

        # per‐roll probability
        probability = threshold / 10000

        # probability of at least one success in 'rolls' tries
        return round((1 - (1 - probability) ** rolls) * 100, 2)

    # Function to write items to file
    def write_items_to_file(f, items_to_write):
        # Sort items by item_id
        sorted_items = dict(sorted(items_to_write.items()))
        
        for item_id, item_data in sorted_items.items():
            sections = []
            
            # Container data
            if item_data.get("Containers"):
                container_data = []
                for container in item_data["Containers"]:
                    room = container.get("Room", "")
                    container_name = container.get("Container", "")
                    chance = container.get("Chance", 0)
                    rolls = container.get("Rolls", 0)
                    
                    effective_chance = effective_chance_calc(rolls, chance)
                    
                    container_data.append((effective_chance, room, container_name))
                
                if container_data:
                    # Sort by effective chance (descending) first, then alphabetically by room and container
                    container_data.sort(key=lambda x: (-x[0], x[1], x[2]))
                    container_lines = [f'{{"{room}", "{container_name}", {effective_chance}}}' 
                                     for effective_chance, room, container_name in container_data]
                    sections.append(f"    container = {{{','.join(container_lines)}}}")
            
            # Vehicle data
            if item_data.get("Vehicles"):
                vehicle_data = []
                for vehicle in item_data["Vehicles"]:
                    type_ = vehicle.get("Type", "")
                    container = vehicle.get("Container", "")
                    chance = vehicle.get("Chance", 0)
                    rolls = vehicle.get("Rolls", 0)
                    
                    effective_chance = effective_chance_calc(rolls, chance)
                    
                    vehicle_data.append((effective_chance, type_, container))
                
                if vehicle_data:
                    # Sort by effective chance (descending) first, then alphabetically by type and container
                    vehicle_data.sort(key=lambda x: (-x[0], x[1], x[2]))
                    vehicle_lines = [f'{{"{type_}", "{container}", {effective_chance}}}' 
                                   for effective_chance, type_, container in vehicle_data]
                    sections.append(f"    vehicle = {{{','.join(vehicle_lines)}}}")
            
            # Stories data
            if item_data.get("Stories"):
                story_lines = []
                # Sort by story ID A to Z
                stories = sorted(item_data["Stories"], key=lambda x: (x["id"], x["link"]))
                for story in stories:
                    story_lines.append(f'{{"{story["id"]}", "{story["link"]}"}}')
                
                if story_lines:
                    sections.append(f"    stories = {{{','.join(story_lines)}}}")
            

            # Clothing data
            if item_data.get("Clothing"):
                clothing_data = []
                for clothing in item_data["Clothing"]:
                    outfit = clothing.get("outfit_name", "")
                    probability = clothing.get("Chance", 0)
                    guid = clothing.get("GUID", "")
                    clothing_data.append((outfit, probability, guid))  # Restructure for sorting
                
                if clothing_data:
                    # Sort by probability (descending) first, then by outfit name A to Z
                    clothing_data.sort(key=lambda x: (-x[1], x[0], x[2]))
                    clothing_lines = [f'{{"{outfit}", {probability}, "{guid}"}}' 
                                    for outfit, probability, guid in clothing_data]
                    sections.append(f"    outfit = {{{','.join(clothing_lines)}}}")
            
            # Foraging data
            if item_data.get("Foraging") and item_data["Foraging"]:
                foraging = item_data["Foraging"]
                min_count = foraging.get("minCount", 1)
                max_count = foraging.get("maxCount", 1)
                amount = f"{min_count}-{max_count}" if min_count != max_count else f"{min_count}"
                
                foraging_props = []
                foraging_props.append(f'"{amount}"')
                foraging_props.append(f'{foraging.get("skill", 0)}')
                foraging_props.append(f'{foraging.get("snowChance", 0)}')
                foraging_props.append(f'{foraging.get("rainChance", 0)}')
                foraging_props.append(f'{foraging.get("dayChance", 0)}')
                foraging_props.append(f'{foraging.get("nightChance", 0)}')
                
                zones = foraging.get("zones", {})
                if zones:
                    zone_items = [f'["{zone}"] = {value}' for zone, value in zones.items()]
                    foraging_props.append(f'{{{", ".join(zone_items)}}}')
                else:
                    foraging_props.append('{}')
                
                months = foraging.get("months", {})
                if months:
                    month_items = [f'["{month}"] = {value}' for month, value in months.items()]
                    foraging_props.append(f'{{{", ".join(month_items)}}}')
                else:
                    foraging_props.append('{}')
                
                bonus_months = foraging.get("bonusMonths", {})
                if bonus_months:
                    bonus_items = [f'["{month}"] = {value}' for month, value in bonus_months.items()]
                    foraging_props.append(f'{{{", ".join(bonus_items)}}}')
                else:
                    foraging_props.append('{}')
                
                malus_months = foraging.get("malusMonths", {})
                if malus_months:
                    malus_items = [f'["{month}"] = {value}' for month, value in malus_months.items()]
                    foraging_props.append(f'{{{", ".join(malus_items)}}}')
                else:
                    foraging_props.append('{}')
                
                sections.append(f"    foraging = {{{', '.join(foraging_props)}}}")
            
            # Fishing data
            if item_data.get("Fishing") and item_data["Fishing"]:
                fishing = item_data["Fishing"]
                fishing_data = []
                
                # Add lures with their chances as objects
                lures = fishing.get("lures", [])
                for lure in lures:
                    lure_name = lure.get("name", "")
                    lure_chance = lure.get("chance", 0)
                    
                    # Convert lure name to wiki link using Item class
                    try:
                        lure_item = Item(lure_name)
                        lure_link = lure_item.wiki_link
                        fishing_data.append((lure_chance, lure_link))
                    except Exception:
                        # Fallback if item doesn't exist
                        fishing_data.append((lure_chance, lure_name))
                
                if fishing_data:
                    # Sort by chance (descending) first, then alphabetically by lure name
                    fishing_data.sort(key=lambda x: (-x[0], x[1]))
                    fishing_lines = [f'{{"{lure_link}", {lure_chance}}}' 
                                   for lure_chance, lure_link in fishing_data]
                    sections.append(f"    fishing = {{{','.join(fishing_lines)}}}")
            
            # Butchering data
            if item_data.get("Butchering"):
                butchering_data = []
                for butchering in item_data["Butchering"]:
                    animal_id = butchering.get("animal", "")
                    amount = butchering.get("amount", "1")
                    
                    # Format animal name using the animal_data mapping
                    if animal_id in animal_data:
                        animal_info = animal_data[animal_id]
                        animal_type = animal_info["type"]
                        animal_name = animal_info["name"]
                        # Create wiki link format: [[Type|Name]]
                        # Escape any quotes in the animal names for Lua safety
                        escaped_type = animal_type.replace('"', '\\"')
                        escaped_name = animal_name.replace('"', '\\"')
                        formatted_animal_name = f"[[{escaped_type}|{escaped_name}]]"
                    else:
                        # Fallback to old format if animal not found in mapping
                        formatted_animal_name = animal_id.replace("_", " ").title()
                    
                    butchering_data.append((formatted_animal_name, amount))
                
                if butchering_data:
                    # Sort alphabetically by animal name (for wiki links, sort by the display name part)
                    butchering_data.sort(key=lambda x: x[0])
                    butchering_lines = [f'{{"{animal_name}", "{amount}"}}' 
                                      for animal_name, amount in butchering_data]
                    sections.append(f"    butchering = {{{','.join(butchering_lines)}}}")
            
            # Attached Weapons data
            if item_data.get("AttachedWeapons"):
                attached_weapons_data = []
                for weapon in item_data["AttachedWeapons"]:
                    outfit = weapon.get("outfit", "Any")
                    definition_id = weapon.get("definition_id", "Unknown")
                    effective_chance = weapon.get("effective_chance", 0)
                    days_required = weapon.get("days_required", 0)
                    
                    # Format definition_id for Lua safety
                    escaped_definition_id = definition_id.replace('"', '\\"')
                    
                    attached_weapons_data.append({
                        "outfit": outfit,  # Outfit links are already created in get_attached_weapon_info
                        "definition_id": escaped_definition_id,
                        "effective_chance": effective_chance,
                        "days_required": days_required
                    })
                
                if attached_weapons_data:
                    # Sort by outfit, then definition_id
                    attached_weapons_data.sort(key=lambda x: (x["outfit"], x["definition_id"]))
                    attached_weapons_lines = [
                        f'{{"{weapon["outfit"]}", "{weapon["definition_id"]}", {weapon["days_required"]}, {weapon["effective_chance"]}}}'
                        for weapon in attached_weapons_data
                    ]
                    sections.append(f"    attachedWeapons = {{{','.join(attached_weapons_lines)}}}")

            if sections:
                # Sort sections alphabetically by their type (container, vehicle, etc.)
                # This ensures consistent ordering of sections
                sections.sort(key=lambda x: x.split()[0])
                f.write(f"  [\"{item_id}\"] = {{\n")
                f.write(',\n'.join(sections))
                f.write("\n  },\n")
    
    # Write each category to separate Lua files
    new_index = {}
    
    # Sort categories alphabetically
    sorted_categories = sorted(category_items.keys())
    
    for category in tqdm.tqdm(sorted_categories, desc="Writing Lua files"):
        items = category_items[category]
        current_items = {}
        current_file_number = 1
        estimated_lines = 0
        
        # Sort items alphabetically by item_id
        for item_id, item_data in sorted(items.items()):
            item_lines = 5
            
            # If adding this item would exceed line limit, write current file and start new one
            if estimated_lines + item_lines > 3250 and current_items:
                # Write current file
                file_suffix = "" if current_file_number == 1 else str(current_file_number)
                category_name = category if current_file_number == 1 else f"{category}{current_file_number}"
                output_file = os.path.join(output_dir, f"{category}{file_suffix}_data.lua")
                
                with open(output_file, "w") as f:
                    write_header(f, category, current_file_number if current_file_number > 1 else None)
                    write_items_to_file(f, current_items)
                    f.write("}\n\nreturn data")
                
                # Store items in index
                new_index[category_name] = list(current_items.keys())
                
                # Reset for next file
                current_items = {}
                estimated_lines = 0
                current_file_number += 1
            
            # Add item to current batch
            current_items[item_id] = item_data
            estimated_lines += item_lines
        
        # Write remaining items
        if current_items:
            file_suffix = "" if current_file_number == 1 else str(current_file_number)
            category_name = category if current_file_number == 1 else f"{category}{current_file_number}"
            output_file = os.path.join(output_dir, f"{category}{file_suffix}_data.lua")
            
            with open(output_file, "w") as f:
                write_header(f, category, current_file_number if current_file_number > 1 else None)
                write_items_to_file(f, current_items)
                f.write("}\n\nreturn data")
            
            # Store items in index
            new_index[category_name] = list(current_items.keys())
    
    # Create index file
    index_file = os.path.join(output_dir, "index.lua")
    with open(index_file, "w") as f:
        f.write("--[[\n")
        f.write("Index of all distribution data files\n")
        f.write("\nStructure:\n")
        f.write("index[category] = {item_id1, item_id2, ...}\n")
        f.write("For categories with multiple files, the category name will have a number suffix\n")
        f.write("--]]\n\n")
        
        f.write("local index = {\n")
        
        # Sort categories alphabetically
        sorted_categories = sorted(new_index.keys())
        for category_name in sorted_categories:
            items = new_index[category_name]
            # Sort items within each category
            sorted_items = sorted(items)
            items_str = ", ".join([f'"{item_id}"' for item_id in sorted_items])
            f.write(f"  [\"{category_name}\"] = {{ {items_str} }},\n")
        
        f.write("}\n\nreturn index")


def calculate_missing_items(itemname_path, itemlist_path, missing_items_path):
    """
    Calculate items that exist in itemname_en.txt but not in the processed item list.
    """
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


def combine_items_by_page(all_items):
    """
    Combines distribution data for items that share the same wiki page.
    
    This function:
    1. Uses page_manager to get the official page-to-item mappings
    2. For each page, combines all secondary item data into the primary item's data
    3. Removes duplicate entries in container, vehicle, and other lists
    4. Returns a new dictionary with combined items
    
    Args:
        all_items (dict): Dictionary of all items with their distribution data
        
    Returns:
        dict: Updated dictionary with combined items
    """
    from scripts.objects.item import Item
    from scripts.core import page_manager
    
    # Initialize page_manager
    page_manager.init()
    
    # Get the flattened page dictionary (this removes the top-level "item" key)
    flattened_page_dict = page_manager.get_flattened_page_dict()
    
    # Dictionary to store combined items
    combined_items = {}
    # Dictionary to track which items have been processed
    processed_items = set()
    # Dictionary to map secondary items to their primary item
    item_mapping = {}
    
    print("Combining items by page...")
    
    # Build a mapping of item IDs to their pages and primary IDs
    item_to_page_info = {}
    
    # Special case: Items that should not be combined
    # Why Is It When Something Happens, It's Always You Three
    do_not_combine = {"VHS_Retail", "VHS_Home", "Disc_Retail"}
    
    for page_name, page_data in flattened_page_dict.items():
        item_ids = page_data.get("item_id", [])
        if not item_ids or len(item_ids) == 1:
            continue  # Skip pages with only one item or no items
            
        # The first item ID in the list is considered the primary ID
        primary_id_full = item_ids[0]  # e.g., "Base.Hat_Bandana"
        
        # Remove "Base." prefix to match the distribution data format
        primary_id = primary_id_full.replace("Base.", "") if primary_id_full.startswith("Base.") else primary_id_full
        
        # Map all item IDs (including primary) to this page
        for item_id_full in item_ids:
            # Remove "Base." prefix to match distribution data format
            item_id = item_id_full.replace("Base.", "") if item_id_full.startswith("Base.") else item_id_full
            
            # Skip mapping if this is a do-not-combine item
            if item_id in do_not_combine:
                continue
            
            item_to_page_info[item_id] = {
                "page": page_name,
                "primary_id": primary_id,
                "is_primary": item_id == primary_id
            }
    
    print(f"Found {len(item_to_page_info)} items with page mappings")
    
    # First pass: Process all items that have page mappings
    for item_id, item_data in all_items.items():
        # Skip already processed items
        if item_id in processed_items:
            continue
            
        # Skip if this is a do-not-combine item
        if item_id in do_not_combine:
            combined_items[item_id] = item_data
            processed_items.add(item_id)
            continue
            
        # Check if this item has a page mapping
        page_info = item_to_page_info.get(item_id)
        if not page_info:
            # No page mapping, keep as is
            combined_items[item_id] = item_data
            processed_items.add(item_id)
            continue
            
        primary_id = page_info["primary_id"]
        is_primary = page_info["is_primary"]
        
        # If this is the primary item, initialize its entry
        if is_primary:
            combined_items[primary_id] = item_data.copy()
            processed_items.add(primary_id)
        else:
            # This is a secondary item, map it to the primary
            item_mapping[item_id] = primary_id
            processed_items.add(item_id)
            
            # If the primary item hasn't been processed yet, initialize it
            if primary_id not in combined_items:
                # Check if the primary item exists in all_items
                if primary_id in all_items:
                    combined_items[primary_id] = all_items[primary_id].copy()
                else:
                    # Create an empty structure for the primary item
                    combined_items[primary_id] = {
                        "name": primary_id,
                        "Containers": [],
                        "Vehicles": [],
                        "Foraging": {},
                        "Clothing": [],
                        "Stories": [],
                        "Fishing": {},
                        "Butchering": [],
                        "AttachedWeapons": [] # Ensure AttachedWeapons is initialized
                    }
            
            # Combine data from secondary item into primary item
            secondary_data = item_data
            
            # Combine container data
            if secondary_data.get("Containers"):
                if not combined_items[primary_id].get("Containers"):
                    combined_items[primary_id]["Containers"] = []
                combined_items[primary_id]["Containers"].extend(secondary_data["Containers"])
            
            # Combine vehicle data
            if secondary_data.get("Vehicles"):
                if not combined_items[primary_id].get("Vehicles"):
                    combined_items[primary_id]["Vehicles"] = []
                combined_items[primary_id]["Vehicles"].extend(secondary_data["Vehicles"])
            
            # Combine foraging data (take the one with more information if both exist)
            if secondary_data.get("Foraging") and secondary_data["Foraging"]:
                if not combined_items[primary_id].get("Foraging") or not combined_items[primary_id]["Foraging"]:
                    combined_items[primary_id]["Foraging"] = secondary_data["Foraging"]
                elif len(secondary_data["Foraging"]) > len(combined_items[primary_id]["Foraging"]):
                    combined_items[primary_id]["Foraging"] = secondary_data["Foraging"]
            
            # Combine clothing data
            if secondary_data.get("Clothing"):
                if not combined_items[primary_id].get("Clothing"):
                    combined_items[primary_id]["Clothing"] = []
                combined_items[primary_id]["Clothing"].extend(secondary_data["Clothing"])
            
            # Combine stories data
            if secondary_data.get("Stories"):
                if not combined_items[primary_id].get("Stories"):
                    combined_items[primary_id]["Stories"] = []
                combined_items[primary_id]["Stories"].extend(secondary_data["Stories"])
                
            # Combine fishing data
            if secondary_data.get("Fishing") and secondary_data["Fishing"]:
                if not combined_items[primary_id].get("Fishing"):
                    combined_items[primary_id]["Fishing"] = {}
                
                # If primary item doesn't have fishing data or secondary has more lures, use secondary's data
                if (not combined_items[primary_id]["Fishing"] or 
                    (secondary_data["Fishing"].get("lures") and 
                     len(secondary_data["Fishing"].get("lures", [])) > 
                     len(combined_items[primary_id]["Fishing"].get("lures", [])))):
                    combined_items[primary_id]["Fishing"] = secondary_data["Fishing"]
                
                # Ensure isRiver and isLake are set if either item has them as true
                if secondary_data["Fishing"].get("isRiver", False):
                    combined_items[primary_id]["Fishing"]["isRiver"] = True
                if secondary_data["Fishing"].get("isLake", False):
                    combined_items[primary_id]["Fishing"]["isLake"] = True
                
            # Combine butchering data
            if secondary_data.get("Butchering"):
                if not combined_items[primary_id].get("Butchering"):
                    combined_items[primary_id]["Butchering"] = []
                combined_items[primary_id]["Butchering"].extend(secondary_data["Butchering"])
            
            # Combine Attached Weapons data
            if secondary_data.get("AttachedWeapons"):
                if not combined_items[primary_id].get("AttachedWeapons"):
                    combined_items[primary_id]["AttachedWeapons"] = []
                combined_items[primary_id]["AttachedWeapons"].extend(secondary_data["AttachedWeapons"])
    
    # Second pass: Process any remaining items (those without page mappings)
    for item_id, item_data in all_items.items():
        if item_id not in processed_items:
            combined_items[item_id] = item_data
            processed_items.add(item_id)
    
    # Third pass: Remove duplicates in each list
    print("Removing duplicates...")
    for item_id, item_data in combined_items.items():
        # Remove duplicate container entries
        if item_data.get("Containers"):
            unique_containers = []
            container_set = set()
            for container in item_data["Containers"]:
                container_key = (
                    container.get("Room", ""), 
                    container.get("Container", ""), 
                    container.get("Chance", 0),
                    container.get("Rolls", 0)
                )
                if container_key not in container_set:
                    container_set.add(container_key)
                    unique_containers.append(container)
            item_data["Containers"] = unique_containers
        
        # Remove duplicate vehicle entries
        if item_data.get("Vehicles"):
            unique_vehicles = []
            vehicle_set = set()
            for vehicle in item_data["Vehicles"]:
                vehicle_key = (
                    vehicle.get("Type", ""), 
                    vehicle.get("Container", ""), 
                    vehicle.get("Chance", 0),
                    vehicle.get("Rolls", 0)
                )
                if vehicle_key not in vehicle_set:
                    vehicle_set.add(vehicle_key)
                    unique_vehicles.append(vehicle)
            item_data["Vehicles"] = unique_vehicles
        
        # Remove duplicate clothing entries
        if item_data.get("Clothing"):
            unique_clothing = []
            clothing_set = set()
            for clothing in item_data["Clothing"]:
                clothing_key = (
                    clothing.get("outfit_name", ""), 
                    clothing.get("Chance", 0),
                    clothing.get("GUID", "")
                )
                if clothing_key not in clothing_set:
                    clothing_set.add(clothing_key)
                    unique_clothing.append(clothing)
            item_data["Clothing"] = unique_clothing
        
        # Remove duplicate stories entries
        if item_data.get("Stories"):
            unique_stories = []
            story_set = set()
            for story in item_data["Stories"]:
                story_key = (
                    story.get("id", ""), 
                    story.get("link", "")
                )
                if story_key not in story_set:
                    story_set.add(story_key)
                    unique_stories.append(story)
            item_data["Stories"] = unique_stories
            
                    # Remove duplicate fishing lure entries
            if item_data.get("Fishing") and item_data["Fishing"].get("lures"):
                unique_lures = []
                lure_set = set()
                for lure in item_data["Fishing"]["lures"]:
                    lure_key = (
                        lure.get("name", ""),
                        lure.get("chance", 0)
                    )
                    if lure_key not in lure_set:
                        lure_set.add(lure_key)
                        unique_lures.append(lure)
                item_data["Fishing"]["lures"] = unique_lures
                
            # Remove duplicate butchering entries
            if item_data.get("Butchering"):
                unique_butchering = []
                butchering_set = set()
                for butchering in item_data["Butchering"]:
                    butchering_key = (
                        butchering.get("animal", ""),
                        butchering.get("amount", ""),
                        butchering.get("type", "")
                    )
                    if butchering_key not in butchering_set:
                        butchering_set.add(butchering_key)
                        unique_butchering.append(butchering)
                item_data["Butchering"] = unique_butchering

            # Remove duplicate Attached Weapons entries
            if item_data.get("AttachedWeapons"):
                unique_attached_weapons = []
                attached_weapons_set = set()
                for weapon in item_data["AttachedWeapons"]:
                    attached_weapons_key = (
                        weapon.get("outfit", ""),
                        weapon.get("definition_id", ""),
                        weapon.get("effective_chance", 0),
                        weapon.get("days_required", 0)
                    )
                    if attached_weapons_key not in attached_weapons_set:
                        attached_weapons_set.add(attached_weapons_key)
                        unique_attached_weapons.append(weapon)
                item_data["AttachedWeapons"] = unique_attached_weapons
    
    # Print statistics
    original_count = len(all_items)
    combined_count = len(combined_items)
    combined_pages_count = len([item for item in item_mapping.values()])
    
    print(f"Original item count: {original_count}")
    print(f"Combined item count: {combined_count}")
    print(f"Reduced by: {original_count - combined_count} items")
    print(f"Number of secondary items combined: {len(item_mapping)}")
    
    # Save the mapping for reference
    save_cache(item_mapping, "item_page_mapping.json", cache_path)
    
    return combined_items


def translate_outfit_name(outfit_label):
    """Convert an outfit ID to a readable name, following outfit_parser.py's rules."""
    # Add spaces before capital letters, but skip if preceded by "KY"
    name_with_spaces = re.sub(r'(?<!^)(?<!KY)(?=[A-Z])', ' ', outfit_label)
    name_with_spaces = name_with_spaces.replace('_', ' ')
    # Ensure only one space between words
    return re.sub(r'\s+', ' ', name_with_spaces).strip()

def get_outfit_link(outfit_id, outfits_data=None):
    """
    Convert an outfit ID to a wiki link. Uses male version by default unless only female exists.
    Returns link in format [[Name (gender)|Name]] with sentence case display.
    
    Args:
        outfit_id: The outfit identifier (e.g., "ArmyInstructor")
        outfits_data: Optional dictionary containing outfit data from outfit_parser
        
    Returns:
        A wiki link to the outfit page (e.g., "[[Army Instructor (male)|Army instructor]]")
    """
    if outfits_data is None:
        from scripts.parser.outfit_parser import get_outfits
        outfits_data = get_outfits()
    
    translated_name = translate_outfit_name(outfit_id)
    
    # Convert to sentence case for display (first letter capital, rest lowercase)
    display_name = translated_name[0].upper() + translated_name[1:].lower()
    
    # Check if outfit exists in male/female versions
    in_male = outfit_id in outfits_data.get("MaleOutfits", {})
    in_female = outfit_id in outfits_data.get("FemaleOutfits", {})
    
    # Default to male unless only female exists
    if in_male or not in_female:
        return f"[[{translated_name} (male)|{display_name}]]"
    else:
        return f"[[{translated_name} (female)|{display_name}]]"


def main():
    """
    Main function to process and generate distribution data files.
    
    This function:
    1. Parses distribution data from various sources
    2. Processes items and builds JSON data
    3. Combines items that share the same wiki page
    4. Categorizes items by type
    5. Generates Lua data files by category
    6. Creates an index file
    """

    file_paths = {
        "proceduraldistributions": os.path.join(DATA_DIR, "distributions", "proceduraldistributions.json"),
        "foraging": os.path.join(DATA_DIR, "distributions", "foraging.json"),
        "vehicle_distributions": os.path.join(DATA_DIR, "distributions", "vehicle_distributions.json"),
        "clothing": os.path.join(DATA_DIR, "distributions", "clothing.json"),
        "stories": os.path.join(DATA_DIR, "distributions", "stories.json"),
        "distributions": os.path.join(DATA_DIR, "distributions", "distributions.json"),
        "fishing": os.path.join(DATA_DIR, "parsed_fish_data.json")
    }

    # Load fishing data
    Fish.load()
    fishing_data = load_cache(file_paths["fishing"])

    # Parse butchering data
    lua_runtime = lua_helper.load_lua_file("AnimalPartsDefinitions.lua")
    butchering_data = lua_helper.parse_lua_tables(lua_runtime)
    save_cache(butchering_data, "butchering_data.json", cache_path)

    # Parse attached weapons
    lua_runtime = lua_helper.load_lua_file("AttachedWeaponDefinitions.lua")
    parsed_data = lua_helper.parse_lua_tables(lua_runtime)
    save_cache(parsed_data, "attached_weapon_definitions.json", cache_path)

    # Parse distribution data
    print("Parsing distribution data...")
    distribution_parser.main()
    
    # Process item list and build JSON data
    print("Processing item list...")
    file_paths["butchering"] = os.path.join(DATA_DIR, "distributions", "butchering_data.json")
    item_list = process_json(file_paths)

    print("Building item JSON data...")
    procedural_data = load_cache(file_paths["proceduraldistributions"])
    distribution_data = load_cache(file_paths["distributions"])
    vehicle_data = load_cache(file_paths["vehicle_distributions"])
    foraging_data = load_cache(file_paths["foraging"])
    clothing_data = load_cache(file_paths["clothing"])
    stories_data = load_cache(file_paths["stories"])
    butchering_data_loaded = load_cache(file_paths["butchering"])
    attached_weapons_data = load_cache(os.path.join(DATA_DIR, "distributions", "attached_weapon_definitions.json"))

    build_item_json(item_list, procedural_data, distribution_data, vehicle_data, foraging_data, 
                   clothing_data, stories_data, fishing_data, butchering_data_loaded, attached_weapons_data)

    # Load all_items and combine items by page
    print("Loading and combining items by page...")
    all_items = load_cache(os.path.join(DATA_DIR, "distributions", "all_items.json"))
    combined_items = combine_items_by_page(all_items)
    save_cache(combined_items, "combined_items.json", cache_path)

    # Initialize language before categorization
    print("Initializing language...")
    from scripts.core.language import Language
    Language.set("en")  # Set to english to avoid user input
    from scripts.core.language import Translate
    Translate.load()

    # Categorize items
    print("Categorizing items...")
    category_items = {}
    index = {}
    processed_items = set()  # Track which items have been assigned to a category
    
    for item_id, item_data in tqdm.tqdm(combined_items.items(), desc="Categorizing items"):
        # Skip if this item has already been processed
        if item_id in processed_items:
            continue

        # Check if item has any distribution data
        has_data = (
                (item_data.get("Containers") and len(item_data["Containers"]) > 0) or
                (item_data.get("Vehicles") and len(item_data["Vehicles"]) > 0) or
                (item_data.get("Stories") and len(item_data["Stories"]) > 0) or
                (item_data.get("Clothing") and len(item_data["Clothing"]) > 0) or
                (item_data.get("Foraging") and item_data["Foraging"]) or
                (item_data.get("Fishing") and item_data["Fishing"]) or
                (item_data.get("Butchering") and len(item_data["Butchering"]) > 0) or
                (item_data.get("AttachedWeapons") and len(item_data["AttachedWeapons"]) > 0)
        )

        # Only process items that have distribution data
        if not has_data:
            continue

        try:
            # Check if the item exists before trying to create an Item object
            full_item_id = f"Base.{item_id}"
            if not Item.exists(full_item_id):
                # Item doesn't exist in parsed data, put in "misc" category
                if "misc" not in category_items:
                    category_items["misc"] = {}
                    index["misc"] = []

                category_items["misc"][item_id] = item_data
                index["misc"].append(item_id)
                processed_items.add(item_id)
                continue

            # Try to get the item object to find its categories
            item_obj = Item(full_item_id)
            categories = find_all_categories(item_obj)

            # If no categories found, use "misc" as default
            if not categories:
                categories = ["misc"]

            # Add item to the first matching category only
            for category in categories:
                if category not in category_items:
                    category_items[category] = {}
                    index[category] = []

                category_items[category][item_id] = item_data
                index[category].append(item_id)
                processed_items.add(item_id)
                break  # Stop after first category match

        except Exception as e:
            # If there's an error (item not found, etc.), put in "misc" category
            if "misc" not in category_items:
                category_items["misc"] = {}
                index["misc"] = []

            category_items["misc"][item_id] = item_data
            index["misc"].append(item_id)
            processed_items.add(item_id)
            print(f"Error processing {item_id}: {e}")

    # Generate Lua data files by category
    print("Generating Lua data files...")
    build_tables(category_items, index)

    # Calculate missing items
    print("Calculating missing items...")
    itemname_path = os.path.join("resources", "Translate", "EN", "ItemName_EN.txt")
    itemlist_path = os.path.join("output", "distributions", "Item_list.txt")
    missing_items_path = os.path.join("output", "distributions", "missing_items.txt")

    calculate_missing_items(itemname_path, itemlist_path, missing_items_path)
    print("Script completed successfully.")


if __name__ == "__main__":
    main()

