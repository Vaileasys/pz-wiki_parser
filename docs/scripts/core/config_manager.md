[Previous Folder](../animals/animal_article.md) | [Previous File](cache.md) | [Next File](constants.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# config_manager.py

## Functions

### [`_ensure_loaded()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L23)

Ensure the config is loaded into memory.
If the config file does not exist, it is reset to defaults.
Updates cached `_config` and `_data`.

### [`_update_missing_entries()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L39)

Check for missing sections or keys in the loaded config.
If any are missing, add them from `CONFIG_DEFAULTS` and rewrite the file.

### [`_bool_to_config(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L58)

### [`reset()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L64)

Reset the config file to the default values in `CONFIG_DEFAULTS`.
Overwrites the existing config file.

### [`refresh()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L78)

Clear the current in-memory config and reload it from file.
Updates cached `_config` and `_data`.

### [`get(key, section = 'Settings')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L88)

Get a config value from the in-memory cache.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Config key to retrieve._
  - **section (str)**:
      - _Section to look in (default 'Settings')._

<ins>**Returns:**</ins>
  - **str or None**:
      - _Config value as string, or None if not found._

### [`get_debug_mode()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L103)

Get the `debug_mode` setting as a boolean.

<ins>**Returns:**</ins>
  - **bool**:
      - _Debug mode status._

### [`get_first_time_run()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L113)

Get the `first_time_run` setting as a boolean.

<ins>**Returns:**</ins>
  - **bool**:
      - _First time run status._

### [`get_default_language() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L123)

Get the `default_language` setting.

<ins>**Returns:**</ins>
  - **str**:
      - _Default language code._

### [`get_version() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L133)

Get the `version` setting.

<ins>**Returns:**</ins>
  - **str**:
      - _Configured version string._

### [`get_game_directory() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L143)

Get the `game_directory` setting.

<ins>**Returns:**</ins>
  - **str**:
      - _Path to the game directory._

### [`get_zomboid_decompiler() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L153)

Get the `zomboid_decompiler` setting.

<ins>**Returns:**</ins>
  - **str**:
      - _Path to the zomboid decompiler._

### [`get_pywikibot() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L163)

Get the `pywikibot` setting.

<ins>**Returns:**</ins>
  - **str**:
      - _Path to the pywikibot._

### [`get_max_workers()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L173)

Get the `max_workers` setting.

<ins>**Returns:**</ins>
  - **str**:
      - _Number of max workers._

### [`set(key, value, section = 'Settings')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L183)

Update a config value and write it to the config file.
Also updates the in-memory cache.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Config key to update._
  - **value (str)**:
      - _Value to set._
  - **section (str)**:
      - _Section to update (default 'Settings')._

### [`set_debug_mode(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L204)

Set the `debug_mode` setting.

<ins>**Args:**</ins>
  - **value (bool or str)**:
      - _New debug mode value._

### [`set_first_time_run(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L214)

Set the `first_time_run` setting.

<ins>**Args:**</ins>
  - **value (bool or str)**:
      - _New first time run value._

### [`set_default_language(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L224)

Set the `default_language` setting.

<ins>**Args:**</ins>
  - **value (str)**:
      - _New default language code._

### [`set_version(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L234)

Set the `version` setting.

<ins>**Args:**</ins>
  - **value (str)**:
      - _New version string._

### [`set_game_directory(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L244)

Set the `game_directory` setting.

<ins>**Args:**</ins>
  - **value (str)**:
      - _New game directory path._

### [`set_zomboid_decompiler(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L254)

Set the `zomboid_decompiler` setting.

<ins>**Args:**</ins>
  - **value (str)**:
      - _New zomboid decompiler path._

### [`set_pywikibot(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L264)

Set the `pywikibot` setting.

<ins>**Args:**</ins>
  - **value (str)**:
      - _New pywikibot path._

### [`set_max_workers(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L274)

Set the `max_workers` setting.

<ins>**Args:**</ins>
  - **value (str)**:
      - _New number of max workers._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L284)

Main entry point to reset the config and update dependent modules.
Used to fully reset the config system.


[Previous Folder](../animals/animal_article.md) | [Previous File](cache.md) | [Next File](constants.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
