import os
import csv
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from scripts.parser import item_parser
from scripts.core import translate, logging_file


parsed_burn_data = {}

# gets 'Tags' for item_data
def get_tags(item_data):
    tags = []
    tags = item_data.get('Tags', '')
    return tags


# Gets parsed item data for an item id
def get_item_data_from_id(item_id):
    all_item_data = item_parser.get_item_data()
    item_data = all_item_data[item_id]
    return item_data


def fix_item_id(item_id):
    """
    Checks if an item_id is formatted correctly (i.e., 'module.item_name'). 
    If not, it'll assume it's just the 'item_name' and search the parsed item data for its 'module'. 
    It will then return the full item_id.

    :param item_id: The Item ID to check, which could be either in the format 'module.item_name' or just 'item_name' (without the module).
    :type item_id: str

    :returns: The correct item_id in the format 'module.item_name'. Otherwise it'll return the input string.
    :rtype: item_id (str)

    :example:
        Given `item_id = "Cooked"` and `item_parser.get_item_data()` contains a key like `"Food.Cooked"`, 
        this function will return `"Food.Cooked"`.
    """
    if '.' in item_id:
        return item_id
    else:
        all_item_data = item_parser.get_item_data()
        for key in all_item_data.keys():
            if key.endswith(f'.{item_id}'):
                return key
        else:
            print(f"No Item ID found for '{item_id}'")
            return item_id


def get_clothing_xml_value(item_data, xml_value):
    if 'ClothingItem' in item_data:
        clothing_item = item_data['ClothingItem']
        file_path = os.path.join("resources", "clothing", "clothingItems", f"{clothing_item}.xml")

        if not os.path.exists(file_path):
            logging_file.log_to_file(f"No XML file found for ClothingItem '{clothing_item}'. Is it in the correct directory?")
            return None
        
        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Find all matching elements
            elements = root.findall(xml_value)
            if elements:
                # If there's only one element, return it as a string
                if len(elements) == 1:
                    value = elements[0].text
#                    print(f"Single value found for '{xml_value}': {value}")
                    return value
                # If there are multiple elements, return a list of strings
                values = [element.text for element in elements if element.text]
#                print(f"Multiple values found for '{xml_value}': {values}")
                return values
            else:
#                print(f"'{xml_value}' not found for '{clothing_item}'")
                return None
        except ET.ParseError as e:
            print(f"Error parsing XML file: {file_path}\n{e}")
            return None
        

# gets model for item_data as PNG
def get_model(item_data):
    texture_names_path = Path("resources") / "texture_names.json"
    model = None

    if 'ClothingItem' in item_data:
        model = get_clothing_xml_value(item_data, "textureChoices")
        if model is None:
            model = get_clothing_xml_value(item_data, "m_BaseTextures")
        
        # Remove filepath and capitalize
        if model is not None:
            if isinstance(model, list):
                model = [value.split("\\")[-1].capitalize() for value in model]
            else:
                model = model.split("\\")[-1].capitalize()

            with open(texture_names_path, 'r') as file:
                texture_data = json.load(file)

            if isinstance(model, str):
                model = [model]
            
            # Check the json file and get the correct capitalisation for the model texture
            for i, model_value in enumerate(model):
                for values in texture_data.values():
                    for value in values:
                        
                        if value.lower() == model_value.lower():
                            model[i] = value
                            break

                    else:
                        continue
                    break

    elif 'WorldStaticModelsByIndex' in item_data:
        model = item_data['WorldStaticModelsByIndex']

    if model is None:
        model = item_data.get('WorldStaticModel',item_data.get('WeaponSprite', item_data.get('StaticModel', '')))

    if model == '':
        return ''
    
    # Remove _Ground suffix
    if isinstance(model, list):
        model = [value.replace('_Ground', '').replace('Ground', '') for value in model]
    else:
        model = model.replace('_Ground', '').replace('Ground', '')
    
    # Add PNG extension
    if isinstance(model, list):
        model = [f"{value}_Model.png" for value in model]
    elif isinstance(model, str):
        model = f"{model}_Model.png"

    return model


def get_body_parts(item_data, link=True, default=""):
    """Gets body parts for an item and returns as a list.

    :returns: Translated body parts.
    :rtype: body_parts (list)
    """

    # Taken from 'BloodClothingType.class' init() - updated Build 42.0.2
    BODY_PART_DICT = {
        "Apron": ["Torso_Upper", "Torso_Lower", "UpperLeg_L", "UpperLeg_R"],
        "ShirtNoSleeves": ["Torso_Upper", "Torso_Lower", "Back"],
        "JumperNoSleeves": ["Torso_Upper", "Torso_Lower", "Back"],
        "Shirt": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R"],
        "ShirtLongSleeves": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R"],
        "Jumper": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R"],
        "Jacket": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R", "Neck"],
        "LongJacket": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R", "Neck", "Groin", "UpperLeg_L", "UpperLeg_R"],
        "ShortsShort": ["Groin", "UpperLeg_L", "UpperLeg_R"],
        "Trousers": ["Groin", "UpperLeg_L", "UpperLeg_R", "LowerLeg_L", "LowerLeg_R"],
        "Shoes": ["Foot_L", "Foot_R"],
        "FullHelmet": ["Head"],
        "Bag": ["Back"],
        "Hands": ["Hand_L", "Hand_R"],
        "Hand_L": ["Hand_L"],
        "Hand_R": ["Hand_R"],
        "Head": ["Head"],
        "Neck": ["Neck"],
        "Groin": ["Groin"],
        "UpperBody": ["Torso_Upper"],
        "LowerBody": ["Torso_Lower"],
        "LowerLegs": ["LowerLeg_L", "LowerLeg_R"],
        "LowerLeg_L": ["LowerLeg_L"],
        "LowerLeg_R": ["LowerLeg_R"],
        "UpperLegs": ["UpperLeg_L", "UpperLeg_R"],
        "UpperLeg_L": ["UpperLeg_L"],
        "UpperLeg_R": ["UpperLeg_R"],
        "UpperArms": ["UpperArm_L", "UpperArm_R"],
        "UpperArm_L": ["UpperArm_L"],
        "UpperArm_R": ["UpperArm_R"],
        "LowerArms": ["ForeArm_L", "ForeArm_R"],
        "ForeArm_L": ["ForeArm_L"],
        "ForeArm_R": ["ForeArm_R"],
    }

    # Taken from 'BodyPartType.class' getDisplayName() - updated Build 42.0.2
    BODY_PART_TRANSLATIONS = {
        "Hand_L": "Left_Hand",
        "Hand_R": "Right_Hand",
        "ForeArm_L": "Left_Forearm",
        "ForeArm_R": "Right_Forearm",
        "UpperArm_L": "Left_Upper_Arm",
        "UpperArm_R": "Right_Upper_Arm",
        "Torso_Upper": "Upper_Torso",
        "Torso_Lower": "Lower_Torso",
        "Head": "Head",
        "Neck": "Neck",
        "Groin": "Groin",
        "UpperLeg_L": "Left_Thigh",
        "UpperLeg_R": "Right_Thigh",
        "LowerLeg_L": "Left_Shin",
        "LowerLeg_R": "Right_Shin",
        "Foot_L": "Left_Foot",
        "Foot_R": "Right_Foot",
        "Back": "Back",
        "Unknown": "Unknown_Body_Part"
    }

    language_code = translate.get_language_code()
    blood_location = item_data.get('BloodLocation', None)
    if blood_location is None:
        return default

    if isinstance(blood_location, str):
        blood_location = [blood_location]

    body_parts = []
    
    for location in blood_location:
        if location in BODY_PART_DICT:
            for part in BODY_PART_DICT[location]:
                if link:
                    translation_string = BODY_PART_TRANSLATIONS.get(part, "Unknown_Body_Part")
                    translated_part = translate.get_translation(translation_string, 'BodyPart')
                
                    if language_code != 'en':
                        body_parts.append(f"[[Body parts/{language_code}#{translated_part}|{translated_part}]]")
                    else:
                        body_parts.append(f"[[Body parts#{translated_part}|{translated_part}]]")
                else:
                    body_parts.append(part)

        else:
            if link:
                if language_code != 'en':
                    body_parts.append(f"[[Body parts#{location}|{location}]]")
                else:
                    body_parts.append(f"[[Body parts/{language_code}#{location}|{location}]]")
            else:
                body_parts.append(location)

    return body_parts


# returns a formatted skill
def get_skill_type_mapping(item_data, item_id):
    skill_mapping = {
        "Axe": "Axe (skill)",
        "SmallBlunt": "Short Blunt",
        "Blunt": "Long Blunt",
        "SmallBlade": "Short Blade",
        "LongBlade": "Long Blade",
    }

    skill = item_data.get('Categories', item_data.get('SubCategory'))
    if skill is not None:
        if isinstance(skill, str):
            skill = [skill]
        if "Improvised" in skill:
            skill = [cat for cat in skill if cat != "Improvised"]
        if skill:
            if len(skill) > 1:
                skill = "<br>".join(skill)
                print(f"More than one skill value found for {item_id} with a value of: {skill}")
                return skill
            skill = skill[0]
            if skill == "Firearm":
                skill = "Aiming"

            skill_translation = translate.get_translation(skill, "Categories")
            language_code = translate.get_language_code()
            if language_code == "en":
                skill_page = skill_mapping.get(skill, skill_translation)
                link = f"[[{skill_page}]]"
            else:
                skill_page = skill_mapping.get(skill, skill)
                lang = f"/{language_code}"
                if skill_page != skill_translation:
                    link = f"[[{skill_page}{lang}|{skill_translation}]]"
                else:
                    link = f"[[{skill_page}{lang}]]"

            return link if skill_page else "N/A"


# parses burn info from camping_fuel.lua
def get_burn_data(tables=None):
    """Parses burn time from camping_fuel.lua.

    Args:
        tables (list, optional): List of table names to retrieve from the parsed data. If None, returns all parsed data. Defaults to None.

    Returns:
        dict: Parsed burn data, either all tables or the specified ones.
    """
    global parsed_burn_data
    output_data = {}

    # Record first run so we don't parse data every call
    if parsed_burn_data != {}:
        first_run = False
    else:
        first_run = True

    # Only parse data once, not on every call
    if first_run:
        file_path = Path("resources") / "lua" / "camping_fuel.lua"
        json_file_path = Path("output") / "logging" / "parsed_burn_data.json"

        if not file_path.exists():
            print(f"Lua file not found, ensure 'setup' has been run: {file_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        table_pattern= re.compile(r"(\w+)\s*=\s*{(.*?)}", re.DOTALL)
        key_value_pattern = re.compile(r'(\w+)\s*=\s*([\d./]+)')

        # Parse table/dict
        for match in table_pattern.finditer(content):
            table_name = match.group(1)
            table_content = match.group(2)

            # Parse key-value pairs
            table_data = {}
            for kv_match in key_value_pattern.finditer(table_content):
                key = kv_match.group(1)
                value = kv_match.group(2)

                if '/' in value:
                    value = eval(value)
                else:
                    value = float(value)

                table_data[key] = value
            
            # Add the table to data dictionary
            parsed_burn_data[table_name] = table_data

        # Save parsed data to a json file, for debugging
        json_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(parsed_burn_data, json_file, indent=4)
#            print(f"JSON file saved to {json_file_path}")

    if tables is None:
        return parsed_burn_data
    
    for table in tables:
        output_data[table] = parsed_burn_data[table]

    return output_data


# Gets and calculates the burn time and outputs it as an hours and minutes string.
def get_burn_time(item_id, item_data):
    valid_fuel = False
    module, item_type = item_id.split(".")
    category = item_data["Type"]
    weight = float(item_data.get("Weight", 1))
    tags = item_data.get("Tags", [])
    if isinstance(tags, str): tags = [tags]
    fabric_type = item_data.get("FabricType", "")
    fuel_data = get_burn_data()
    fire_fuel_ratio = float(item_data.get("FireFuelRatio", 0))
    campingFuelType = fuel_data["campingFuelType"]
    campingFuelCategory = fuel_data["campingFuelCategory"]
    campingLightFireType = fuel_data["campingLightFireType"]
    campingLightFireCategory = fuel_data["campingLightFireCategory"]

    # Logic copied from `ISCampingMenu.shouldBurn()` and `ISCampingMenu.isValidFuel()`
    if "IsFireFuel" in tags or float(item_data.get("FireFuelRatio", 0)) > 0: valid_fuel = True
    if campingFuelType.get(item_type) or campingFuelCategory.get(category): valid_fuel = True
    if campingFuelType.get(item_type) == 0: valid_fuel = False
    if campingFuelCategory.get(category) == 0: valid_fuel = False
    if "NotFireFuel" in tags: valid_fuel = False
    if category.lower() == "clothing" and (fabric_type == "" or fabric_type.lower() == "leather"): valid_fuel = False

    if valid_fuel:
        # Logic copied from `ISCampingMenu.getFuelDurationForItemInHours()`
        value = None
        if campingFuelType.get(item_type): value = campingFuelType[item_type]
        elif campingLightFireType.get(item_type): value = campingLightFireType[item_type]
        elif campingFuelCategory.get(category): value = campingFuelCategory[category]
        elif campingLightFireCategory.get(category): value = campingLightFireCategory[category]

        burn_ratio = 2/3

        if category.lower() in ["clothing", "container", "literature", "map"]: burn_ratio = 1/4
        if fire_fuel_ratio > 0: burn_ratio = fire_fuel_ratio
        weight_value = weight * burn_ratio

        if value:
            value = min(value, weight_value)
        else:
            value = weight_value

        # Process value, changing to 'hours, minutes'
        hours = int(value)
        minutes = (value - hours) * 60

        # Translate 'hour' and 'minute' then determine if should be plural
        hours_unit = translate.get_translation("IGUI_Gametime_hour", None)
        minutes_unit = translate.get_translation("IGUI_Gametime_minute", None)
        if hours != 1: hours_unit = translate.get_translation("IGUI_Gametime_hours", None)
        if minutes != 1: minutes_unit = translate.get_translation("IGUI_Gametime_minutes", None)

        # Remove decimal where appropriate
        if minutes % 1 == 0:
            minutes = f"{int(minutes)}"
        else:
            minutes = f"{minutes:.1f}".removesuffix(".0")

        # Convert to appropriate string layout
        if hours > 0:
            if minutes != 0:
                burn_time = f"{hours} {hours_unit}, {minutes} {minutes_unit}"
            else:
                burn_time = f"{hours} {hours_unit}"
        else:
            burn_time = f"{minutes} {minutes_unit}"
    else:
        burn_time = ""
    
    return burn_time


# format a link
def format_link(name, page=None):
    langauge_code = translate.get_language_code()
    if langauge_code != "en":
        link = f"[[{page}/{langauge_code}|{name}]]"
    else:
        if page is None or page == name:
            link = f"[[{page}]]"
        else:
            link = f"[[{page}|{name}]]"

    return link


# TODO: Unused. Can it be removed? We should instead have a for loop using format_link()
# formats values to be links (list)
def format_links(values):
    if not values:
        return ''
    if not isinstance(values, list):
        values = [values]
    values = [f"[[{v.strip()}]]" for v in values]
    values = format_br(values)
    return values


# formats values separated by <br> (list)
def format_br(values):
    if not values:
        return ''
    if not isinstance(values, list):
        values = [values]
    return "<br>".join(values)


# Gets an item name. This is for special cases where the name needs to be manipulated.
def get_name(item_id, item_data, language="en"):
    lang_code = translate.get_language_code()
    # The following keys are used to construct the name:
    # item_id: The item ID this special case is applicable to.
    # prefix: The text to appear at the beginning of the string.
    # infix: The text to appear in the middle of the string. Default will be the DisplayName.
    # suffix: The text to appear at the end of the string.
    # replace: Replace the entire string with this. This overwrites all other strings.
    ITEM_NAMES = {
        "bible": {
            "item_id": ["Base.Book_Bible", "Base.BookFancy_Bible", "Base.Paperback_Bible"],
            "suffix": f': {translate.get_translation("TheBible", "BookTitle", language if language == "en" else lang_code)}'
        },
        "Newspaper_Dispatch_New": {
            "item_id": ["Base.Newspaper_Dispatch_New"],
            "suffix": f': {translate.get_translation("NationalDispatch", "NewspaperTitle", language if language == "en" else lang_code)}'
        },
        "Newspaper_Herald_New": {
            "item_id": ["Base.Newspaper_Herald_New"],
            "suffix": f': {translate.get_translation("KentuckyHerald", "NewspaperTitle", language if language == "en" else lang_code)}'
        },
        "Newspaper_Knews_New": {
            "item_id": ["Base.Newspaper_Knews_New"],
            "suffix": f': {translate.get_translation("KnoxKnews", "NewspaperTitle", language if language == "en" else lang_code)}'
        },
        "Newspaper_Times_New": {
            "item_id": ["Base.Newspaper_Times_New"],
            "suffix": f': {translate.get_translation("LouisvilleSunTimes", "NewspaperTitle", language if language == "en" else lang_code)}'
        },
        "BusinessCard_Nolans": {
            "item_id": ["Base.BusinessCard_Nolans"],
            "suffix": f': {translate.get_translation("NolansUsedCars", "IGUI", language if language == "en" else lang_code)}'
        },
        "Flier_Nolans": {
            "item_id": ["Base.Flier_Nolans"],
            "suffix": f': {translate.get_translation("NolansUsedCars_title", "PrintMedia", language if language == "en" else lang_code)}'
        }
    }

    # Check if item_id is in the dict, and therefore is a special case
    item_key = None
    for key, value in ITEM_NAMES.items():
        if item_id in value["item_id"]:
            item_key = key
            break

    # If the item_id doesn't exist in the dict, we return the translation (normal)
    if item_key is None:
        # We don't need to translate if language is "en", as it's already been translated in the parser.
        if translate.get_language_code() == "en" or language == "en":
            return item_data.get("DisplayName", "Unknown")
        return translate.get_translation(item_id, "DisplayName")

    special_case = ITEM_NAMES[item_key]

    # Special case: return 'replace' value
    if special_case.get("replace"):
        return special_case["replace"]

    # Special case: combine 'prefix', 'infix', 'suffix'
    prefix = special_case.get("prefix", "")
    infix = special_case.get("infix", "")
    suffix = special_case.get("suffix", "")
    # infix should always be present, and defaults to DisplayName
    if infix == "":
        if language == "en":
            infix = translate.get_translation(item_id, "DisplayName", "en")
        else:
            infix = translate.get_translation(item_id, "DisplayName")

    item_name = prefix + infix + suffix

    return item_name


# get page name based on item_id using 'item_id_dictionary.csv'
def get_page(item_id, name="Unknown"):
    dict_csv = 'resources/item_id_dictionary.csv'
    
    with open(dict_csv, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if item_id in row[1:]:
                return row[0]

#    print(f"Couldn't find a page for '{item_id}'")
    logging_file.log_to_file(f"Couldn't find a page for '{item_id}'")
    return name


def find_icon(item_id, all_icons=False):
    """
    Retrieves the icon associated with a given item_id. Can return a single icon (string) (default) or multiple icons (list),
    depending on the 'get_all_icons' parameter.

    :param item_id (str): The ID of the item for which to retrieve the icon.
    :param get_all_icons (bool, optional): If True, returns all icon variants as a list. If False (default), returns only the first icon as a string.

    :return: The icon (or list of icons) associated with the item_id. Returns the default icon ("Question_On") if no specific icon is found.
    :rtype: icon (list[str])
    """
    icon_dir = os.path.join('resources', 'icons')
    icon_default = "Question_On"
    icon = icon_default

    def check_icon_exists(icon_name):
        if os.path.exists(icon_dir):
            files = os.listdir(icon_dir)

            if isinstance(icon_name, list):
                updated_icons = []
                for name in icon_name:
                    for file in files:
                        if file.lower() == name.lower():
                            updated_icons.append(file)
                            break
                return updated_icons

            elif isinstance(icon_name, str):
                for file in files:
                    if file.lower() == icon_name.lower():
                        return file
        return icon_name

    if item_id:

        # Try get icon from custom icons
        icons_csv = os.path.join('resources', 'icons.csv')
        if os.path.exists(icons_csv):
            with open(icons_csv, newline='', encoding='UTF-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if row['item_id'] == item_id:
                        icon = row['icon'] + ".png"
                        icon = [icon]

                        # Return the icon in the expected format based on 'all_icons'
                        if all_icons:
                            return icon
                        return icon[0]
        else:
            print(f"File '{icons_csv}' does not exist. Getting icon from item properties.")

        # Try get icon from item properties
        parsed_item_data = item_parser.get_item_data()
        if item_id in parsed_item_data:
            item_data = parsed_item_data[item_id]
            if 'Icon' in item_data:
                icon = item_data['Icon']

                # Get icon for tiles
                if icon == 'default':
                    icon = item_data.get('WorldObjectSprite', 'Flatpack')

                # Check if icon has variants
                else:
                    icon_variants = ['Rotten', '_Rotten', 'Spoiled', 'Cooked', 'Burnt', '_Burnt', 'Overdone']
                    icons = []
                    if isinstance(icon, str):
                        icons = [icon]
                    for variant in icon_variants:
                        variant_icon = f"{icon}{variant}.png"
                        if os.path.exists(os.path.join(icon_dir, variant_icon)):
                            icons.append(variant_icon)
                    icon = icons

            # Get 'IconsForTexture' icons
            # We need to check for lowercase property key as game now ignores case (╯°□°）╯︵ ┻━┻
            elif any(key.lower() == 'iconsfortexture' for key in item_data):
                icon = next(value for key, value in item_data.items() if key.lower() == 'iconsfortexture')
            
            # tile items may not have `Icon` but will still use `WorldObjectSprite` as icon
            elif 'WorldObjectSprite' in item_data:
                icon = item_data['WorldObjectSprite']
            else:
                icon = icon_default

            # Remove 'Item_' prefix if it has it
            if isinstance(icon, str):
                icon = icon.removeprefix("Item_")
            elif isinstance(icon, list):
                icon = [i.removeprefix("Item_") for i in icon]


        else:
            print(f"'{item_id}' could not be found while getting icon.")
            icon = icon_default
    
    else:
        icon = icon_default
    
    if all_icons:
        # Convert string to list
        if isinstance(icon, str):
            icon = [icon]
        # Add '.png' to the end if it's missing.
        icon = [i if i.endswith('.png') else f"{i}.png" for i in icon]
    else:
        # Convert list to string
        if isinstance(icon, list):
            icon = icon[0]
        # Add '.png' to the end if it's missing.
        if not icon.endswith('.png'):
            icon = f"{icon}.png"
    

    # Check if the icon exists
    matched_icon = check_icon_exists(icon)
    if matched_icon:
        if matched_icon != icon:
            logging_file.log_to_file(f"Icon was modified for {item_id} with icon: {icon}", False, "log_modified_icons.txt")
        icon = matched_icon
    else:
        logging_file.log_to_file(f"Missiong icon for '{item_id}' with icon: {icon}", False, "log_missing_icons.txt")

    return icon


def get_icon(item_id, format=False, all_icons=False, cycling=False):
    """
    Retrieves the icon(s) associated with a given item_id, with optional formatting and cycling through multiple icons.

    :param item_id: The ID of the item for which to retrieve the icon(s).
    :type item_id: str
    :param format: If True, formats the icon(s) with language-specific links, display names, and cycling support. 
                                    Defaults to False.
    :type format: bool, optional
    :param all_icons: If True, returns all icon variants for the item_id. If False, only the primary icon is returned.
                                       Defaults to False.
    :type all_icons: bool, optional
    :param cycling: If True, formats the icons as a cycling image if there are multiple icons. 
                                     This option will force all_icons to be True. Defaults to False.
    :type cycling: bool, optional

    :return: The icon(s) associated with the item_id. If format is True, returns a formatted string. If format is False, 
             returns either a single icon (str).
    :rtype: icon_result (str)
    """
    # Make sure item_id has a value
    if not item_id:
        return item_id
    item_id = fix_item_id(item_id)
    parsed_item_data = item_parser.get_item_data()
    # Check if item_id exists
    if item_id in parsed_item_data:

        # All cycling icons should get all icons
        if cycling:
            all_icons = True
        
        # Get the icon(s) for the item_id
        icons = find_icon(item_id, all_icons)

        # Format icons
        if format:
            
            language_code = translate.get_language_code()
            lcs = ""
            if language_code != "en":
                lcs = f"/{language_code}"

            item_data = parsed_item_data[item_id]
            name = item_data.get('DisplayName', 'Unknown')
            page = get_page(item_id, name)
            name = translate.get_translation(item_id, 'DisplayName')
            # Convert strings to a list for further processing
            if isinstance(icons, str):
                icons = [icons]
            icon_list = []
            # Iterate through each icon and format it
            for icon in icons:
                icon_formatted = f"[[File:{icon}|32x32px|link={page}{lcs}|{name}]]"
                icon_list.append(icon_formatted)

            # Convert to cycling icon if enabled and more than one icon
            if cycling and len(icon_list) > 1:
                icon_result = f'<span class="cycle-img">{"".join(icon_list)}</span>'
            else:
                icon_result = ''.join(icon_list)


        else:
            icon_result = icons
    else:
        print(f"Item ID '{item_id}' doesn't exist")

    return icon_result


def get_guid(item_data):
    guid = get_clothing_xml_value(item_data, 'm_GUID')

    if isinstance(guid, list):
        print("Multiple GUIDs found:", guid)
        return ''
    
    return guid


def get_fluid_name(fluid_data, lang=None):
    display_name = fluid_data.get('DisplayName', 'Fluid')
    display_name_prefix = "Fluid_Name_"
    if display_name.startswith(display_name_prefix):
        display_name = display_name[len(display_name_prefix):]

    if lang is None:
        name = translate.get_translation(display_name, 'FluidID')
    else:
        name = translate.get_translation(display_name, 'FluidID', lang)
    return name