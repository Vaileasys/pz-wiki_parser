[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_article.md) | [Next File](tiles_codesnip.md) | [Next Folder](../tools/update_icons.md) | [Back to Index](../../index.md)

# tiles_batch.py

Project Zomboid Wiki Tile Processing Orchestrator

This script orchestrates the complete tile processing pipeline for the Project Zomboid Wiki.
It manages cache generation, data parsing, and the generation of various wiki components
including infoboxes, code snippets, scrapping tables, and complete articles.

The script handles:
- Cache management and validation
- Data parsing from game files
- Generation of wiki components
- Article assembly and organization
- List generation for furniture and crafting surfaces

## Functions

### [`generate_cache(cache_path: str, cache_label: str, parser_func, game_version: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_batch.py#L43)

Generate or load a cache file for tile data.


<ins>**Args:**</ins>
  - **cache_path (str)**:
      - _Path to the cache file._
  - **cache_label (str)**:
      - _Human-readable label for the cache type._
  - **parser_func (callable)**:
      - _Function to parse data if cache needs regeneration._
  - **game_version (str)**:
      - _Current game version for cache validation._

<ins>**Returns:**</ins>
  - **tuple:**
      - (cache_data, cache_version) where:
        - cache_data: The loaded data or None if loading failed
        - cache_version: Version string of the cache or None if loading failed

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_batch.py#L71)

Main execution function for the tile processing pipeline.

This function:
1. Ensures all necessary caches are present and up-to-date
2. Loads or generates required data from game files
3. Generates various wiki components:
- Infoboxes for tile properties
- CodeSnips showing tile definitions
- Scrapping tables for dismantling info
- Complete wiki articles
- Furniture and crafting surface lists
4. Provides progress feedback through echo messages



[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_article.md) | [Next File](tiles_codesnip.md) | [Next Folder](../tools/update_icons.md) | [Back to Index](../../index.md)
