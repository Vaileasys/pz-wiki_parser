import os
import shutil
import json
import re
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core import logger
from scripts.core.version import Version
from scripts.core.language import Language, Translate
from scripts.lists import hotbar_slots
from scripts.core.constants import PBAR_FORMAT, RESOURCE_PATH
from scripts.utils import utility, lua_helper, util
from scripts.utils.util import capitalize


language_code = ""
lcs = ""
# Clothing vision penalties (percents)
clothing_penalties = {}
hotbar_slot_data = {}
# Descriptors for item IDs
all_descriptors = {}
processed_item_ids = []
item_ids_already_processed = []


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


def get_item_ids(item_id):
    item_id_data = utility.get_item_id_data(True)
    
    all_item_ids = []

    for key, values in item_id_data.items():
        if item_id in values and item_id not in all_item_ids:
            all_item_ids.extend(values)

    if not all_item_ids:
        return [item_id]

    return all_item_ids


def get_descriptor(item_ids: list):
    global all_descriptors
    if not item_ids:
        return []
    
    if not all_descriptors:
        with open(f"{RESOURCE_PATH}\\item_descriptors.json", "r") as file:
            all_descriptors = json.load(file)
    
    descriptors = []
    for item in item_ids:
        descriptor = None
        item = item.split(".")[1] if len(item.split(".")) > 1 else item

        for key, value in all_descriptors.items():
            position = value["position"]
            name = value["name"]

            if position == "start" and item.startswith(key):
                descriptor = name
                break
            elif position == "end" and item.endswith(key):
                descriptor = name
                break
            elif position == "both" and key in item:
                descriptor = name
                break

        descriptors.append(descriptor)
    
    return descriptors


def enumerate_params(parameters):
    new_parameters = {}
    for key, value in parameters.items():
        # Remove key-value pairs if they have no value
        if not value:
            continue
        if isinstance(value, list):
            new_parameters[key] = value[0]
            for i, v in enumerate(value[1:], start=2):
                new_parameters[f"{key}{i}"] = v
        else:
            new_parameters[key] = value
    return new_parameters


def remove_descriptor(value: str) -> str:
    """Removes the descriptor from the end of string."""
    if value is None:
        return None
    return re.sub(r'\s*<small>\(.*?\)</small>$', '', value).strip()


def get_any_property(items: dict, script_param: bool|str|int|float|list, default=None) -> str:
    """
    Gets the first property value that isn't None and returns it.
    
    Used for items with multiple variants.
    """
    #TODO: check for differences instead of only getting one. This may need to wait until template rewrite with LUA.
    for item_id, item_data in items.items():
        script_value = item_data.get(script_param)
        if script_value is not None:
            break
        else:
            continue
    
    if script_value is None:
        script_value = default

    return script_value


def get_param_values(items: dict, script_param: str, rstring:bool = False, default:str = None) -> list|str:
    """
    Gets the script parameter values for a list of items.

    :param items: dict - A dictionary where keys are item IDs and values are item data dictionaries.
    :param script_param: str - The key for the script parameter to retrieve values from each item.
    :param rstring: bool, optional - If True, returns a string with values joined by "<br>", otherwise returns a list. Default is False.
    :param default: str, optional - The default value to use if the script parameter is not found in an item. Default is None.
    :return: list or str - A list of unique parameter values or a string if rstring is True.
    """
    values = []
    for item_id, item_data in items.items():
        script_value = item_data.get(script_param, default)
        if script_value is not None and script_value not in values:
            descriptor = item_data.get("DescriptorFormatted")

            new_value = str(script_value) + descriptor

            if new_value is not None and new_value not in values:
                values.append(new_value)

    if rstring:
        return "<br>".join(values)
    
    return values


def generate_infobox(item_id, item_data):
    global processed_item_ids
    try:
        if item_id in processed_item_ids:
            global item_ids_already_processed
            item_ids_already_processed.append(item_id)
            return None

        # Get all items their data and store as 'all_items'
        all_item_ids = get_item_ids(item_id)
        all_items = {}
        if len(all_item_ids) > 1:
            descriptors = get_descriptor(all_item_ids)
            for i, id in enumerate(all_item_ids):
                id_data = utility.get_item_data_from_id(id)
                if not id_data:
                    logger.write(f"Missing item_id for '{id}' when getting item data from item id.")
                    continue
                descriptor = descriptors[i]
                if descriptor is not None:
                    descriptor_formatted = f" <small>({descriptor})</small>"
                else:
                    descriptor_formatted = ""
                    descriptor = ""
                id_data["Descriptor"] = descriptor
                id_data["DescriptorFormatted"] = descriptor_formatted
                all_items[id] = id_data

        else:
            all_items[item_id] = item_data
            all_items[item_id]["Descriptor"] = ""
            all_items[item_id]["DescriptorFormatted"] = ""
        
        # Update the item_id and item_data to be the primary item's
        item_id = list(all_items.keys())[0]
        item_data = list(all_items.values())[0]

        # Add item ids to the processed list, so we don't create infoboxes unecessarily
        processed_item_ids.extend(all_item_ids)

        name = utility.get_name(item_id, item_data)

        icons = utility.find_icon(item_id, True)

        model = utility.get_model(item_data)

        fluid_capacity_ml = float(get_any_property(all_items, 'capacity', 0)) * 1000
        fluid_capacity = None
        if fluid_capacity_ml != 0.0:
            fluid_capacity = f"{str(int(fluid_capacity_ml))}"

        attachment_type = get_any_property(all_items, "AttachmentType"),
        hotbar_attachments = []
        if attachment_type is not None:
            for attachment in attachment_type:
                for slot, slot_data in hotbar_slot_data.items():
                    slot_attachments = slot_data.get("attachments", {})
                    if attachment in slot_attachments:
                        slot_name = slot_data.get("name")
                        slot_link = f"[[AttachmentsProvided#{slot}|{slot_name}]]"
                        hotbar_attachments.append(slot_link)
            attachment_type = "<br>".join(hotbar_attachments) if hotbar_attachments else None
        else:
            attachment_type = None
        
        attachments_provided = get_any_property(all_items, 'AttachmentsProvided')
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
            attachments_provided = None

        material = get_any_property(all_items, 'FabricType')
        material_value = get_any_property(all_items, 'MetalValue')
        if not material and material_value:
            material = 'metal'
        material = capitalize(material)
        
        recipes = get_any_property(all_items, 'TeachedRecipes')
        if recipes is not None:
            if isinstance(recipes, str):
                recipes = [recipes]
            for i in range(len(recipes)):
                recipes[i] = recipes[i].replace(" ", "_")
                recipes[i] = Translate.get(recipes[i], 'TeachedRecipes')
            recipes = "<br>".join(recipes)

        # (Attachments) Get weapons that it's used for.
        weapon = None
        weapons = get_any_property(all_items, 'MountOn')
        if weapons:
            if isinstance(weapons, str):
                weapons = [weapons]
            weapon_list = []
            for weapon_id in weapons:
                weapon_icon = utility.get_icon(weapon_id, True, True, False)
                weapon_list.append(weapon_icon)
            weapon = ''.join(weapon_list)
        
        endurance_mod = util.format_positive(float(item_data.get('EnduranceMod', 1)) - 1)
        endurance_mod = None if endurance_mod == "0" else endurance_mod

        burn_time = utility.get_burn_time(item_id, item_data)
        
        # TODO: fix/finish
        category = []
        foraging = []
        body_location = []
        guid = []

        for id, id_data in all_items.items():
            descriptor = id_data.get("DescriptorFormatted")
            display_category = 'DisplayCategory'
            display_category = Translate.get(id_data.get(display_category, 'Item'), display_category)
            display_category = display_category + descriptor
            if not any(x in category for x in (display_category, remove_descriptor(display_category))):
                category.append(display_category)

            bl = id_data.get('BodyLocation', item_data.get('CanBeEquipped'))
            if bl is not None:
                bl = f"[[BodyLocation{lcs}#{bl}|{bl}]]"
                if not any(x in body_location for x in (bl, remove_descriptor(bl))):
                    body_location.append(bl + descriptor)
                if bl in clothing_penalties:
                    id_clothing_penalty = f"-{clothing_penalties[bl]}%"
                    if id_clothing_penalty not in foraging:
                        foraging.append(id_clothing_penalty + descriptor)

            id_guid = utility.get_guid(id_data)
            if id_guid is not None and id_guid not in guid:
                guid.append(id_guid)

        category = "<br>".join(category) if category else None
        foraging = "<br>".join(foraging) if foraging else None

        equipped = get_any_property(all_items, 'CanBeEquipped') if not body_location else None

        evolved_recipe = get_any_property(all_items, 'EvolvedRecipeName')
        if evolved_recipe:
            evolved_recipe_translated = Translate.get(item_id, 'EvolvedRecipeName')
            if evolved_recipe_translated:
                evolved_recipe = evolved_recipe_translated
        
        tags = item_data.get("Tags")
        
        parameters = {
            "name": name,
            "model": model,
            "icon":  icons,
            "icon_name": name,
            "category": category,
            "weight": get_param_values(all_items, 'Weight', True, default=1),
            "capacity": get_any_property(all_items, 'Capacity'),
            "container_name": Translate.get(get_any_property(all_items, 'ContainerName'), 'ContainerName'),
            "weight_reduction": get_any_property(all_items, 'WeightReduction'),
            "max_units": get_any_property(all_items, 'UseDelta'),
            "fluid_capacity": fluid_capacity,
            "equipped": equipped,
            "body_location": body_location,
            "attachment_type": attachment_type,
            "attachments_provided": attachments_provided,
            "function": None,
            "weapon": weapon,
            "part_type": Translate.get(get_any_property(all_items, 'PartType'), 'PartType'),
            "skill_type": utility.get_skill_type_mapping(item_data, item_id),
            "ammo_type": utility.get_icon(get_any_property(all_items, 'AmmoType'), True, True, False),
            "clip_size": get_any_property(all_items, 'MaxAmmo', None),
            "material": material,
            "material_value": material_value,
            "can_boil_water": capitalize(get_any_property(all_items, 'CanBoilWater')),
            "writable": capitalize(get_any_property(all_items, 'CanBeWrite')),
            "recipes": recipes,
            "skill_trained": Translate.get(get_any_property(all_items, 'SkillTrained'), 'SkillTrained'),
            "foraging_change": foraging,
            "page_number": get_any_property(all_items, 'NumberOfPages') or get_any_property(all_items, 'PageToWrite'),
            "packaged": capitalize(get_any_property(all_items, 'Packaged')),
            "rain_factor": get_any_property(all_items, 'RainFactor'),
            "days_fresh": get_any_property(all_items, 'DaysFresh'),
            "days_rotten": get_any_property(all_items, 'DaysTotallyRotten'),
            "cant_be_frozen": capitalize(get_any_property(all_items, 'CantBeFrozen')),
            "feed_type": get_any_property(all_items, 'AnimalFeedType'),
            "condition_max": get_any_property(all_items, 'ConditionMax'),
            "condition_lower_chance": get_any_property(all_items, 'ConditionLowerChanceOneIn'),
            "run_speed": get_any_property(all_items, 'RunSpeedModifier'),
            "stomp_power": get_any_property(all_items, 'StompPower'),
            "combat_speed": get_any_property(all_items, 'CombatSpeedModifier'),
            "scratch_defense": get_any_property(all_items, 'ScratchDefense'),
            "bite_defense": get_any_property(all_items, 'BiteDefense'),
            "bullet_defense": get_any_property(all_items, 'BulletDefense'),
            "neck_protection": get_any_property(all_items, 'NeckProtectionModifier'),
            "insulation": get_any_property(all_items, 'Insulation'),
            "wind_resistance": get_any_property(all_items, 'WindResistance'),
            "water_resistance": get_any_property(all_items, 'WaterResistance'),
            "discomfort_mod": get_any_property(all_items, 'DiscomfortModifier'),
            "endurance_mod": endurance_mod,
            "light_distance": get_any_property(all_items, 'LightDistance'),
            "light_strength": get_any_property(all_items, 'LightStrength'),
            "torch_cone": get_any_property(all_items, 'TorchCone'),
            "wet_cooldown": get_any_property(all_items, 'WetCooldown'),
            "burn_time": burn_time,
            "sensor_range": get_any_property(all_items, 'SensorRange') or get_any_property(all_items, 'RemoteRange'),
            "two_way": get_any_property(all_items, 'TwoWay'),
            "mic_range": get_any_property(all_items, 'MicRange'),
            "transmit_range": get_any_property(all_items, 'TransmitRange'),
            "min_channel": get_any_property(all_items, 'MinChannel'),
            "max_channel": get_any_property(all_items, 'MaxChannel'),
            "damage_type": None,
            "min_damage": get_any_property(all_items, 'MinDamage'),
            "max_damage": get_any_property(all_items, 'MaxDamage'),
            "door_damage": get_any_property(all_items, 'DoorDamage'),
            "tree_damage": get_any_property(all_items, 'TreeDamage'),
            "sharpness": get_any_property(all_items, 'Sharpness'),
            "min_range": get_any_property(all_items, 'MinRange'),
            "max_range": get_any_property(all_items, 'MaxRange'),
            "min_range_mod": get_any_property(all_items, 'MinRangeModifier'),
            "max_range_mod": get_any_property(all_items, 'MaxRangeModifier'),
            "recoil_delay": get_any_property(all_items, 'RecoilDelay') or get_any_property(all_items, 'RecoilDelayModifier'),
            "sound_radius": get_any_property(all_items, 'SoundRadius'),
            "base_speed": get_any_property(all_items, 'BaseSpeed'),
            "push_back": get_any_property(all_items, 'PushBackMod'),
            "aiming_time": get_any_property(all_items, 'AimingTime'),
            "reload_time": get_any_property(all_items, 'ReloadTime'),
            "crit_chance": get_any_property(all_items, 'CriticalChance'),
            "crit_multiplier": get_any_property(all_items, 'CritDmgMultiplier'),
            "angle_mod": get_any_property(all_items, 'AngleModifier'),
            "kill_move": capitalize(get_any_property(all_items, 'CloseKillMove').replace('_', ' ')) if get_any_property(all_items, 'CloseKillMove') else None,
            "weight_mod": get_any_property(all_items, 'WeightModifier'),
            "effect_power": get_any_property(all_items, 'ExplosionPower') or get_any_property(all_items, 'FirePower'),
            "effect_range": get_any_property(all_items, 'ExplosionRange') or get_any_property(all_items, 'FireRange') or get_any_property(all_items, 'SmokeRange') or get_any_property(all_items, 'NoiseRange'),
            "effect_duration": get_any_property(all_items, 'NoiseDuration'),
            "effect_timer": get_any_property(all_items, 'ExplosionTimer'),
            "hunger_change": get_any_property(all_items, 'HungerChange'),
            "thirst_change": get_any_property(all_items, 'ThirstChange'),
            "calories": get_any_property(all_items, 'Calories'),
            "carbohydrates": get_any_property(all_items, 'Carbohydrates'),
            "proteins": get_any_property(all_items, 'Proteins'),
            "lipids": get_any_property(all_items, 'Lipids'),
            "unhappy_change": get_any_property(all_items, 'UnhappyChange'),
            "boredom_change": get_any_property(all_items, 'BoredomChange'),
            "stress_change": get_any_property(all_items, 'StressChange'),
            "fatigue_change": get_any_property(all_items, 'FatigueChange'),
            "endurance_change": get_any_property(all_items, 'EnduranceChange'),
            "flu_change": get_any_property(all_items, 'FluReduction'),
            "pain_change": get_any_property(all_items, 'PainReduction'),
            "sick_change": get_any_property(all_items, 'ReduceFoodSickness'),
            "alcoholic": capitalize(get_param_values(all_items, 'Alcoholic', True)),
            "alcohol_power": get_any_property(all_items, 'AlcoholPower'),
            "reduce_infection_power": get_any_property(all_items, 'ReduceInfectionPower'),
            "bandage_power": get_param_values(all_items, 'BandagePower', True),
            "poison_power": get_any_property(all_items, 'PoisonPower'),
            "cook_minutes": get_any_property(all_items, 'MinutesToCook'),
            "burn_minutes": get_any_property(all_items, 'MinutesToBurn'),
            "dangerous_uncooked": capitalize(get_any_property(all_items, 'DangerousUncooked')),
            "bad_microwaved": capitalize(get_any_property(all_items, 'BadInMicrowave')),
            "good_hot": capitalize(get_any_property(all_items, 'GoodHot')),
            "bad_cold": capitalize(get_any_property(all_items, 'BadCold')),
            "spice": capitalize(get_any_property(all_items, 'Spice')),
            "evolved_recipe": evolved_recipe,
            "tag": tags,
            "guid": guid,
            "clothing_item": get_param_values(all_items, 'ClothingItem'),
            "item_id": all_item_ids,
        }

        parameters = enumerate_params(parameters)
        parameters["infobox_version"] = Version.get()

        return parameters
    except Exception as e:
        logger.write(f"Error generating data for {item_id}", True, exception=e)


def write_to_output(parameters, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    item_id = parameters.get("item_id")
    output_file = os.path.join(output_dir, f'{item_id}.txt')
    content = []
    content.append("{{Infobox item")

    for key, value in parameters.items():
        content.append(f"|{key}={value}")
    
    content.append("}}")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(content))


def process_item(item_data, item_id, output_dir):
    parameters = generate_infobox(item_id, item_data)
    if parameters is not None:
        write_to_output(parameters, output_dir)


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
        elapsed_time = pbar.format_dict["elapsed"]
        pbar.bar_format = f"Finished processing items after {elapsed_time:.2f} seconds."


def main():
    global hotbar_slot_data
    global language_code
    global lcs
    language_code = Language.get()
    if language_code != "en":
        lcs = f"/{language_code}"
    generate_clothing_penalties()
    output_dir = f'output\\{language_code}\\infoboxes'

    hotbar_slot_data = hotbar_slots.get_hotbar_slots()

    while True:
        choice = input("1: Automatic\n2: Manual\nQ: Quit\n> ").strip().lower()
        if choice == '1':
            automatic_extraction(output_dir)
            utility.save_cache({"data": item_ids_already_processed}, "item_ids_already_processed.json")
            print(f"Extraction complete, the files can be found in '{output_dir}'.")
            return
        elif choice == '2':
            item_data, item_id = get_item()
            parameters = generate_infobox(item_id, item_data)
            if parameters is not None:
                write_to_output(parameters, output_dir)
                output_path = os.path.join(output_dir, item_id + ".txt")
                print(f"Extraction complete, the file can be found in '{output_path}'.")
            else:
                print(f"Error writing file. Refer to log: {logger.get_log_path()}")
            return
        elif choice == 'q':
            return
        else:
            print("Invalid choice.")
    


if __name__ == "__main__":
    main()
