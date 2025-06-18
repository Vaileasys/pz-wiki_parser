#!/usr/bin/env python3
"""
Project Zomboid Wiki Evolved Recipes Generator

This script processes items in Project Zomboid that are part of evolved recipes
(recipes that can change or improve over time, like food combinations). It generates
wiki markup using the EvolvedRecipesForItem template to document these recipes.

The script handles:
- Parsing item data for evolved recipe properties
- Processing spice attributes for recipes
- Formatting recipe combinations and variations
- Generating MediaWiki template markup
- Special handling for cooked food variants
"""

import os
from tqdm import tqdm
from scripts.core.constants import ITEM_DIR, PBAR_FORMAT
from scripts.core.file_loading import write_file
from scripts.objects.item import Item
from scripts.utils import echo

ROOT_DIR = os.path.join(ITEM_DIR, "evolved_recipes")

def main():
    """
    Main execution function for evolved recipes generation.

    This function:
    1. Loads parsed item data
    2. Identifies items with evolved recipe properties
    3. Processes special attributes like spices
    4. Formats recipe data for wiki template
    5. Creates output files with proper template markup

    The output is saved in the 'output/evolved_recipes' directory,
    with one file per item that has evolved recipe properties.
    Special handling is included for:
    - Spice attributes
    - List-type recipe values
    - Cooked food variants
    """
    for item_id, item in tqdm(Item.all().items(), desc="Processing Items", bar_format=PBAR_FORMAT, unit=" items"):
        evolved_recipe = item.evolved_recipe
        if not evolved_recipe:
            continue
        content = ["{{EvolvedRecipesForItem", f"|id={item_id}"]

        if item.spice:
            content.append("|spice=true")

        for recipe, value in evolved_recipe.items():
            count, cooked = value
            param = recipe.lower() if not cooked else f"{recipe.lower()}cooked"
            content.append(f"|{param}={count}")

        content.append("}}")

        output_file = f"{item_id}.txt"
        output_dir = write_file(content, rel_path=output_file, root_path=ROOT_DIR, suppress=True)

    echo.success(f"Evolved recipe files written to '{output_dir}'")


if __name__ == '__main__':
    from scripts.core.language import Language
    Language.set("en")
    main()
