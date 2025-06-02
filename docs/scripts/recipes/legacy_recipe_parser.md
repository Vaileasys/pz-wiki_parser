[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](legacy_recipe_output.md) | [Next File](researchrecipes.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)

# legacy_recipe_parser.py

Project Zomboid Wiki Legacy Recipe Parser

This script parses legacy recipe definitions from Project Zomboid's script files.
It handles the complex task of parsing various recipe formats, including crafting
recipes, fluid recipes, and construction recipes, converting them into a structured
format for wiki documentation.

The script handles:
- Parsing recipe blocks from multiple source files
- Processing nested recipe definitions
- Handling item mappers and substitutions
- Processing fluid and energy recipes
- Managing construction and crafting recipes
- Cache management for parsed data

## Functions

### [`remove_comments(text)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L31)

_Removes block comments from text._

<ins>**Args:**</ins>
  - **text (str)**:
      - _Text containing block comments._

<ins>**Returns:**</ins>
  - **str:**
      - Text with all block comments removed.
      - Comments start with /* and end with */.
      - Supports nested comments and preserves non-comment text.

### [`get_recipe_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L68)

_Returns the parsed recipe data._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed recipe data, initializing it if empty.
      - This function serves as the main interface to access the parsed recipe data,
      - ensuring the data is loaded before being accessed.

### [`gather_recipe_lines(directory: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L84)

_Gathers recipe definitions from all relevant files in the directory._

<ins>**Args:**</ins>
  - **directory (str)**:
      - _Root directory to search for recipe files._

<ins>**Returns:**</ins>
  - **list:**
      - All lines from valid recipe files.
      - Searches for files that:
        - Start with 'recipes', 'entity', or 'craftrecipe'
        - End with '.txt'
        - Don't contain 'test' or 'dbg' in the name

### [`extract_recipe_blocks(lines)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L116)

_Extracts individual recipe blocks from a list of lines._

<ins>**Args:**</ins>
  - **lines (list)**:
      - _List of text lines to process._

<ins>**Returns:**</ins>
  - **list:**
      - List of tuples containing (recipe_name, recipe_text).

<ins>**Handles:**</ins>
  - Recipe block detection and extraction
  - Proper bracket matching
  - Comment removal
  - Recipe name extraction

### [`parse_recipe_block(recipe_name, recipe_text)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L166)

_Parses a recipe block into a structured dictionary._

<ins>**Args:**</ins>
  - **recipe_name (str)**:
      - _Name of the recipe._
  - **recipe_text (str)**:
      - _Raw text of the recipe block._

<ins>**Returns:**</ins>
  - **dict:**
      - Structured recipe data including:
        - name: Recipe name
        - inputs: List of input items
        - outputs: List of output items
        - itemMappers: Dictionary of item mappings
        - Additional properties like category

<ins>**Handles:**</ins>
  - Item mapper definitions
  - Input and output blocks
  - Property parsing
  - Comment removal

### [`parse_items_block(block_text, is_output, recipe_dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L259)

_Parses a block of item definitions within a recipe._

<ins>**Args:**</ins>
  - **block_text (str)**:
      - _Text containing item definitions._
  - **is_output (bool)**:
      - _Whether this is an output block._
  - **recipe_dict (dict)**:
      - _Parent recipe dictionary for context._

<ins>**Returns:**</ins>
  - **list:**
      - List of parsed item definitions.

<ins>**Handles:**</ins>
  - Fluid items and modifiers
  - Energy items
  - Regular items
  - Item properties and amounts

### [`is_any_fluid_container(item_obj)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L348)

_Checks if an item object represents any fluid container._

<ins>**Args:**</ins>
  - **item_obj (dict)**:
      - _Item object to check._

<ins>**Returns:**</ins>
  - **bool:**
      - True if the item is any fluid container, False otherwise.

### [`parse_fluid_line(line)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L364)

_Parses a fluid line definition._

<ins>**Args:**</ins>
  - **line (str)**:
      - _Line containing fluid definition._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed fluid information including:
        - sign: '+' or '-' for fluid addition/removal
        - items: List of fluid types
        - amount: Fluid amount
      - Returns None if parsing fails.

### [`parse_energy_line(line)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L394)

_Parses an energy line definition._

<ins>**Args:**</ins>
  - **line (str)**:
      - _Line containing energy definition._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed energy information including:
        - energy: True flag
        - amount: Energy amount
      - Returns None if parsing fails.

### [`parse_item_line(line)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L420)

_Parses an item line definition._

<ins>**Args:**</ins>
  - **line (str)**:
      - _Line containing item definition._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed item information including:
        - items: List of item types
        - amount: Item amount
        - index: Item index
        - Additional properties
      - Returns None if parsing fails.

### [`extract_block(text, start_index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L514)

_Extracts a complete block of text between braces._

<ins>**Args:**</ins>
  - **text (str)**:
      - _Text to extract block from._
  - **start_index (int)**:
      - _Starting position for extraction._

<ins>**Returns:**</ins>
  - **tuple:**
      - (block_text, end_index) where:
        - block_text: Extracted block content
        - end_index: Index after the closing brace

### [`parse_module_block(text)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L541)

_Parses a module block definition._

<ins>**Args:**</ins>
  - **text (str)**:
      - _Text containing module definition._

<ins>**Returns:**</ins>
  - **tuple:**
      - (skin_mapping, entity_blocks) where:
        - skin_mapping: Dictionary of skin mappings
        - entity_blocks: List of entity block definitions

### [`parse_module_skin_mapping(module_block)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L567)

_Parses skin mappings from a module block._

<ins>**Args:**</ins>
  - **module_block (str)**:
      - _Module block text._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary of skin mappings.

### [`parse_entity_blocks(module_block, skin_mapping)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L600)

_Parses entity blocks from a module block._

<ins>**Args:**</ins>
  - **module_block (str)**:
      - _Module block text._
  - **skin_mapping (dict)**:
      - _Dictionary of skin mappings._

<ins>**Returns:**</ins>
  - **list:**
      - List of parsed entity blocks.

### [`parse_sprite_config(block_text)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L643)

_Parses sprite configuration from a block._

<ins>**Args:**</ins>
  - **block_text (str)**:
      - _Block containing sprite configuration._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed sprite configuration.

### [`parse_construction_recipe(text)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L688)

_Parses a construction recipe definition._

<ins>**Args:**</ins>
  - **text (str)**:
      - _Text containing construction recipe._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed construction recipe data.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_parser.py#L735)

_Main execution function for legacy recipe parsing._



[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](legacy_recipe_output.md) | [Next File](researchrecipes.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
