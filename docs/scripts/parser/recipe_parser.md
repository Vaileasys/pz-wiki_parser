[Previous Folder](../objects/animal.md) | [Previous File](radio_parser.md) | [Next File](script_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# recipe_parser.py

## Functions

### [`remove_base_prefix(value: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L5)

Remove 'base:' prefix (case insensitive) from anywhere in the value.

<ins>**Args:**</ins>
  - **value (str)**:
      - _The input string to clean._

<ins>**Returns:**</ins>
  - **str**:
      - _The value with 'base:' prefix removed._

### [`parse_recipe_block(recipe_lines: List[str], block_id: str = 'Unknown') -> Dict[str, Any]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L27)

Parse a CraftRecipe block and return a structured dictionary.

### [`is_any_fluid_container(item_object: Dict[str, Any]) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L152)

Detect the legacy “any fluid container” wildcard:  item 1 [*]

### [`parse_items_block(block_text: str, is_output: bool = False, recipe_dict: Dict[str, Any] = None) -> List[Dict[str, Any]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L164)

Parse an inputs/outputs block, preserving legacy behaviour.

### [`parse_fluid_line(line: str) -> Dict[str, Any]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L276)

### [`parse_energy_line(line: str) -> Dict[str, Any]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L301)

### [`parse_item_line(line: str) -> Dict[str, Any]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L319)

### [`extract_block(text: str, start_index: int) -> Tuple[str, int]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L430)

### [`parse_module_block(full_text: str) -> List[Dict[str, str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L444)

### [`parse_module_skin_mapping(module_block: str) -> Dict[str, Dict[str, Dict[str, str]]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L458)

### [`parse_entity_blocks(module_block: str) -> List[Dict[str, Any]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L501)

### [`parse_sprite_config(block_text: str) -> Tuple[Dict[str, List[str]], float]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L555)

### [`parse_construction_recipe(full_text: str) -> List[Dict[str, Any]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L591)

Parse every `entity … { component CraftRecipe { … } }` in the source text
and return a list of normalised recipe dictionaries.

The routine now:

  1.  Collects a *global* skin‑mapping for **all** modules first.
  2.  Parses each entity and resolves its (skinName, entityStyle) pair
      against that global table so the `outputs` field is always filled
      when the information exists anywhere in the file‑set.


[Previous Folder](../objects/animal.md) | [Previous File](radio_parser.md) | [Next File](script_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
