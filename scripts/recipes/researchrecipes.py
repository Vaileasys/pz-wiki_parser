#!/usr/bin/env python3
"""
Project Zomboid Wiki Research Recipes Generator

This script processes items in Project Zomboid that can be researched to learn new
recipes. It generates wiki markup showing which recipes can be learned by researching
each item, using the Crafting/sandbox template for proper formatting.

The script handles:
- Parsing item data for researchable recipes
- Generating formatted wiki markup with recipe lists
- Creating output in both research and crafting directories
- Proper template formatting for wiki integration
- Expanding meta recipes into their component recipes
"""

import os
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.parser import metarecipe_parser
from scripts.utils import echo

def main():
    """
    Main execution function for research recipes generation.

    This function:
    1. Loads parsed item data
    2. Identifies items with researchable recipes
    3. Generates wiki markup using Crafting/sandbox template
    4. Creates output files in both research and crafting directories
    5. Handles proper formatting for wiki integration
    6. Expands meta recipes into their component recipes

    The output is saved in two locations:
    - output/recipes/researchrecipes/
    - output/recipes/crafting/
    Each containing one file per researchable item.
    """
    parsed_item_data = item_parser.get_item_data()
    # Load meta recipe data for expansion
    metarecipe_data = metarecipe_parser.get_metarecipe_data()

    research_dir = os.path.join("output", "recipes", "researchrecipes")
    crafting_dir = os.path.join("output", "recipes", "crafting")
    os.makedirs(research_dir, exist_ok=True)
    os.makedirs(crafting_dir, exist_ok=True)

    for item_id, item_data in tqdm(parsed_item_data.items(), desc="Processing research recipes"):
        researchable_recipes = item_data.get("ResearchableRecipes")
        if not researchable_recipes:
            continue

        # Ensure researchable_recipes is always a list.
        if not isinstance(researchable_recipes, list):
            researchable_recipes = [researchable_recipes]
            
        # Expand meta recipes
        expanded_recipes = metarecipe_parser.expand_recipe_list(researchable_recipes)

        lines = [
            "The following recipes can be learned by researching this item:",
            "",
            f"{{{{Crafting/sandbox|header=Research recipes|id={item_id}_research"
        ]
        for recipe in expanded_recipes:
            lines.append(f"|{recipe}")
        lines.append("}}")

        output_content = "\n".join(lines)

        research_file_path = os.path.join(research_dir, f"{item_id}_research.txt")
        crafting_file_path = os.path.join(crafting_dir, f"{item_id}_research.txt")

        try:
            with open(research_file_path, "w") as f:
                f.write(output_content)
            with open(crafting_file_path, "w") as f:
                f.write(output_content)
        except Exception as e:
            echo.error(f"Error writing file for {item_id}: {e}")


if __name__ == '__main__':
    main()
