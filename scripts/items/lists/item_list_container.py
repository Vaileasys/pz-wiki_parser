# List for item containers (bags, etc.)
import os
import random
from tqdm import tqdm
from scripts.core.version import Version
from scripts.core.language import Language
from scripts.objects.item import Item
from scripts.objects.attachment import HotbarSlot
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.utils import table_helper, echo
from scripts.utils.util import convert_int, convert_percentage, link, check_zero
from scripts.core.cache import save_cache, load_cache

TABLE_PATH = os.path.join(TABLES_DIR, "container_table.json")

table_map = None
table_type_map = None
category_cache = None


# Taken from 'AcceptItemFunction.lua'
def find_accept_item(item: Item):
    """Returns a formatted string of accepted items based on the 'AcceptItemFunction' key in the item data.

    Args:
        item_data (dict): Item data containing the 'AcceptItemFunction' key.

    Returns:
        str: A formatted string with item links, images, or text. Returns "-" if no accepted items are found.
    """
    # From AcceptItemFunction.lua (42.7.0)
    ITEM_MAP = {
        "AmmoStrap_Bullets": {
            "Ammo": {
                "page": "Ammo (tag)",
                "text": "Ammo",
                "image": "{{Tag Ammo}}",
            },  # tag
            "ShotgunShell": {
                "page": "ShotgunShell (tag)",
                "text": "ShotgunShell",
                "image": "{{Tag ShotgunShell}}",
            },  # tag
        },
        "AmmoStrap_Shells": {
            "ShotgunShell": {
                "page": "ShotgunShell (tag)",
                "text": "ShotgunShell",
                "image": "{{Tag ShotgunShell}}",
            }  # tag
        },
        "KeyRing": {
            "Key": {
                "page": "Security",
                "text": "Keys",
                "image": "category-Key",
            },  # category
            "FitsKeyRing": {
                "page": "FitsKeyRing (tag)",
                "image": "{{Tag FitsKeyRing}}",
            },  # tag
        },
        "HolsterShoulder": {
            "PistolMagazine": {
                "page": "PistolMagazine (tag)",
                "image": "{{Tag PistolMagazine}}",
            },  # tag
            "MaxItems": {"text": "2 items max."},  # text (custom)
        },
        "Wallet": {
            "Map": {
                "page": "Map (item)",
                "text": "Maps",
                "image": "category-Map",
            },  # category
            "Literature": {
                "page": "Literature",
                "text": "Literature",
                "image": "category-Literature",
            },  # category
            "FitsWallet": {
                "page": "FitsWallet (tag)",
                "image": "{{Tag FitsWallet}}",
            },  # tag
        },
    }

    accept_item = item.accept_item_function
    if not accept_item:
        return "-"
    accept_item = accept_item.replace("AcceptItemFunction.", "")

    accepted_items = []

    for accept_item_key, accept_item_entries in ITEM_MAP.items():
        if accept_item == accept_item_key:
            for key, values in accept_item_entries.items():
                page = values.get("page")
                text = values.get("text", key)
                image = values.get("image")
                if image:
                    link_text = ""
                    if page:
                        link_text = f"|link={page}{Language.get_subpage()}"

                    # Build image
                    if image.lower().startswith("file:"):
                        string = f"[[{image}|32x32px{link_text}|{text}]]"

                    # Build cycling image category/type
                    elif image.lower().startswith("category-"):
                        category = image.replace("category-", "")
                        category_items_list = []

                        for cat_type, cat_items in get_cached_types().items():
                            if cat_type == category:
                                for cat_item_id, cat_item_data in cat_items.items():
                                    cat_item_name = cat_item_data.get("name")
                                    cat_item_icon = cat_item_data.get("icon")

                                    cat_item_image = f"[[File:{cat_item_icon}|32x32px{link_text}|{cat_item_name}]]"
                                    if cat_item_image not in category_items_list:
                                        category_items_list.append(cat_item_image)

                        # Build the string joining the list
                        if len(category_items_list) > 1:
                            # Get 10 random items from the list to limit the number of items we cycle through
                            if len(category_items_list) > 10:
                                category_items_list = random.sample(
                                    category_items_list, 10
                                )

                            category_items_str = "".join(category_items_list)
                            string = (
                                f'<span class="cycle-img">{category_items_str}</span>'
                            )

                        # Convert list to string if it's a single value, bypassing adding cycle-img
                        else:
                            string = category_items_list[0]

                    # Use the image value as it's probably already an image
                    else:
                        string = image

                elif page:
                    string = link(page, text)
                else:
                    string = text

                accepted_items.append(str(string))

            if accept_item_key not in ["HolsterShoulder"]:
                return_string = "".join(accepted_items)
            else:
                return_string = "<br>".join(accepted_items)

    return return_string


def get_cached_types() -> dict:
    """Returns cached item 'Type', storing them in cache for faster operations"""
    global category_cache
    cache_version = Version.get()
    CACHE_FILE = "item_type_data.json"

    # Load cache if data dict is empty
    if not category_cache:
        category_cache, cache_version = load_cache(
            CACHE_FILE, get_version=True, suppress=True
        )

    # Generate data if data dict is empty or cache is old
    if not category_cache or cache_version != Version.get():
        with tqdm(
            total=Item.count(),
            desc="Preparing items based on 'Type'",
            bar_format=PBAR_FORMAT,
            unit=" items",
            leave=False,
        ) as pbar:
            for item_id, item in Item.all().items():
                pbar.set_postfix_str(f"Processing: {item.type[:20]} ({item_id[:20]})")
                name = item.name
                icon = item.get_icon(False, False)
                page = item.page
                if item.type not in category_cache:
                    category_cache[item.type] = {}

                category_cache[item.type][item_id] = {
                    "name": name,
                    "icon": icon,
                    "page": page,
                }
                pbar.update(1)
        echo.info("Items organised by type and cached.")

        save_cache(category_cache, CACHE_FILE)

    return category_cache


# Get the list type, for mapping the section/table
def find_table_type(item: Item):
    if item.can_be_equipped:
        echo.write(
            f"[DEBUG] Item '{item.item_id}' - can_be_equipped: {item.can_be_equipped} (type: {type(item.can_be_equipped).__name__})"
        )
        if hasattr(item.can_be_equipped, "location_id"):
            echo.write(
                f"[DEBUG] Item '{item.item_id}' - location_id: {item.can_be_equipped.location_id}"
            )
            if item.can_be_equipped.location_id == "Back":
                return "Back"
            return "Torso"
        else:
            echo.warning(
                f"[DEBUG] Item '{item.item_id}' - can_be_equipped object has no 'location_id' attribute!"
            )

    if item.accept_item_function:
        heading = item.accept_item_function.replace("AcceptItemFunction.", "")
        # Try to get a name for the heading
        if Item.exists(heading):
            heading = Item(heading).name
        return heading.capitalize()

    return "Containers"


# Process items, returning the heading and row data.
def process_item(item: Item):
    table_type = find_table_type(item)
    if table_type not in table_type_map:
        echo.warning(f"'{table_type}' could not be found in table map.")
        table_type = "Containers"
    columns = table_map.get(table_type_map[table_type], table_map["generic"])

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = convert_int(item.weight) if "weight" in columns else None
    item_dict["capacity"] = (item.capacity or "-") if "capacity" in columns else None
    item_dict["weight_reduction"] = (
        convert_percentage(item.weight_reduction, True, True, default="-")
        if "weight_reduction" in columns
        else None
    )
    item_dict["weight_full"] = (
        convert_int(item.calculate_weight()) if "weight_full" in columns else None
    )
    item_dict["weight_full_organized"] = (
        convert_int(item.calculate_weight("organized"))
        if "weight_full_organized" in columns
        else None
    )
    item_dict["weight_full_disorganized"] = (
        convert_int(item.calculate_weight("disorganized"))
        if "weight_full_disorganized" in columns
        else None
    )
    item_dict["move_speed"] = (
        convert_percentage(item.run_speed_modifier, False, default="-")
        if "move_speed" in columns
        else None
    )

    if "extra_slots" in columns:
        slots = []
        for slot_id in item.attachments_provided:
            slots.append(HotbarSlot(slot_id).wiki_link)
        item_dict["extra_slots"] = "<br>".join(slots) if slots else "-"

    if "body_location" in columns:
        echo.write(f"[DEBUG] Item '{item.item_id}' - Processing body_location column")
        echo.write(
            f"[DEBUG] Item '{item.item_id}' - can_be_equipped value: {item.can_be_equipped} (type: {type(item.can_be_equipped).__name__})"
        )
        if item.can_be_equipped:
            if hasattr(item.can_be_equipped, "wiki_link"):
                item_dict["body_location"] = item.can_be_equipped.wiki_link or "-"
                echo.write(
                    f"[DEBUG] Item '{item.item_id}' - body_location set to: {item_dict['body_location']}"
                )
            else:
                echo.error(
                    f"[DEBUG] Item '{item.item_id}' - can_be_equipped has no 'wiki_link' attribute!"
                )
                item_dict["body_location"] = "-"
        else:
            echo.write(
                f"[DEBUG] Item '{item.item_id}' - can_be_equipped is None, setting to '-'"
            )
            item_dict["body_location"] = "-"
    else:
        item_dict["body_location"] = None

    item_dict["accept_item"] = (
        find_accept_item(item) if "accept_item" in columns else None
    )
    item_dict["max_item_size"] = (
        check_zero(item.max_item_size, default="-")
        if "max_item_size" in columns
        else None
    )
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.page

    return table_type, item_dict


# Get necessary literature items and process them
def find_items():
    container_dict = {}
    item_count = 0

    get_cached_types()

    # Get items
    with tqdm(
        total=Item.count(),
        desc="Processing items",
        bar_format=PBAR_FORMAT,
        unit=" items",
        leave=False,
    ) as pbar:
        for item_id, item in Item.all().items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("container"):
                echo.write(f"\n[DEBUG] Processing container item: {item_id}")
                try:
                    table_type, item_data = process_item(item)
                except Exception as e:
                    echo.error(f"[ERROR] Failed to process item '{item_id}': {e}")
                    import traceback

                    traceback.print_exc()
                    pbar.update(1)
                    continue

                # Add heading to dict if it hasn't been added yet.
                if table_type not in container_dict:
                    container_dict[table_type] = []

                container_dict[table_type].append(item_data)

                item_count += 1

            pbar.update(1)

    echo.info(
        f"Finished processing {item_count} items for {len(container_dict)} tables."
    )

    return container_dict


def main():
    global table_map
    global table_type_map
    Language.get()
    table_map, column_headings, table_type_map = table_helper.get_table_data(
        TABLE_PATH, "type_map"
    )
    items = find_items()

    mapped_table = {
        item_type: table_map[table_type]
        for item_type, table_type in table_type_map.items()
    }

    table_helper.create_tables(
        "container_item_list",
        items,
        columns=column_headings,
        table_map=mapped_table,
        suppress=True,
        bot_flag_type="container_item_list",
        combine_tables=False,
    )


if __name__ == "__main__":
    main()
