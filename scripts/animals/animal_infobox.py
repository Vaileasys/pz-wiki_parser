"""
Item infobox generator.

This module processes `Item` objects into structured infobox parameters, formatted for wiki output.
It handles individual items, pages with multiple item IDs, and supports both combined and standalone infobox generation.

Main functions:
- Extract item attributes into infobox fields
- Merge multiple item definitions into unified infobox data, based on page
- Format and output infobox content as text files
"""

import os
import re
from tqdm import tqdm
from scripts.core import logger
from scripts.core.version import Version
from scripts.utils import echo, color, util
from scripts.objects.item import Item
from scripts.objects.fluid import Fluid
from scripts.objects.animal import Animal, AnimalBreed
from scripts.core import page_manager
from scripts.core.file_loading import write_file, clear_dir
from scripts.core.constants import ANIMAL_DIR, PBAR_FORMAT

ROOT_PATH = os.path.join(ANIMAL_DIR, "infoboxes")

pages_dict = {} # Unprocessed item page dict from the raw page dict

numbered_params = ["model", "icon", "icon_name"]


def generate_animal_data(breed: AnimalBreed):
    """
    Extracts relevant parameters from an Item object into a dictionary.

    Args:
        item (Item): The item object to process.

    Returns:
        dict: Dictionary of infobox parameters for the given item.
    """
    animal = breed.animal

    param = {}
    #-------------- GENERAL --------------#
    param["name"] = re.sub(r'\([^()]*\)', lambda m: f'<br><span style="font-size:88%">{m.group(0)}</span>', breed.name)
    param["model"] = breed.model_files
    param["icon"] = [breed.icon_file, breed.icon_dead_file, breed.icon_skeleton_file]
    param["icon_name"] = [breed.name, breed.get_name("dead"), breed.get_name("skeleton")]
    param["group"] = animal.group_link
    gender = f'({animal.gender})' if animal.baby else f'({_translations_cache("IGUI_Animal_Adult")} {animal.gender})'
    param["stage"] = f'{animal.name} {gender}'
    param["breed"] = breed.breed_name

    #-------------- STATS --------------#
    param["health"] = util.convert_int(1 / (animal.health_loss_multiplier or 1))
    param["weight"] = f"{util.convert_int(round(breed.min_weight, 2))}–{util.convert_int(round(breed.max_weight, 2))}"
    param["size"] = f"{animal.min_size}–{animal.max_size}"
    param["trailer_size"] = animal.trailer_base_size
    param["age"] = f"{animal.min_age}–{animal.max_age}"
    param["daily_water"] = animal.daily_water if animal.daily_water != "0 mL" else None
    param["daily_hunger"] = animal.daily_hunger

    #-------------- HUSBANDRY --------------#
#    param["min_enclosure_size"] = animal.min_enclosure_size

    #-------------- PRODUCTS --------------#
#    products = []
#    products.append(animal.egg_type.icon) if animal.egg_type else None
#    products.append(Item("Base.WoolRaw").icon) if animal.max_wool else None
#    products.append(breed.milk_type.rgb_link) if breed.milk_type else None
#    products.append(animal.dung.icon) if animal.dung else None
#    param["products"] = ' '.join(products) if products else None
#    param["parts"] = ' '.join([Item(part).icon for part in breed.parts.all_parts]) if breed.parts else None
#    param["egg_season"] = animal.lay_egg_period_month_start if animal.lay_egg_period_start else None
#    param["egg_per_season"] = f"{animal.min_clutch_size}–{animal.max_clutch_size}" if animal.min_clutch_size else None
#    param["egg_per_day"] = animal.eggs_per_day
#    param["milk_range"] = f"{util.convert_int(breed.min_milk)}–{util.convert_int(breed.max_milk)}" if breed.min_milk else None
#    param["milk_rate"] = breed.milk_inc if breed.max_milk else None
#    param["wool_max"] = '–'.join([str(util.convert_int(wool)) for wool in breed.max_wool]) if breed.max_wool else None
#    param["wool_rate"] = breed.wool_inc if breed.max_wool else None
#    param["meat_ratio"] = breed.meat_ratio if breed.meat_ratio else None

    #-------------- TECHNICAL --------------#
    param["breed_id"] = breed.breed_id
    param["animal_id"] = animal.animal_id
    param["full_breed_id"] = breed.full_breed_id

    param["infobox_version"] = Version.get()
    
    return param


def _translations_cache(key, default=None):
    from scripts.core.language import Translate
    cache = {}
    if key in cache:
        return cache.get(key)
    
    translation = Translate.get(key, default=default or key)
    cache[key] = translation
    return translation
    

def build_infobox(infobox_data: dict) -> list[str]:
    """
    Builds an infobox template from the provided parameters.

    Args:
        infobox_data (dict): Dictionary of key-value infobox fields.

    Returns:
        list[str]: A list of lines forming the infobox template.
    """
    if not infobox_data:
        return None
    content = []
    content.append("{{Infobox animal")
    for key, value in infobox_data.items():
        content.append(f"|{key}={value}")
    content.append("}}")
    return content


def process_pages(pages: dict) -> None:
    """
    Generates infoboxes for all items grouped by page name and writes output files.

    Args:
        pages (dict): Mapping of page names to their item_id entries.
    """
    from urllib.parse import quote

    output_dir = None

    with tqdm(total=len(pages), desc="Building page infoboxes", unit=" pages", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        clear_dir(directory=ROOT_PATH)
        for page_name, page in pages.items():
            pbar.set_postfix_str(f'Processing page: {page_name[:30]}')
            full_breed_ids = page.get("full_breed_id", [])
            page_data = {}

            if len(full_breed_ids) > 1:
                echo.warning(f"{page_name} has more than one full breed ID. Using {full_breed_ids[0]}.")

            full_breed_id = full_breed_ids[0] # We should only have 1 key for animals, so we skip the rest

            breed = AnimalBreed.from_key(full_breed_id)
            if not breed.is_valid:
                echo.warning(f"Full breed ID '{full_breed_id}' not found in the parsed data. Skipping.")
                continue
            animal_params = generate_animal_data(breed)
            
            param = util.enumerate_params(animal_params, whitelist=numbered_params)
            content = build_infobox(param)

            if not content:
                continue

            page_name = page_name.replace(" ", "_")
            output_dir = write_file(content, quote(page_name, safe='()') + ".txt", root_path=ROOT_PATH, suppress=True)
            pbar.update(1)
    
        elapsed_time = pbar.format_dict["elapsed"]
    if not output_dir:
        echo.error("Infobox generation failed. No files saved.")
        return
    echo.success(f"Files saved to '{output_dir}' after {elapsed_time:.2f} seconds.")


def process_animals(full_breed_id_list: list, page_names: bool = False) -> None:
    """
    Generates infoboxes for a list of specific item IDs and writes output files.

    Args:
        item_id_list (list): List of item IDs to process.
    """
    with tqdm(total=len(full_breed_id_list), desc="Building animal infoboxes", unit=" animals", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        clear_dir(directory=ROOT_PATH)
        for full_breed_id in full_breed_id_list:
            breed = AnimalBreed.from_key(full_breed_id)
            pbar.set_postfix_str(f'Processing: {breed.animal.group} ({full_breed_id[:30]})')
            infobox_data = generate_animal_data(breed)
            infobox_data = util.enumerate_params(infobox_data, numbered_params)
            content = build_infobox(infobox_data)
            output_dir = write_file(content, full_breed_id + ".txt", root_path=ROOT_PATH, suppress=True)
            pbar.update(1)
        elapsed_time = pbar.format_dict["elapsed"]
    echo.success(f"Files saved to '{output_dir}' after {elapsed_time:.2f} seconds.")


## ------------------- Initialisation/Preparation ------------------- ##
def prepare_pages(full_breed_id_list: list) -> dict:
    """
    Prepares and validates the item-to-page mappings for later infobox generation.

    Args:
        item_id_list (list): List of item IDs to process.

    Returns:
        dict: Updated pages dictionary containing valid item_id groupings.
    """
    global pages_dict
    raw_page_dict = page_manager.get_raw_page_dict()
    animal_page_dict = raw_page_dict.get('animal', {})
    #save_cache(item_page_dict, "item_page_dict.json")

    seen_animals = set()
    pages_dict = animal_page_dict.copy()

    with tqdm(total=len(full_breed_id_list), desc="Building page list", unit=" animals", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        for full_breed_id in full_breed_id_list:
            pbar.set_postfix_str(f'Processing animal key: {full_breed_id[:30]}')

            if full_breed_id in seen_animals:
                continue

            seen_animals.add(full_breed_id)

            page = AnimalBreed.from_key(full_breed_id).page
            page_data:dict = pages_dict.get(page)

            if not page_data:
                pages_dict[page] = {"full_breed_id": [full_breed_id]}
                logger.write(
                    message=f"'{full_breed_id}' missing from page dict, added to '{color.style(page, color.GREEN)}' {color.style('[new]', color.YELLOW)}.",
                    print_bool=True,
                    category="warning",
                    file_name="missing_pages_log.txt"
                )

            else:
                key_list:list = page_data.setdefault("full_breed_id", [])
                if full_breed_id not in key_list:
                    key_list.append(full_breed_id)
                    logger.write(
                        message=f"'{full_breed_id}' missing from page dict, added to '{color.style(page, color.GREEN)}'.",
                        print_bool=True,
                        category="warning",
                        file_name="missing_pages_log.txt"
                    )
                seen_animals.update(key_list)
            pbar.update(1)
    
    #save_cache(pages_dict, "temp.json")
    return pages_dict


def select_animal() -> list:
    """
    Prompts the user to input one or more animal keys (semicolon-separated) and returns the valid ones.

    Returns:
        list[str]: A list of valid animal keys.
    """
    while True:
        query = input("Enter one or more animal keys (separated by semicolons):\n> ")
        full_breed_ids = [full_breed_id.strip() for full_breed_id in query.split(';') if full_breed_id.strip()]
        valid_keys = []
        invalid_keys = []

        for full_breed_id in full_breed_ids:
            if AnimalBreed.key_exists(full_breed_id):
                breed = AnimalBreed.from_key(full_breed_id)
                echo.success(f"Found full_breed_id: '{breed.full_breed_id}' ({breed.name})")
                valid_keys.append(breed.full_breed_id)
            else:
                invalid_keys.append(full_breed_id)

        if valid_keys:
            if invalid_keys:
                print(f"Some animal keys weren't found and were skipped: {', '.join(invalid_keys)}")
            return valid_keys

        print("Couldn't find any of the keys. Try again.")


def select_page() -> dict[str, dict[str, list[str]]]:
    """
    Prompts the user to input one or more page names (semicolon-separated) and returns a
    dictionary of valid pages and their associated item IDs.

    Returns:
        dict: A dictionary mapping page names to their valid item IDs.
    """
    while True:
        query = input("Enter one or more page names (separated by semicolons):\n> ")
        page_names = [name.strip() for name in query.split(';') if name.strip()]
        valid_pages = {}

        for name in page_names:
            if name in pages_dict:
                full_breed_ids = pages_dict[name].get("full_breed_id")
                valid_ids = [full_breed_id for full_breed_id in full_breed_ids if AnimalBreed.key_exists(full_breed_id)] if full_breed_ids else []
                if valid_ids:
                    valid_pages[name] = {"full_breed_id": valid_ids}
                else:
                    print(f"No valid animal keys found for page '{name}'. Skipping.")
            else:
                print(f"Page '{name}' not found. Skipping.")

        if valid_pages:
            return valid_pages

        print("None of the entered pages had valid item IDs. Try again.")


def choose_process(run_directly: bool):
    """
    Presents the user with infobox generation options.

    Args:
        run_directly (bool): Whether to allow quitting or going back.

    Returns:
        str: The selected menu option.
    """
    WIP = color.style("[WIP]", color.BRIGHT_YELLOW)
    options = [
        "1: All: Pages - Generate infoboxes based on page. " + WIP,
        "2: All: Animal Key - Generate infoboxes for every animal, naming as the Animal Key. " + WIP,
        "3: Select: Page - Choose one or more pages to generate an infobox for. " + WIP,
        "4: Select: Animal Key - Choose one or more Animal Key to generate an infobox for. " + WIP
    ]
    options.append("Q: Quit" if run_directly else "B: Back")

    while True:
        print("\nWhich items do you want to generate an infobox for?")
        choice = input("\n".join(options) + "\n> ").strip().lower()

        if choice in ('q', 'b'):
            break

        try:
            if int(choice) in range(1, 5):
                break
        except ValueError:
            pass
        print("Invalid choice.")

    return choice


def init_dependencies():
    """Initialises required modules so they don't interrupt tqdm progress bars."""
    from scripts.core.language import Language
    Language.get()
    page_manager.init()


def main(pre_choice: int = None, run_directly: bool = False):
    """
    Entry point for infobox generation.

    Args:
        run_directly (bool): Whether the script is being run directly.
    """
    init_dependencies()
    full_breed_id_list = list(AnimalBreed.get_full_breed_ids().keys())
    pages = prepare_pages(full_breed_id_list)

    if not pre_choice or not pre_choice in [1, 2, 3, 4]:
        user_choice = choose_process(run_directly)
    else:
        user_choice = str(pre_choice)

    if user_choice == '3':
        pages = select_page()
    elif user_choice == '4':
        full_breed_id_list = select_animal()

    if user_choice in ['1', '3']:
        process_pages(pages)
    elif user_choice in ['2', '4']:
        process_animals(full_breed_id_list)


if __name__ == "__main__":
    main(run_directly=True)

    # Testing - exports all infoboxes to a single txt file
    import random
    from scripts.core.file_loading import load_file
    from pathlib import Path
    from scripts.core.language import Language

    query_path = Path(ROOT_PATH.format(language_code=Language.get()))
    content = ['<div style="display: flex; flex-wrap: wrap;">']

    all_files = [file for file in query_path.iterdir() if file.is_file()]
    random.shuffle(all_files)
    sample_files = all_files[:20]

    for file in sample_files:
        lines = load_file(file.name, ROOT_PATH)
        content.append("<div>")
        breed = AnimalBreed.from_key(file.stem)
#        content.append(breed.wiki_link)
        content.extend(lines)
        content.append("</div>")

    content.append("</div>")
    write_file(content)


    # Test query string:
    # cowangus;ewefriesian;turkeyhenmeleagris