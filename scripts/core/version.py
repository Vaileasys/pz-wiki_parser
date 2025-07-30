import hashlib
import json
from pathlib import Path

from scripts.core import config_manager as config, logger
from scripts.core.constants import DATA_DIR, SNAPSHOT_DIR
from scripts.core.file_loading import get_scripts_dir, get_lua_dir
from scripts.utils import color

SNAPSHOT_FILE = Path(DATA_DIR) / "media_snapshot.json"
SNAP_DIR = Path(SNAPSHOT_DIR)

SCRIPTS_DIR = Path(get_scripts_dir())
LUA_DIR = Path(get_lua_dir())

MEDIA_DIRS = [
    SCRIPTS_DIR,
    LUA_DIR
]

def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def _scan_game(directories: list[Path] = MEDIA_DIRS) -> dict[str, str]:
    all_files = {}
    for base_dir in directories:
        for f in base_dir.rglob("*"):
            if f.is_file():
                relative_path = str(f.relative_to(base_dir))
                key = f"{base_dir.name}/{relative_path}"
                all_files[key] = _hash_file(f)
    return all_files

def _load_snapshot(version: str, name: str = "media") -> dict[str, str]:
    path = get_snapshot_file(version, name)
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_snapshot(snapshot: dict[str, str], version: str, name: str = "media"):
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    path = get_snapshot_file(version, name)
    with path.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=4)

def _compare_snapshots(old: dict[str, str], new: dict[str, str]) -> dict[str, list[str]]:
    old_keys = set(old.keys())
    new_keys = set(new.keys())

    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    modified = sorted(k for k in (old_keys & new_keys) if old[k] != new[k])

    return {
        "added": added,
        "removed": removed,
        "modified": modified
    }

def get_snapshot_file(version: str, name: str = "media") -> Path:
    return SNAP_DIR / f"{name}_snapshot_v{version}.json"

def compare_versions(old_version: str, new_version: str, directories: list[Path] = MEDIA_DIRS, name: str = "media"):
    old_snapshot = _load_snapshot(old_version, name)
    new_snapshot_path = get_snapshot_file(new_version, name)

    if new_snapshot_path.exists():
        with new_snapshot_path.open("r", encoding="utf-8") as f:
            new_snapshot = json.load(f)
    else:
        print(color.warning(f"Snapshot for version {new_version} not found — generating and saving it now."))
        new_snapshot = _scan_game(directories)
        _save_snapshot(new_snapshot, new_version, name)

    if not old_snapshot:
        print(color.error(f"No snapshot found for version: {old_version}"))
        return

    changes = _compare_snapshots(old_snapshot, new_snapshot)
    output_lines = [f"Comparison: {name} snapshot v{old_version} -> v{new_version}"]

    for key in ("added", "removed", "modified"):
        entries = changes[key]
        header = f"\n{key.capitalize()} files ({len(entries)}):"
        output_lines.append(header)
        print(color.info(header))

        if entries:
            symbol = '+' if key == 'added' else '-' if key == 'removed' else '*'
            for f in entries:
                line = f"  {symbol} {f}"
                output_lines.append(line)
                print(color.info(line))
        else:
            output_lines.append("  None")
            print(color.info("  None"))

    # Write to file
    diff_path = SNAP_DIR / f"{name}_diff_v{old_version}_v{new_version}.txt"
    with diff_path.open("w", encoding="utf-8") as f:
        f.write('\n'.join(output_lines))

    print(color.success(f"\nSaved diff to {diff_path}"))

class Version:
    # Version is stored in config.ini. This will update when changed in the script.
    _version = None

    @classmethod
    def get(cls):
        """Returns the current version. If unset, pulls from config."""
        # If version_number isn't defined, we update it
        if cls._version is None:
            cls.update()
        return cls._version

    @classmethod
    def set(cls, new_version: str):
        cls._version = new_version

    @classmethod
    def update(cls):
        """Loads version from config and checks for changes."""
        cls.set(config.get_version())
        current = _scan_game([SCRIPTS_DIR])
        previous = _load_snapshot(cls._version)

        if current != previous:
            print(color.warning("Detected a potential version change."))
            print(color.warning(f"Current version: {cls._version}"))
            new_version = input("Enter a new version number (leave blank to skip):\n> ").strip()

            if new_version:
                old_version = cls._version
                config.set('version', new_version)
                cls.set(new_version)
                logger.write(f"Version number updated to {new_version}.", True)
                _save_snapshot(current, new_version, "scripts")

                prompt = input("Would you like to compare versions? (Y/N): ").strip().lower()
                if prompt == 'y':
                    compare_versions(old_version, new_version, MEDIA_DIRS, name="media")

            else:
                print("Version update skipped.")
                _save_snapshot(current, cls._version, "scripts")
        else:
            _save_snapshot(current, cls._version, "scripts")

    @classmethod
    def change(cls):
        """Prompts the user for a new version number and updates it."""
        new_version = input("Enter the new version number:\n> ").strip()
        config.set('version', new_version)
        cls.update()
        logger.write(f"Version number updated to {new_version}.", True)

    @classmethod
    def main(cls):
        cls.change()


def main():
    Version.main()

if __name__ == "__main__":
    Version.main()
