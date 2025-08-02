import hashlib
import json
from pathlib import Path

from scripts.core import config_manager as config, logger
from scripts.core import file_loading
from scripts.utils import color

SCRIPTS_DIR = Path(file_loading.get_scripts_dir())
LUA_DIR = Path(file_loading.get_lua_dir())

MEDIA_DIRS = [
    SCRIPTS_DIR,
    LUA_DIR
]


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
        from scripts.tools import diff
        cls.set(config.get_version())
        current = diff.scan_game_snapshot([SCRIPTS_DIR])
        previous = diff.load_snapshot(cls._version, name="scripts")

        if current != previous:
            print(color.warning("Detected a potential version change."))
            print(color.warning(f"Current version: {cls._version}"))
            new_version = input("Enter a new version number (leave blank to skip):\n> ").strip()

            if new_version:
                old_version = cls._version
                config.set('version', new_version)
                cls.set(new_version)
                logger.write(f"Version number updated to {new_version}.", True)
                diff.save_snapshot(current, new_version, "scripts")

                prompt = input("Would you like to compare versions? (Y/N): ").strip().lower()
                if prompt == 'y':
                    from scripts.parser import script_parser
                    script_parser.compare_script_versions()
                    diff.snapshot_diff(old_version, new_version, MEDIA_DIRS, name="media")

            else:
                print("Version update skipped.")
                diff.save_snapshot(current, cls._version, "scripts")
        else:
            diff.save_snapshot(current, cls._version, "scripts")

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
