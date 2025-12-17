import os
from scripts.core.language import Language, Translate, LANGUAGE_CODES
from scripts.core import config_manager as config
from scripts.utils import echo

COMMON_LANGUAGE_CODES = [
    "en",
    "tr",
    "es",
    "ru",
    "pt-br",
    "uk",
    "pl",
    "it",
    "th",
    "fr",
    "zh-hant",
    "zh-hans",
]

once_run_scripts = set()


def _mark_once(key):
    """Return True the first time a key is seen in this batch, else False."""
    if key in once_run_scripts:
        return False
    once_run_scripts.add(key)
    return True


def reset_mark_once():
    """Reset the once_run_scripts set for a new batch."""
    once_run_scripts.clear()


def select_languages():
    """
    Prompt user for language selection.

    Returns:
        list: List of language codes to process.
    """

    print()
    print("Enter language code, 'all', or 'common':")
    while True:
        choice = input("> ").strip().lower()

        if not choice:
            # Use default language
            default_lang = config.get_default_language()
            echo.info(
                f"Using default language: {default_lang} ({LANGUAGE_CODES[default_lang]['language']})"
            )
            languages = [default_lang]

        elif choice == "all":
            echo.info(f"Will process all {len(LANGUAGE_CODES)} supported languages")
            # Ensure 'en' is processed first, then the rest in alphabetical order
            all_langs = sorted(LANGUAGE_CODES.keys())
            if "en" in all_langs:
                all_langs.remove("en")
                languages = ["en", *all_langs]
            else:
                languages = all_langs

        elif choice == "common":
            echo.info(
                f"Will process common language set ({len(COMMON_LANGUAGE_CODES)} languages)"
            )
            languages = COMMON_LANGUAGE_CODES

        elif choice in LANGUAGE_CODES:
            language_name = LANGUAGE_CODES[choice]["language"]
            echo.info(f"Selected language: {choice} ({language_name})")
            languages = [choice]

        else:
            echo.error(f"Invalid language code '{choice}'. Please try again.")
            continue
        return languages


def setup_language(lang_code):
    """
    Set up the language system for the specified language code.

    Args:
        lang_code (str): Language code to set up
    """
    Language.set(lang_code)
    Language.set_subpage(lang_code)

    # Force translation loading for the new language
    Translate.load()

    # Clear translations cache
    from scripts.items.item_infobox import translations_cache

    translations_cache.clear()


def batch_items(lang_code):
    """
    Run items batch processing for a single language.

    Args:
        lang_code (str): Language code to process
    """

    def run_infobox(lang_code):
        from scripts.items.item_infobox import batch_entry

        batch_entry(lang_code)

    def run_body_part():
        if not _mark_once("run_body_part"):
            return
        from scripts.items.item_body_part import get_items, write_to_file

        data = get_items()
        if data is not None:
            write_to_file(data)

    def run_codesnip():
        if not _mark_once("run_codesnip"):
            return
        from scripts.items.item_codesnip import main as codesnip_main

        codesnip_main()

    def run_consumables():
        if not _mark_once("run_consumables"):
            return
        from scripts.items.item_consumables import process_items
        from scripts.objects.item import Item

        items_list = list(Item.keys())
        process_items(items_list)

    def run_container_contents():
        if not _mark_once("run_container_contents"):
            return
        from scripts.items.item_container_contents import (
            main as container_contents_main,
        )

        container_contents_main()

    def run_distribution():
        if not _mark_once("run_distribution"):
            return
        from scripts.items.item_distribution import main as distribution_main

        distribution_main()

    def run_literature_titles():
        if not _mark_once("run_literature_titles"):
            return
        from scripts.items.item_literature_titles import main as literature_titles_main

        literature_titles_main()

    def run_fixing():
        from scripts.items.item_fixing import main as fixing_main

        fixing_main()

    def run_recmedia_transcripts():
        from scripts.items.item_recmedia_transcript import (
            main as recmedia_transcripts_main,
        )

        recmedia_transcripts_main(batch=True)

    def run_tags():
        if not _mark_once("run_tags"):
            return
        from scripts.items.item_tags import (
            write_tag_image,
            write_tag_list,
            write_tag_table,
            generate_article_templates,
            generate_article_modding,
        )

        write_tag_image()
        write_tag_list()
        write_tag_table()
        generate_article_templates()
        generate_article_modding()

    def run_item_lists():
        from scripts.items.item_lists import run_all_modules

        run_all_modules()

    # Run for every language
    run_infobox(lang_code)
    run_fixing()
    run_recmedia_transcripts()
    run_item_lists()

    # Run once
    run_body_part()
    run_codesnip()
    run_consumables()
    run_container_contents()
    run_distribution()
    run_literature_titles()
    run_tags()


def batch_recipes(lang_code):
    """
    Run recipes batch processing.

    Args:
        lang_code (str): Language code to process (only used for setup, recipes run once per batch)
    """
    if not _mark_once("run_recipes"):
        return

    from scripts.recipes.craft_recipes import main as craft_recipes_main
    from scripts.recipes.evolved_recipes import main as evolved_recipes_main
    from scripts.recipes.researchrecipes import main as research_recipes_main
    from scripts.recipes.teached_recipes import main as teached_recipes_main

    craft_recipes_main(batch=True)
    evolved_recipes_main(batch=True)
    research_recipes_main(batch=True)
    teached_recipes_main(batch=True)


def batch_tiles(lang_code):
    """
    Run tiles batch processing.

    Args:
        lang_code (str): Language code to process
    """
    from scripts.tiles.tiles_batch import main as tiles_batch_main

    tiles_batch_main(lang_code)


def batch_fluids(lang_code):
    """
    Run fluids batch processing.

    Args:
        lang_code (str): Language code to process
    """
    from scripts.fluids.fluid_infobox import automatic_extraction
    from scripts.fluids.fluid_compatibility import main as fluid_compatibility_main
    from scripts.fluids.fluid_article import main as fluid_article_main

    automatic_extraction()
    fluid_compatibility_main()
    fluid_article_main()


def batch_lists(lang_code):
    """
    Run lists batch processing.

    Args:
        lang_code (str): Language code to process
    """
    from scripts.core.cache import load_cache
    from scripts.core.constants import DATA_DIR
    from scripts.lists.attachment_list import main as attachment_list_main
    from scripts.lists.body_parts_list import main as body_parts_list_main
    from scripts.lists.body_locations_list import main as body_locations_list_main
    from scripts.lists.fluid_list import main as fluid_list_main
    from scripts.lists.furniture_list import generate_furniture_lists
    from scripts.lists.furniture_surfaces_list import generate_surface_list
    from scripts.lists.hotbar_slots import main as hotbar_slots_main

    attachment_list_main()
    body_parts_list_main()
    body_locations_list_main()
    fluid_list_main()
    hotbar_slots_main()

    named_tiles_cache_file = "named_furniture.json"
    named_tiles_data, _ = load_cache(
        os.path.join(DATA_DIR, named_tiles_cache_file),
        "Named Tiles",
        get_version=True,
    )
    generate_furniture_lists(named_tiles_data)

    named_tiles_cache_file = "named_furniture.json"
    named_tiles_data, _ = load_cache(
        os.path.join(DATA_DIR, named_tiles_cache_file),
        "Named Tiles",
        get_version=True,
    )
    generate_surface_list(named_tiles_data)


def batch_animals(lang_code):
    """
    Run animals batch processing.

    Args:
        lang_code (str): Language code to process
    """
    from scripts.animals.animal_infobox import main as animal_infobox_main
    from scripts.animals.animal_products import main as animal_products_main
    from scripts.animals.animal_stages import main as animal_stages_main
    from scripts.animals.animal_genes import main as animal_genes_main
    from scripts.animals.animal_food import main as animal_food_main
    from scripts.animals.animal_list_pzwiki import main as animal_list_main

    animal_infobox_main(pre_choice=2)
    animal_products_main()
    animal_stages_main()
    animal_genes_main()
    animal_food_main()
    animal_list_main()


def batch_vehicles(lang_code):
    """
    Run vehicles batch processing.

    Args:
        lang_code (str): Language code to process
    """
    from scripts.vehicles.vehicle_infobox import automatic_extraction
    from scripts.vehicles.vehicle_parts import main as vehicle_parts_main
    from scripts.vehicles.vehicle_list_detailed import (
        main as vehicle_list_detailed_main,
    )
    from scripts.vehicles.vehicle_list_pzwiki import (
        main as vehicle_list_pzwiki_main,
    )
    from scripts.vehicles.vehicle_spawns import main as vehicle_spawns_main

    automatic_extraction()
    vehicle_parts_main()
    vehicle_list_detailed_main()
    vehicle_list_pzwiki_main()
    vehicle_spawns_main()


def batch_misc(lang_code):
    """
    Run misc batch processing.

    Args:
        lang_code (str): Language code to process
    """

    def run_outfits():
        if not _mark_once("run_outfits"):
            return
        from scripts.misc.outfits import main as outfits_main

        outfits_main()

    run_outfits()


def main():
    """
    Main function for the items batch processor.
    """
    # Language selection first
    languages = select_languages()

    # Display menu and handle user input
    while True:
        print("Select a batch processing option:")
        print()
        print("1: All")
        print("2: Items")
        print("3: Recipes")
        print("4: Tiles")
        print("5: Fluids")
        print("6: Lists")
        print("7: Animals")
        print("8: Vehicles")
        print("9: Misc")
        print()
        print("B: Back")
        print()

        user_input = input("> ").strip().upper()

        batch_functions = []
        if user_input == "1":
            batch_functions = [
                batch_items,
                batch_recipes,
                batch_tiles,
                batch_fluids,
                batch_lists,
                batch_animals,
                batch_vehicles,
                batch_misc,
            ]
        elif user_input == "2":
            batch_functions = [batch_items]
        elif user_input == "3":
            batch_functions = [batch_recipes]
        elif user_input == "4":
            batch_functions = [batch_tiles]
        elif user_input == "5":
            batch_functions = [batch_fluids]
        elif user_input == "6":
            batch_functions = [batch_lists]
        elif user_input == "7":
            batch_functions = [batch_animals]
        elif user_input == "8":
            batch_functions = [batch_vehicles]
        elif user_input == "9":
            batch_functions = [batch_misc]
        elif user_input == "B":
            print()
            break
        else:
            echo.error("Invalid option. Please select 1-10, or B.")
            continue

        # Reset once_run_scripts for this batch
        reset_mark_once()

        # Process each language
        for i, lang_code in enumerate(languages, 1):
            if len(languages) > 1:
                echo.info(
                    f"[{i}/{len(languages)}] Processing language: {lang_code} ({LANGUAGE_CODES[lang_code]['language']})"
                )

            # Setup language to lear translations
            setup_language(lang_code)

            # Run all selected batches
            for batch_func in batch_functions:
                batch_func(lang_code)

        echo.success("Batch processing completed")
        print()
