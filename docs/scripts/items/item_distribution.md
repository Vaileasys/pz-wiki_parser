[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_container_contents.md) | [Next File](item_fixing.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)

# item_distribution.py

## Functions

### [`load_item_dictionary(item_name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L18)

Load and search for a modified item name based on a dictionary in itemname_en.txt.

### [`process_json(file_paths)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L56)

Process JSON files and gather a list of unique items and their counts.

### [`build_item_json(item_list, procedural_data, distribution_data, vehicle_data, foraging_data, attached_weapons_data, clothing_data, stories_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L142)
### [`build_tables(category_items, index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L507)

Build Lua tables from pre-categorized item data, organizing items by category.

Split files that would exceed 2500 lines into multiple numbered files.

<ins>**Args:**</ins>
  - **category_items (dict)**:
      - _Dictionary of items organized by category_
  - **index (dict)**:
      - _Dictionary of item IDs organized by category_
      - _Output files to data_files directory with category-based filenames._

### [`calculate_missing_items(itemname_path, itemlist_path, missing_items_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L782)

Calculate items that exist in itemname_en.txt but not in the processed item list.

### [`combine_items_by_page(all_items)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L804)

Combines distribution data for items that share the same wiki page.

This function:
1. Uses page_manager to get the official page-to-item mappings
2. For each page, combines all secondary item data into the primary item's data
3. Removes duplicate entries in container, vehicle, and other lists
4. Returns a new dictionary with combined items

<ins>**Args:**</ins>
  - **all_items (dict)**:
      - _Dictionary of all items with their distribution data_

<ins>**Returns:**</ins>
  - **dict:**
      - Updated dictionary with combined items

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L1049)

Main function to process and generate distribution data files.

This function:
1. Parses distribution data from various sources
2. Processes items and builds JSON data
3. Combines items that share the same wiki page
4. Categorizes items by type
5. Generates Lua data files by category
6. Creates an index file



[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_container_contents.md) | [Next File](item_fixing.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)
