import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import difflib

from scripts.core import file_loading, constants, config_manager as cfg
from scripts.utils import echo

FILE_TYPES = (".txt", ".lua")


def generate_line_diff(old_path: Path, new_path: Path) -> list[dict] | bool:
    """Return grouped diff blocks with full 'old' and 'new' line lists."""
    try:
        old_lines = old_path.read_text(encoding="utf-8").splitlines()
        new_lines = new_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return True

    matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
    blocks = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue

        block = {
            "start_line_old": i1 + 1,
            "start_line_new": j1 + 1,
            "old": old_lines[i1:i2] if tag in ("replace", "delete") else [],
            "new": new_lines[j1:j2] if tag in ("replace", "insert") else []
        }

        blocks.append(block)

    return blocks or True


def compare_dirs(
    old: dict[str, str],
    new: dict[str, str],
    max_workers: int | None = None,
    use_snapshots: bool = False
    ) -> dict[str, list[str] | dict[str, dict[int, dict[str, str]] | bool]]:
    """
    Compare two directories and return a dict with added, removed, and changed files.
    Includes line-by-line diffs for .lua and .txt files.
    """
    old_dir = Path(old.get("path"))
    new_dir = Path(new.get("path"))

    if use_snapshots:
        old_files = file_loading.load_json(old["path"])
        new_files = file_loading.load_json(new["path"])
    else:
        old_files = file_loading.build_file_map(old_dir, old.get("version"))
        new_files = file_loading.build_file_map(new_dir, new.get("version"))

    old_keys = set(old_files)
    new_keys = set(new_files)

    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    common = sorted(old_keys & new_keys)

    modified: dict[str, dict[int, dict[str, str]] | bool] = {}

    def compare_pair(path: str) -> tuple[str, dict[int, dict[str, str]] | bool] | None:
        old_path = old_files[path]
        new_path = new_files[path]

        # Snapshots are hashes
        if use_snapshots:
            if old_path != new_path:
                return path, True
            return None

        # Do file comparisons
        if file_loading.hash_file(old_path) != file_loading.hash_file(new_path):
            if path.endswith(FILE_TYPES):
                return path, generate_line_diff(old_path, new_path)
            return path, True
        return None
    
    max_workers = cfg.get_max_workers() if isinstance(cfg.get_max_workers(), int) else None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(compare_pair, path): path
            for path in common
        }

        with tqdm(total=len(futures), desc="Comparing files", unit=" files", bar_format=constants.PBAR_FORMAT, leave=False) as pbar:
            for future in as_completed(futures):
                path = futures[future]
                pbar.set_postfix_str(f"{path[:100]}{'...' if len(path) > 100 else ''}")
                result = future.result()
                if result:
                    path, diff = result
                    modified[path] = diff
                pbar.update(1)
        
        echo.success("File comparisons complted.")

    return {
        "added": added,
        "removed": removed,
        "modified": modified
    }


def save_diff_to_json(
    diff_data: dict[str, list[str] | dict[str, object]],
    old: dict[str, str],
    new: dict[str, str]
    ):
    """Save raw diff to JSON file."""
    old_version = old.get("version", "old")
    new_version = new.get("version", "new")

    output_file = f"diff_{old_version}_to_{new_version}.json"
    output_path = os.path.join(constants.DIFF_DIR, output_file)

    file_loading.save_json(output_path, diff_data)

    echo.success(f"Diff JSON saved to \"{output_path}\"")


def save_diff_to_txt(
    diff_data: dict[str, list[str] | dict[str, object]],
    old: dict[str, str],
    new: dict[str, str]
    ):
    """Save diff as a readable TXT summary."""
    old_version = old.get("version", "old")
    new_version = new.get("version", "new")

    rel_path = f"diff_{old_version}_to_{new_version}.txt"

    added = diff_data.get("added", [])
    removed = diff_data.get("removed", [])
    modified = sorted(diff_data.get("modified", {}).keys())

    content = []
    content.append(f"Comparison: media snapshot v{old_version} -> v{new_version}")
    content.append("")

    content.append(f"Added files ({len(added)}):")
    for path in added:
        content.append(f"  + {path}")
    content.append("")

    content.append(f"Removed files ({len(removed)}):")
    for path in removed:
        content.append(f"  - {path}")
    content.append("")

    content.append(f"Modified files ({len(modified)}):")
    for path in modified:
        content.append(f"  * {path}")
    content.append("")

    file_loading.write_file(content, rel_path=rel_path, root_path=constants.DIFF_DIR)


## ------ COMPARE SNAPSHOTS ------ ##

SNAPSHOT_FILE = Path(constants.DATA_DIR) / "media_snapshot.json"
SNAP_DIR = Path(constants.SNAPSHOT_DIR)

SCRIPTS_DIR = Path(file_loading.get_scripts_dir())
LUA_DIR = Path(file_loading.get_lua_dir())

MEDIA_DIRS = [
    SCRIPTS_DIR,
    LUA_DIR
]

def get_snapshot_file(version: str, name: str = "media") -> Path:
    return SNAP_DIR / f"{name}_snapshot_v{version}.json"

def scan_game_snapshot(directories: list[Path] = MEDIA_DIRS) -> dict[str, str]:
    all_files = {}
    for base_dir in directories:
        for f in base_dir.rglob("*"):
            if f.is_file():
                relative_path = str(f.relative_to(base_dir))
                key = f"{base_dir.name}/{relative_path}"
                all_files[key] = file_loading.hash_file(f)
    return all_files

def load_snapshot(version: str, name: str = "media") -> dict[str, str]:
    path = get_snapshot_file(version, name)
    if path.exists():
        return file_loading.load_json(str(path))
    return {}

def save_snapshot(snapshot: dict[str, str], version: str, name: str = "media"):
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    path = get_snapshot_file(version, name)
    return file_loading.save_json(str(path), snapshot)


def snapshot_diff(old_version: str, new_version: str, directories: list[Path], name: str = "media") -> list[str]:
    """Loads snapshots and runs a `compare_dirs()` style diff."""
    old_path = get_snapshot_file(old_version, name)
    new_path = get_snapshot_file(new_version, name)

    if not old_path.exists():
        echo.warning(f"Snapshot for version {old_version} not found - generating one for {new_version}.")
        snapshot = scan_game_snapshot(directories)
        save_snapshot(snapshot, new_version, name)
        return []
    
    snapshot = scan_game_snapshot(directories)
    save_snapshot(snapshot, new_version, name)

    old = {"version": old_version, "path": str(old_path)}
    new = {"version": new_version, "path": str(new_path)}

    # Patch `compare_dirs` to work with JSON maps instead of file trees
    diff_data = compare_dirs(old, new, use_snapshots=True)

    save_diff_to_txt(diff_data, old, new)
    return diff_data


def main():
    old_version = input("Enter first version (old):\n> ")
    old_path = input(f"Enter path for {old_version} (old):\n> ")
    new_version = input("Enter second version (new):\n> ")
    new_path = input(f"Enter path for {new_version} (new):\n> ")

    old = {"version": str(old_version), "path": os.path.join(old_path)}
    new = {"version": str(new_version), "path": os.path.join(new_path)}

    diff = compare_dirs(old, new)
    save_diff_to_json(diff, old, new)
    save_diff_to_txt(diff, old, new)


if __name__ == "__main__":
    main()
