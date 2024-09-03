import os
import chardet
import script_parser
from core import logging

language_code = None

language_codes = {
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

property_prefixes = {
    'DisplayName': "ItemName_",
    'DisplayCategory': "IGUI_ItemCat_",
    'Categories': "IGUI_perks_",
    'SubCategory': "IGUI_perks_",
    'SkillTrained': "IGUI_perks_",
    'TeachedRecipes': "Recipe_",
    'PartType': "Tooltip_weapon_",
    'EvolvedRecipeName': "EvolvedRecipeName_",
}

file_whitelist = (
    "ItemName_",
    "IG_UI_",
    "Recipes_",
    "Tooltip_",
    "EvolvedRecipeName_",
)

translations_en = {}
translations_lang = {}


# getter for language code
def get_language_code():
    global language_code
    return language_code


# setter for language code
def set_language_code(new_language_code):
    global language_code
    language_code = new_language_code


# change language code based on user input
def change_language():
    language_code = input("Enter language code (default 'en')\n> ").strip().lower()
    if language_code in language_codes:
        print(f"Language code '{language_code}' selected.")
    else:
        language_code = "en"
        print("Unrecognised language code, setting to 'en'")
    set_language_code(language_code)

    language = language_codes.get(language_code, ("UTF-8", "Unknown"))[1]
    print(f"Language changed to '{language_code}' ({language})")

    return language_code


# Detect encoding and return best-fit
def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
#        print(f"File encoded with '{encoding}'")
    return encoding


def parse_translation_file(language_code):
    base_dir = "resources/Translate"
    language_dir = os.path.join(base_dir, language_code.upper())
    if not os.path.exists(language_dir):
        raise FileNotFoundError(f"No file found for '{language_dir}'. Ensure the file is in the correct path, or try a different language code.")
    
    # get encoding for the chosen language
    encoding = language_codes.get(language_code, ("UTF-8", "Unknown"))[0]
    encoding_detected = False
    parsed_translations = {}

    for root, dirs, files in os.walk(language_dir):
        for file_name in files:
            # check if the file is whitelisted
            if not any(file_name.startswith(prefix) for prefix in file_whitelist):
                continue

            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    for line in file:
                        line = line.strip()

                        if '=' not in line or '{' in line or '}' in line:
                            continue

                        parts = line.split('=', 1)

                        # ensure that the line was split into exactly two parts
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].split('"')[1]
                            parsed_translations[key] = value
                        else:
                            print(f"More or less than 2 parts for {line}, skipping.")
                            
            except UnicodeDecodeError:
                if encoding_detected:
                    print(f"Unable to decode the file '{file_path}' even after trying to detect encoding.")
                    break
                print(f"There was an issue decoding the file '{file_path}' with encoding '{encoding}'. Trying to detect encoding.")
                encoding = detect_file_encoding(file_path)
                encoding_detected = True
            except Exception as e:
                print(f"Error processing file '{file_name}': {e}")
                continue

    return parsed_translations


"""
Gets the translation for a property value

property_value: the property to be translated
property_name: the name of the property being translated
lang_code: language code can be specified, leaving empty will use global 'language_code' 
"""
def get_translation(property_value, property_name="DisplayName", lang_code=None):
    if not property_value:
        return property_value
    if translations_en == {}:
        init_translations()

    global language_code
    if lang_code is not None:
        if lang_code != "en" and lang_code != language_code:
            raise ValueError(f"'lang_code' when translating {property_value} doesn't match 'language_code' or 'en'. Ensure the correct language code is used.")

    property_prefix = property_prefixes.get(property_name) + property_value
    translation = None
    try:
        if lang_code == "en":
            translation = translations_en.get(property_prefix, None)
        else:
            translation = translations_lang.get(property_prefix, None)
    except KeyError:
        translation = None

    if translation is None:
        logging.log_to_file(f"No translation found for '{property_prefix}' prefix")
        translation = property_value
        # try get the item's name from DisplayName instead
        if property_name == "DisplayName":
            module_check, item_check = property_value.split(".")

            #check if script_parser has been run yet
            if script_parser.parsed_item_data != "":
                for module, module_data in script_parser.parsed_item_data.items():
                    if module == module_check:
                        for item, item_data in module_data.items():
                            if item == item_check:
                                translation = item_data.get("DisplayName", item)
                            # special case for 'SaucePan' in fixing (should be 'Saucepan')
                            elif item == item_check.capitalize():
                                translation = item_data.get("DisplayName", item)

    return translation


def init_translations():
    print("Initialising translations")
    global translations_en
    global translations_lang
    language_code = change_language()
    translations_en = parse_translation_file('en')
    if language_code == 'en':
        
        translations_lang = translations_en
    else:
        translations_lang = parse_translation_file(language_code)

def main():
    init_translations()