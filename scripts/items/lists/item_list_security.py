import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "security_table.json")

table_map = {}

def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    if "type" in columns:
        if item.has_tag("Lock"):
            item_dict["type"] = "Lock"
        elif item.type == "Key":
            item_dict["type"] = "Key"
        else:
            item_dict["type"] = "-"
    if "lock_unlock" in columns:
        locks = []
        if item.has_tag("CarKey"):
            locks.append(util.link("Vehicle"))
        if item.has_tag("BuildingKey"):
            locks.append(util.link("Door"))
        if item.id_type in ("Padlock", "CombinationPadlock"):
            locks.extend([util.link("Wooden Crate"), util.link("Metal Crate")])
        if item.id_type == "KeyPadlock":
            locks.append(Item("Base.Padlock").wiki_link)
        item_dict["lock_unlock"] = "<br>".join(locks) if locks else "-"
        
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def find_table_type(item: Item):
    return "security"

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("security"):
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

    table_helper.create_tables("security", items, table_map=table_map, columns=column_headings, suppress=True)

if __name__ == "__main__":
    main()