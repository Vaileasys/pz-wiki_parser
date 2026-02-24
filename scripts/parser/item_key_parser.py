"""
Parse ItemKey declarations from a Java file.
"""

import re
from pathlib import Path

from scripts.core import constants
from scripts.utils import echo
from scripts.core import cache

CLASS_RE = re.compile(r'public\s+static\s+class\s+(\w+)')
ITEM_RE = re.compile(
    r'public\s+static\s+final\s+ItemKey\s+(\w+)\s*=\s*\w+\("([^"]+)"\)'
)
JAVA_PATH = Path("output/ZomboidDecompiler/source/zombie/scripting/objects", "ItemKey.java")
OUTPUT_PATH = Path(constants.OUTPUT_DIR) / "item_keys.json"
RES_PATH = Path(constants.ITEM_KEY_PATH)


def parse_item_keys(java_path: Path) -> dict[str, dict[str, str]]:
    """
    Parse ItemKey declarations from a Java file and return a nested dictionary.
    """
    result: dict[str, dict[str, str]] = {}
    current_class: str | None = None

    for line in java_path.read_text(encoding="utf-8").splitlines():
        # Detect class
        class_match = CLASS_RE.search(line)
        if class_match:
            current_class = class_match.group(1)
            result.setdefault(current_class, {})
            continue

        if not current_class:
            continue

        # Detect ItemKey line
        item_match = ITEM_RE.search(line)
        if item_match:
            item_key, item_id = item_match.groups()
            result[current_class][item_id] = item_key

    return result


def main(update: bool = False):
    java_file = JAVA_PATH
    if java_file.exists():
        echo.info(f"Parsing ItemKey declarations from '{java_file}'...")
    else:
        echo.error(f"Java file '{java_file}' does not exist. Ensure you have setup and run the ZomboidDecompiler.")
        return
    
    data = parse_item_keys(java_file)
    
    cache.save_cache(data, OUTPUT_PATH.name, data_dir=OUTPUT_PATH.parent, suppress=True)
    echo.success(f"Item keys parsed and saved to '{OUTPUT_PATH}'.")
    
    while True:
        user_input = None
        if not update:
            user_input = input("Update the existings resource file? (Y/N): ").strip().lower()
        if user_input == "y" or update:
            echo.info(f"Updating resource file at '{RES_PATH}'...")
            cache.save_cache(data, RES_PATH.name, data_dir=RES_PATH.parent, suppress=True)
            echo.success("Resource file updated.")
            break
        elif user_input == "n":
            break
        else:
            echo.error("Invalid input. Please enter 'Y' or 'N'.")


if __name__ == "__main__":
    main()
