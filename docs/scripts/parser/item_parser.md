[Previous Folder](../objects/components.md) | [Previous File](fluid_parser.md) | [Next File](literature_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# item_parser.py

## Functions

### [`get_item_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L23)
### [`is_blacklisted(item_name, item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L30)

_Check if item is blacklisted_

### [`parse_fluid_container(lines, start_index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L47)

_Parse fluid container_

### [`parse_item(lines, start_index, module_name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L119)

_Parse an item and its properties_

### [`parse_module(lines)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L208)

_Parse the module and its items_

### [`parse_files(file_paths: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L244)

_Parses a list of .txt files and updates the global parsed_data._

<ins>**Args:**</ins>
  - **file_paths (list[str])**:
      - _List of absolute file paths to parse._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed item data.

### [`get_new_items(old_dict, new_dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L281)

_Compares the new dict with the old dict and returns a dict of new items and another for changed properties._

### [`init()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/item_parser.py#L307)

_Initialise parser_



[Previous Folder](../objects/components.md) | [Previous File](fluid_parser.md) | [Next File](literature_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
