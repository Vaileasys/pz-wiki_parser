import os
import platform
from pathlib import Path
from scripts.core import config_manager as config
from scripts.utils import echo, color


def get_install_path():
    EXISTS_TAG = color.style("[exists]", color.BRIGHT_GREEN)
    PLATFORM_PATHS = {
        "Windows": [
            Path("C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid"),
            Path("C:/Program Files/Steam/steamapps/common/ProjectZomboid")
        ],
        "Linux": [
            Path.home() / ".steam/steam/steamapps/common/ProjectZomboid/projectzomboid",
            Path.home() / ".local/share/Steam/steamapps/common/ProjectZomboid/projectzomboid"
        ],
        "Darwin": [
            Path.home() / "Library/Application Support/Steam/steamapps/common/ProjectZomboid"
        ]
    }
    paths_list = PLATFORM_PATHS.get(platform.system(), [])
    count = len(paths_list)

    print("Please select your install location:")
    for i, path in enumerate(paths_list, start=1):
        status = EXISTS_TAG if path.exists() else ""
        print(f"{i}: {str(path)} {status}")
    print(f"{count+1}: Other")

    try: #TODO: consider returning Path object.
        choice = int(input("> ").strip())
        if 0 < choice < count+1:
            selected_path = paths_list[choice-1]
            if selected_path.exists():
                return selected_path
            else:
                echo.error("That path doesn't exist on your system.")
                return get_install_path()
        elif choice == count+1:
            manual_path = Path(input("Please enter the install location: ").strip())
            if manual_path.exists():
                return manual_path
            else:
                echo.error("That path doesn't exist.")
                return get_install_path()
        else:
            raise ValueError
    except ValueError:
        echo.error("Invalid choice, please try again.")
        return get_install_path()


def verify_media_directory(install_path):
    """Verify that the media directory exists in the game installation."""
    media_dir = os.path.join(install_path, 'media')
    if not os.path.exists(media_dir):
        raise FileNotFoundError("Media directory not found, likely incorrect installation path.")
    return media_dir


def main():
    install_path = get_install_path()
    config.set_game_directory(install_path)

    try:
        verify_media_directory(install_path)
    except FileNotFoundError as e:
        echo.error(e)
        return

    echo.info("Game directory set successfully")
    
    try:
        from scripts.core.file_loading import map_game_files
        map_game_files()
        echo.success("File map built.")
    except Exception as e:
        echo.error(f"Failed to build file map: {e}")
        return


if __name__ == "__main__":
    main()
