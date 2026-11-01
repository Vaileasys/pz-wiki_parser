import os
from tqdm import tqdm

from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.core.cache import save_cache
from scripts.utils import table_helper, echo
from scripts.objects.item import Item
from scripts.items.groups.food_groups import (FoodGroups, include_in_food_groups, is_food_item)

TABLE_PATH = os.path.join(TABLES_DIR, "food_table.json")

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
    """Return the shared food group ID used as the list table type."""
    return FoodGroups.find_type(item)


def find_items():
    food_items: dict[str, Item] = {}
    nutrition_items: dict[str, Item] = {}

    for item_id, item in Item.items():
        if is_food_item(item):
            food_items[item_id] = item

            if item.get("Calories"):
                nutrition_items[item_id] = item

    return food_items, nutrition_items


def main():
    global language_code
    global table_map
    language_code = Language.get()
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)
    save_cache({"recipes": FoodGroups.get_recipe_product_ids()}, "recipe_products_data.json")

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

            if not include_in_food_groups(item):
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
