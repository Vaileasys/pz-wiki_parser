# Parses literature lua files

import os
from lupa import LuaRuntime
from scripts.core import utility
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


def lua_to_python(value):
    """Convert Lua data to Python dict/list/value."""
    
    # Return basic values
    if isinstance(value, (float, int, bool, str, type(None))):
        return value

    # Determine whether it's a list (array) or dict
    if type(value).__name__ == '_LuaTable':
        keys = list(value.keys())
        is_array = all(isinstance(k, int) for k in keys)
        if is_array:
            keys.sort()
            return [lua_to_python(value[k]) for k in keys]
        else:
            result = {}
            for k in keys:
                py_key = lua_to_python(k)
                py_val = lua_to_python(value[k])
                result[py_key] = py_val
            return result
    
    # Return string as a fallback
    return str(value)


def merge_dicts(base_dict, new_dict):
    """Merge each key in new_dict with base_dict."""
    for key, val in new_dict.items():
        base_dict[key] = val
    return base_dict


def parse_lua_files():
    lua = LuaRuntime(unpack_returned_tuples=True)

    VALID_KEYS = ["PrintMediaDefinitions", "SpecialLootSpawns"]

    for lua_file_name in FILES_LIST:
        lua_file_path = os.path.join(LUA_DIRECTORY, lua_file_name)

        if not os.path.exists(lua_file_path):
            print(f"Warning: {lua_file_path} does not exist. Skipping.")
            continue

        with open(lua_file_path, "r", encoding="utf-8") as f:
            lua_script = f.read()

        lua.execute(lua_script)
        globals_table = lua.globals()


        for definition in globals_table.keys():
            if definition in VALID_KEYS:
                lua_data = globals_table[definition]
                if lua_data:
                    parsed_dict = lua_to_python(lua_data)
                    if isinstance(parsed_dict, dict):
                        if definition not in parsed_data:
                            parsed_data[definition] = {}
                        merge_dicts(parsed_data[definition], parsed_dict)
                    else:
                        print(f"Warning: '{definition}' in {lua_file_name} isn't a dict. Skipping.")
    
    return parsed_data


def init():
    global parsed_data

    cache_file = os.path.join(DATA_PATH, CACHE_JSON)
    # Try to get cache from json file
    parsed_data = utility.load_cache(cache_file, "literature")

    # Parse items if there is no cache, or it's outdated.
    if not parsed_data:
        parsed_data = parse_lua_files()
        utility.save_cache(parsed_data, CACHE_JSON)


if __name__ == "__main__":
    init()