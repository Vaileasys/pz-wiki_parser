[Previous Folder](../objects/attachment.md) | [Previous File](evolvedrecipe_parser.md) | [Next File](literature_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# item_parser.py

## Functions

### [`get_item_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L24)
### [`is_blacklisted(item_name, item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L31)

Check if item is blacklisted

### [`parse_fluid_container(lines, start_index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L48)

Parse fluid container

### [`parse_item(lines, start_index, module_name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L120)

Parse an item and its properties

### [`parse_module(lines)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L209)

Parse the module and its items

### [`parse_files(file_paths: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L245)

Parses a list of .txt files and updates the global parsed_data.


<ins>**Args:**</ins>
  - **file_paths (list[str])**:
      - _List of absolute file paths to parse._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed item data.

### [`get_new_items(old_dict, new_dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L282)

Compares the new dict with the old dict and returns a dict of new items and another for changed properties.

### [`init()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L308)

Initialise parser



[Previous Folder](../objects/attachment.md) | [Previous File](evolvedrecipe_parser.md) | [Next File](literature_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
