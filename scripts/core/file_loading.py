# File loading system

import os
from pathlib import Path
from scripts.core import config_manager
from scripts.core.constants import OUTPUT_PATH
from scripts.core.language import Language
from scripts.core.version import Version
from scripts.core.cache import save_cache, load_cache
from scripts.utils.echo import echo, echo_warning, echo_success, echo_error, ignore_warnings

#ignore_warnings()

_game_file_map_cache= {}

def get_game_dir():
    return config_manager.get_config("game_directory")

def get_media_dir():
    return f"{get_game_dir()}\\media"

def get_lua_dir():
    return f"{get_media_dir()}\\lua"

def get_scripts_dir():
    return f"{get_media_dir()}\\scripts"

def get_maps_dir():
    return f"{get_media_dir()}\\maps"


def map_dir(base_dir, extension=None, media_type="scripts", suppress=False, exclude_ext=None):
    """
    Maps all files with the given extension in a directory.

    Args:
        base_dir (str): Directory to scan.
        extension (str): File extension to include.
        media_type (str): Media type this map is for ("scripts", "lua").
        suppress (bool): If True, hides duplicate warnings.

    Returns:
        dict[str, list[str]]: {filename: [relative_paths]}
    """

    BLACKLIST = {
        "tempNotWorking": {"folder": True, "type": "scripts"}
    }

    mapping = {}
    exclude_ext = set(exclude_ext or [])

    duplicate_cache = []

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [
            d for d in dirs
            if not (
                d in BLACKLIST and BLACKLIST[d]["folder"]
                and (BLACKLIST[d]["type"] == media_type or BLACKLIST[d]["type"] == "all")
            )
        ]

        
        for file in files:
            if extension and not file.endswith(extension):
                continue

            if any(file.endswith(ext) for ext in exclude_ext):
                continue

            name = os.path.splitext(file)[0]

            # Skip blacklisted files
            if name in BLACKLIST:
                entry = BLACKLIST[name]
                if not entry["folder"] and (entry["type"] == media_type or entry["type"] == "all"):
                    continue

            rel_path = os.path.relpath(os.path.join(root, file), base_dir).replace("\\", "/")

            if name in mapping:
                mapping[name].append(rel_path)
                if not suppress:
                    if name not in duplicate_cache:
                        echo_warning(f"Duplicate file name detected: '{name}'")
                        duplicate_cache.append(name)
            else:
                mapping[name] = [rel_path]
                
    duplicate_cache.clear()

    return mapping


def map_game_files(suppress=False):
    """
    Maps script and lua files, then saves to cache.

    Args:
        suppress (bool): If True, hides duplicate warnings.

    Returns:
        dict: {'scripts': ..., 'lua': ...}
    """
    global _game_file_map_cache

    loaded_cache, cache_version = load_cache("game_file_map.json", get_version=True)

    if cache_version != Version.get():
        scripts = map_dir(get_scripts_dir(), ".txt", "scripts", suppress=suppress)
        lua = map_dir(get_lua_dir(), ".lua", "lua", suppress=suppress)
        maps = map_dir(get_maps_dir(), media_type="maps", suppress=suppress, exclude_ext=[".lotheader", ".png", ".bin", ".lotpack", ".zip", ".bak"])

        mapping = {
            "scripts": scripts,
            "lua": lua,
            "maps": maps
        }

        _game_file_map_cache = mapping
        save_cache(mapping, "game_file_map.json", suppress=suppress)
    else:
        mapping = loaded_cache

    return mapping


def get_file_paths(mapping: dict, filename: str, *, prefer=None) -> list[str]:
    """
    Returns all matching file paths from the mapping, optionally filtered by keyword.

    Args:
        mapping (dict): Output from map_dir().
        filename (str): Filename without extension.
        prefer (str, optional): Keyword to prioritise in path.

    Returns:
        list[str]: All matching paths (may be empty).
    """
    filename = os.path.splitext(filename)[0]
    paths = mapping.get(filename, [])

    if prefer:
        preferred = [p for p in paths if prefer in p]
        if preferred:
            return preferred

    return paths


def get_game_file_map() -> dict:
    """
    Returns the cached game file map. Loads from disk once if needed.

    Returns:
        dict: {'scripts': ..., 'lua': ...}
    """
    global _game_file_map_cache
    if not _game_file_map_cache:
        _game_file_map_cache = map_game_files()
    return _game_file_map_cache


def get_lua_files(filenames: str | list[str], prefer: str = None, media_type: str = "lua") -> list[str]:
    """
    Resolves base Lua filenames to absolute paths using the file map.

    Args:
        filenames (str or list[str]): Lua file names (no extension or path).
        prefer (str, optional): Keyword to prioritise among duplicates.
        media_type (str): Media type ("lua", "scripts", etc.).

    Returns:
        list[str]: Absolute file paths.
    """
    if isinstance(filenames, str):
        filenames = [filenames]

    filenames = [n.replace("\\", "/") for n in filenames]
    lua_map = get_game_file_map().get(media_type, {})
    paths = []

    base_dir = {"lua": get_lua_dir(), "scripts": get_scripts_dir(), "maps": get_maps_dir()}
    base_dir = base_dir.get(media_type, get_lua_dir())

    for filename in filenames:
        filename_lower = filename.lower()
        is_lua_file = filename_lower.endswith(".lua")
        filename_key = os.path.splitext(filename)[0]

        if is_lua_file:
            rel_paths = get_file_paths(lua_map, filename_key, prefer=prefer)
            if rel_paths:
                for rel_path in rel_paths:
                    abs_path = os.path.join(base_dir, rel_path)
                    paths.append(abs_path)
            else:
                echo_warning(f"Lua file '{filename}' not found in map.")
        else:
            folder_matches = []
            for rel_paths in lua_map.values():
                for rel_path in rel_paths:
                    if rel_path.lower().startswith(f"{filename_lower}/"):
                        folder_matches.append(os.path.join(base_dir, rel_path))

            if folder_matches:
                paths.extend(folder_matches)
            else:
                echo_warning(f"Lua folder '{filename}' not found in map.")

    return paths


def get_script_files(prefix: str = None) -> list[str]:
    """
    Retrieves a list of script .txt files from the game scripts folder, optionally filtering by prefix.

    Args:
        prefix (str | None): Only files starting with this prefix will be included. If None, all .txt files are included.

    Returns:
        list[str]: List of absolute file paths.
    """
    script_files = []
    for root, _, files in os.walk(get_scripts_dir()):
        for file in files:
            if file.endswith(".txt") and (prefix is None or file.startswith(prefix)):
                script_files.append(os.path.join(root, file))
    return sorted(script_files)


def get_script_relpath(name: str, prefer: str = None) -> str | None:
    """
    Retrieves the relative path to a script (.txt) file by name, as stored in the file map.

    Args:
        name (str): The filename without extension (e.g., "AssaultRifle").
        prefer (str, optional): Keyword to prioritise among duplicates (e.g., "weapons").

    Returns:
        str | None: The relative file path (e.g., "weapons/AssaultRifle.txt") if found, else None.
    """
    file_map = get_game_file_map().get("scripts", {})
    rel_paths = get_file_paths(file_map, name, prefer=prefer)
    return rel_paths[0].replace("/", "\\") if rel_paths else None


def get_lua_relpath(name: str, prefer: str = None) -> str | None:
    """
    Retrieves the relative path to a Lua (.lua) file by name, as stored in the file map.

    Args:
        name (str): The filename without extension (e.g., "ISInventoryPage").
        prefer (str, optional): Keyword to prioritise among duplicates (e.g., "client").

    Returns:
        str | None: The relative file path (e.g., "client/ISInventoryPage.lua") if found, else None.
    """
    file_map = get_game_file_map().get("lua", {})
    rel_paths = get_file_paths(file_map, name, prefer=prefer)
    return rel_paths[0].replace("\\", "/") if rel_paths else None


def get_script_path(name: str, prefer: str = None) -> str | None:
    """
    Retrieves the absolute path to a script (.txt) file by name.

    Args:
        name (str): The filename without extension (e.g., "AssaultRifle").
        prefer (str, optional): Keyword to prioritise among duplicates (e.g., "weapons").

    Returns:
        str | None: The absolute file path if found, otherwise None.
    """
    rel_path = get_script_relpath(name, prefer=prefer)
    if rel_path:
        return os.path.join(get_scripts_dir(), rel_path.replace("/", "\\"))
    return None

def get_lua_path(name: str, prefer: str = None) -> str | None:
    """
    Retrieves the absolute path to a Lua (.lua) file by name.

    Args:
        name (str): The filename without extension (e.g., "ISInventoryPage").
        prefer (str, optional): Keyword to prioritise among duplicates (e.g., "client").

    Returns:
        str | None: The absolute file path if found, otherwise None.
    """
    rel_path = get_lua_relpath(name, prefer=prefer)
    if rel_path:
        return os.path.join(get_lua_dir(), rel_path.replace("/", "\\"))
    return None


def read_file(path: str) -> str:
    """
    Reads the contents of a file as a string.

    Args:
        path (str): Path to the file.

    Returns:
        str: File contents.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, IsADirectoryError):
        echo_warning(f"File not found or is a directory: {path}")
    except PermissionError:
        echo_warning(f"Permission denied: {path}")
    except UnicodeDecodeError:
        echo_warning(f"Could not decode file as UTF-8: {path}")
    except OSError as e:
        echo_warning(f"OS error while reading {path}: {e}")
    
    return ""


def write_file(content:list, rel_path="output.txt", suppress=False):
    """
    Writes content to a file, creating directories as needed.

    :param list content: A list of strings to write to the file.
    :param str rel_path: The relative path where the file will be saved. If no file extension is given, the path is treated as a directory.
    :return: The directory the file is saved to.
    """
    output_path = Path(OUTPUT_PATH) / Language.get() / rel_path
    output_dir = output_path.parent if output_path.suffix else output_path
    output_dir.mkdir(parents=True, exist_ok=True)

    if output_path.suffix:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(content))

        if not suppress:
            echo(f"File saved to '{output_path}'")
        
    else:
        echo_error(f"No file written. '{output_path}' appears to be a directory.")
    
    return output_dir


if __name__ == "__main__":
#    print(get_game_file_map())
    result = map_game_files()
    echo_success(f"Mapped {len(result['scripts'])} script files, {len(result['lua'])} lua files and {len(result['maps'])} maps files.")