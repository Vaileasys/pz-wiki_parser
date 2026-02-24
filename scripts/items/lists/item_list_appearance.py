import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "appearance_table.json")

table_map = {}


def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = (
        table_map.get(table_type)
        if table_map.get(table_type) is not None
        else table_map.get("default")
    )

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    if "type" in columns:
        if item.make_up_type:
            app_type = item.make_up_type
        elif item.has_tag("DoHairdo"):
            app_type = "Hair"
        elif (
            "HairDye" in item.item_id
            or item.has_tag("Scissors")
            or item.has_tag("Razor")
        ):
            app_type = "Hair & Beard"
        else:
            app_type = "-"
        item_dict["type"] = app_type
    if "mirror" in columns:
        if item.item_id in ("Base.Mirror", "Base.MakeupFoundation"):
            mirror = util.tick("Cannot be used as a mirror")
        else:
            mirror = util.cross("Cannot be used as a mirror")
        item_dict["mirror"] = mirror
    if "capacity" in columns:
        if item.fluid_container:
            item_dict["capacity"] = (
                f"{util.convert_int(item.fluid_container.capacity)} L"
            )
        elif item.get("UseDelta") or item.item_type == "drainable":
            item_dict["capacity"] = f"{util.convert_int(item.units)} units"
        else:
            item_dict["capacity"] = "-"

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name

    return table_type, item_dict


def find_table_type(item: Item):
    return "appearance"


def process_items() -> dict:
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
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("appearance"):
                table_type, item_dict = generate_data(item)

                # Add table_type to dict if it hasn't been added yet.
                if table_type not in items:
                    items[table_type] = []

                items[table_type].append(item_dict)

                item_count += 1

            pbar.update(1)

    echo.info(f"Finished processing {item_count} items for {len(items)} tables.")

    return items


def main():
    Language.get()
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)

    items = process_items()

    table_helper.create_tables(
        "appearance_item_list",
        items,
        table_map=table_map,
        columns=column_headings,
        suppress=True,
        bot_flag_type="appearance_item_list",
        combine_tables=False,
    )


if __name__ == "__main__":
    main()
