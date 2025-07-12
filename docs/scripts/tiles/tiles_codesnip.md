[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_batch.md) | [Next File](tiles_infobox.md) | [Next Folder](../tools/update_icons.md) | [Back to Index](../../index.md)

# tiles_codesnip.py

Project Zomboid Wiki CodeSnip Generator

This script generates MediaWiki CodeSnip templates for Project Zomboid tile definitions.
It processes tile data and creates formatted code snippets that can be embedded in wiki
pages, showing the exact tile definitions from the game's source files.

Each tile's definition is formatted as a JSON code block within a CodeSnip template,
which provides syntax highlighting and source attribution on the wiki. The script
generates individual files for each tile definition and maintains a mapping of
all generated snippets.

## Functions

### [`generate_codesnips(named_tiles_data: Dict[str, Dict[str, dict]], lang_code: str, game_version: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_codesnip.py#L19)

Generate a CodeSnip wikitext snippet for each tile in every named group,

write each snippet to its own file, and return a mapping of
sprite_name -> codesnip wikitext.

<ins>**Args:**</ins>
  - **named_tiles_data (dict)**:
      - _Tiles organized by group name._
  - **lang_code (str)**:
      - _Language code (used as folder name)._
  - **game_version (str)**:
      - _Current game version._

<ins>**Returns:**</ins>
  - **dict:**
      - Mapping from sprite_name to its CodeSnip wikitext.



[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_batch.md) | [Next File](tiles_infobox.md) | [Next Folder](../tools/update_icons.md) | [Back to Index](../../index.md)
