from scripts.core import config_manager, logger

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
        """Loads version from config."""
        cls.set(config_manager.get_config('version'))

    @classmethod
    def change(cls):
        """Prompts the user for a new version number and updates it."""
        new_version = input("Enter the new version number:\n> ").strip()
        config_manager.set_config('version', new_version)
        cls.update()
        logger.write(f"Version number updated to {new_version}.", True)

    @classmethod
    def main(cls):
        cls.change()


if __name__ == "__main__":
    Version.main()
