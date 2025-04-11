# Tool used to update/create the 'texture_names.json' file

import shutil
from pathlib import Path
from scripts.core import config_manager
from scripts.core.constants import RESOURCE_PATH
from scripts.utils.util import load_cache, save_cache

RESOURCES_DIR = Path(RESOURCE_PATH)
ICON_DIR = RESOURCES_DIR / "icons"
TEXTURES_JSON = "texture_names.json"
TEXTURES_JSON_PATH = RESOURCES_DIR / TEXTURES_JSON

new_textures = {}
textures_data = {}

def load_existing_textures():
    if TEXTURES_JSON_PATH.exists():
        return load_cache(TEXTURES_JSON_PATH, suppress=True)
    return {}


def get_texture_names(textures_dir: Path, folder_key: str = None, prefix_blacklist: list = [], prefix_whitelist: list = []):
    """
    Extracts all texture names from the directory, categorised by prefix.
    Returns a dictionary of all textures, grouped by prefix or folder key.
    """
    global new_textures
    global textures_data
    texture_dict = {}

    for file in textures_dir.glob('*.png'):
        filename = file.name

        # Extract prefix and name
        if "_" in filename:
            prefix, name = filename.split("_", 1)
            if prefix != "Item":
                name = filename
        else:
            prefix, name = "Other", filename  # Default case

        # If prefix is blacklisted, skip it
        if prefix in prefix_blacklist:
            continue

        # If a whitelist exists, ensure prefix is included
        if prefix_whitelist and prefix not in prefix_whitelist:
            continue

        # Determine the assigned key
        assigned_key = folder_key if folder_key else prefix

        # Add texture to the dictionary
        texture_dict.setdefault(assigned_key, []).append(name)

    for key, texture_list in texture_dict.items():
        # Ensure key exists in the existing dictionary
        if key not in textures_data:
            textures_data[key] = []

        new_entries = []
        for name in texture_list:
            if name not in textures_data[key]:  # Use name directly
                textures_data[key].append(name)
                new_entries.append(name)

        if new_entries:
            new_textures.setdefault(key, []).extend(new_entries)


def copy_new_textures(texture_dir):
    if new_textures:
        for folder_key, files in new_textures.items():
            prefix_dir = texture_dir / "new_textures" / folder_key
            prefix_dir.mkdir(parents=True, exist_ok=True)

            for filename in files:
                if folder_key == "Item":
                    filename = f"Item_{filename}"
                texture_path = texture_dir / filename
                if texture_path.exists():
                    new_filename = filename if folder_key != "Item" else filename
                    shutil.copy(texture_path, prefix_dir / new_filename)

            print(f"New textures copied to '{prefix_dir}'")


def save_new_texture_data():
    # Save only if there are new textures
    if new_textures:
        for key, files in new_textures.items():
            print(f"{key}: {len(files)} new textures found")

        save_cache(new_textures, "new_textures.json")
    else:
        print("No new textures found.")


def main():
    global textures_data
    textures_data = load_existing_textures()
    get_texture_names(ICON_DIR)
    copy_new_textures(ICON_DIR)

    # Prefixes to be skipped
    prefix_blacklist = ["Item", "Build", "Zombie", "Male", "Male", "Puddles", "Bob", "BobZ", "BobZ2", "BobZ3", "F", "Hair"]
    
    # Texture folders to be copied
    texture_folders = [
        ".",
#        "Clothes",
#        "weapons",
#        "WorldItems"
    ]
    textures_dir = Path(config_manager.get_config("game_directory")) / "media" / "textures"

    for folder_name in texture_folders:
        source_folder = textures_dir / folder_name if folder_name != "." else textures_dir
        if source_folder.exists():
            if folder_name == ".":
                # Non-recursive for root folder
                get_texture_names(textures_dir, prefix_whitelist=["Item", "Build"])
                copy_new_textures(textures_dir)
#                get_texture_names(textures_dir, prefix_blacklist=prefix_blacklist, folder_key="textures")
                
            else:
                # Recursive for other folders
                get_texture_names(source_folder, folder_key=folder_name)
                for subfolder in source_folder.glob("**/*"):
                    if subfolder.is_dir():
                        get_texture_names(subfolder, folder_key=folder_name)
        else:
            print(f"Source folder {source_folder} does not exist, skipping...")

    save_new_texture_data()
    if new_textures:
        for key in textures_data:
            textures_data[key].sort(key=str.lower)

        save_cache(textures_data, TEXTURES_JSON, RESOURCES_DIR)


if __name__ == "__main__":
    main()
