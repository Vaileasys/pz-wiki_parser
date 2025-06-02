[Previous Folder](../objects/components.md) | [Previous File](recipe_parser.md) | [Next File](stash_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# script_parser.py

## Functions

### [`inject_templates(script_dict: dict, script_type: str, template_dict: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L106)

Injects and merges template! and template entries into each script definition.

### [`post_process(script_dict: dict, script_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L231)

Applies post-processing logic based on script type.

### [`split_list(value: str, character: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L241)

Splits by a specific character and normalises as a list

### [`split_dict(value: list[str], character: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L245)

Splits at a specific character and normalises as a dict.

### [`split_pipe_list(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L265)

Splits at pipes '|' and normalises as a list.

### [`split_slash_list(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L269)

Splits at slashes '/' and normalises as a list.

### [`split_space_list(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L273)

Splits at spaces ' ' and normalises as a list.

### [`split_semicolon_list(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L277)

Splits at semicolons ';' and normalises as a list.

### [`split_colon_list(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L281)

Splits at colons ':' and normalises as a list.

### [`split_colon_dict(value: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L285)

Splits at colons ':' and normalises as a dict.

### [`split_equal_dict(value: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L289)

Splits at equals '=' and normalises as a dict.

### [`split_space_dict(value: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L293)

Splits at spaces ' ' and normalises as a dict.

### [`parse_evolved_recipe(value: str, block_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L300)

Special case for processing values of 'EvolvedRecipe'.

### [`parse_fluid(value: str, block_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L325)

Special case for processing values of 'fluid'.

### [`parse_fixer(value: str, block_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L340)

Special case for processing values of 'fixer'.

### [`parse_item_mapper(lines: list[str], block_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L372)

Special case for processing values of 'itemMapper'.

### [`process_value(key: str, value: str, block_id: str, script_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L400)

Processes a raw value string into its appropriate type based on key and script type rules.

Applies special handling for known keys and uses config-based rules to convert values into lists or dictionaries based on separators.

<ins>**Args:**</ins>
  - **key (str)**:
      - _The key associated with the value (e.g., "Tags", "EvolvedRecipe")._
  - **value (str)**:
      - _The raw string value to be processed._
  - **block_id (str, optional)**:
      - _Identifier for the current script block, used in warnings. Defaults to "Unknown"._
  - **script_type (str, optional)**:
      - _Type of script being parsed (e.g., "item", "fixing"). Determines which rules apply._

<ins>**Returns:**</ins>
  - str | list | dict: The processed value, cast into a normalised format (e.g., list, dict, or scalar).

### [`normalise(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L489)

Convert a string to its type: int, float, bool, or str.


<ins>**Args:**</ins>
  - **value (str)**:
      - _The input string to normalise._

<ins>**Returns:**</ins>
  - str | int | float | bool: The value converted to its appropriate type.

### [`remove_comments(lines: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L521)

Strip // single‑line comments and nested /* … */ block comments.

Parameters:
lines : list[str]
Raw lines read from a text file.
Returns
list[str]
Lines with comments removed; blank lines are dropped.

### [`parse_key_value_line(line: str, data: dict, block_id: str, script_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L567)

Parses a single key-value line and inserts or merges it into the provided data dictionary.

Supports both '=' and ':' as separators, applies script-type-specific processing rules, and handles merging of values, lists, and nested dictionaries.

<ins>**Args:**</ins>
  - **line (str)**:
      - _The script line containing a key-value pair._
  - **data (dict)**:
      - _The dictionary to update with the parsed key and value._
  - **block_id (str, optional)**:
      - _Identifier for the current script block, used for warnings. Defaults to "Unknown"._
  - **script_type (str, optional)**:
      - _Type of script being parsed (e.g., "item", "vehicle"). Used to apply config rules._

<ins>**Returns:**</ins>
  - None

### [`parse_block(lines: list[str], block_id: str, script_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L629)

Parse a block of script lines into a nested dictionary.


<ins>**Args:**</ins>
  - **lines (list[str])**:
      - _Block of script lines._
  - **block_id (str, optional)**:
      - _Identifier for this block. Defaults to "Unknown"._
  - **script_type (str, optional)**:
      - _Script type to apply correct parsing rules. Defaults to ""._

<ins>**Returns:**</ins>
  - **dict:**
      - Parsed block as a structured dictionary.

### [`extract_script_data(script_type: str, do_post_processing: bool, cache_result: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L699)

Parses all script files of a given script type, extracting blocks into dictionaries keyed by FullType (i.e. [Module].[Type])


<ins>**Args:**</ins>
  - **script_type (str)**:
      - _Type of script to extract (e.g., "item", "vehicle")._
  - **prefix (str)**:
      - _Required prefix of the block type (e.g., "vehicle_")._

<ins>**Returns:**</ins>
  - **dict[str, dict]:**
      - A dictionary of parsed script blocks keyed by full ID (FullType).

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L869)


[Previous Folder](../objects/components.md) | [Previous File](recipe_parser.md) | [Next File](stash_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
