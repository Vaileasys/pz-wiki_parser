"""
Item Merger Script
Finds items that share the same name but have separate pages in the wiki.
"""

import json
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

from scripts.objects.item import Item
from scripts.core.constants import PBAR_FORMAT
from scripts.utils import echo


def find_items_with_shared_names():
    """
    Find items that share the same display name but have separate wiki pages.

    Returns:
        dict: Mapping of display names to lists of items with that name and different pages
    """
    # Build a mapping of item names to items with that name
    name_to_items = defaultdict(list)

    echo.info("Analyzing items...")
    total_items = Item.count()

    with tqdm(
        total=total_items,
        desc="Processing items",
        bar_format=PBAR_FORMAT,
        unit=" items",
    ) as pbar:
        for item in Item.values():
            if not item.valid:
                pbar.update(1)
                continue

            # Get the item's display name and page
            item_name = item.name
            item_page = item.page
            has_page = item.has_page

            # Store item information
            name_to_items[item_name].append(
                {
                    "item_id": item.item_id,
                    "id_type": item.id_type,
                    "page_name": item_page,
                    "has_page": has_page,
                    "categories": item.item_categories,
                }
            )

            pbar.update(1)

    # Filter to only include names where items have different pages
    shared_name_items = {}
    for item_name, items in name_to_items.items():
        # Check if there are multiple different pages for this name
        unique_pages = set(item_info["page_name"] for item_info in items)

        # Only include if there are multiple unique pages
        if len(unique_pages) > 1:
            shared_name_items[item_name] = items

    return shared_name_items


def create_merge_list():
    """Main function to create the merge list JSON."""
    echo.info("Finding items with shared names but separate pages...")
    shared_items = find_items_with_shared_names()

    # Prepare output structure
    output = {
        "items": {},
    }

    # Add each shared name group to the output
    for item_name, items in sorted(shared_items.items()):
        output["items"][item_name] = {"items": items}

    # Write to output file
    output_path = Path(__file__).parent.parent.parent / "output" / "merge_list.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

def main():
    """Main entry point for the item merger script."""
    create_merge_list()
    echo.info("Item merger completed.")


if __name__ == "__main__":
    main()
