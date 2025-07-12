[Previous Folder](../roomdefine.md) | [Previous File](constants.md) | [Next File](language.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# file_loading.py

File Loading System

Provides utilities for mapping, locating, reading, and writing game-related files
(like scripts, lua, maps, clothing) under the game's media directory.

## Functions

### [`get_game_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L20)

Return the base directory where the game is installed.

### [`get_media_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L24)

Return the path to the media folder within the game directory.

### [`get_lua_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L28)

Return the path to the 'media/lua' directory.

### [`get_scripts_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L32)

Return the path to the 'media/scripts' directory.

### [`get_maps_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L36)

Return the path to the 'media/maps' directory.

### [`get_clothing_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L40)

Return the path to the 'media/clothing' directory.

### [`map_dir(base_dir, extension, media_type, suppress, exclude_ext)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L52)

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
  - **dict[str, list[str]]:**
      - {filename: [relative_paths]}

### [`map_game_files(suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L116)

Maps script and lua files, then saves to cache.


<ins>**Args:**</ins>
  - **suppress (bool)**:
      - _If True, hides duplicate warnings._

<ins>**Returns:**</ins>
  - **dict:**
      - {'scripts': ..., 'lua': ...}

### [`get_file_paths(mapping: dict, filename: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L151)

Returns all matching file paths from the mapping, optionally filtered by keyword.


<ins>**Args:**</ins>
  - **mapping (dict)**:
      - _Output from map_dir()._
  - **filename (str)**:
      - _Filename without extension._
  - **prefer (str, optional)**:
      - _Keyword to prioritise in path._

<ins>**Returns:**</ins>
  - **list[str]:**
      - All matching paths (may be empty).

### [`get_game_file_map()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L174)

Returns the cached game file map. Loads from disk once if needed.


<ins>**Returns:**</ins>
  - **dict:**
      - {'scripts': ..., 'lua': ...}

### [`get_files_by_type(filenames: str | list[str], media_type: str, prefer: str, prefix: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L188)

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
  - **list[str]:**
      - Absolute file paths.

### [`get_script_files(filenames: str | list[str], media_type: str, prefer: str, prefix: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L230)

Return absolute paths to script files, filtering by filenames, duplicates, or prefix.

### [`get_lua_files(filenames: str | list[str], media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L235)

Return absolute paths to Lua files, optionally filtering by name or preference keyword.

### [`get_clothing_files(filenames: str | list[str], media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L240)

Return absolute paths to clothing XML files, with optional name or preference filtering.

### [`get_relpath_by_type(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L246)

Retrieves the relative path to a file by name, as stored in the file map for the specified media type.


<ins>**Args:**</ins>
  - **name (str)**:
      - _The filename without extension._
  - **media_type (str)**:
      - _Media type ("lua", "scripts", "maps", "clothing", etc.)._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates._

<ins>**Returns:**</ins>
  - str | None: The relative file path if found, else None.

### [`get_script_relpath(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L263)

Return the relative path of a script file by name, optionally prioritising a substring.

### [`get_lua_relpath(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L267)

Return the relative path of a Lua file by name, optionally prioritising a substring.

### [`get_clothing_relpath(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L271)

Return the relative path of a clothing file by name, optionally prioritizing a substring.

### [`get_abs_path_by_type(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L277)

Retrieves the absolute path to a file by name for the specified media type.


<ins>**Args:**</ins>
  - **name (str)**:
      - _The filename without extension._
  - **media_type (str)**:
      - _Media type ("lua", "scripts", "maps", "clothing", etc.)._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates._

<ins>**Returns:**</ins>
  - str | None: The absolute file path if found, otherwise None.

### [`get_script_path(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L295)

Return the absolute path to a script file by name, optionally prioritizing a substring.

### [`get_lua_path(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L299)

Return the absolute path to a Lua file by name, optionally prioritizing a substring.

### [`get_clothing_path(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L303)

Return the absolute path to a clothing file by name, optionally prioritizing a substring.

### [`read_file(path: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L310)

Reads the contents of a file as a string.


<ins>**Args:**</ins>
  - **path (str)**:
      - _Path to the file._

<ins>**Returns:**</ins>
  - **str:**
      - File contents.

### [`write_file(content: list[str], rel_path: str, root_path: str, suppress: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L335)

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
  - **Path:**
      - Directory where the file was saved.

### [`load_file(rel_path, root_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L364)

Load a text file and return its lines as a list.


<ins>**Args:**</ins>
  - **rel_path (str)**:
      - _Relative path to the file._
  - **root_path (str, optional)**:
      - _Root directory to join with rel_path. Defaults to 'OUTPUT_LANG_DIR'._

<ins>**Returns:**</ins>
  - **list[str]:**
      - List of lines from the file, or an empty list if not found.

### [`clear_dir(directory: str, suppress: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L385)

Delete the contents of a directory at `root_path/rel_path`.

Only deletes contents under `PROJECT_ROOT`.

<ins>**Args:**</ins>
  - **directory (str)**:
      - _Directory to clear (automatically formats `language_code`)._
  - **suppress (bool)**:
      - _If True, suppress warning/info messages._

<ins>**Returns:**</ins>
  - **Path:**
      - The absolute path to the directory that was cleared.



[Previous Folder](../roomdefine.md) | [Previous File](constants.md) | [Next File](language.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
