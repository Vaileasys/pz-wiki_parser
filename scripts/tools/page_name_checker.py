"""
Page name checker tool.

Compares item page names with their actual item names and outputs differences to JSON.
This helps identify items where the wiki page name doesn't match the in-game item name.
"""

import os
from tqdm import tqdm
from scripts.core import page_manager, constants
from scripts.core.file_loading import save_json
from scripts.objects.item import Item
from scripts.utils import echo


def get_output_path():
    """Get the output file path for the page name checker results."""
    return os.path.join(constants.OUTPUT_DIR, "page_name_differences.json")


def check_page_names():
    """
    Check all items for differences between page names and item names.
    
    For pages with multiple item IDs: if the first item's name matches the page name,
    all items from that page are excluded from results.
    
    Returns:
        dict: Dictionary with item IDs as keys and page_name/item_name as values.
    """
    page_manager.init()
    
    # Get the flattened page dictionary (page -> data)
    page_dict = page_manager.get_flattened_page_dict()
    echo.info(f"Found {len(page_dict)} pages to check")
    
    # First pass: identify pages to skip (multi-item pages where first item matches page name)
    pages_to_skip = set()
    echo.info("Identifying pages to skip...")
    
    for page_name, page_data in page_dict.items():
        item_ids = page_data.get("item_id", [])
        
        if len(item_ids) > 1:
            # Get the first item's name
            first_item_id = item_ids[0]
            try:
                first_item = Item(first_item_id)
                first_item_name = first_item.name
                
                # If first item's name matches page name, skip this entire page
                if first_item_name == page_name:
                    pages_to_skip.add(page_name)
            except Exception:
                continue
    
    if pages_to_skip:
        echo.info(f"Skipping {len(pages_to_skip)} pages where first item matches page name")
    
    # Get all item IDs
    item_ids = list(Item.keys())
    
    differences = {}
    items_without_pages = []
    
    # Second pass: check each item
    with tqdm(
        total=len(item_ids),
        desc="Checking page names",
        unit=" items",
        bar_format=constants.PBAR_FORMAT
    ) as pbar:
        for item_id in item_ids:
            pbar.set_postfix_str(f"{item_id[:50]}{'...' if len(item_id) > 50 else ''}")
            
            # Get page name
            pages = page_manager.get_pages(item_id, id_type="item_id")
            
            if not pages:
                items_without_pages.append(item_id)
                pbar.update(1)
                continue
            page_name = pages[0]
            
            # Skip if this page is in the skip list
            if page_name in pages_to_skip:
                pbar.update(1)
                continue
            
            # Get item name
            try:
                item = Item(item_id)
                item_name = item.name
            except Exception:
                pbar.update(1)
                continue
            
            # Compare page name and item name
            if page_name != item_name:
                differences[item_id] = {
                    "page_name": page_name,
                    "item_name": item_name
                }
            
            pbar.update(1)
    
    echo.success(f"Found {len(differences)} items with differing page/item names")
    
    if items_without_pages:
        echo.warning(f"{len(items_without_pages)} items have no associated page")
    
    return differences


def main():
    """
    Entry point for the page name checker tool.
    
    Checks all items for differences between their wiki page names and in-game item names,
    then outputs the results to a JSON file.
    """
    differences = check_page_names()
    output_path = get_output_path()
    save_json(output_path, differences)
    
    echo.write("")
    echo.success(f"Results saved to: {output_path}")
    echo.info(f"Total differences found: {len(differences)}")


if __name__ == "__main__":
    main()