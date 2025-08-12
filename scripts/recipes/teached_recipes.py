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
from collections import defaultdict
from tqdm import tqdm
from scripts.objects.item import Item
from scripts.objects.craft_recipe import CraftRecipe
from scripts.parser import metarecipe_parser
from scripts.core.file_loading import write_file
from scripts.core.constants import OUTPUT_DIR, PBAR_FORMAT
from scripts.core import page_manager
from scripts.utils import echo


def main():
    """
    Main execution function for taught recipes generation.

    This function:
    1. Loads parsed item data
    2. Identifies items that teach recipes
    3. Generates wiki markup for each teaching item
    4. Creates files organized by individual IDs and by wiki pages
    5. Includes proper bot flags for wiki integration
    6. Expands meta recipes into their component recipes

    The output is saved in multiple locations:
    - output/recipes/teachedrecipes/id/ (individual item files)
    - output/recipes/teachedrecipes/page/ (page-combined files)
    """
    # Initialize page manager
    page_manager.init()

    # Load meta recipe data for expansion
    metarecipe_data = metarecipe_parser.get_metarecipe_data()

    # Create directory structure
    teached_id_dir = os.path.join(OUTPUT_DIR, "recipes", "teachedrecipes", "id")
    teached_page_dir = os.path.join(OUTPUT_DIR, "recipes", "teachedrecipes", "page")

    for dir_path in [teached_id_dir, teached_page_dir]:
        os.makedirs(dir_path, exist_ok=True)

    # Collect data for pages
    page_recipes = defaultdict(list)  # page_name -> list of (item_id, expanded_recipes)

    # First pass: collect all items and organize by pages
    items_with_taught = {}
    for item_id, item in tqdm(
        Item.all().items(),
        desc="Collecting teached recipes",
        bar_format=PBAR_FORMAT,
        leave=False,
    ):
        teached_recipes = item.teached_recipes
        if not teached_recipes:
            continue

        # Ensure teached_recipes is always a list
        if not isinstance(teached_recipes, list):
            teached_recipes = [teached_recipes]

        # Expand meta recipes
        expanded_recipes = metarecipe_parser.expand_recipe_list(teached_recipes)
        items_with_taught[item_id] = expanded_recipes

        # Find pages for this item
        pages = page_manager.get_pages(item_id, "item_id")
        if pages:
            for page in pages:
                page_recipes[page].append((item_id, expanded_recipes))
        else:
            pass

    # Second pass: generate individual files
    for item_id, expanded_recipes in tqdm(
        items_with_taught.items(),
        desc="Generating individual files",
        bar_format=PBAR_FORMAT,
        leave=False,
    ):
        content = [
            f"<!-- Bot flag|TeachedRecipes|id={item_id} -->",  # TODO: change to 'BOT_FLAG' constant
            "Reading this item will teach the following recipes:",
        ]

        for recipe in expanded_recipes:
            recipe_link = CraftRecipe(recipe).wiki_link
            content.append(f"*{recipe_link}")

        content.append(
            f"<!-- Bot flag end|TeachedRecipes|id={item_id} -->"
        )  # TODO: change to 'BOT_FLAG_END' constant

        teached_file = f"{item_id}_Teached.txt"

        try:
            write_file(
                content, rel_path=teached_file, root_path=teached_id_dir, suppress=True
            )
        except Exception as e:
            echo.error(f"Error writing individual file for {item_id}: {e}")

    # Third pass: generate page-combined files
    for page_name, page_items in tqdm(
        page_recipes.items(),
        desc="Generating page files",
        bar_format=PBAR_FORMAT,
        leave=False,
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
        content = [
            f"<!-- Bot flag|TeachedRecipes|id={page_name} -->",  # TODO: change to 'BOT_FLAG' constant
            "Reading items on this page will teach the following recipes:",
        ]

        for recipe in sorted(all_recipes):
            recipe_link = CraftRecipe(recipe).wiki_link
            content.append(f"*{recipe_link}")

        content.append(
            f"<!-- Bot flag end|TeachedRecipes|id={page_name} -->"
        )  # TODO: change to 'BOT_FLAG_END' constant

        teached_page_file = f"{page_name}_Teached.txt"

        try:
            write_file(
                content,
                rel_path=teached_page_file,
                root_path=teached_page_dir,
                suppress=True,
            )
        except Exception as e:
            echo.error(f"Error writing page file for {page_name}: {e}")

    echo.success(
        f"Teached recipes written - {len(items_with_taught)} individual items, {len(page_recipes)} pages"
    )
