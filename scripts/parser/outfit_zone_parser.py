"""
Parses outfit zombie zone definitions from ZombiesZoneDefinition.lua.

Loads and caches ZombiesZoneDefinition data used to determine which zombie zones
can spawn specific outfits.
"""

import os

from lupa import LuaRuntime, LuaError

from scripts.core.constants import CACHE_DIR
from scripts.core.file_loading import get_lua_dir, read_file
from scripts.utils import echo
from scripts.utils.lua_helper import parse_lua_tables, save_cache


def parse_outfit_zones(force_regenerate: bool = False) -> dict:
    """
    Parse outfit zombie zone definitions.

    Args:
        force_regenerate: Reparse the Lua file instead of using cache.
    """
    cache_file = os.path.join(CACHE_DIR, "zone_definitions.json")

    if not force_regenerate and os.path.exists(cache_file):
        echo.info("Loading zone definitions from cache...")

        try:
            import json

            with open(cache_file, "r", encoding="utf-8") as f:
                cached_data = json.load(f)

            echo.success("Loaded cached zone definitions data")
            return cached_data
        except Exception as e:
            echo.warning(f"Failed to load cache, regenerating: {e}")

    echo.info("Loading ZombiesZoneDefinition.lua file...")

    lua_dir = get_lua_dir()
    zone_file_path = os.path.join(
        lua_dir,
        "shared",
        "npcs",
        "ZombiesZoneDefinition.lua",
    )

    if not os.path.exists(zone_file_path):
        echo.error(f"ZombiesZoneDefinition.lua not found at {zone_file_path}")
        return {}

    lua_runtime = LuaRuntime(unpack_returned_tuples=True)
    lua_path = os.path.normpath(get_lua_dir()).replace(os.sep, "/")

    extra_paths = [
        f"{lua_path}/?.lua",
        f"{lua_path}/shared/?.lua",
        f"{lua_path}/client/?.lua",
        f"{lua_path}/server/?.lua",
    ]

    lua_runtime.execute(
        "package.path = package.path .. ';" + ";".join(extra_paths) + "'"
    )

    lua_content = read_file(zone_file_path)

    try:
        lua_runtime.execute(lua_content)
    except LuaError as e:
        echo.error(f"Failed to execute Lua file {zone_file_path}: {e}")
        return {}

    try:
        parsed_data = parse_lua_tables(
            lua_runtime,
            tables=["ZombiesZoneDefinition"],
        )
    except LuaError as e:
        echo.warning(f"Failed to parse ZombiesZoneDefinition table: {e}")
        parsed_data = {}

    try:
        all_tables = parse_lua_tables(lua_runtime)
    except LuaError as e:
        echo.warning(f"Failed to parse all tables: {e}")
        all_tables = {}

    if "ZombiesZoneDefinition" not in parsed_data and all_tables:
        echo.warning(
            "ZombiesZoneDefinition not found in globals, available tables: "
            + ", ".join(all_tables.keys())
        )
        parsed_data = all_tables

    echo.success(f"Parsed {len(parsed_data)} zone definition tables")

    try:
        save_cache(parsed_data, "zone_definitions.json")
        echo.success(f"Saved zone definitions data to cache: {cache_file}")
    except Exception as e:
        echo.error(f"Failed to save cache: {e}")

    return parsed_data