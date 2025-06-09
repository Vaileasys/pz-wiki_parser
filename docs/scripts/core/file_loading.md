[Previous Folder](../consumables.md) | [Previous File](constants.md) | [Next File](language.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# file_loading.py

## Functions

### [`get_game_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L14)
### [`get_media_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L17)
### [`get_lua_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L20)
### [`get_scripts_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L23)
### [`get_maps_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L26)
### [`get_clothing_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L29)
### [`map_dir(base_dir, extension, media_type, suppress, exclude_ext)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L40)

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

### [`map_game_files(suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L104)

Maps script and lua files, then saves to cache.


<ins>**Args:**</ins>
  - **suppress (bool)**:
      - _If True, hides duplicate warnings._

<ins>**Returns:**</ins>
  - **dict:**
      - {'scripts': ..., 'lua': ...}

### [`get_file_paths(mapping: dict, filename: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L139)

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

### [`get_game_file_map()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L162)

Returns the cached game file map. Loads from disk once if needed.


<ins>**Returns:**</ins>
  - **dict:**
      - {'scripts': ..., 'lua': ...}

### [`get_files_by_type(filenames: str | list[str], media_type: str, prefer: str, prefix: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L176)

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

### [`get_script_files(filenames: str | list[str], media_type: str, prefer: str, prefix: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L218)
### [`get_lua_files(filenames: str | list[str], media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L222)
### [`get_clothing_files(filenames: str | list[str], media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L226)
### [`get_relpath_by_type(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L231)

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

### [`get_script_relpath(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L248)
### [`get_lua_relpath(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L251)
### [`get_clothing_relpath(name: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L254)
### [`get_abs_path_by_type(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L259)

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

### [`get_script_path(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L277)
### [`get_lua_path(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L280)
### [`get_clothing_path(name: str, media_type: str, prefer: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L283)
### [`read_file(path: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L289)

Reads the contents of a file as a string.


<ins>**Args:**</ins>
  - **path (str)**:
      - _Path to the file._

<ins>**Returns:**</ins>
  - **str:**
      - File contents.

### [`write_file(content: list, rel_path, root_path, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L314)

Writes content to a file, creating directories as needed.

:param list content: A list of strings to write to the file.
:param str rel_path: The relative path where the file will be saved. If no file extension is given, the path is treated as a directory.
:param str root_path: The root path where the rel_path will be appended. {language_code} will be formatted to current language code.
:return: The directory the file is saved to.

### [`load_file(rel_path, root_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/file_loading.py#L341)

Load a text file and return its lines as a list.


<ins>**Args:**</ins>
  - **rel_path (str)**:
      - _Relative path to the file._
  - **root_path (str, optional)**:
      - _Root directory to join with rel_path. Defaults to 'OUTPUT_LANG_DIR'._

<ins>**Returns:**</ins>
  - **list[str]:**
      - List of lines from the file, or an empty list if not found.



[Previous Folder](../consumables.md) | [Previous File](constants.md) | [Next File](language.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
