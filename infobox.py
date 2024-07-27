import os
import shutil
from core import logging
import script_parser
from core import translate

skill_id = {
    "Firearm": "Aiming",
}


page_mapping = {
    "Axe": "Axe (skill)",
}

def get_item(parsed_data):
    while True:
        item_id = input("Enter an item id\n> ")
        for module, module_data in parsed_data.items():
            for item_type, item_data in module_data.items():
                if f"{module}.{item_type}" == item_id:
                    return item_data, item_id
        print(f"No item found for '{item_id}', please try again.")


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
            skill = skill_id.get(skill, skill)

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


# formats sub-properties (i.e. property values separated by ';')
def format_sub_prop(values, format=None):
    if not values:
        return ''
    if not isinstance(values, list):
        values = [values]
    # link
    if format == "link":
        values = [f"[[{v.strip()}]]" for v in values]
    if len(values) > 1:
        return "<br>".join(values)
    else:
        return values[0]


def write_to_output(parsed_data, item_data, item_id, output_dir='output/infoboxes'):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{item_id}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("{{Infobox item")

            category = 'DisplayCategory'
            category = translate.get_translation(item_data.get(category, 'Item'), category)
            
            skill_type = get_skill_type_mapping(item_data, item_id)

            material = item_data.get('FabricType', '')
            material_value = item_data.get('MetalValue', '')
            if not material and material_value:
                material = 'metal'
            material = material.capitalize()

            weapon = script_parser.get_module_from_item(parsed_data, item_data, 'MountOn')
            weapon = get_icons_for_item_ids(parsed_data, weapon.values())

            ammo_type = get_icons_for_item_ids(parsed_data, item_data.get('AmmoType', ''))

            parameters = {
                "name": translate.get_translation(item_id, "DisplayName"),
                "model": f"{item_data.get('WeaponSprite', item_data.get('WorldStaticModel', item_data.get('StaticModel', '')))}_Model.png",
                "icon": f"{item_data.get('Icon', 'Question')}.png",
                "icon_name": item_data.get('DisplayName', ''),
                "category": category,
                "weight": item_data.get('Weight', 1),
                "weight_reduction": item_data.get('WeightReduction', ''),
                "max_units": item_data.get('UseDelta', ''),
                "equipped": item_data.get('CanBeEquipped', ''),
                "attachment_type": item_data.get('AttachmentType', ''),
                "function": '',
                "weapon": weapon,
                "part_type": item_data.get('PartType', ''),
                "skill_type": skill_type,
                "ammo_type": ammo_type,
                "clip_size": item_data.get('MaxAmmo', ''),
                "material": material,
                "material_value": material_value,
                "can_boil_water": item_data.get('IsCookable', '').capitalize(),
                "writable": item_data.get('CanBeWrite', '').capitalize(),
                "recipes": format_sub_prop(item_data.get('TeachedRecipes', '')),
                "skill_trained": item_data.get('SkillTrained', ''),
                "page_number": item_data.get('NumberOfPages') or item_data.get('PageToWrite', ''),
                "packaged": item_data.get('Packaged', '').capitalize(),
                "rain_factor": item_data.get('RainFactor', ''),
                "days_fresh": item_data.get('DaysFresh', ''),
                "days_rotten": item_data.get('DaysTotallyRotten', ''),
                "cant_be_frozen": item_data.get('CantBeFrozen', '').capitalize(),
                "condition_max": item_data.get('ConditionMax', ''),
                "condition_lower_chance": item_data.get('ConditionLowerChanceOneIn', ''),
                "run_speed": item_data.get('RunSpeedModifier', ''),
                "combat_speed": item_data.get('CombatSpeedModifier', ''),
                "scratch_defense": item_data.get('ScratchDefense', ''),
                "bite_defense": item_data.get('BiteDefense', ''),
                "bullet_defense": item_data.get('BulletDefense', ''),
                "neck_protection": item_data.get('NeckProtectionModifier', ''),
                "insulation": item_data.get('Insulation', ''),
                "wind_resistance": item_data.get('WindResistance', ''),
                "water_resistance": item_data.get('WaterResistance', ''),
                "light_distance": item_data.get('LightDistance', ''),
                "light_strength": item_data.get('LightStrength', ''),
                "torch_cone": item_data.get('TorchCone', ''),
                "wet_cooldown": item_data.get('WetCooldown', ''),
                "sensor_range": item_data.get('SensorRange') or item_data.get('RemoteRange', ''),
                "two_way": item_data.get('TwoWay', ''),
                "mic_range": item_data.get('MicRange', ''),
                "transmit_range": item_data.get('TransmitRange', ''),
                "min_channel": item_data.get('MinChannel', ''),
                "max_channel": item_data.get('MaxChannel', ''),
                "damage_type": '',
                "min_damage": item_data.get('MinDamage', ''),
                "max_damage": item_data.get('MaxDamage', ''),
                "door_damage": item_data.get('DoorDamage', ''),
                "tree_damage": item_data.get('TreeDamage', ''),
                "min_range": item_data.get('MinRange', ''),
                "max_range": item_data.get('MaxRange', ''),
                "min_range_mod": item_data.get('MinRangeModifier', ''),
                "max_range_mod": item_data.get('MaxRangeModifier', ''),
                "recoil_delay": item_data.get('RecoilDelay') or item_data.get('RecoilDelayModifier', ''),
                "sound_radius": item_data.get('SoundRadius', ''),
                "base_speed": item_data.get('BaseSpeed', ''),
                "push_back": item_data.get('PushBackMod', ''),
                "aiming_time": item_data.get('AimingTime', ''),
                "reload_time": item_data.get('ReloadTime', ''),
                "crit_chance": item_data.get('CriticalChance', ''),
                "crit_multiplier": item_data.get('CritDmgMultiplier', ''),
                "angle_mod": item_data.get('AngleModifier', ''),
                "kill_move": item_data.get('CloseKillMove', '').replace('_', ' ').capitalize() if item_data.get(
                    'CloseKillMove') else '',
                "weight_mod": item_data.get('WeightModifier', ''),
                "effect_power": item_data.get('ExplosionPower') or item_data.get('FirePower', ''),
                "effect_range": item_data.get('ExplosionRange') or item_data.get('FireRange') or item_data.get(
                    'SmokeRange') or item_data.get('NoiseRange', ''),
                "effect_duration": item_data.get('NoiseDuration', ''),
                "effect_timer": item_data.get('ExplosionTimer', ''),
                "hunger_change": item_data.get('HungerChange', ''),
                "thirst_change": item_data.get('ThirstChange', ''),
                "calories": item_data.get('Calories', ''),
                "carbohydrates": item_data.get('Carbohydrates', ''),
                "proteins": item_data.get('Proteins', ''),
                "lipids": item_data.get('Lipids', ''),
                "unhappy_change": item_data.get('UnhappyChange', ''),
                "boredom_change": item_data.get('BoredomChange', ''),
                "stress_change": item_data.get('StressChange', ''),
                "fatigue_change": item_data.get('FatigueChange', ''),
                "endurance_change": item_data.get('EnduranceChange', ''),
                "flu_change": item_data.get('FluReduction', ''),
                "pain_change": item_data.get('PainReduction', ''),
                "sick_change": item_data.get('ReduceFoodSickness', ''),
                "alcoholic": item_data.get('Alcoholic', '').capitalize(),
                "alcohol_power": item_data.get('AlcoholPower', ''),
                "reduce_infection_power": item_data.get('ReduceInfectionPower', ''),
                "bandage_power": item_data.get('BandagePower', ''),
                "poison_power": item_data.get('PoisonPower', ''),
                "cook_minutes": item_data.get('MinutesToCook', ''),
                "burn_minutes": item_data.get('MinutesToBurn', ''),
                "dangerous_uncooked": item_data.get('DangerousUncooked', '').capitalize(),
                "bad_microwaved": item_data.get('BadInMicrowave', '').capitalize(),
                "good_hot": item_data.get('GoodHot', '').capitalize(),
                "bad_cold": item_data.get('BadCold', '').capitalize(),
                "spice": item_data.get('Spice', '').capitalize(),
                "evolved_recipe": item_data.get('EvolvedRecipeName', ''),
                "tags": format_sub_prop(item_data.get('Tags', '')),  # TODO: use param tag1, tag2, etc.
                "item_id": item_id,
                "infobox_version": "41.78.16"
            }

            for key, value in parameters.items():
                if value:
                    file.write(f"\n|{key}={value}")

            file.write("\n}}")
    except Exception as e:
        print(f"Error writing file {item_id}.txt: {e}")
        logging.log_to_file(f"Error writing file {item_id}.txt: {e}")
        


def process_item(parsed_data, item_data, item_id, output_dir):
    write_to_output(parsed_data, item_data, item_id, output_dir)


def automatic_extraction(parsed_data):
    output_dir = 'output/infoboxes'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for module, module_data in parsed_data.items():
        for item_type, item_data in module_data.items():
            item_id = f"{module}.{item_type}"
            process_item(parsed_data, item_data, item_id, output_dir)


def main():
    parsed_data = script_parser.main()

    choice = input("Select extraction mode (1: automatic, 2: manual):\n> ")
    if choice == '1':
        automatic_extraction(parsed_data)
        print("Extraction complete, the files can be found in output/infoboxes.")
    elif choice == '2':
        item_data, item_id = get_item(parsed_data)
        write_to_output(parsed_data, item_data, item_id)
        print("Extraction complete, the file can be found in output/infoboxes.")
    else:
        print("Invalid choice. Please restart the script and choose 1 or 2.")


if __name__ == "__main__":
    main()
