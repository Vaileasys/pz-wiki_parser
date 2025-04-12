# Parses literature lua files

import os
from scripts.core.version import Version
from scripts.core.constants import DATA_PATH
from scripts.utils import lua_helper
from scripts.core.cache import save_cache, load_cache

CACHE_JSON = "literature_data.json"

FILES_LIST = [
    'SpecialItemData_Books.lua',
    'SpecialItemData_Comics.lua',
    'SpecialItemData_Magazines.lua',
    'SpecialItemData_Misc.lua',
    'SpecialItemData_Photos.lua',
    'PrintMediaDefinitions.lua'
]

parsed_data = {}

def get_literature_data():
    if parsed_data == {}:
        init()
    return parsed_data


def parse_lua_files():
    LUA_TABLES = ["SpecialLootSpawns", "PrintMediaDefinitions"]
    parsed_data = {}

    # Initialise and load files into lua runtime environment
    lua_runtime = lua_helper.load_lua_file(FILES_LIST)

    # Parse lua tables and convert to python data
    parsed_data = lua_helper.parse_lua_tables(lua_runtime, tables=LUA_TABLES)
    
    return parsed_data


def init():
    global parsed_data

    cache_file = os.path.join(DATA_PATH, CACHE_JSON)
    # Try to get cache from json file
    parsed_data, cache_version = load_cache(cache_file, "literature", get_version=True)

    # Parse items if there is no cache, or it's outdated.
    if cache_version != Version.get():
        parsed_data = parse_lua_files()
        save_cache(parsed_data, CACHE_JSON)


if __name__ == "__main__":
    init()