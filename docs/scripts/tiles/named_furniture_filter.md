[Previous Folder](../recipes/craft_recipes.md) | [Next File](tiles_article.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)

# named_furniture_filter.py

Project Zomboid Wiki Named Furniture Filter

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

### [`process_tiles(tiles_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/named_furniture_filter.py#L156)

Process and organize tile data into furniture groups.


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
        - Split by sprite prefix if multiple exist
        - Handle facing directions for multi-sprite objects
        - Group by signature for variant handling

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/named_furniture_filter.py#L289)

Main execution function for the named furniture filter.

This function:
1. Loads the tile data cache
2. Processes tiles into furniture groups
3. Saves the processed data back to cache
4. Provides progress feedback through echo messages



[Previous Folder](../recipes/craft_recipes.md) | [Next File](tiles_article.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)
