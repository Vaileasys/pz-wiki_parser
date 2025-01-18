# Parses literature lua files

import os
import json
from lupa import LuaRuntime

LUA_DIRECTORY = "resources/lua/"
JSON_DIR = "output/logging"
JSON_FILE = "parsed_literature_data.json"

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
    global parsed_data
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


def init():
    global parsed_data
    lua = LuaRuntime(unpack_returned_tuples=True)
    os.makedirs(JSON_DIR, exist_ok=True)

    printmedia_dict = {}
    specialloot_dict = {}

    for lua_file_name in FILES_LIST:
        lua_file_path = os.path.join(LUA_DIRECTORY, lua_file_name)

        if not os.path.exists(lua_file_path):
            print(f"Warning: {lua_file_path} does not exist. Skipping.")
            continue

        with open(lua_file_path, "r", encoding="utf-8") as f:
            lua_script = f.read()

        lua.execute(lua_script)
        globals_table = lua.globals()

        # Check if this file is for PrintMediaDefinitions
        if "PrintMediaDefinitions" in globals_table.keys():
            print_media_dict = globals_table["PrintMediaDefinitions"]
        else:
            print_media_dict = None
        if print_media_dict:
            parsed_pm = lua_to_python(print_media_dict)
            if isinstance(parsed_pm, dict):
                merge_dicts(printmedia_dict, parsed_pm)
            else:
                print(f"Warning: 'PrintMediaDefinitions' in {lua_file_name} isn't a dict. Skipped.")

        # Check if this file is for SpecialLootSpawns
        if "SpecialLootSpawns" in globals_table.keys():
            special_loot_dict = globals_table["SpecialLootSpawns"]
        else:
            special_loot_dict = None
        if special_loot_dict:
            parsed_sl = lua_to_python(special_loot_dict)
            if isinstance(parsed_sl, dict):
                merge_dicts(specialloot_dict, parsed_sl)
            else:
                print(f"Warning: 'SpecialLootSpawns' in {lua_file_name} isn't a dict. Skipped.")

    parsed_data = {
        "PrintMediaDefinitions": printmedia_dict,
        "SpecialLootSpawns": specialloot_dict
    }

    # Dump to JSON
    json_file_path = os.path.join(JSON_DIR, JSON_FILE)
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(parsed_data, json_file, indent=4)
        print(f"Data dumped to JSON file: {json_file_path}")


if __name__ == "__main__":
    init()