[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_container_contents.md) | [Next File](item_fixing.md) | [Next Folder](groups/ammo_groups.md) | [Back to Index](../../index.md)

# item_distribution.py

## Functions

### [`load_item_dictionary(item_name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L21)

Load and search for a modified item name based on a dictionary in itemname_en.txt.

### [`process_json(file_paths)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L61)

Process JSON files and gather a list of unique items and their counts.

### [`build_item_json(item_list, procedural_data, distribution_data, vehicle_data, foraging_data, clothing_data, stories_data, fishing_data, butchering_data, attached_weapons_data, container_contents_data, outfits_data = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L256)

### [`merge_case_insensitive_duplicates(items_dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L1152)

Merge items that have the same ID but different capitalization.

This prevents issues where items like "Bag_Schoolbag" and "Bag_SchoolBag"
are treated as separate items, causing later overwrites and split index entries.

<ins>**Args:**</ins>
  - **items_dict (dict)**:
      - _Dictionary of item_id -> item_data_

<ins>**Returns:**</ins>
  - **dict**:
      - _Deduplicated dictionary with merged data_

### [`build_tables(category_items, index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L1400)

Build Lua tables from pre-categorized item data, organizing items by category.
Split files that would exceed 2500 lines into multiple numbered files.

<ins>**Args:**</ins>
  - **category_items (dict)**:
      - _Dictionary of items organized by category_
  - **index (dict)**:
      - _Dictionary of item IDs organized by category_
  - **Output files to data_files directory with category-based filenames.**:

### [`calculate_missing_items(itemname_path, itemlist_path, missing_items_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L1911)

Calculate items that exist in itemname_en.txt but not in the processed item list.

### [`combine_items_by_page(all_items)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L1933)

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
  - **dict**:
      - _Updated dictionary with combined items_

### [`extract_raw_outfit_id(outfit_name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L2260)

Extract the raw outfit ID by removing gender suffixes.

<ins>**Args:**</ins>
  - **outfit_name (str)**:
      - _Outfit name like "Armor Test Kelly Gang (male)"_

<ins>**Returns:**</ins>
  - **str**:
      - _Raw outfit ID like "ArmorTestKellyGang"_

### [`get_outfit_link(outfit_id, outfits_data = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L2279)

Convert an outfit ID to a wiki link using the page dictionary.

<ins>**Args:**</ins>
  - **outfit_id**:
      - _The outfit identifier (e.g., "ArmyInstructor")_
  - **outfits_data**:
      - _Optional dictionary containing outfit data (no longer used for linking)_

<ins>**Returns:**</ins>
  - **A wiki link to the outfit page if found in page dictionary, otherwise the raw ID**:

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_distribution.py#L2308)

Main function to process and generate distribution data files.

This function:
1. Checks if decompiler has run successfully
2. Parses distribution data from various sources
3. Processes items and builds JSON data
4. Combines items that share the same wiki page
5. Categorizes items by type
6. Generates Lua data files by category
7. Creates an index file

<ins>**Returns:**</ins>
  - **bool**:
      - _True if processing completed successfully, False otherwise_


[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_container_contents.md) | [Next File](item_fixing.md) | [Next Folder](groups/ammo_groups.md) | [Back to Index](../../index.md)
