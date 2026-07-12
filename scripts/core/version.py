from pathlib import Path
import re

from scripts.core import config_manager as config, logger, file_loading
from scripts.parser.java_parser import update_resources
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
    _parsed_version = None

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
    def parsed_version(cls, update: bool = False):
        """Parses the version from the decompiled game. Requires ZomboidDecompiler."""
        
        from scripts.parser.java_parser import parse_game_version
        
        parsed_version = parse_game_version()
        
        cls._parsed_version = f"{parsed_version[0]}.{parsed_version[1]}.{parsed_version[2]}"
        
        if update:
            cls.set(cls._parsed_version)
            config.set('version', cls._parsed_version)
        
        return cls._parsed_version

    @classmethod
    def update(cls):
        """Loads version from config and checks for changes."""
        from scripts.tools import diff
        cls.set(config.get_version())
        current = diff.scan_game_snapshot([SCRIPTS_DIR])
        previous = diff.load_snapshot(cls._version, name="scripts")
        decompiled = False

        if current != previous:
            print(color.warning("Detected a potential version change."))
            print(color.warning(f"Current version: {cls._version}"))
            
            options = [
                f"1. Parse the version from the decompiled game. {color.style('[requires ZomboidDecompiler]', color.BRIGHT_YELLOW)}",
                "2. Manually enter a new version number.",
                "3. Skip (keep current version)."
                ]
            
            while True:
                print("\nHow would you like to update the version number?")
                choice = input("\n".join(options) + "\n> ").strip().lower()
                
                try:
                    if int(choice) in range(1, 4):
                        break
                except ValueError:
                    pass
                print("Invalid choice.")
                
            if choice == "1":
                from scripts.core.runner import run_zomboid_decompiler
                failed = run_zomboid_decompiler()
                if not failed:
                    new_version = cls.parsed_version(update=True)
                    decompiled = True
                else:
                    new_version = None
            elif choice == "2":
                new_version = input("Enter a new version number:\n> ").strip()
            else:
                new_version = None

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
            
            if new_version and decompiled:
                update_resources()
                
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
