[Previous File](animal_genes.md) | [Next File](animal_list_pzwiki.md) | [Next Folder](../core/cache.md) | [Back to Index](../../index.md)

# animal_infobox.py

Item infobox generator.

This module processes `Item` objects into structured infobox parameters, formatted for wiki output.
It handles individual items, pages with multiple item IDs, and supports both combined and standalone infobox generation.

Main functions:
- Extract item attributes into infobox fields
- Merge multiple item definitions into unified infobox data, based on page
- Format and output infobox content as text files

## Functions

### [`generate_animal_data(breed: AnimalBreed)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L33)

Extracts relevant parameters from an Item object into a dictionary.

<ins>**Args:**</ins>
  - **item (Item)**:
      - _The item object to process._

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary of infobox parameters for the given item._

### [`_translations_cache(key, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L95)

### [`build_infobox(infobox_data: dict) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L106)

Builds an infobox template from the provided parameters.

<ins>**Args:**</ins>
  - **infobox_data (dict)**:
      - _Dictionary of key-value infobox fields._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _A list of lines forming the infobox template._

### [`process_pages(pages: dict) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L126)

Generates infoboxes for all items grouped by page name and writes output files.

<ins>**Args:**</ins>
  - **pages (dict)**:
      - _Mapping of page names to their item_id entries._

### [`process_animals(full_breed_id_list: list, page_names: bool = False) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L172)

Generates infoboxes for a list of specific item IDs and writes output files.

<ins>**Args:**</ins>
  - **item_id_list (list)**:
      - _List of item IDs to process._

### [`prepare_pages(full_breed_id_list: list) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L194)

Prepares and validates the item-to-page mappings for later infobox generation.

<ins>**Args:**</ins>
  - **item_id_list (list)**:
      - _List of item IDs to process._

<ins>**Returns:**</ins>
  - **dict**:
      - _Updated pages dictionary containing valid item_id groupings._

### [`select_animal() -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L250)

Prompts the user to input one or more animal keys (semicolon-separated) and returns the valid ones.

<ins>**Returns:**</ins>
  - **list[str]**:
      - _A list of valid animal keys._

### [`select_page() -> dict[str, dict[str, list[str]]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L279)

Prompts the user to input one or more page names (semicolon-separated) and returns a
dictionary of valid pages and their associated item IDs.

<ins>**Returns:**</ins>
  - **dict**:
      - _A dictionary mapping page names to their valid item IDs._

### [`choose_process(run_directly: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L309)

Presents the user with infobox generation options.

<ins>**Args:**</ins>
  - **run_directly (bool)**:
      - _Whether to allow quitting or going back._

<ins>**Returns:**</ins>
  - **str**:
      - _The selected menu option._

### [`init_dependencies()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L345)

Initialises required modules so they don't interrupt tqdm progress bars.

### [`main(pre_choice: int = None, run_directly: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/animals/animal_infobox.py#L352)

Entry point for infobox generation.

<ins>**Args:**</ins>
  - **run_directly (bool)**:
      - _Whether the script is being run directly._


[Previous File](animal_genes.md) | [Next File](animal_list_pzwiki.md) | [Next Folder](../core/cache.md) | [Back to Index](../../index.md)
