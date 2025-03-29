from lupa import LuaRuntime
from scripts.core import version
from scripts.utils import utility, lua_helper

# TODO: merge with distribution_parser.py

CACHE_JSON = "distributions_2.json"
LUA_FILE = "Distributions.lua"

parsed_data = {}


def get_distribution_data():
    if parsed_data == {}:
        init()
    return parsed_data

def convert_list_to_dict(data):
    """Converts lists with alternating key-value pairs into dicts.
    E.g. ["Apple", 8, "Banana", 10] -> {"Apple": 8, "Banana": 10}
    """
    if isinstance(data, list):
        # Check if it can be converted to a dict
        if len(data) % 2 == 0 and all(isinstance(data[i], str) for i in range(0, len(data), 2)):
            # Convert to dict
            return {data[i]: data[i + 1] for i in range(0, len(data), 2)}
        else:
            # Process nested lists
            return [convert_list_to_dict(item) for item in data]
    elif isinstance(data, dict):
        # Process dict values
        return {key: convert_list_to_dict(value) for key, value in data.items()}
    return data


def sort_proc_list(item):
    """Sorts keys within procList."""
    PROCLIST_ORDER = ["name", "min", "max", "weightChance", "forceForTiles"]
    if not isinstance(item, dict):
        return item

    ordered_keys = [key for key in PROCLIST_ORDER if key in item]
    remaining_keys = [key for key in item if key not in PROCLIST_ORDER]

    sorted_keys = ordered_keys + remaining_keys
    return {key: sort_keys(item[key]) for key in sorted_keys}


def sort_keys(data, is_top_level=False):
    """
    Sorts data:
    - Top-level: lowercase first keys are first, then uppercase, with each group sorted alphabetically.
    - Nested: boolean keys first.
    - Special case for procList items.
    """
    if isinstance(data, dict):
        keys = list(data.keys())

        if is_top_level:
            # Top-level: lowercase first, then uppercase, both alphabetically
            sorted_keys = sorted(keys, key=lambda k: (k[0].isupper(), k.lower()))
        else:
            # Nested: boolean keys first, others in original order
            boolean_keys = [k for k in keys if isinstance(data[k], bool)]
            other_keys = [k for k in keys if k not in boolean_keys]

            sorted_keys = boolean_keys + other_keys

        # Apply sorting
        sorted_data = {}
        for key in sorted_keys:
            if key == "procList" and isinstance(data[key], list):
                # Apply special procList sorting
                sorted_data[key] = [sort_proc_list(item) for item in data[key]]
            else:
                sorted_data[key] = sort_keys(data[key])

        return sorted_data

    elif isinstance(data, list):
        return [sort_keys(item) for item in data]

    return data


def init():
    global parsed_data

    # Update parsed data if it's empty
    if not parsed_data:
        cached_data, cache_version = utility.load_cache(CACHE_JSON, get_version=True)

        # Check if cache is outdated
        if cache_version != version.get_version():
            CLUTTER_FILES = [
                "Distribution_BagsAndContainers.lua",
                "Distribution_BinJunk.lua",
                "Distribution_ShelfJunk.lua",
                "Distribution_ClosetJunk.lua",
                "Distribution_CounterJunk.lua",
                "Distribution_DeskJunk.lua",
                "Distribution_SideTableJunk.lua",
                "ProceduralDistributions.lua"
            ]

            lua_runtime = lua_helper.load_lua_file(LUA_FILE, dependencies=CLUTTER_FILES)
            parsed_data = lua_helper.parse_lua_tables(lua_runtime)
#            parsed_data = convert_list_to_dict(parsed_data)
            parsed_data = sort_keys(parsed_data, is_top_level=True) # Sort keys for readability in json file
            utility.save_cache(parsed_data, CACHE_JSON)
        else:
            parsed_data = cached_data


if __name__ == "__main__":
    init()
