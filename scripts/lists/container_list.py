# List for item containers (bags, etc.)

import random
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core.version import Version
from scripts.core.language import Language, Translate
from scripts.lists import hotbar_slots
from scripts.core.constants import RESOURCE_DIR, PBAR_FORMAT
from scripts.utils import utility, util, table_helper
from scripts.core.cache import save_cache, load_cache
from scripts.utils import echo

TABLE_PATH = f"{RESOURCE_DIR}/tables/container_table.json"

table_map = None
table_type_map = None
hotbar_data = None
category_cache = None


def calculate_weight(item_data, trait=None):
    TRAITS = {
        "organized": 1.3,
        "disorganized": 0.7
    }

    trait_mod = TRAITS.get(trait, 1.0)
    weight = float(item_data.get('Weight', 1.0))
    capacity = float(item_data.get('Capacity', 1.0))
    weight_reduction = int(item_data.get('WeightReduction', 0))

    if weight_reduction == 0:
        weight_full = (weight * 0.3) + (capacity * trait_mod)
    else:
        weight_full = (weight * 0.3) + (capacity * trait_mod) * (weight_reduction / 100)

    return round(weight_full, 2)


# Taken from 'AcceptItemFunction.lua'
def get_accept_item(item_data: dict):
    """Returns a formatted string of accepted items based on the 'AcceptItemFunction' key in the item data.

    Args:
        item_data (dict): Item data containing the 'AcceptItemFunction' key.

    Returns:
        str: A formatted string with item links, images, or text. Returns "-" if no accepted items are found.
    """
    # From AcceptItemFunction.lua (42.7.0)
    ITEM_MAP = {
        "AmmoStrap_Bullets": {
            "Ammo": {"page": "Ammo (tag)", "text": "Ammo", "image": "{{Tag Ammo}}"}, # tag
            "ShotgunShell": {"page": "ShotgunShell (tag)", "text": "ShotgunShell", "image": "{{Tag ShotgunShell}}"} # tag
        },
        "AmmoStrap_Shells": {
            "ShotgunShell": {"page": "ShotgunShell (tag)", "text": "ShotgunShell", "image": "{{Tag ShotgunShell}}"} # tag
        },
        "KeyRing": {
            "Key": {"page": "Security", "text": "Keys", "image": "category-Key"}, # category
            "FitsKeyRing": {"page": "FitsKeyRing (tag)", "image": "{{Tag FitsKeyRing}}"}, # tag
        },
        "HolsterShoulder": {
            "PistolMagazine": {"page": "PistolMagazine (tag)", "image": "{{Tag PistolMagazine}}"}, # tag
            "MaxItems": {"text": "2 items max."} # text (custom)
        },
        "Wallet": {
            "Map": {"page": "Map (item)", "text": "Maps", "image": "category-Map"}, # category
            "Literature": {"page": "Literature", "text": "Literature", "image": "category-Literature"}, # category
            "FitsWallet": {"page": "FitsWallet (tag)", "image": "{{Tag FitsWallet}}"}, # tag
        }
    }

    accept_item = item_data.get('AcceptItemFunction')
    if not accept_item:
        return "-"
    accept_item = accept_item.replace("AcceptItemFunction.", "")
    language_code = Language.get()

    accepted_items = []

    for accept_item_key, accept_item_entries in ITEM_MAP.items():
        if accept_item == accept_item_key:
            for key, values in accept_item_entries.items():
                page = values.get("page")
                text = values.get("text", key)
                image = values.get("image")
                if image:
                    link = ""
                    if page:
                        link = f"|link={page}{Language.get_subpage}"

                    # Build image
                    if image.lower().startswith("file:"):
                        string = f"[[{image}|32x32px{link}|{text}]]"

                    # Build cycling image category/type
                    elif image.lower().startswith("category-"):
                        category = image.replace("category-", "")
                        category_items_list = []

                        for cat_type, cat_items in get_cached_types().items():
                            if cat_type == category:
                                for cat_item_id, cat_item_data in cat_items.items():
                                    cat_item_name = cat_item_data.get("name")
                                    cat_item_icon = cat_item_data.get("icon")

                            

                                    cat_item_image = f"[[File:{cat_item_icon}|32x32px{link}|{cat_item_name}]]"
                                    if cat_item_image not in category_items_list:
                                        category_items_list.append(cat_item_image)

                        
                        
                        # Build the string joining the list
                        if len(category_items_list) > 1:
                            # Get 10 random items from the list to limit the number of items we cycle through
                            if len(category_items_list) > 10:
                                category_items_list = random.sample(category_items_list, 10)
                            
                            category_items_str = "".join(category_items_list)
                            string = f'<span class="cycle-img">{category_items_str}</span>'

                        # Convert list to string if it's a single value, bypassing adding cycle-img
                        else:
                            string = category_items_list[0]

                    # Use the image value as it's probably already an image
                    else:
                        string = image
                    
                elif page:
                    if language_code != "en":
                        string = f"[[{page}/{language_code}|{text}]]"
                    elif page == text:
                        string = f"[[{page}]]"
                    else:
                        string = f"[[{page}|{text}]]"
                else:
                    string = text

                accepted_items.append(str(string))

            if accept_item_key not in ["HolsterShoulder"]:
                return_string = "".join(accepted_items)
            else:
                return_string = "<br>".join(accepted_items)

    return return_string


def get_cached_types():
    """Returns cached item 'Type', storing them in cache for faster operations"""
    global category_cache
    cache_version = Version.get()
    CACHE_FILE = "item_type_data.json"

    # Load cache if data dict is empty
    if not category_cache:
        category_cache, cache_version = load_cache(CACHE_FILE, get_version=True, suppress=True)

    # Generate data if data dict is empty or cache is old
    if not category_cache or cache_version != Version.get():
        parsed_item_data = item_parser.get_item_data()
        with tqdm(total=len(parsed_item_data), desc="Preparing items based on 'Type'", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
            for cat_item_id, cat_item_data in parsed_item_data.items():
                cat_type = cat_item_data.get("Type", "Normal")
                pbar.set_postfix_str(f"Processing: {cat_type[:20]} ({cat_item_id[:20]})")
                name = utility.get_name(cat_item_id, cat_item_data)
                icon = utility.get_icon(cat_item_id)
                page = utility.get_page(cat_item_id, name)
                if cat_type not in category_cache:
                    category_cache[cat_type] = {}

                category_cache[cat_type][cat_item_id] = {"name": name, "icon": icon, "page": page}
                pbar.update(1)
        echo.info("Items organised by type and cached.")

        save_cache(category_cache, CACHE_FILE)
    
    return category_cache


# Get the list type, for mapping the section/table
def find_table_type(item_data):
    body_location = item_data.get("CanBeEquipped")
    if body_location:
        if body_location == "Back":
            return "Back"
        return "Torso"
    
    if item_data.get('AcceptItemFunction'):
        heading = item_data.get('AcceptItemFunction').replace("AcceptItemFunction.", "")
        # Try to get a name for the heading
        heading_item = "Base." + heading
        heading_translated = Translate.get(heading_item, "DisplayName")
        if heading_translated != heading_item:
            heading = heading_translated
        return heading.capitalize()

    return "Containers"


# Process items, returning the heading and row data.
def process_item(item_id, item_data, pbar):
    language_code = Language.get()

    heading = find_table_type(item_data)
    if heading not in table_type_map:
        pbar.write(f"Warning: '{heading}' could not be found in table map.")
        heading = "Containers"
    columns = table_map.get(table_type_map[heading], table_map["generic"])

    item_name = utility.get_name(item_id, item_data) # set item name
    page_name = utility.get_page(item_id, item_name) # set page name

    item = {}

    if "icon" in columns:
        icon = utility.get_icon(item_id, True, True, True)
        item["icon"] = icon

    if "name" in columns:
        item_link = f"[[{page_name}]]"
        if language_code != "en":
            item_link = f"[[{page_name}/{language_code}|{item_name}]]"
        item["name"] = item_link

    if "weight" in columns:
        item["weight"] = item_data.get('Weight', '1')
    
    if "capacity" in columns:
        item["capacity"] = item_data.get('Capacity', '-')

    if "weight_reduction" in columns:
        item["weight_reduction"] = util.convert_percentage(item_data.get('WeightReduction', '-'), True, True)

    if "weight_full" in columns:
        weight_full = util.convert_int(calculate_weight(item_data))
        item["weight_full"] = str(weight_full)

    if "weight_full_organized" in columns:
        weight_full_organized = util.convert_int(calculate_weight(item_data, "organized"))
        item["weight_full_organized"] = str(weight_full_organized)

    if "weight_full_disorganized" in columns:
        weight_full_disorganized = util.convert_int(calculate_weight(item_data, "disorganized"))
        item["weight_full_disorganized"] = str(weight_full_disorganized)

    if "move_speed" in columns:
        item["move_speed"] = util.convert_percentage(item_data.get("RunSpeedModifier", '-'), False)

    if "extra_slots" in columns:
        slots_list = []
        extra_slots = item_data.get("AttachmentsProvided", ['-'])
        if isinstance(extra_slots, str):
            extra_slots = [extra_slots]
        for slot in extra_slots:
            if slot != "-":
                slot_name = hotbar_data.get(slot, {}).get("name")
                slot_page = f"AttachmentsProvided#{slot}"
                slot = util.link(slot_page, slot_name)
            slots_list.append(slot)
        item["extra_slots"] = "<br>".join(slots_list)

    if "body_location" in columns:
        body_location = item_data.get("CanBeEquipped")
        if body_location:
            if language_code == 'en':
                item["body_location"] = f"[[BodyLocation#{body_location}|{body_location}]]"
            else:
                item["body_location"] = f"[[BodyLocation/{language_code}#{body_location}|{body_location}]]"
        else:
            item["body_location"] = "-"

    if "accept_item" in columns:
        item["accept_item"] = get_accept_item(item_data)

    if "max_item_size" in columns:
        item["max_item_size"] = util.convert_int(item_data.get('MaxItemSize', '-'))

    if "item_id" in columns:
        item["item_id"] = f"{{{{ID|{item_id}}}}}"
    
    # Remove any values that are None
    item = {k: v for k, v in item.items() if v is not None}

    # Ensure column order is correct
    item = {key: item[key] for key in columns if key in item}

    # Add item_name for sorting
    item["item_name"] = item_name

    return heading, item


# Get necessary literature items and process them
def find_items():
    container_dict = {}
    parsed_item_data = item_parser.get_item_data()
    item_count = 0

    get_cached_types()

    # Get items
    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item_data.get("Type") == "Container":
                heading, item = process_item(item_id, item_data, pbar)

                # Add heading to dict if it hasn't been added yet.
                if heading not in container_dict:
                    container_dict[heading] = []

                container_dict[heading].append(item)

                item_count += 1

            pbar.update(1)

    echo.info(f"Finished processing {item_count} items for {len(container_dict)} tables.")
           
    return container_dict


def main():
    global hotbar_data
    global table_map
    global table_type_map
    table_map, column_headings, table_type_map = table_helper.get_table_data(TABLE_PATH, "type_map")
    hotbar_data = hotbar_slots.get_hotbar_slots(suppress=True)
    items = find_items()

    mapped_table = {
        item_type: table_map[table_type]
        for item_type, table_type in table_type_map.items()
    }
    
    table_helper.create_tables("container", items, columns=column_headings, table_map=mapped_table)
                

if __name__ == "__main__":
    main()