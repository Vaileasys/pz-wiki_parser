import configparser
import os
from scripts.core import logger

config_file = 'config.ini'
config_data = {}

# Default configuration: [section] key = value
config_default = {
    "Settings": {
        "first_time_run": '0',
        "default_language": 'en',
        "version": '42.5.1',
        "game_directory": 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\ProjectZomboid',
    }
}

def setup_config():
    """
    Sets up the config file with default settings from config_default.
    """
    config = configparser.ConfigParser()

    for section, settings in config_default.items():
        config[section] = settings

    with open(config_file, 'w') as file:
        config.write(file)
    
    print(f"Configuration file '{config_file}' created.")


def update_missing_entries(config=None):
    """
    Checks if there are missing sections or keys in the config file, and update the config file with any missing entries from config_default.
    """
    if config is None:
        config = open_config()
    updated = False

    # Check for missing sections/keys
    for section, default_settings in config_default.items():
        if not config.has_section(section):
            # Add missing section
            config.add_section(section)
            updated = True
        
        for key, value in default_settings.items():
            if key not in config[section]:
                # Add missing key-value pair
                config.set(section, key, value)
                updated = True

    # If any updates were made, save the updated config
    if updated:
        with open(config_file, 'w') as file:
            config.write(file)
        logger.write(f"Repaired config file '{config_file}' as it was missing some entries.", True)


def open_config():
    """
    Open the config object.

    :return: Loaded config object.
    """
    config = configparser.ConfigParser()

    if not os.path.exists(config_file):
        print(f"Config file '{config_file}' not found. Creating it.")
        setup_config()
    
    config.read(config_file)
    update_missing_entries(config)

    return config


def load_config():
    """
    Load configuration from the config file into a dictionary.

    :return: Config file dictionary.
    """
    config = open_config()
    
    # Convert the loaded config into a dictionary
    config_dict = {section: dict(config.items(section)) for section in config.sections()}

    return config_dict


def set_config(key, value, section="Settings"):
    """
    Update or add an entry in the configuration file.

    :param key: The key to update or add.
    :param value: The value to set for the specified key.
    :param section: Section where the key-value pair should be added or updated (optional).
    """
    config = open_config()

    # Check if section exists, if not, add it
    if not config.has_section(section):
        config.add_section(section)

    # Set the new value for the key in the section
    config.set(section, key, str(value))

    # Save the updated config back to the INI file
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    logger.write(f"Configuration updated: [{section}] {key} = {value}")


def get_config(key, section='Settings'):
    """
    Get an entry from the configuration file.

    :param key: The key to get the value for.
    :param section: Section where the key-value pair should be taken from (optional).
    :return: Value of the config key.
    """
    global config_file
    global config_data
    if config_data == {}:
        config_data = load_config()

    if section not in config_data:
        print(f"Section '{section} does not exist in {config_file}")
        return None
    
    if key not in config_data[section]:
        print(f"Key '{key} does not exist in section {section} in {config_file}")
        return None

    return config_data[section][key]


def main():
     # lazy imports to stop import loops
    from scripts.core.language import Language
    from scripts.core.version import Version

    # Reset the config file
    setup_config()
    Language.update_default()
    Version.update()
    print("Config file reset.")
    