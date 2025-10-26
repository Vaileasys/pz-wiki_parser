#!/usr/bin/env python3
"""
Project Zomboid Wiki Items Batch Processor

This script provides batch processing for item-related data including infoboxes,
distributions, container contents, and articles. Supports multiple languages
with automatic language switching.
"""

from scripts.core.language import Language, Translate, LANGUAGE_CODES
from scripts.core import config_manager as config
from scripts.utils import echo, color


def print_header(heading: str):
    """Print a formatted header."""
    border = "=" * 50
    print(color.style(f"{border}\n{heading.center(50)}\n{border}", color.BLUE))


def select_languages():
    """
    Prompt user for language selection.

    Returns:
        list: List of language codes to process.
    """
    print_header("Language Selection")

    print()
    print("Enter language code, 'all' for all languages, or press Enter for default:")
    while True:
        choice = input("> ").strip().lower()

        if not choice:
            # Use default language
            default_lang = config.get_default_language()
            echo.info(f"Using default language: {default_lang} ({LANGUAGE_CODES[default_lang]['language']})")
            languages = [default_lang]

        elif choice == "all":
            echo.info(f"Will process all {len(LANGUAGE_CODES)} supported languages")
            languages = list(LANGUAGE_CODES.keys())

        elif choice in LANGUAGE_CODES:
            language_name = LANGUAGE_CODES[choice]['language']
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
    echo.info(f"Setting up language: {lang_code} ({LANGUAGE_CODES[lang_code]['language']})")
    Language.set(lang_code)
    Language.set_subpage(lang_code)
    # Force translation loading for the new language
    Translate.load()

    echo.success(f"Language setup completed for {lang_code}")


def run_items_batch(lang_code):
    """
    Run the items batch for a specific language.

    Args:
        lang_code (str): Language code to process
    """
    # Import and call the item infobox batch entry function
    from scripts.items.item_infobox import batch_entry

    print_header("Items Batch Processing")
    echo.info("Items batch processing - will process all item-related data")

    # Clear translations cache for item processing - objects will automatically re-fetch with new language
    try:
        from scripts.items.item_infobox import translations_cache
        translations_cache.clear()
    except ImportError:
        pass  # translations_cache might not exist if module not loaded

    batch_entry(lang_code)
    echo.success(f"Items batch completed for {lang_code}")


def run_items_batch_for_languages(languages):
    """
    Run items batch processing for specified languages.

    Args:
        languages (list): List of language codes to process
    """
    # Process each language
    for i, lang_code in enumerate(languages, 1):
        if len(languages) > 1:
            echo.info(f"[{i}/{len(languages)}] Running items batch for language: {lang_code}")
        setup_language(lang_code)
        run_items_batch(lang_code)

    echo.success("Items batch processing completed for all languages")


def main():
    """
    Main function for the items batch processor.
    """
    # Language selection first
    languages = select_languages()

    # Display menu and handle user input
    while True:
        print_header("Items Batch Processor")
        print("Select a batch processing option:")
        print()
        print("1: All")
        print("2: Items")
        print()
        print("Q: Quit")
        print()

        user_input = input("> ").strip().upper()
        if user_input in ["1", "2"]:
            run_items_batch_for_languages(languages)
            print()
        elif user_input == "Q":
            echo.info("Goodbye!")
            exit(0)
        else:
            echo.error("Invalid option. Please select 1, 2, or Q.")


if __name__ == "__main__":
    main()