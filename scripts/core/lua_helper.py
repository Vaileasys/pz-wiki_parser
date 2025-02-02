import os
from lupa import LuaRuntime, LuaError
from scripts.core import utility
from scripts.core.constants import LUA_PATH

def load_lua_file(lua_runtime: LuaRuntime, file_path: str, dependencies: list[str]=None, lua_fallback: str=None) -> LuaRuntime:
    """
    Loads and executes a Lua file in the given Lua runtime.

    :param lua_runtime (LuaRuntime): The initialized Lua runtime.
    :param file_path (str): The path to the Lua file to load.
    :param dependencies (list[str], optional): List of additional Lua files to load (LUA_PATH is already included). Defaults to None.
    :param lua_fallback (str, optional): Lua code for handling undefined variables. Defaults to None.
    :return: The Lua runtime after executing the files.
    """
    if lua_fallback:
    # Global fallback for undefined variables
        lua_runtime.execute(lua_fallback)
    
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

        # Check if cache_file includes a directory path
        if not os.path.dirname(file_path):
            file_path = os.path.join(LUA_PATH, file_path)

        # Load the main Lua file
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Main Lua file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as lua_file:
            try:
                lua_runtime.execute(lua_file.read())
            except LuaError as e:
                raise LuaError(f"Error executing main Lua file '{file_path}': {e}")

    except (FileNotFoundError, IOError, LuaError) as e:
        print(f"Error: {e}")
        raise

    return lua_runtime


def lua_to_python(lua_data: object) -> object:
    """
    Converts Lua data to its Python equivalent (dict, list, or basic value).

    :param lua_data: The Lua data to convert (basic type or Lua table).
    :return: The corresponding Python data (dict, list, basic type, or string).
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


def parse_lua_tables(lua_files: list[str], tables: list[str] = None, lua_fallback=None) -> dict:
    """
    Parses Lua files and extracts specified tables, converting them to Python data structures.

    :param lua_files: List of Lua file paths to parse.
    :param tables: List of table names to extract. If None, extracts all relevant tables.
    :return: Dictionary containing extracted tables with their Python data representations.
    """
    parsed_data = {}
    lua_runtime = LuaRuntime(unpack_returned_tuples=True)

    # Common Lua standard libraries to skip
    STANDARD_LUA_LIBS = {
        "math", "os", "io", "string", "table", "debug", "coroutine", "package", "utf8", "python", "_G"
    }

    for file in lua_files:
        try:
            file_path = os.path.join(LUA_PATH, file)

            # Load the Lua file
            lua_runtime = load_lua_file(lua_runtime, file_path, lua_fallback=lua_fallback)

            globals_dict = lua_runtime.globals()

            # If specific tables are provided, only extract those
            if tables:
                for table_name in tables:
                    try:
                        lua_table = lua_runtime.eval(table_name)
                        parsed_data[table_name] = lua_to_python(lua_table)
                    except LuaError:
                        print(f"Warning: Table '{table_name}' not found in '{file_path}'.")
            else:
                # Extract all relevant tables, excluding standard libraries
                for key, value in globals_dict.items():
                    if key not in STANDARD_LUA_LIBS and type(value).__name__ == '_LuaTable':
                        parsed_data[key] = lua_to_python(value)

        except (FileNotFoundError, IOError, LuaError) as e:
            print(f"Error processing '{file_path}': {e}")
            continue

    return parsed_data


# For testing lua file
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
#if __name__ == "__main__":
#    lua_files = ["forageSystem.lua"]
#    parsed_data = parse_lua_tables(lua_files, lua_fallback=test_lua_fallback)
#    utility.save_cache(parsed_data, "foraging_2.json")