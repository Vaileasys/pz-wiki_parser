[Previous Folder](../navbox/navbox.md) | [Previous File](animal_gene.md) | [Next File](attachment.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# animal_part.py

## Classes

### `AnimalPart`

#### Class Methods

##### [`_parse()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L69)

##### [`load(attribute: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L88)

Loads animal part data from the cache, re-parsing the Lua file if outdated.

<ins>**Args:**</ins>
  - **attribute (str, optional)**:
      - _The name of a specific class attribute to return,_
  - **such as "_meat_data" or "_animals_data".**:

<ins>**Returns:**</ins>
  - **dict**:
      - _The full animal data by default, or the specified attribute if provided._

##### [`all() -> dict[str, 'AnimalPart']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L119)

Returns all known animal part instances.

<ins>**Returns:**</ins>
  - **dict[str, AnimalPart]**:
      - _Mapping of breed ID to animal part instance._

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L131)

Returns the total number of Animal types parsed.

<ins>**Returns:**</ins>
  - **int**:
      - _Number of unique Animal types._

##### [`exists(animal_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L143)

Checks if a Animal with the given id exists in the parsed data.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if found, False otherwise._

##### [`get_breeds(item_id: str) -> 'list[AnimalBreed]'`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L155)

#### Static Methods

##### [`_convert_meat_variants(raw_data: dict, prefix: str = 'IGUI_AnimalMeat_') -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L43)

Convert variants list to dict using 'extraName' with prefix stripped as keys.

##### [`_split_commas(obj)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L58)

Recursively split strings with commas into lists.

#### Object Methods

##### [`__new__(parts_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L19)

Ensures only one part instance exists per parts ID.

##### [`__init__(parts_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L31)

Initialise the part instance with its data if not already initialised.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L163)

Returns a raw value from the animal part data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Key to look up._
  - **default**:
      - _Value to return if key is missing._

<ins>**Returns:**</ins>
  - **Any**:
      - _Value from the raw data or default._

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L263)

#### Properties

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L177)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L181)

##### [`skull`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L185)

##### [`leather`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L191)

##### [`head`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L197)

##### [`parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L203)

##### [`part_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L207)

##### [`bones`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L215)

##### [`bone_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L219)

##### [`no_skeleton`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L227)

##### [`all_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L231)

##### [`animal`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L247)

##### [`breed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L258)

### `AnimalMeat`

#### Class Methods

##### [`all() -> dict[str, 'AnimalPart']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L289)

Returns all known meat instances.

<ins>**Returns:**</ins>
  - **dict[str, AnimalMeat]**:
      - _Mapping of meat to animal part instance._

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L299)

Returns the total number of Animal types parsed.

<ins>**Returns:**</ins>
  - **int**:
      - _Number of unique Animal types._

##### [`exists(animal_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L309)

Checks if a Animal with the given id exists in the parsed data.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if found, False otherwise._

#### Object Methods

##### [`__new__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L271)

Ensures only one meat instance exists per item ID.

##### [`__init__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L280)

Initialise the meat instance with its data if not already initialised.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L318)

Returns a raw value from the animal part data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Key to look up._
  - **default**:
      - _Value to return if key is missing._

<ins>**Returns:**</ins>
  - **Any**:
      - _Value from the raw data or default._

##### [`get_display_name(cut: 'AnimalMeatVariant') -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L331)

Returns the display name for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'

##### [`get_base_name(cut: 'AnimalMeatVariant') -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L335)

Returns the base name for a specific cut, translating it. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'

##### [`get_extra_name(cut: 'AnimalMeatVariant') -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L339)

Returns the extra name for a specific cut, translating it. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'

##### [`get_link(cut: 'AnimalMeatVariant') -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L343)

Returns the wiki link for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'

##### [`get_base_chance(cut: 'AnimalMeatVariant') -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L347)

Returns the base chance for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'

##### [`get_hunger_boost(cut: 'AnimalMeatVariant') -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L351)

Returns the hunger boost for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'

##### [`get_hunger(cut: 'AnimalMeatVariant') -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L355)

Returns the base hunger for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L418)

#### Properties

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L361)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L363)

##### [`variants`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L365)

##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L372)

##### [`name_prime`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L377)

##### [`name_medium`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L379)

##### [`name_poor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L381)

##### [`base_name_prime`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L384)

##### [`base_name_medium`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L386)

##### [`base_name_poor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L388)

##### [`extra_name_prime`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L391)

##### [`extra_name_medium`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L393)

##### [`extra_name_poor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L395)

##### [`hunger_prime`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L400)

##### [`hunger_medium`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L402)

##### [`hunger_poor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L404)

##### [`animals`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L407)

### `AnimalMeatVariant`

#### Object Methods

##### [`__init__(cut_type: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L423)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L447)

#### Properties

##### [`base_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L428)

##### [`extra_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L430)

##### [`hunger_boost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L432)

##### [`base_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L434)

##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L436)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L440)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_part.py#L444)


[Previous Folder](../navbox/navbox.md) | [Previous File](animal_gene.md) | [Next File](attachment.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
