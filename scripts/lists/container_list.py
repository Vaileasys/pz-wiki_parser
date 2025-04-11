# List for item containers (bags, etc.)

import os
import random
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core.version import Version
from scripts.core.language import Language, Translate
from scripts.lists import hotbar_slots
from scripts.core.constants import PBAR_FORMAT
from scripts.utils import utility, util

hotbar_data = {}

# Used for getting table values
TABLE_DICT = {
    "generic": ['icon', 'name', 'weight', 'item_id'],
    "container": ['icon', 'name', 'weight', 'capacity', 'weight_reduction', 'weight_full', 'weight_full_organized', 'weight_full_disorganized', 'move_speed', 'accept_item', 'max_item_size', 'item_id'],
    "accept_item": ['icon', 'name', 'weight', 'capacity', 'weight_reduction', 'weight_full', 'weight_full_organized', 'weight_full_disorganized', 'accept_item', 'max_item_size', 'item_id'],
    "wearable": ['icon', 'name', 'weight', 'capacity', 'weight_reduction', 'weight_full', 'weight_full_organized', 'weight_full_disorganized', 'move_speed', 'extra_slots', 'body_location', 'accept_item', 'max_item_size', 'item_id'],
}

# Map table values with their headings
COLUMNS_DICT = {
    "icon": "! Icon",
    "name": "! Name",
    "weight": "! [[File:Status_HeavyLoad_32.png|32px|link=Heavy load|Encumbrance]]",
    "capacity": "! [[File:UI_Weight_Max.png|32px|link=|Capacity]]",
    "weight_reduction": "! [[File:UI_Weight_Decrease.png|32px|link=|Encumbrance reduced]]",
    "weight_full": "! [[File:Status_HeavyLoad_32.png|32px|link=Heavy load|Full encumbrance]] {{Tooltip|(full)|Full encumbrance}}",
    "weight_full_organized": "! [[File:Trait_organized.png|18px|link=Organized|Full encumbrance with organized]] {{Tooltip|(full)|Full encumbrance with organized}}",
    "weight_full_disorganized": "! [[File:Trait_disorganized.png|18px|link=Disorganized|Full encumbrance with disorganized]] {{Tooltip|(full)|Full encumbrance with disorganized}}",
    "move_speed": "! [[File:UI_Speed.png|link=|Movement speed]]",
    "extra_slots": "! Hotbar slots",
    "body_location": "! [[File:UI_BodyPart.png|32px|link=|Body location]]",
    "accept_item": "! Valid items",
    "max_item_size": "! [[File:UI_Weight_Max.png|32px|link=Heavy load|Maximum content encumbrance]] {{Tooltip|(item)|Maximum content encumbrance}}",
    "item_id": "! Item ID",
}

# Map the headings to their table_key (TABLE_DICT key)
TABLE_MAPPING = {
    "Back": "wearable",
    "Torso": "wearable",
    "Key ring": "accept_item",
    "Wallet": "accept_item",
    "Containers": "container",
    "Other": "generic",
}

# Map sections to the correct position
# TODO: not currently used. Intended to be used as part of a merge_txt_files function.
SECTION_DICT = {
    'Wearable': [
        'Back',
        'Torso'
    ],
    'Containers': None,
    'Key ring': None,
    'Wallet': None,
}

TABLE_HEADER ='{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"'

category_cache = {}


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
    # From AcceptItemFunction.lua (42.2.0)
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
                        link = f"|link={page}"
                        if language_code != "en":
                            link = f"|link={page}/{language_code}"

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
        category_cache, cache_version = utility.load_cache(CACHE_FILE, get_version=True, suppress=True)

    # Generate data if data dict is empty or cache is old
    if not category_cache or cache_version != Version.get():
        parsed_item_data = item_parser.get_item_data()
        with tqdm(total=len(parsed_item_data), desc="Preparing items based on 'Type'", bar_format=PBAR_FORMAT, unit=" items") as pbar:
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
            pbar.bar_format = f"Items organised."

        utility.save_cache(category_cache, CACHE_FILE)
    
    return category_cache


# Get the list type, for mapping the section/table
def get_list_type(item_id, item_data):
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

    heading = get_list_type(item_id, item_data)
    if heading not in TABLE_MAPPING:
        pbar.write(f"Warning: '{heading}' could not be found in table map.")
        heading = "Containers"
    columns = TABLE_DICT.get(TABLE_MAPPING[heading], TABLE_DICT["generic"])

    item_name = utility.get_name(item_id, item_data) # set item name
    page_name = utility.get_page(item_id, item_name) # set page name
    name_ref = page_name # set item ref (used for sorting)

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
        item["weight_reduction"] = utility.convert_to_percentage(item_data.get('WeightReduction', '-'), True, True)

    if "weight_full" in columns:
        weight_full = utility.convert_int(calculate_weight(item_data))
        item["weight_full"] = str(weight_full)

    if "weight_full_organized" in columns:
        weight_full_organized = utility.convert_int(calculate_weight(item_data, "organized"))
        item["weight_full_organized"] = str(weight_full_organized)

    if "weight_full_disorganized" in columns:
        weight_full_disorganized = utility.convert_int(calculate_weight(item_data, "disorganized"))
        item["weight_full_disorganized"] = str(weight_full_disorganized)

    if "move_speed" in columns:
        item["move_speed"] = utility.convert_to_percentage(item_data.get("RunSpeedModifier", '-'), False)

    if "extra_slots" in columns:
        slots_list = []
        extra_slots = item_data.get("AttachmentsProvided", ['-'])
        if isinstance(extra_slots, str):
            extra_slots = [extra_slots]
        for slot in extra_slots:
            if slot != "-":
                slot_name = hotbar_data.get(slot, {}).get("name")
                slot_page = f"AttachmentsProvided#{slot}"
                slot = util.format_link(name=slot_name, page=slot_page)
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
        item["max_item_size"] = utility.convert_int(item_data.get('MaxItemSize', '-'))

    if "item_id" in columns:
        item["item_id"] = f"{{{{ID|{item_id}}}}}"
    
    item["item_ref"] = name_ref

    return heading, item


# Write to txt files. Separate file for each heading.
def write_to_output(container_dict):
    # write to output.txt
    language_code = Language.get()
    output_dir = os.path.join('output', language_code, 'item_list', 'container')

    os.makedirs(output_dir, exist_ok=True)

    for heading, items in container_dict.items():
        columns = TABLE_DICT.get(TABLE_MAPPING[heading], TABLE_DICT["generic"])

        # Build the table heading based on values
        table_headings = []
        for col in columns:
            mapped_headings = COLUMNS_DICT.get(col, col)
            table_headings.append(mapped_headings)
        table_headings = "\n".join(table_headings)

        output_path = os.path.join(output_dir, f"{heading}.txt")
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(f'<!--BOT_FLAG-start-{heading.replace(" ", "_")}. DO NOT REMOVE-->')
            file.write(f"{TABLE_HEADER}\n")
            file.write(f"{table_headings}\n")

            items = sorted(items, key=lambda x: x['item_ref'])
            for item in items:
                # Remove 'item_ref' from the dict, so it doesn't get added to the table.
                item.pop("item_ref", None)
                row = "\n| ".join([value for key, value in item.items()])
                file.write(f"|-\n| {row}\n")

            file.write("|}")
            file.write(f'<!--BOT_FLAG-end-{heading.replace(" ", "_")}. DO NOT REMOVE-->')

    print(f"Output saved to {output_dir}")


# Get necessary literature items and process them
def get_items():
    container_dict = {}
    parsed_item_data = item_parser.get_item_data()

    get_cached_types()

    # Get items
    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item_data.get("Type") == "Container":
                heading, item = process_item(item_id, item_data, pbar)

                # Add heading to dict if it hasn't been added yet.
                if heading not in container_dict:
                    container_dict[heading] = []

                container_dict[heading].append(item)

            pbar.update(1)

        pbar.bar_format = f"Items processed."
           
    return container_dict


# Combines txt files based on their position in SECTION_DICT
def combine_files():
    language_code = Language.get()
    clothing_dir = f'output/{language_code}/item_list/container/'
    output_file = f'output/{language_code}/item_list/container_list.txt'

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    file_dict = {}

    # Get the file name and its contents
    for file in os.listdir(clothing_dir):
        if file.endswith('.txt'):
            file_name = file[:-4]
            file_path = os.path.join(clothing_dir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_dict[file_name] = f.read()

    # Lookup a the file name in SECTION_DICT and write the section and its contents
    with open(output_file, 'w', encoding='utf-8') as output_f:
        output_f.write("{{Legend container}}\n")
        for section, items in SECTION_DICT.items():
            # Nested sections
            if isinstance(items, list):
                output_f.write(f"==={section}===\n")
                for subkey in items:
                    content = file_dict.get(subkey, None)
                    if content is not None:
                        output_f.write(f"===={subkey}====\n")
                        output_f.write(f"{content}\n\n")
                    else:
                        print(f"Skipping '{subkey}': No content found.")
            else:
                content = file_dict.get(section, None)
                if content is not None:
                    output_f.write(f"==={section}===\n")
                    output_f.write(f"{content}\n\n")
                else:
                    print(f"Skipping '{section}': No content found.")

    print(f"Combined files written to {output_file}")


def main():
    global language_code
    global hotbar_data
    language_code = language_code = Language.get()
    hotbar_data = hotbar_slots.get_hotbar_slots(suppress=True)
    items = get_items()
    write_to_output(items)
    combine_files()
                

if __name__ == "__main__":
    main()