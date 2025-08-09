import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.craft_recipe import CraftRecipe
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "material_table.json")

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
    if "leather_type" in columns:
        leather_type_dict = {
            "Unprocessed": [
                "LeatherFullLarge", "LeatherFullMedium", "LeatherFullSmall"
            ],
            "Furred": [
                "LeatherFurLarge", "LeatherFurMedium", "LeatherFurSmall", 
                "LeatherFurWetLarge", "LeatherFurWetMedium", "LeatherFurWetSmall", 
                "LeatherFurTannedLarge", "LeatherFurTannedMedium", "LeatherFurTannedSmall"
            ],
            "Crude": [
                "LeatherCrudeLarge", "LeatherCrudeMedium", "LeatherCrudeSmall",
                "LeatherCrudeWetLarge", "LeatherCrudeWetMedium", "LeatherCrudeWetSmall",
                "LeatherCrudeTannedLarge", "LeatherCrudeTannedMedium", "LeatherCrudeTannedSmall"
            ],
            "Wet": [
                "LeatherCrudeWetLarge", "LeatherCrudeWetMedium", "LeatherCrudeWetSmall", 
                "LeatherFurWetLarge", "LeatherFurWetMedium", "LeatherFurWetSmall", 
            ],
            "Tanned": [
                "LeatherCrudeWetLarge", "LeatherCrudeWetMedium", "LeatherCrudeWetSmall",
                "LeatherCrudeTannedLarge", "LeatherCrudeTannedMedium", "LeatherCrudeTannedSmall", 
                "LeatherFurWetLarge", "LeatherFurWetMedium", "LeatherFurWetSmall", 
                "LeatherFurTannedLarge", "LeatherFurTannedMedium", "LeatherFurTannedSmall"
            ]
        }
        leather_types = []
        for type, type_list in leather_type_dict.items():
            if item.has_tag(type_list):
                leather_types.append(type)
        if not leather_types:
            leather_types = ["-"]
        item_dict["leather_type"] = "<br>".join(leather_types)

    if "leather_size" in columns:
        if item.has_tag("LeatherCrudeLarge", "LeatherCrudeWetLarge", "LeatherCrudeTannedLarge",
                        "LeatherFurLarge", "LeatherFurWetLarge", "LeatherFurTannedLarge",
                        "LeatherFullLarge"):
            leather_size = "Large"
        elif item.has_tag("LeatherCrudeMedium", "LeatherCrudeWetMedium", "LeatherCrudeTannedMedium",
                          "LeatherFurMedium", "LeatherFurWetMedium", "LeatherFurTannedMedium",
                          "LeatherFullMedium"):
            leather_size = "Medium"
        elif item.has_tag("LeatherCrudeSmall", "LeatherCrudeWetSmall", "LeatherCrudeTannedSmall",
                          "LeatherFurSmall", "LeatherFurWetSmall", "LeatherFurTannedSmall",
                          "LeatherFullSmall"):
            leather_size = "Small"
        else:
            leather_size = "-"
        item_dict["leather_size"] = leather_size
    if "metal_size" in columns:
        if item.has_tag("SmeltableIronLarge", "SmeltableSteelLarge"):
            metal_size = "Large"
        elif item.has_tag("SmeltableIronSmall", "SmeltableSteelSmall"):
            metal_size = "Small"
        elif item.has_tag("SmeltableIronMedium", "SmeltableSteelMedium"):
            metal_size = "Medium"
        elif item.has_tag("SmeltableIronMediumPlus", "SmeltableSteelMediumPlus"):
            metal_size = "Medium+"
        else:
            metal_size = "-"
        item_dict["metal_size"] = metal_size
    if "capacity" in columns:
        item_dict["capacity"] = f"{util.convert_int(item.units)} units" if (item.get("UseDelta") or item.type == "Drainable") else "-"
#    item_dict["product"] = find_product(item) if "product" in columns else None

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def find_product(item: Item):
    products = []
    for recipe_id, recipe in CraftRecipe.all().items():
        if item.item_id in recipe.input_items:
            products.extend(recipe.output_items)
    
    if len(products) == 1:
        return Item(products[0]).icon
    else:
        # TODO: correctly get all the recipe products
        return "-"
    return "<br>".join(products)



def find_table_type(item: Item):
    if item.has_tag("ToolHead", "SawBlade") or (("Head" in item.id_type or "Blade" in item.id_type) and not "Broken" in item.id_type):
        return "tool_head"
    if (item.has_tag("LeatherCrudeLarge", "LeatherCrudeWetLarge", "LeatherCrudeTannedLarge",
                    "LeatherCrudeMedium", "LeatherCrudeWetMedium", "LeatherCrudeTannedMedium",
                    "LeatherCrudeSmall", "LeatherCrudeWetSmall", "LeatherCrudeTannedSmall",
                    "LeatherFurLarge", "LeatherFurWetLarge", "LeatherFurTannedLarge",
                    "LeatherFurMedium", "LeatherFurWetMedium", "LeatherFurTannedMedium",
                    "LeatherFurSmall", "LeatherFurWetSmall", "LeatherFurTannedSmall",
                    "LeatherFullLarge", "LeatherFullMedium", "LeatherFullSmall"
                    )
        or "Leather" in item.id_type
        or item.fabric_type == "Leather"
        or "Hide" in item.id_type
        ):
        return "leather"
    if "Denim" in item.id_type:
        return "denim"
    if item.get("DisplayCategory") == "Paint":
        return "paint"
    if item.has_tag("Wallpaper"):
        return "wallpaper"
    if ("Iron" in item.id_type
        or "Hematite" in item.id_type
        or item.has_tag("SmeltableIronLarge", "SmeltableIronMedium", "SmeltableIronMediumPlus", "SmeltableIronSmall")):
        return "iron"
    if "Steel" in item.id_type or item.has_tag("SmeltableSteelLarge", "SmeltableSteelMedium", "SmeltableSteelMediumPlus", "SmeltableSteelSmall"):
        return "steel"
    if "Copper" in item.id_type or "Malachite" in item.id_type:
        return "copper"
    if ("Clay" in item.id_type or "Ceramic" in item.id_type or "Unfired" in item.id_type) and not "CrucibleWith" in item.id_type:
        return "clay"
    if "Brass" in item.id_type:
        return "brass"
    if "Silver" in item.id_type:
        return "silver"
    if "Gold" in item.id_type:
        return "gold"
    if ("Aluminum" in item.id_type
        or item.has_tag("Aluminum", "ScrapAluminum")):
        return "aluminum"
    if "Glass" in item.id_type:
        return "glass"
    if ("Stone" in item.id_type
        or "Limestone" in item.id_type
        or "Quicklime" in item.id_type
        or item.has_tag("Stone", "Limestone")):
        return "stone"
    if "Sheet" in item.id_type or "Cotton" in item.id_type:
        return "cotton"
    if (item.has_tag("Thread", "HeavyThread", "Twine")
        or "Flax" in item.id_type
        or "Hemp" in item.id_type
        or "Burlap" in item.id_type
        or "Dogbane" in item.id_type
        or "String" in item.id_type
        or "Rope" in item.id_type
        or "Yarn" in item.id_type
        or "WoolRaw" in item.id_type
        or "CheeseCloth" in item.id_type
        ):
        return "fibre"
    if (item.has_tag("Glue", "Tape", "FiberglassTape", "Epoxy")
        or "Zipties" in item.id_type):
        return "repair"
    if item.has_tag("AnimalBone", "LargeAnimalBone") or "Bone" in item.id_type:
        return "bone"
    if ("Wood" in item.id_type
        or "Twigs" in item.id_type
        or "Firewood" in item.id_type
        or "LogStack" in item.id_type
        or "Branch" in item.id_type
        or "Plank" in item.id_type
        or item.has_tag("WoodHandle", "Log", "LongStick", "MakeWoodCharcoalLarge", "MakeWoodCharcoalSmall", "MakeWoodCharcoalMedium")
        ):
        return "wood"
    if item.has_tag("Charcoal"):
        return "charcoal"
    return "other"

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("material"):
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

    table_helper.create_tables("material_item_list", items, table_map=table_map, columns=column_headings, suppress=True, bot_flag_type="material_item_list", combine_tables=False)

if __name__ == "__main__":
    main()