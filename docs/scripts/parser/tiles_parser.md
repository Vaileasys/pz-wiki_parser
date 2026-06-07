[Previous Folder](../objects/animal.md) | [Previous File](stash_parser.md) | [Next File](zone_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# tiles_parser.py

This script was originally written in JavaScript by User:Jab.
It has been converted to python for use in the wiki parser.

## Functions

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L451)

## Classes

### `BufferReader`

#### Object Methods

##### [`__init__(data: bytes)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L64)

##### [`read_int32() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L68)

##### [`read_uint8() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L73)

##### [`read_string() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L78)

### `TileProperty`

#### Object Methods

##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L97)

### `TilePropertyAliasMap`

#### Class Methods

##### [`generate(prop_value_map: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L107)

##### [`get_id_from_name(name: str) -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L119)

##### [`get_name_from_id(idx: int) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L123)

##### [`get_id_from_value(prop_id: int, value: str) -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L130)

##### [`get_value_string(prop_id: int, idx: int) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L136)

### `PropertyContainer`

#### Object Methods

##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L156)

##### [`set_flag(flag: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L163)

##### [`set_property(name: str, value: str, is_flag: bool = True)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L172)

##### [`val(name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L189)

##### [`to_json() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L202)

### `IsoSprite`

#### Object Methods

##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L232)

##### [`to_json() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L260)

### `IsoSpriteManager`

#### Object Methods

##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L293)

##### [`add_sprite(name: str, id_: int) -> IsoSprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L306)

### `IsoWorld`

#### Object Methods

##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L325)

##### [`load_tile_definitions_property_strings(path: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L329)

##### [`set_custom_property_values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L347)

##### [`generate_tile_property_lookup_tables()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L356)

##### [`transform_tile_definition(spr, base, name, val)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L360)

##### [`set_open_door_properties(base, defs)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L401)

##### [`read_tile_definitions(path: str, file_num: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L422)


[Previous Folder](../objects/animal.md) | [Previous File](stash_parser.md) | [Next File](zone_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
