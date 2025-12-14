import os
from tqdm import tqdm

from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.core.cache import save_cache
from scripts.utils import table_helper, echo
from scripts.objects.item import Item
from scripts.objects.forage import ForagingItem
from scripts.objects.craft_recipe import CraftRecipe
from scripts.objects.evolved_recipe import EvolvedRecipe

TABLE_PATH = os.path.join(TABLES_DIR, "food_table.json")

evolvedrecipe_results = []
evolvedrecipe_base = []
recipe_products = []
forage_categories = {}
table_map = {}


def generate_data(item: Item, table_type: str):
    columns = (
        table_map.get(table_type)
        if table_map.get(table_type) is not None
        else table_map.get("default")
    )

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = item.weight if "weight" in columns else None
    item_dict["hunger"] = (item.hunger_change or "-") if "hunger" in columns else None
    if "hunger_weight" in columns:
        hunger_weight = (
            item.hunger_change / item.weight
            if item.weight and item.hunger_change
            else None
        )
        if not hunger_weight:
            item_dict["hunger_weight"] = "-"
        else:
            item_dict["hunger_weight"] = f"{hunger_weight:.0f}"
    item_dict["thirst"] = (item.thirst_change or "-") if "thirst" in columns else None
    item_dict["calories"] = (
        ((item.calories if item.get("Calories") else "-") or "0")
        if "calories" in columns
        else None
    )
    item_dict["carbohydrates"] = (
        ((item.carbohydrates if item.get("Carbohydrates") else "-") or "0")
        if "carbohydrates" in columns
        else None
    )
    item_dict["lipids"] = (
        ((item.lipids if item.get("Lipids") else "-") or "0")
        if "lipids" in columns
        else None
    )
    item_dict["proteins"] = (
        ((item.proteins if item.get("Proteins") else "-") or "0")
        if "proteins" in columns
        else None
    )
    if "unhappiness" in columns:
        unhappiness = item.unhappy_change
        if unhappiness and item.remove_unhappiness_when_cooked:
            item_dict["unhappiness"] = f"{unhappiness}*"
        elif unhappiness:
            item_dict["unhappiness"] = unhappiness
        else:
            item_dict["unhappiness"] = "-"
    item_dict["boredom"] = (
        (item.boredom_change or "-") if "boredom" in columns else None
    )
    item_dict["stress"] = (item.stress_change or "-") if "stress" in columns else None
    item_dict["fatigue"] = (
        (item.fatigue_change or "-") if "fatigue" in columns else None
    )
    item_dict["alcohol"] = (item.alcoholic or "-") if "alcohol" in columns else None
    if "sickness" in columns:  # TODO: look at raw food
        if item.reduce_food_sickness:
            item_dict["sickness"] = item.reduce_food_sickness
        elif item.dangerous_uncooked:
            item_dict["sickness"] = "?"
        else:
            item_dict["sickness"] = "-"
    item_dict["poison"] = (item.poison_power or "-") if "poison" in columns else None
    item_dict["fresh"] = (item.days_fresh or "∞") if "fresh" in columns else None
    item_dict["rotten"] = (
        (item.days_totally_rotten or "∞") if "rotten" in columns else None
    )
    item_dict["cooked"] = (
        ((item.minutes_to_cook if item.is_cookable else "-") or "-")
        if "cooked" in columns
        else None
    )
    item_dict["burned"] = (
        ((item.minutes_to_burn if item.is_cookable else "-") or "-")
        if "burned" in columns
        else None
    )
    if "spice" in columns:
        if item.spice:
            item_dict["spice"] = "[[File:UI Tick.png|link=|Used as spice in cooking]]"
        else:
            item_dict["spice"] = (
                "[[File:UI Cross.png|link=|Used as ingredient in cooking]]"
            )
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name

    return item_dict


def find_table_type(item: Item):
    display_name = item.name_en
    table_type = None
    if item.id_type in evolvedrecipe_results or item.item_id in evolvedrecipe_results:
        table_type = "evolved_recipes"
    elif item.id_type in evolvedrecipe_base or item.item_id in evolvedrecipe_base:
        table_type = "evolved_recipes_base"
    elif "Canned" in display_name or "Can of Food" in display_name:
        table_type = "canned"
    elif "Jar of" in display_name and item.id_type.startswith("Canned"):
        table_type = "pickled"
    else:
        food_type = item.food_type.lower() if item.food_type else ""
        foraging_item = ForagingItem(item.id_type)
        if food_type == "egg" or item.id_type in ("EggCarton"):
            table_type = "egg"
        elif food_type == "candy" or item.id_type in (
            "CandyPackage",
            "Lollipop",
            "MintCandy",
            "Gum",
            "Chocolate",
        ):
            table_type = "candy"
        elif food_type == "herb" or foraging_item.has_category("WildHerbs"):
            table_type = "herb"
        elif (
            food_type
            in ("vegetable", "vegetables", "mushroom", "greens", "hotpepper", "bean")
            or foraging_item.has_category("Vegetables", "Mushrooms")
            or item.id_type in ("Squash", "PumpkinSliced", "PumpkinSmashed")
        ):
            table_type = "vegetable"
        elif food_type in ("fruits", "citrus", "berry") or foraging_item.has_category(
            "Berries", "Fruits"
        ):
            table_type = "fruit"
        elif food_type in (
            "meat",
            "poultry",
            "bacon",
            "beef",
            "sausage",
            "venison",
        ) or item.id_type in ("HotdogPack"):
            table_type = "meat"
        elif (
            food_type in ("seafood", "fish", "roe")
            or item.has_tag("FishMeat")
            or "Fish" in display_name
            or item.id_type in ("Mussels")
        ):
            table_type = "seafood"
        elif food_type == "insect" or foraging_item.has_category("Insects", "FishBait"):
            table_type = "insect"
        elif food_type == "game" or "Dead" in display_name:
            table_type = "game"
        elif item.item_id in recipe_products:
            table_type = "prepared"
        elif (
            food_type in ("bread", "pasta", "rice")
            or item.id_type in ("BunsHamburger", "BunsHotdog")
            or ""
        ):
            table_type = "grains"
        elif item.spice:
            table_type = "spice"
        elif (
            foraging_item.has_category("WildPlants")
            or "Sheaf" in item.id_type
            or "Rippled" in item.id_type
            or "Tuft" in item.id_type
            or "Hemp" in item.id_type
            or "Hops" in item.id_type
            or "Dried" in item.id_type
        ):
            table_type = "plant"
        elif food_type in (
            "cheese",
            "chocolate",
            "cocoa",
            "coffee",
            "oil",
            "nut",
            "seed",
            "stock",
            "sugar",
            "tea",
            "thickener",
            "catfood",
            "dogfood",
            "noexplicit",
        ):
            table_type = "miscellaneous"
        elif food_type:
            table_type = item.food_type

    return table_type if table_type else "miscellaneous"


def find_items():
    food_items: dict[str, Item] = {}
    nutrition_items: dict[str, Item] = {}

    for item_id, item in Item.items():
        if item.type == "food" or item.display_category == "Food":
            food_items[item_id] = item

            if item.get("Calories"):
                nutrition_items[item_id] = item

    return food_items, nutrition_items


def main():
    global language_code
    global evolvedrecipe_results
    global evolvedrecipe_base
    global recipe_products
    global table_map
    language_code = Language.get()
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)

    # cooking_recipe_data = {}
    for recipe_id, recipe in CraftRecipe.all().items():
        blacklisted_recipes = [
            "SlicePumpkin",
            "SliceWatermelon",
            "SmashPumpkin",
            "SmashWatermelon",
            "OpenPackOfBuns",
            "OpenCandyPackage",
            "OpenMacAndCheese",
            "PutEggsInCarton",
            "OpenEggCarton",
        ]
        # Skip blacklisted recipes
        if recipe_id in blacklisted_recipes:
            continue

        if recipe.category == "Cooking":
            # cooking_recipe_data[recipe_id] = recipe.data
            # Get output items directly from the CraftRecipe object
            recipe_products.extend(recipe.output_items)

    # save_cache(cooking_recipe_data, "cooking_recipe_data.json")
    save_cache({"recipes": recipe_products}, "recipe_products_data.json")

    # Store all evolvedrecipe products in a list for determining section
    for er in EvolvedRecipe.values():
        result = er.result_item
        if result and result.valid:
            evolvedrecipe_results.append(result.item_id)
        else:
            echo.warning(f"EvolvedRecipe with invalid result item: {er.recipe_id}")

        base = er.base_item
        if base and base.valid:
            evolvedrecipe_base.append(base.item_id)
        else:
            echo.warning(f"EvolvedRecipe with invalid base item: {er.recipe_id}")

    with tqdm(
        total=0,
        desc="Preparing items",
        bar_format=PBAR_FORMAT,
        unit=" items",
        leave=False,
    ) as pbar:
        food_items, nutrition_items = find_items()

        # Update the total once we know how many items
        pbar.total = len(food_items) + len(nutrition_items)
        pbar.refresh()

        all_food_data = {"nutrition": []}

        # Process food items
        for item_id, item in food_items.items():
            pbar.set_postfix_str(f"Generating: Food ({item_id[:40]})")

            # Blacklisted types of items
            if item.has_tag("Smokable", "Feather"):
                continue
            # Animal parts
            if (
                any(x in item.name_en for x in ("Head", "Animal"))
                and "Sunflower" not in item.name_en
            ):
                continue
            # Droppings
            if any(x in item.name_en for x in ("Dung", "Droppings")):
                continue
            if item.foraging:
                if (
                    item.foraging.has_category("MedicinalPlants", "Medical")
                    and not item.hunger_change
                ):
                    continue
            if item.eat_type == "pipe":
                continue

            table_type = find_table_type(item)
            food_data = generate_data(item, table_type)

            if table_type not in all_food_data:
                all_food_data[table_type] = []

            all_food_data[table_type].append(food_data)

            pbar.update(1)

        # Process nutrition items
        for item_id, item in nutrition_items.items():
            pbar.set_postfix_str(f"Generating: Nutrition ({item_id[:40]})")
            nutrition_data = generate_data(item, "nutrition")
            all_food_data["nutrition"].append(nutrition_data)

            pbar.update(1)

        pbar.set_postfix_str("Creating tables...")
        table_helper.create_tables(
            "food_item_list",
            all_food_data,
            table_map=table_map,
            columns=column_headings,
            bot_flag_type="food_item_list",
            combine_tables=False,
            drop_empty_columns=True,
        )


if __name__ == "__main__":
    main()
