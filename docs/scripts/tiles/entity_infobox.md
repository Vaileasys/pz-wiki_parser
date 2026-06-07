[Previous Folder](../recipes/craft_recipes.md) | [Previous File](entity_health.md) | [Next File](named_furniture_filter.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)

# entity_infobox.py

## Functions

### [`_build_composite_sprite_name(sprite_ids: List[str]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_infobox.py#L37)

Generate a composite name from multiple sprite IDs.

<ins>**Args:**</ins>
  - **sprite_ids (List[str])**:
      - _List of sprite identifiers._

<ins>**Returns:**</ins>
  - **str**:
      - _Combined name where sprites are joined with '+'._

### [`build_entity_icon_params(sprite_outputs: Dict[str, List[str]]) -> Tuple[List[str], List[str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_infobox.py#L56)

Generate icon and sprite_id parameters from spriteOutputs.

<ins>**Args:**</ins>
  - **sprite_outputs (Dict[str, List[str]])**:
      - _Dictionary mapping facing directions to sprite lists._

<ins>**Returns:**</ins>
  - **Tuple[List[str], List[str]]**:
      - _Tuple containing (icon_lines, sprite_id_lines)._

### [`build_entity_infobox(entity_name: str, entity_def: dict, lang_code: str, game_version: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_infobox.py#L103)

Build a complete infobox template for an entity.

<ins>**Args:**</ins>
  - **entity_name (str)**:
      - _Name identifier of the entity._
  - **entity_def (dict)**:
      - _Entity definition dictionary._
  - **lang_code (str)**:
      - _Language code for translations._
  - **game_version (str)**:
      - _Current game version._

<ins>**Returns:**</ins>
  - **str**:
      - _Complete MediaWiki infobox template markup._

### [`generate_entity_infoboxes(entity_data: Dict[str, dict], lang_code: str, game_version: str) -> Dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_infobox.py#L198)

Generate infobox templates for all entities.

<ins>**Args:**</ins>
  - **entity_data (Dict[str, dict])**:
      - _Dictionary of entity definitions._
  - **lang_code (str)**:
      - _Language code for translations._
  - **game_version (str)**:
      - _Current game version._

<ins>**Returns:**</ins>
  - **Dict[str, str]**:
      - _Dictionary mapping entity names to their infobox markup._

### [`build_merged_entity_infobox(base_name: str, entity_variants: List[tuple], lang_code: str, game_version: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_infobox.py#L249)

Build a merged infobox for all level variants of an entity.

<ins>**Args:**</ins>
  - **base_name (str)**:
      - _Base name without level suffix._
  - **entity_variants (List[tuple])**:
      - _List of (entity_name, entity_def) tuples._
  - **lang_code (str)**:
      - _Language code for translations._
  - **game_version (str)**:
      - _Current game version._

<ins>**Returns:**</ins>
  - **str**:
      - _Complete MediaWiki infobox template markup with merged level variants._

### [`generate_merged_entity_infoboxes(grouped_entities: Dict[str, List[tuple]], lang_code: str, game_version: str) -> Dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_infobox.py#L394)

Generate merged infobox templates for all base entities.

<ins>**Args:**</ins>
  - **grouped_entities (Dict[str, List[tuple]])**:
      - _Dictionary mapping base names to list of (entity_name, entity_def) tuples._
  - **lang_code (str)**:
      - _Language code for translations._
  - **game_version (str)**:
      - _Current game version._

<ins>**Returns:**</ins>
  - **Dict[str, str]**:
      - _Dictionary mapping base entity names to their merged infobox markup._

### [`main(lang_code: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_infobox.py#L441)

Main execution function for entity infobox generation.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_
  - **This function**:
  - **1. Loads the parsed entity data cache**:
  - **2. Generates entity infoboxes**:
  - **3. Outputs files to output/{lang_code}/tiles/entity_infoboxes/**:


[Previous Folder](../recipes/craft_recipes.md) | [Previous File](entity_health.md) | [Next File](named_furniture_filter.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)
