#!/usr/bin/env python3
"""
Project Zomboid Wiki Research Recipes Generator

This script processes items in Project Zomboid that can be researched to learn new
recipes. It generates wiki markup showing which recipes can be learned by researching
each item, using the Crafting/sandbox template for proper formatting.

The script handles:
- Parsing item data for researchable recipes (from item's ResearchableRecipes property)
- Finding recipes where the item is a product (product-based research)
- Combining all researchable recipes into a single unified list
- Generating formatted wiki markup with recipe lists
- Creating output in both research and crafting directories
- Proper template formatting for wiki integration
- Expanding meta recipes into their component recipes
"""

import os
from collections import defaultdict
from tqdm import tqdm
from scripts.objects.item import Item
from scripts.objects.craft_recipe import CraftRecipe
from scripts.parser import metarecipe_parser
from scripts.core import page_manager
from scripts.core.language import Language
from scripts.utils import echo


def find_recipes_producing_item(item_id: str) -> list[str]:
    """
    Find all recipes that produce the given item as an output.

    Args:
        item_id (str): The item ID to search for

    Returns:
        list[str]: List of recipe IDs that produce this item
    """
    producing_recipes = []

    for recipe_id, recipe_obj in CraftRecipe.all().items():
        if item_id in recipe_obj.output_items:
            # Include any recipe that has learnable requirements
            has_skill_requirements = bool(recipe_obj.skill_required)
            has_auto_learn = bool(
                recipe_obj.auto_learn_all or recipe_obj.auto_learn_any
            )

            # If the recipe has any form of skill/learning requirements, it can be researched
            if has_skill_requirements or has_auto_learn:
                producing_recipes.append(recipe_id)

    return producing_recipes


def main(batch: bool = False):
    """
    Main execution function for research recipes generation.

    Args:
        batch (bool): If True, skip language initialization

    This function:
    1. Loads parsed item data
    2. Identifies items with researchable recipes (traditional and product-based)
    3. Combines all researchable recipes into a single unified list per item
    4. Generates wiki markup using Crafting/sandbox template
    5. Creates output files organized by individual IDs and by wiki pages
    6. Handles proper formatting for wiki integration
    7. Expands meta recipes into their component recipes

    The output is saved in multiple locations:
    - output/recipes/researchrecipes/id/ (individual item files)
    - output/recipes/researchrecipes/page/ (page-combined files)
    - output/recipes/crafting/id/ (individual item files)
    - output/recipes/crafting/page/ (page-combined files)
    """
    if not batch:
        Language.get()
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

    # Build a mapping of item_id to all item_ids on the same page(s)
    # This allows us to merge recipes for items that share a page
    item_to_page_items = {}  # item_id -> set of all item_ids (including itself) on same page(s)

    # First pass: collect all items and organize by pages
    items_with_research = {}
    for item_id, item in tqdm(Item.all().items(), desc="Collecting research recipes"):
        all_research_data = []  # List of (recipe_id, research_level, source_type)

        # Get recipes from item's researchable_recipes property
        researchable_recipes = item.researchable_recipes
        if researchable_recipes:
            # Ensure researchable_recipes is always a list
            if not isinstance(researchable_recipes, list):
                researchable_recipes = [researchable_recipes]

            # Expand meta recipes
            expanded_recipes = metarecipe_parser.expand_recipe_list(
                researchable_recipes
            )

            # Add research data for each recipe
            for recipe_id in expanded_recipes:
                try:
                    recipe_obj = CraftRecipe(recipe_id)
                    all_research_data.append((recipe_id, 0, "research_item"))
                except Exception as e:
                    echo.warning(
                        f"Error processing recipe {recipe_id} for item {item_id}: {e}"
                    )
                    all_research_data.append((recipe_id, -1, "research_item"))

        # Get recipes where this item is a product
        producing_recipes = find_recipes_producing_item(item_id)
        for recipe_id in producing_recipes:
            try:
                recipe_obj = CraftRecipe(recipe_id)
                all_research_data.append((recipe_id, 0, "product_item"))
            except Exception as e:
                echo.warning(
                    f"Error processing producing recipe {recipe_id} for item {item_id}: {e}"
                )
                all_research_data.append((recipe_id, -1, "product_item"))

        # Only include items that have research data
        if all_research_data:
            items_with_research[item_id] = all_research_data

            # Find pages for this item
            pages = page_manager.get_pages(item_id, "item_id")
            if pages:
                for page in pages:
                    page_recipes[page].append((item_id, all_research_data))
            else:
                # If no page found, create a fallback page name
                page_recipes[f"Unknown_Items"].append((item_id, all_research_data))

    # Build item_to_page_items mapping after collecting all items
    for iid in items_with_research.keys():
        pages = page_manager.get_pages(iid, "item_id")
        if pages:
            # Get all item IDs from all pages this item appears on
            related_items = set()
            for page in pages:
                page_ids = page_manager.get_ids(page, "item_id")
                if page_ids:
                    related_items.update(page_ids)
            item_to_page_items[iid] = related_items
        else:
            # If no page found, just use the item itself
            item_to_page_items[iid] = {iid}

    # Second pass: generate individual files
    for item_id, research_data in tqdm(
        items_with_research.items(), desc="Generating individual files"
    ):
        # Collect all recipes into a single set to avoid duplicates
        all_recipes = set()

        # Add recipes from this item
        for recipe_id, research_level, source_type in research_data:
            all_recipes.add(recipe_id)

        # Merge recipes from all items on the same page(s)
        related_items = item_to_page_items.get(item_id, {item_id})
        for related_id in related_items:
            if related_id != item_id and related_id in items_with_research:
                related_data = items_with_research[related_id]
                for recipe_id, research_level, source_type in related_data:
                    all_recipes.add(recipe_id)

        lines = []

        # Add single research recipes section
        if all_recipes:
            lines.append(
                f"{{{{Crafting/sandbox|header=Research recipes|id={item_id}_research"
            )
            for recipe_id in sorted(all_recipes):
                lines.append(f"|{recipe_id}")
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

        for item_id, research_data in page_items:
            page_item_ids.append(item_id)
            for recipe_id, research_level, source_type in research_data:
                all_recipes.add(recipe_id)

        lines = []

        # Add single research recipes section
        if all_recipes:
            lines.append(
                f"{{{{Crafting/sandbox|header=Research recipes|id={page_name}_research"
            )
            for recipe_id in sorted(all_recipes):
                lines.append(f"|{recipe_id}")
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

    # Count statistics
    total_recipes = 0
    unique_recipes = set()

    for research_data in items_with_research.values():
        for recipe_id, research_level, source_type in research_data:
            total_recipes += 1
            unique_recipes.add(recipe_id)

    echo.success(
        f"Research recipes written - {len(items_with_research)} individual items, {len(page_recipes)} pages\n"
        f"  {total_recipes} total recipe entries"
    )
