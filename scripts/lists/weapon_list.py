import os
from tqdm import tqdm
from scripts.parser import item_parser, script_parser
from scripts.core import translate, utility

pbar_format = "{l_bar}{bar:30}{r_bar}"

# table header for melee weapons
melee_header = """<div style="overflow: auto; white-space: nowrap;">
{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"
! rowspan=2 | <<icon>>
! rowspan=2 | <<name>>
! rowspan=2 | [[File:Status_HeavyLoad_32.png|link=|<<weight>>]]
! rowspan=2 | [[File:UI_Hand.png|32px|link=|<<equipped>>]]
! colspan=4 | <<damage>>
! colspan=2 | <<range>>
! rowspan=2 | [[File:UI_AttackSpeed.png|32px|link=|<<attack_speed>>]]
! rowspan=2 | [[File:UI_Critical_Chance.png|32px|link=|<<crit_chance>>]]
! rowspan=2 | [[File:UI_Critical_Multiply.png|32px|link=|<<crit_multiplier>>]]
! rowspan=2 | [[File:UI_Knockback.png|32px|link=|<<knockback>>]]
! rowspan=2 | [[File:UI_Condition_Max.png|32px|link=|<<max_condition>>]]
! rowspan=2 | [[File:UI_Condition_Chance.png|32px|<<condition_lower_chance>>]]
! rowspan=2 | [[File:UI_Condition_Average.png|32px|link=|<<average_condition>>]]
! rowspan=2 | <<item_id>>
|-
! [[File:UI_Damage_Min.png|32px|link=|<<min_damage>>]]
! [[File:UI_Damage_Max.png|32px|link=|<<max_damage>>]]
! [[File:Door.png|32px|link=|<<door_damage>>]]
! rowspan=2 | [[File:Container_Plant.png|32px|link=|<<tree_damage>>]]
! [[File:UI_Range_Min.png|32px|link=|<<min_range>>]]
! style="border-right: var(--border-mw);" | [[File:UI_Range_Max.png|32px|link=|<<max_range>>]]\n"""

# TODO: re-add this line after fixing repairing - goes before item_id
# ! rowspan=2 | [[File:UI_Condition.png|32px|link=|<<repairable>>]]

# table header for firearms
firearm_header = """<div style="overflow: auto; white-space: nowrap;">
{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"
! rowspan=2 | <<icon>>
! rowspan=2 | <<name>>
! rowspan=2 | [[File:Status_HeavyLoad_32.png|link=|<<weight>>]]
! rowspan=2 | [[File:UI_Hand.png|32px|link=|<<equipped>>]]
! rowspan=2 | [[File:PistolAmmo.png|link=|<<ammo>>]]
! rowspan=2 | [[File:BerettaClip.png|link=|<<mag_capacity>>]]
! colspan=2 | <<damage>>
! colspan=2 | <<range>>
! rowspan=2 | [[File:UI_Accuracy.png|32px|link=|<<accuracy>>]]
! rowspan=2 | [[File:UI_Accuracy_Add.png|32px|link=|<<accuracy_add>>]]
! rowspan=2 | [[File:UI_Critical_Chance.png|32px|link=|<<crit_chance>>]]
! rowspan=2 | [[File:UI_Critical_Add.png|32px|link=|<<crit_chance_add>>]]
! rowspan=2 | [[File:UI_Noise.png|32px|link=|<<noise_radius>>]]
! rowspan=2 | [[File:UI_Knockback.png|32px|link=|<<knockback>>]]
! rowspan=2 | <<item_id>>
|-
! [[File:UI_Damage_Min.png|32px|link=|<<min_damage>>]]
! [[File:UI_Damage_Max.png|32px|link=|<<max_damage>>]]
! [[File:UI_Range_Min.png|32px|link=|<<min_range>>]]
! style="border-right: var(--border-mw);" | [[File:UI_Range_Max.png|32px|link=|<<max_range>>]]\n"""

# TODO: re-add this line after fixing repairing - goes before item_id
# ! rowspan=2 | [[File:UI_Condition.png|32px|link=|<<repairable>>]]

# store translated skills
skills = {}


def combine_weapon_files(folder="melee"):
    """
    Combines all .txt files from the weapon directory into a single file.
    """
    lc = translate.get_language_code()
    weapon_dir = f'output/{lc}/item_list/weapons/{folder}'
    output_file = f'output/{lc}/item_list/weapons/{folder}_list.txt'

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Open the output file to write
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in sorted(os.listdir(weapon_dir)):
            if filename.endswith('.txt'):
                file_path = os.path.join(weapon_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n')

    print(f"Combined '{folder}' files written to {output_file}")


# function to be efficient with translating skills
def translate_skill(skill, property="Categories"):
    if skill not in skills:
        try:
            skill_translated = translate.get_translation(skill, property, 'en')
            skills[skill] = skill_translated
        except Exception as e:
            print(f"Error translating skill '{skill}': {e}")
            skill_translated = skill
    else:
        skill_translated = skills[skill]
    return skill_translated


# Check if it can be fixed
def check_fixing(item_id):
    module, item_name = item_id.split('.')
    parsed_fixing_data = script_parser.get_fixing_data(True)
    language_code = translate.get_language_code()
    lcs = ""
    if language_code != "en":
        lcs = f"/{language_code}"
    for fixing, fixing_data in parsed_fixing_data[module].items():
        if isinstance(fixing_data, dict) and 'Require' in fixing_data:
            if item_name in fixing_data['Require']:
                return f'[[File:UI Tick.png|link=Condition{lcs}#<<repairing>>|<<repairable>>]]'
    return f'[[File:UI Cross.png|link=Condition{lcs}#<<repairing>>|<<not_repairable>>]]'


# get values for each firearm
def process_item_firearm(item_data, item_id):
    all_item_data = item_parser.get_item_data()
    language_code = translate.get_language_code()
    if language_code == 'en':
        lcs = ""
    else:
        lcs = f"/{language_code}"
    skill = "Handgun"
    equipped = "<<1h>>"
    if item_data.get("RequiresEquippedBothHands", '').lower() == "true":
        skill = "Rifle"
        equipped = "<<2h>>"
        if int(item_data.get("ProjectileCount")) > 1:
            skill = "Shotgun"
    equipped = translate.get_wiki_translation(equipped)
    
    name = utility.get_name(item_id, item_data, language="en")
    page_name = utility.get_page(item_id)
    name = utility.get_name(item_id, item_data)
    link = utility.format_link(name, page_name)
    icon = utility.get_icon(item_id, True, True, True)
    
    ammo = "-"
    ammo_id = item_data.get('AmmoType', '')
    if ammo_id:
        ammo = utility.get_icon(ammo_id, True, True, True)

    condition_max = item_data.get("ConditionMax", '0')
    condition_chance = item_data.get("ConditionLowerChanceOneIn", '0')
    condition_average = str(int(condition_max) * int(condition_chance))
    repairable = check_fixing(item_id)
    repairable = translate.get_wiki_translation(repairable)

    item = {
        "name": name,
        "icon": icon,
        "name_link": link,
        "weight": item_data.get('Weight', '1'),
        "equipped": equipped,
        "ammo": ammo,
        "clip_size": item_data.get('MaxAmmo', item_data.get('ClipSize', '')),
        "damage_min": item_data.get('MinDamage', '-'),
        "damage_max": item_data.get('MaxDamage', '-'),
        "min_range": item_data.get('MinRange', '-'),
        "max_range": item_data.get('MaxRange', '-'),
        "hit_chance": item_data.get('HitChance', '-') + '%',
        "hit_chance_mod": '+' + item_data.get('AimingPerkHitChanceModifier', '-') + '%',
        "crit_chance": item_data.get('CriticalChance', '-') + '%',
        "crit_chance_mod": '+' + item_data.get('AimingPerkCritModifier', '-') + '%',
        "sound_radius": item_data.get('SoundRadius', '-'),
        "knockback": item_data.get('PushBackMod', '-'),
#        "condition_max": condition_max,
#        "condition_chance": condition_chance,
#        "condition_average": condition_average,
#        "repairable": repairable, # TODO: re-add after fixing repairing
        "item_id": f'{{{{ID|{item_id}}}}}',
    }

    return skill, item


# get values for each melee waepon
def process_item_melee(item_data, item_id):
    language_code = translate.get_language_code()
    if language_code == 'en':
        lcs = ""
    else:
        lcs = f"/{language_code}"
    
    skill = item_data.get("Categories", '')
    if isinstance(skill, str):
        skill = [skill]
    # Remove "Improvised" from list if more than 1
    if "Improvised" in skill and len(skill) > 1:
        skill = [cat for cat in skill if cat != "Improvised"]

    skill = " and ".join(skill)
    skill_translated = translate_skill(skill, "Categories")
    if skill_translated is not None:
        skill = skill_translated
    #FIXME: translate skill just before writing, so we can name files in English.
#    if skill == "Improvised":
#        skill = "<<improvised>>"
#        skill = translate.get_wiki_translation(skill)
    
    
    name = utility.get_name(item_id, item_data, language="en")
    page_name = utility.get_page(item_id, name)
    name = utility.get_name(item_id, item_data)
    link = utility.format_link(name, page_name)
    icon = utility.get_icon(item_id, True, True, True)

    equipped = "<<1h>>"
    if item_data.get("RequiresEquippedBothHands", "FALSE").lower() == "true":
        equipped = "<<2h>>"
    elif item_data.get("TwoHandWeapon", "FALSE").lower() == "true":
        equipped = "{{Tooltip|<<2h>>*|<<limited_impact_desc>>}}"
    if item_data.get("CloseKillMove") == "Jaw_Stab":
        equipped = "{{Tooltip|<<1h>>*|<<jaw_stab_desc>>}}"
    equipped = translate.get_wiki_translation(equipped)

    crit_chance = item_data.get("CriticalChance", "-")
    if crit_chance != "-":
        crit_chance = f"{crit_chance}%"
    crit_multiplier = item_data.get("CritDmgMultiplier", "-")
    if crit_multiplier != "-":
        crit_multiplier = f"{crit_multiplier}×"

    condition_max = item_data.get("ConditionMax", '0')
    condition_chance = item_data.get("ConditionLowerChanceOneIn", '0')
    condition_average = str(int(condition_max) * int(condition_chance))
    repairable = check_fixing(item_id)
    repairable = translate.get_wiki_translation(repairable)

    item = {
        "name": name,
        "icon": icon,
        "name_link": link,
        "weight": item_data.get('Weight', '1'),
        "equipped": equipped,
        "damage_min": item_data.get('MinDamage', '-'),
        "damage_max": item_data.get('MaxDamage', '-'),
        "damage_door": item_data.get('DoorDamage', '-'),
        "damage_tree": item_data.get('TreeDamage', '-'),
        "min_range": item_data.get('MinRange', '-'),
        "max_range": item_data.get('MaxRange', '-'),
        "base_speed": item_data.get('BaseSpeed', '1'),
        "crit_chance": crit_chance,
        "crit_multiplier": crit_multiplier,
        "knockback": item_data.get('PushBackMod', '-'),
        "condition_max": condition_max,
        "condition_chance": condition_chance,
        "condition_average": condition_average,
#        "repairable": repairable, # TODO: re-add after fixing repairing
        "item_id": f"{{{{ID|{item_id}}}}}",
    }

    return skill, item


# write to file
def write_items_to_file(skills, header, category):
    language_code = translate.get_language_code()
    output_dir = f'output/{language_code}/item_list/weapons/{category}/'
    os.makedirs(output_dir, exist_ok=True)
    
    for skill, items in skills.items():
        output_path = f"{output_dir}{skill}.txt"
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(f"<!--BOT FLAG-start-{skill}. DO NOT REMOVE-->")
            header = translate.get_wiki_translation(header)
            file.write(f"{header}")
            sorted_items = sorted(items, key=lambda x: x['name'])

            for item in sorted_items:
                # remove 'name' before writing
                item = [value for key, value in item.items() if key != 'name']
                item = '\n| '.join(item)
                file.write(f"|-\n| {item}\n")
            caption = ""
            if skill in ('Axe', 'Long Blunt', 'Short Blunt', 'Long Blade', 'Spear'):
                caption = '|-\n|+ style="caption-side:bottom; font-weight:normal;" | <nowiki>*</nowiki><<limited_impact_desc>>\n'
            elif skill == ('Short Blade'):
                caption = '|-\n|+ style="caption-side:bottom; font-weight:normal;" | <nowiki>*</nowiki><<jaw_stab_desc>>\n'
            caption = translate.get_wiki_translation(caption)
            file.write(caption)
            file.write("|}</div>")
            file.write(f"<!--BOT_FLAG-end-{skill.replace(" ", "_")}. DO NOT REMOVE-->")
    
    print(f"{category.title()} tables completed. Files can be found in '{output_dir}'")


def get_items():
    melee_skills = {}
    firearm_skills = {}
    parsed_item_data = item_parser.get_item_data()

    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=pbar_format, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f"Processing: {item_id[:15]}")
            if item_data.get("Type") == "Weapon":

                if item_data.get("Categories"):
                    skill, item = process_item_melee(item_data, item_id)

                    if skill not in melee_skills:
                        melee_skills[skill] = []
                    melee_skills[skill].append(item)

                elif item_data.get("SubCategory") == "Firearm":
                    skill, item = process_item_firearm(item_data, item_id)

                    if skill not in firearm_skills:
                        firearm_skills[skill] = []
                    firearm_skills[skill].append(item)

                # TODO: add explosives

            pbar.update(1)
        pbar.bar_format = f"Items processed."

    write_items_to_file(melee_skills, melee_header, 'melee')
    write_items_to_file(firearm_skills, firearm_header, 'firearm')


def main():
    get_items()
    while True:
        user_input = input("Want to merge list files? (Y/N)\n> ").lower()
        
        if user_input == "n":
            break
        elif user_input == "y":
            combine_weapon_files("melee")
            combine_weapon_files("firearm")
            break


if __name__ == "__main__":
    main()
