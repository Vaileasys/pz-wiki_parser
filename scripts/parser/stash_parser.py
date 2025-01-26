import os
import json
from lupa import LuaRuntime

STASH_DIRECTORY = "resources/lua/stashes"

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
    all_stashes = {}

    for filename in os.listdir(directory):
        if filename.endswith(".lua"):
            file_path = os.path.join(directory, filename)
            file_key = os.path.splitext(filename)[0]
            stashes = parse_lua_stash(file_path)
            all_stashes[file_key] = stashes

    return all_stashes


def dump_to_json(data):
    """Dump data to JSON for debugging."""
    output_file = "output/logging/parsed_stash_data.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data dumped to JSON file '{output_file}'")


def init():
    """Initialise script, replacing 'stash_data' dictionary"""
    global stash_data
    stash_data = parse_all_stash_files(STASH_DIRECTORY)
    dump_to_json(stash_data)


if __name__ == "__main__":
    init()
