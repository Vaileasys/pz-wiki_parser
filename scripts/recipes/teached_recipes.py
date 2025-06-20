#!/usr/bin/env python3
"""
Project Zomboid Wiki Taught Recipes Generator

This script processes items in Project Zomboid that teach recipes (like recipe books
or VHS tapes) and generates wiki markup showing which recipes each item teaches.
It creates individual files for each item that contains recipe teaching information.

The script handles:
- Parsing item data for recipe teaching properties
- Generating formatted wiki markup with recipe links
- Creating individual files for each teaching item
- Proper bot flag markup for wiki integration
- Expanding meta recipes into their component recipes
"""

import os
from tqdm import tqdm
from scripts.objects.item import Item
from scripts.objects.craft_recipe import CraftRecipe
from scripts.parser import metarecipe_parser
from scripts.core.file_loading import write_file
from scripts.core.constants import OUTPUT_DIR, PBAR_FORMAT
from scripts.utils import echo

def main():
    """
    Main execution function for taught recipes generation.

    This function:
    1. Loads parsed item data
    2. Identifies items that teach recipes
    3. Generates wiki markup for each teaching item
    4. Creates individual files with recipe lists
    5. Includes proper bot flags for wiki integration
    6. Expands meta recipes into their component recipes

    The output is saved in the 'output/recipes/teachedrecipes' directory,
    with one file per teaching item.
    """
    # Load meta recipe data for expansion
    metarecipe_data = metarecipe_parser.get_metarecipe_data()
    
    teached_dir = os.path.join(OUTPUT_DIR, "recipes", "teachedrecipes")

    for item_id, item in tqdm(Item.all().items(), desc="Processing teached recipes", bar_format=PBAR_FORMAT, leave=False):
        teached_recipes = item.teached_recipes
        if not teached_recipes:
            continue

        # Ensure teached_recipes is always a list.
        if not isinstance(teached_recipes, list):
            teached_recipes = [teached_recipes]
            
        # Expand meta recipes
        expanded_recipes = metarecipe_parser.expand_recipe_list(teached_recipes)

        content = [
            f"<!-- Bot flag|TeachedRecipes|id={item_id} -->", #TODO: change to 'BOT_FLAG' constant
            "Reading this item will teach the following recipes:"
        ]

        for recipe in expanded_recipes:
            recipe_link = CraftRecipe(recipe).wiki_link
            content.append(f"*{recipe_link}")

        content.append(f"<!-- Bot flag end|TeachedRecipes|id={item_id} -->") #TODO: change to 'BOT_FLAG_END' constant
        teached_file = f"{item_id}_Teached.txt"

        output_file_path = write_file(content, rel_path=teached_file, root_path=teached_dir, suppress=True)
    
    echo.success(f"Teached recipes written to '{output_file_path}'")


if __name__ == '__main__':
    main()
