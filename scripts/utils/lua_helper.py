import os
from lupa import LuaRuntime, LuaError
from scripts.utils.util import save_cache
from scripts.core.constants import LUA_PATH

def load_lua_file(lua_files: list[str], lua_runtime: LuaRuntime=None, dependencies: list[str]=None, inject_lua: str=None) -> LuaRuntime:
    """
    Loads and executes a Lua file in the given Lua runtime.

    :param lua_files (str or list[str]): List of Lua file paths to load and execute. A single file path can also be provided as a string.
    :param lua_runtime (LuaRuntime, optional): An existing Lua runtime instance. If not provided, a new Lua runtime will be initialised.
    :param dependencies (list[str], optional): List of additional Lua dependency files to load before the main files (LUA_PATH is already included).
    :param inject_lua (str, optional): Lua code to inject directly into the runtime before executing any files. Useful for adding stubs or fallbacks.
    :return (LuaRuntime): The Lua runtime after executing the files.
    """

    def get_lua_files(paths):
        """Returns a list of Lua files from given paths, including subdirectories if paths are directories.

        :param paths (str or list[str]): The path to get all files from.
        :return (list[str]): List of lua file paths.
        """
        files_list = []

        # Ensure paths is a list
        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            path = os.path.join(LUA_PATH, path)
            try:
                # Is directory
                if os.path.isdir(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.endswith('.lua'):
                                full_path = os.path.join(root, file)
                                files_list.append(full_path)
                # Is lua file
                elif os.path.isfile(path) and path.endswith('.lua'):
                    files_list.append(path)
                else:
                    print(f"Warning: {path} is not a valid lua file or directory.")
            except (PermissionError, FileNotFoundError) as e:
                print(f"Error accessing {path}: {e}")

        return files_list

    # Initialise new Lua runtime environment if one wasn't provided
    if not lua_runtime:
        lua_runtime = LuaRuntime(unpack_returned_tuples=True)

    # Inject Lua into the runtime environemnt. Can be used for fallbacks, such as creating stubs.
    if inject_lua:
        if isinstance(inject_lua, list):
            inject_lua = "\n\n".join(inject_lua)
        lua_runtime.execute(inject_lua)

    try:
        # Load dependencies
        if dependencies:
            dependency_files = get_lua_files(dependencies)
            for dependency_path in dependency_files:
                with open(dependency_path, 'r', encoding='utf-8') as f:
                    try:
                        lua_runtime.execute(f.read())
                    except LuaError as e:
                        raise LuaError(f"Error executing dependency '{dependency_path}': {e}")
        
        # Load main lua files
        lua_files_list = get_lua_files(lua_files)
        for lua_file_path in lua_files_list:
            with open(lua_file_path, 'r', encoding='utf-8') as lua_file:
                try:
                    lua_runtime.execute(lua_file.read())
                except LuaError as e:
                    raise LuaError(f"Error executing main Lua file '{lua_file_path}': {e}")

    except (FileNotFoundError, IOError, LuaError) as e:
        print(f"Error: {e}")
        raise

    return lua_runtime


def lua_to_python(lua_data: object) -> object:
    """
    Converts Lua data to its Python equivalent (dict, list, or basic value).

    :param lua_data: The Lua data to convert. Can be a basic type (int, float, bool, str, None), Lua table (converted to Python dict or list), or a Lua function (converted to a string).
    :return: The corresponding Python data structure (dict, list, basic type, or string).
    """
    try:
        # Return basic values
        if isinstance(lua_data, (float, int, bool, str, type(None))):
            return lua_data

        # Determine whether it's a list (array) or dict (table)
        if type(lua_data).__name__ == '_LuaTable':
            keys = list(lua_data.keys())
            is_array = all(isinstance(k, int) for k in keys)

            if is_array:
                return [lua_to_python(lua_data[k]) for k in keys]
            else:
                # Move lua functions to the bottom of the data
                regular_items = {}
                function_items = {}

                for k in keys:
                    value = lua_data[k]
                    python_key = lua_to_python(k)

                    if type(value).__name__ == '_LuaFunction':
                        function_items[python_key] = str(value)
                    else:
                        regular_items[python_key] = lua_to_python(value)

                # Merge dicts, adding regular items first
                return {**regular_items, **function_items}

        # Return string as a fallback
        return str(lua_data)

    except KeyError as e:
        raise KeyError(f"Invalid key encountered in Lua table: {e}")
    except LuaError as e:
        raise LuaError(f"Lua execution error while accessing data: {e}")
    except Exception as e:
        raise TypeError(f"Unsupported data type encountered: {e}")


def parse_lua_tables(lua_runtime: LuaRuntime, tables: list[str] = None) -> dict:
    """
    Parses Lua tables from the provided Lua runtime and converts them into Python data structures.

    :param lua_runtime: The initialised Lua runtime environment containing the Lua code to parse.
    :param tables: List of Lua table names to extract. If None, all global tables (excluding standard Lua libraries) will be extracted.
    :return: Dictionary containing extracted tables with their Python data representations.
    """
    parsed_data = {}
    globals_dict = lua_runtime.globals()

    STANDARD_LUA_LIBS = {
        "math", "os", "io", "string", "table", "debug", "coroutine", "package", "utf8", "python", "_G"
    }

    if tables:
        if isinstance(tables, str):
            tables = [tables]

        for table_name in tables:
            try:
                lua_table = lua_runtime.eval(table_name)
                parsed_data[table_name] = lua_to_python(lua_table)
            except LuaError:
                print(f"Warning: Table '{table_name}' not found.")
    else:
        for key, value in globals_dict.items():
            if key not in STANDARD_LUA_LIBS and type(value).__name__ == '_LuaTable':
                parsed_data[key] = lua_to_python(value)

    return parsed_data


## ------------------------- EVERYTHING BENEATH HERE IS FOR TESTING/EXAMPLE ------------------------- ##


LUA_CLUTTER_TABLES = ("""
    ClutterTables = ClutterTables or setmetatable({}, {
        __index = function(_, key)
            return setmetatable({}, {
                __index = function(_, inner_key)
                    return function() return tostring(inner_key) end
                end
            })
        end
    })
""")
LUA_BAGS_AND_CONTAINERS = ("""
    BagsAndContainers = BagsAndContainers or setmetatable({}, {
        __index = function(_, key)
            return setmetatable({}, {
                __index = function(_, inner_key)
                    return function() return tostring(inner_key) end
                end
            })
        end
    })
""")
LUA_EVENTS = ("""
    local function fallback()
        return setmetatable({}, {
            __index = function(_, key)
                return function() return tostring(key) end
            end
        })
    end

    Events = Events or {}

    setmetatable(Events, {
        __index = function(_, key)
            return fallback()
        end
    })

    setmetatable(_G, {
        __index = function(_, key)
            return fallback()
        end
    })
""")
# Inject lua: Foraging - initialises and stubs Events table
if __name__ == "__main__":
    lua_runtime = load_lua_file("forageSystem.lua", inject_lua=LUA_EVENTS)
    parsed_data = parse_lua_tables(lua_runtime)
    save_cache(parsed_data, "foraging_2.json")

# Basic usage: Recorded media
if __name__ == "__main__":
    lua_runtime = load_lua_file("recorded_media.lua")
    parsed_data = parse_lua_tables(lua_runtime)
    save_cache(parsed_data, "recorded_media.json")

# Basic usage: Burn time
if __name__ == "__main__":
    lua_runtime = load_lua_file("camping_fuel.lua")
    parsed_data = parse_lua_tables(lua_runtime)
    save_cache(parsed_data, "camping_fuel.json")

# Basic usage: Attached weapon definitions
if __name__ == "__main__":
    lua_runtime = load_lua_file("AttachedWeaponDefinitions.lua")
    parsed_data = parse_lua_tables(lua_runtime)
    save_cache(parsed_data, "attached_weapon_definitions.json")

# Inject lua and multiple files: All distributions - initialises ClutterTables and BagsAndContainers tables
DISTRIBUTION_LUA_FILES = [
    "Distribution_BagsAndContainers.lua",
    "Distribution_BinJunk.lua",
    "Distribution_ClosetJunk.lua",
    "Distribution_CounterJunk.lua",
    "Distribution_DeskJunk.lua",
    "Distribution_ShelfJunk.lua",
    "Distribution_SideTableJunk.lua",
    "ProceduralDistributions.lua",
    "Distributions.lua",
]
if __name__ == "__main__":
    lua_runtime = load_lua_file(DISTRIBUTION_LUA_FILES) # Initialise and load lua files into lua environment
    parsed_data = parse_lua_tables(lua_runtime) # Get all the tables and convert to python data
    save_cache(parsed_data, "distributions_all.json") # Save to json file

LUA_COPY_TABLE = ("""
    function copyTable(tbl)
        local copy = {}
        for k, v in pairs(tbl) do
            if type(v) == "table" then
                copy[k] = copyTable(v)  -- Recursively copy nested tables
            else
                copy[k] = v
            end
        end
        return copy
    end
""")
if __name__ == "__main__":
    lua_runtime = load_lua_file("animal", inject_lua=LUA_COPY_TABLE)
    parsed_data = parse_lua_tables(lua_runtime, tables=["AnimalDefinitions"])
    save_cache(parsed_data, "animal_definitions.json")

# Loads lua files, inject multiple strings and define a specific table (this one is a local table, so we get the index with [1])
# Load order matters. We can either modify the order of the list, or use 'dependencies'
VEHICLE_DIST_FILES = [
    "VehicleDistribution_GloveBoxJunk.lua",
    "VehicleDistribution_SeatJunk.lua",
    "VehicleDistribution_TrunkJunk.lua",
    "VehicleDistributions.lua",
]
if __name__ == "__main__":
    lua_runtime = load_lua_file(VEHICLE_DIST_FILES, inject_lua=[LUA_EVENTS, LUA_CLUTTER_TABLES])
    parsed_data = parse_lua_tables(lua_runtime, tables=["VehicleDistributions[1]"])
    parsed_data = dict(sorted(parsed_data["VehicleDistributions[1]"].items()))
    save_cache(parsed_data, "vehicles.json")

# Table: Parse a specific table
TABLES = ["PrintMediaDefinitions"]
FILES_LIST = [
    'SpecialItemData_Books.lua',
    'SpecialItemData_Comics.lua',
    'SpecialItemData_Magazines.lua',
    'SpecialItemData_Misc.lua',
    'SpecialItemData_Photos.lua',
    'PrintMediaDefinitions.lua'
]
if __name__ == "__main__":
    lua_runtime = load_lua_file(FILES_LIST) # Initialise and load lua files into lua environment
    parsed_data = parse_lua_tables(lua_runtime, tables=TABLES) # Get only the defined tables and convert to python data
    save_cache(parsed_data, "literature2.json") # Save to json file