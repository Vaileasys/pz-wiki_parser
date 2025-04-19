import importlib
import sys
import os
from scripts.core import config_manager, setup, logger, cache
from scripts.core.version import Version

menu_structure = {
    '0': {
        'name': 'Settings',
        'description': 'Modify script settings',
        'sub_options': None
    },
    '1': {
        'name': 'Data generation',
        'description': 'Generate working data.',
        'sub_options': {
            '1': {'module': 'item_infobox', 'name': 'Item infobox', 'description': 'Generates item infoboxes.'},
            '2': {'module': 'fluid_infobox', 'name': 'Fluid infobox', 'description': 'Generates fluid infoboxes.'},
            '3': {'module': 'fixing', 'name': 'Fixing', 'description': 'Generates fixing recipes.'},
            '4': {'module': 'consumables', 'name': 'Consumables', 'description': 'Generate consumables tables.'},
            '5': {'module': 'codesnip', 'name': 'Codesnips', 'description': 'Generate codesnip files.'},
            '6': {'module': 'distribution', 'name': 'Distributions', 'description': 'Generate distribution files.'},
            '7': {'module': 'evolvedrecipe', 'name': 'Evolved recipes', 'description': 'Parse evolved recipes.'},
            '8': {'module': 'item_body_part', 'name': 'Body part', 'description': 'Generates body part templates.'},
        },
    },
    '2': {
        'name': 'Page generation',
        'description': 'Generate pages or lists.',
        'sub_options': {
            '1': {'module': 'item_article', 'name': 'Item article', 'description': 'Generate articles for items.'},
            '2': {'module': 'fluid_article', 'name': 'Fluid article', 'description': 'Generate articles for fluids.'},
            '3': {'module': 'lists.item_list', 'name': 'Item list', 'description': 'Returns all items in a list organised by DisplayCategory.'},
            '4': {'module': 'lists.weapon_list', 'name': 'Weapon list', 'description': 'Return all weapons in a list with stats organised by their skill.'},
            '5': {'module': 'lists.clothing_list', 'name': 'Clothing list', 'description': 'Return all clothing in a list with stats organised by body location.'},
            '6': {'module': 'lists.food_list', 'name': 'Food list', 'description': 'Generate food and nutrition pages.'},
            '7': {'module': 'scripts.parser.radio_parser', 'name': 'Radio transcripts', 'description': 'Generate radio transcripts.'},
            '8': {'module': 'scripts.parser.outfit_parser', 'name': 'Outfit parser', 'description': 'Parse outfit xml files.'},
            '9': {'module': 'roomdefine', 'name': 'Room definitions', 'description': 'Create roomdef item page.'},
        },
    },
    '3': {
        'name': 'Recipes',
        'description': 'Manage and generate tags.',
        'sub_options': {
            '1': {'module': 'scripts.recipes.craft_recipes', 'name': 'CraftRecipe parser', 'description': 'Process recipes.'},
            '2': {'module': 'scripts.recipes.researchrecipes', 'name': 'Research recipes', 'description': 'Process research recipes.'},
            '3': {'module': 'scripts.recipes.teached_recipes', 'name': 'Teached recipes', 'description': 'Process teached recipes.'},
            '4': {'module': 'scripts.recipes.evolvedrecipe', 'name': 'Evolved recipes', 'description': 'Process evolved recipes.'},
            '5': {'module': 'scripts.recipes.legacy_recipe_format', 'name': 'Legacy recipe parser', 'description': 'Process recipes.'}, # TODO Remove after implementation
        }
    },
    '4': {
        'name': 'Tags',
        'description': 'Manage and generate tags.',
        'sub_options': None # Handled by item_tags.py
    },
    '5': {
        'name': 'Tools',
        'description': 'Data analysis and generate reports.',
        'sub_options': {
            '1': {'module': 'tools.item_dict', 'name': 'Item dictionary', 'description': 'Generate a list of items with their item ID and compare with another version.'},
            '2': {'module': 'tools.compare_item_lists', 'name': 'Compare item lists', 'description': "Generates a list of unique items comparing 'PZwiki:Item_list' versions."}
        },
    }
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
        'name': 'Clear cache',
        'description': 'Clear the data cache.',
        'module': 'setup'
    },
    '4': {
        'name': 'Run First Time Setup',
        'description': 'Run the initial setup again.',
        'module': 'setup'
    },
}

def display_menu(menu, is_root=False, title=None):
    if title:
        print("\033[94m" + "=" * 50)
        print(f"{title.center(50)}")
        print("=" * 50 + "\033[0m")
        
    for key, value in menu.items():
        print(f"{key}: {value['name']} - {value['description']}")

    if not is_root:
        print("B: Back")
    if is_root:
        print("Q: Quit")


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


def navigate_menu(menu, is_root=False, title=None):
    while True:
        if is_root:
            version_number = Version.get()
            title = f"Main Menu (Game version: {version_number})"
        display_menu(menu, is_root, title)
        user_input = input("> ").strip().upper()

        if is_root and user_input == "Q" or not is_root and user_input == "B":
            break

        if user_input in menu:
            selected_option = menu[user_input]
            if not selected_option.get("sub_options"):
                print("\033[94m" + "=" * 50)
                print(f"{selected_option['name'].center(50)}")
                print("=" * 50 + "\033[0m")

            # Check if it's the settings menu and link to settings_structure
            if selected_option['name'] == 'Settings' and selected_option['sub_options'] is None:
                navigate_menu(settings_structure)
            elif selected_option['name'] == 'Clear cache':
                cache.clear_cache()
                print("\nReturning to the menu...\n")
            elif selected_option['name'] == 'Run First Time Setup':
                handle_module('scripts.core.setup')
                print("\nReturning to the menu...\n")
            elif selected_option['name'] == 'Tags':
                handle_module('scripts.item_tags')
                print("\nReturning to the menu...\n")
            elif 'module' in selected_option:
                handle_module(selected_option['module'])
                print("\nReturning to the menu...\n")
            elif 'sub_options' in selected_option:
                navigate_menu(selected_option['sub_options'], title=selected_option['name'])
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
            logger.write("Setup first time set up completed.")

        else:
            logger.write("Skipping first-time setup.", True)
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
