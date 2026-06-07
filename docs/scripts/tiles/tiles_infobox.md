[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_container_mapping.md) | [Next File](tiles_scrapping.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)

# tiles_infobox.py

Project Zomboid Wiki Infobox Generator

This script generates MediaWiki infobox templates for Project Zomboid tiles. It processes
tile definitions and properties to create structured information boxes that appear at
the top of wiki articles, containing key information about each tile type.

The script handles:
- Display names and translations
- Tile properties and statistics
- Tool requirements and skill levels
- Container capacities and special features
- Multi-tile object composition
- Image and sprite references

## Functions

### [`_parse_grid(pos: str) -> Tuple[int, int]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L59)

Parse a grid position string into column and row coordinates.

<ins>**Args:**</ins>
  - **pos (str)**:
      - _Position string in format "row,column"_

<ins>**Returns:**</ins>
  - **tuple[int, int]**:
      - _A tuple of (column, row) coordinates._
  - **Returns (0, 0) if parsing fails.**:

### [`_build_output_name(sprite_ids: List[str]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L77)

Generate a composite name from multiple sprite IDs.

<ins>**Args:**</ins>
  - **sprite_ids (List[str])**:
      - _List of sprite identifiers._

<ins>**Returns:**</ins>
  - **str**:
      - _Combined name where the first ID is the base and subsequent_
  - **ones are appended as suffixes, joined with '+'.**:

### [`_get_composite_names(tile_list: List[dict]) -> List[Tuple[str, str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L93)

Generate composite names for multi-tile objects based on facing direction.

<ins>**Args:**</ins>
  - **tile_list (List[dict])**:
      - _List of tile entries with sprite and facing information._

<ins>**Returns:**</ins>
  - **List[Tuple[str, str]]**:
      - _List of tuples containing (facing_direction, composite_name)._

### [`extract_tile_stats(tiles: Dict[str, dict], definitions: Dict[str, dict], lang_code: str) -> Tuple[float, int, str, str, str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L115)

Extract key statistics and requirements for a tile group.

<ins>**Args:**</ins>
  - **tiles (Dict[str, dict])**:
      - _Dictionary of tile definitions._
  - **definitions (Dict[str, dict])**:
      - _Dictionary of game definitions._
  - **lang_code (str)**:
      - _Language code for translations._

<ins>**Returns:**</ins>
  - **Tuple[float, int, str, str, str, str]**:
      - _Tuple containing:_
  - **- encumbrance**:
      - _Weight/encumbrance value_
  - **- max_size**:
      - _Maximum size of the tile group_
  - **- pickup_skill**:
      - _Required skill for pickup_
  - **- pickup_tool**:
      - _Required tool for pickup_
  - **- dis_skill**:
      - _Required skill for disassembly_
  - **- dis_tool**:
      - _Required tool for disassembly_

### [`generate_infoboxes(named_tiles_data: Dict[str, Dict], definitions: Dict[str, Dict], lang_code: str, game_version: str) -> Dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L168)

Generate infobox templates for all tile groups.

<ins>**Args:**</ins>
  - **named_tiles_data (Dict[str, Dict])**:
      - _Dictionary of tile groups and their definitions._
  - **definitions (Dict[str, Dict])**:
      - _Dictionary of game definitions._
  - **lang_code (str)**:
      - _Language code for translations._
  - **game_version (str)**:
      - _Current game version._

<ins>**Returns:**</ins>
  - **Dict[str, str]**:
      - _Dictionary mapping tile group names to their infobox markup._

### [`build_infobox(display_name: str, tiles: Dict[str, dict], definitions: Dict[str, dict], lang_code: str, game_version: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L233)

Build a complete infobox template for a tile group.

<ins>**Args:**</ins>
  - **display_name (str)**:
      - _Display name of the tile group._
  - **tiles (Dict[str, dict])**:
      - _Dictionary of tile definitions._
  - **definitions (Dict[str, dict])**:
      - _Dictionary of game definitions._
  - **lang_code (str)**:
      - _Language code for translations._
  - **game_version (str)**:
      - _Current game version._

<ins>**Returns:**</ins>
  - **str**:
      - _Complete MediaWiki infobox template markup._

### [`prepare_tile_list(tiles: Dict[str, dict]) -> Tuple[List[dict], Dict[str, int]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L279)

Process tile definitions into a structured list and count facings.

<ins>**Args:**</ins>
  - **tiles (Dict[str, dict])**:
      - _Dictionary of tile definitions._

<ins>**Returns:**</ins>
  - **Tuple[List[dict], Dict[str, int]]**:
      - _Tuple containing:_
  - **- List of processed tile entries with extracted properties**:
  - **- Dictionary counting tiles for each facing direction**:

### [`build_icon_params(tile_list: List[dict], max_size: int) -> List[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L336)

Generate icon parameters for the infobox template.

<ins>**Args:**</ins>
  - **tile_list (List[dict])**:
      - _List of processed tile entries._
  - **max_size (int)**:
      - _Maximum size of the tile group._

<ins>**Returns:**</ins>
  - **List[str]**:
      - _List of icon parameter lines for the infobox template._

### [`build_sprite_tile_params(tile_list: List[dict]) -> Tuple[List[str], List[str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L371)

### [`build_misc_params(tile_list: List[dict], definitions: Dict[str, dict], lang_code: str) -> List[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_infobox.py#L392)


[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_container_mapping.md) | [Next File](tiles_scrapping.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)
