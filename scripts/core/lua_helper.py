import os
from lupa import LuaRuntime, LuaError
from scripts.core import utility
from scripts.core.constants import LUA_PATH

def load_lua_file(lua_files: list[str], lua_runtime: LuaRuntime=None, dependencies: list[str]=None, inject_lua: str=None) -> LuaRuntime:
    """
    Loads and executes a Lua file in the given Lua runtime.

    :param lua_files (list[str]): List of Lua file paths to load and execute. A single file path can also be provided as a string.
    :param lua_runtime (LuaRuntime, optional): An existing Lua runtime instance. If not provided, a new Lua runtime will be initialised.
    :param dependencies (list[str], optional): List of additional Lua dependency files to load before the main files (LUA_PATH is already included).
    :param inject_lua (str, optional): Lua code to inject directly into the runtime before executing any files. Useful for adding stubs or fallbacks.
    :return: The Lua runtime after executing the files.
    """
    # Initialise new Lua runtime environment if one wasn't provided
    if not lua_runtime:
        lua_runtime = LuaRuntime(unpack_returned_tuples=True)

    # Inject Lua into the runtime environemnt. Can be used for fallbacks, such as creating stubs.
    if inject_lua:
        lua_runtime.execute(inject_lua)
    
    try:
        # Load extra Lua files if provided
        if dependencies:
            for dependency in dependencies:
                dependency_path = os.path.join(LUA_PATH, dependency)
                if not os.path.isfile(dependency_path):
                    raise FileNotFoundError(f"Dependency file not found: {dependency_path}")

                with open(dependency_path, 'r', encoding='utf-8') as f:
                    try:
                        lua_runtime.execute(f.read())
                    except LuaError as e:
                        raise LuaError(f"Error executing extra Lua file '{dependency_path}': {e}")
                    
        if isinstance(lua_files, str):
            lua_files = [lua_files]
        
        for lua_file in lua_files:
            lua_file_path = os.path.join(LUA_PATH, lua_file)

            # Load the Lua files
            if not os.path.isfile(lua_file_path):
                raise FileNotFoundError(f"Lua file not found: {lua_file_path}")

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


# Inject lua: Foraging - initialises and stubs Events table
test_lua_fallback = ("""
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
if __name__ == "__main__":
    lua_runtime = load_lua_file("forageSystem.lua", inject_lua=test_lua_fallback)
    parsed_data = parse_lua_tables(lua_runtime)
    utility.save_cache(parsed_data, "foraging_2.json")

# Basic usage: Recorded media
if __name__ == "__main__":
    lua_runtime = load_lua_file("recorded_media.lua")
    parsed_data = parse_lua_tables(lua_runtime)
    utility.save_cache(parsed_data, "recorded_media.json")

# Basic usage: Burn time
if __name__ == "__main__":
    lua_runtime = load_lua_file("camping_fuel.lua")
    parsed_data = parse_lua_tables(lua_runtime)
    utility.save_cache(parsed_data, "camping_fuel.json")

# Basic usage: Attached weapon definitions
if __name__ == "__main__":
    lua_runtime = load_lua_file("AttachedWeaponDefinitions.lua")
    parsed_data = parse_lua_tables(lua_runtime)
    utility.save_cache(parsed_data, "attached_weapon_definitions.json")

# Inject lua and multiple files: All distributions - initialises ClutterTables and BagsAndContainers tables
distributions_lua = ("""
    ClutterTables = ClutterTables or setmetatable({}, {
        __index = function(_, key)
            return setmetatable({}, {
                __index = function(_, inner_key)
                    return function() return tostring(inner_key) end
                end
            })
        end
    })

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
DISTRIBUTION_LUA_FILES = [
    "ProceduralDistributions.lua",
    "VehicleDistributions.lua",
    "VehicleDistribution_GloveBoxJunk.lua",
    "VehicleDistribution_SeatJunk.lua",
    "VehicleDistribution_TrunkJunk.lua",
    "Distribution_BinJunk.lua",
    "Distribution_BagsAndContainers.lua",
    "Distribution_BinJunk.lua",
    "Distribution_ClosetJunk.lua",
    "Distribution_CounterJunk.lua",
    "Distribution_DeskJunk.lua",
    "Distribution_ShelfJunk.lua",
    "Distribution_SideTableJunk.lua",
]
if __name__ == "__main__":
    lua_runtime = load_lua_file("Distributions.lua", dependencies=DISTRIBUTION_LUA_FILES, inject_lua=distributions_lua) # Initialise and load lua files into lua environment
    parsed_data = parse_lua_tables(lua_runtime) # Get all the tables and convert to python data
    utility.save_cache(parsed_data, "distributions_all.json") # Save to json file

copy_table_fallback = ("""
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
ANIMAL_LUA_FILES = [
    "animal/ChickenDefinitions.lua",
    "animal/CowDefinitions.lua",
    "animal/DeerDefinitions.lua",
    "animal/MouseDefinitions.lua",
    "animal/PigDefinitions.lua",
    "animal/RabbitDefinitions.lua",
    "animal/RaccoonDefinitions.lua",
    "animal/RatDefinitions.lua",
    "animal/SheepDefinitions.lua",
    "animal/TurkeyDefinitions.lua",
]
if __name__ == "__main__":
    lua_runtime = load_lua_file(ANIMAL_LUA_FILES, inject_lua=copy_table_fallback)
    parsed_data = parse_lua_tables(lua_runtime)
    utility.save_cache(parsed_data, "animal_definitions.json")


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
    utility.save_cache(parsed_data, "literature2.json") # Save to json file