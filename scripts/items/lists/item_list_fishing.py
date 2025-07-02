import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "fishing_table.json")

table_map = {}

def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    item_dict["type"] = find_type(item) if "type" in columns else None
    if "weapon" in columns:
        if item.type == "Weapon":
            weapon = util.tick(text="Can be used as a weapon", link="Weapon")
        else:
            weapon = util.cross(text="Cannot be used as a weapon", link="Weapon")
        item_dict["weapon"] = weapon
    item_dict["tooltip"] = (item.tooltip or "-") if "tooltip" in columns else None

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def find_type(item: Item):
    item_types = []

    if item.has_tag("FishingNet"):
        item_types.append(Item("FishingNet").name)
    if item.has_tag("FishingRod"):
        item_types.append(Item("FishingRod").name)
    if item.has_tag("FishingSpear"):
        item_types.append("Fishing Spear")
    if item.fishing_lure:
        item_types.append("Lure")
    if item.has_tag("FishingHook"):
        item_types.append("Hook")
    if item.has_tag("FishingLine"):
        item_types.append("Line")
    if item.id_type in ("Bobber"):
        item_types.append("Bobber")
    if "AddBaitToChum" in item.evolved_recipe:
        item_types.append(f"{util.link(Item('Chum').name)} Ingredient")

    if not item_types:
        return "-"
    
    return "<br>".join(item_types)


def find_table_type(item: Item):
    if item.has_tag("FishingHook", "FishingLine") or item.fishing_lure or item.id_type in ("Bobber", "FishingHookBox"):
        return "tackle"
    if item.has_tag("FishingSpear", "FishingRod", "FishingNet") or item.id_type in ("FishingRodBreak", "BrokenFishingNet"):
        return "gear"
    return "other"    

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("fishing"):
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

    table_helper.create_tables("fishing", items, table_map=table_map, columns=column_headings, suppress=True)

if __name__ == "__main__":
    main()