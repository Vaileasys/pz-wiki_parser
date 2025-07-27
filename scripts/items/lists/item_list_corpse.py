import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.animal import Animal, AnimalBreed
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "corpse_table.json")

table_map = {}

def generate_data(item: Item, animal: Animal = None, breed: AnimalBreed = None, stage: str = None):
    table_type = find_table_type(item, stage)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    if animal:
        if stage == "skeleton":
            item_dict["icon"] = breed.icon_skeleton or breed.icon_dead or breed.icon or "-"
            item_dict["name"] = breed.get_link("skeleton") or "-"
            item_dict["weight"] = f"{animal.min_weight}–{animal.max_weight}"
            item_dict["group"] = animal.group_link or "-"
            item_dict["breed_id"] = breed.breed_id
            item_dict["animal_id"] = animal.animal_id
        else: # stage == "dead"
            item_dict["icon"] = breed.icon_dead or breed.icon or "-"
            item_dict["name"] = breed.get_link("dead") or "-"
            item_dict["weight"] = f"{animal.min_weight}–{animal.max_weight}"
            item_dict["group"] = animal.group_link or "-"
            item_dict["breed_id"] = breed.breed_id
            item_dict["animal_id"] = animal.animal_id
    else:
        item_dict["icon"] = item.icon if "icon" in columns else None
        item_dict["name"] = item.wiki_link if "name" in columns else None
        item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None

    
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    if animal:
        item_dict["item_name"] = breed.get_name(stage)
    
    return table_type, item_dict


def find_table_type(item: Item, stage: str = None):
    if item.item_id == "Base.CorpseAnimal":
        return f"animal_{stage}"
    return "corpse"


def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count() + Animal.count() - 1, desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("corpse"):
                if item_id == "Base.CorpseAnimal":
                    for animal_id, animal in Animal.all().items():
                        for breed in animal.breeds:
                            stages = ["dead"] # ["dead", "skeleton"] - skeleton icons are not currently used, and weight is the same as dead
                            for stage in stages:
                                table_type, item_dict = generate_data(item, animal, breed, stage)

                                # Add table_type to dict if it hasn't been added yet.
                                if table_type not in items:
                                    items[table_type] = []

                                items[table_type].append(item_dict)

                        item_count += 1

                else:
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

    table_helper.create_tables("corpse", items, table_map=table_map, columns=column_headings, suppress=True, bot_flag_type="corpse_item_list", combine_tables=False)

if __name__ == "__main__":
    main()