import os
from core import translate
import script_parser

page_mapping = {
    "Axe": "Axe (skill)",
}


# gets 'Tags' for item_data
def get_tags(item_data):
    tags = []
    tags = item_data.get('Tags', '')
    return tags


#get an icon for item_data
def get_icon(item_data):
    icon = item_data.get('Icon', '')
    if icon in ('', 'default'):
        if 'IconsForTexture' in item_data:
            icon = item_data.get('IconsForTexture')
            icon = icon[0]
        else:
            icon = item_data.get('WorldObjectSprite', 'Question')

    return icon

# gets all icons for item_data and return as a list
def get_icons(item_data):
    icon_dir = 'resources/icons/'
    icons = []

    # check if 'IconsForTexture' property exists and use it for icon
    if 'IconsForTexture' in item_data:
        icons = item_data.get('IconsForTexture', [''])
        icons = [f"{icon}.png" for icon in icons]
    else:
        # get 'Icon' property
        icon = item_data.get('Icon', 'Question')

        # check if 'WorldObjectSprite' property exists and use it for icon
        if icon == "default":
            icon = item_data.get('WorldObjectSprite', ['Flatpack'])
        icons.append(f"{icon}.png")

        # check if icon has variants
        icon_variants = ['Rotten', 'Cooked', '_Cooked', 'Burnt', 'Overdone']
        for variant in icon_variants:
            variant_icon = f"{icon}{variant}.png"
            if os.path.exists(os.path.join(icon_dir, variant_icon)):
                icons.append(variant_icon)

    return icons


# gets 'Icon' for an item_id
def get_icon_from_id(item_id):
    current_module, current_item_type = item_id.split('.')
    icon = "Question"
    for module, module_data in script_parser.parsed_item_data.items():
        if module == current_module:
            for item_type, item_data in module_data.items():
                if item_type == current_item_type:
                    icon = item_data.get('Icon')

    return icon


# gets 'Icon' for list of item_id and formats as wiki image.
def get_icons_for_item_ids(item_ids):
    parsed_data = script_parser.parsed_item_data
    if not item_ids:
        return ""
    
    if isinstance(item_ids, str):
        item_ids = [item_ids]

    icons = []

    for item_id in item_ids:
        try:
            module, item_type = item_id.split('.')
        except ValueError:
            continue
        icon = parsed_data.get(module, {}).get(item_type, {}).get('Icon', 'Unknown')
        display_name = parsed_data.get(module, {}).get(item_type, {}).get('DisplayName', 'Unknown')
        if icon != 'Unknown' and display_name != 'Unknown':
            icons.append(f"[[File:{icon}.png|link={display_name}]]")
    return "".join(icons)


# gets model for item_data as PNG
def get_model(item_data):
    model = item_data.get('WeaponSprite', item_data.get('WorldStaticModel', item_data.get('StaticModel', '')))
    if model == '':
        return ''
    if model.endswith('_Ground'):
        model = model.replace('_Ground', '')
    model = f"{model}_Model.png"
    return model


# returns a formatted skill
def get_skill_type_mapping(item_data, item_id):

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
            if translate.language_code == "en":
                skill_page = page_mapping.get(skill, skill_translation)
                link = f"[[{skill_page}]]"
            else:
                skill_page = page_mapping.get(skill, skill)

            if translate.language_code != "en":
                lang = f"/{translate.language_code}"
            else:
                lang = ""
            if skill_page != skill_translation:
                link = f"[[{skill_page}{lang}|{skill_translation}]]"
            return link
        else:
            return "N/A"
        
    return


# formats values to be a link
def format_link(values):
    if not values:
        return ''
    if not isinstance(values, list):
        values = [values]
    values = [f"[[{v.strip()}]]" for v in values]
    values = format_br(values)
    return values


# formats values separated by <br>
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
def get_module_from_item(item_data, property_name):
    item_types = item_data.get(property_name, [])
    modules = {}
    
    for item_type in item_types:
        item_type = item_type.strip()
        for module, items in script_parser.parsed_item_data.items():
            if item_type in items:
                modules[item_type] = f"{module}.{item_type}"
                break

    return modules