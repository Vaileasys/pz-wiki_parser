[Previous Folder](../objects/animal.md) | [Previous File](outfit_parser.md) | [Next File](outfit_zone_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# outfit_story_parser.py

Parses outfit usage from decompiled randomized story Java files.

Scans randomizedWorld story classes for outfit ID references and caches both
story-to-outfit and outfit-to-story lookup data.

## Functions

### [`parse_outfit_stories(outfit_data: dict, force_regenerate: bool = False) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_story_parser.py#L16)

Parse randomized story files for outfit references.

<ins>**Args:**</ins>
  - **outfit_data**:
      - _Parsed outfit data._
  - **force_regenerate**:
      - _Reparse files instead of using cache._

### [`get_outfit_ids(outfit_data: dict) -> set[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_story_parser.py#L121)

Return all outfit IDs from male and female outfit data.

<ins>**Args:**</ins>
  - **outfit_data**:
      - _Parsed outfit data._

### [`get_story_files() -> dict[str, list[str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_story_parser.py#L134)

Return randomized story Java files grouped by story type.

### [`search_file_for_outfits(file_path: str, outfit_ids: set[str]) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_story_parser.py#L184)

Search a Java file for outfit ID references.

<ins>**Args:**</ins>
  - **file_path**:
      - _Java file path._
  - **outfit_ids**:
      - _Outfit IDs to search for._


[Previous Folder](../objects/animal.md) | [Previous File](outfit_parser.md) | [Next File](outfit_zone_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
