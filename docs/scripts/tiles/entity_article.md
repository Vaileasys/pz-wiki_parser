[Previous Folder](../recipes/craft_recipes.md) | [Next File](entity_health.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)

# entity_article.py

## Functions

### [`extract_base_name(entity_name: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L14)

Extract the base name from an entity name by removing level suffix.

<ins>**Args:**</ins>
  - **entity_name (str)**:
      - _Full entity name (e.g., "Wood_BarElementCorner_Lvl1" or "WoodenWallLvl1")_

<ins>**Returns:**</ins>
  - **str**:
      - _Base name without level suffix (e.g., "Wood_BarElementCorner" or "WoodenWall")_

### [`group_entities_by_base(entity_data: Dict[str, dict]) -> Dict[str, List[tuple]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L29)

Group entities by their base name, sorting level variants together.

<ins>**Args:**</ins>
  - **entity_data (Dict[str, dict])**:
      - _Dictionary of all entity definitions_

<ins>**Returns:**</ins>
  - **Dict[str, List[tuple]]**:
      - _Dictionary mapping base names to list of (entity_name, entity_def) tuples_

### [`create_header(base_name: str, entity_variants: List[tuple], game_version: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L60)

Create the header markup for an entity article.

<ins>**Args:**</ins>
  - **base_name (str)**:
      - _Base name of the entity (without level suffix)._
  - **entity_variants (List[tuple])**:
      - _List of (entity_name, entity_def) tuples for all level variants._
  - **game_version (str)**:
      - _Current game version._

<ins>**Returns:**</ins>
  - **str**:
      - _Header markup with metadata templates._

### [`create_infobox(base_name: str, entity_variants: List[tuple], infoboxes: Dict[str, str]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L83)

Get the infobox for an entity from the generated infoboxes.

<ins>**Args:**</ins>
  - **base_name (str)**:
      - _Base name of the entity (without level suffix)._
  - **entity_variants (List[tuple])**:
      - _List of (entity_name, entity_def) tuples for all level variants._
  - **infoboxes (Dict[str, str])**:
      - _Dictionary mapping base names to merged infobox markup._

<ins>**Returns:**</ins>
  - **str**:
      - _Infobox markup._

### [`create_intro(base_name: str, entity_variants: List[tuple]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L101)

Create the introduction paragraph for an entity article.

<ins>**Args:**</ins>
  - **base_name (str)**:
      - _Base name of the entity (without level suffix)._
  - **entity_variants (List[tuple])**:
      - _List of (entity_name, entity_def) tuples for all level variants._

<ins>**Returns:**</ins>
  - **str**:
      - _Introduction paragraph._

### [`create_usage(base_name: str, entity_variants: List[tuple]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L139)

Create the usage section for an entity article.

<ins>**Args:**</ins>
  - **base_name (str)**:
      - _Base name of the entity (without level suffix)._
  - **entity_variants (List[tuple])**:
      - _List of (entity_name, entity_def) tuples for all level variants._

<ins>**Returns:**</ins>
  - **str**:
      - _Usage section markup._

### [`create_crafting(base_name: str, entity_variants: List[tuple]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L153)

Create the crafting section for an entity article.

<ins>**Args:**</ins>
  - **base_name (str)**:
      - _Base name of the entity (without level suffix)._
  - **entity_variants (List[tuple])**:
      - _List of (entity_name, entity_def) tuples for all level variants._

<ins>**Returns:**</ins>
  - **str**:
      - _Crafting section markup._

### [`create_navigation() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L178)

Create the navigation section for an entity article.

<ins>**Returns:**</ins>
  - **str**:
      - _Navigation section markup._

### [`collect_entity_sprites(grouped_entities: Dict[str, List[tuple]]) -> Set[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L189)

Collect all unique sprite names from all entities, including composite names.

<ins>**Args:**</ins>
  - **grouped_entities (Dict[str, List[tuple]])**:
      - _Dictionary mapping base names to entity variants._

<ins>**Returns:**</ins>
  - **Set[str]**:
      - _Set of unique sprite names used by entities (both individual and composite)._

### [`copy_entity_sprites(sprites: Set[str], lang_code: str, source_dir: str = 'resources/tile_images') -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L217)

Copy sprite images from source directory to output directory.
Also copies stitched composite sprites from the entity_images_stitched directories.

<ins>**Args:**</ins>
  - **sprites (Set[str])**:
      - _Set of sprite names to copy (including composite names)._
  - **lang_code (str)**:
      - _Language code for output directory._
  - **source_dir (str)**:
      - _Source directory containing individual sprite images._

### [`assemble_article(header: str, infobox: str, intro: str, usage: str, crafting: str, navigation: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L274)

Combine all article sections into a complete wiki article.

<ins>**Args:**</ins>
  - **header (str)**:
      - _Article header with metadata templates._
  - **infobox (str)**:
      - _Infobox template markup._
  - **intro (str)**:
      - _Article introduction paragraph._
  - **usage (str)**:
      - _Usage section markup._
  - **crafting (str)**:
      - _Crafting section markup._
  - **navigation (str)**:
      - _Navigation template markup._

<ins>**Returns:**</ins>
  - **str**:
      - _Complete wiki article text with all sections properly formatted._

### [`generate_entity_articles(grouped_entities: Dict[str, List[tuple]], infoboxes: Dict[str, str], lang_code: str, game_version: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L322)

Generate and save wiki articles for all entities.

<ins>**Args:**</ins>
  - **grouped_entities (Dict[str, List[tuple]])**:
      - _Dictionary mapping base names to list of (entity_name, entity_def) tuples._
  - **infoboxes (Dict[str, str])**:
      - _Dictionary mapping base names to their merged infobox markup._
  - **lang_code (str)**:
      - _Language code for output directory._
  - **game_version (str)**:
      - _Current game version._
  - **The function generates complete wiki articles by combining various components**:
  - **and saves them to individual files in the output directory structure.**:
  - **Each article includes metadata, infobox, introduction, usage information,**:
  - **crafting recipes, code snippets, and navigation elements.**:

### [`main(lang_code: str, entity_data: Dict[str, dict] = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/entity_article.py#L381)

Main execution function for entity article generation.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_
  - **entity_data (Dict[str, dict], optional)**:
      - _Pre-loaded entity data. If None, loads from cache._
  - **This function**:
  - **1. Loads the parsed entity data cache (if not provided)**:
  - **2. Groups entities by base name (merging level variants)**:
  - **3. Generates merged entity infoboxes**:
  - **4. Generates complete entity articles**:
  - **5. Outputs files to output/{lang_code}/tiles/entity_articles/**:


[Previous Folder](../recipes/craft_recipes.md) | [Next File](entity_health.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)
