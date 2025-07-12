[Previous Folder](../lists/attachment_list.md) | [Previous File](attachment.md) | [Next File](clothing_item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

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
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L182)
##### [`group`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L188)
##### [`alias`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L192)
##### [`multi_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L196)
##### [`exclusive`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L200)
##### [`hide_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L204)
##### [`alt_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L208)
##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L212)

### `BodyPart`

Static reference for body part display names.

#### Object Methods
##### [`__new__(body_part_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L241)
##### [`__init__(body_part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L252)
##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L255)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L258)
#### Properties
##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L262)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L265)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L270)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L275)

### `BodyPartList`

Helper class that wraps a list of BodyPart objects with additional properties for convenience.

Supports iteration and indexing.

#### Object Methods
##### [`__init__(body_parts: list[BodyPart])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L285)

Args:

body_parts (list[BodyPart]): A list of BodyPart objects.

##### [`__iter__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L292)

Returns an iterator over the body parts.

##### [`__getitem__(index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L296)

Returns the body part at the given index.

##### [`__len__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L300)

Returns the number of body parts.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L304)

Returns a debug representation of the body part list.

#### Properties
##### [`body_part_ids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L309)

Returns the internal names of each body part.

##### [`names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L314)

Returns the translated names of each body part.

##### [`wiki_links`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L319)

Returns the internal names of each body part.

##### [`display_names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L324)

Returns the display name keys of each body part.


### `BloodLocation`

Maps a named blood location to a set of body parts.

#### Class Methods
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L392)
#### Object Methods
##### [`__new__(blood_location: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L370)
##### [`__init__(blood_location: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L381)
##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L385)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L388)
#### Properties
##### [`body_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L396)

Returns a list-like wrapper of BodyPart instances for this blood location.


### `BloodLocationList`

Helper class that wraps a list of BloodLocation objects with additional properties for convenience.

Supports iteration and indexing.

#### Object Methods
##### [`__init__(locations: list[BloodLocation])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L406)

Args:

locations (list[BloodLocation]): A list of BloodLocation objects.

##### [`__iter__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L413)

Returns an iterator over the blood locations.

##### [`__getitem__(index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L417)

Returns the blood location at the given index.

##### [`__len__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L421)

Returns the number of blood locations.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L425)

Returns a debug representation of the blood location list.

#### Properties
##### [`names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L430)

Returns the names of all blood locations.

##### [`body_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/body_location.py#L435)


[Previous Folder](../lists/attachment_list.md) | [Previous File](attachment.md) | [Next File](clothing_item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
