import os
from lupa import LuaRuntime, LuaError
from scripts.core.file_loading import get_lua_files, read_file, get_lua_dir
from scripts.core.cache import save_cache
from scripts.utils.echo import echo_error, echo_warning

def load_lua_file(lua_files: str | list[str], lua_runtime: LuaRuntime = None, dependencies: list[str] = None, inject_lua: str = None, prefer: str = None, media_type: str = "lua") -> LuaRuntime:
    """
    Loads and executes Lua files in the given Lua runtime.

    :param lua_files: Lua file names or paths (single or list).
    :param lua_runtime: Existing runtime or None to create one.
    :param dependencies: Lua dependencies to load first.
    :param inject_lua: Optional code to run before loading any files.
    :param prefer: Optional keyword to prioritise among duplicate file paths.
    :param media_type: The section of the game file map to search.
    :return: Lua runtime.
    """
    if not lua_runtime:
        lua_runtime = LuaRuntime(unpack_returned_tuples=True)
        lua_path = os.path.normpath(get_lua_dir()).replace(os.sep, "/")
        lua_runtime.execute(f"package.path = package.path .. ';{lua_path}/?.lua;{lua_path}/?/init.lua'")

    if inject_lua:
        lua_runtime.execute("\n\n".join(inject_lua) if isinstance(inject_lua, list) else inject_lua)

    try:
        # Load dependencies
        if dependencies:
            for dep_path in get_lua_files(dependencies, media_type=media_type):
                try:
                    lua_runtime.execute(read_file(dep_path))
                except LuaError as e:
                    raise LuaError(f"Error executing dependency '{dep_path}': {e}")

        # Load main files
        for lua_path in get_lua_files(lua_files, prefer=prefer, media_type=media_type):
            try:
                lua_runtime.execute(read_file(lua_path))
            except LuaError as e:
                raise LuaError(f"Error executing main Lua file '{lua_path}': {e}")

    except (FileNotFoundError, IOError, LuaError) as e:
        echo_error(str(e))
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
                echo_warning(f"Table '{table_name}' not found.")
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
ANIMAL_FILES = [
    'ChickenDefinitions.lua',
    'CowDefinitions.lua',
    'DeerDefinitions.lua',
    'MouseDefinitions.lua',
    'PigDefinitions.lua',
    'RabbitDefinitions.lua',
    'RaccoonDefinitions.lua',
    'RatDefinitions.lua',
    'SheepDefinitions.lua',
    'TurkeyDefinitions.lua',
]
if __name__ == "__main__":
    lua_runtime = load_lua_file(ANIMAL_FILES, inject_lua=LUA_COPY_TABLE)
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