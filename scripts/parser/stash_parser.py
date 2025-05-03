import os
from lupa import LuaRuntime
from scripts.core.version import Version
from scripts.core.constants import DATA_DIR
from scripts.core.cache import save_cache, load_cache

STASH_DIRECTORY = os.path.join("resources", "lua", "stashes")
CACHE_JSON = "stash_data.json"

stash_data = {}

def get_stash_data():
    global stash_data
    if not stash_data:
        init()
    return stash_data


def parse_lua_stash(file_path):
    """Parse lua stash file, returning it as a dicitonary."""
    stash_dict = {}

    lua = LuaRuntime(unpack_returned_tuples=True)

    # Mocks require function to prevent missing module errors
    def mock_require(module_name):
        return None

    # Method to create a new stash entry
    def newStash(id, item_type, item_id, custom_name):
        stash = {
            "type": item_type,
            "item": item_id,
            "customName": custom_name,
            "zombies": 0,
            "barricades": 0,
            "buildingX": 0,
            "buildingY": 0,
            "spawnTable": "",
            "spawnOnlyOnZed": False,
            "containers": [],
            "stamps": []
        }

        # Methods in the stash object for Lua compatibility
        def addContainer(*args):
            args = list(args) + [None] * (8 - len(args))
            _, container_type, sprite, item, room, x, y, z = args[:8]
            stash["containers"].append({
                "containerType": container_type,
                "containerSprite": sprite,
                "containerItem": item,
                "room": room,
                "x": x,
                "y": y,
                "z": z
            })

        def addStamp(*args):
            args = list(args) + [None] * (8 - len(args))
            _, symbol, text, x, y, r, g, b = args[:8]
            stash["stamps"].append({
                "symbol": symbol,
                "text": text,
                "mapX": x,
                "mapY": y,
                "r": r,
                "g": g,
                "b": b
            })

        # Add methods to the dict so lua can call them
        stash["addContainer"] = addContainer
        stash["addStamp"] = addStamp

        stash_dict[id] = stash
        return stash

    # Inject functions into Lua environment
    lua.globals().require = mock_require
    lua.globals().StashUtil = {"newStash": newStash}

    # Read and execute the Lua script
    with open(file_path, 'r') as file:
        lua_code = file.read()
        lua.execute(lua_code)

    return remove_functions(stash_dict)


def remove_functions(data):
    """Removes functions from the dictionary."""
    if isinstance(data, dict):
        return {k: remove_functions(v) for k, v in data.items() if not callable(v)}
    elif isinstance(data, list):
        return [remove_functions(v) for v in data]
    return data


def parse_all_stash_files(directory):
    """Parse all lua stash files, returning them as a dictionary, separated by file name."""
    global stash_data

    cache_file = os.path.join(DATA_DIR, CACHE_JSON)
    # Try to get cache from json file
    stash_data, cache_version = load_cache(cache_file, "stash", get_version=True)

    # Parse stash if there is no cache, or it's outdated.
    if cache_version != Version.get():
        for filename in os.listdir(directory):
            if filename.endswith(".lua"):
                file_path = os.path.join(directory, filename)
                file_key = os.path.splitext(filename)[0]
                stashes = parse_lua_stash(file_path)
                stash_data[file_key] = stashes

        save_cache(stash_data, CACHE_JSON)


def init():
    """Initialise script"""
    parse_all_stash_files(STASH_DIRECTORY)


if __name__ == "__main__":
    init()
