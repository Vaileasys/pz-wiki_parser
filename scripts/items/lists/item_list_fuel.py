import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.objects.item import Item
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.utils.table_helper import get_table_data, create_tables
from scripts.utils.util import tick, cross
from scripts.utils import echo

TABLE_PATH = os.path.join(TABLES_DIR, "fuel_table.json")

table_map = {}


def find_table_type(item: Item):
    if item.item_type == "map":
        return "Literature"
    elif item.item_type in ("food", "drainable", "normal", "moveable"):
        return "Miscellaneous"
    return item.item_type


def process_item(item: Item):
    table_type = find_table_type(item)
    columns = (
        table_map.get(table_type)
        if table_map.get(table_type) is not None
        else table_map.get("default")
    )

    tinder = (
        tick(text="Can be used to start a fire", link="Campfire")
        if item.is_tinder
        else cross(text="Can't be used to start a fire", link="Campfire")
    )

    item_content = {
        "icon": item.icon,
        "name": item.wiki_link,
        "weight": item.weight,
        "burn_time": item.burn_time,
        "tinder": tinder,
        "item_id": item.item_id,
    }

    # Remove any values that are None
    item_content = {k: v for k, v in item_content.items() if v is not None}

    # Ensure column order is correct
    item_content = {key: item_content[key] for key in columns if key in item_content}

    # Add item_name for sorting
    item_content["item_name"] = item.name

    return table_type, item_content


def find_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(
        total=Item.count(),
        desc="Processing items",
        bar_format=PBAR_FORMAT,
        unit=" items",
        leave=False,
    ) as pbar:
        for item_id in Item.keys():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            item = Item(item_id)
            if item.burn_time:
                heading, item_content = process_item(item)

                # Add heading to dict if it hasn't been added yet.
                if heading not in items:
                    items[heading] = []

                items[heading].append(item_content)

                item_count += 1

            pbar.update(1)

    echo.info(f"Finished processing {item_count} items for {len(items)} tables.")

    return items


def main():
    Language.get()
    global table_map
    table_map, column_headings = get_table_data(TABLE_PATH)

    items = find_items()

    create_tables(
        "fuel_item_list",
        items,
        table_map=table_map,
        columns=column_headings,
        suppress=True,
        bot_flag_type="fuel_item_list",
        combine_tables=False,
    )


if __name__ == "__main__":
    main()
