import os
import csv
from scripts.parser import item_parser
from scripts.core import translate, logging_file, version

# @deprecated: Use version.get_version() directly instead.
version = version.get_version()


# gets 'Tags' for item_data
def get_tags(item_data):
    tags = []
    tags = item_data.get('Tags', '')
    return tags


#get an icon for item_data
def get_icon(item_data, item_id=""):
    icons_csv = 'resources/icons.csv'
    # get icon from icons.csv instead if it exists
    if os.path.exists(icons_csv) and item_id != "":
        with open(icons_csv, newline='', encoding='UTF-8') as csv_file:
            csv_file = csv.reader(csv_file)
            for row in csv_file:
                if row[0] == item_id:
                    return row[1]
    else:
        print(f"File {icons_csv} does not exist. Getting icon from item properties.")

    icon = item_data.get('Icon', '')
    if icon in ('', 'default'):
        if 'IconsForTexture' in item_data:
            icon = item_data.get('IconsForTexture')
            # change to a list, i.e. if it's a string
            if not isinstance(icon, list):
                icon = [icon]
            icon = icon[0]
        else:
            icon = item_data.get('WorldObjectSprite', 'Question_On')

    return icon


# gets all icons for item_data and return as a list
def get_icons(item_data):
    icon_dir = 'resources/icons/'
    icons = []

    # check if 'IconsForTexture' property exists and use it for icon
    if 'IconsForTexture' in item_data:
        icons = item_data.get('IconsForTexture', [''])
        if isinstance(icons, str):
            icons = [icons]
        icons = [f"{icon}.png" for icon in icons]
    else:
        # get 'Icon' property
        icon = item_data.get('Icon', 'Question_On')

        # check if 'WorldObjectSprite' property exists and use it for icon
        if icon == "default":
            icon = item_data.get('WorldObjectSprite', ['Flatpack'])
        icons.append(f"{icon}.png")

        # check if icon has variants
        icon_variants = ['Rotten', 'Spoiled', 'Cooked', '_Cooked', 'Burnt', 'Overdone']
        for variant in icon_variants:
            variant_icon = f"{icon}{variant}.png"
            if os.path.exists(os.path.join(icon_dir, variant_icon)):
                icons.append(variant_icon)

    return icons


# gets parsed item data for an item id
def get_item_data_from_id(query_item_id):
    for item_id, item_data in item_parser.get_item_data().items():
        if query_item_id == item_id:
            return item_data


# gets 'Icon' for list of item_id and formats as wiki image.
def get_icons_for_item_ids(item_ids):
    all_item_data = item_parser.get_item_data()
    language_code = translate.get_language_code()
    if not item_ids:
        return ""
    
    if isinstance(item_ids, str):
        item_ids = [item_ids]

    icons = []

    for item_id in item_ids:
        item_data = all_item_data.get(item_id, {})
        icon = item_data.get('Icon', 'Question_On')
        name = item_data.get('DisplayName', 'Unknown')
        translated_name = translate.get_translation(item_id, 'DisplayName')
        page = get_page(item_id, name)
        if icon != 'Question_On' and name != 'Unknown':
            if language_code == 'en':
                icons.append(f"[[File:{icon}.png|link={page}|{name}]]")
            else:
                icons.append(f"[[File:{icon}.png|link={page}/{language_code}|{translated_name}]]")
    return "".join(icons)


# get 'Icon' from an item_id and format as a wiki image.
def get_icon_for_item_id(item_id):
    parsed_data = item_parser.get_item_data()
    language_code = translate.get_language_code()
    if not item_id:
        return ""
    
    icon = ""

    icon = parsed_data.get(item_id, {}).get('Icon', 'Question_On')
    name = parsed_data.get(item_id, {}).get('DisplayName', 'Unknown')
    translated_name = translate.get_translation(item_id, 'DisplayName')
    page = get_page(item_id, name)
    if name != 'Unknown':
        if language_code == 'en':
            icon = f"[[File:{icon}.png|link={page}|{name}]]"
        else:
            icon = f"[[File:{icon}.png|link={page}/{language_code}|{translated_name}]]"
    return icon

# gets model for item_data as PNG
def get_model(item_data):
    model = item_data.get('WorldStaticModel',item_data.get('WeaponSprite', item_data.get('StaticModel', '')))
    if model == '':
        return ''
    if model.endswith('_Ground'):
        model = model.replace('_Ground', '')
    elif model.endswith('Ground'):
        model = model.replace('Ground', '')
    model = f"{model}_Model.png"
    return model


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
    if page is None or name == page:
        link = f"[[{name}]]"
    
    lcs = ""
    langauge_code = translate.get_language_code()
    if langauge_code != "en":
        lcs = "/" + langauge_code
        link = f"[[{page}{lcs}|{name}]]"

    return link


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
    if len(values) > 1:
        return "<br>".join(values)
    else:
        return values[0]
    

# find a module for an item and return item_id (used for property values that don't define the module)
# TODO: check if this is still needed with the new parser (item_id)
def get_module_from_item(item_data, property_name):
    item_names = item_data.get(property_name, [])
    item_ids = {}
    
    for item_name in item_names:
        item_name = item_name.strip()
        for item_id, item_data in item_parser.get_item_data().items():
            if item_name == item_id.split('.', 1)[1]:
                item_ids[item_name] = item_id
                break

    return item_ids



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
