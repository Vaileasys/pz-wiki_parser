import importlib
import sys
import os
from scripts.core import version, config_manager, logging, setup

menu_structure = {
    '0': {
        'name': 'Settings',
        'description': 'Modify script settings',
        'sub_options': None
    },
    '1': {
        'name': 'Properties',
        'description': 'Work with item properties.',
        'sub_options': {
            '1': {'module': 'property_list', 'name': 'Property list', 'description': 'Return all values of a specific property.'},
            '2': {'module': 'get_property_value', 'name': 'Property value', 'description': 'Returns the value of a property for a specific item.'},
            '3': {'module': 'sort_by_property', 'name': 'Sort by property', 'description': 'Sort all parsed data and organise for a user defined property.'},
        },
    },
    '2': {
        'name': 'Data generation',
        'description': 'Generate working data.',
        'sub_options': {
            '1': {'module': 'infobox', 'name': 'Infobox', 'description': 'Generates infoboxes.'},
            '2': {'module': 'fixing', 'name': 'Fixing', 'description': 'Generates fixing recipes.'},
            '3': {'module': 'consumables', 'name': 'Consumables', 'description': 'Generate consumables tables.'},
            '4': {'module': 'codesnip', 'name': 'Codesnips', 'description': 'Generate codesnip files.'},
            '5': {'module': 'distribution', 'name': 'Distributions', 'description': 'Generate distribution files.'},
            '6': {'module': 'item_dict', 'name': 'Item dictionary', 'description': 'Generate a list of items with their item ID and compare with another version.'},
            '7': {'module': 'evolvedrecipe', 'name': 'Evolved recipes', 'description': 'Parse evolved recipes.'}
        },
    },
    '3': {
        'name': 'Page generation',
        'description': 'Generate pages or lists.',
        'sub_options': {
            '1': {'module': 'article', 'name': 'Article', 'description': 'Generate wiki articles.'},
            '2': {'module': 'item_list', 'name': 'Item list', 'description': 'Returns all items in a list organised by DisplayCategory.'},
            '3': {'module': 'weapon_list', 'name': 'Weapon list', 'description': 'Return all weapons in a list with stats organised by their skill.'},
            '4': {'module': 'clothing_list', 'name': 'Clothing list', 'description': 'Return all clothing in a list with stats organised by body location.'},
            '5': {'module': 'nutrition', 'name': 'nutrition', 'description': 'Generate nutrition page.'},
        },
    },
    '4': {
        'name': 'Tags',
        'description': 'Manage and generate tags.',
        'sub_options': {
            '1': {'module': 'item_tags', 'name': 'Item tags', 'description': 'Outputs all tags and items with those tags.'},
            '2': {'module': 'article_tag', 'name': 'Article tags', 'description': 'Generates modding articles for tags.'},
            '3': {'module': 'article_tag_image', 'name': 'Article tag images', 'description': 'Generates template articles for tag cycling images.'},
        },
    },
    '5': {
        'name': 'Dev',
        'description': 'Module testing.',
        'sub_options': {
            '1': {'module': 'placeholder', 'name': 'placeholder', 'description': 'placeholder.'},
        },
    },
}

settings_structure = {
    '0': {
        'name': 'Reset config file',
        'description': 'Reset the config file to default values.',
        'module': 'core.config_manager'
    },
    '1': {
        'name': 'Change version',
        'description': 'Change the game version of the parsed data.',
        'module': 'core.version'
    },
    '2': {
        'name': 'Change language',
        'description': 'Change the language to be used for outputs.',
        'module': 'core.translate'
    },
    '3': {
        'name': 'Run First Time Setup',
        'description': 'Run the initial setup again.',
        'module': 'setup'
    },
}

def display_menu(menu, is_root=False):
    if is_root:
        version_number = version.get_version()
        print("Game version:", version_number)

    for key, value in menu.items():
        print(f"{key}: {value['name']} - {value['description']}")

    if not is_root:
        print("B: Back")
    if is_root:
        print("Q: Quit")


def change_version():
    # Specify the path to the version.py file
    version_file_path = os.path.join(os.path.dirname(__file__), 'scripts', 'core', 'version.py')

    new_version = input("Enter the new version number: ").strip()

    # Read the existing content of version.py
    with open(version_file_path, 'r') as file:
        lines = file.readlines()

    # Replace the version number in the correct line
    with open(version_file_path, 'w') as file:
        for line in lines:
            if 'version_number =' in line:
                line = f'    version_number = "{new_version}"\n'
            file.write(line)

    print(f"Version number updated to {new_version} in {version_file_path}")

    # Reload the version module to reflect changes immediately
    try:
        importlib.reload(version)
        # Print the new version to confirm
        updated_version = version.get_version()
        if updated_version:
            print("New game version:", updated_version)
        else:
            print("Error: Version number is None after update.")
    except Exception as e:
        print(f"Error reloading version module: {e}")


def handle_module(module_name, user_input=None):
    try:
        module = importlib.import_module(module_name)
        if user_input is not None:
            module.main(user_input)
        else:
            module.main()
    except ImportError as e:
        print(f"Error importing module {module_name}: {e}")
    except AttributeError as e:
        print(f"Module {module_name} does not have a main() function: {e}")
    except Exception as e:
        print(f"An error occurred while running {module_name}: {e}")


def navigate_menu(menu, is_root=False):
    while True:
        display_menu(menu, is_root)
        user_input = input("> ").strip().upper()

        if is_root and user_input == "Q" or not is_root and user_input == "B":
            break

        if user_input in menu:
            selected_option = menu[user_input]

            # Check if it's the settings menu and link to settings_structure
            if selected_option['name'] == 'Settings' and selected_option['sub_options'] is None:
                navigate_menu(settings_structure)
            elif selected_option['name'] == 'Run First Time Setup':
                handle_module('scripts.setup')
                print("\nReturning to the menu...\n")
            elif 'module' in selected_option:
                handle_module(selected_option['module'])
                print("\nReturning to the menu...\n")
            elif 'sub_options' in selected_option:
                navigate_menu(selected_option['sub_options'])
        else:
            print("Invalid input. Please try again.")


def check_first_run():
    first_time_run = config_manager.get_config('first_time_run')
    # Convert config entry to a boolean
    if first_time_run == '1':
        first_time_run = True
    else:
        first_time_run = False

    if not first_time_run:
        # If the flag is False (0), it's the first run
        choice = input("Would you like to run the first-time setup? (Y/N): ").strip().upper()
        if choice == 'Y':
            setup.main()
            logging.log_to_file("Setup first time set up completed.")

        else:
            logging.log_to_file("Skipping first-time setup.", True)
        config_manager.set_config('first_time_run', '1')


def main():
    # Add the /scripts/ directory to the system path
    script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
    sys.path.append(script_dir)

    check_first_run()

    print("\nWelcome to the wiki parser!\n")
    navigate_menu(menu_structure, is_root=True)


if __name__ == "__main__":
    main()
