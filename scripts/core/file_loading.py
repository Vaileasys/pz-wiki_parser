"""
File Loading System

Provides utilities for mapping, locating, reading, and writing game-related files
(like scripts, lua, maps, clothing) under the game's media directory.
"""

import os
import shutil
from pathlib import Path
import hashlib
import json

from scripts.core import config_manager as config
from scripts.core.constants import OUTPUT_LANG_DIR, PROJECT_ROOT
from scripts.core.language import Language
from scripts.utils import echo

_game_file_map_cache = {}


def get_game_dir():
    """Return the base directory where the game is installed."""
    return config.get_game_directory()


def get_media_dir():
    """Return the path to the media folder within the game directory."""
    return os.path.join(get_game_dir(), "media")


def get_lua_dir():
    """Return the path to the 'media/lua' directory."""
    return os.path.join(get_media_dir(), "lua")


def get_scripts_dir():
    """Return the path to the 'media/scripts' directory."""
    return os.path.join(get_media_dir(), "scripts")


def get_maps_dir():
    """Return the path to the 'media/maps' directory."""
    return os.path.join(get_media_dir(), "maps")


def get_clothing_dir():
    """Return the path to the 'media/clothing' directory."""
    return os.path.join(get_media_dir(), "clothing")


BASE_MEDIA_DIRS = {
    "lua": get_lua_dir(),
    "scripts": get_scripts_dir(),
    "maps": get_maps_dir(),
    "clothing": get_clothing_dir(),
}


def map_dir(
    base_dir, extension=None, media_type="scripts", suppress=False, exclude_ext=None
):
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

    echo.info(f"Generating directory map for '{media_type}'...")

    BLACKLIST = {"tempNotWorking": {"folder": True, "type": "scripts"}}

    mapping = {}
    exclude_ext = set(exclude_ext or [])

    duplicate_cache = []

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [
            d
            for d in dirs
            if not (
                d in BLACKLIST
                and BLACKLIST[d]["folder"]
                and (
                    BLACKLIST[d]["type"] == media_type or BLACKLIST[d]["type"] == "all"
                )
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
                if not entry["folder"] and (
                    entry["type"] == media_type or entry["type"] == "all"
                ):
                    continue

            rel_path = os.path.relpath(os.path.join(root, file), base_dir).replace(
                os.path.sep, "/"
            )

            if name in mapping:
                mapping[name].append(rel_path)
                if not suppress:
                    if name not in duplicate_cache:
                        echo.warning(f"Duplicate file name detected: '{name}'")
                        duplicate_cache.append(name)
            else:
                mapping[name] = [rel_path]

    duplicate_cache.clear()

    return mapping


def map_game_files(suppress=False):
    from scripts.core.version import Version
    from scripts.core.cache import save_cache, load_cache

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
        maps = map_dir(
            get_maps_dir(),
            media_type="maps",
            suppress=suppress,
            exclude_ext=[".lotheader", ".png", ".bin", ".lotpack", ".zip", ".bak"],
        )
        clothing = map_dir(
            get_clothing_dir(), ".xml", media_type="clothing", suppress=suppress
        )

        mapping = {"scripts": scripts, "lua": lua, "maps": maps, "clothing": clothing}

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


## -------------------- Get files -------------------- ##


def get_files_by_type(
    filenames: str | list[str] = None,
    media_type: str = "scripts",
    prefer: str = None,
    prefix: str = None,
) -> list[str]:
    """
    Resolves filenames to absolute paths using the file map for the specified media type.

    Args:
        filenames (str or list[str], optional): File names (no extension or path). If None, includes all files.
        media_type (str): Media type ("lua", "scripts", "maps", "clothing", etc.).
        prefer (str, optional): Keyword to prioritise among duplicates.
        prefix (str, optional): Only include files starting with this prefix.

    Returns:
        list[str]: Absolute file paths.
    """
    file_map = get_game_file_map().get(media_type, {})
    paths = []

    base_dir = BASE_MEDIA_DIRS.get(media_type, get_media_dir())

    if filenames is None:
        filenames = list(file_map.keys())
    elif isinstance(filenames, str):
        filenames = [filenames]

    filenames = [n.replace("\\", "/") for n in filenames]

    for filename in filenames:
        filename_key = os.path.splitext(filename)[0]

        if prefix and not filename_key.startswith(prefix):
            continue

        rel_paths = get_file_paths(file_map, filename_key, prefer=prefer)
        if rel_paths:
            for rel_path in rel_paths:
                abs_path = os.path.join(base_dir, rel_path)
                paths.append(abs_path)
        else:
            echo.warning(
                f"{media_type.capitalize()} file '{filename}' not found in map."
            )

    return sorted(paths)


def get_script_files(
    filenames: str | list[str] = None,
    media_type: str = "scripts",
    prefer: str = None,
    prefix: str = None,
) -> list[str]:
    """Return absolute paths to script files, filtering by filenames, duplicates, or prefix."""
    return get_files_by_type(
        filenames, media_type=media_type, prefer=prefer, prefix=prefix
    )


def get_lua_files(
    filenames: str | list[str] = None, media_type: str = "lua", prefer: str = None
) -> list[str]:
    """Return absolute paths to Lua files, optionally filtering by name or preference keyword."""
    return get_files_by_type(filenames, media_type=media_type, prefer=prefer)


def get_clothing_files(
    filenames: str | list[str] = None, media_type: str = "clothing", prefer: str = None
) -> list[str]:
    """Return absolute paths to clothing XML files, with optional name or preference filtering."""
    return get_files_by_type(filenames, media_type=media_type, prefer=prefer)


## -------------------- Get rel path -------------------- ##


def get_relpath_by_type(name: str, media_type: str, prefer: str = None) -> str | None:
    """
    Retrieves the relative path to a file by name, as stored in the file map for the specified media type.

    Args:
        name (str): The filename without extension.
        media_type (str): Media type ("lua", "scripts", "maps", "clothing", etc.).
        prefer (str, optional): Keyword to prioritise among duplicates.

    Returns:
        str | None: The relative file path if found, else None.
    """
    file_map = get_game_file_map().get(media_type, {})
    rel_paths = get_file_paths(file_map, name, prefer=prefer)
    return rel_paths[0].replace("\\", "/") if rel_paths else None


def get_script_relpath(name: str, prefer: str = None) -> str | None:
    """Return the relative path of a script file by name, optionally prioritising a substring."""
    return get_relpath_by_type(name, media_type="scripts", prefer=prefer)


def get_lua_relpath(name: str, prefer: str = None) -> str | None:
    """Return the relative path of a Lua file by name, optionally prioritising a substring."""
    return get_relpath_by_type(name, media_type="lua", prefer=prefer)


def get_clothing_relpath(name: str, prefer: str = None) -> str | None:
    """Return the relative path of a clothing file by name, optionally prioritizing a substring."""
    return get_relpath_by_type(name, media_type="clothing", prefer=prefer)


## -------------------- Get abs path -------------------- ##


def get_abs_path_by_type(name: str, media_type: str, prefer: str = None) -> str | None:
    """
    Retrieves the absolute path to a file by name for the specified media type.

    Args:
        name (str): The filename without extension.
        media_type (str): Media type ("lua", "scripts", "maps", "clothing", etc.).
        prefer (str, optional): Keyword to prioritise among duplicates.

    Returns:
        str | None: The absolute file path if found, otherwise None.
    """
    rel_path = get_relpath_by_type(name, media_type, prefer=prefer)
    if rel_path:
        base_dir = BASE_MEDIA_DIRS.get(
            media_type, get_media_dir()
        )  # fallback to media root if unknown
        return os.path.join(base_dir, rel_path.replace("/", os.sep))
    return None


def get_script_path(
    name: str, media_type: str = "scripts", prefer: str = None
) -> str | None:
    """Return the absolute path to a script file by name, optionally prioritizing a substring."""
    return get_abs_path_by_type(name, media_type=media_type, prefer=prefer)


def get_lua_path(name: str, media_type: str = "lua", prefer: str = None) -> str | None:
    """Return the absolute path to a Lua file by name, optionally prioritizing a substring."""
    return get_abs_path_by_type(name, media_type=media_type, prefer=prefer)


def get_clothing_path(
    name: str, media_type: str = "clothing", prefer: str = None
) -> str | None:
    """Return the absolute path to a clothing file by name, optionally prioritizing a substring."""
    return get_abs_path_by_type(name, media_type=media_type, prefer=prefer)


## -------------------- Helpers -------------------- ##


def build_file_map(base_dir: Path, name: str = "unknown") -> dict[str, Path]:
    """Get a mapping of relative file paths to absolute paths."""
    print(f"Building file map for {name}...")
    return {str(f.relative_to(base_dir)): f for f in base_dir.rglob("*") if f.is_file()}


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


## -------------------- General file access -------------------- ##


def load_json(path: str) -> dict:
    """Load JSON data from a file. Returns empty dict on failure."""
    if not os.path.exists(path):
        echo.warning(f"Failed to load JSON from {path} – path does not exist")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as e:
        echo.warning(f"Failed to load JSON from {path} – {e}")
        return {}


def save_json(path: str, data: dict) -> bool:
    """Save dictionary data to a JSON file. Returns True if successful."""
    try:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except OSError as e:
        echo.error(f"Could not write to {path} – {e}")
        return False


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
        echo.warning(f"File not found or is a directory: {path}")
    except PermissionError:
        echo.warning(f"Permission denied: {path}")
    except UnicodeDecodeError:
        echo.warning(f"Could not decode file as UTF-8: {path}")
    except OSError as e:
        echo.warning(f"OS error while reading {path}: {e}")

    return ""


def write_file(
    content: list[str],
    rel_path: str = "output.txt",
    root_path: str = OUTPUT_LANG_DIR,
    suppress: bool = False,
):
    """
    Writes content to a file, creating directories as needed.

    Args:
        content (list[str]): A list of strings to write to the file.
        rel_path (str): Relative path where the file will be saved. If no file extension is given, it's treated as a directory.
        root_path (str): Root path to prepend to `rel_path`. {language_code} will be formatted to current language code.
        clear_root (bool): If True, deletes all contents under `root_path` before writing.
        suppress (bool): If True, suppresses info messages.

    Returns:
        Path: Directory where the file was saved.
    """
    output_path = Path(root_path.format(language_code=Language.get())) / rel_path
    output_dir = output_path.parent if output_path.suffix else output_path
    output_dir.mkdir(parents=True, exist_ok=True)

    if output_path.suffix:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write("\n".join(content))
        if not suppress:
            echo.info(f"File saved to '{output_path}'")
    else:
        echo.error(f"No file written. '{output_path}' appears to be a directory.")

    return output_dir


def load_file(rel_path, root_path=None):
    """
    Load a text file and return its lines as a list.

    Args:
        rel_path (str): Relative path to the file.
        root_path (str, optional): Root directory to join with rel_path. Defaults to 'OUTPUT_LANG_DIR'.

    Returns:
        list[str]: List of lines from the file, or an empty list if not found.
    """
    if root_path is None:
        root_path = os.path.join(OUTPUT_LANG_DIR)

    path = Path(root_path.format(language_code=Language.get())) / rel_path

    if os.path.exists(path):
        file_str = read_file(path)
        return file_str.splitlines()
    return []


def clear_dir(directory: str = OUTPUT_LANG_DIR, suppress: bool = False) -> Path:
    """
    Delete the contents of a directory at `root_path/rel_path`.
    Only deletes contents under `PROJECT_ROOT`.

    Args:
        directory (str): Directory to clear (automatically formats `language_code`).
        suppress (bool): If True, suppress warning/info messages.

    Returns:
        Path: The absolute path to the directory that was cleared.
    """
    # Build rel and abs paths
    root_rel = Path(directory.format(language_code=Language.get()))
    root_abs = root_rel.resolve()

    if not root_abs.exists():
        # Ensure it's in the project root before creating
        try:
            root_abs.relative_to(PROJECT_ROOT)
        except ValueError:
            if not suppress:
                echo.warning(f"Skipping clear: '{root_rel}' is outside project root.")
            return root_abs

        # Create the directory if it doesn't exist
        root_abs.mkdir(parents=True, exist_ok=True)
        if not suppress:
            echo.info(f"Created directory: '{root_rel}'")
        return root_abs

    # Ensure it's in the project root
    try:
        root_abs.relative_to(PROJECT_ROOT)
    except ValueError:
        if not suppress:
            echo.warning(f"Skipping clear: '{root_rel}' is outside project root.")
        return root_abs

    # Delete contents
    for child in root_abs.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()

    if not suppress:
        echo.info(f"Cleared contents of '{root_rel}'")

    return root_abs


if __name__ == "__main__":
    #    print(get_game_file_map())
    result = map_game_files()
    echo.success(
        f"Mapped {len(result['scripts'])} script files, {len(result['lua'])} lua files and {len(result['maps'])} maps files."
    )
