[Previous Folder](../article_content/hotbar_slots_content.md) | [Previous File](constants.md) | [Next File](language.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# file_loading.py

## Functions

### [`get_game_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L17)
### [`get_media_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L20)
### [`get_lua_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L23)
### [`get_scripts_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L26)
### [`get_maps_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L29)
### [`map_dir(base_dir, extension, media_type, suppress, exclude_ext)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L33)

_Maps all files with the given extension in a directory._

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
### [`map_game_files(suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L97)

_Maps script and lua files, then saves to cache._

<ins>**Args:**</ins>
  - **suppress (bool)**:
      - _If True, hides duplicate warnings._

<ins>**Returns:**</ins>
  - **dict:**
      - {'scripts': ..., 'lua': ...}
### [`get_file_paths(mapping: dict, filename: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L130)

_Returns all matching file paths from the mapping, optionally filtered by keyword._

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
### [`get_game_file_map()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L153)

_Returns the cached game file map. Loads from disk once if needed._

<ins>**Returns:**</ins>
  - **dict:**
      - {'scripts': ..., 'lua': ...}
### [`get_lua_files(filenames: str | list[str], prefer: str, media_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L166)

_Resolves base Lua filenames to absolute paths using the file map._

<ins>**Args:**</ins>
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates._
  - **media_type (str)**:
      - _Media type ("lua", "scripts", etc.)._

<ins>**Returns:**</ins>
  - **list[str]:**
      - Absolute file paths.
### [`get_script_files(prefix: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L216)

_Retrieves a list of script .txt files from the game scripts folder, optionally filtering by prefix._

<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **list[str]:**
      - List of absolute file paths.
### [`get_script_relpath(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L234)

_Retrieves the relative path to a script (.txt) file by name, as stored in the file map._

<ins>**Args:**</ins>
  - **name (str)**:
      - _The filename without extension (e.g., "AssaultRifle")._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates (e.g., "weapons")._

<ins>**Returns:**</ins>
      - str | None: The relative file path (e.g., "weapons/AssaultRifle.txt") if found, else None.
### [`get_lua_relpath(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L250)

_Retrieves the relative path to a Lua (.lua) file by name, as stored in the file map._

<ins>**Args:**</ins>
  - **name (str)**:
      - _The filename without extension (e.g., "ISInventoryPage")._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates (e.g., "client")._

<ins>**Returns:**</ins>
      - str | None: The relative file path (e.g., "client/ISInventoryPage.lua") if found, else None.
### [`get_script_path(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L266)

_Retrieves the absolute path to a script (.txt) file by name._

<ins>**Args:**</ins>
  - **name (str)**:
      - _The filename without extension (e.g., "AssaultRifle")._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates (e.g., "weapons")._

<ins>**Returns:**</ins>
      - str | None: The absolute file path if found, otherwise None.
### [`get_lua_path(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L282)

_Retrieves the absolute path to a Lua (.lua) file by name._

<ins>**Args:**</ins>
  - **name (str)**:
      - _The filename without extension (e.g., "ISInventoryPage")._
  - **prefer (str, optional)**:
      - _Keyword to prioritise among duplicates (e.g., "client")._

<ins>**Returns:**</ins>
      - str | None: The absolute file path if found, otherwise None.
### [`read_file(path: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L299)

_Reads the contents of a file as a string._

<ins>**Args:**</ins>
  - **path (str)**:
      - _Path to the file._

<ins>**Returns:**</ins>
  - **str:**
      - File contents.
### [`write_file(content: list, rel_path, root_path, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L324)

_Writes content to a file, creating directories as needed._
### [`load_file(rel_path, root_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L351)

_Load a text file and return its lines as a list._

<ins>**Args:**</ins>
  - **rel_path (str)**:
      - _Relative path to the file._
  - **root_path (str, optional)**:
      - _Root directory to join with rel_path. Defaults to 'OUTPUT_LANG_DIR'._

<ins>**Returns:**</ins>
  - **list[str]:**
      - List of lines from the file, or an empty list if not found.


[Previous Folder](../article_content/hotbar_slots_content.md) | [Previous File](constants.md) | [Next File](language.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
