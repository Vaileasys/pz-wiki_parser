import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "household_table.json")

table_map = {}

def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    if "weapon" in columns:
        if item.type == "Weapon":
            item_dict["weapon"] = util.tick(text="Can be used as a weapon", link="Weapon")
        else:
            item_dict["weapon"] = util.cross(text="Cannot be used as a weapon", link="Weapon")
    if "capacity" in columns:
        if item.fluid_container:
            item_dict["capacity"] = f"{util.convert_int(item.fluid_container.capacity)} L"
        elif item.type == "Drainable":
            item_dict["capacity"] = f"{util.convert_int(1 / item.use_delta)} units"
        else:
            item_dict["capacity"] = "-"
    if "color" in columns:
        colors = []
        if item.has_tag("Pen"):
            colors.append(util.rgb(0.129, 0.129, 0.129))
        if item.has_tag("Pencil"):
            colors.append(util.rgb(0.2, 0.2, 0.2))
        if item.has_tag("RedPen"):
            colors.append(util.rgb(0.65, 0.054, 0.054))
        if item.has_tag("BluePen"):
            colors.append(util.rgb(0.156, 0.188, 0.49))
        if item.has_tag("GreenPen"):
            colors.append(util.rgb(0.06, 0.39, 0.17))
        if not colors:
            colors = ["-"]
        item_dict["color"] = " ".join(colors)
    if "eraser" in columns:
        if item.has_tag("Eraser"):
            item_dict["eraser"] = util.tick(text="Can remove writing")
        else:
            item_dict["eraser"] = util.cross(text="Cannot remove writing")

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def find_table_type(item: Item):
    if item.has_tag("Write", "Eraser"):
        return "writing"
    if (
        item.has_tag("CleanStains")
        or Item(item.item_when_dry).has_tag("CleanStains")
        or Item(item.replace_on_deplete).has_tag("CleanStains")
        or item.id_type == "Soap2"
        or item.fluid_container.has_fluid("Bleach", "CleaningLiquid")
        ):
        return "cleaning"
    return "other"    

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("household"):
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

    table_helper.create_tables("household", items, table_map=table_map, columns=column_headings, suppress=True)

if __name__ == "__main__":
    main()