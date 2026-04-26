import re
from pathlib import Path

from scripts.core import constants, cache
from scripts.utils import echo

CLASS_RE = re.compile(r'public\s+static\s+class\s+(\w+)')
GAME_VERSION_RE = re.compile(r'GameVersion\s+gameVersion\s*=\s*new\s+GameVersion\((\d+),\s*(\d+),\s*"([^"]*)"\)')
BUILD_VERSION_RE = re.compile(r'private\s+static\s+final\s+int\s+buildVersion\s*=\s*(\d+)')


def parse_game_version()  -> list[int, int, int]:
    """Parse game version from Core.java."""
    java_path = Path("output/ZomboidDecompiler/source/zombie/core", "Core.java")
    if not java_path.exists():
        echo.error(f"Java file '{java_path}' does not exist. Ensure you have setup and run the ZomboidDecompiler.")
        return []
    
    text = java_path.read_text(encoding="utf-8")
    
    game_version = GAME_VERSION_RE.search(text)
    build_version = BUILD_VERSION_RE.search(text)
    
    if not game_version:
        echo.error("Could not find 'GameVersion' in 'Core.java'.")
        return []
    
    major, minor, _ = game_version.groups()
    build = int(build_version.group(1)) if build_version else 0
    
    return [int(major), int(minor), build]


def parse_static_registry(java_path: Path, java_type: str, *, grouped: bool = False) -> dict:
    """Parse static final declarations of a given Java type.
    
    Extracts constant names and their string values from a Java file.

    Args:
        java_path (Path): Path to the Java file.
        java_type (str): The Java type to parse.
        grouped (bool, optional): Whether to group constants by their enclosing class. Defaults to False.

    Returns:
        dict: A dictionary mapping constant values to their names, optionally grouped by class.
    """
    declaration_re = re.compile(rf'public\s+static\s+final\s+{re.escape(java_type)}\s+(\w+)\s*=\s*\w+\("([^"]+)"\)')
    
    data = {}
    current_class: str | None = None
    
    for line in java_path.read_text(encoding="utf-8").splitlines():
        class_match = CLASS_RE.search(line)
        if class_match:
            current_class = class_match.group(1)
            if grouped:
                data.setdefault(current_class, {})
            continue

        match = declaration_re.search(line)
        if not match:
            continue
        
        key, value = match.groups()
        
        if grouped:
            if current_class:
                data.setdefault(current_class, {})[value] = key
        else:
            data[value] = key
        
    return data

def process_registry(
    java_type: str,
    java_path: Path,
    output_path: Path,
    res_path: Path,
    *,
    grouped: bool = False,
    is_update: bool = False,
    label: str | None = None,
    do_flip: bool = False
    ) -> dict:
    label = label or java_type
    
    if not java_path.exists():
        echo.error(f"Java file '{java_path}' does not exist. Ensure you have setup and run the ZomboidDecompiler.")
        return {}
    
    echo.info(f"Parsing {label} declarations from '{java_path}'...")
    
    data = parse_static_registry(java_path, java_type, grouped=grouped)
    
    cache.save_cache(data, output_path.name, data_dir=output_path.parent, suppress=True)
    echo.success(f"{label} parsed and saved to '{output_path}'.")
    
    while True:
        user_input = None
        if not is_update:
            user_input = input(f"Do you want to update the '{label}' resource file? (Y/N)\n> ").strip().lower()
        
        if user_input == "y" or is_update:
            echo.info(f"Updating {label} resource file at '{res_path}'...")
            cache.save_cache(data, res_path.name, data_dir=res_path.parent, suppress=True)
            echo.success(f"{label} resource file updated.")
            break
        
        if user_input == "n":
            break
        
        echo.error("Invalid input. Please enter 'Y' or 'N'.")
    
    return data

def update_item_keys(is_update: bool = False) -> dict:
    java_path = Path("output/ZomboidDecompiler/source/zombie/scripting/objects", "ItemKey.java")
    return process_registry(
        java_type = "ItemKey",
        java_path = java_path,
        output_path = Path(constants.OUTPUT_DIR) / "item_keys.json",
        res_path = Path(constants.ITEM_KEY_PATH),
        grouped = True,
        is_update = is_update
    )

def update_item_body_locations(is_update: bool = False) -> dict:
    java_path = Path("output/ZomboidDecompiler/source/zombie/scripting/objects", "ItemBodyLocation.java")
    return process_registry(
        java_type = "ItemBodyLocation",
        java_path = java_path,
        output_path = Path(constants.OUTPUT_DIR) / "item_body_locations.json",
        res_path = Path(constants.ITEM_BODY_LOCATIONS_PATH),
        is_update = is_update
    )

def main(is_update: bool = False):
    update_item_keys(is_update=is_update)
    update_item_body_locations(is_update=is_update)

if __name__ == "__main__":
    main()