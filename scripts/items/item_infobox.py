"""
Item infobox generator.

This module processes `Item` objects into structured infobox parameters, formatted for wiki output.
It handles individual items, pages with multiple item IDs, and supports both combined and standalone infobox generation.

Main functions:
- Extract item attributes into infobox fields
- Merge multiple item definitions into unified infobox data, based on page
- Format and output infobox content as text files
"""

import os
import re
from tqdm import tqdm
from scripts.core import logger
from scripts.core.version import Version
from scripts.utils import echo, color, util
from scripts.objects.item import Item
from scripts.objects.skill import Skill
from scripts.objects.craft_recipe import CraftRecipe
from scripts.objects.attachment import AttachmentType, HotbarSlot
from scripts.objects.recorded_media import RecMedia
from scripts.core import page_manager
from scripts.core.file_loading import write_file, clear_dir
from scripts.core.constants import ITEM_DIR, PBAR_FORMAT, RESOURCE_DIR

ROOT_PATH = os.path.join(ITEM_DIR, "infoboxes")

processed_items = []
multi_id_page_dict = {} # Item ids that share a page: {'item_id': 'page'}
pages_dict: dict = {} # Unprocessed item page dict from the raw page dict
all_descriptors = None

numbered_params = ["model", "icon", "icon_name", "weight", "body_location", "weapon", "tag", "guid", "item_id"]


def generate_item_data(item: Item):
    """
    Extracts relevant parameters from an Item object into a dictionary.

    Args:
        item (Item): The item object to process.

    Returns:
        dict: Dictionary of infobox parameters for the given item.
    """
    param = {}
    #-------------- GENERAL --------------#
    param["name"] = re.sub(r'\([^()]*\)', lambda m: f'<br><span style="font-size: 88%;">{m.group(0)}</span>', item.name)
    param["model"] = item.models
    param["icon"] = item.icons
    param["icon_name"] = [item.name for _ in item.icons]
    param["category"] = item.display_category
    param["weight"] = item.weight
    param["capacity"] = item.capacity
    param["container_name"] = item.fluid_container.container_name if item.fluid_container else None
    param["vehicle_type"] = item.vehicle_type_name if item.get("VehicleType") else None
    param["vehicle_part"] = "<br>".join(set(part.common_link for part in item.vehicle_part_types)) if item.vehicle_part_types else None

    #-------------- PROPERTIES --------------#
    param["weight_reduction"] = item.weight_reduction
    param["max_units"] = item.use_delta if item.get("UseDelta") or item.type == "Drainable" else None
    param["fluid_capacity"] = util.convert_unit(item.fluid_container.capacity, unit="L") if item.fluid_container else None
    param["equipped"] = (
        "Two-handed" if item.type == "Weapon" and item.two_hand_weapon
        else "One-handed" if item.type == "Weapon"
        else param.get("equipped")
    )
    param["body_location"] = item.body_location.wiki_link if item.body_location else item.can_be_equipped.wiki_link if item.can_be_equipped else None
    param["attachment_type"] = "<br>".join([HotbarSlot(slot).wiki_link for slot in AttachmentType(item.attachment_type).slots]) if item.attachment_type else None
    param["attachments_provided"] = "<br>".join([HotbarSlot(a).wiki_link for a in item.attachments_provided]) if item.attachments_provided else None
    # Unused
    #param["function"] = None
    param["weapon"] = [f"{weapon.icon} {weapon.wiki_link}" for weapon in item.weapons] if item.weapons else None
    param["part_type"] = "Magazine" if item.has_tag("PistolMagazine", "RifleMagazine") else item.part_type
    param["skill_type"] = item.skill.wiki_link if item.skill else None
    param["ammo_type"] = f"{Item(item.ammo_type).icon} {Item(item.ammo_type).wiki_link}" if item.ammo_type else None
    param["clip_size"] = item.max_ammo if (item.has_tag("PistolMagazine", "RifleMagazine") or item.type == "Weapon") else item.clip_size
    param["material"] = "Metal" if not item.material and item.metal_value > 0 else item.material
    param["can_boil_water"] = item.has_tag("Cookable") or item.has_tag("CookableMicrowave")
    param["writable"] = item.can_be_write
    param["recipes"] = "<br>".join([CraftRecipe(rec).wiki_link for rec in item.teached_recipes]) if len(item.teached_recipes) < 5 else "''See [[#Learned recipes|Learned recipes]]''"
    # Unused
    #param["researchable_recipes"] = [CraftRecipe(rec).wiki_link for rec in item.researchable_recipes] if item.researchable_recipes else None
    param["skill_trained"] = item.skill_trained.wiki_link if item.skill_trained else None
    param["foraging_change"] = f"-{util.convert_int(item.foraging_penalty)}%" if item.foraging_penalty else None
    param["page_number"] = (item.page_to_write or item.number_of_pages) if (item.page_to_write or item.number_of_pages) > 0 else None
    param["packaged"] = item.packaged
    param["rain_factor"] = item.fluid_container.rain_factor if item.fluid_container else None
    param["days_fresh"] = f'{item.days_fresh} {get_translation("day" if item.days_fresh == 1 else "days")}' if item.get("DaysFresh") else None
    param["days_rotten"] = f'{item.days_totally_rotten} {get_translation("day" if item.days_totally_rotten == 1 else "days")}' if item.get("DaysTotallyRotten") else None
    param["cant_be_frozen"] = item.cant_be_frozen if item.get("DaysFresh") else None
    param["feed_type"] = item.animal_feed_type
    param["condition_max"] = item.get("ConditionMax")
    param["condition_lower_chance"] = item.get("ConditionLowerChanceOneIn")
    param["run_speed"] = item.get("RunSpeedModifier")
    param["stomp_power"] = item.stomp_power if (item.body_location.location_id == "Shoes" if item.body_location else False) else None
    param["combat_speed"] = util.convert_percentage(item.combat_speed_modifier) if item.combat_speed_modifier != 1.0 else None
    param["scratch_defense"] = item.scratch_defense if item.scratch_defense else None
    param["bite_defense"] = item.bite_defense if item.bite_defense else None
    param["bullet_defense"] = item.bullet_defense
    param["neck_protection"] = util.convert_percentage(item.neck_protection_modifier, True) if ("Neck" in item.body_parts or item.neck_protection_modifier < 1.0) else None
    param["insulation"] = item.insulation
    param["wind_resistance"] = item.wind_resistance
    param["water_resistance"] = item.water_resistance
    param["discomfort_mod"] = item.discomfort_modifier
    param["endurance_mod"] = util.format_positive(item.endurance_mod - 1.0) if item.get("EnduranceMod") else None
    param["light_distance"] = item.light_distance
    param["light_strength"] = item.light_strength
    param["torch_cone"] = item.torch_cone
    param["wet_cooldown"] = item.wet_cooldown
    param["burn_time"] = item.burn_time
    param["sensor_range"] = item.sensor_range
    param["two_way"] = item.two_way
    param["mic_range"] = item.mic_range
    param["transmit_range"] = item.transmit_range
    param["min_channel"] = util.convert_unit(item.min_channel, "Hz", "k", "M") if item.type == "Radio" else None
    param["max_channel"] = util.convert_unit(item.max_channel, "Hz", "k", "M") if item.type == "Radio" else None
    param["max_capacity"] = item.get("MaxCapacity")
    param["brake_force"] = item.brake_force
    param["engine_loudness"] = item.engine_loudness
    param["degradation_standard"] = item.condition_lower_standard
    param["degradation_offroad"] = item.condition_lower_offroad
    param["suspension_damping"] = item.suspension_damping
    param["suspension_compression"] = item.suspension_compression
    param["wheel_friction"] = item.wheel_friction
    param["chance_damaged"] = item.chance_to_spawn_damaged
    param["mechanics_tool"] = "<br>".join(item.vehicle_part.install.formatted_items) if item.vehicle_part else None
    if item.vehicle_part:
        skills = []
        for skill_id, level in item.vehicle_part.install.skills.items():
            skills.append(f"{Skill(skill_id).wiki_link} {level}")
        param["recommended_level"] = "<br>".join(skills)
    param["required_recipe"] = (item.vehicle_part.install.recipes 
                                if item.vehicle_part 
                                else None)

    #-------------- PERFORMANCE --------------#
    # Unused
    #param["damage_type"] = None
    param["min_damage"] = item.min_damage if item.type == "Weapon" else None
    param["max_damage"] = item.max_damage if item.type == "Weapon" else None
    param["door_damage"] = item.door_damage if item.type == "Weapon" else None
    param["tree_damage"] = item.tree_damage if item.type == "Weapon" else None
    param["sharpness"] = item.sharpness
    param["min_range"] = item.min_range if item.type == "Weapon" else None
    param["max_range"] = item.max_range if item.type == "Weapon" else None
    param["min_range_mod"] = item.min_sight_range if item.type == "Weapon" else None
    param["max_range_mod"] = item.max_sight_range if item.type == "Weapon" else None
    param["recoil_delay"] = item.recoil_delay or item.recoil_delay_modifier
    param["sound_radius"] = item.sound_radius
    param["base_speed"] = item.base_speed if item.type == "Weapon" and not item.has_tag("Firearm") else None
    param["push_back"] = item.push_back_mod if item.type == "Weapon" else None
    param["knockdown"] = item.knockdown_mod if item.type == "Weapon" else None
    param["aiming_time"] = item.aiming_time or item.aiming_time_modifier
    param["reload_time"] = item.reload_time or item.aiming_time_modifier
    param["crit_chance"] = item.critical_chance if item.type == "Weapon" else None
    param["crit_multiplier"] = util.check_zero(item.crit_dmg_multiplier)
    # Unused
    #param["angle_mod"] = item.projectile_spread_modifier  # 'AngleModifier' removed in b42
    param["kill_move"] = item.close_kill_move.replace('_', ' ') if isinstance(item.close_kill_move, str) else item.close_kill_move
    param["weight_mod"] = item.weight_modifier
    param["effect_power"] = item.explosion_power or item.fire_power
    param["effect_range"] = item.explosion_range or item.fire_range or item.smoke_range or item.noise_range
    param["effect_duration"] = item.noise_duration
    param["effect_timer"] = item.explosion_timer

    #-------------- NUTRITION --------------#
    param["hunger_change"] = util.check_zero(item.hunger_change)
    param["thirst_change"] = util.check_zero(item.thirst_change)
    param["calories"] = str(item.get("Calories")) if item.get("Calories") is not None else None
    param["carbohydrates"] = str(item.get("Carbohydrates")) if item.get("Carbohydrates") is not None else None
    param["proteins"] = str(item.get("Proteins")) if item.get("Proteins") is not None else None
    param["lipids"] = str(item.get("Lipids")) if item.get("Lipids") is not None else None

    #-------------- EFFECT --------------#
    param["unhappy_change"] = util.check_zero(item.unhappy_change)
    param["boredom_change"] = util.check_zero(item.boredom_change)
    param["stress_change"] = util.check_zero(item.stress_change)
    param["fatigue_change"] = util.check_zero(item.fatigue_change)
    param["endurance_change"] = util.check_zero(item.endurance_change)
    param["flu_change"] = util.check_zero(item.flu_reduction)
    param["pain_change"] = util.check_zero(item.pain_reduction)
    param["sick_change"] = util.check_zero(item.reduce_food_sickness)
    param["alcoholic"] = util.check_zero(item.alcoholic)
    param["alcohol_power"] = util.check_zero(item.alcohol_power)
    param["reduce_infection_power"] = util.check_zero(item.reduce_infection_power)
    param["bandage_power"] = util.check_zero(item.bandage_power)
    param["poison_power"] = util.check_zero(item.poison_power)

    #-------------- COOKING --------------#
    param["cook_minutes"] = f'{item.minutes_to_cook} {get_translation("minute" if item.minutes_to_cook == 1 else "minutes")}' if item.is_cookable else None
    param["burn_minutes"] = f'{item.minutes_to_burn} {get_translation("minute" if item.minutes_to_burn == 1 else "minutes")}' if item.is_cookable else None
    param["dangerous_uncooked"] = item.dangerous_uncooked
    param["bad_microwaved"] = item.bad_in_microwave
    param["good_hot"] = item.good_hot
    param["bad_cold"] = item.bad_cold
    param["spice"] = item.spice
    # Not needed? this is just the recipe/ingredient name. The fallback is the item's name.
    #param["evolved_recipe"] = item.evolved_recipe_name 

    #-------------- TECHNICAL --------------#
    from scripts.items.item_tags import Tag
    param["tag"] = [Tag(tag).wiki_link for tag in item.tags] if item.tags else None
    param["guid"] = item.guid
    param["clothing_item"] = util.link("ClothingItem", item.clothing_item) if item.clothing_item else None
    param["rm_guid"] = None
    param["item_id"] = item.item_id

    param["infobox_version"] = Version.get()
    
    return param


def post_process_rm(data: dict, page: str):
    """Post processing of generated item data to add recorded media properties."""
    rm_id = RecMedia.get_id_from_page(page)
    rm = RecMedia(rm_id)

    #TODO: add more params and don't hardcode 'boredom_change'
    data["name"] = rm.name
    data["icon_name"] = rm.name
    data["boredom_change"] = "-5 per line"
    data["rm_guid"] = rm.id

    return data


translations_cache = {}
def get_translation(translation_key: str):
    from scripts.core.language import Translate

    translation_keys = {
        "day": "IGUI_Gametime_day",
        "days": "IGUI_Gametime_days",
        "minute": "IGUI_Gametime_minute",
        "minutes": "IGUI_Gametime_minutes"
    }

    global translations_cache
    if translation_key in translations_cache:
        return translations_cache.get(translation_key)

    if translation_key in translation_keys:
        translation = Translate.get(translation_keys.get(translation_key, translation_key))
        translations_cache[translation_key] = translation

        return translation
    
    return ""


def build_infobox(infobox_data: dict) -> list[str]:
    """
    Builds an infobox template from the provided parameters.

    Args:
        infobox_data (dict): Dictionary of key-value infobox fields.

    Returns:
        list[str]: A list of lines forming the infobox template.
    """
    if not infobox_data:
        return None
    content = []
    content.append("{{Infobox item")
    for key, value in infobox_data.items():
        content.append(f"|{key}={value}")
    content.append("}}")
    return content


def join_keys(params: dict) -> dict: #TODO: missing keys to join
    """
    Converts list values of specific keys into <br>-joined strings.

    Args:
        params (dict): Infobox parameters.

    Returns:
        dict: Updated dictionary with joined string values for specified keys.
    """
    STR_KEYS = [] # Keys that should be strings instead of indexed keys
    for key in STR_KEYS:
        if key in params and isinstance(params[key], list):
            params[key] = "<br>".join(str(v) for v in params[key])
    
    return params


def get_descriptor(item_id: str) -> str | None:
    """
    Returns a short label for the item, based on patterns in its ID.

    Matches are defined in 'item_descriptors.json' using start, end, or contains rules.

    Args:
        item_id (str): Full item ID.

    Returns:
        str | None: Descriptor if matched, otherwise None.
    """
    from scripts.core.cache import load_json
    global all_descriptors

    if not item_id:
        return None

    if not all_descriptors:
        all_descriptors = load_json(os.path.join(RESOURCE_DIR, "item_descriptors.json"))
    
    descriptor = None
    item = Item(item_id)
    item_type = item.id_type
    
    for key, value in all_descriptors.items():
        position = value.get("position")
        name = value.get("name")

        if position == "start" and item_type.startswith(key):
            descriptor = name
            break
        elif position == "end" and item_type.endswith(key):
            descriptor = name
            break
        elif position == "contains" and key in item_type:
            descriptor = name
            break
    
    return descriptor


def merge_items(page_data: dict) -> dict:
    """
    Merges parameters from multiple item variants into a single infobox-ready dictionary.

    Identical values shared across all items are included once without a descriptor.

    Keys listed in `DESCRIPTOR_KEYS` will trigger descriptor formatting if their values differ between items.
    Keys listed in `SKIP_KEYS` are only included from the first (primary) item.

    Args:
        page_data (dict): Mapping of item_id to parameter dictionaries.

    Returns:
        dict: Merged dictionary of parameters with values enumerated and descriptors applied where needed.
    """
    SKIP_KEYS = ["name"]
    DESCRIPTOR_KEYS = ["category", "weight", "combat_speed", "days_fresh", "days_rotten", "tag", "clothing_item", "body_location", "guid"]

    item_ids = list(page_data.keys())
    if not item_ids:
        return {}

    if len(item_ids) == 1:
        return util.enumerate_params(page_data[item_ids[0]], whitelist=numbered_params)

    primary_id = item_ids[0]
    total_items = len(item_ids)

    # Track which items each value appears in for each key
    key_sources: dict[str, dict[str, set[str]]] = {}  # key -> value -> set of item_ids

    for item_id in item_ids:
        params = page_data[item_id]
        for key, value in params.items():
            if item_id != primary_id and key in SKIP_KEYS:
                continue
            values = value if isinstance(value, list) else [value]
            for val in values:
                if not val:
                    continue
                key_sources.setdefault(key, {}).setdefault(val, set()).add(item_id)

    # Build merged output - apply descriptors only if values differ
    merged_params = {}
    for key, val_map in key_sources.items():
        use_descriptor = key in DESCRIPTOR_KEYS and len(val_map) > 1

        entries = []
        seen_displays = set()

        for val, ids in val_map.items():
            if not use_descriptor or len(ids) == total_items:
                # Value is shared by all items - no descriptor
                display = val
                if display not in seen_displays:
                    seen_displays.add(display)
                    entries.append(display)
            else:
                # Value appears in a subset of items - add descriptor per item
                for item_id in sorted(ids):
                    descriptor = get_descriptor(item_id)
                    display = f"{val} <small>({descriptor})</small>" if descriptor else val
                    if display not in seen_displays:
                        seen_displays.add(display)
                        entries.append(display)

        merged_params[key] = entries if len(entries) > 1 else (entries[0] if entries else None)

    # Post-process and enumerate list entries
    merged_params = join_keys(merged_params)
    return util.enumerate_params(merged_params, numbered_params)


def process_pages(pages: dict) -> None:
    """
    Generates infoboxes for all items grouped by page name and writes output files.

    Args:
        pages (dict): Mapping of page names to their item_id entries.
    """
    from urllib.parse import quote
    with tqdm(total=len(pages), desc="Building page infoboxes", unit=" pages", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        clear_dir(directory=ROOT_PATH)
        for page_name, page in pages.items():
            pbar.set_postfix_str(f'Processing page: {page_name[:30]}')
            item_ids = page.get("item_id", [])
            page_data = {}
            for item_id in item_ids:
                item = Item(item_id)
                if not item.valid:
                    echo.warning(f"Item ID '{item_id}' not found in the parsed data. Skipping.")
                    continue
                item_params = generate_item_data(item)

                if item.media_category:
                    post_process_rm(item_params, page_name)

                page_data[item_id] = item_params
            
            if not page_data:
                continue
            
            param = merge_items(page_data)
            content = build_infobox(param)
            if not content:
                continue
            page_name = page_name.replace(" ", "_")
            output_dir = write_file(content, quote(page_name, safe='()') + ".txt", root_path=ROOT_PATH, suppress=True)
            pbar.update(1)
    
        elapsed_time = pbar.format_dict["elapsed"]
    echo.success(f"Files saved to '{output_dir}' after {elapsed_time:.2f} seconds.")


def process_items(item_id_list: list) -> None:
    """
    Generates infoboxes for a list of specific item IDs and writes output files.

    Args:
        item_id_list (list): List of item IDs to process.
    """
    with tqdm(total=len(item_id_list), desc="Building item infoboxes", unit=" items", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        clear_dir(directory=ROOT_PATH)
        for item_id in item_id_list:
            item = Item(item_id)
            pbar.set_postfix_str(f'Processing: {item.type} ({item_id[:30]})')
            infobox_data = generate_item_data(item)
            infobox_data = util.enumerate_params(infobox_data, numbered_params)
            content = build_infobox(infobox_data)
            output_dir = write_file(content, item_id + ".txt", root_path=ROOT_PATH, suppress=True)
            pbar.update(1)
        elapsed_time = pbar.format_dict["elapsed"]
    echo.success(f"Files saved to '{output_dir}' after {elapsed_time:.2f} seconds.")


## ------------------- Initialisation/Preparation ------------------- ##
def prepare_media_pages(rm_id) -> set:
    rec_list = RecMedia.get_item_dict().get(rm_id)

    with tqdm(total=len(rec_list), desc="Getting media pages", unit=" pages", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        for rm_id in rec_list:
            pbar.set_postfix_str(f'Processing RM id: {rm_id[:30]}')

            if not RecMedia.exists(rm_id):
                echo.warning(f"'{rm_id}' could not be found as a 'RecMedia', please check '{rm_id}' media results.")
                continue

            page = RecMedia(rm_id).page
            page_data:dict = pages_dict.get(page)

            if not page_data:
                pages_dict[page] = {"rm_guid": [rm_id]} #NOTE: this modifies the global variable
                logger.write(
                    message=f"'{rm_id}' missing from page dict, added to '{color.style(page, color.GREEN)}' {color.style('[new]', color.YELLOW)}.",
                    print_bool=True,
                    category="warning",
                    file_name="missing_pages_log.txt"
                )

            else:
                id_list: list = page_data.setdefault("rm_guid", [])
                if rm_id not in id_list:
                    id_list.append(rm_id)
                    logger.write(
                        message=f"'{rm_id}' missing from page dict, added to '{color.style(page, color.GREEN)}'.",
                        print_bool=True,
                        category="warning",
                        file_name="missing_pages_log.txt"
                    )
            pbar.update(1)

    return 

def prepare_pages(item_id_list: list) -> dict:
    """
    Prepares and validates the item-to-page mappings for later infobox generation.

    Args:
        item_id_list (list): List of item IDs to process.

    Returns:
        dict: Updated pages dictionary containing valid item_id groupings.
    """
    global pages_dict
    raw_page_dict = page_manager.get_raw_page_dict()
    item_page_dict = raw_page_dict.get('item')
    #save_cache(item_page_dict, "item_page_dict.json")

    seen_items = set()
    pages_dict = item_page_dict.copy()

    with tqdm(total=len(item_id_list), desc="Building page list", unit=" items", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        for item_id in item_id_list:
            pbar.set_postfix_str(f'Processing item id: {item_id[:30]}')

            is_media = True if item_id in RecMedia.get_item_dict() else False

            if item_id in seen_items and not is_media:
                continue

            seen_items.add(item_id)

            if is_media:
                prepare_media_pages(item_id) # Gets the media pages and adds them to the page dict
                continue

            page = Item(item_id).page
            page_data:dict = pages_dict.get(page)

            if not page_data:
                pages_dict[page] = {"item_id": [item_id]}
                logger.write(
                    message=f"'{item_id}' missing from page dict, added to '{color.style(page, color.GREEN)}' {color.style('[new]', color.YELLOW)}.",
                    print_bool=True,
                    category="warning",
                    file_name="missing_pages_log.txt"
                )

            else:
                id_list:list = page_data.setdefault("item_id", [])
                if item_id not in id_list:
                    id_list.append(item_id)
                    logger.write(
                        message=f"'{item_id}' missing from page dict, added to '{color.style(page, color.GREEN)}'.",
                        print_bool=True,
                        category="warning",
                        file_name="missing_pages_log.txt"
                    )
                seen_items.update(id_list)
            pbar.update(1)
    
    #save_cache(pages_dict, "temp.json")
    return pages_dict


def select_item() -> list:
    """
    Prompts the user to input one or more item IDs (semicolon-separated) and returns the valid ones.

    Returns:
        list[str]: A list of valid item IDs.
    """
    while True:
        query = input("Enter one or more item IDs (separated by semicolons):\n> ")
        item_ids = [item_id.strip() for item_id in query.split(';') if item_id.strip()]
        valid_items = []
        invalid_items = []

        for item_id in item_ids:
            if Item.exists(item_id):
                item = Item(item_id)
                echo.success(f"Found item_id: '{item.item_id}' ({item.name})")
                valid_items.append(item.item_id)
            else:
                invalid_items.append(item_id)

        if valid_items:
            if invalid_items:
                print(f"Some IDs weren't found and were skipped: {', '.join(invalid_items)}")
            return valid_items

        print("Couldn't find any of the IDs. Try again.")


def select_page() -> dict[str, dict[str, list[str]]]:
    """
    Prompts the user to input one or more page names (semicolon-separated) and returns a
    dictionary of valid pages and their associated item IDs.

    Returns:
        dict: A dictionary mapping page names to their valid item IDs.
    """
    while True:
        query = input("Enter one or more page names (separated by semicolons):\n> ")
        page_names = [name.strip() for name in query.split(';') if name.strip()]
        valid_pages = {}

        for name in page_names:
            if name in pages_dict:
                item_ids = pages_dict[name].get("item_id")
                valid_ids = [item_id for item_id in item_ids if Item.exists(item_id)] if item_ids else []
                if valid_ids:
                    valid_pages[name] = {"item_id": valid_ids}
                else:
                    print(f"No valid item IDs found for page '{name}'. Skipping.")
            else:
                print(f"Page '{name}' not found. Skipping.")

        if valid_pages:
            return valid_pages

        print("None of the entered pages had valid item IDs. Try again.")


def choose_process(run_directly: bool):
    """
    Presents the user with infobox generation options.

    Args:
        run_directly (bool): Whether to allow quitting or going back.

    Returns:
        str: The selected menu option.
    """
    WIP = color.style("[WIP]", color.BRIGHT_YELLOW)
    options = [
        "1: All: Pages - Generate infoboxes based on page, merging data from each Item ID. " + WIP,
        "2: All: Item IDs - Generate infoboxes for every item (no infobox merging). ",
        "3: Select: Page - Choose one or more pages to generate an infobox for. " + WIP,
        "4: Select: Item ID - Choose one or more Item IDs to generate an infobox for. "
    ]
    options.append("Q: Quit" if run_directly else "B: Back")

    while True:
        print("\nWhich items do you want to generate an infobox for?")
        choice = input("\n".join(options) + "\n> ").strip().lower()

        if choice in ('q', 'b'):
            break

        try:
            if int(choice) in range(1, 5):
                break
        except ValueError:
            pass
        print("Invalid choice.")

    return choice


def init_dependencies():
    """Initialises required modules so they don't interrupt tqdm progress bars."""
    from scripts.core.language import Language
    Language.get()
    page_manager.init()


def main(run_directly: bool = False):
    """
    Entry point for infobox generation.

    Args:
        run_directly (bool): Whether the script is being run directly.
    """
    init_dependencies()
    item_id_list = list(Item.keys())
    pages = prepare_pages(item_id_list)

    user_choice = choose_process(run_directly)

    if user_choice == '3':
        pages = select_page()
    elif user_choice == '4':
        item_id_list = select_item()

    if user_choice in ['1', '3']:
        process_pages(pages)
    elif user_choice in ['2', '4']:
        process_items(item_id_list)


if __name__ == "__main__":
    main(run_directly=True)

    # Testing - exports all infoboxes to a single txt file
#    from scripts.core.file_loading import load_file
#    from pathlib import Path
#    from scripts.core.language import Language

#    query_path = Path(ROOT_PATH.format(language_code=Language.get()))
#    content = ['<div style="display: flex; flex-wrap: wrap;">']
#    for file in query_path.iterdir():
#        if file.is_file():
#            lines = load_file(file.name, ROOT_PATH)
#            content.append("<div>")
#            content.extend(lines)
#            content.append("</div>")
#    content.append("</div>")

#    write_file(content)


    # Test query string:
    # Base.NormalCarSeat1;Base.SmallGasTank1;Base.OldTire1;Base.RadioBlack;Base.HamRadio2;Base.CarBattery1;Base.OldBrake1;Base.OldCarMuffler1;Base.RearCarDoor1;Base.RearWindow1;Base.RearWindshield1;Base.BigTrunk1;Base.LightbarYellow;Base.LightBulb;Base.ModernSuspension3;Base.HoodOrnament_Spiffo;Base.EngineParts
