from scripts.utils.lua_helper import load_lua_file, parse_lua_tables
from scripts.core.cache import save_cache
from scripts.utils import echo

_data = {}


def get_coord(data: dict, rlink: bool = True) -> str:
    """
    Returns the coords as a wikilink or plain string based on the rlink.

    :param data (dict): A dictionary containing the coordinate data.
        - "x" (int): The X coordinate.
        - "y" (int): The Y coordinate.
        - "width" (int): The width of the area.
        - "height" (int): The height of the area.
    :param rlink (bool): If True, returns the coordinates as a wikilink. Defaults to True.
        If False, returns as a plain string. Defaults to True.
    :return (str): The formatted coordinates, either as a wikilink or a plain string.
    """
    coord_x = data.get("x", 0)
    coord_y = data.get("y", 0)
    width = data.get("width", 0)
    height = data.get("height", 0)

    centre_x = int(coord_x + (width / 2))
    centre_y = int(coord_y + (height / 2))
    coords = f"{centre_x}x{centre_y}"

    if not rlink:
        return coords
    
    return f"[https://b42map.com/?{coords} {coords}]"


def get_zone_data(key: str = None) -> dict|list:
    USE_NAME = ("ParkingStall", "ZombiesType", "ZoneStory", "Ranch", "WaterFlow", "LootZone")
    check_data()
    if key is None:
        return _data
    
    rvalue = _data.get(key)

    if not rvalue:
        echo.error(f"Couldn't find zone data for '{key}'")
        return {}

    if key not in USE_NAME:
        rvalue = _clean_name_data(rvalue)

    return rvalue


def _clean_name_data(data: dict) -> list:
    """Flatten the structure by removing the 'name' level."""
    cleaned_data = []

    for entries in data.values():
        # Each `entries` is already a list of objects
        cleaned_data.extend(entries)

    return cleaned_data


def check_data():
    """Check if _data is empty, and parse data if so."""
    if not _data:
        parse_data()
        return False
    return True


def parse_data() -> dict:
    """Load data from the Lua file and organize by type and name."""
    global _data
    lua_runtime = load_lua_file(lua_files="objects.lua", prefer="Muldraugh, KY", media_type="maps")
    parsed_data = parse_lua_tables(lua_runtime)

    objects = parsed_data.get("objects", [])
    _data = {}

    for entry in objects:
        obj_type = entry.get("type", "Unknown")
        name = entry.get("name", "Unknown")

        if obj_type not in _data:
            _data[obj_type] = {}

        _data[obj_type].setdefault(name, []).append(entry)

    save_cache(_data, "parsed_zone_data.json")
    return _data


def main():
    data = get_zone_data("ParkingStall")
    save_cache(data, "temp_data.json")

if __name__ == "__main__":
    main()
