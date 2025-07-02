import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.farming import Farming
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "gardening_table.json")

table_map = {}

def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    if table_type == "seed":
        crop = Farming.from_item(item)
    elif table_type == "seed_packet":
        crop = Farming.from_recipe(item.teached_recipes)
    else:
        crop = None

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    item_dict["sprite"] = crop.get_sprite(dim="64x64px") if "sprite" in columns else None
    if "capacity" in columns:
        if item.fluid_container:
            item_dict["capacity"] = f"{util.convert_int(item.fluid_container.capacity)} L"
        elif item.type == "Drainable":
            item_dict["capacity"] = f"{util.convert_int(1 / item.use_delta)} units"
        else:
            item_dict["capacity"] = "-"
    item_dict["cure"] = get_cure(item) if "cure" in columns else None
    item_dict["seed"] = crop.seed_item.icon if "seed" in columns else None
    item_dict["product"] = crop.vegetable_item.icon if "product" in columns else None
    item_dict["water"] = crop.water_needed if "water" in columns else None
    item_dict["grow_time"] = f"{crop.grow_time_days} days" if "grow_time" in columns else None
    item_dict["sow_months"] = "<br>".join(crop.sow_months) if "sow_months" in columns else None
    item_dict["best_months"] = ("<br>".join(crop.best_months) if crop.best_months else "-") if "best_months" in columns else None
    item_dict["poor_months"] = ("<br>".join(crop.risk_months) if crop.risk_months else "-") if "poor_months" in columns else None
    item_dict["teached_recipes"] = "<br>".join(get_teached_recipes(item)) if "teached_recipes" in columns else None

    if "weapon" in columns:
        if item.type == "Weapon":
            item_dict["weapon"] = util.tick(text="Can be used as a weapon", link="Weapon")
        else:
            item_dict["weapon"] = util.cross(text="Cannot be used as a weapon", link="Weapon")
    if "dirt" in columns:
        if item.has_tag("TakeDirt"):
            item_dict["dirt"] = util.tick(text="Can pick-up dirt", link="TakeDirt (tag)")
        else:
            item_dict["dirt"] = util.cross(text="Cannot pick-up dirt", link="TakeDirt (tag)")
    if "dung" in columns:
        if item.has_tag("TakeDung"):
            item_dict["dung"] = util.tick(text="Can pick-up dung", link="TakeDung (tag)")
        else:
            item_dict["dung"] = util.cross(text="Cannot pick-up dung", link="TakeDung (tag)")
    if "plow" in columns:
        if item.has_tag("DigPlow"):
            item_dict["plow"] = util.tick(text="Can plow land", link="Plowed Land")
        else:
            item_dict["plow"] = util.cross(text="Cannot plow land", link="Plowed Land")
    if "scythe" in columns:
        if item.has_tag("Scythe"):
            item_dict["scythe"] = util.tick(text="Can scythe grass", link="Scythe (tag)")
        else:
            item_dict["scythe"] = util.cross(text="Cannot scythe grass", link="Scythe (tag)")
    if "cut_plant" in columns:
        if item.has_tag("CutPlant"):
            item_dict["cut_plant"] = util.tick(text="Can cut plants", link="CutPlant (tag)")
        else:
            item_dict["cut_plant"] = util.cross(text="Cannot cut plants", link="CutPlant (tag)")
    if "dig_worms" in columns:
        if item.has_tag("DigWorms"):
            item_dict["dig_worms"] = util.tick(text="Can dig up worms", link="Worm")
        else:
            item_dict["dig_worms"] = util.cross(text="Cannot dig up worms", link="Worm")
    
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def get_cure(item: Item):
    if item.id_type == "GardeningSprayAphids":
        return "[[File:Insect_Aphid.png|link=Agriculture#Plant diseases|Aphids]]"
    if item.id_type in ("GardeningSprayCigarettes", "InsectRepellent"):
        return "[[File:Insect Fly.png|link=Agriculture#Plant diseases|Flies]]"
    if item.id_type == "GardeningSprayMilk":
        return "[[File:Mildew.png|link=Agriculture#Plant diseases|Mildew]]"
    if item.id_type == "SlugRepellent":
        return "[[File:Snail.png|link=Agriculture#Plant diseases|Slugs]]"
    return "-"


FIX_PRODUCT_ID = {
    "Barley": "BarleySheaf",
    "BroadleafPlantain": "Plantain",
    "Carrot": "Carrots",
    "Habanero": "PepperHabanero",
    "Hemp": "HempBundle",
    "Jalapeno": "PepperJalapeno",
    "Mint": "MintHerb",
    "Poppy": "Poppies",
    "Rose": "Roses",
    "Rye": "RyeSheaf",
    "Sunflower": "SunflowerHead",
    "Wheat": "WheatSheaf",
    "WildGarlic": "WildGarlic2"
}


def get_teached_recipes(item: Item):

    teached_recipes = []
    if item.teached_recipes:
        for recipe in item.teached_recipes:
            result = recipe
            if "BagSeed" in item.id_type:
                rec = item.id_type.split("BagSeed")[0]
                rec = FIX_PRODUCT_ID.get(rec, rec)
                rec_item = Item(rec)

                if rec_item.valid:
                    result = util.link(rec_item.page, recipe)
            teached_recipes.append(result)
    else:
        teached_recipes = ["-"]
    return teached_recipes

def find_table_type(item: Item):
    if item.has_tag("isSeed"):
        return "seed"
    if item.teached_recipes:
        return "seed_packet"
    #if item.has_tag("FarmingLoot", "Compost", "Fertilizer"):
    #    return "farming_loot"
    if item.type in ("Moveable", "Food"):
        return "plant"
    if item.has_tag("TakeDirt", "TakeDung", "DigPlow", "Scythe", "CutPlant"):
        return "tool"
    return "other"    

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("gardening"):
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

    table_helper.create_tables("gardening", items, table_map=table_map, columns=column_headings, suppress=True)

if __name__ == "__main__":
    main()