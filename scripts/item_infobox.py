import os
import shutil
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core import translate, utility, logger, version, lua_helper
from scripts.lists import hotbar_slots
from scripts.core.constants import PBAR_FORMAT

# clothing vision penalties (percents)
clothing_penalties = {}

hotbar_slot_data = {}


def generate_clothing_penalties():
    """Extracts clothing penalties from 'forageSystem.lua' and stores in memory as 'clothing_penalties'."""
    global clothing_penalties
    lua_runtime = lua_helper.load_lua_file("forageSystem.lua", inject_lua=lua_helper.LUA_EVENTS)
    parsed_data = lua_helper.parse_lua_tables(lua_runtime, tables=["forageSystem.clothingPenalties"])
    clothing_penalties = parsed_data.get("forageSystem.clothingPenalties", {})
#    utility.save_cache(clothing_penalties, "clothingPenalties.json")

def get_item():
    while True:
        query_item_id = input("Enter an item id\n> ")
        for item_id, item_data in item_parser.get_item_data().items():
            if item_id == query_item_id:
                return item_data, item_id
        print(f"No item found for '{query_item_id}', please try again.")


def add_parameters_with_key(base_dict, key, items):
    if len(items) == 1:
        base_dict[key] = items[0]
    else:
        base_dict[key] = items[0]
        for index, item in enumerate(items[1:], start=2):
            base_dict[f'{key}{index}'] = item


# inserts new parameters into the parameters dictionary, after a defined parameter
def insert_parameters_after(parameters, new_parameters_dict):
    """
    Inserts new parameters into the parameters dictionary, after a defined parameter.

    Args:
        parameters (dict): the base parameters dictionary
        new_parameters_dict (dict): a dictionary with the new parameters to add.
            The keys of this dictionary are the parameter names to insert after.
            The values are dictionaries with the new parameters to add.
            The keys of these dictionaries are the parameter names, and the values
            can be either a single value, or a list of values.

    Returns:
        dict: a new parameters dictionary with the new parameters inserted
    """
    combined_parameters = {}
    insertion_points = {key: False for key in new_parameters_dict.keys()}

    # insert new parameters after the specified keys
    for key, value in parameters.items():
        combined_parameters[key] = value
        
        if key in new_parameters_dict:
            insertion_points[key] = True
            new_params = new_parameters_dict[key]
            for new_key, new_value in new_params.items():
                if isinstance(new_value, list):
                    add_parameters_with_key(combined_parameters, new_key, new_value)
                else:
                    combined_parameters[new_key] = new_value
    
    # add new parameters at the end if insertion point wasn't found
    for insert_after_key, was_inserted in insertion_points.items():
        if not was_inserted:
            new_params = new_parameters_dict[insert_after_key]
            for new_key, new_value in new_params.items():
                if isinstance(new_value, list):
                    add_parameters_with_key(combined_parameters, new_key, new_value)
                else:
                    combined_parameters[new_key] = new_value

    return combined_parameters


def write_to_output(item_data, item_id, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{item_id}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("{{Infobox item")

            name = utility.get_name(item_id, item_data)

            icons = utility.find_icon(item_id, True)

            model = utility.get_model(item_data)

            category = 'DisplayCategory'
            category = translate.get_translation(item_data.get(category, 'Item'), category)

            fluid_capacity_ml = float(item_data.get('capacity', 0)) * 1000
            fluid_capacity = ''
            if fluid_capacity_ml != 0.0:
                fluid_capacity = f"{str(int(fluid_capacity_ml))}"

            attachment_type = item_data.get("AttachmentType"),
            hotbar_attachments = []
            if attachment_type:
                for attachment in attachment_type:
                    for slot, slot_data in hotbar_slot_data.items():
                        slot_attachments = slot_data.get("attachments", {})
                        if attachment in slot_attachments:
                            slot_name = slot_data.get("name")
                            slot_link = f"[[AttachmentsProvided#{slot}|{slot_name}]]"
                            hotbar_attachments.append(slot_link)
                attachment_type = "<br>".join(hotbar_attachments)
            else:
                attachment_type = ''
            
            attachments_provided = item_data.get('AttachmentsProvided')
            if attachments_provided:
                if isinstance(attachments_provided, str):
                    attachments_provided = [attachments_provided]
                hotbar_attachments = []

                for slot in attachments_provided:
                    slot_name = hotbar_slot_data[slot].get("name")
                    slot_link = f"[[AttachmentsProvided#{slot}|{slot_name}]]"
                    hotbar_attachments.append(slot_link)
                attachments_provided = "<br>".join(hotbar_attachments)
            else:
                attachments_provided = ''

            material = item_data.get('FabricType', '')
            material_value = item_data.get('MetalValue', '')
            if not material and material_value:
                material = 'metal'
            material = material.capitalize()
            
            recipes = item_data.get('TeachedRecipes', '')
            if recipes != '':
                if isinstance(recipes, str):
                    recipes = [recipes]
                for i in range(len(recipes)):
                    recipes[i] = recipes[i].replace(" ", "_")
                    recipes[i] = translate.get_translation(recipes[i], 'TeachedRecipes')
                recipes = utility.format_br(recipes)

            # (Attachments) Get weapons that it's used for.
            weapon = ''
            weapons = item_data.get('MountOn')
            if weapons:
                if isinstance(weapons, str):
                    weapons = [weapons]
                weapon_list = []
                for weapon_id in weapons:
                    weapon_icon = utility.get_icon(weapon_id, True, True, False)
                    weapon_list.append(weapon_icon)
                weapon = ''.join(weapon_list)

            burn_time = utility.get_burn_time(item_id, item_data)
            
            foraging = ''
            body_location = item_data.get('BodyLocation', '')
            if body_location in clothing_penalties:
                foraging = f"-{clothing_penalties[body_location]}%"

            evolved_recipe = item_data.get('EvolvedRecipeName', '')
            if evolved_recipe:
                evolved_recipe_translated = translate.get_translation(item_id, 'EvolvedRecipeName')
                if evolved_recipe_translated:
                    evolved_recipe = evolved_recipe_translated
            
            tags = utility.get_tags(item_data)
            
            guid = utility.get_guid(item_data)
            
            parameters = {
                "name": name,
                # "model": (added with 'insert_parameters_after')
                # "icon":  (added with 'insert_parameters_after')
                "icon_name": name,
                "category": category,
                "weight": item_data.get('Weight', 1),
                "capacity": item_data.get('Capacity', ''),
                "container_name": translate.get_translation(item_data.get('ContainerName', ''), 'ContainerName'),
                "weight_reduction": item_data.get('WeightReduction', ''),
                "max_units": item_data.get('UseDelta', ''),
                "fluid_capacity": fluid_capacity,
                "equipped": item_data.get('CanBeEquipped', ''),
                "body_location": item_data.get('BodyLocation', ''),
                "attachment_type": attachment_type,
                "attachments_provided": attachments_provided,
                "function": '',
                "weapon": weapon,
                "part_type": translate.get_translation(item_data.get('PartType', ''), 'PartType'),
                "skill_type": utility.get_skill_type_mapping(item_data, item_id),
                "ammo_type": utility.get_icon(item_data.get('AmmoType', ''), True, True, False),
                "clip_size": item_data.get('MaxAmmo', ''),
                "material": material,
                "material_value": material_value,
                "can_boil_water": item_data.get('CanBoilWater', '').capitalize(),
                "writable": item_data.get('CanBeWrite', '').capitalize(),
                "recipes": recipes,
                "skill_trained": translate.get_translation(item_data.get('SkillTrained', ''), 'SkillTrained'),
                "foraging_change": foraging,
                "page_number": item_data.get('NumberOfPages') or item_data.get('PageToWrite', ''),
                "packaged": item_data.get('Packaged', '').capitalize(),
                "rain_factor": item_data.get('RainFactor', ''),
                "days_fresh": item_data.get('DaysFresh', ''),
                "days_rotten": item_data.get('DaysTotallyRotten', ''),
                "cant_be_frozen": item_data.get('CantBeFrozen', '').capitalize(),
                "feed_type": item_data.get('AnimalFeedType', ''),
                "condition_max": item_data.get('ConditionMax', ''),
                "condition_lower_chance": item_data.get('ConditionLowerChanceOneIn', ''),
                "run_speed": item_data.get('RunSpeedModifier', ''),
                "stomp_power": item_data.get('StompPower', ''),
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
                "burn_time": burn_time,
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
                "sharpness": item_data.get('Sharpness', ''),
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
                "evolved_recipe": evolved_recipe,
                # "tag": (added with 'insert_parameters_after')
                "guid": guid,
                "clothing_item": item_data.get('ClothingItem', ''),
                "item_id": item_id,
                "infobox_version": version.get_version()
            }

            # new parameters to be added and parameter keys go here
            icon_model_parameters = {'model': model, 'icon': icons}
            tag_parameters = {'tag': tags}

            # These parameters will be added afterwards. For parameters that need to be defined, e.g. icon2, icon3, etc.
            # 'after_param': param_key,
            new_parameters_dict = {
                'name': icon_model_parameters,
                'evolved_recipe': tag_parameters
            }

            parameters = insert_parameters_after(parameters, new_parameters_dict)

            for key, value in parameters.items():
                if value:
                    file.write(f"\n|{key}={value}")

            file.write("\n}}")
    except Exception as e:
        logger.write(f"Error writing file {item_id}.txt: {e}", True)


def process_item(item_data, item_id, output_dir):
    write_to_output(item_data, item_id, output_dir)


def automatic_extraction(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    parsed_item_data = item_parser.get_item_data()
    with tqdm(total=len(parsed_item_data), desc="Processing items", unit=" items", bar_format=PBAR_FORMAT, unit_scale=True) as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f'Processing: {item_data.get("Type", "Unknown")} ({item_id[:30]})')
            process_item(item_data, item_id, output_dir)
            pbar.update(1)
        pbar.bar_format = f"Finished processing items."


def main():
    global hotbar_slot_data
    language_code = translate.get_language_code()
    generate_clothing_penalties()
    output_dir = f'output/{language_code}/infoboxes'

    hotbar_slot_data = hotbar_slots.get_hotbar_slots()

    while True:
        choice = input("1: Automatic\n2: Manual\nQ: Quit\n> ").strip().lower()
        if choice == '1':
            automatic_extraction(output_dir)
            print(f"Extraction complete, the files can be found in {output_dir}.")
            return
        elif choice == '2':
            item_data, item_id = get_item()
            write_to_output(item_data, item_id, output_dir)
            print(f"Extraction complete, the file can be found in {output_dir}.")
            return
        elif choice == 'q':
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
