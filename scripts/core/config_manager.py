import configparser
import os

CONFIG_FILE = 'config.ini'
CONFIG_DEFAULTS = {
    "Settings": {
        "first_time_run": 'false',
        "default_language": 'en',
        "version": '42.8.1',
        "game_directory": 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\ProjectZomboid',
        "debug_mode": 'false'
    }
}

_config = None
_data = {}


def _ensure_loaded():
    """
    Ensure the config is loaded into memory.
    If the config file does not exist, it is reset to defaults.
    Updates cached `_config` and `_data`.
    """
    global _config, _data
    if _config is None:
        _config = configparser.ConfigParser()
        if not os.path.exists(CONFIG_FILE):
            reset()
        _config.read(CONFIG_FILE)
        _update_missing_entries()
        _data = {section: dict(_config.items(section)) for section in _config.sections()}


def _update_missing_entries():
    """
    Check for missing sections or keys in the loaded config.
    If any are missing, add them from `CONFIG_DEFAULTS` and rewrite the file.
    """
    updated = False
    for section, defaults in CONFIG_DEFAULTS.items():
        if not _config.has_section(section):
            _config.add_section(section)
            updated = True
        for key, value in defaults.items():
            if key not in _config[section]:
                _config.set(section, key, value)
                updated = True
    if updated:
        with open(CONFIG_FILE, 'w') as file:
            _config.write(file)


def _to_bool(value):
    """
    Convert a value to boolean by checking common 'true' strings.

    Args:
        value: Any value to check.

    Returns:
        bool: True if the value matches a 'true' string; False otherwise.
    """
    return str(value).lower() in ('true', 't', '1', 'yes', 'y', 'on')


def _bool_to_config(value):
    if not isinstance(value, bool):
        value = _to_bool(value)
    return "true" if value else "false"


def reset():
    """
    Reset the config file to the default values in `CONFIG_DEFAULTS`.
    Overwrites the existing config file.
    """
    from scripts.utils.echo import echo_info
    config = configparser.ConfigParser()
    for section, values in CONFIG_DEFAULTS.items():
        config[section] = values
    with open(CONFIG_FILE, 'w') as file:
        config.write(file)
    echo_info("Config file reset.")


def refresh():
    """
    Clear the current in-memory config and reload it from file.
    Updates cached `_config` and `_data`.
    """
    global _config, _data
    _config = None
    _ensure_loaded()


def get(key, section='Settings'):
    """
    Get a config value from the in-memory cache.

    Args:
        key (str): Config key to retrieve.
        section (str): Section to look in (default 'Settings').

    Returns:
        str or None: Config value as string, or None if not found.
    """
    _ensure_loaded()
    return _data.get(section, {}).get(key)


def get_debug_mode():
    """
    Get the `debug_mode` setting as a boolean.

    Returns:
        bool: Debug mode status.
    """
    _ensure_loaded()
    return _to_bool(_data['Settings']['debug_mode'])


def get_first_time_run():
    """
    Get the `first_time_run` setting as a boolean.

    Returns:
        bool: First time run status.
    """
    _ensure_loaded()
    return _to_bool(_data['Settings']['first_time_run'])


def get_default_language():
    """
    Get the `default_language` setting.

    Returns:
        str: Default language code.
    """
    _ensure_loaded()
    return _data['Settings']['default_language']


def get_version():
    """
    Get the `version` setting.

    Returns:
        str: Configured version string.
    """
    _ensure_loaded()
    return _data['Settings']['version']


def get_game_directory():
    """
    Get the `game_directory` setting.

    Returns:
        str: Path to the game directory.
    """
    _ensure_loaded()
    return _data['Settings']['game_directory']


def set(key, value, section='Settings'):
    """
    Update a config value and write it to the config file.
    Also updates the in-memory cache.

    Args:
        key (str): Config key to update.
        value (str): Value to set.
        section (str): Section to update (default 'Settings').
    """
    _ensure_loaded()
    if not _config.has_section(section):
        _config.add_section(section)
    _config.set(section, key, str(value))
    with open(CONFIG_FILE, 'w') as file:
        _config.write(file)
    if section not in _data:
        _data[section] = {}
    _data[section][key] = str(value)


def set_debug_mode(value):
    """
    Set the `debug_mode` setting.

    Args:
        value (bool or str): New debug mode value.
    """
    set('debug_mode', _bool_to_config(value))


def set_first_time_run(value):
    """
    Set the `first_time_run` setting.

    Args:
        value (bool or str): New first time run value.
    """
    set('first_time_run', _bool_to_config(value))


def set_default_language(value):
    """
    Set the `default_language` setting.

    Args:
        value (str): New default language code.
    """
    set('default_language', value)


def set_version(value):
    """
    Set the `version` setting.

    Args:
        value (str): New version string.
    """
    set('version', value)


def set_game_directory(value):
    """
    Set the `game_directory` setting.

    Args:
        value (str): New game directory path.
    """
    set('game_directory', value)


def main():
    """
    Main entry point to reset the config and update dependent modules.
    Used to fully reset the config system.
    """
    # lazy imports to stop import loops
    from scripts.core.language import Language
    from scripts.core.version import Version

    # Reset the config file to defaults
    reset()
    refresh()  # reload cache after resetting

    Language.update_default()
    Version.update()
    
if __name__ == "__main__":
    print(get_debug_mode())