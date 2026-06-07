[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_article.md) | [Next File](tiles_codesnip.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)

# tiles_batch.py

## Functions

### [`parse_entities()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_batch.py#L31)

Wrapper function to parse entity data.

### [`generate_cache(cache_path: str, cache_label: str, parser_func, game_version: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_batch.py#L36)

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
  - **tuple**:
      - _(cache_data, cache_version) where:_
  - **- cache_data**:
      - _The loaded data or None if loading failed_
  - **- cache_version**:
      - _Version string of the cache or None if loading failed_

### [`main(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_batch.py#L64)

Main execution function for the tile processing pipeline.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_
  - **This function**:
  - **1. Ensures all necessary caches are present and up-to-date**:
  - **2. Loads or generates required data from game files**:
  - **3. Generates various wiki components**:
  - **- Infoboxes for tile properties**:
  - **- CodeSnips showing tile definitions**:
  - **- Scrapping tables for dismantling info**:
  - **- Complete wiki articles**:
  - **- Furniture and crafting surface lists**:
  - **4. Provides progress feedback through echo messages**:


[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_article.md) | [Next File](tiles_codesnip.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)
