import importlib
import sys
import os

menu_structure = {
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
            '5': {'module': 'distribution', 'name': 'Generate distributions', 'description': 'Generate distribution files.'},
        },
    },
    '3': {
        'name': 'Page generation',
        'description': 'Generate pages or lists.',
        'sub_options': {
            '1': {'module': 'item_list', 'name': 'Item list', 'description': 'Returns all items in a list organised by DisplayCategory.'},
            '2': {'module': 'weapon_list', 'name': 'Weapon list', 'description': 'Return all weapons in a list with stats organised by their skill.'},
            '3': {'module': 'article', 'name': 'Article', 'description': 'Generate wiki articles.'},
            '4': {'module': 'nutrition', 'name': 'nutrition', 'description': 'Generate nutrition page.'},
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


def display_menu(menu, is_root=False):
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


def navigate_menu(menu, is_root=False):
    while True:
        display_menu(menu, is_root)
        user_input = input("> ").strip().upper()

        if is_root and user_input == "Q":
            break
        elif not is_root and user_input == "B":
            return  # Go back to the previous menu

        if user_input in menu:
            selected_option = menu[user_input]

            # If it's a final option, run the module
            if 'module' in selected_option:
                handle_module(selected_option['module'])
                print("\nReturning to the current menu...\n")
            elif 'sub_options' in selected_option:
                # Navigate into the submenu
                navigate_menu(selected_option['sub_options'])
        else:
            print("Invalid input. Please try again.")


def main():
    # Add the /scripts/ directory to the system path
    script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
    sys.path.append(script_dir)

    print("Welcome to the script runner!")
    navigate_menu(menu_structure, is_root=True)


if __name__ == "__main__":
    main()
