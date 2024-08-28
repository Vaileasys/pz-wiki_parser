import os
import shutil
import script_parser
from core import translate
from core import utility

# table header for melee weapons
melee_header = """{| class="wikitable theme-red sortable" style="text-align: center;"
! rowspan=2 | Icon
! rowspan=2 | Name
! rowspan=2 | [[File:Moodle_Icon_HeavyLoad.png|link=|Encumbrance]]
! rowspan=2 | [[File:UI_Hand.png|32px|link=|Equipped]]
! colspan=4 | Damage
! colspan=2 | Range
! rowspan=2 | [[File:UI_AttackSpeed.png|32px|link=|Attack speed]]
! rowspan=2 | [[File:UI_CriticalHit_Chance.png|32px|32px|link=|Crit chance]]
! rowspan=2 | [[File:UI_CriticalHit_Multiply.png|32px|link=|Crit multiplier]]
! rowspan=2 | [[File:UI_Knockback.png|32px|link=|Knockback]]
! rowspan=2 | [[File:UI_Condition_Max.png|32px|link=|Max condition]]
! rowspan=2 | [[File:UI_Condition_Chance.png|Condition lower chance, 1 in (x + (maintenance × 2 + weapon level))]]
! rowspan=2 | [[File:UI_Condition_Average.png|32px|link=|Average condition at level 0]]
! rowspan=2 | Item ID
|-
! [[File:UI_Damage_Min.png|32px|link=|Minimum damage]]
! [[File:UI_Damage_Max.png|32px|link=|Maximum damage]]
! [[File:UI_Door.png|32px|link=|Door damage]]
! rowspan=2 | [[File:Container_Plant.png|32px|link=|Tree damage]]
! [[File:UI_Range_Min.png|32px|link=|Minimum range]]
! style="border-right: var(--border-mw);" | [[File:UI_Range_Max.png|32px|link=|Maximum range]]\n"""

# table header for firearms
firearm_header = """{| class="wikitable theme-red sortable" style="text-align: center;"
! rowspan=2 | Icon
! rowspan=2 | Name
! rowspan=2 | [[File:Moodle_Icon_HeavyLoad.png|link=|Encumbrance]]
! rowspan=2 | [[File:UI_Hand.png|32px|link=|Equipped]]
! rowspan=2 | [[File:UI_Ammo.png|link=|Ammunition]]
! rowspan=2 | [[File:BerettaClip.png|link=|Magazine capacity]]
! colspan=2 | Damage
! colspan=2 | Range
! rowspan=2 | [[File:UI_Accuracy.png|32px|link=|Accuracy]]
! rowspan=2 | [[File:UI_Accuracy_Add.png|32px|link=|Accuracy increased per aiming level]]
! rowspan=2 | [[File:UI_CriticalHit_Chance.png|32px|link=|Crit chance]]
! rowspan=2 | [[File:UI_Critical_Add.png|32px|link=|Critical hit chance increased per aiming level]]
! rowspan=2 | [[File:UI_Noise.png|32px|link=|Noise radius]]
! rowspan=2 | [[File:UI_Knockback.png|32px|link=|Knockback]]
! rowspan=2 | Item ID
|-
! [[File:UI_Damage_Min.png|32px|link=|Minimum damage]]
! [[File:UI_Damage_Max.png|32px|link=|Maximum damage]]
! [[File:UI_Range_Min.png|32px|link=|Minimum range]]
! style="border-right: var(--border-mw);" | [[File:UI_Range_Max.png|32px|link=|Maximum range]]\n"""

# store translated skills
skills = {}


# function to be efficient with translating skills
def translate_skill(skill, property="Categories"):
    if skill not in skills:
        try:
            skill_translated = translate.get_translation(skill, property)
            skills[skill] = skill_translated
        except Exception as e:
            print(f"Error translating skill '{skill}': {e}")
            skill_translated = skill
    else:
        skill_translated = skills[skill]
    return skill_translated


# get values for each firearm
def process_item_firearm(item_data, item_id):
    skill = "Handgun"
    equipped = "1H"
    if item_data.get("RequiresEquippedBothHands", '').lower() == "true":
        skill = "Rifle"
        equipped = "2H"
        if int(item_data.get("ProjectileCount")) > 1:
            skill = "Shotgun"
    
    name = item_data.get('DisplayName', 'Unknown')
    page_name = utility.get_page(item_id)
    link = utility.format_link(name, page_name)
    icon = utility.get_icon(item_data, item_id)
    
    ammo = "-"
    ammo_id = item_data.get('AmmoType', '')
    if ammo_id:
        ammo_data = utility.get_item_data_from_id(ammo_id)
        ammo_name = ammo_data.get('DisplayName', 'Unknown')
        ammo_page = utility.get_page(ammo_id)
        ammo_icon = utility.get_icon(ammo_data, ammo_id)
        ammo = f"[[File:{ammo_icon}.png|link={ammo_page}|{ammo_name}]]"

    crit_chance = item_data.get('CriticalChance', '-')
    # calculation from: IsoPlayer.class > calculateCritChance()
    crit_chance_mod = ((int(item_data.get('AimingPerkCritModifier', 0)) / 2) + 3)
    # do not display decimal place if value is a whole number
    crit_chance_mod = (
        str(int(crit_chance_mod)) if crit_chance_mod.is_integer() 
        else str(crit_chance_mod)
    )

    condition_max = item_data.get("ConditionMax", '0')
    condition_chance = item_data.get("ConditionLowerChanceOneIn", '0')
    condition_average = str(int(condition_max) * int(condition_chance))

    item = {
        "name": name,
        "icon": f"[[File:{icon}.png|link={page_name}|{name}]]",
        "name_link": link,
        "weight": item_data.get('Weight', '1'),
        "equipped": equipped,
        "ammo": ammo,
        "clip_size": item_data.get('ClipSize', item_data.get('MaxAmmo', '')),
        "damage_min": item_data.get('MinDamage', '-'),
        "damage_max": item_data.get('MaxDamage', '-'),
        "min_range": item_data.get('MinRange', '-'),
        "max_range": item_data.get('MaxRange', '-'),
        "hit_chance": item_data.get('HitChance', '-') + '%',
        #calculation from: SwipeStatePlayer.class > CalcHitChance()
        "hit_chance_mod": '+' + item_data.get('AimingPerkHitChanceModifier', '-') + '%',
        "crit_chance": crit_chance + '%',
        "crit_chance_mod": '+' + crit_chance_mod + '%',
        "sound_radius": item_data.get('SoundRadius', '-'),
        "knockback": item_data.get('PushBackMod', '-'),
#        "condition_max": condition_max,
#        "condition_chance": condition_chance,
#        "condition_average": condition_average,
        "item_id": f'{{{{ID|{item_id}}}}}',
    }

    return skill, item


# get values for each melee waepon
def process_item_melee(item_data, item_id):

    skill = item_data.get("Categories", '')
    if isinstance(skill, str):
        skill = [skill]
    # remove "Improvised" from list
    if "Improvised" in skill and len(skill) > 1:
        skill = [cat for cat in skill if cat != "Improvised"]

    skill = " and ".join(skill)
    skill_translated = translate_skill(skill, "Categories")
    if skill_translated is not None:
        skill = skill_translated
    
    name = item_data.get('DisplayName', 'Unknown')
    page_name = utility.get_page(item_id)
    link = utility.format_link(name, page_name)
    icon = utility.get_icon(item_data, item_id)

    equipped = "1H"
    if item_data.get("RequiresEquippedBothHands") == "TRUE":
        equipped = "{{Tooltip|2H*|Limited impact when used one-handed.}}"
    elif item_data.get("TwoHandWeapon", "FALSE") == "TRUE":
        equipped = "2H"

    condition_max = item_data.get("ConditionMax", '0')
    condition_chance = item_data.get("ConditionLowerChanceOneIn", '0')
    condition_average = str(int(condition_max) * int(condition_chance))

    item = {
        "name": name,
        "icon": f"[[File:{icon}.png|link={page_name}|{name}]]",
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
        "crit_chance": item_data.get('CriticalChance', '-'),
        "crit_multiplier": item_data.get('CritDmgMultiplier', '-'),
        "knockback": item_data.get('PushBackMod', '-'),
        "condition_max": condition_max,
        "condition_chance": condition_chance,
        "condition_average": condition_average,
        "item_id": f"{{{{ID|{item_id}}}}}",
    }

    return skill, item


# write to file
def write_items_to_file(skills, header, category):
    output_dir = f'output/item_list/weapons/{category}/'
    os.makedirs(output_dir, exist_ok=True)
    
    for skill, items in skills.items():
        output_path = f"{output_dir}{skill}.txt"
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(f"==={skill}===\n{header}")

            sorted_items = sorted(items, key=lambda x: x['name'])

            for item in sorted_items:
                # remove 'name' before writing
                item = [value for key, value in item.items() if key != 'name']
                item = '\n| '.join(item)
                file.write(f"|-\n| {item}\n")
            file.write("|}")


def get_items():
    melee_skills = {}
    firearm_skills = {}

    for module, module_data in script_parser.parsed_item_data.items():
        for item_type, item_data in module_data.items():
            if item_data.get("Type") == "Weapon":
                item_id = f"{module}.{item_type}"

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

    write_items_to_file(melee_skills, melee_header, 'melee')
    write_items_to_file(firearm_skills, firearm_header, 'firearm')


if __name__ == "__main__":
    script_parser.init()
    get_items()
