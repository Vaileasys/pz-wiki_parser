#!/usr/bin/env python3

import importlib, sys, os
from scripts.core import config_manager as config, setup, logger, cache
from scripts.core.language import Language
from scripts.utils import echo, color

menu_structure = {
    "0": {
        "name": "Settings",
        "description": "Modify script settings",
        "sub_options": None,
    },
    "1": {
        "name": "Items",
        "description": "",
        "sub_options": {
            "1": {
                "module": "scripts.items.item_infobox",
                "name": "Item infobox",
                "description": "Generates item infoboxes.",
            },
            "2": {
                "module": "scripts.items.item_codesnip",
                "name": "Item codesnips",
                "description": "Generate codesnip files.",
            },
            "3": {
                "module": "scripts.items.item_consumables",
                "name": "Consumables",
                "description": "Generate consumables tables.",
            },
            "4": {
                "module": "scripts.items.item_distribution",
                "name": "Distributions",
                "description": "Generate distribution files.",
            },
            "5": {
                "module": "scripts.items.item_container_contents",
                "name": "Container contents",
                "description": "Generate container contents.",
            },
            "6": {
                "module": "scripts.items.item_body_part",
                "name": "Body part",
                "description": "Generates body part templates.",
            },
            "7": {
                "module": "scripts.items.item_recmedia_transcript",
                "name": "Recorded media transcripts",
                "description": "Generate transcripts for recorded media items (VHS/CD).",
            },
            "8": {
                "module": "scripts.items.item_article",
                "name": "Item article",
                "description": "Generate articles for items.",
            },
            "9": {
                "module": "scripts.items.item_tags",
                "name": "Tags",
                "description": "Manage and generate tags.",
            },
        },
    },
    "2": {
        "name": "Fluids",
        "description": "",
        "sub_options": {
            "1": {
                "module": "scripts.fluids.fluid_infobox",
                "name": "Fluid infobox",
                "description": "Generates fluid infoboxes.",
            },
            "2": {
                "module": "scripts.fluids.fluid_compatibility",
                "name": "Fluid compatibility",
                "description": "Generate fluid compatibility table.",
            },
            "3": {
                "module": "scripts.fluids.fluid_article",
                "name": "Fluid article",
                "description": "Generate articles for fluids.",
            },
        },
    },
    "3": {
        "name": "Tiles",
        "description": "",
        "sub_options": {
            "1": {
                "module": "scripts.tiles.tiles_batch",
                "name": "Tile batch",
                "description": "Process tiles.",
            },
            "2": {
                "module": "scripts.tiles.tiles_stitcher",
                "name": "Tile stitcher",
                "description": "Stitch tile sprites.",
            },
        },
    },
    "4": {
        "name": "Recipes",
        "description": "Manage and generate recipies.",
        "sub_options": {
            "1": {
                "module": "scripts.recipes.craft_recipes",
                "name": "CraftRecipe parser",
                "description": "Process recipes.",
            },
            "2": {
                "module": "scripts.recipes.researchrecipes",
                "name": "Research recipes",
                "description": "Process research recipes.",
            },
            "3": {
                "module": "scripts.recipes.teached_recipes",
                "name": "Teached recipes",
                "description": "Process teached recipes.",
            },
            "4": {
                "module": "scripts.recipes.evolved_recipes",
                "name": "Evolved recipes",
                "description": "Process evolved recipes.",
            },
            "5": {
                "module": "scripts.items.item_fixing",
                "name": "Fixing",
                "description": "Generates fixing recipes.",
            },
        },
    },
    "5": {
        "name": "Vehicles",
        "description": "",
        "sub_options": {
            "1": {
                "module": "scripts.vehicles.vehicle_list_pzwiki",
                "name": "Vehicle list (maintenance)",
                "description": "Generate vehicle list for the 'PZwiki:Vehicle_list' page.",
            },
            "2": {
                "module": "scripts.vehicles.vehicle_list_detailed",
                "name": "Vehicle list (detailed)",
                "description": "Generate detailed vehicle lists for both just the base vehicles and all variants.",
            },
            "3": {
                "module": "scripts.vehicles.vehicle_infobox",
                "name": "Vehicle infobox",
                "description": "Generates vehicle infoboxes.",
            },
            "4": {
                "module": "scripts.vehicles.vehicle_parts",
                "name": "Vehicle parts",
                "description": "Generate table of a vehicle's parts.",
            },
            "5": {
                "module": "scripts.vehicles.vehicle_spawns",
                "name": "Vehicle spawns",
                "description": "Generate list of vehicle spawns.",
            },
            "6": {
                "module": "scripts.vehicles.vehicle_article",
                "name": "Vehicle article",
                "description": "Generate articles for vehicles.",
            },
        },
    },
    "6": {
        "name": "Animals",
        "description": "",
        "sub_options": {
            "1": {
                "module": "scripts.animals.animal_list_pzwiki",
                "name": "Animal list (maintenance)",
                "description": "Generate animal list for the 'PZwiki:Animal_list' page.",
            },
            "2": {
                "module": "scripts.animals.animal_article",
                "name": "Animal article",
                "description": "Generate articles for animals. Runs the required modules automatically.",
            },
            "3": {
                "module": "scripts.animals.animal_infobox",
                "name": "Animal infobox",
                "description": "Generate animal infoboxes.",
            },
            "4": {
                "module": "scripts.animals.animal_food",
                "name": "Animal food list",
                "description": "Generate list of foods for each animal.",
            },
            "5": {
                "module": "scripts.animals.animal_products",
                "name": "Animal products",
                "description": "Generate product tables for animals.",
            },
            "6": {
                "module": "scripts.animals.animal_genes",
                "name": "Animal genes",
                "description": "Generate tables of genes for animals.",
            },
            "7": {
                "module": "scripts.animals.animal_stages",
                "name": "Animal stages",
                "description": "Generate tables of stages for animals.",
            },
        },
    },
    "7": {
        "name": "Lists",
        "description": "Generate lists for articles",
        "sub_options": {
            "1": {
                "module": "items.item_lists",
                "name": "Item lists",
                "description": "Generate item lists.",
            },
            "2": {
                "module": "lists.recmedia_list",
                "name": "Recorded media list",
                "description": "Generate recorded media tables.",
            },
            "3": {
                "module": "lists.body_locations_list",
                "name": "BodyLocation list",
                "description": "Generate a BloodLocation table.",
            },
            "4": {
                "module": "lists.body_parts_list",
                "name": "BloodLocation/Body part list",
                "description": "Generate a BloodLocation/body part table.",
            },
            "5": {
                "module": "lists.attachment_list",
                "name": "Attachment list",
                "description": "Generate AttachmentType and AttachmentsProvided tables.",
            },
            "6": {
                "module": "lists.fluid_list",
                "name": "Fluid list",
                "description": "Generate the fluid table.",
            },
            "7": {
                "module": "scripts.parser.outfit_parser",
                "name": "Outfit list",
                "description": "Parse outfit xml files.",
            },
        },
    },
    "8": {
        "name": "Tools",
        "description": "Data analysis and generate reports.",
        "sub_options": {
            "1": {
                "module": "tools.update_icons",
                "name": "Update icons",
                "description": "Updates 'texture_names.json' (used for various scripts) adding new icons into a folder. Ensure .pack icons are added manually to 'resources/icons/'.",
            },
            "2": {
                "module": "tools.vehicle_render_data",
                "name": "Vehicle render data",
                "description": "Generate a JSON file with vehicle mesh and texture data, which can be used in blender.",
            },
            "3": {
                "module": "scripts.core.runner",
                "name": "External processes",
                "description": "Run external processes, such as ZomboidDecompiler and pywikibot (requires setup).",
            },
            "4": {
                "module": "scripts.tools.diff",
                "name": "Version differences",
                "description": "Generate a diff between 2 versions of the game, showing line-by-line differences.",
            },
        },
    },
    "9": {
        "name": "Other",
        "description": "",
        "sub_options": {
            "1": {
                "module": "parser.script_parser",
                "name": "Script parser",
                "description": "Parse game scripts.",
            },
            "2": {
                "module": "scripts.misc.room_define",
                "name": "Room definitions",
                "description": "Create roomdef item page.",
            },
            "3": {
                "module": "scripts.parser.radio_parser",
                "name": "Radio transcripts",
                "description": "Generate radio transcripts.",
            },
            "4": {
                "module": "scripts.misc.spawn_points",
                "name": "Spawn points",
                "description": "Parse spawn points file.",
            },
        },
    },
}

settings_structure = {
    "0": {
        "name": "Reset config file",
        "description": "Reset the config file to default values.",
        "module": "core.config_manager",
    },
    "1": {
        "name": "Change version",
        "description": "Change the game version of the parsed data.",
        "module": "core.version",
    },
    "2": {
        "name": "Change language",
        "description": "Change the language to be used for outputs.",
        "module": "core.language",
    },
    "3": {"name": "Clear cache", "description": "Clear the data cache."},
    "4": {
        "name": "Toggle debug",
        "description": f"Toggle debug mode, to show or hide debug prints. Current: {config.get_debug_mode()}",
    },
    "5": {
        "name": "Run First Time Setup",
        "description": "Run the initial setup again.",
        "module": "setup",
    },
}


def print_header(heading: str):
    border = "=" * 50
    print(color.style(f"{border}\n{heading.center(50)}\n{border}", color.BLUE))


def display_menu(menu, is_root=False, title=None):
    if title:
        print_header(title)

    for key, option in menu.items():
        name = option["name"]
        description = option.get("description", "").strip()

        # Top-level (root) menus show only key and name, no hyphen or description
        if is_root:
            print(f"{key}: {name}")
        else:
            if description:
                print(f"{key}: {name} - {description}")
            else:
                print(f"{key}: {name}")

    if not is_root:
        print("B: Back")
    else:
        print("Q: Quit")


def handle_module(module_name, user_input=None):
    try:
        module = importlib.import_module(module_name)
        if config.get_debug_mode():
            cache.clear_cache()
        if user_input is not None:
            module.main(user_input)
        else:
            module.main()
    except ImportError as error:
        echo.error(f"Error importing module {module_name}: {error}")
    except AttributeError as error:
        echo.error(f"Module {module_name} does not have a main() function: {error}")
    except Exception as error:
        echo.error(f"An error occurred while running {module_name}: {error}")


def navigate_menu(menu, is_root=False, title=None):
    while True:
        if is_root:
            from scripts.core.version import Version

            title = f"Main Menu (Game version: {Version.get()})"
        display_menu(menu, is_root, title)
        user_input = input("> ").strip().upper()

        if (is_root and user_input == "Q") or (not is_root and user_input == "B"):
            break

        if user_input in menu:
            selected = menu[user_input]
            name = selected["name"]
            title = name
            subs = selected.get("sub_options")

            # If no sub-options, simply run or show header
            if not subs and not is_root:
                print_header(title)

            if name == "Settings" and subs is None:
                navigate_menu(settings_structure, title=name)
            elif name == "Clear cache":
                cache.clear_cache()
            elif name == "Toggle debug":
                new_debug = not config.get_debug_mode()
                config.set_debug_mode(new_debug)
                settings_structure["4"]["description"] = (
                    f"Toggle debug mode, to show or hide debug prints. Current: {new_debug}"
                )
            elif name == "Run First Time Setup":
                print_header(title)
                handle_module("scripts.core.setup")
            elif "module" in selected:
                handle_module(selected["module"])
            elif subs:
                navigate_menu(subs, title=name)
        else:
            echo.write("[!] Invalid input. Please try again.", color.error)


def check_first_run():
    is_first_run = config.get_first_time_run()
    if is_first_run:
        choice = (
            input("Would you like to run the first-time setup? (Y/N): ").strip().upper()
        )
        if choice == "Y":
            setup.main()
            logger.write("Setup first time set up completed.")
        else:
            logger.write("Skipping first-time setup.", True)
        config.set_first_time_run(False)


def main():
    # Add the /scripts/ directory to the system path
    scripts_path = os.path.join(os.path.dirname(__file__), "scripts")
    sys.path.append(scripts_path)

    # Allows setting the language externally
    if len(sys.argv) > 1:
        Language.set(sys.argv[1])

    check_first_run()

    from scripts.core.version import Version

    Version.update()  # Checks if there was a version change

    navigate_menu(menu_structure, is_root=True)


if __name__ == "__main__":
    main()
