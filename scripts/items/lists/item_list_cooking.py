import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.evolved_recipe import EvolvedRecipe
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "cooking_table.json")

table_map = {}
evolved_recipes = {}

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
    if "knife_type" in columns:
        if item.has_tag("SharpKnife"):
            item_dict["knife_type"] = util.link("SharpKnife (tag)", "Sharp")
        elif item.has_tag("DullKnife"):
            item_dict["knife_type"] = util.link("DullKnife (tag)", "Dull")
        elif item.has_tag("MeatCleaver"):
            item_dict["knife_type"] = util.link("MeatCleaver (tag)", "Meat Cleaver")
        elif item.has_tag("PizzaCutter"):
            item_dict["knife_type"] = util.link("PizzaCutter (tag)", "Pizza Cutter")
    if "capacity" in columns:
        if item.fluid_container:
            item_dict["capacity"] = f"{util.convert_int(item.fluid_container.capacity)} L"
        elif item.get("UseDelta") or item.type == "Drainable":
            item_dict["capacity"] = f"{util.convert_int(item.units)} units"
        else:
            item_dict["capacity"] = "-"
    if "evolved_recipe" in columns:
        recipes = evolved_recipes.get(item.item_id, ["-"])
        item_dict["evolved_recipe"] = "<br>".join(recipes)
    
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def find_table_type(item: Item):
    global evolved_recipes
    if item.has_tag("MixingUtensil"):
        return "mixing_utensil"
    if item.has_tag("DullKnife") or item.has_tag("SharpKnife") or item.has_tag("MeatCleaver") or item.has_tag("PizzaCutter"):
        return "knife"
    if item.has_tag("BottleOpener") or item.has_tag("CanOpener"):
        return "can_bottle_opener"

    is_evolved_recipe = False
    for recipe_id, evolved_recipe in EvolvedRecipe.all().items():
        if evolved_recipe.base_item.item_id == item.item_id:
            is_evolved_recipe = True
            if item.item_id not in evolved_recipes:
                evolved_recipes[item.item_id] = [] #set
            evolved_recipes[item.item_id].append(evolved_recipe.wiki_link)

    if is_evolved_recipe:
        return "evolved_recipe"
    
    return "other"
    

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("cooking"):
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

    table_helper.create_tables("cooking_item_list", items, table_map=table_map, columns=column_headings, suppress=True, bot_flag_type="cooking_item_list", combine_tables=False)

if __name__ == "__main__":
    main()