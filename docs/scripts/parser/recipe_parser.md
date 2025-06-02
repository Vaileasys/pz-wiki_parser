[Previous Folder](../objects/components.md) | [Previous File](radio_parser.md) | [Next File](script_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# recipe_parser.py

## Functions

### [`parse_recipe_block(recipe_lines: List[str], block_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L4)

Parse a CraftRecipe block and return a structured dictionary.

### [`is_any_fluid_container(item_object: Dict[str, Any])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L111)

Detect the legacy “any fluid container” wildcard:  item 1 [*]

### [`parse_items_block(block_text: str, is_output: bool, recipe_dict: Dict[str, Any])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L123)

Parse an inputs/outputs block, preserving legacy behaviour.

### [`parse_fluid_line(line: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L229)
### [`parse_energy_line(line: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L246)
### [`parse_item_line(line: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L260)
### [`extract_block(text: str, start_index: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L333)
### [`parse_module_block(full_text: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L347)
### [`parse_module_skin_mapping(module_block: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L361)
### [`parse_entity_blocks(module_block: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L396)
### [`parse_sprite_config(block_text: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L440)
### [`parse_construction_recipe(full_text: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/recipe_parser.py#L470)

Parse every `entity … { component CraftRecipe { … } }` in the source text

and return a list of normalised recipe dictionaries.
The routine now:
1.  Collects a *global* skin‑mapping for **all** modules first.
2.  Parses each entity and resolves its (skinName, entityStyle) pair
against that global table so the `outputs` field is always filled
when the information exists anywhere in the file‑set.



[Previous Folder](../objects/components.md) | [Previous File](radio_parser.md) | [Next File](script_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
