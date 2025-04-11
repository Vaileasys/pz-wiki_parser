import json
import os
import shutil
import re
from tqdm import tqdm
from scripts.core.constants import DATA_PATH
from scripts.core.language import Language
from scripts.core.version import Version


def load_json(path:str) -> dict:
    """Load JSON data from a file. Returns empty dict on failure."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as e:
        echo(f"Warning: Failed to load JSON from {path} – {e}")
        return {}


def save_json(path:str, data:dict) -> bool:
    """Save dictionary data to a JSON file. Returns True if successful."""
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except OSError as e:
        echo(f"Error: Could not write to {path} – {e}")
        return False


def capitalize(value):
    """
    Safely perform the capitalize method if a value is not a string. Lists will also be capitalized, provided their values are strings.

    :param value: The string or list of strings to capitalize.
    :type value: str
    :return: Capitalized values if a string or list, otherwise None.
    :rtype: str | list | None
    """
#    print(value)
    if isinstance(value, str):
        value = [value]
        is_string = True
    elif isinstance(value, list):
        is_string = False
    else:
        return None

    rvalue = []
    
    for v in value:
        if isinstance(v, str):
            v = v.capitalize()
        else:
            v = None

        rvalue.append(v)

    if is_string:
        return rvalue[0]
    
    return rvalue


def format_positive(value):
    """
    Formats a number with '+' if positive, trimming trailing zeros. Returns original value as string if invalid.
    
    :param value: The value to format.
    :type value: float | int | str | any
    :return: Formatted string with '+' prefix if positive, or original value as a string if invalid.
    :rtype: str
    """
    try:
        value = float(value)
        text = f"{value:.10f}".rstrip("0").rstrip(".")
        return f"+{text}" if value > 0 else text
    except (ValueError, TypeError):
        return str(value)


def format_link(name:str, page:str=None) -> str:
    """
    Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages.

    :param name: The display text of the link.
    :param page: The target page (optional). Defaults to `name`.
    :return: The formatted wiki link.
    """
    language_code = Language.get()
    
    if language_code != "en":
        return f"[[{page or name}/{language_code}|{name}]]"
    
    if page is None or page == name:
        return f"[[{name}]]"
    else:
        return f"[[{page}|{name}]]"
    
# Save parsed data to json file
def save_cache(data: dict, data_file: str, data_dir=DATA_PATH, suppress=False):
    """Caches data by saving it to a json file.

    Args:
        data (dict): Data to be cached, by storing it in a json file.
        data_file (str): Name of the JSON file to be saved as. Including the file extension is optional.
        data_dir (_type_, optional): Custom directory for the JSON file. Defaults to value of 'scripts.core.constants.DATA_PATH'.
        suppress (bool, optional): Suppress displaying warnings/print statements. Defaults to False.
    """
    if not data_file.endswith(".json"):
        data_file + ".json"
    data_file_path = os.path.join(data_dir, data_file)
    os.makedirs(os.path.dirname(data_file_path), exist_ok=True)

    # Adds space between words for CamelCase strings and cleans string
    cache_name = re.sub(r'(?<=[a-z])([A-Z])', r' \1', data_file.replace(".json", "")).replace("_", " ").strip().lower()

    data_copy = data.copy() # Copy so we don't modify the existing usable data.
    # Add version number to data. Version can be checked to save time parsing.
    data_copy["version"] = Version.get()
    
    save_json(data_file_path, data_copy)
    
    if not suppress:
        echo(f"{cache_name.capitalize()} saved to '{data_file_path}'")


def load_cache(cache_file, cache_name="data", get_version=False, backup_old=False, suppress=False):
    """Loads the cache from a json file with the option to return the version of it, and back it up if it's old.

    Args:
        cache_file (str): Path to the cache file.
        cache_name (str, optional): String to be used in prints. Should be a name for the type of cache, e.g. 'item'. Defaults to None.
        get_version (bool, optional): If True, returns the version of the cached data. Defaults to False.
        backup_old (bool, optional): If True, backs up the cache, only if it's an old version. Defaults to False.
        suppress (bool, optional): Suppress displaying print statements (errors still displayed). Defaults to False.

    Returns:
        dict: Cached data if valid, otherwise an empty dictionary.
        str: Version of the cached data, if 'get_version' is True.
    """
    cache_version = None
    json_cache = {}

    # Check if cache_file includes a directory path
    if not os.path.dirname(cache_file):
        cache_file = os.path.join(DATA_PATH, cache_file)

    if cache_name.strip().lower() != "data":
        cache_name = cache_name.strip() + " data"

    try:
        if os.path.exists(cache_file):
            json_cache = load_json(cache_file)
            
            cache_version = json_cache.get("version")
            # Remove 'version' key before returning.
            json_cache.pop("version", None)

            if not suppress:
                echo(f"{cache_name.capitalize()} loaded from cache: '{cache_file}' ({cache_version})")

            if backup_old and cache_version != Version.get():
                shutil.copy(cache_file, cache_file.replace(".json", "_old.json"))

    except json.JSONDecodeError as e:
        echo(f"Error decoding JSON file 'cache_file': {e}")

    except Exception as e:
        echo(f"Error getting {cache_name.lower()} '{cache_file}': {e}")

    if get_version:
        return json_cache, cache_version
    return json_cache


def clear_cache(cache_path=DATA_PATH, cache_name=None, suppress=False):
    """Clears the cache at a specified file path.

    Args:
        cache_path (str): File path of the cache to be deleted. Can be a single file, or entire folder. Must be a file or folder in 'scripts.core.constants.DATA_PATH'.
        cache_name (str, optional): String to be used in print statements. Should be a name for the type of cache, e.g. 'item'. Defaults to None.
        suppress (bool, optional): Suppress displaying print statements (errors still displayed). Defaults to False.
    """
    if cache_name:
        cache_name = cache_name + " cache"
    else:
        cache_name = "cache"
    try:
        if cache_path != DATA_PATH:
            cache_path = os.path.join(DATA_PATH, cache_path)

        # Check if it's a file or directory
        if os.path.exists(cache_path):
            if os.path.isdir(cache_path):
                shutil.rmtree(cache_path)  # Delete directory
                os.makedirs(cache_path)  # Recreate directory
            else:
                os.remove(cache_path)  # Delete file

        if not suppress:
            echo(f"{cache_name.capitalize()} cleared.")
    except Exception as e:
        echo(f"Error clearing {cache_name.lower()} '{cache_path}': {e}")


def echo(message):
    """Safely print if there's an instance of a tqdm progress bar"""
    if tqdm._instances:
        tqdm.write(f"{message}")
    else:
        print(f"{message}")