[Previous Folder](../navbox/navbox.md) | [Previous File](vehicle_part.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# zone.py

## Classes

### `Zone`

Handle zone data as one class:
- Zone._parse() builds { zone_type: { name: [entries...] } }
- Zone.load() loads from cache (re-parse if version mismatch)
- Zone(zone_type) -> a handle for that type (returns nested dict)
- Zone(zone_type, name) -> a handle for that name group (returns list)

#### Class Methods

##### [`_parse()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L50)

Parse objects.lua -> nested dict, then save cache.

##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L75)

Load from cache, re-parse if version mismatch.

##### [`types()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L90)

List available zone types.

##### [`names_for(zone_type, include_empty = True)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L97)

List name groups for a given zone type.

##### [`exists(zone_type, name = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L108)

#### Static Methods

##### [`coord(data: dict[str, int], rlink = True)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L152)

Return centre coords as wikilink or plain string.

#### Object Methods

##### [`__new__(zone_type, name = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L21)

##### [`__init__(zone_type, name = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L31)

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L116)

If self.name is None -> return nested dict {name: [entries...]} for the zone type.
If self.name is set  -> return the list of entries for that group.

##### [`flat()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L123)

Flatten to a single list (only meaningful for type handles).

##### [`dump(filename = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L133)

Dump to JSON file.

### `RanchZone`

Represents a single ranch zone entry.

#### Class Methods

##### [`_parse()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L200)

Parses RanchZoneDefinitions.lua to extract ranch zone data and caches it.

##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L215)

Loads RanchZone data from the cache, re-parsing the Lua file if the data is outdated.

<ins>**Returns:**</ins>
  - **dict**:
      - _Raw RanchZone data._

##### [`all() -> dict[str, 'RanchZone']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L238)

Returns all known RanchZone instances.

<ins>**Returns:**</ins>
  - **dict[str, RanchZone]**:
      - _Mapping of item ID to RanchZone instance._

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L250)

Returns the total number of RanchZone types parsed.

<ins>**Returns:**</ins>
  - **int**:
      - _Number of unique RanchZone types._

##### [`exists(id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L262)

Checks if a RanchZone with the given id exists in the parsed data.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if found, False otherwise._

##### [`animal_index() -> dict[str, list[str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L274)

Return a mapping of all maleType and femaleType values to the list of corresponding ranch zones.

#### Object Methods

##### [`__new__(id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L174)

Ensures only one RanchZone instance exists per RanchZone ID.

##### [`__init__(id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L186)

Initialises RanchZone instance if not already initialised.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L340)

Returns a raw value from the RanchZone data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Key to look up._
  - **default**:
      - _Value to return if key is missing._

<ins>**Returns:**</ins>
  - **Any**:
      - _Value from the raw data or default._

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L413)

#### Properties

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L354)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L358)

##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L362)

##### [`possible_def`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L366)

##### [`def_list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L370)

##### [`global_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L374)

##### [`chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L378)

##### [`female_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L382)

##### [`male_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L385)

##### [`min_female_nb`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L389)

##### [`max_female_nb`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L392)

##### [`min_male_nb`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L395)

##### [`max_male_nb`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L398)

##### [`forced_breed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L402)

##### [`chance_for_baby`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L406)

##### [`male_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/zone.py#L410)


[Previous Folder](../navbox/navbox.md) | [Previous File](vehicle_part.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
