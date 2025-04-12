import os
import shutil
import json
import re
from scripts.core.constants import DATA_PATH
from scripts.core.version import Version
from scripts.utils.echo import echo_success, echo_error, echo_warning, echo_info


def load_json(path:str) -> dict:
    """Load JSON data from a file. Returns empty dict on failure."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as e:
        echo_warning(f"Failed to load JSON from {path} – {e}")
        return {}


def save_json(path:str, data:dict) -> bool:
    """Save dictionary data to a JSON file. Returns True if successful."""
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except OSError as e:
        echo_error(f"Could not write to {path} – {e}")
        return False


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
        echo_info(f"{cache_name.capitalize()} saved to '{data_file_path}'")


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
                echo_info(f"{cache_name.capitalize()} loaded from cache: '{cache_file}' ({cache_version})")

            if backup_old and cache_version != Version.get():
                shutil.copy(cache_file, cache_file.replace(".json", "_old.json"))

    except json.JSONDecodeError as e:
        echo_error(f"Failed to decode JSON file 'cache_file': {e}")

    except Exception as e:
        echo_error(f"Failed getting {cache_name.lower()} '{cache_file}': {e}")

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
            echo_success(f"{cache_name.capitalize()} cleared.")
    except Exception as e:
        echo_error(f"Failed clearing {cache_name.lower()} '{cache_path}': {e}")