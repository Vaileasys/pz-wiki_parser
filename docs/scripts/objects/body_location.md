[Previous Folder](../lists/body_locations_list.md) | [Next File](clothing_item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# body_location.py

## Classes

### `BodyLocation`
#### Class Methods
##### [`_load_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L16)
##### [`_parse_locations()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L22)
##### [`_parse_items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L91)
##### [`_rearrange_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L110)
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L148)
#### Object Methods
##### [`__new__(location_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L157)
##### [`__init__(location_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L168)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L176)
#### Properties
##### [`group`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L182)
##### [`alias`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L186)
##### [`multi_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L190)
##### [`exclusive`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L194)
##### [`hide_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L198)
##### [`alt_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L202)
##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L206)

### `BodyPart`

Static reference for body part display names.

#### Object Methods
##### [`__new__(body_part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L235)
##### [`__init__(body_part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L246)
##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L249)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L252)
#### Properties
##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L256)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L259)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L264)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L269)

### `BodyPartList`

Helper class that wraps a list of BodyPart objects with additional properties for convenience.

Supports iteration and indexing.

#### Object Methods
##### [`__init__(body_parts: list[BodyPart])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L279)

Args:

body_parts (list[BodyPart]): A list of BodyPart objects.

##### [`__iter__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L286)

Returns an iterator over the body parts.

##### [`__getitem__(index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L290)

Returns the body part at the given index.

##### [`__len__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L294)

Returns the number of body parts.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L298)

Returns a debug representation of the body part list.

#### Properties
##### [`names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L303)

Returns the internal names of each body part.

##### [`wiki_links`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L308)

Returns the internal names of each body part.

##### [`display_names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L313)

Returns the display name keys of each body part.


### `BloodLocation`

Maps a named blood location to a set of body parts.

#### Object Methods
##### [`__new__(blood_location: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L359)
##### [`__init__(blood_location: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L370)
##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L374)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L377)
#### Properties
##### [`body_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L381)

Returns a list-like wrapper of BodyPart instances for this blood location.


### `BloodLocationList`

Helper class that wraps a list of BloodLocation objects with additional properties for convenience.

Supports iteration and indexing.

#### Object Methods
##### [`__init__(locations: list[BloodLocation])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L391)

Args:

locations (list[BloodLocation]): A list of BloodLocation objects.

##### [`__iter__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L398)

Returns an iterator over the blood locations.

##### [`__getitem__(index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L402)

Returns the blood location at the given index.

##### [`__len__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L406)

Returns the number of blood locations.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L410)

Returns a debug representation of the blood location list.

#### Properties
##### [`names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L415)

Returns the names of all blood locations.

##### [`body_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L420)


[Previous Folder](../lists/body_locations_list.md) | [Next File](clothing_item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
