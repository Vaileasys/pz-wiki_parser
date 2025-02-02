# Parses literature lua files

import os
from lupa import LuaRuntime, LuaError
from scripts.core import utility, version, lua_helper
from scripts.core.constants import DATA_PATH

LUA_DIRECTORY = "resources/lua/"
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
    lua = LuaRuntime(unpack_returned_tuples=True)
    VALID_KEYS = ["PrintMediaDefinitions", "SpecialLootSpawns"]
    parsed_data = {}

    for lua_file_name in FILES_LIST:
        lua_file_path = os.path.join(LUA_DIRECTORY, lua_file_name)

        if not os.path.exists(lua_file_path):
            print(f"Warning: {lua_file_path} does not exist. Skipping.")
            continue

        try:
            lua = lua_helper.load_lua_file(lua, lua_file_path)
        except (FileNotFoundError, LuaError) as e:
            print(f"Error processing {lua_file_name}: {e}")
            continue

        globals_table = lua.globals()


        for definition in globals_table.keys():
            if definition in VALID_KEYS:
                lua_data = globals_table[definition]
                if lua_data:
                    parsed_dict = lua_helper.lua_to_python(lua_data)
                    if isinstance(parsed_dict, dict):
                        if definition not in parsed_data:
                            parsed_data[definition] = {}
                        # Merge dictionaries
                        parsed_data[definition] = {**parsed_data[definition], **parsed_dict}
                    else:
                        print(f"Warning: '{definition}' in {lua_file_name} isn't a dict. Skipping.")
    
    return parsed_data


def init():
    global parsed_data

    cache_file = os.path.join(DATA_PATH, CACHE_JSON)
    # Try to get cache from json file
    parsed_data, cache_version = utility.load_cache(cache_file, "literature", get_version=True)

    # Parse items if there is no cache, or it's outdated.
    if cache_version != version.get_version():
        parsed_data = parse_lua_files()
        utility.save_cache(parsed_data, CACHE_JSON)


if __name__ == "__main__":
    init()