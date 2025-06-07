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
from scripts.parser import item_parser
from scripts.parser import metarecipe_parser
from scripts.utils.utility import get_recipe
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
    parsed_item_data = item_parser.get_item_data()
    # Load meta recipe data for expansion
    metarecipe_data = metarecipe_parser.get_metarecipe_data()
    
    teached_dir = os.path.join("output", "recipes", "teachedrecipes")
    os.makedirs(teached_dir, exist_ok=True)

    for item_id, item_data in tqdm(parsed_item_data.items(), desc="Processing teached recipes"):
        teached_recipes = item_data.get("TeachedRecipes")
        if not teached_recipes:
            continue

        # Ensure teached_recipes is always a list.
        if not isinstance(teached_recipes, list):
            teached_recipes = [teached_recipes]
            
        # Expand meta recipes
        expanded_recipes = metarecipe_parser.expand_recipe_list(teached_recipes)

        lines = [
            f"<!-- Bot flag|TeachedRecipes|id={item_id} -->\nReading this item will teach the following recipes:"
        ]

        for recipe in expanded_recipes:
            recipe_link = get_recipe(recipe)
            lines.append(f"*{recipe_link}")

        output_content = "\n".join(lines) + f"\n<!-- Bot flag end|TeachedRecipes|id={item_id} -->"
        teached_file_path = os.path.join(teached_dir, f"{item_id}_Teached.txt")

        try:
            with open(teached_file_path, "w") as f:
                f.write(output_content)
        except Exception as e:
            tqdm.write(f"Error writing file for {item_id}: {e}")


if __name__ == '__main__':
    main()
