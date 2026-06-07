[Previous Folder](../navbox/navbox.md) | [Previous File](outfit_story.md) | [Next File](profession.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# outfit_zone.py

Provides access to outfit zombie zone spawn data.

OutfitZone loads parsed ZombiesZoneDefinition data and provides helpers for
finding which zombie zones reference a given outfit ID.

## Classes

### `OutfitZone`

Provides cached lookup for outfit zombie zone spawn data.

#### Class Methods

##### [`load(force: bool = False) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_zone.py#L16)

Load outfit zone data.

<ins>**Args:**</ins>
  - **force**:
      - _Reload data even if already loaded._

##### [`all() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_zone.py#L33)

Return all outfit zone data.

##### [`get(outfit_id: str) -> list[dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_zone.py#L38)

Return zones that reference an outfit ID.

<ins>**Args:**</ins>
  - **outfit_id**:
      - _Outfit ID to search for._

##### [`has(outfit_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_zone.py#L74)

Check whether an outfit appears in any zone.

<ins>**Args:**</ins>
  - **outfit_id**:
      - _Outfit ID to check._

#### Static Methods

##### [`_dedupe_zones(zones: list[dict]) -> list[dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit_zone.py#L84)

Remove duplicate zone names.

<ins>**Args:**</ins>
  - **zones**:
      - _Zone match dictionaries._


[Previous Folder](../navbox/navbox.md) | [Previous File](outfit_story.md) | [Next File](profession.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
