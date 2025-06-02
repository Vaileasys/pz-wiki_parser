[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_navbox.md) | [Next File](tiles_stitcher.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)

# tiles_scrapping.py

Project Zomboid Wiki Scrapping Table Generator

This script generates wiki tables for item scrapping and breakage information in Project Zomboid.
It processes tile definitions to create formatted MediaWiki tables showing what materials
can be obtained from disassembling or breaking various objects in the game.

The script handles both disassembly (intentional scrapping) and breakage (destruction)
mechanics, generating separate tables for each process with relevant drop rates and quantities.

## Functions

### [`generate_scrapping_tables(tiles: dict, definitions: dict, lang_code: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_scrapping.py#L18)

_Generate scrapping and breakage tables for tiles in the specified language._

<ins>**Args:**</ins>
  - **tiles (dict)**:
      - _Dictionary containing tile definitions and properties._
  - **definitions (dict)**:
      - _Dictionary containing scrapping and material definitions._
  - **lang_code (str)**:
      - _Language code for localization._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary containing generated scrapping and breakage information for each tile group.
      - The function creates MediaWiki-formatted tables for both scrapping and breakage mechanics,
      - saving them to separate files in the output directory.

### [`_generate_disassembly_section(generic: dict, definitions: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_scrapping.py#L76)

_Generate a MediaWiki table for disassembly (scrapping) information._

<ins>**Args:**</ins>
  - **generic (dict)**:
      - _Generic properties of the tile containing material information._
  - **definitions (dict)**:
      - _Dictionary containing scrap item definitions and rules._

<ins>**Returns:**</ins>
  - **str:**
      - MediaWiki-formatted table showing disassembly materials, chances, and quantities.
      - Returns empty string if no materials are defined.

### [`_generate_breakage_section(generic: dict, definitions: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_scrapping.py#L158)

_Generate a MediaWiki table for breakage (destruction) information._

<ins>**Args:**</ins>
  - **generic (dict)**:
      - _Generic properties of the tile containing material information._
  - **definitions (dict)**:
      - _Dictionary containing material definitions for breakage._

<ins>**Returns:**</ins>
  - **str:**
      - MediaWiki-formatted table showing breakage materials, chances, and quantities.
      - Returns empty string if no materials are defined.



[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_navbox.md) | [Next File](tiles_stitcher.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)
