import os
import json
import shutil
import subprocess
from pathlib import Path
from scripts.core import config_manager
from scripts.core.constants import LUA_PATH

def get_install_path():
    print("Please select your install location:")
    print("1: C:\\Program Files (x86)\\Steam\\steamapps\\common\\ProjectZomboid")
    print("2: C:\\Program Files\\Steam\\steamapps\\common\\ProjectZomboid")
    print("3: Other")

    choice = input("> ").strip()

    if choice == '1':
        return r"C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid"
    elif choice == '2':
        return r"C:\Program Files\Steam\steamapps\common\ProjectZomboid"
    elif choice == '3':
        install_path = input("Please enter the install location: ").strip()
        return install_path.replace('/', '\\')
    else:
        print("Invalid choice, please try again.")
        return get_install_path()


def verify_media_directory(install_path):
    media_dir = os.path.join(install_path, 'media')
    if not os.path.exists(media_dir):
        raise FileNotFoundError("Media directory not found, likely incorrect installation path.")
    return media_dir


def copy_scripts_and_radio(media_dir):
    # Define source directories
    scripts_dir = os.path.join(media_dir, 'scripts')
    radio_dir = os.path.join(media_dir, 'radio')

    # Define destination directories
    scripts_destination = os.path.join('resources', 'scripts')
    radio_destination = os.path.join('resources', 'radio')

    # Check and copy scripts folder
    if not os.path.exists(scripts_dir):
        raise FileNotFoundError(f"Scripts directory not found in {scripts_dir}.")

    if os.path.exists(scripts_destination):
        shutil.rmtree(scripts_destination)

    shutil.copytree(scripts_dir, scripts_destination)
    print(f"Copied {scripts_dir} to {scripts_destination}")

    # Check and copy radio folder
    if not os.path.exists(radio_dir):
        raise FileNotFoundError(f"Radio directory not found in {radio_dir}.")

    if os.path.exists(radio_destination):
        shutil.rmtree(radio_destination)

    shutil.copytree(radio_dir, radio_destination)
    print(f"Copied {radio_dir} to {radio_destination}")


def copy_lua_files(media_dir: str) -> None:
    """
    Copies specific Lua files from the Project Zomboid 'lua' directory to the
    local 'resources/lua' directory.

    :param media_dir: The path to the 'media' directory in the Project Zomboid installation.
    """
    lua_dir = Path(media_dir) / 'lua'
    if not lua_dir.exists():
        raise FileNotFoundError(f"Lua directory not found in {lua_dir}.")

    # Lua files to copy, with their destination folder
    # Key: Lua file
    # Value: destination folder inside 'resources/lua'. Leave blank to add to 'lua' folder.
    lua_files_to_copy = {
        'Ammo.lua': None,
        'Animals.lua': None,
        'Berries.lua': None,
        'Clothing.lua': None,
        'DeadAnimals.lua': None,
        'Distribution_BagsAndContainers.lua': None,
        'Distribution_BinJunk.lua': None,
        'Distribution_ClosetJunk.lua': None,
        'Distribution_CounterJunk.lua': None,
        'Distribution_DeskJunk.lua': None,
        'Distribution_ShelfJunk.lua': None,
        'Distribution_SideTableJunk.lua': None,
        'Fruits.lua': None,
        'ForestGoods.lua': None,
        'ForestRarities.lua': None,
        'Herbs.lua': None,
        'Insects.lua': None,
        'Junk.lua': None,
        'MedicinalPlants.lua': None,
        'Medical.lua': None,
        'Mushrooms.lua': None,
        'Stones.lua': None,
        'Vegetables.lua': None,
        'WildPlants.lua': None,
        'forageSystem.lua': None,
        'BodyLocations.lua': None,
        'Distributions.lua': None,
        'ProceduralDistributions.lua': None,
        'AttachedWeaponDefinitions.lua': None,
        'VehicleDistributions.lua': None,
        'VehicleDistribution_SeatJunk.lua': None,
        'VehicleDistribution_TrunkJunk.lua': None,
        'VehicleDistribution_GloveBoxJunk.lua': None,
        'forageDefinitions.lua': None,
        'SpecialLootSpawns.lua': None,
        'SpecialItemData_Books.lua': None,
        'SpecialItemData_Comics.lua': None,
        'SpecialItemData_Magazines.lua': None,
        'SpecialItemData_Misc.lua': None,
        'SpecialItemData_Photos.lua': None,
        'PrintMediaDefinitions.lua': None,
        'camping_fuel.lua': None,
        'MainCreationMethods.lua': None,
        'ISHotbarAttachDefinition.lua': None,
        'AttachedLocations.lua': None,
        'recorded_media.lua': None,
        # stashes
        'BrandenburgStashDesc.lua': 'stashes',
        'EkronStashDesc.lua': 'stashes',
        'IrvingtonStashDesc.lua': 'stashes',
        'LouisvilleStashDesc.lua': 'stashes',
        'MarchRidgeStashDesc.lua': 'stashes',
        'MulStashDesc.lua': 'stashes',
        'RiversideStashDesc.lua': 'stashes',
        'RosewoodStashDesc.lua': 'stashes',
        'WorldStashDesc.lua': 'stashes',
        'WpStashDesc.lua': 'stashes',
        # animal
        'ChickenDefinitions.lua': 'animal',
        'CowDefinitions.lua': 'animal',
        'DeerDefinitions.lua': 'animal',
        'MouseDefinitions.lua': 'animal',
        'PigDefinitions.lua': 'animal',
        'RabbitDefinitions.lua': 'animal',
        'RaccoonDefinitions.lua': 'animal',
        'RatDefinitions.lua': 'animal',
        'SheepDefinitions.lua': 'animal',
        'TurkeyDefinitions.lua': 'animal',
    }

    destination_dir = Path(LUA_PATH)

    # Copy each file from the lua directory to the destination
    find_and_copy_files(destination_dir, lua_dir, lua_files_to_copy)


def find_and_copy_files(destination_dir, input_dir, files_to_copy, rename_func=None):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file in files_to_copy:
                src = Path(root) / file
                dst = destination_dir
                folder = files_to_copy[file]
                if folder:
                    dst = destination_dir / folder
                dst.mkdir(parents=True, exist_ok=True)
                dst_filename = rename_func(Path(root).name) if rename_func else file
                dst = dst / dst_filename
                shutil.copy(src, dst)
                print(f"Copied {file} to {dst}")


def rename_spawnpoints(folder_name: str) -> str:
    return folder_name.replace(", KY", "").replace(" ", "_").lower() + ".lua"


def copy_spawnpoint_files(media_dir):
    spawnpoint_files = {
        'spawnpoints.lua': 'spawnpoints'
    }
    lua_dir = Path(media_dir) / 'maps'
    if not lua_dir.exists():
        raise FileNotFoundError(f"Lua directory not found in {lua_dir}.")
    
    destination_dir = Path(LUA_PATH)
    find_and_copy_files(destination_dir, lua_dir, spawnpoint_files, rename_func=rename_spawnpoints)


def copy_xml_files(media_dir):
    # Define the specific XML files and their locations
    files_to_copy = {
        'fileGuidTable.xml': os.path.join(media_dir, 'fileGuidTable.xml')
    }
    source_clothing_dir = os.path.join(media_dir, 'clothing')
    destination_dir = os.path.join('resources')
    clothing_destination_dir = os.path.join('resources', 'clothing')

    # Ensure destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    if not os.path.exists(clothing_destination_dir):
        os.makedirs(clothing_destination_dir)

    # Copy each file to the resources directory
    for file_name, src_path in files_to_copy.items():
        dst_path = os.path.join(destination_dir, file_name)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied {file_name} to {dst_path}")
        else:
            print(f"{file_name} not found in {src_path}, skipping.")

    # Copy contents of the clothing folder
    if os.path.exists(source_clothing_dir):
        for item in os.listdir(source_clothing_dir):
            src_path = os.path.join(source_clothing_dir, item)
            dst_path = os.path.join(clothing_destination_dir, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
            print(f"Copied {item} to {dst_path}")
    else:
        print(f"Clothing folder not found at {source_clothing_dir}, skipping.")


def copy_java_files(install_path):
    # Define the source directory
    java_dir = os.path.join(install_path, 'zombie', 'randomizedWorld')

    # Define the destination directory
    destination_dir = os.path.join('resources', 'java')

    # Check if source directory exists
    if not os.path.exists(java_dir):
        raise FileNotFoundError(f"Java directory not found in {java_dir}. Please check the installation path.")

    # Ensure destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # List of valid prefixes
    valid_prefixes = ('RVS', 'RZS', 'RDS', 'RB', 'RBTS')

    # Copy all .class files from java_dir and its subdirectories to destination_dir if they start with valid prefixes
    for root, _, files in os.walk(java_dir):
        for file in files:
            if file.endswith('.class') and file.startswith(valid_prefixes):
                src = os.path.join(root, file)
                dst = os.path.join(destination_dir, file)
                shutil.copy(src, dst)
                print(f"Copied {file} to {dst}")


def handle_translations(media_dir):

    print("Would you like to use:")
    print("1: Local translation")
    print("2: Latest on GitHub (requires git)")

    choice = input("> ").strip()

    if choice == '1':
        translation_dir = os.path.join(media_dir, 'lua', 'shared', 'Translate')
        destination_dir = os.path.join('resources', 'Translate')

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        if os.path.exists(translation_dir):
            shutil.copytree(translation_dir, destination_dir, dirs_exist_ok=True)
            print(f"Copied local translation to {destination_dir}")
        else:
            print(f"Translation directory not found in {translation_dir}")
    elif choice == '2':
        repo_url = "https://github.com/TheIndieStone/ProjectZomboidTranslations/"
        translate_dir = 'resources/Translate'
        # Clear directory
        if os.path.exists(translate_dir):
            shutil.rmtree(translate_dir)

        try:
            subprocess.run(["git", "clone", repo_url, translate_dir], check=True)
            print(f"Successfully cloned the repository into {translate_dir}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone the repository: {e}")
    else:
        print("Invalid choice, please try again.")
        handle_translations(media_dir)


def main():
    install_path = get_install_path()
    config_manager.set_config('game_directory', install_path)

    try:
        media_dir = verify_media_directory(install_path)
    except FileNotFoundError as e:
        print(e)
        return

    try:
        copy_scripts_and_radio(media_dir)
        copy_lua_files(media_dir)
        copy_spawnpoint_files(media_dir)
        copy_xml_files(media_dir)
        copy_java_files(install_path)
        handle_translations(media_dir)
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
