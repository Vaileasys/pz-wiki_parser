#!/usr/bin/env python3
"""
Project Zomboid Wiki Evolved Recipes Information Display

This script displays comprehensive information about evolved recipes in Project Zomboid.
It uses the EvolvedRecipe object to show detailed information about each recipe including
properties, compatible items, and recipe mechanics.

The script displays:
- Basic recipe information (name, ID, script type)
- Recipe properties (cookable, hidden, max items, etc.)
- Result and base items
- Compatible ingredients with their properties
- Recipe mechanics and settings
"""

import os
from tqdm import tqdm
from scripts.core.constants import ITEM_DIR, PBAR_FORMAT
from scripts.core.file_loading import write_file
from scripts.objects.evolved_recipe import EvolvedRecipe
from scripts.utils import echo

ROOT_DIR = os.path.join(ITEM_DIR, "evolved_recipes_info")


def format_recipe_info(recipe):
    """
    Format detailed information about an evolved recipe.

    Args:
        recipe (EvolvedRecipe): The evolved recipe object to format

    Returns:
        list: Formatted lines of information about the recipe
    """
    lines = []

    # Basic Information
    lines.append(f"=== {recipe.name} ({recipe.recipe_id}) ===")
    lines.append(f"Script Type: {recipe.script_type}")
    lines.append(f"Valid: {recipe.valid}")
    lines.append(f"Hidden: {recipe.hidden}")
    lines.append("")

    # Recipe Properties
    lines.append("**Recipe Properties:**")
    lines.append(f"- Max Items: {recipe.max_items}")
    lines.append(f"- Cookable: {recipe.cookable}")
    lines.append(f"- Add Ingredient If Cooked: {recipe.add_ingredient_if_cooked}")
    lines.append(f"- Can Add Spices Empty: {recipe.can_add_spices_empty}")
    lines.append(f"- Allow Frozen: {recipe.allow_frozen}")
    lines.append(f"- Minimum Water: {recipe.minimum_water}")
    lines.append("")

    # Items
    if recipe.result_item:
        lines.append(
            f"**Result Item:** {recipe.result_item.name} ({recipe.result_item.item_id})"
        )
    else:
        lines.append(f"**Result Item:** {recipe.get('ResultItem', 'None')}")

    if recipe.base_item:
        lines.append(
            f"**Base Item:** {recipe.base_item.name} ({recipe.base_item.item_id})"
        )
    else:
        lines.append(f"**Base Item:** {recipe.get('BaseItem', 'None')}")
    lines.append("")

    # Template and Sound
    if recipe.template:
        lines.append(f"**Template:** {recipe.template}")
    if recipe.add_sound:
        lines.append(f"**Add Sound:** {recipe.add_sound}")
    lines.append("")

    # Compatible Items
    if recipe.items_list:
        lines.append("**Compatible Items:**")
        for item_id, item_data in recipe.items_list.items():
            item = item_data["item"]
            hunger = item_data["hunger"]
            cooked = item_data["cooked"]
            spice = item_data["spice"]

            status = []
            if cooked:
                status.append("cooked only")
            if spice:
                status.append("spice")

            status_str = f" ({', '.join(status)})" if status else ""
            lines.append(f"- {item.name} ({item_id}) - Hunger: {hunger}{status_str}")
    else:
        lines.append("**Compatible Items:** None found")
    lines.append("")

    # Raw Data (for debugging)
    lines.append("**Raw Data:**")
    for key, value in recipe.data.items():
        lines.append(f"- {key}: {value}")
    lines.append("")

    return lines


def main():
    """
    Main execution function for evolved recipes information display.

    This function:
    1. Loads all evolved recipes
    2. Formats detailed information for each recipe
    3. Creates output files with comprehensive recipe data
    4. Provides both individual files and a summary

    The output includes:
    - Individual files for each recipe with detailed information
    - A summary file listing all recipes
    - Statistics about recipe types and properties
    """
    recipes = EvolvedRecipe.all()

    if not recipes:
        echo.warning("No evolved recipes found!")
        return

    echo.info(f"Found {len(recipes)} evolved recipes")

    # Create summary content
    summary_lines = []
    summary_lines.append("= Evolved Recipes Summary =")
    summary_lines.append("")
    summary_lines.append(f"Total Recipes: {len(recipes)}")
    summary_lines.append("")

    # Statistics
    cookable_count = sum(1 for r in recipes.values() if r.cookable)
    hidden_count = sum(1 for r in recipes.values() if r.hidden)
    spice_count = sum(1 for r in recipes.values() if r.can_add_spices_empty)

    summary_lines.append("**Statistics:**")
    summary_lines.append(f"- Cookable Recipes: {cookable_count}")
    summary_lines.append(f"- Hidden Recipes: {hidden_count}")
    summary_lines.append(f"- Can Add Spices Empty: {spice_count}")
    summary_lines.append("")

    # Recipe list
    summary_lines.append("**All Recipes:**")
    for recipe_id, recipe in sorted(recipes.items()):
        summary_lines.append(f"- {recipe.name} ({recipe_id})")
    summary_lines.append("")

    # Write summary file
    summary_file = "evolved_recipes_summary.txt"
    write_file(summary_lines, rel_path=summary_file, root_path=ROOT_DIR, suppress=True)

    # Process individual recipes
    for recipe_id, recipe in tqdm(
        recipes.items(),
        desc="Processing Recipes",
        bar_format=PBAR_FORMAT,
        unit=" recipes",
    ):
        if not recipe.valid:
            continue

        content = format_recipe_info(recipe)
        output_file = f"{recipe_id}_info.txt"
        write_file(content, rel_path=output_file, root_path=ROOT_DIR, suppress=True)

    echo.success(f"Evolved recipe information written to '{ROOT_DIR}'")
    echo.info(f"Summary file: {os.path.join(ROOT_DIR, summary_file)}")


if __name__ == "__main__":
    from scripts.core.language import Language

    Language.set("en")
    main()
