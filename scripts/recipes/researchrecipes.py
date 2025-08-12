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
from collections import defaultdict
from tqdm import tqdm
from scripts.objects.item import Item
from scripts.parser import metarecipe_parser
from scripts.core import page_manager
from scripts.utils import echo


def main():
    """
    Main execution function for research recipes generation.

    This function:
    1. Loads parsed item data
    2. Identifies items with researchable recipes
    3. Generates wiki markup using Crafting/sandbox template
    4. Creates output files organized by individual IDs and by wiki pages
    5. Handles proper formatting for wiki integration
    6. Expands meta recipes into their component recipes

    The output is saved in multiple locations:
    - output/recipes/researchrecipes/id/ (individual item files)
    - output/recipes/researchrecipes/page/ (page-combined files)
    - output/recipes/crafting/id/ (individual item files)
    - output/recipes/crafting/page/ (page-combined files)
    """
    # Initialize page manager
    page_manager.init()

    # Load meta recipe data for expansion
    metarecipe_data = metarecipe_parser.get_metarecipe_data()

    # Create directory structure
    research_id_dir = os.path.join("output", "recipes", "researchrecipes", "id")
    research_page_dir = os.path.join("output", "recipes", "researchrecipes", "page")
    crafting_id_dir = os.path.join("output", "recipes", "crafting", "id")
    crafting_page_dir = os.path.join("output", "recipes", "crafting", "page")

    for dir_path in [
        research_id_dir,
        research_page_dir,
        crafting_id_dir,
        crafting_page_dir,
    ]:
        os.makedirs(dir_path, exist_ok=True)

    # Collect data for pages
    page_recipes = defaultdict(list)  # page_name -> list of (item_id, expanded_recipes)

    # First pass: collect all items and organize by pages
    items_with_research = {}
    for item_id, item in tqdm(Item.all().items(), desc="Collecting research recipes"):
        researchable_recipes = item.researchable_recipes
        if not researchable_recipes:
            continue

        # Ensure researchable_recipes is always a list
        if not isinstance(researchable_recipes, list):
            researchable_recipes = [researchable_recipes]

        # Expand meta recipes
        expanded_recipes = metarecipe_parser.expand_recipe_list(researchable_recipes)
        items_with_research[item_id] = expanded_recipes

        # Find pages for this item
        pages = page_manager.get_pages(item_id, "item_id")
        if pages:
            for page in pages:
                page_recipes[page].append((item_id, expanded_recipes))
        else:
            # If no page found, create a fallback page name
            page_recipes[f"Unknown_Items"].append((item_id, expanded_recipes))

    # Second pass: generate individual files
    for item_id, expanded_recipes in tqdm(
        items_with_research.items(), desc="Generating individual files"
    ):
        lines = [
            "The following recipes can be learned by researching this item.",
            f"{{{{Crafting/sandbox|header=Research recipes|id={item_id}_research",
        ]
        for recipe in expanded_recipes:
            lines.append(f"|{recipe}")
        lines.append("}}")

        output_content = "\n".join(lines)

        # Write individual files
        research_file_path = os.path.join(research_id_dir, f"{item_id}_research.txt")
        crafting_file_path = os.path.join(crafting_id_dir, f"{item_id}_research.txt")

        try:
            with open(research_file_path, "w") as f:
                f.write(output_content)
            with open(crafting_file_path, "w") as f:
                f.write(output_content)
        except Exception as e:
            echo.error(f"Error writing individual file for {item_id}: {e}")

    # Third pass: generate page-combined files
    for page_name, page_items in tqdm(
        page_recipes.items(), desc="Generating page files"
    ):
        if not page_items:
            continue

        # Combine all recipes from items on this page
        all_recipes = set()
        page_item_ids = []

        for item_id, expanded_recipes in page_items:
            page_item_ids.append(item_id)
            all_recipes.update(expanded_recipes)

        # Generate combined content
        lines = [
            "The following recipes can be learned by researching items on this page.",
            f"{{{{Crafting/sandbox|header=Research recipes|id={page_name}_research",
        ]
        for recipe in sorted(all_recipes):
            lines.append(f"|{recipe}")
        lines.append("}}")

        output_content = "\n".join(lines)

        # Write page files
        research_page_path = os.path.join(
            research_page_dir, f"{page_name}_research.txt"
        )
        crafting_page_path = os.path.join(
            crafting_page_dir, f"{page_name}_research.txt"
        )

        try:
            with open(research_page_path, "w") as f:
                f.write(output_content)
            with open(crafting_page_path, "w") as f:
                f.write(output_content)
        except Exception as e:
            echo.error(f"Error writing page file for {page_name}: {e}")

    echo.success(
        f"Research recipes written - {len(items_with_research)} individual items, {len(page_recipes)} pages"
    )