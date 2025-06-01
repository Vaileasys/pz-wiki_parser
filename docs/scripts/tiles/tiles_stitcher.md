[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_scrapping.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)

# tiles_stitcher.py

> Project Zomboid Wiki Tile Stitcher

This script is responsible for combining multiple sprite tiles into composite images
for the Project Zomboid Wiki. It handles multi-tile furniture and objects that span
multiple grid cells, combining their individual sprites into a single cohesive image
while maintaining proper positioning and orientation.

The script processes sprites based on their facing direction (North, South, East, West)
and grid positions, using threading for improved performance.

## Functions

### [`parse_grid_position(position_string: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L59)

_Parse a grid position string into column and row indices._

<ins>**Args:**</ins>
  - **position_string (str)**:
      - _A string in the format "row,column" where both values are integers._

<ins>**Returns:**</ins>
  - **tuple[int, int]:**
      - A tuple containing (column_index, row_index).
      - Returns (0, 0) if the parsing fails.
### [`build_output_name(sprite_identifier_list: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L77)

_Generate an output filename by combining multiple sprite identifiers._

<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **str:**
      - Combined filename where the first identifier is the base and subsequent
      - ones are appended as suffixes, joined with '+'.
### [`composite_sprites(facing_direction: str, sprite_entries_list: list[dict], output_base_name: str, progress_bar)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L93)

_Create a composite image by combining multiple sprite images for a specific facing direction._

<ins>**Args:**</ins>
  - **facing_direction (str)**:
      - _The direction the sprite is facing ('N', 'S', 'E', or 'W')._
      - _sprite_entries_list (list[dict]): List of sprite entries containing sprite IDs and grid positions._
  - **output_base_name (str)**:
      - _Base name for the output file._
      - _progress_bar: tqdm progress bar instance for tracking progress._
      - _The function handles:_
      - _- Sorting sprites by grid position_
      - _- Computing canvas size based on sprite positions_
      - _- Compositing sprites onto a single image_
      - _- Saving the resulting image to the appropriate directory_
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_stitcher.py#L176)

_Main execution function for the tile stitcher._


[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_scrapping.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)
