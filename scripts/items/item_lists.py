"""
Menu-based helper module to run item list generators for the PZwiki.

Allows running individual or all item list scripts, each of which generates
wiki-ready tables for specific item categories in Project Zomboid.
"""
import os
import importlib
from scripts.utils import color, echo
from scripts.core.constants import ITEM_DIR
from scripts.core.language import Language

OUTPUT_DIR = os.path.join(ITEM_DIR.format(language_code=Language.get()), "lists")

MODULES = {
    "1": {"module": "scripts.items.lists.item_list_pzwiki", "name": "Item list (maintenance)", "description": "item list for the 'PZwiki:Item_list' page."},
    "2": {"module": "scripts.items.lists.item_list_animal_part", "name": "Animal part", "description": "item list for the 'Animal part' page."},
    "3": {"module": "scripts.items.lists.item_list_appearance", "name": "Appearance", "description": "item list for the 'Appearance' page."},
    "4": {"module": "scripts.items.lists.item_list_camping", "name": "Camping", "description": "item list for the 'Camping' page."},
    "5": {"module": "scripts.items.lists.item_list_clothing", "name": "Clothing", "description": "item list for the 'Clothing' page."},
    "6": {"module": "scripts.items.lists.item_list_communication", "name": "Communication", "description": "item list for the 'Communications' page."},
    "7": {"module": "scripts.items.lists.item_list_container", "name": "Container", "description": "item list for the 'Container' page."},
    "8": {"module": "scripts.items.lists.item_list_cooking", "name": "Cooking", "description": "item list for the 'Cooking (item)' page."},
    "9": {"module": "scripts.items.lists.item_list_corpse", "name": "Corpse", "description": "item list for the 'Corpse' page."},
    "10": {"module": "scripts.items.lists.item_list_debug", "name": "Debug", "description": "item list for the 'Debug' page."},
    "11": {"module": "scripts.items.lists.item_list_electronic", "name": "Electronic", "description": "item list for the 'Electronics' page."},
    "12": {"module": "scripts.items.lists.item_list_entertainment", "name": "Entertainment", "description": f"item list for the 'Entertainment' page. {color.YELLOW}[WIP]{color.RESET}"},
    "13": {"module": "scripts.items.lists.item_list_fire_source", "name": "Fire source", "description": "item list for the 'Fire source' page."},
    "14": {"module": "scripts.items.lists.item_list_fishing", "name": "Fishing", "description": "item list for the 'Fishing (item)' page."},
    "15": {"module": "scripts.items.lists.item_list_fluid_container", "name": "Fluid container", "description": "item list for the 'Fluid container' page."},
    "16": {"module": "scripts.items.lists.item_list_food", "name": "Food", "description": f"item list for the 'Food' and 'Nutritional values' pages. {color.YELLOW}[WIP]{color.RESET}"},
    "17": {"module": "scripts.items.lists.item_list_fuel", "name": "Fuel", "description": "item list for the 'Fuel' page."},
    "18": {"module": "scripts.items.lists.item_list_gardening", "name": "Gardening", "description": "item list for the 'Gardening' page."},
    "19": {"module": "scripts.items.lists.item_list_household", "name": "Household", "description": "item list for the 'Household' page."},
    "20": {"module": "scripts.items.lists.item_list_instrument", "name": "Instrument", "description": "item list for the 'Instrument' page."},
    "21": {"module": "scripts.items.lists.item_list_junk", "name": "Junk", "description": "item list for the 'Junk' page."},
    "22": {"module": "scripts.items.lists.item_list_light_source", "name": "Light source", "description": "item list for the 'Light sources' page."},
    "23": {"module": "scripts.items.lists.item_list_literature", "name": "Literature", "description": "item list for the 'Literature' page."},
    "24": {"module": "scripts.items.lists.item_list_material", "name": "Material", "description": "item list for the 'Material' page."},
    "25": {"module": "scripts.items.lists.item_list_medical", "name": "Medical", "description": "item list for the 'Medical' page."},
    "26": {"module": "scripts.items.lists.item_list_memento", "name": "Memento", "description": "item list for the 'Memento' page."},
    "27": {"module": "scripts.items.lists.item_list_security", "name": "Security", "description": "item list for the 'Security' page."},
    "28": {"module": "scripts.items.lists.item_list_sport", "name": "Sport", "description": "item list for the 'Sport' page."},
    "29": {"module": "scripts.items.lists.item_list_tool", "name": "Tool", "description": "item list for the 'Tools' page."},
    "30": {"module": "scripts.items.lists.item_list_trapping", "name": "Trapping", "description": "item list for the 'Trapping' page."},
    "31": {"module": "scripts.items.lists.item_list_vehicle_maintenance", "name": "Vehicle maintenance", "description": f"item list for the 'Vehicle maintenance' page. {color.YELLOW}[WIP]{color.RESET}"},
    "32": {"module": "scripts.items.lists.item_list_weapon", "name": "Weapon", "description": "item list for the 'Weapon', 'Weapon parts' and 'Ammo' pages."},
}

def display_menu(start=0, page_size=10, run_directly=False):
    """
    Displays a page menu of item list modules to choose from.

    Args:
        start (int): Index of the first module to display.
        page_size (int): Number of modules to display per page.
        run_directly (bool): If True, shows 'Quit' instead of 'Back'.
    """
    keys = list(MODULES.keys())
    end = start + page_size

    echo.write(f"\nSelect a module to run:", color.info)
    print("0: Run all modules")
    for key in keys[start:end]:
        mod = MODULES[key]
        print(f"{key}: {mod['name']} - {mod['description']}")
    if end < len(keys):
        print("]: Next page")
    if start > 0:
        print("[: Previous page")
    print("Q: Quit" if run_directly else "B: Back")


def run_module(module_path: str):
    """
    Dynamically imports and runs a module's main() function.

    Args:
        module_path (str): The full import path to the module.
    """
    try:
        mod = importlib.import_module(module_path)
        if hasattr(mod, "main"):
            mod.main()
        else:
            echo.error(f"Module '{module_path}' has no 'main()' function.")
    except Exception as e:
        echo.error(f"Failed to run '{module_path}': {e}")


def main(run_directly=False):
    """
    Handles input and navigation for the item list module menu.

    Args:
        run_directly (bool): If True, enables quitting directly from the menu.
    """
    page = 0
    page_size = 10

    while True:
        display_menu(start=page * page_size, page_size=page_size, run_directly=run_directly)
        choice = input("> ").strip().lower()

        if choice == ("q" if run_directly else "b"):
            break
        elif choice == "]" and (page + 1) * page_size < len(MODULES):
            page += 1
        elif choice == "[" and page > 0:
            page -= 1
        elif choice == "0":
            for mod in MODULES.values():
                echo.write(f"\n[Running] {mod['name']}", color.warning)
                run_module(mod["module"])
            print("")
            echo.success(f"Finished generating item lists. Files saved to '{OUTPUT_DIR}'")
            break
        elif choice in MODULES:
            mod = MODULES[choice]
            print(f"\n[Running] {mod['name']}")
            run_module(mod["module"])
        else:
            echo.write(f"\n[!] Invalid input. Please try again", color.error)


if __name__ == "__main__":
    main(run_directly=True)