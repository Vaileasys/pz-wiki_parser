import os
import shutil
import script_parser


def get_item(parsed_data):
    while True:
        item_id = input("Enter an item id\n>")
        for module, module_data in parsed_data.items():
            for item_type, item_data in module_data.items():
                if f"{module}.{item_type}" == item_id:
                    return item_data, item_id
        print(f"No item found for '{item_id}', please try again.")


def write_to_output(item_data, item_id, translate_names, language_code, output_dir='output/infoboxes'):
    #TODO: Translation
    # check output directory exists before writing
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{item_id}.txt')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("{{Infobox item")

        #All used infobox parameters and their matching keys
        parameters = {
            "name": item_data.get('DisplayName', ''),
            "model": f"{item_data.get('WeaponSprite', item_data.get('WorldStaticModel', item_data.get('StaticModel', '')))}_Model.png",
            "icon": f"{item_data.get('Icon', 'Question')}.png",
            "icon_name": item_data.get('DisplayName', ''),
            "category": item_data.get('DisplayCategory', ''),
            "weight": item_data.get('Weight', 1),
            "weight_reduction": item_data.get('WeightReduction', ''),
            "max_units": item_data.get('UseDelta', ''),
            "equipped": item_data.get('CanBeEquipped', ''),
            "attachment_type": item_data.get('AttachmentType', ''),
            "function": '',
            "weapon": item_data.get('MountOn', ''),
            "part_type": item_data.get('PartType', ''),
            "skill_type": item_data.get('Categories', item_data.get('SubCategory', '')),
            "ammo_type": item_data.get('AmmoType', ''),
            "clip_size": item_data.get('MaxAmmo', ''),
            "material": item_data.get('FabricType', ''),
            "material_value": item_data.get('MetalValue', ''),
            "can_boil_water": item_data.get('IsCookable', ''),
            "writable": item_data.get('CanBeWrite', ''),
            "recipes": item_data.get('TeachedRecipes') or item_data.get('SkillTrained', ''),
            "page_number": item_data.get('NumberOfPages') or item_data.get('PageToWrite', ''),
            "packaged": item_data.get('Packaged', ''),
            "rain_factor": item_data.get('RainFactor', ''),
            "days_fresh": item_data.get('DaysFresh', ''),
            "days_rotten": item_data.get('DaysTotallyRotten', ''),
            "cant_be_frozen": item_data.get('CantBeFrozen', ''),
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
            "kill_move": item_data.get('CloseKillMove', '').replace('_', ' ').lower().capitalize() if item_data.get(
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
            "alcoholic": item_data.get('Alcoholic', ''),
            "alcohol_power": item_data.get('AlcoholPower', ''),
            "reduce_infection_power": item_data.get('ReduceInfectionPower', ''),
            "bandage_power": item_data.get('BandagePower', ''),
            "poison_power": item_data.get('PoisonPower', ''),
            "cook_minutes": item_data.get('MinutesToCook', ''),
            "burn_minutes": item_data.get('MinutesToBurn', ''),
            "dangerous_uncooked": item_data.get('DangerousUncooked', ''),
            "bad_microwaved": item_data.get('BadInMicrowave', ''),
            "good_hot": item_data.get('GoodHot', ''),
            "bad_cold": item_data.get('BadCold', ''),
            "spice": item_data.get('Spice', ''),
            "evolved_recipe": item_data.get('EvolvedRecipeName', ''),
            "tag": '',
            "item_id": item_id,
            "infobox_version": "41.78.16"
        }

        for key, value in parameters.items():
            if value:
                file.write(f"\n|{key}={value}")

        file.write("\n}}")


def process_item(item_id, item_data, translate_names, language_code, output_dir):
    write_to_output(item_data, item_id, translate_names, language_code, output_dir)


def automatic_extraction(parsed_data, translate_names, language_code):
    output_dir = 'output/infoboxes'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for module, module_data in parsed_data.items():
        for item_type, item_data in module_data.items():
            item_id = f"{module}.{item_type}"
            process_item(item_id, item_data, translate_names, language_code, output_dir)


def main():
    parsed_data = script_parser.main()
    translate_names, language_code = script_parser.get_language()

    choice = input("Select extraction mode (1: automatic, 2: manual):\n> ")
    if choice == '1':
        automatic_extraction(parsed_data, translate_names, language_code)
        print("Extraction complete, the files can be found in output/infoboxes.")
    elif choice == '2':
        item_data, item_id = get_item(parsed_data)
        write_to_output(item_data, item_id, translate_names, language_code)
        print("Extraction complete, the file can be found in output/infoboxes.")
    else:
        print("Invalid choice. Please restart the script and choose 1 or 2.")


if __name__ == "__main__":
    main()
