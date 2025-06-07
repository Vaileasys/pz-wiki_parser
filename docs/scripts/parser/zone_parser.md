[Previous Folder](../objects/body_location.md) | [Previous File](tiles_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# zone_parser.py

## Functions

### [`get_coord(data: dict, rlink: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/zone_parser.py#L8)

Returns the coords as a wikilink or plain string based on the rlink.

:param data (dict): A dictionary containing the coordinate data.
- "x" (int): The X coordinate.
- "y" (int): The Y coordinate.
- "width" (int): The width of the area.
- "height" (int): The height of the area.
:param rlink (bool): If True, returns the coordinates as a wikilink. Defaults to True.
If False, returns as a plain string. Defaults to True.
:return (str): The formatted coordinates, either as a wikilink or a plain string.

### [`get_zone_data(key: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/zone_parser.py#L36)
### [`_clean_name_data(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/zone_parser.py#L54)

Flatten the structure by removing the 'name' level.

### [`check_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/zone_parser.py#L65)

Check if _data is empty, and parse data if so.

### [`parse_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/zone_parser.py#L73)

Load data from the Lua file and organize by type and name.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/zone_parser.py#L95)


[Previous Folder](../objects/body_location.md) | [Previous File](tiles_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
