[Previous Folder](../roomdefine.md) | [Previous File](cache.md) | [Next File](constants.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# config_manager.py

## Functions

### [`_ensure_loaded()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L20)

Ensure the config is loaded into memory.

If the config file does not exist, it is reset to defaults.
Updates cached `_config` and `_data`.

### [`_update_missing_entries()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L36)

Check for missing sections or keys in the loaded config.

If any are missing, add them from `CONFIG_DEFAULTS` and rewrite the file.

### [`_bool_to_config(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L55)
### [`reset()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L61)

Reset the config file to the default values in `CONFIG_DEFAULTS`.

Overwrites the existing config file.

### [`refresh()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L75)

Clear the current in-memory config and reload it from file.

Updates cached `_config` and `_data`.

### [`get(key, section)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L85)

Get a config value from the in-memory cache.


<ins>**Args:**</ins>
  - **key (str)**:
      - _Config key to retrieve._
  - **section (str)**:
      - _Section to look in (default 'Settings')._

<ins>**Returns:**</ins>
  - **str or None:**
      - Config value as string, or None if not found.

### [`get_debug_mode()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L100)

Get the `debug_mode` setting as a boolean.


<ins>**Returns:**</ins>
  - **bool:**
      - Debug mode status.

### [`get_first_time_run()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L111)

Get the `first_time_run` setting as a boolean.


<ins>**Returns:**</ins>
  - **bool:**
      - First time run status.

### [`get_default_language()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L122)

Get the `default_language` setting.


<ins>**Returns:**</ins>
  - **str:**
      - Default language code.

### [`get_version()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L133)

Get the `version` setting.


<ins>**Returns:**</ins>
  - **str:**
      - Configured version string.

### [`get_game_directory()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L144)

Get the `game_directory` setting.


<ins>**Returns:**</ins>
  - **str:**
      - Path to the game directory.

### [`set(key, value, section)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L155)

Update a config value and write it to the config file.

Also updates the in-memory cache.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Config key to update._
  - **value (str)**:
      - _Value to set._
  - **section (str)**:
      - _Section to update (default 'Settings')._

### [`set_debug_mode(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L176)

Set the `debug_mode` setting.


<ins>**Args:**</ins>
  - **value (bool or str)**:
      - _New debug mode value._

### [`set_first_time_run(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L186)

Set the `first_time_run` setting.


<ins>**Args:**</ins>
  - **value (bool or str)**:
      - _New first time run value._

### [`set_default_language(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L196)

Set the `default_language` setting.


<ins>**Args:**</ins>
  - **value (str)**:
      - _New default language code._

### [`set_version(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L206)

Set the `version` setting.


<ins>**Args:**</ins>
  - **value (str)**:
      - _New version string._

### [`set_game_directory(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L216)

Set the `game_directory` setting.


<ins>**Args:**</ins>
  - **value (str)**:
      - _New game directory path._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L226)

Main entry point to reset the config and update dependent modules.

Used to fully reset the config system.



[Previous Folder](../roomdefine.md) | [Previous File](cache.md) | [Next File](constants.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
