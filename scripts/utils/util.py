from tqdm import tqdm
import json
import os


def echo(message):
    """Safely print if there's an instance of a tqdm progress bar"""
    if tqdm._instances:
        tqdm.write(f"{message}")
    else:
        print(f"{message}")


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