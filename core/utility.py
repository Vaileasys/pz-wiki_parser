import os
from core import translate

page_mapping = {
    "Axe": "Axe (skill)",
}

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


# gets icon from a property that is an item_id.
def get_icons_for_item_ids(parsed_data, item_ids):
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


# formats values to be a link
def format_link(values):
    if not values:
        return ''
    if not isinstance(values, list):
        values = [values]
    values = [f"[[{v.strip()}]]" for v in values]
    values = format_line_break(values)
    return values


# formats values separated by <br>
def format_line_break(values):
    if not values:
        return ''
    if not isinstance(values, list):
        values = [values]
    if len(values) > 1:
        return "<br>".join(values)
    else:
        return values[0]