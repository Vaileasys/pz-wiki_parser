import os
import chardet
import script_parser
from core import logging

language_code = None

language_codes = {
    'ar': "Cp1252",
    'ca': "ISO-8859-15",
    'ch': "UTF-8",
    'cn': "UTF-8",
    'cs': "Cp1250",
    'da': "Cp1252",
    'de': "Cp1252",
    'en': "UTF-8",
    'es': "Cp1252",
    'fi': "Cp1252",
    'fr': "Cp1252",
    'hu': "Cp1250",
    'id': "UTF-8",
    'it': "Cp1252",
    'jp': "UTF-8",
    'ko': "UTF-16",
    'nl': "Cp1252",
    'no': "Cp1252",
    'ph': "UTF-8",
    'pl': "Cp1250",
    'pt': "Cp1252",
    'ptbr': "Cp1252",
    'ro': "UTF-8",
    'ru': "Cp1251",
    'th': "UTF-8",
    'tr': "Cp1254",
    'ua': "Cp1251"
}

property_prefixes = {
    'DisplayName': "ItemName_",
    'DisplayCategory': "IGUI_ItemCat_",
    'Categories': "IGUI_perks_",
    'SubCategory': "IGUI_perks_",
}


def set_language_code():
    global language_code
    language_code = input("Enter language code (default 'en')\n> ").strip().lower()
    if language_code in language_codes:
        print(f"Language code '{language_code}' selected.")
    else:
        language_code = "en"
        print("Unrecognised language code, setting to 'en'")
    return language_code


# Detect encoding and return best-fit
def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
#        print(f"File encoded with '{encoding}'")
    return encoding

def parse_translation_file(file_path, language_code, property_prefix):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No file found for '{file_path}'. Ensure the file is in the correct path, or try a different language code.")
    
    encoding = language_codes.get(language_code, "UTF-8")
#    print(f"Encoding for language code '{language_code}' set to {encoding}")

    encoding_detected = False
    translation = None

    while True:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                for line in file:
                    # check if the key exists, then get its value
                    if property_prefix in line:
                        parts = line.split('=', 1)

                        if len(parts) == 2:
                            translation = parts[1].split('"')[1]
                            return translation
                        
        except UnicodeDecodeError:
            if encoding_detected:
                print(f"Unable to decode the file '{file_path}' even after trying to detect encoding.")
                break
            print(f"There was an issue decoding the file '{file_path}' with encoding '{encoding}'. Trying to detect encoding.")
            encoding = detect_file_encoding(file_path)
            encoding_detected = True
        else: 
            break
    return translation


"""
Gets the translation for a property value

property_value: the property to be translated
property_name: the name of the property being translated
lang_code: language code can be specified, leaving empty will use global 'language_code' 
"""
def get_translation(property_value, property_name="DisplayName", lang_code=None):
    global language_code
    if language_code is None:
        language_code = set_language_code()
    if lang_code is None:
        lang_code = language_code

    if property_name == "DisplayName":
        file_path = f'resources/Translate/ItemName/ItemName_{lang_code.upper()}.txt'
    else:
        file_path = f'resources/Translate/IG_UI/IG_UI_{lang_code.upper()}.txt' if lang_code != "en" else 'resources/Translate/IG_UI/IG_UI_EN.txt'
    
    property_prefix = property_prefixes.get(property_name, property_name) + property_value
    if not property_prefix:
        raise ValueError(f"Failed translating due to unsupported property name '{property_name}'")
    
    translation = parse_translation_file(file_path, lang_code, property_prefix)
    

    if translation is None:
        logging.log_to_file(f"No translation found for item with prefix '{property_prefix}' in '{file_path}'")
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