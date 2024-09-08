import os
import json
import chardet
import re
from scripts.parser import item_parser
from scripts.core import logging_file, config_manager

language_code = None
default_language = None

LANGUAGE_CODES = {
    'ar': ("Cp1252", "Arabic"),
    'ca': ("ISO-8859-15", "Catalan"),
    'ch': ("UTF-8", "Chinese"),
    'cn': ("UTF-8", "Chinese"),
    'cs': ("Cp1250", "Czech"),
    'da': ("Cp1252", "Danish"),
    'de': ("Cp1252", "German"),
    'en': ("UTF-8", "English"),
    'es': ("Cp1252", "Spanish"),
    'fi': ("Cp1252", "Finnish"),
    'fr': ("Cp1252", "French"),
    'hu': ("Cp1250", "Hungarian"),
    'id': ("UTF-8", "Indonesian"),
    'it': ("Cp1252", "Italian"),
    'jp': ("UTF-8", "Japanese"),
    'ko': ("UTF-16", "Korean"),
    'nl': ("Cp1252", "Dutch"),
    'no': ("Cp1252", "Norwegian"),
    'ph': ("UTF-8", "Filipino"),
    'pl': ("Cp1250", "Polish"),
    'pt': ("Cp1252", "Portuguese"),
    'ptbr': ("Cp1252", "Portuguese (Brazilian)"),
    'ro': ("UTF-8", "Romanian"),
    'ru': ("Cp1251", "Russian"),
    'th': ("UTF-8", "Thai"),
    'tr': ("Cp1254", "Turkish"),
    'ua': ("Cp1251", "Ukrainian")
}

PROPERTY_PREFIXES = {
    'DisplayName': "ItemName_",
    'DisplayCategory': "IGUI_ItemCat_",
    'Categories': "IGUI_perks_",
    'SubCategory': "IGUI_perks_",
    'SkillTrained': "IGUI_perks_",
    'TeachedRecipes': "Recipe_",
    'PartType': "Tooltip_weapon_",
    'EvolvedRecipeName': "EvolvedRecipeName_",
    'Wiki': "Wiki_",
}

FILE_WHITELIST = (
    "ItemName_",
    "IG_UI_",
    "Recipes_",
    "Tooltip_",
    "EvolvedRecipeName_",
    "Wiki_"
)

translations_cache = {}


def get_wiki_translation(value):
    """
    Gets the translations for a value within `<< >>` delimiters for defining the string to translate.

    :param str value: The value to be translated. Can be a line with multiple strings wrapped in `<< >>`.
    :return: Value with all strings translated.
    :rtype: str
    """
    placeholders = re.findall(r'\<\<(.*?)\>\>', value)
    
    # Replace each placeholder with its translation
    for placeholder in placeholders:
        placeholder = f"{placeholder}"
        translated_value = get_translation(placeholder, 'Wiki')
        value = value.replace(f'<<{placeholder}>>', translated_value)

    return value


# change language code based on user input
def change_language():
    global language_code

    language_code = input(f"Enter language code (default '{default_language}')\n> ").strip().lower()

    if language_code not in LANGUAGE_CODES:
        language_code = default_language
        print(f"Unrecognised language code, defaulting to '{default_language}'.")

    set_language_code(language_code)

    language = LANGUAGE_CODES.get(language_code, ("UTF-8", "Unknown"))[1]
    print(f"Language changed to '{language_code}' ({language})")

    return language_code


# Detect encoding and return best-fit
def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        logging_file.log_to_file(f"File encoded with '{encoding}'")
    return encoding


def get_translation(property_value, property_key="DisplayName", lang_code=language_code):
    """
    Searches for the property value based on the property key and language code to return the translation.

    :param property_value: Property value to be translated.
    :param property_key: Key for the property being translated (optional).
    :param lang_code: Language code forced for translations. Leaving empty will use global 'language_code' (optional).
    :return: Translation for the property.
    """
    global language_code

    if not property_value:
        return property_value
    
    if language_code is None:
        language_code = get_language_code()

    if lang_code is None:
        lang_code = language_code

    if lang_code is not None and lang_code != "en" and lang_code != language_code:
        raise ValueError(f"'{lang_code}' when translating {property_value} doesn't match '{language_code}' or 'en'. Ensure the correct language code is used.")

    translations_lang = translations_cache.get(lang_code, {})
    property_prefix = PROPERTY_PREFIXES.get(property_key) + property_value
    translation = translations_lang.get(property_prefix)
    if translation is None:
        logging_file.log_to_file(f"No translation found for '{property_prefix}' prefix")
        translation = property_value

        # Try get the item's name from DisplayName instead
        if property_key == "DisplayName":
            item_data = item_parser.get_item_data().get(property_value)
            if item_data:
                translation = item_data.get("DisplayName", property_value)
            else: 
                # Special case: handle 'SaucePan' in fixing (should be 'Saucepan')
                item_data = item_parser.get_item_data().get(property_value.capitalize())
                if item_data:
                    translation = item_data.get("DisplayName", property_value.capitalize())
    return translation


def parse_translation_file(language_code):
    language_dir = os.path.join("resources", "Translate", language_code.upper())
    if not os.path.exists(language_dir):
        raise FileNotFoundError(f"No file found for '{language_dir}'. Ensure the file is in the correct path, or try a different language code.")
    
    # Get encoding for the chosen language
    encoding = LANGUAGE_CODES.get(language_code, ("UTF-8", "Unknown"))[0]
    encoding_detected = False
    parsed_translations = {}

    for root, dirs, files in os.walk(language_dir):
        for file_name in files:
            # Check if the file is whitelisted
            if not any(file_name.startswith(prefix) for prefix in FILE_WHITELIST):
                continue

            file_path = os.path.join(root, file_name)

            # Handle json files
            if file_name.endswith(".json"):
                try:
                    with open(file_path, 'r', encoding="UTF-8") as json_file:
                        json_data = json.load(json_file)
                        parsed_translations.update(json_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON file '{file_name}': {e}")
                except Exception as e:
                    print(f"Error processing JSON file '{file_name}': {e}")
                continue

            # Handle text files
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    for line in file:
                        line = line.strip()

                        if '=' not in line or '{' in line or '}' in line:
                            continue

                        parts = line.split('=', 1)


                        if len(parts[1].split('"')) > 1:
                            value = parts[1].split('"')[1]
                        else:
                            value = parts[1].strip()

                        # Ensure the line was split into exactly two parts
                        if len(parts) == 2:
                            key = parts[0].strip()
                            if len(parts[1].split('"')) > 1:
                                value = parts[1].split('"')[1]
                            else:
                                # Special case: Translations don't contain 2 quotation marks
                                value = parts[1].strip()
                            parsed_translations[key] = value
                        else:
                            print(f"More or less than 2 parts for {line}, skipping.")
                            
            except UnicodeDecodeError:
                if encoding_detected:
                    print(f"Unable to decode the file '{file_name}' even after trying to detect encoding.")
                    break
                logging_file.log_to_file(f"There was an issue decoding the file '{file_name}' with encoding '{encoding}'. Trying to detect encoding.")
                encoding = detect_file_encoding(file_path)
                encoding_detected = True
            except Exception as e:
                print(f"Error processing file '{file_name}' for line '{line}': {e}")
                continue

    return parsed_translations


def cache_translations():
    global translations_cache
    for language_code in LANGUAGE_CODES:
        try:
            # Parse translation files for the language
            parsed_translations = parse_translation_file(language_code)
            
            # Store the parsed translations in the translations_cache
            translations_cache[language_code] = parsed_translations
        
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred for language '{language_code}': {e}")

    # Save to json for debugging.
    output_dir = os.path.join('output', 'logging')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'translations_cache.json')

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(translations_cache, json_file, ensure_ascii=False, indent=4)
    
    return translations_cache


def get_language_code():
    global language_code
    if language_code is None:
        init_translations()
    return language_code


def set_language_code(new_language_code):
    global language_code
    language_code = new_language_code


def update_default_language():
    """
    Updates the default language to the latest config entry.
    Use 'get_default_langauge' instead for returning the default language.
    
    :return: Updated default language.
    """
    global default_language
    default_language = config_manager.get_config('default_language')
    return default_language


def get_default_language():
    global default_language
    if default_language is None:
        default_language = update_default_language()
    return default_language


def init_translations():
    print("Initialising translations")
    global translations_cache
    global default_language
    global language_code
    default_language = config_manager.get_config('default_language')
    if language_code is None:
        language_code = change_language()
    cache_translations()


def main():
    init_translations()