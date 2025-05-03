from tqdm import tqdm
from scripts.core.language import Language, Translate
from scripts.utils import utility, table_helper
from scripts.utils.util import format_link, format_positive
from scripts.utils.echo import echo
from scripts.parser import item_parser, fixing_parser
from scripts.recipes import legacy_recipe_parser
from scripts.core.constants import RESOURCE_DIR, PBAR_FORMAT

TABLE_PATH = f"{RESOURCE_DIR}/tables/weapon_table.json"

box_types = {}
all_items = {}
table_map = {}
table_type_map = {}

def check_fixing(item_id):
    """ Check if it can be fixed """
    module, item_name = item_id.split('.')
    parsed_fixing_data = fixing_parser.get_fixing_data(True)
    for fixing, fixing_data in parsed_fixing_data[module].items():
        if isinstance(fixing_data, dict) and 'Require' in fixing_data:
            if item_name in fixing_data['Require']:
                return f'[[File:UI Tick.png|link=Condition{Language.get_subpage()}#<<repairing>>|<<repairable>>]]'
    return f'[[File:UI Cross.png|link=Condition{Language.get_subpage()}#<<repairing>>|<<not_repairable>>]]'


def generate_ammo_data(item_id, item_data):
    table_type = item_data.get("TableType")
    box_data = box_types.get(item_id, {})
    round_id = None
    box_id = None
    carton_id = None
    magazine = None
    weapons = []

    if table_type == "carton":
        # Get carton
        carton_id = item_id
        carton_q = 1
        # Get box
        box_id = box_data.get("contents")
        box_q = box_data.get("quantity")
        # Get round
        round_id = box_types.get(box_id, {}).get("contents")
        round_q = box_types.get(box_id, {}).get("quantity") * box_q
    elif table_type == "box":
        # Get box
        box_id = item_id
        box_q = 1
        # Get round
        round_id = box_data.get("contents")
        round_q = box_data.get("quantity")
        # Get carton
        for key, value in box_types.items():
            if value.get("contents") == box_id:
                carton_id = key
                carton_q = value.get("quantity") * box_q
                break
    elif table_type == "round":
        # Get round
        round_id = item_id
        round_q = 1
        # Get box
        for key, value in box_types.items():
            if value.get("contents") == item_id:
                box_id = key
                box_q = value.get("quantity")
                break
        # Get carton
        for key, value in box_types.items():
            if value.get("contents") == box_id:
                carton_id = key
                carton_q = value.get("quantity") * box_q
                break
    
    
    for key, value in all_items.items():
        # Get firearms
        if value.get("TableType") in table_type_map.get("firearm") and value.get("AmmoType") == round_id:
            weapons.append(key)
            continue
        
        # Get magazine
        if value.get("TableType") == "magazine" and value.get("AmmoType") == round_id:
            magazine = key

    # Add data to dict
    if carton_id and carton_id != item_id:
        item_data["AmmoCarton"] = carton_id
        item_data["AmmoCartonQuantity"] = carton_q
    if box_id and box_id != item_id:
        item_data["AmmoBox"] = box_id
        item_data["AmmoBoxQuantity"] = box_q
    if round_id and round_id != item_id:
        item_data["AmmoType"] = round_id
        item_data["AmmoTypeQuantity"] = round_q
    if weapons:
        item_data["Weapons"] = weapons
    if magazine:
        item_data["Magazine"] = magazine

    return item_data


def get_function(item_id, item_data):
    strings = {
        "reload_time": {
            "value": "{desc1} reload time by {var1}.",
            "var": ["ReloadTimeModifier"],
            "desc": ["ReloadTimeModifier"]
        },
        "light": {
            "value": "Adds a toggleable light with distance {var1} and strength {var2}.",
            "var": ["LightDistance", "LightStrength"]
        },
        "spread": {
            "value": "{desc1} the spread by {var1}.",
            "var": ["ProjectileSpreadModifier"],
            "desc": ["ProjectileSpreadModifier"]
        },
        "max_range": {
            "value": "{desc1} maximum range by {var1}.",
            "var": ["MaxRangeModifier"],
            "desc": ["MaxRangeModifier"]
        },
        "recoil": {
            "value": "{desc1} recoil by {var1}.",
            "var": ["RecoilDelayModifier"],
            "desc": ["RecoilDelayModifier"]
        },
        "sight_range": {
            "value": "Sight range changed to {var1}–{var2}.",
            "var": ["MinSightRange", "MaxSightRange"]
        },
        "low_light": {
            "value": "{desc1} low-light penalty when aiming by {var1}.",
            "var": ["AimingLowLightModifier"],
            "desc": ["AimingLowLightModifier"]
        },
        "hit_chance": {
            "value": "{desc1} accuracy by {var1}.",
            "var": ["HitChanceModifier"],
            "desc": ["HitChanceModifier"]
        }
    }

    string_list = []

    for entry in strings.values():
        if not isinstance(entry, dict) or "value" not in entry:
            continue

        template = entry["value"]
        var_names = entry.get("var", [])
        desc_names = entry.get("desc", [])

        var_values = []
        desc_values = []

        for var in var_names:
            value = item_data.get(var)
            if value is None:
                break
            var_values.append(value)
        else:
            for desc_var in desc_names:
                try:
                    val = float(item_data.get(desc_var, 0))
                except (TypeError, ValueError):
                    val = 0
                desc = "increases" if val > 0 else "decreases"
                desc_values.append(desc)

            format_map = {f"var{i+1}": val for i, val in enumerate(var_values)}
            for i, desc in enumerate(desc_values):
                placeholder = f"{{desc{i+1}}}"
                if template.startswith(placeholder):
                    desc = desc.capitalize()
                format_map[f"desc{i+1}"] = desc

            string_list.append(template.format(**format_map))

    return "style=\"text-align:left;\" | "+ "<br>".join(string_list) if string_list else "-"


def generate_data(item_id, item_data):
    notes = None
    table_type = item_data.get("TableType")
    for key, value in table_type_map.items():
        if table_type in value:
            columns = table_map.get(key)
            break
        else:
            columns = table_map.get("default")

    item_name = utility.get_name(item_id, item_data)

    if table_type in ("round", "box", "carton"):
        item_data = generate_ammo_data(item_id, item_data)

    item = {}

    item["icon"] = item_data.get("IconFormatted") if "icon" in columns else None
    item["name"] = format_link(item_name, utility.get_page(item_id, item_name)) if "name" in columns else None
    item["weight"] = item_data.get("Weight", "1") if "weight" in columns else None
    if "equipped" in columns:
        equipped = "<<1h>>"
        if item_data.get("RequiresEquippedBothHands", "false").lower() == "true":
            equipped = "<<2h>>"
        elif item_data.get("TwoHandWeapon", "false").lower() == "true":
            equipped = "{{Tooltip|<<2h>>*|<<limited_impact_desc>>}}"
            notes = "<nowiki>*</nowiki><<limited_impact_desc>>"
        if item_data.get("CloseKillMove") == "Jaw_Stab":
            equipped = "{{Tooltip|<<1h>>*|<<jaw_stab_desc>>}}"
            notes = "<nowiki>*</nowiki><<jaw_stab_desc>>"
        item["equipped"] = Translate.get_wiki(equipped)
    if "ammo" in columns:
        item["ammo"] = utility.get_icon(item_data.get("AmmoType"), True, True, True) if item_data.get("AmmoType") is not None else "-"
    item["capacity"] = item_data.get('MaxAmmo', item_data.get('ClipSize', '-')) if "capacity" in columns else None
    item["min_damage"] = item_data.get('MinDamage', '-') if "min_damage" in columns else None
    item["max_damage"] = item_data.get('MaxDamage', '-') if "max_damage" in columns else None
    item["door_damage"] = item_data.get('DoorDamage', '-') if "door_damage" in columns else None
    item["tree_damage"] = item_data.get('TreeDamage', '-') if "tree_damage" in columns else None
    item["min_range"] = item_data.get('MinRange', '-') if "min_range" in columns else None
    item["max_range"] = item_data.get('MaxRange', '-') if "max_range" in columns else None
    item["attack_speed"] = item_data.get('BaseSpeed', '1') if "attack_speed" in columns else None
    if "endurance_mod" in columns:
        endurance_mod = format_positive(float(item_data.get('EnduranceMod', 1)) - 1)
        item["endurance_mod"] = "-" if endurance_mod == "0" else endurance_mod
    item["hit_chance"] = item_data.get('HitChance', '-') + '%' if "hit_chance" in columns else None
    item["hit_chance_mod"] = '+' + item_data.get('AimingPerkHitChanceModifier', '-') + '%' if "hit_chance_mod" in columns else None
    if "crit_chance" in columns:
        item["crit_chance"] = item_data.get("CriticalChance") + "%" if item_data.get("CriticalChance") is not None else "-"
    if "crit_multiplier" in columns:
        item["crit_multiplier"] = item_data.get("CritDmgMultiplier") + "×" if item_data.get("CritDmgMultiplier") is not None else "-"
    if "crit_chance_mod" in columns:
        item["crit_chance_mod"] = "+" + item_data.get("AimingPerkCritModifier") + "%" if item_data.get("AimingPerkCritModifier") is not None else "-"
    if "sound_radius" in columns:
        sound_radius = item_data.get('SoundRadius', item_data.get('NoiseRange'))
        sound_radius_int = int(sound_radius) if sound_radius is not None else 0
        if sound_radius_int <= 0 and item_data.get("ExplosionSound") is not None:
            sound_radius = "50" # Defined in IsoTrap.class.triggerExplosion() (find: getExplosionSound)
        if sound_radius is not None:
            item["sound_radius"] = sound_radius
        else:
            item["sound_radius"] = "-"
    item["knockback"] = item_data.get('PushBackMod', '-') if "knockback" in columns else None
    if "condition_max" in columns or "condition_lower_chance" in columns:
        condition_max = item_data.get("ConditionMax", '0')
        condition_lower_chance = item_data.get("ConditionLowerChanceOneIn", '0')
        item["condition_max"] = condition_max if "condition_max" in columns else None
        item["condition_lower_chance"] = condition_lower_chance if "condition_max" in columns else None
        item["condition_average"] = str(int(condition_max) * int(condition_lower_chance)) if "condition_max" in columns and "condition_lower_chance" in columns else None
    item["repairable"] = Translate.get_wiki(check_fixing(item_id)) if "repairable" in columns else None
    if "magazine" in columns:
        item["magazine"] = utility.get_icon(item_data.get("Magazine"), True, True, True) if item_data.get("Magazine") else "-"
    if "weapon" in columns:
        if table_type == "magazine":
            item["weapon"] = utility.get_icon(item_data.get("GunType"), True, True, True) if item_data.get("GunType") is not None else "-"
        elif item_data.get("MountOn"):
            weapons_list = []
            weapons = item_data.get("MountOn") if isinstance(item_data.get("MountOn"), list) else [item_data.get("MountOn")]
            for weapon in weapons:
                weapon  = "Base." + weapon if not weapon.startswith("Base.") else weapon
                weapons_list.append(utility.get_icon(weapon, True, True, True))
            item["weapon"] = "".join(weapons_list)
        elif item_data.get("Weapons"):
            weapons = []
            for weapon in item_data.get("Weapons"):
                weapons.append(all_items.get(weapon).get("IconFormatted"))
            item["weapon"] = "".join(weapons)
        else:
            item["weapon"] = "-"
    item["rounds"] = utility.get_icon(item_data.get("AmmoType"), True, True, True) + f" ({item_data.get('AmmoTypeQuantity')})" if "rounds" in columns else None
    item["box"] = utility.get_icon(item_data.get("AmmoBox"), True, True, True) + f" ({item_data.get('AmmoBoxQuantity')})" if "box" in columns else None
    item["carton"] = utility.get_icon(item_data.get("AmmoCarton"), True, True, True) + f" ({item_data.get('AmmoCartonQuantity')})" if "carton" in columns else None
    if "effect" in columns:
        effects = {
            "Smoke": {"property": "SmokeRange", "string": "Smoke"}, # Priority 1
            "Noise": {"property": "NoiseDuration", "string": "[[Noise{lcs}|Noise]]"}, # Priority 2
            "Fire": {"property": "FirePower", "string": "[[Fire{lcs}|Fire]]"}, # Priority 3
            "Explosion": {"property": "ExplosionPower", "string": "[[Fire{lcs}|Explosion]]"}, # Priority 4
        }
        for key, value in effects.items():
            if item_data.get(value["property"]):
                effect = key
                item["effect"] = value["string"].format(lcs=Language.get_subpage())
                break
            else:
                item["effect"] = "-"
    item["effect_power"] = item_data.get(f'{effect}Range', '-') if "effect_power" in columns else None
    item["effect_range"] = item_data.get(f'{effect}Range', '-') if "effect_range" in columns else None
    item["effect_timer"] = item_data.get(f'{effect}Range', '-') if "effect_timer" in columns else None
    item["sensor_range"] = item_data.get('SensorRange', '-') if "sensor_range" in columns else None
    item["part_type"] = Translate.get("Tooltip_weapon_" + item_data.get("PartType", "-")) if "part_type" in columns else None
    item["weight_mod"] = item_data.get('WeightModifier', '-') if "weight_mod" in columns else None
    item["aiming_time"] = item_data.get('AimingTimeModifier', '-') if "aiming_time" in columns else None
    item["function"] = get_function(item_id, item_data) if "function" in columns else None
    item["item_id"] = item_id if "item_id" in columns else None

    # Remove any values that are None
    item = {k: v for k, v in item.items() if v is not None}

    # Ensure column order is correct
    item = {key: item[key] for key in columns if key in item}

    # Add item_name for sorting
    item["item_name"] = item_name
    item["notes"] = notes if notes else None

    return item


def find_table_type(item_id, item_data):
    table_type = None
    tags = item_data.get("Tags")

    if item_data.get("Type") == "Weapon":
        skill = item_data.get("Categories")
        if skill:
            # Melee
            skill = [skill] if isinstance(skill, str) else skill
            # Remove "Improvised" from list if more than 1
            if "Improvised" in skill and len(skill) > 1:
                skill = [cat for cat in skill if cat != "Improvised"]
                if len(skill) > 1:
                    echo(f"WARNING: More than 1 skill ({','.join(skill)})")
            table_type = skill[0]
        elif item_data.get("SubCategory") == "Firearm":
            # Firearm
            table_type = "handgun"
            if item_data.get("RequiresEquippedBothHands", "").lower() == "true":
                table_type = "rifle"
                if int(item_data.get("ProjectileCount")) > 1:
                    table_type = "shotgun"
        elif item_data.get("DisplayCategory") == "Explosives":
            # Explosives
            table_type = "explosive"
    elif item_data.get("Type").lower() == "WeaponPart".lower():
        # Weapon parts
        table_type = "weapon_part"
    elif item_id in box_types:
        # Ammo (box & carton)
        table_type = box_types[item_id].get("type")
    elif item_data.get("Tags") is not None:
        tags = item_data.get("Tags")
        tags = [tags] if isinstance(tags, str) else tags
        # Ammo (rounds)
        if any(tag.lower() == "ammo" for tag in tags):
            table_type = "round"
        elif any(tag.lower() in {"pistolmagazine", "riflemagazine"} for tag in tags):
            # Magazine
            table_type = "magazine"

    item_data["TableType"] = table_type

    return item_data


def find_items():
    items = {}
    all_item_data = item_parser.get_item_data()
    for item_id, item_data in all_item_data.items():
        item_data = find_table_type(item_id, item_data)
        if item_data.get("TableType"):
            item_data["IconFormatted"] = utility.get_icon(item_id, True, True, True)
            items[item_id] = item_data
    
    return items


def find_boxes():
    global box_types

    ammo_recipes = {
        "OpenBoxOfShotgunShells": "box",
        "OpenBoxOfBullets50": "box",
        "OpenBoxOfBullets20": "box",
        "OpenCartonOfBullets": "carton"
    }

    recipes_data = legacy_recipe_parser.get_recipe_data()["recipes"]
    for recipe in recipes_data:
        name = recipe.get("name")
        if name in ammo_recipes:
            outputs = recipe.get("outputs", [])
            
            for output in outputs:
                mapper = output.get("mapper")
                quantity = output.get("index")
                items = output.get("items")

            if mapper == "ammoTypes":
                item_mappers = recipe.get("itemMappers", {}).get(mapper)
                for key, value in item_mappers.items():
                    box_types[value] = {
                        "type": ammo_recipes.get(name),
                        "contents": key,
                        "quantity": quantity
                    }
            
            elif items is not None:
                box_types[recipe.get("inputs")[0].get("items")[0]] = {
                    "type": ammo_recipes.get(name),
                    "contents": items[0],
                    "quantity": quantity
                }


def main():
    global table_map
    global all_items
    global table_type_map
    Language.get()
    table_map, column_headings, table_type_map = table_helper.get_table_data(TABLE_PATH, "type_map")
    find_boxes()

    with tqdm(total=0, desc="Preparing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        all_items = find_items()

        pbar.total = len(all_items)
        pbar.refresh()

        generated_data = {}

        for item_id, item_data in all_items.items():
            table_type = item_data.get("TableType")
            pbar.set_postfix_str(f'Generating: {table_type} ({item_id[:30]})')
            if table_type is not None:
                new_item = generate_data(item_id, item_data)

                note = new_item.pop("notes", None)

                if table_type not in generated_data:
                    generated_data[table_type] = [{"notes": [note]}] if note else [{"notes": []}]
                else:
                    if note:
                        if generated_data[table_type] and "notes" in generated_data[table_type][0]:
                            if note not in generated_data[table_type][0]["notes"]:
                                generated_data[table_type][0]["notes"].append(note)
                        else:
                            generated_data[table_type].insert(0, {"notes": [note]})
                
                generated_data[table_type].append(new_item)

            pbar.update(1)

        mapped_table = {
            item_type: table_map[key]
            for key, value_list in table_type_map.items()
            for item_type in value_list
        }

        pbar.set_postfix_str("Creating tables...")
        table_helper.create_tables("weapon", generated_data, columns=column_headings, table_map=mapped_table, combine_tables=False, suppress=True)


if __name__ == "__main__":
    main()