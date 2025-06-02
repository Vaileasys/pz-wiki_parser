[Previous Folder](../article_content/hotbar_slots_content.md) | [Previous File](cache.md) | [Next File](constants.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# config_manager.py

## Functions

### [`setup_config()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L20)

Sets up the config file with default settings from config_default.

### [`update_missing_entries(config)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L35)

Checks if there are missing sections or keys in the config file, and update the config file with any missing entries from config_default.

### [`open_config()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L63)

Open the config object.

:return: Loaded config object.

### [`load_config()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L81)

Load configuration from the config file into a dictionary.

:return: Config file dictionary.

### [`set_config(key, value, section)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L95)

Update or add an entry in the configuration file.

:param key: The key to update or add.
:param value: The value to set for the specified key.
:param section: Section where the key-value pair should be added or updated (optional).

### [`get_config(key, section)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L124)

Get an entry from the configuration file.

:param key: The key to get the value for.
:param section: Section where the key-value pair should be taken from (optional).
:return: Value of the config key.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/config_manager.py#L148)


[Previous Folder](../article_content/hotbar_slots_content.md) | [Previous File](cache.md) | [Next File](constants.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
