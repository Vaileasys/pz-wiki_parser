[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_infobox.md) | [Next File](tiles_stitcher.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)

# tiles_scrapping.py

## Functions

### [`generate_scrapping_tables(tiles: dict, definitions: dict, lang_code: str) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_scrapping.py#L5)

Generate scrapping and breakage tables for tiles in the specified language.

<ins>**Args:**</ins>
  - **tiles (dict)**:
      - _Dictionary containing tile definitions and properties._
  - **definitions (dict)**:
      - _Dictionary containing scrapping and material definitions._
  - **lang_code (str)**:
      - _Language code for localization._

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary containing generated scrapping and breakage information for each tile group._
  - **The function creates MediaWiki-formatted tables for both scrapping and breakage mechanics,**:
  - **saving them to separate files in the output directory.**:

### [`_generate_disassembly_section(generic: dict, definitions: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_scrapping.py#L63)

Generate a MediaWiki table for disassembly (scrapping) information.

<ins>**Args:**</ins>
  - **generic (dict)**:
      - _Generic properties of the tile containing material information._
  - **definitions (dict)**:
      - _Dictionary containing scrap item definitions and rules._

<ins>**Returns:**</ins>
  - **str**:
      - _MediaWiki-formatted table showing disassembly materials, chances, and quantities._
  - **Returns empty string if no materials are defined.**:

### [`_generate_breakage_section(generic: dict, definitions: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_scrapping.py#L145)

Generate a MediaWiki table for breakage (destruction) information.

<ins>**Args:**</ins>
  - **generic (dict)**:
      - _Generic properties of the tile containing material information._
  - **definitions (dict)**:
      - _Dictionary containing material definitions for breakage._

<ins>**Returns:**</ins>
  - **str**:
      - _MediaWiki-formatted table showing breakage materials, chances, and quantities._
  - **Returns empty string if no materials are defined.**:


[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_infobox.md) | [Next File](tiles_stitcher.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)
