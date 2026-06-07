[Previous Folder](../navbox/navbox.md) | [Previous File](profession.md) | [Next File](skill.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# recorded_media.py

## Classes

### `RecMedia`

Represents a single recorded media entry.

#### Class Methods

##### [`_parse()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L44)

Parses RecMedia data from the provided Lua file and caches it.

##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L57)

Loads RecMedia data from the cache, re-parsing the Lua file if the data is outdated.

<ins>**Returns:**</ins>
  - **dict**:
      - _Raw RecMedia data._

##### [`all() -> dict[str, 'RecMedia']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L80)

Returns all known RecMedia instances.

<ins>**Returns:**</ins>
  - **dict[str, RecMedia]**:
      - _Mapping of item ID to RecMedia instance._

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L92)

Returns the total number of RecMedia types parsed.

<ins>**Returns:**</ins>
  - **int**:
      - _Number of unique RecMedia types._

##### [`exists(rec_media_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L104)

Checks if a RecMedia with the given id exists in the parsed data.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if found, False otherwise._

##### [`get_media_items() -> 'list[Item]'`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L116)

##### [`get_item_dict() -> dict[str, list['RecMedia']]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L126)

##### [`get_page_dict() -> dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L147)

##### [`get_id_from_page(page: str) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L162)

#### Object Methods

##### [`__new__(guid: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L19)

Ensures only one RecMedia instance exists per recorded media ID.

##### [`__init__(guid: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L31)

Initialise the RecMedia instance with its data if not already initialised.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L167)

Returns a raw value from the RecMedia data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Key to look up._
  - **default**:
      - _Value to return if key is missing._

<ins>**Returns:**</ins>
  - **Any**:
      - _Value from the raw data or default._

##### [`get_speaker_lines() -> list[tuple[str, 'RecMediaLine']]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L180)

Returns a list of (speaker, RecMediaLine) tuples based on color-coded speaker identity.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L283)

#### Properties

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L200)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L204)

##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L208)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L213)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L217)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L221)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L236)

##### [`title_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L240)

##### [`title`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L244)

##### [`subtitle_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L248)

##### [`subtitle`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L252)

##### [`author_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L256)

##### [`author`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L260)

##### [`extra_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L264)

##### [`extra`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L268)

##### [`category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L272)

##### [`spawning`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L276)

##### [`lines`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L280)

### `RecMediaLine`

Represents a single line of recorded media content.

#### Object Methods

##### [`__init__(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L290)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L314)

#### Properties

##### [`text_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L294)

##### [`text`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L298)

##### [`color`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L303)

##### [`codes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/recorded_media.py#L311)


[Previous Folder](../navbox/navbox.md) | [Previous File](profession.md) | [Next File](skill.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
