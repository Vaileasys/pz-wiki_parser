[Previous Folder](../animals/animal_article.md) | [Previous File](constants.md) | [Next File](language.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# file_loading.py

File Loading System

Provides utilities for mapping, locating, reading, and writing game-related files
(like scripts, lua, maps, clothing) under the game's media directory.

## Functions

### [`get_game_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L21)

Return the base directory where the game is installed.

### [`get_media_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L25)

Return the path to the media folder within the game directory.

### [`get_lua_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L29)

Return the path to the 'media/lua' directory.

### [`get_scripts_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L33)

Return the path to the 'media/scripts' directory.

### [`get_maps_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L37)

Return the path to the 'media/maps' directory.

### [`get_clothing_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L41)

Return the path to the 'media/clothing' directory.

### [`map_dir(base_dir, extension = None, media_type = 'scripts', suppress = False, exclude_ext = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L53)

Maps all files with the given extension in a directory.

<ins>**Args:**</ins>
  - **base_dir (str)**:
      - _Directory to scan._
  - **extension (str)**:
      - _File extension to include._
  - **media_type (str)**:
      - _Media type this map is for ("scripts", "lua")._
  - **suppress (bool)**:
      - _If True, hides duplicate warnings._

<ins>**Returns:**</ins>
  - **dict[str, list[str]]**:
      - _{filename: [relative_paths]}_

### [`map_game_files(suppress = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L119)

### [`get_file_paths(mapping: dict, filename: str, *, prefer = None) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L156)

Returns all matching file paths from the mapping, optionally filtered by keyword.

<ins>**Args:**</ins>
  - **mapping (dict)**:
      - _Output from map_dir()._
  - **filename (str)**:
      - _Filename without extension._
  - **prefer (str, optional)**:
      - _Keyword to prioritise in path._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _All matching paths (may be empty)._

### [`get_game_file_map() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L179)

Returns the cached game file map. Loads from disk once if needed.

<ins>**Returns:**</ins>
  - **dict**:
      - _{'scripts': ..., 'lua': ...}_

### [`get_files_by_type(filenames: str | list[str] = None, media_type: str = 'scripts', prefer: str = None, prefix: str = None) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L194)

Resolves filenames to absolute paths using the file map for the specified media type.

<ins>**Args:**</ins>
  - **filenames (str or list[str], optional)**:
      - _File names (no extension or path). If None, includes all files._
  - **media_type (str)**:
      - _Media type ("lua", "scripts", "maps", "clothing", etc.)._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates._
  - **prefix (str, optional)**:
      - _Only include files starting with this prefix._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _Absolute file paths._

### [`get_script_files(filenames: str | list[str] = None, media_type: str = 'scripts', prefer: str = None, prefix: str = None) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L236)

Return absolute paths to script files, filtering by filenames, duplicates, or prefix.

### [`get_lua_files(filenames: str | list[str] = None, media_type: str = 'lua', prefer: str = None) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L241)

Return absolute paths to Lua files, optionally filtering by name or preference keyword.

### [`get_clothing_files(filenames: str | list[str] = None, media_type: str = 'clothing', prefer: str = None) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L246)

Return absolute paths to clothing XML files, with optional name or preference filtering.

### [`get_relpath_by_type(name: str, media_type: str, prefer: str = None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L252)

Retrieves the relative path to a file by name, as stored in the file map for the specified media type.

<ins>**Args:**</ins>
  - **name (str)**:
      - _The filename without extension._
  - **media_type (str)**:
      - _Media type ("lua", "scripts", "maps", "clothing", etc.)._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates._

<ins>**Returns:**</ins>
  - **str | None**:
      - _The relative file path if found, else None._

### [`get_script_relpath(name: str, prefer: str = None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L269)

Return the relative path of a script file by name, optionally prioritising a substring.

### [`get_lua_relpath(name: str, prefer: str = None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L273)

Return the relative path of a Lua file by name, optionally prioritising a substring.

### [`get_clothing_relpath(name: str, prefer: str = None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L277)

Return the relative path of a clothing file by name, optionally prioritizing a substring.

### [`get_abs_path_by_type(name: str, media_type: str, prefer: str = None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L283)

Retrieves the absolute path to a file by name for the specified media type.

<ins>**Args:**</ins>
  - **name (str)**:
      - _The filename without extension._
  - **media_type (str)**:
      - _Media type ("lua", "scripts", "maps", "clothing", etc.)._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates._

<ins>**Returns:**</ins>
  - **str | None**:
      - _The absolute file path if found, otherwise None._

### [`get_script_path(name: str, media_type: str = 'scripts', prefer: str = None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L301)

Return the absolute path to a script file by name, optionally prioritizing a substring.

### [`get_lua_path(name: str, media_type: str = 'lua', prefer: str = None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L305)

Return the absolute path to a Lua file by name, optionally prioritizing a substring.

### [`get_clothing_path(name: str, media_type: str = 'clothing', prefer: str = None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L309)

Return the absolute path to a clothing file by name, optionally prioritizing a substring.

### [`build_file_map(base_dir: Path, name: str = 'unknown') -> dict[str, Path]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L316)

Get a mapping of relative file paths to absolute paths.

### [`hash_file(path: Path) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L326)

### [`load_json(path: str) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L336)

Load JSON data from a file. Returns empty dict on failure.

### [`save_json(path: str, data: dict) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L349)

Save dictionary data to a JSON file. Returns True if successful.

### [`read_file(path: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L362)

Reads the contents of a file as a string.

<ins>**Args:**</ins>
  - **path (str)**:
      - _Path to the file._

<ins>**Returns:**</ins>
  - **str**:
      - _File contents._

### [`write_file(content: list[str], rel_path: str = 'output.txt', root_path: str = OUTPUT_LANG_DIR, suppress: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L387)

Writes content to a file, creating directories as needed.

<ins>**Args:**</ins>
  - **content (list[str])**:
      - _A list of strings to write to the file._
  - **rel_path (str)**:
      - _Relative path where the file will be saved. If no file extension is given, it's treated as a directory._
  - **root_path (str)**:
      - _Root path to prepend to `rel_path`. {language_code} will be formatted to current language code._
  - **clear_root (bool)**:
      - _If True, deletes all contents under `root_path` before writing._
  - **suppress (bool)**:
      - _If True, suppresses info messages._

<ins>**Returns:**</ins>
  - **Path**:
      - _Directory where the file was saved._

### [`load_file(rel_path, root_path = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L416)

Load a text file and return its lines as a list.

<ins>**Args:**</ins>
  - **rel_path (str)**:
      - _Relative path to the file._
  - **root_path (str, optional)**:
      - _Root directory to join with rel_path. Defaults to 'OUTPUT_LANG_DIR'._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _List of lines from the file, or an empty list if not found._

### [`clear_dir(directory: str = OUTPUT_LANG_DIR, suppress: bool = False) -> Path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L437)

Delete the contents of a directory at `root_path/rel_path`.
Only deletes contents under `PROJECT_ROOT`.

<ins>**Args:**</ins>
  - **directory (str)**:
      - _Directory to clear (automatically formats `language_code`)._
  - **suppress (bool)**:
      - _If True, suppress warning/info messages._

<ins>**Returns:**</ins>
  - **Path**:
      - _The absolute path to the directory that was cleared._


[Previous Folder](../animals/animal_article.md) | [Previous File](constants.md) | [Next File](language.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
