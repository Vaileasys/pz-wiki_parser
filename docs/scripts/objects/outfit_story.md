[Previous Folder](../navbox/navbox.md) | [Previous File](outfit.md) | [Next File](outfit_zone.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# outfit_story.py

Provides access to randomized story outfit usage data.

OutfitStory loads parsed randomized story data and provides helpers for finding
which stories reference a given outfit ID.

## Classes

### `OutfitStory`

Provides cached lookup for outfit usage in randomized stories.

#### Class Methods

##### [`load(force: bool = False) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_story.py#L17)

Load outfit story data.

<ins>**Args:**</ins>
  - **force**:
      - _Reload data even if already loaded._

##### [`all() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_story.py#L35)

Return all outfit story data.

##### [`get(outfit_id: str) -> list[dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_story.py#L40)

Return stories that reference an outfit ID.

<ins>**Args:**</ins>
  - **outfit_id**:
      - _Outfit ID to search for._

##### [`has(outfit_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_story.py#L51)

Check whether an outfit appears in any story.

<ins>**Args:**</ins>
  - **outfit_id**:
      - _Outfit ID to check._

##### [`story_types() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_story.py#L61)

Return story data grouped by story type.

##### [`outfit_to_stories() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_story.py#L67)

Return story data grouped by outfit ID.


[Previous Folder](../navbox/navbox.md) | [Previous File](outfit.md) | [Next File](outfit_zone.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
