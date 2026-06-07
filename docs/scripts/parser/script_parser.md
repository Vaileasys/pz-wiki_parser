[Previous Folder](../objects/animal.md) | [Previous File](recipe_parser.md) | [Next File](stash_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# script_parser.py

## Functions

### [`inject_templates(script_dict: dict, script_type: str, template_dict: dict) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L205)

Injects and merges template! and template entries into each script definition.

### [`post_process(script_dict: dict, script_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L354)

Applies post-processing logic based on script type.

### [`split_list(value: str, character: str) -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L365)

Splits by a specific character and normalises as a list

### [`split_dict(value: list[str], character: str) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L370)

Splits at a specific character and normalises as a dict.

### [`split_pipe_list(value: str) -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L391)

Splits at pipes `|` and normalises as a list.

### [`split_slash_list(value: str) -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L396)

Splits at slashes `/` and normalises as a list.

### [`split_space_list(value: str) -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L401)

Splits at spaces ` ` and normalises as a list.

### [`split_semicolon_list(value: str) -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L406)

Splits at semicolons `;` and normalises as a list.

### [`split_colon_list(value: str) -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L411)

Splits at colons `:` and normalises as a list.

### [`split_colon_dict(value: list[str]) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L416)

Splits at colons `:` and normalises as a dict.

### [`split_equal_dict(value: list[str]) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L421)

Splits at equals `=` and normalises as a dict.

### [`split_space_dict(value: list[str]) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L426)

Splits at spaces ` ` and normalises as a dict.

### [`parse_evolved_recipe(value: str, block_id: str = 'Unknown') -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L434)

Special case for processing values of 'EvolvedRecipe'.

### [`parse_fluid(value: str, block_id: str = 'Unknown') -> list[list]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L460)

Special case for processing values of 'fluid'.

### [`parse_fixer(value: str, block_id: str = 'Unknown') -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L476)

Special case for processing values of 'fixer'.

### [`parse_item_mapper(lines: list[str], block_id: str = 'Unknown') -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L506)

Special case for processing values of 'itemMapper'.

### [`compare_script_versions(script_type: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L537)

Compares current script data against the cached version(s).
If script_type is empty, runs for all cached types.

### [`process_value(key: str, value: str, block_id: str = 'Unknown', script_type: str = '') -> str | list | dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L600)

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
  - **str | list | dict**:
      - _The processed value, cast into a normalised format (e.g., list, dict, or scalar)._

### [`normalise(value: str) -> str | int | float | bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L691)

Convert a string to its type: int, float, bool, or str.

<ins>**Args:**</ins>
  - **value (str)**:
      - _The input string to normalise._

<ins>**Returns:**</ins>
  - **str | int | float | bool**:
      - _The value converted to its appropriate type._

### [`remove_comments(lines: list[str]) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L732)

Strip // single‑line comments and nested /* … */ block comments.

<ins>**Args:**</ins>
  - **lines**:
      - _list[str]_
  - **Raw lines read from a text file.**:
  - **Returns**:
  - **list[str]**:
  - **Lines with comments removed; blank lines are dropped.**:

### [`parse_key_value_line(line: str, data: dict, block_id: str = 'Unknown', script_type: str = '') -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L778)

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
  - **None**:

### [`parse_block(lines: list[str], block_id: str = 'Unknown', script_type: str = '') -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L846)

Parse a block of script lines into a nested dictionary.

<ins>**Args:**</ins>
  - **lines (list[str])**:
      - _Block of script lines._
  - **block_id (str, optional)**:
      - _Identifier for this block. Defaults to "Unknown"._
  - **script_type (str, optional)**:
      - _Script type to apply correct parsing rules. Defaults to ""._

<ins>**Returns:**</ins>
  - **dict**:
      - _Parsed block as a structured dictionary._

### [`is_blacklisted(filepath: str, script_type: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L921)

Check if a file should be blacklisted based on file and folder blacklists.

<ins>**Args:**</ins>
  - **filepath (str)**:
      - _Path to the file to check_
  - **script_type (str)**:
      - _Type of script being parsed_

<ins>**Returns:**</ins>
  - **bool**:
      - _True if file should be blacklisted, False otherwise_

### [`parse_entity_block(lines: list[str], entity_name: str, script_type: str = 'entity') -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L949)

Parse an entity block to extract component data.

<ins>**Args:**</ins>
  - **lines (list[str])**:
      - _Lines within the entity block_
  - **entity_name (str)**:
      - _Name of the entity_
  - **script_type (str)**:
      - _Script type (should be "entity")_

<ins>**Returns:**</ins>
  - **dict**:
      - _Parsed entity data with flattened component fields_

### [`check_cache_version(script_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L1035)

### [`extract_script_data(script_type: str, do_post_processing: bool = True, cache_result: bool = True, use_cache = True) -> dict[str, dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L1044)

Parses all script files of a given script type, extracting blocks into dictionaries keyed by FullType (i.e. [Module].[Type])

<ins>**Args:**</ins>
  - **script_type (str)**:
      - _Type of script to extract (e.g., "item", "vehicle")._
  - **prefix (str)**:
      - _Required prefix of the block type (e.g., "vehicle_")._

<ins>**Returns:**</ins>
  - **dict[str, dict]**:
      - _A dictionary of parsed script blocks keyed by full ID (FullType)._

### [`main(run_directly = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/script_parser.py#L1311)


[Previous Folder](../objects/animal.md) | [Previous File](recipe_parser.md) | [Next File](stash_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
