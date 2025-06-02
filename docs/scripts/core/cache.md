[Previous Folder](../article_content/hotbar_slots_content.md) | [Next File](config_manager.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# cache.py

## Functions

### [`load_json(path: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/cache.py#L10)

Load JSON data from a file. Returns empty dict on failure.

### [`save_json(path: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/cache.py#L22)

Save dictionary data to a JSON file. Returns True if successful.

### [`save_cache(data: dict, data_file: str, data_dir, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/cache.py#L33)

Caches data by saving it to a json file.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Data to be cached, by storing it in a json file._
  - **data_file (str)**:
      - _Name of the JSON file to be saved as. Including the file extension is optional._
  - **data_dir (_type_, optional)**:
      - _Custom directory for the JSON file. Defaults to value of 'scripts.core.constants.DATA_PATH'._
  - **suppress (bool, optional)**:
      - _Suppress displaying warnings/print statements. Defaults to False._

### [`load_cache(cache_file, cache_name, get_version, backup_old, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/cache.py#L60)

Loads the cache from a json file with the option to return the version of it, and back it up if it's old.


<ins>**Args:**</ins>
  - **cache_file (str)**:
      - _Path to the cache file._
  - **cache_name (str, optional)**:
      - _String to be used in prints. Should be a name for the type of cache, e.g. 'item'. Defaults to None._
  - **get_version (bool, optional)**:
      - _If True, returns the version of the cached data. Defaults to False._
  - **backup_old (bool, optional)**:
      - _If True, backs up the cache, only if it's an old version. Defaults to False._
  - **suppress (bool, optional)**:
      - _Suppress displaying print statements (errors still displayed). Defaults to False._

<ins>**Returns:**</ins>
  - **dict:**
      - Cached data if valid, otherwise an empty dictionary.
  - **str:**
      - Version of the cached data, if 'get_version' is True.

### [`clear_cache(cache_path, cache_name, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/cache.py#L109)

Clears the cache at a specified file path.


<ins>**Args:**</ins>
  - **cache_path (str)**:
      - _File path of the cache to be deleted. Can be a single file, or entire folder. Must be a file or folder in 'scripts.core.constants.DATA_PATH'._
  - **cache_name (str, optional)**:
      - _String to be used in print statements. Should be a name for the type of cache, e.g. 'item'. Defaults to None._
  - **suppress (bool, optional)**:
      - _Suppress displaying print statements (errors still displayed). Defaults to False._



[Previous Folder](../article_content/hotbar_slots_content.md) | [Next File](config_manager.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
