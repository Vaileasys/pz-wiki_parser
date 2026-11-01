import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.items.groups.material_groups import MaterialGroups
from scripts.objects.craft_recipe import CraftRecipe
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "material_table.json")

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
    if "weapon" in columns:
        if item.item_type == "weapon":
            item_dict["weapon"] = util.tick(
                text="Can be used as a weapon", link="Weapon"
            )
        else:
            item_dict["weapon"] = util.cross(
                text="Cannot be used as a weapon", link="Weapon"
            )
    if "leather_type" in columns:
        leather_type_dict = {
            "Unprocessed": [
                "LeatherFullLarge",
                "LeatherFullMedium",
                "LeatherFullSmall",
            ],
            "Furred": [
                "LeatherFurLarge",
                "LeatherFurMedium",
                "LeatherFurSmall",
                "LeatherFurWetLarge",
                "LeatherFurWetMedium",
                "LeatherFurWetSmall",
                "LeatherFurTannedLarge",
                "LeatherFurTannedMedium",
                "LeatherFurTannedSmall",
            ],
            "Crude": [
                "LeatherCrudeLarge",
                "LeatherCrudeMedium",
                "LeatherCrudeSmall",
                "LeatherCrudeWetLarge",
                "LeatherCrudeWetMedium",
                "LeatherCrudeWetSmall",
                "LeatherCrudeTannedLarge",
                "LeatherCrudeTannedMedium",
                "LeatherCrudeTannedSmall",
            ],
            "Wet": [
                "LeatherCrudeWetLarge",
                "LeatherCrudeWetMedium",
                "LeatherCrudeWetSmall",
                "LeatherFurWetLarge",
                "LeatherFurWetMedium",
                "LeatherFurWetSmall",
            ],
            "Tanned": [
                "LeatherCrudeWetLarge",
                "LeatherCrudeWetMedium",
                "LeatherCrudeWetSmall",
                "LeatherCrudeTannedLarge",
                "LeatherCrudeTannedMedium",
                "LeatherCrudeTannedSmall",
                "LeatherFurWetLarge",
                "LeatherFurWetMedium",
                "LeatherFurWetSmall",
                "LeatherFurTannedLarge",
                "LeatherFurTannedMedium",
                "LeatherFurTannedSmall",
            ],
        }
        leather_types = []
        for type, type_list in leather_type_dict.items():
            if item.has_tag(type_list):
                leather_types.append(type)
        if not leather_types:
            leather_types = ["-"]
        item_dict["leather_type"] = "<br>".join(leather_types)

    if "leather_size" in columns:
        if item.has_tag(
            "LeatherCrudeLarge",
            "LeatherCrudeWetLarge",
            "LeatherCrudeTannedLarge",
            "LeatherFurLarge",
            "LeatherFurWetLarge",
            "LeatherFurTannedLarge",
            "LeatherFullLarge",
        ):
            leather_size = "Large"
        elif item.has_tag(
            "LeatherCrudeMedium",
            "LeatherCrudeWetMedium",
            "LeatherCrudeTannedMedium",
            "LeatherFurMedium",
            "LeatherFurWetMedium",
            "LeatherFurTannedMedium",
            "LeatherFullMedium",
        ):
            leather_size = "Medium"
        elif item.has_tag(
            "LeatherCrudeSmall",
            "LeatherCrudeWetSmall",
            "LeatherCrudeTannedSmall",
            "LeatherFurSmall",
            "LeatherFurWetSmall",
            "LeatherFurTannedSmall",
            "LeatherFullSmall",
        ):
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
        item_dict["capacity"] = (
            f"{util.convert_int(item.units)} units"
            if (item.get("UseDelta") or item.item_type == "drainable")
            else "-"
        )
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
    return MaterialGroups.find_type(item)


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

    table_helper.create_tables(
        "material_item_list",
        items,
        table_map=table_map,
        columns=column_headings,
        suppress=True,
        bot_flag_type="material_item_list",
        combine_tables=False,
    )


if __name__ == "__main__":
    main()
