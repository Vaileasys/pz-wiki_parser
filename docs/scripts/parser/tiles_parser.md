[Previous Folder](../objects/attachment.md) | [Previous File](stash_parser.md) | [Next File](zone_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# tiles_parser.py

This script was originally written in JavaScript by User:Jab.
It has been converted to python for use in the wiki parser.

## Functions

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L450)

## Classes

### `BufferReader`
#### Object Methods
##### [`__init__(data: bytes)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L63)
##### [`read_int32()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L67)
##### [`read_uint8()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L72)
##### [`read_string()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L77)

### `TileProperty`
#### Object Methods
##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L96)

### `TilePropertyAliasMap`
#### Class Methods
##### [`generate(prop_value_map: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L106)
##### [`get_id_from_name(name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L118)
##### [`get_name_from_id(idx: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L122)
##### [`get_id_from_value(prop_id: int, value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L129)
##### [`get_value_string(prop_id: int, idx: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L135)

### `PropertyContainer`
#### Object Methods
##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L155)
##### [`set_flag(flag: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L162)
##### [`set_property(name: str, value: str, is_flag: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L171)
##### [`val(name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L188)
##### [`to_json()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L201)

### `IsoSprite`
#### Object Methods
##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L231)
##### [`to_json()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L259)

### `IsoSpriteManager`
#### Object Methods
##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L292)
##### [`add_sprite(name: str, id_: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L305)

### `IsoWorld`
#### Object Methods
##### [`__init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L324)
##### [`load_tile_definitions_property_strings(path: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L328)
##### [`set_custom_property_values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L346)
##### [`generate_tile_property_lookup_tables()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L355)
##### [`transform_tile_definition(spr, base, name, val)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L359)
##### [`set_open_door_properties(base, defs)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L400)
##### [`read_tile_definitions(path: str, file_num: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/tiles_parser.py#L421)


[Previous Folder](../objects/attachment.md) | [Previous File](stash_parser.md) | [Next File](zone_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
