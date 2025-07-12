[Previous Folder](../tools/update_icons.md) | [Previous File](echo.md) | [Next File](media_helper.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# lua_helper.py

## Functions

### [`load_lua_file(lua_files: str | list[str], lua_runtime: LuaRuntime, dependencies: list[str], inject_lua: str, prefer: str, media_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/lua_helper.py#L7)

Loads and executes Lua files in the given Lua runtime.

:param lua_files: Lua file names or paths (single or list).
:param lua_runtime: Existing runtime or None to create one.
:param dependencies: Lua dependencies to load first.
:param inject_lua: Optional code to run before loading any files.
:param prefer: Optional keyword to prioritise among duplicate file paths.
:param media_type: The section of the game file map to search.
:return: Lua runtime.

### [`lua_to_python(lua_data: object)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/lua_helper.py#L56)

Converts Lua data to its Python equivalent (dict, list, or basic value).

:param lua_data: The Lua data to convert. Can be a basic type (int, float, bool, str, None), Lua table (converted to Python dict or list), or a Lua function (converted to a string).
:return: The corresponding Python data structure (dict, list, basic type, or string).

### [`parse_lua_tables(lua_runtime: LuaRuntime, tables: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/lua_helper.py#L103)

Parses Lua tables from the provided Lua runtime and converts them into Python data structures.

:param lua_runtime: The initialised Lua runtime environment containing the Lua code to parse.
:param tables: List of Lua table names to extract. If None, all global tables (excluding standard Lua libraries) will be extracted.
:return: Dictionary containing extracted tables with their Python data representations.



[Previous Folder](../tools/update_icons.md) | [Previous File](echo.md) | [Next File](media_helper.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
