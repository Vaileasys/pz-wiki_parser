import hashlib
import json
from pathlib import Path

from scripts.core import config_manager as config, logger
from scripts.core.constants import DATA_DIR
from scripts.core.file_loading import get_scripts_dir, get_lua_dir
from scripts.utils import color

SNAPSHOT_FILE = Path(DATA_DIR) / "media_snapshot.json"

MEDIA_DIRS = [
    Path(get_scripts_dir()),
#    Path(get_lua_dir())
]

def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def _scan_game() -> dict[str, str]:
    all_files = {}
    for base_dir in MEDIA_DIRS:
        for f in base_dir.rglob("*"):
            if f.is_file():
                relative_path = str(f.relative_to(base_dir))
                key = f"{base_dir.name}/{relative_path}"
                all_files[key] = _hash_file(f)
    return all_files

def _load_snapshot() -> dict[str, str]:
    if SNAPSHOT_FILE.exists():
        with SNAPSHOT_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_snapshot(snapshot: dict[str, str]):
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SNAPSHOT_FILE.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

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
        current = _scan_game()
        previous = _load_snapshot()

        if current != previous:
            print(color.warning("Detected a potential version change."))
            print(color.warning(f"Current version: {cls._version}"))
            new_version = input("Enter a new version number (leave blank to skip):\n> ").strip()

            if new_version:
                config.set('version', new_version)
                cls.set(new_version)
                logger.write(f"Version number updated to {new_version}.", True)
            else:
                print("Version update skipped.")

        _save_snapshot(current)

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
