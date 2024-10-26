import os
import shutil
import subprocess

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


def copy_lua_files(media_dir):
    lua_dir = os.path.join(media_dir, 'lua')
    if not os.path.exists(lua_dir):
        raise FileNotFoundError(f"Lua directory not found in {lua_dir}.")

    lua_files_to_copy = [
        'ProceduralDistributions.lua',
        'Distributions.lua',
        'AttachedWeaponDefinitions.lua',
        'VehicleDistributions.lua',
        'foraging_clean.lua',
        'forageDefinitions.lua'
    ]

    destination_dir = os.path.join('resources', 'lua')
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for root, _, files in os.walk(lua_dir):
        for file in files:
            if file in lua_files_to_copy:
                src = os.path.join(root, file)
                dst = os.path.join(destination_dir, file)
                shutil.copy(src, dst)
                print(f"Copied {file} to {dst}")


def copy_xml_files(media_dir):
    # Define the specific XML files and their locations
    files_to_copy = {
        'clothing.xml': os.path.join(media_dir, 'clothing', 'clothing.xml'),
        'fileGuidTable.xml': os.path.join(media_dir, 'fileGuidTable.xml')
    }
    destination_dir = 'resources'

    # Copy each file to the resources directory
    for file_name, src_path in files_to_copy.items():
        dst_path = os.path.join(destination_dir, file_name)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied {file_name} to {dst_path}")
        else:
            print(f"{file_name} not found in {src_path}, skipping.")


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

    try:
        media_dir = verify_media_directory(install_path)
    except FileNotFoundError as e:
        print(e)
        return

    try:
        copy_scripts_and_radio(media_dir)
        copy_lua_files(media_dir)
        copy_xml_files(media_dir)
        copy_java_files(install_path)
        handle_translations(media_dir)
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
