[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_infobox.md) | [Next File](tiles_scrapping.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)

# tiles_navbox.py

Project Zomboid Wiki Navigation Box Generator

This script generates navigation boxes (navboxes) for tile-related pages on the
Project Zomboid Wiki. Navigation boxes provide quick links between related articles
and help users navigate through different categories of tiles.

The script handles:
- Category organization for tiles
- Link generation between related articles
- Template generation for MediaWiki navboxes
- Proper grouping of tile types

## Functions

### [`generate_navbox(tiles_data: dict, lang_code: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_navbox.py#L21)

_Generate a navigation box template for tile articles._

<ins>**Args:**</ins>
  - **tiles_data (dict)**:
      - _Dictionary containing tile definitions and properties._
  - **lang_code (str)**:
      - _Language code for localization._

<ins>**Returns:**</ins>
  - **str:**
      - MediaWiki markup for the navigation box template.

### [`save_navbox(navbox_content: str, lang_code: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_navbox.py#L35)

_Save the generated navigation box to a file._

<ins>**Args:**</ins>
  - **navbox_content (str)**:
      - _Generated navigation box markup._
  - **lang_code (str)**:
      - _Language code for determining output path._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_navbox.py#L55)

_Main execution function for navigation box generation._



[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_infobox.md) | [Next File](tiles_scrapping.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)
