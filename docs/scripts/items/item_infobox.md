[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_groups.md) | [Next File](item_lists.md) | [Next Folder](groups/ammo_groups.md) | [Back to Index](../../index.md)

# item_infobox.py

Item infobox generator.

This module processes `Item` objects into structured infobox parameters, formatted for wiki output.
It handles individual items, pages with multiple item IDs, and supports both combined and standalone infobox generation.

Main functions:
- Extract item attributes into infobox fields
- Merge multiple item definitions into unified infobox data, based on page
- Format and output infobox content as text files

## Functions

### [`generate_item_data(item: Item, language_code: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L48)

Extracts relevant parameters from an Item object into a dictionary.

<ins>**Args:**</ins>
  - **item (Item)**:
      - _The item object to process._
  - **language_code (str, optional)**:
      - _Language code to use for translations._

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary of infobox parameters for the given item._

### [`post_process_rm(data: dict, page: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L374)

Post processing of generated item data to add recorded media properties.

### [`get_translation(translation_key: str, language_code: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L391)

Get translation for a given key.

<ins>**Args:**</ins>
  - **translation_key (str)**:
      - _The key to translate_
  - **language_code (str, optional)**:
      - _Language code to use. If None, uses current language._

<ins>**Returns:**</ins>
  - **str**:
      - _The translated string or the original key if translation not found_

### [`build_infobox(infobox_data: dict) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L435)

Builds an infobox template from the provided parameters.

<ins>**Args:**</ins>
  - **infobox_data (dict)**:
      - _Dictionary of key-value infobox fields._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _A list of lines forming the infobox template._

### [`join_keys(params: dict) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L455)

Converts list values of specific keys into <br>-joined strings.

<ins>**Args:**</ins>
  - **params (dict)**:
      - _Infobox parameters._

<ins>**Returns:**</ins>
  - **dict**:
      - _Updated dictionary with joined string values for specified keys._

### [`get_descriptor(item_id: str) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L473)

Returns a short label for the item, based on patterns in its ID.

Matches are defined in 'item_descriptors.json' using start, end, or contains rules.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _Full item ID._

<ins>**Returns:**</ins>
  - **str | None**:
      - _Descriptor if matched, otherwise None._

### [`merge_items(page_data: dict) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L518)

Merges parameters from multiple item variants into a single infobox-ready dictionary.

Identical values shared across all items are included once without a descriptor.

Keys listed in `DESCRIPTOR_KEYS` will trigger descriptor formatting if their values differ between items.
Keys listed in `SKIP_KEYS` are only included from the first (primary) item.

<ins>**Args:**</ins>
  - **page_data (dict)**:
      - _Mapping of item_id to parameter dictionaries._

<ins>**Returns:**</ins>
  - **dict**:
      - _Merged dictionary of parameters with values enumerated and descriptors applied where needed._

### [`process_pages(pages: dict, language_code: str = None) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L605)

Generates infoboxes for all items grouped by page name and writes output files.

<ins>**Args:**</ins>
  - **pages (dict)**:
      - _Mapping of page names to their item_id entries._
  - **language_code (str, optional)**:
      - _Language code to use for translations._

### [`process_items(item_id_list: list, language_code: str = None) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L661)

Generates infoboxes for a list of specific item IDs and writes output files.

<ins>**Args:**</ins>
  - **item_id_list (list)**:
      - _List of item IDs to process._
  - **language_code (str, optional)**:
      - _Language code to use for translations._

### [`prepare_media_pages(rm_id) -> set`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L692)

### [`prepare_pages(item_id_list: list) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L741)

Prepares and validates the item-to-page mappings for later infobox generation.

<ins>**Args:**</ins>
  - **item_id_list (list)**:
      - _List of item IDs to process._

<ins>**Returns:**</ins>
  - **dict**:
      - _Updated pages dictionary containing valid item_id groupings._

### [`select_item() -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L812)

Prompts the user to input one or more item IDs (semicolon-separated) and returns the valid ones.

<ins>**Returns:**</ins>
  - **list[str]**:
      - _A list of valid item IDs._

### [`select_page() -> dict[str, dict[str, list[str]]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L843)

Prompts the user to input one or more page names (semicolon-separated) and returns a
dictionary of valid pages and their associated item IDs.

<ins>**Returns:**</ins>
  - **dict**:
      - _A dictionary mapping page names to their valid item IDs._

### [`choose_process(run_directly: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L877)

Presents the user with infobox generation options.

<ins>**Args:**</ins>
  - **run_directly (bool)**:
      - _Whether to allow quitting or going back._

<ins>**Returns:**</ins>
  - **str**:
      - _The selected menu option._

### [`init_dependencies()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L914)

Initialises required modules so they don't interrupt tqdm progress bars.

### [`main(run_directly: bool = False, language: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L919)

Entry point for infobox generation.

<ins>**Args:**</ins>
  - **run_directly (bool)**:
      - _Whether the script is being run directly._
  - **language (str, optional)**:
      - _Language code to use. If None, uses current language._

### [`batch_entry(language_code = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox.py#L955)

Entry point for batch processing.

This function runs both processing modes automatically:
1. Process all pages (with merging) - generates merged infoboxes for items that share pages
2. Process all individual items (no merging) - generates individual infoboxes for each item

<ins>**Args:**</ins>
  - **language_code (str, optional)**:
      - _Language code to use. If None, uses current language._


[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_groups.md) | [Next File](item_lists.md) | [Next Folder](groups/ammo_groups.md) | [Back to Index](../../index.md)
