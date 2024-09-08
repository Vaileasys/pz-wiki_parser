from scripts.core import config_manager, logging_file

# Version is stored in config.ini. This will update when changed in the script.
version_number = None

def get_version():
    global version_number
    # If version_number isn't defined, we update it
    if version_number is None:
        update_version()
    return version_number


def set_version(new_version):
    global version_number
    version_number = new_version


def update_version():
    """Update version to latest config entry"""
    set_version(config_manager.get_config('version'))


def change_version():
    new_version = input("Enter the new version number:\n> ").strip()
    config_manager.set_config('version', new_version)
    update_version()
    logging_file.log_to_file(f"Version number updated to {new_version}.", True)

def main():
    change_version()

if __name__ == "__main__":
    main()
