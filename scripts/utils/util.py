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