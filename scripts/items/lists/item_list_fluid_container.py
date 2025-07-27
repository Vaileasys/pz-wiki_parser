import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.objects.item import Item
from scripts.core.constants import ITEM_DIR, RESOURCE_DIR, PBAR_FORMAT
from scripts.utils.table_helper import get_table_data, create_tables
from scripts.utils import echo
from scripts.utils.util import convert_int, check_zero, tick, cross

TABLE_PATH = os.path.join(RESOURCE_DIR, "tables", "container_table.json")
ROOT_PATH = os.path.join(ITEM_DIR, "lists")

table_map = {}

def process_item(item: Item):
    table_type = "fluid_container"
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")
    heading = table_type

    capacity = f"{item.fluid_container.capacity} L"

    rain_factor = check_zero(convert_int(item.fluid_container.rain_factor), default="-")

    boilable = tick(link="Heat source", text="Can be boiled in an oven or campfire") if item.has_tag("Cookable") else cross(link="Heat source", text="Can't be boiled in an oven or campfire")
    boilable_microwave = tick(link="White Microwave", text="Can be boiled in a microwave") if item.has_tag("CookableMicrowave") else cross(link="White Microwave", text="Can't be boiled in a microwave")
    coffee_maker = tick(link="Espresso Deluxe", text="Can be used in an espresso machine") if item.has_tag("CoffeeMaker") else cross(link="Espresso Deluxe", text="Can't be used in an espresso machine")

    fluids = []
    for fluid in item.fluid_container.fluids:
        fluids.append(fluid.wiki_link + " " + fluid.rgb)
    fluids = "<br>".join(fluids) if fluids else "-"

    item_content = {
        "icon": item.icon,
        "name": item.wiki_link,
        "container_name": item.fluid_container.container_name,
        "weight": convert_int(item.weight),
        "fluid_capacity": convert_int(capacity),
        "weight_full": convert_int(item.weight_full),
        "rain_factor": rain_factor,
        "boilable": boilable,
        "boilable_microwave": boilable_microwave,
        "coffee_maker": coffee_maker,
        "fluids": fluids,
        "item_id": item.item_id
    }

    # Remove any values that are None
    item_content = {k: v for k, v in item_content.items() if v is not None}

    # Convert all values to strings
    item_content = {k: str(v) for k, v in item_content.items()}

    # Ensure column order is correct
    item_content = {key: item_content[key] for key in columns if key in item_content}

    # Add item_name for sorting
    item_content["item_name"] = item.name

    return heading, item_content


def find_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id in Item.keys():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            item = Item(item_id)
            if item.has_category("fluid_container"):
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

    create_tables("fluid_container", items, table_map=table_map, columns=column_headings, root_path=ROOT_PATH, suppress=True, bot_flag_type="fluid_container_item_list", combine_tables=False)


if __name__ == "__main__":
    main()