[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_scrapping.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)

# tiles_stitcher.py

Project Zomboid Wiki Tile Stitcher

This script is responsible for combining multiple sprite tiles into composite images
for the Project Zomboid Wiki. It handles multi-tile furniture and objects that span
multiple grid cells, combining their individual sprites into a single cohesive image
while maintaining proper positioning and orientation.

The script processes sprites based on their facing direction (North, South, East, West)
and grid positions, using threading for improved performance.

This script supports both:
- Furniture tiles (from named_furniture.json with explicit SpriteGridPos)
- Entity tiles (from parsed_entity_data.json with spriteOutputs lists)

## Functions

### [`parse_grid_position(position_string: str) -> tuple[int, int]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L81)

Parse a grid position string into column and row indices.

<ins>**Args:**</ins>
  - **position_string (str)**:
      - _A string in the format "row,column" where both values are integers._

<ins>**Returns:**</ins>
  - **tuple[int, int]**:
      - _A tuple containing (column_index, row_index)._
  - **Returns (0, 0) if the parsing fails.**:

### [`build_output_name(sprite_identifier_list: list[str]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L99)

Generate an output filename by combining multiple sprite identifiers.

<ins>**Args:**</ins>
  - **sprite_identifier_list (list[str])**:
      - _List of sprite identifiers to combine._

<ins>**Returns:**</ins>
  - **str**:
      - _Combined filename where the first identifier is the base and subsequent_
  - **ones are appended as suffixes, joined with '+'.**:

### [`build_entity_output_name(sprite_identifier_list: list[str]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L117)

Generate an output filename for entity sprites by joining all identifiers with '+'.

<ins>**Args:**</ins>
  - **sprite_identifier_list (list[str])**:
      - _List of sprite identifiers to combine._

<ins>**Returns:**</ins>
  - **str**:
      - _Combined filename where all identifiers are joined with '+'._

### [`extract_entity_stitching_tasks(entity_data: dict) -> list[tuple[str, list[dict], str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L130)

Extract stitching tasks from entity data.

<ins>**Args:**</ins>
  - **entity_data (dict)**:
      - _Dictionary of entity definitions from parsed_entity_data.json._

<ins>**Returns:**</ins>
  - **list[tuple[str, list[dict], str]]**:
      - _List of stitching tasks in the format_
  - **(facing_direction, sprite_entries_list, output_base_name).**:

### [`composite_sprites(facing_direction: str, sprite_entries_list: list[dict], output_base_name: str, progress_bar, output_images_path: str = None, horizontal_offsets: dict = None, vertical_offsets: dict = None) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L180)

Create a composite image by combining multiple sprite images for a specific facing direction.

<ins>**Args:**</ins>
  - **facing_direction (str)**:
      - _The direction the sprite is facing ('N', 'S', 'E', or 'W')._
  - **sprite_entries_list (list[dict])**:
      - _List of sprite entries containing sprite IDs and grid positions._
  - **output_base_name (str)**:
      - _Base name for the output file._
  - **progress_bar**:
      - _tqdm progress bar instance for tracking progress._
  - **output_images_path (str, optional)**:
      - _Base path for output images. Defaults to OUTPUT_IMAGES_BASE_PATH._
  - **horizontal_offsets (dict, optional)**:
      - _Horizontal offset values. Defaults to SPRITE_HORIZONTAL_OFFSETS._
  - **vertical_offsets (dict, optional)**:
      - _Vertical offset values. Defaults to SPRITE_VERTICAL_OFFSETS._
  - **The function handles**:
  - **- Sorting sprites by grid position**:
  - **- Computing canvas size based on sprite positions**:
  - **- Compositing sprites onto a single image**:
  - **- Saving the resulting image to the appropriate directory**:

### [`stitch_furniture_tiles() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L289)

Process furniture tiles from named_furniture cache and create composite images.

### [`stitch_entity_tiles() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L349)

Process entity tiles from parsed_entity_data cache and create composite images.

### [`stitch_entity_sprites_for_lang(lang_code: str = None) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L390)

Convenience function to stitch entity sprites. Can be called from other scripts.

<ins>**Args:**</ins>
  - **lang_code (str, optional)**:
      - _Language code (currently unused but kept for API compatibility)._

### [`main() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L400)

Main execution function for the tile stitcher.

Processes both furniture and entity caches to identify multi-tile objects and creates
composite images for each valid combination. Uses multi-threading to improve
performance when processing multiple sprites.


[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_scrapping.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)
