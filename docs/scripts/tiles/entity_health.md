[Previous Folder](../recipes/craft_recipes.md) | [Previous File](entity_article.md) | [Next File](entity_infobox.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)

# entity_health.py

## Functions

### [`extract_base_name(entity_name: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L18)

Extract the base name from an entity name by removing level suffix.

<ins>**Args:**</ins>
  - **entity_name (str)**:
      - _Full entity name (e.g., "Wood_BarElementCorner_Lvl1")_

<ins>**Returns:**</ins>
  - **str**:
      - _Base name without level suffix (e.g., "Wood_BarElementCorner")_

### [`group_entities_by_base(entity_data: Dict[str, dict]) -> Dict[str, List[tuple]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L33)

Group entities by their base name, sorting level variants together.

<ins>**Args:**</ins>
  - **entity_data (Dict[str, dict])**:
      - _Dictionary of all entity definitions_

<ins>**Returns:**</ins>
  - **Dict[str, List[tuple]]**:
      - _Dictionary mapping base names to list of (entity_name, entity_def) tuples_

### [`get_translated_name(entity_def: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L64)

Get the translated display name for an entity.

<ins>**Args:**</ins>
  - **entity_def (dict)**:
      - _Entity definition dictionary._

<ins>**Returns:**</ins>
  - **str**:
      - _Translated display name._

### [`extract_descriptor(display_name: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L84)

Extract the descriptor (text in parentheses) from a display name.

<ins>**Args:**</ins>
  - **display_name (str)**:
      - _Full display name like "Wooden Wall (Shoddy)"_

<ins>**Returns:**</ins>
  - **str**:
      - _The descriptor text like "Shoddy", or empty string if none found._

### [`map_descriptor(descriptor: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L100)

Map a descriptor to its replacement value.

<ins>**Args:**</ins>
  - **descriptor (str)**:
      - _Original descriptor (e.g., "Shoddy")_

<ins>**Returns:**</ins>
  - **str**:
      - _Mapped descriptor (e.g., "Basic") or original if no mapping exists._

### [`get_min_level(entity_def: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L113)

Extract the minimum skill level required to build an entity.

<ins>**Args:**</ins>
  - **entity_def (dict)**:
      - _Entity definition dictionary._

<ins>**Returns:**</ins>
  - **str**:
      - _Minimum skill level as string, or empty string if none._

### [`build_health_template_single(entity_name: str, entity_def: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L131)

Build a health template for a single entity (not merged).

<ins>**Args:**</ins>
  - **entity_name (str)**:
      - _Name identifier of the entity._
  - **entity_def (dict)**:
      - _Entity definition dictionary._

<ins>**Returns:**</ins>
  - **str**:
      - _MediaWiki health template markup._

### [`build_health_template_merged(base_name: str, entity_variants: List[tuple]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L167)

Build a merged health template for all level variants of an entity.

<ins>**Args:**</ins>
  - **base_name (str)**:
      - _Base name without level suffix._
  - **entity_variants (List[tuple])**:
      - _List of (entity_name, entity_def) tuples._

<ins>**Returns:**</ins>
  - **str**:
      - _MediaWiki health template markup with merged level variants._

### [`has_health_values(entity_def: dict) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L212)

Check if an entity has skillBaseHealth value.

<ins>**Args:**</ins>
  - **entity_def (dict)**:
      - _Entity definition dictionary._

<ins>**Returns:**</ins>
  - **bool**:
      - _True if entity has skillBaseHealth value._
  - **If health is missing but skillBaseHealth exists, health defaults to 0.**:

### [`generate_health_templates(grouped_entities: Dict[str, List[tuple]], lang_code: str) -> Dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L227)

Generate health templates for all entities.

<ins>**Args:**</ins>
  - **grouped_entities (Dict[str, List[tuple]])**:
      - _Dictionary mapping base names to entity variants._
  - **lang_code (str)**:
      - _Language code for output directory._

<ins>**Returns:**</ins>
  - **Dict[str, str]**:
      - _Dictionary mapping base names to their health template markup._

### [`main(lang_code: str, entity_data: Dict[str, dict] = None) -> Dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_health.py#L284)

Main execution function for entity health template generation.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_
  - **entity_data (Dict[str, dict], optional)**:
      - _Pre-loaded entity data. If None, loads from cache._

<ins>**Returns:**</ins>
  - **Dict[str, str]**:
      - _Dictionary mapping base names to their health template markup._
  - **This function**:
  - **1. Loads the parsed entity data cache (if not provided)**:
  - **2. Groups entities by base name (merging level variants)**:
  - **3. Generates health templates**:
  - **4. Outputs files to output/{lang_code}/tiles/entity_hp/**:


[Previous Folder](../recipes/craft_recipes.md) | [Previous File](entity_article.md) | [Next File](entity_infobox.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)
