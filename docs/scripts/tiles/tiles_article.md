[Previous Folder](../recipes/craft_recipes.md) | [Previous File](named_furniture_filter.md) | [Next File](tiles_batch.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)

# tiles_article.py

Project Zomboid Wiki Article Generator

This script generates complete wiki articles for Project Zomboid tiles. It combines
various components including infoboxes, usage information, code snippets, and navigation
elements to create comprehensive wiki pages for each tile type.

The script handles:
- Article structure and formatting
- Usage descriptions based on tile properties
- Dismantling and breakage information
- Code snippet integration
- Navigation elements

## Functions

### [`process_usage(tile_name, tile_data, scrappings)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_article.py#L21)

Build the 'Usage' section for a tile article.


<ins>**Args:**</ins>
  - **tile_name (str)**:
      - _Name of the tile group._
  - **tile_data (dict)**:
      - _Dictionary containing tile properties and variants._
  - **scrappings (dict)**:
      - _Dictionary containing dismantling and breakage information._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for the Usage section, including property-based
      - descriptions and dismantling/breakage information.

### [`process_codesnip(tile_data, codesnips)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_article.py#L122)

Create a CodeBox section containing all CodeSnip templates for a tile group.


<ins>**Args:**</ins>
  - **tile_data (dict)**:
      - _Dictionary of sprite names and their data._
  - **codesnips (dict)**:
      - _Dictionary mapping sprite names to their CodeSnip markup._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for the Code section containing all relevant
      - CodeSnip templates wrapped in a CodeBox.

### [`assemble_article(header, infobox, intro, usage, codesnip, navigation)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_article.py#L144)

Combine all article sections into a complete wiki article.


<ins>**Args:**</ins>
  - **header (str)**:
      - _Article header with metadata templates._
  - **infobox (str)**:
      - _Infobox template markup._
  - **intro (str)**:
      - _Article introduction paragraph._
  - **usage (str)**:
      - _Usage section markup._
  - **codesnip (str)**:
      - _Code section markup._
  - **navigation (str)**:
      - _Navigation template markup._

<ins>**Returns:**</ins>
  - **str:**
      - Complete wiki article text with all sections properly formatted.

### [`sanitize_filename(name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_article.py#L171)

Convert a string into a safe filesystem filename.


<ins>**Args:**</ins>
  - **name (str)**:
      - _Original string to convert._

<ins>**Returns:**</ins>
  - **str:**
      - Sanitized string safe for use as a filename, with special characters
      - replaced by underscores and spaces converted to underscores.

### [`generate_tile_articles(tiles_data, infoboxes, codesnips, scrappings)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_article.py#L191)

Generate and save wiki articles for all tile groups.


<ins>**Args:**</ins>
  - **tiles_data (dict)**:
      - _Dictionary containing all tile group data._
  - **infoboxes (dict)**:
      - _Dictionary mapping tile names to their infobox markup._
  - **codesnips (dict)**:
      - _Dictionary mapping sprite names to their CodeSnip markup._
  - **scrappings (dict)**:
      - _Dictionary containing dismantling and breakage information._
      - _The function generates complete wiki articles by combining various components_
      - _and saves them to individual files in the output directory structure._
      - _Each article includes metadata, infobox, introduction, usage information,_
      - _code snippets, and navigation elements._



[Previous Folder](../recipes/craft_recipes.md) | [Previous File](named_furniture_filter.md) | [Next File](tiles_batch.md) | [Next Folder](../tools/compare_item_lists.md) | [Back to Index](../../index.md)
