#!/usr/bin/env python3

import os
from tqdm import tqdm
from scripts.core.constants import ITEM_DIR, PBAR_FORMAT
from scripts.core.file_loading import write_file
from scripts.core.language import Language
from scripts.objects.evolved_recipe import EvolvedRecipe
from scripts.objects.item import Item
from scripts.utils import echo

INGREDIENTS_DIR = os.path.join("output", "recipes", "evolved_recipes", "ingredients")
TEMPLATE_DIR = os.path.join("output", "recipes", "evolved_recipes", "template")


def format_recipe_info(recipe):
    """
    Format evolved recipe information in wiki article format.

    Args:
        recipe (EvolvedRecipe): The evolved recipe object to format

    Returns:
        list: Formatted lines for the wiki article
    """
    lines = []

    # Starting Item Section
    if recipe.base_item:
        lines.append("===Evolved recipe===\n====Starting item====")
        # Get just the first icon filename without any formatting
        # Use get_icon with all_icons=False to get only the first icon
        icon_name = (
            recipe.base_item.get_icon(format=False, all_icons=False)
            .split("|")[0]
            .replace("[[File:", "")
            .strip()
        )
        # Get just the page name without any formatting
        page_name = recipe.base_item.page
        lines.append(
            f"[[File:{icon_name}|32x32px|link={page_name}|{page_name}]] [[{page_name}]]"
        )
        lines.append("")

    # Ingredients Section
    lines.append("====Ingredients====")

    # Recipe description
    description = [
        f"The recipe {recipe.name.lower()} has a maximum of {recipe.max_items} ingredients."
    ]

    if recipe.can_add_spices_empty:
        description.append(
            "The maximum ingredient count does not include condiments or spices."
        )

    if recipe.allow_frozen:
        description.append("Frozen ingredients can be used.")
    else:
        description.append("Frozen ingredients can not be used.")

    if recipe.minimum_water > 0.0:
        water_ml = int(recipe.minimum_water * 1000)
        description.append(f"It requires at least {water_ml}mL of water.")

    if recipe.cookable:
        description.append("This recipe can be cooked to improve its effect.")

    lines.append(" ".join(description))
    lines.append("")

    # Sort ingredients into categories
    regular_ingredients = []
    cooked_ingredients = []
    canned_ingredients = []
    packaged_ingredients = []
    spices = []

    if recipe.items_list:
        for item_id, item_data in sorted(recipe.items_list.items()):
            item = item_data["item"]
            hunger = item_data["hunger"]
            cooked = item_data["cooked"]
            spice = item_data["spice"]

            # Get just the first icon filename and page name without formatting
            # Use get_icon with all_icons=False to get only the first icon
            icon_name = (
                item.get_icon(format=False, all_icons=False)
                .split("|")[0]
                .replace("[[File:", "")
                .strip()
            )
            page_name = item.page

            # Build the template with optional cooked parameter
            template_parts = [
                "{{Item list dropdown",
                f"icon={icon_name}",
                f"item={page_name}",
                f"hunger={hunger}",
            ]
            if cooked:
                template_parts.append("cooked=true")
            template_parts.append("}}")

            item_entry = "|".join(template_parts)

            # Categorize the ingredient
            if spice:
                spices.append(item_entry)
            elif item.get("cannedfood", False):
                canned_ingredients.append(item_entry)
            elif item.get("packaged", False):
                packaged_ingredients.append(item_entry)
            elif cooked:
                cooked_ingredients.append(item_entry)
            else:
                regular_ingredients.append(item_entry)

    # Add Regular Ingredients
    if regular_ingredients:
        lines.append("=====Regular=====")
        lines.extend(regular_ingredients)
        lines.append("")

    # Add Canned Ingredients
    if canned_ingredients:
        lines.append("=====Canned=====")
        lines.extend(canned_ingredients)
        lines.append("")

    # Add Packaged Ingredients
    if packaged_ingredients:
        lines.append("=====Packaged=====")
        lines.extend(packaged_ingredients)
        lines.append("")

    # Add Ingredients that Require Cooking
    if cooked_ingredients:
        lines.append("=====Requires cooking=====")
        lines.extend(cooked_ingredients)
        lines.append("")

    # Add Spices
    if spices:
        lines.append("=====Condiments & spices=====")
        lines.extend(spices)
        lines.append("")

    return lines


def format_recipe_template(item, evolved_recipe):
    """
    Format evolved recipe template information for an item.

    Args:
        item (Item): The item object to format
        evolved_recipe (dict): The evolved recipe data for the item

    Returns:
        list: Formatted lines for the wiki template
    """
    content = ["{{EvolvedRecipesForItem", f"|id={item.item_id}"]

    if item.spice:
        content.append("|spice=true")

    for recipe, value in evolved_recipe.items():
        count, cooked = value
        param = recipe.lower() if not cooked else f"{recipe.lower()}cooked"
        content.append(f"|{param}={count}")

    content.append("}}")
    return content


def main(batch: bool = False):
    """
    Main execution function for evolved recipes article generation.

    Args:
        batch (bool): If True, skip language initialization

    This function:
    1. Loads all evolved recipes
    2. For each recipe with a result item:
       - Formats the recipe information in wiki article format
       - Creates a file named after the result item's ID
       - Writes the formatted content to the output directory
    3. For each item with evolved recipe properties:
       - Formats the recipe template information
       - Creates a file named after the item's ID
       - Writes the formatted content to the template directory
    """
    if not batch:
        Language.get()
    recipes = EvolvedRecipe.all()

    if not recipes:
        echo.warning("No evolved recipes found!")
        return

    echo.info(f"Found {len(recipes)} evolved recipes")

    # Process recipes for ingredient articles
    for recipe_id, recipe in tqdm(
        recipes.items(),
        desc="Processing Recipe Ingredients",
        bar_format=PBAR_FORMAT,
        unit=" recipes",
    ):
        if not recipe.valid or not recipe.result_item:
            continue

        content = format_recipe_info(recipe)
        output_file = f"{recipe.result_item.item_id}.txt"
        write_file(
            content, rel_path=output_file, root_path=INGREDIENTS_DIR, suppress=True
        )

    echo.success(f"Evolved recipe articles written to '{INGREDIENTS_DIR}'")

    # Process items for template generation
    for item_id, item in tqdm(
        Item.all().items(),
        desc="Processing Recipe Templates",
        bar_format=PBAR_FORMAT,
        unit=" items",
    ):
        evolved_recipe = item.evolved_recipe
        if not evolved_recipe:
            continue

        content = format_recipe_template(item, evolved_recipe)
        output_file = f"{item_id}.txt"
        write_file(content, rel_path=output_file, root_path=TEMPLATE_DIR, suppress=True)

    echo.success(f"Evolved recipe templates written to '{TEMPLATE_DIR}'")
