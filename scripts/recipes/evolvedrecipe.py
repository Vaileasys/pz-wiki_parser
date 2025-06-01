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
from scripts.parser import item_parser


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
    parsed_item_data = item_parser.get_item_data()
    output_dir = os.path.join("output", "evolved_recipes")
    os.makedirs(output_dir, exist_ok=True)

    for item_id, item_data in tqdm(parsed_item_data.items(), desc="Processing Items"):
        evolved_recipe = item_data.get("EvolvedRecipe", {})
        if not evolved_recipe:
            continue
        lines = ["{{EvolvedRecipesForItem", f"|id={item_id}"]

        if item_data.get("Spice") == "TRUE" or item_data.get("Spice") == "true":
            lines.append("|spice=true")

        for key, value in evolved_recipe.items():
            if isinstance(value, list):
                value = '|'.join(value)
            if isinstance(value, str) and value.endswith('|Cooked'):
                value = value[:-len('|Cooked')]
            lines.append(f"|{key.lower()}={value}")

        lines.append("}}")
        output_content = "\n".join(lines)

        output_file_path = os.path.join(output_dir, f"{item_id}.txt")
        try:
            with open(output_file_path, "w") as f:
                f.write(output_content)
        except Exception as e:
            tqdm.write(f"Error writing file for {item_id}: {e}")


if __name__ == '__main__':
    main()
