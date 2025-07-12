[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_fixing.md) | [Next File](item_infobox_legacy.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)

# item_infobox.py

Item infobox generator.

This module processes `Item` objects into structured infobox parameters, formatted for wiki output.
It handles individual items, pages with multiple item IDs, and supports both combined and standalone infobox generation.

Main functions:
- Extract item attributes into infobox fields
- Merge multiple item definitions into unified infobox data, based on page
- Format and output infobox content as text files

## Functions

### [`generate_item_data(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L34)

Extracts relevant parameters from an Item object into a dictionary.


<ins>**Args:**</ins>
  - **item (Item)**:
      - _The item object to process._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary of infobox parameters for the given item.

### [`build_infobox(infobox_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L205)

Builds an infobox template from the provided parameters.


<ins>**Args:**</ins>
  - **infobox_data (dict)**:
      - _Dictionary of key-value infobox fields._

<ins>**Returns:**</ins>
  - **list[str]:**
      - A list of lines forming the infobox template.

### [`join_keys(params: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L223)

Converts list values of specific keys into <br>-joined strings.


<ins>**Args:**</ins>
  - **params (dict)**:
      - _Infobox parameters._

<ins>**Returns:**</ins>
  - **dict:**
      - Updated dictionary with joined string values for specified keys.

### [`merge_items(page_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L241)

Merges parameters across multiple item variants into a single infobox entry.


<ins>**Args:**</ins>
  - **page_data (dict)**:
      - _Mapping of item_id to parameter dictionaries._

<ins>**Returns:**</ins>
  - **dict:**
      - Merged and enumerated infobox-ready parameters.

### [`process_pages(pages: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L292)

Generates infoboxes for all items grouped by page name and writes output files.


<ins>**Args:**</ins>
  - **pages (dict)**:
      - _Mapping of page names to their item_id entries._

### [`process_items(item_id_list: list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L325)

Generates infoboxes for a list of specific item IDs and writes output files.


<ins>**Args:**</ins>
  - **item_id_list (list)**:
      - _List of item IDs to process._

### [`prepare_pages(item_id_list: list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L347)

Prepares and validates the item-to-page mappings for later infobox generation.


<ins>**Args:**</ins>
  - **item_id_list (list)**:
      - _List of item IDs to process._

<ins>**Returns:**</ins>
  - **dict:**
      - Updated pages dictionary containing valid item_id groupings.

### [`select_item()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L402)

Prompts the user to input one or more item IDs (semicolon-separated) and returns the valid ones.


<ins>**Returns:**</ins>
  - **list[str]:**
      - A list of valid item IDs.

### [`select_page()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L431)

Prompts the user to input one or more page names (semicolon-separated) and returns a

dictionary of valid pages and their associated item IDs.

<ins>**Returns:**</ins>
  - **dict:**
      - A dictionary mapping page names to their valid item IDs.

### [`choose_process(run_directly: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L461)

Presents the user with infobox generation options.


<ins>**Args:**</ins>
  - **run_directly (bool)**:
      - _Whether to allow quitting or going back._

<ins>**Returns:**</ins>
  - **str:**
      - The selected menu option.

### [`init_dependencies()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L497)

Initialises required modules so they don't interrupt tqdm progress bars.

### [`main(run_directly: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L504)

Entry point for infobox generation.


<ins>**Args:**</ins>
  - **run_directly (bool)**:
      - _Whether the script is being run directly._



[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_fixing.md) | [Next File](item_infobox_legacy.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)
