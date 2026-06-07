[Previous Folder](../navbox/navbox.md) | [Previous File](attachment.md) | [Next File](clothing_item.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# body_location.py

## Classes

### `BodyLocation`

#### Class Methods

##### [`_load_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L22)

##### [`_parse_locations()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L29)

##### [`_generate_item_body_locations()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L100)

Generates and caches ItemBodyLocations for all loaded items.

##### [`_parse_items() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L131)

##### [`_transform_data() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L150)

##### [`all() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L195)

#### Object Methods

##### [`__new__(location_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L204)

##### [`__init__(location_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L215)

##### [`__repr__() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L226)

#### Properties

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L232)

##### [`group`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L238)

##### [`alias`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L242)

##### [`multi_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L246)

##### [`exclusive`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L250)

##### [`hide_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L254)

##### [`alt_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L258)

##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L262)

##### [`lua_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L266)

### `BodyPart`

Static reference for body part display names.

#### Object Methods

##### [`__new__(body_part_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L298)

##### [`__init__(body_part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L309)

##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L312)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L315)

#### Properties

##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L319)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L322)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L327)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L332)

### `BodyPartList`

Helper class that wraps a list of BodyPart objects with additional properties for convenience.
Supports iteration and indexing.

#### Object Methods

##### [`__init__(body_parts: list[BodyPart])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L342)

<ins>**Args:**</ins>
  - **body_parts (list[BodyPart])**:
      - _A list of BodyPart objects._

##### [`__iter__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L349)

Returns an iterator over the body parts.

##### [`__getitem__(index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L353)

Returns the body part at the given index.

##### [`__len__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L357)

Returns the number of body parts.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L361)

Returns a debug representation of the body part list.

#### Properties

##### [`body_part_ids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L366)

Returns the internal names of each body part.

##### [`names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L371)

Returns the translated names of each body part.

##### [`wiki_links`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L376)

Returns the internal names of each body part.

##### [`display_names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L381)

Returns the display name keys of each body part.

### `BloodLocation`

Maps a named blood location to a set of body parts.

#### Class Methods

##### [`all() -> list['BloodLocation']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L449)

#### Object Methods

##### [`__new__(blood_location: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L427)

##### [`__init__(blood_location: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L438)

##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L442)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L445)

#### Properties

##### [`body_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L453)

Returns a list-like wrapper of BodyPart instances for this blood location.

### `BloodLocationList`

Helper class that wraps a list of BloodLocation objects with additional properties for convenience.
Supports iteration and indexing.

#### Object Methods

##### [`__init__(locations: list[BloodLocation])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L463)

<ins>**Args:**</ins>
  - **locations (list[BloodLocation])**:
      - _A list of BloodLocation objects._

##### [`__iter__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L470)

Returns an iterator over the blood locations.

##### [`__getitem__(index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L474)

Returns the blood location at the given index.

##### [`__len__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L478)

Returns the number of blood locations.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L482)

Returns a debug representation of the blood location list.

#### Properties

##### [`names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L487)

Returns the names of all blood locations.

##### [`body_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L492)


[Previous Folder](../navbox/navbox.md) | [Previous File](attachment.md) | [Next File](clothing_item.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
