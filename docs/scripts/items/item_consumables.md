[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_codesnip.md) | [Next File](item_container_contents.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)

# item_consumables.py

Consumables template generator.

This module processes food items, generating a `{{Consumables}}` templates 
for each valid food item and writes to individual text files for use on the PZwiki.

## Functions

### [`get_variant(item: Item, variant: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_consumables.py#L16)

Returns the icon for a specific variant of the item, if it exists.


<ins>**Args:**</ins>
  - **item (Item)**:
      - _Item object to get icons for._
  - **variant (str, optional)**:
      - _Variant type such as 'cooked', 'rotten', or 'burnt'._

<ins>**Returns:**</ins>
  - **str:**
      - Icon filename for the variant, or the base icon if not found.

### [`generate_data(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_consumables.py#L46)

Extracts and formats consumable data for a given item.


<ins>**Args:**</ins>
  - **item (Item)**:
      - _The item to generate data from._

<ins>**Returns:**</ins>
  - dict | None: Dictionary of parameters for the template, or None if not applicable.

### [`build_template(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_consumables.py#L89)

Builds a `{{Consumables}}` template from the item data.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Parameter data for the template._

<ins>**Returns:**</ins>
  - **list[str]:**
      - Lines of the wiki template content.

### [`process_items(items_list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_consumables.py#L107)

Processes a list of item IDs and writes their template files.


<ins>**Args:**</ins>
  - **items_list (list[str])**:
      - _List of item IDs to process._

### [`select_item()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_consumables.py#L127)

Prompts user to input a valid item ID.


<ins>**Returns:**</ins>
  - **list[str]:**
      - A list containing a single validated item ID.

### [`main(run_directly)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_consumables.py#L141)

Main entry point for the generator. Prompts user for input mode and processes items.


<ins>**Args:**</ins>
  - **run_directly (bool, optional)**:
      - _If True, enables quit option instead of back. Defaults to False._



[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_codesnip.md) | [Next File](item_container_contents.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)
