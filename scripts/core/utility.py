import os
import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from scripts.parser import item_parser
from scripts.core import translate, logging_file


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
            print(f"No XML file found for ClothingItem '{clothing_item}'. Is it in the correct directory?")
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
        if model.endswith('_Ground'):
            model = model.replace('_Ground', '')
        elif model.endswith('Ground'):
            model = model.replace('Ground', '')
    
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
    icon_default = "Question_On"
    icon = icon_default

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

                        return icon
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
                        icon_dir = os.path.join('resources', 'icons')
                        variant_icon = f"{icon}{variant}.png"
                        if os.path.exists(os.path.join(icon_dir, variant_icon)):
                            icons.append(variant_icon)
                    icon = icons
                    

            elif 'IconsForTexture' in item_data:
                icon = item_data['IconsForTexture']
            
            # tile items may not have `Icon` but will still use `WorldObjectSprite` as icon
            elif 'WorldObjectSprite' in item_data:
                icon = item_data['WorldObjectSprite']
            else:
                icon = icon_default     

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
                icon_result = f'<span class="cycle-img">{''.join(icon_list)}</span>'
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