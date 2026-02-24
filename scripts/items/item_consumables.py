"""
Consumables template generator.

This module processes food items, generating a `{{Consumables}}` templates
for each valid food item and writes to individual text files for use on the PZwiki.
"""

import os
from scripts.core.file_loading import write_file, clear_dir
from scripts.core.constants import ITEM_DIR
from scripts.objects.item import Item
from scripts.utils import util, echo

ROOT_DIR = os.path.join(ITEM_DIR, "consumable_properties")


def get_variant(item: Item, variant: str = None):
    """
    Returns the icon for a specific variant of the item, if it exists.

    Args:
        item (Item): Item object to get icons for.
        variant (str, optional): Variant type such as 'cooked', 'rotten', or 'burnt'.

    Returns:
        str: Icon filename for the variant, or the base icon if not found.
    """
    VARIANTS = {
        "rotten": ["Rotten", "Spoiled"],
        "cooked": ["Cooked"],
        "burnt": ["Burnt", "Overdone"],
    }

    icons = item.get_icon(format=False, cycling=False)
    if not variant or variant.lower() not in VARIANTS:
        return icons[0]

    variant = variant.lower()
    for icon in icons:
        icon_name = icon.removesuffix(".png")
        if any(icon_name.lower().endswith(v.lower()) for v in VARIANTS[variant]):
            return icon

    return icons[0]


def generate_data(item: Item):
    """
    Extracts and formats consumable data for a given item.

    Args:
        item (Item): The item to generate data from.

    Returns:
        dict | None: Dictionary of parameters for the template, or None if not applicable.
    """
    if item.item_type == "food" and (item.is_cookable or item.get("DaysTotallyRotten")):
        try:
            perishable = "true" if item.get("DaysTotallyRotten") else None

            parameters = {
                "item_id": item.item_id,
                "name": item.name,
                "image": get_variant(item),
                "cooked_image": get_variant(item, "cooked")
                if item.is_cookable
                else None,
                "rotten_image": get_variant(item, "rotten") if perishable else None,
                "burned_image": get_variant(item, "burnt")
                if item.is_cookable
                else None,
                "hunger": util.convert_int(item.hunger_change)
                if item.hunger_change
                else None,
                "boredom": util.convert_int(item.boredom_change)
                if item.boredom_change
                else None,
                "unhappiness": util.convert_int(item.unhappy_change)
                if item.unhappy_change
                else None,
                "dangerous_uncooked": "true" if item.dangerous_uncooked else None,
                "egg": item.has_tag("Egg"),
                "cookable": "true" if item.is_cookable else None,
                "perishable": perishable,
                "RemoveNegativeEffectOnCooked": "true"
                if item.remove_negative_effect_on_cooked
                else None,
            }

            item_data = {}
            for key, value in parameters.items():
                if value:
                    item_data[key] = value

            return item_data

        except Exception as e:
            echo.error(f"Error generating data for {item.item_id}.txt: {e}", True)


def build_template(data):
    """
    Builds a `{{Consumables}}` template from the item data.

    Args:
        data (dict): Parameter data for the template.

    Returns:
        list[str]: Lines of the wiki template content.
    """
    content = []
    content.append("{{Consumables")
    for key, value in data.items():
        content.append(f"|{key}={value}")
    content.append("}}")
    return content


def process_items(items_list):
    """
    Processes a list of item IDs and writes their template files.

    Args:
        items_list (list[str]): List of item IDs to process.
    """
    clear_dir(directory=ROOT_DIR)
    output_dir = ROOT_DIR
    for item_id in items_list:
        item = Item(item_id)
        item_data = generate_data(item)

        if not item_data:
            continue

        content = build_template(item_data)
        output_dir = write_file(
            content, rel_path=f"{item.item_id}.txt", root_path=ROOT_DIR, suppress=True
        )
    echo.success(f"Consumables template files written to '{output_dir}'")


def select_item():
    """
    Prompts user to input a valid item ID.

    Returns:
        list[str]: A list containing a single validated item ID.
    """
    while True:
        query_item_id = input("Enter an item id\n> ")
        if Item.exists(query_item_id):
            return [query_item_id]
        print(f"No item found for '{query_item_id}', please try again.")


def main(run_directly=False):
    """
    Main entry point for the generator. Prompts user for input mode and processes items.

    Args:
        run_directly (bool, optional): If True, enables quit option instead of back. Defaults to False.
    """
    items_list = list(Item.keys())
    back = "Q: Quit" if run_directly else "B: Back"
    while True:
        print("\nWhich items do you want to generate a consumables template for?")
        choice = input(f"1: All items\n2: Single item\n{back}\n> ").strip().lower()
        if choice == "2":
            items_list = select_item()

        if choice in ["1", "2"]:
            process_items(items_list)
            return
        elif choice.lower() == ("q" if run_directly else "b"):
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main(True)
