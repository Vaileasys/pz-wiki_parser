[Previous Folder](../recipes/craft_recipes.md) | [Next File](tiles_article.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)

# named_furniture_filter.py

> Project Zomboid Wiki Named Furniture Filter

This script processes and organizes tile data for named furniture in Project Zomboid.
It handles both manually defined furniture groups and automatically detected furniture
based on game properties. The script is responsible for grouping related furniture
sprites and organizing them into logical sets for wiki documentation.

The script handles:
- Manual furniture group definitions
- Automatic furniture detection and grouping
- Multi-sprite furniture composition
- Variant handling for similar furniture types
- Directional (facing) furniture organization

## Functions

### [`process_tiles(tiles_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/named_furniture_filter.py#L157)

_Process and organize tile data into furniture groups._

<ins>**Args:**</ins>
  - **tiles_data (dict)**:
      - _Raw tile data from the game files._

<ins>**Returns:**</ins>
  - **dict:**
      - Processed and organized furniture groups.
      - The processing follows these steps:
      - 1. Process manually defined groups from MANUAL_GROUPS
      - 2. Group remaining tiles by their GroupName and CustomName properties
      - 3. Within each group:
      - - Split by sprite prefix if multiple exist
      - - Handle facing directions for multi-sprite objects
      - - Group by signature for variant handling
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/named_furniture_filter.py#L290)

_Main execution function for the named furniture filter._


[Previous Folder](../recipes/craft_recipes.md) | [Next File](tiles_article.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)
