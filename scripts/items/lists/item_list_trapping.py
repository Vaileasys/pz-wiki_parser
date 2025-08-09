import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.trap import Trap
from scripts.utils import table_helper, lua_helper, echo, util
from scripts.core.cache import save_cache

TABLE_PATH = os.path.join(TABLES_DIR, "trapping_table.json")

table_map = {}

def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item = Trap(item) if item.trap else item

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["sprite"] = get_trap_sprite(item) if "sprite" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    item_dict["strength"] = (item.trap_strength if item.trap else "-") if "strength" in columns else None
    item_dict["mouse"] = check_animal(item, "mouse") if "mouse" in columns else None
    item_dict["rat"] = check_animal(item, "rat") if "rat" in columns else None
    item_dict["squirrel"] = check_animal(item, "squirrel") if "squirrel" in columns else None
    item_dict["rabbit"] = check_animal(item, "rabbit") if "rabbit" in columns else None
    item_dict["bird"] = check_animal(item, "bird") if "bird" in columns else None
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def check_animal(item: Trap, query_animal: str):
    if not isinstance(item, Trap):
        return "-"
    
    for animal_type, animal in item.animals.items():
        if animal_type != query_animal:
            continue

        return item.animal_chances.get(animal_type)
    
    return "-"


def get_trap_sprite(item: Trap):
    if not isinstance(item, Trap):
        return "-"
    return f'<span class="cycle-img">{item.get_sprite(sprite="sprite", dim="64x64px")}{item.get_sprite(sprite="closed_sprite", dim="64x64px")}</span>'


def find_table_type(item: Item):
    return "trap"

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("trapping"):
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

    table_helper.create_tables("trapping_item_list", items, table_map=table_map, columns=column_headings, suppress=True, bot_flag_type="trapping_item_list", combine_tables=False)

if __name__ == "__main__":
    main()