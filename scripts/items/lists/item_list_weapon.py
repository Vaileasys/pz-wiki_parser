import os
from tqdm import tqdm
from scripts.core.language import Language, Translate
from scripts.utils import table_helper, echo, util
from scripts.utils.util import format_positive, convert_int
from scripts.objects.item import Item
from scripts.objects.fixing import Fixing
from scripts.objects.craft_recipe import CraftRecipe
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT

TABLE_PATH = os.path.join(TABLES_DIR, "weapon_table.json")

box_types = {}
table_map = {}
table_type_map = {}
all_item_data = {}  # Cache for each item's `TableType`


def check_fixing(item_id):
    """Check if a given item can be fixed"""
    fixing = Fixing(item_id)
    if fixing.valid:
        return f"[[File:UI Tick.png|link=Condition{Language.get_subpage()}#<<repairing>>|<<repairable>>]]"
    return f"[[File:UI Cross.png|link=Condition{Language.get_subpage()}#<<repairing>>|<<not_repairable>>]]"


def generate_ammo_data(item_id: str, table_type: str):
    box_data = box_types.get(item_id, {})
    round_id = None
    box_id = None
    carton_id = None
    magazine = None
    weapons = []
    item_data: dict = all_item_data.get(item_id)

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

    for n_item_id in Item.all():
        # Get firearms
        if (
            all_item_data.get(n_item_id, {}).get("TableType")
            in table_type_map.get("firearm")
            and Item.get_id_from_key(Item(n_item_id).ammo_type) == round_id
        ):
            weapons.append(n_item_id)
            continue

        # Get magazine
        if (
            all_item_data.get(n_item_id, {}).get("TableType") == "magazine"
            and Item.get_id_from_key(Item(n_item_id).ammo_type) == round_id
        ):
            magazine = n_item_id

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


def get_function(item: Item):
    strings = {
        "reload_time": {
            "value": "{desc1} reload time by {var1}.",
            "var": ["ReloadTimeModifier"],
            "desc": ["ReloadTimeModifier"],
        },
        "light": {
            "value": "Adds a toggleable light with distance {var1} and strength {var2}.",
            "var": ["LightDistance", "LightStrength"],
        },
        "spread": {
            "value": "{desc1} the spread by {var1}.",
            "var": ["ProjectileSpreadModifier"],
            "desc": ["ProjectileSpreadModifier"],
        },
        "max_range": {
            "value": "{desc1} maximum range by {var1}.",
            "var": ["MaxRangeModifier"],
            "desc": ["MaxRangeModifier"],
        },
        "recoil": {
            "value": "{desc1} recoil by {var1}.",
            "var": ["RecoilDelayModifier"],
            "desc": ["RecoilDelayModifier"],
        },
        "sight_range": {
            "value": "Sight range changed to {var1}–{var2}.",
            "var": ["MinSightRange", "MaxSightRange"],
        },
        "low_light": {
            "value": "{desc1} low-light penalty when aiming by {var1}.",
            "var": ["AimingLowLightModifier"],
            "desc": ["AimingLowLightModifier"],
        },
        "hit_chance": {
            "value": "{desc1} accuracy by {var1}.",
            "var": ["HitChanceModifier"],
            "desc": ["HitChanceModifier"],
        },
    }

    string_list = []

    for entry in strings.values():
        if not isinstance(entry, dict) or "value" not in entry:
            continue

        template: str = entry["value"]
        var_names = entry.get("var", [])
        desc_names = entry.get("desc", [])

        var_values = []
        desc_values = []

        for var in var_names:
            value = item.get(var)
            if value is None:
                break
            var_values.append(value)
        else:
            for desc_var in desc_names:
                try:
                    val = float(item.get(desc_var))
                except (TypeError, ValueError):
                    val = 0
                desc: str = "increases" if val > 0 else "decreases"
                desc_values.append(desc)

            format_map = {f"var{i + 1}": val for i, val in enumerate(var_values)}
            for i, desc in enumerate(desc_values):
                placeholder = f"{{desc{i + 1}}}"
                if template.startswith(placeholder):
                    desc = desc.capitalize()
                format_map[f"desc{i + 1}"] = desc

            string_list.append(template.format(**format_map))

    return (
        'style="text-align:left;" | ' + "<br>".join(string_list) if string_list else "-"
    )


def generate_data(item_id: str, table_type: str):
    item = Item(item_id)
    notes = None
    for key, value in table_type_map.items():
        # Case-insensitive comparison
        if any(table_type.lower() == v.lower() for v in value):
            columns = table_map.get(key)
            break
        else:
            columns = table_map.get("default")

    if table_type in ("round", "box", "carton"):
        item_data = generate_ammo_data(item_id, table_type)

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = convert_int(item.weight) if "weight" in columns else None
    if "equipped" in columns:
        equipped = "<<1h>>"
        if item.requires_equipped_both_hands:
            equipped = "<<2h>>"
        elif item.two_hand_weapon:
            equipped = "{{Tooltip|<<2h>>*|<<limited_impact_desc>>}}"
            notes = "<nowiki>*</nowiki><<limited_impact_desc>>"
        if item.close_kill_move == "Jaw_Stab":
            equipped = "{{Tooltip|<<1h>>*|<<jaw_stab_desc>>}}"
            notes = "<nowiki>*</nowiki><<jaw_stab_desc>>"
        item_dict["equipped"] = Translate.get_wiki(equipped)
    if "ammo" in columns:
        item_dict["ammo"] = Item(Item.get_id_from_key(item.ammo_type)).icon if item.ammo_type else "-"
    item_dict["capacity"] = (
        (item.max_ammo or item.clip_size) if "capacity" in columns else None
    )
    item_dict["min_damage"] = (
        (convert_int(item.min_damage) or "-") if "min_damage" in columns else None
    )
    item_dict["max_damage"] = (
        (convert_int(item.max_damage) or "-") if "max_damage" in columns else None
    )
    item_dict["door_damage"] = (
        (item.door_damage or "-") if "door_damage" in columns else None
    )
    item_dict["tree_damage"] = (
        (item.tree_damage or "-") if "tree_damage" in columns else None
    )
    item_dict["min_range"] = (
        (convert_int(item.min_range) or "-") if "min_range" in columns else None
    )
    item_dict["max_range"] = (
        (convert_int(item.max_range) or "-") if "max_range" in columns else None
    )
    item_dict["attack_speed"] = (
        convert_int(item.base_speed) if "attack_speed" in columns else None
    )
    if "endurance_mod" in columns:
        endurance_mod = f"{util.convert_int(item.endurance_mod)}×"
        item_dict["endurance_mod"] = (
            "-" if not item.get("EnduranceMod") else endurance_mod
        )
    item_dict["hit_chance"] = (
        (str(convert_int(item.hit_chance)) or "-") + "%"
        if "hit_chance" in columns
        else None
    )
    item_dict["hit_chance_mod"] = (
        f"+{convert_int(item.aiming_perk_hit_chance_modifier)}%"
        if "hit_chance_mod" in columns
        else None
    )
    if "crit_chance" in columns:
        item_dict["crit_chance"] = (
            f"{convert_int(item.critical_chance)}%" if item.critical_chance else "-"
        )
    if "crit_multiplier" in columns:
        item_dict["crit_multiplier"] = (
            f"{convert_int(item.crit_dmg_multiplier)}×"
            if item.crit_dmg_multiplier
            else "-"
        )
    if "crit_chance_mod" in columns:
        item_dict["crit_chance_mod"] = (
            f"+{item.aiming_perk_crit_modifier}%"
            if item.aiming_perk_crit_modifier
            else "-"
        )
    if "sound_radius" in columns:  # FIXME: check item.noise_radius
        sound_radius = item.get("SoundRadius", item.get_default("NoiseRange"))
        if sound_radius <= 0 and item.explosion_sound is not None:
            sound_radius = "50"  # Defined in IsoTrap.class.triggerExplosion() (find: getExplosionSound)
        if sound_radius != 0:
            item_dict["sound_radius"] = sound_radius
        else:
            item_dict["sound_radius"] = "-"
    item_dict["knockback"] = (
        (convert_int(item.push_back_mod) or "-") if "knockback" in columns else None
    )
    if "condition_max" in columns or "condition_lower_chance" in columns:
        condition_max = item.condition_max
        condition_lower_chance = item.condition_lower_chance_one_in
        item_dict["condition_max"] = (
            condition_max if "condition_max" in columns else None
        )
        item_dict["condition_lower_chance"] = (
            condition_lower_chance if "condition_max" in columns else None
        )
        item_dict["condition_average"] = (
            str(int(condition_max) * int(condition_lower_chance))
            if "condition_max" in columns and "condition_lower_chance" in columns
            else None
        )
    item_dict["repairable"] = (
        Translate.get_wiki(check_fixing(item_id)) if "repairable" in columns else None
    )
    if "magazine" in columns:
        item_dict["magazine"] = (
            Item(item_data.get("Magazine")).icon if item_data.get("Magazine") else "-"
        )
    if "weapon" in columns:
        if table_type == "magazine":
            item_dict["weapon"] = (
                Item(item.gun_type).icon if item.gun_type is not None else "-"
            )
        elif item.mount_on:
            weapons_list = []
            weapons = item.mount_on
            for weapon in weapons:
                weapons_list.append(Item(weapon).icon)
            item_dict["weapon"] = "".join(weapons_list)
        elif item_data.get("Weapons"):
            weapons = []
            for weapon in item_data.get("Weapons"):
                weapons.append(Item(weapon).icon)
            item_dict["weapon"] = "".join(weapons)
        else:
            item_dict["weapon"] = "-"
    item_dict["rounds"] = (
        Item(item_data.get("AmmoType")).icon + f" ({item_data.get('AmmoTypeQuantity')})"
        if "rounds" in columns
        else None
    )
    item_dict["box"] = (
        Item(item_data.get("AmmoBox")).icon + f" ({item_data.get('AmmoBoxQuantity')})"
        if "box" in columns
        else None
    )
    item_dict["carton"] = (
        Item(item_data.get("AmmoCarton")).icon
        + f" ({item_data.get('AmmoCartonQuantity')})"
        if "carton" in columns
        else None
    )
    if "effect" in columns:
        effects = {
            "Smoke": {"property": "SmokeRange", "string": "Smoke"},  # Priority 1
            "Noise": {
                "property": "NoiseDuration",
                "string": "[[Noise{lcs}]]",
            },  # Priority 2
            "Fire": {"property": "FirePower", "string": "[[Fire{lcs}]]"},  # Priority 3
            "Explosion": {
                "property": "ExplosionPower",
                "string": "[[Fire{lcs}|Explosion]]",
            },  # Priority 4
        }
        # TODO: add a better way to detect fire effect. FirePower property removed in 42.12.0
        effect = (
            "Fire"
            if (
                item_id.startswith("Base.FlameTrap")
                or item_id.startswith("Base.Molotov")
            )
            else None
        )

        if effect is None:
            for key, value in effects.items():
                if item.get(value["property"]) is not None:
                    effect = key
                    break

        if effect is not None:
            item_dict["effect"] = (
                effects.get(effect).get("string").format(lcs=Language.get_subpage())
            )
        else:
            item_dict["effect"] = "-"
    item_dict["effect_power"] = (
        item.get_default(f"{effect}Power", "-") if "effect_power" in columns else None
    )
    item_dict["effect_range"] = (
        item.get_default(f"{effect}Range", "-") if "effect_range" in columns else None
    )
    item_dict["effect_timer"] = (
        item.get_default(f"{effect}Timer", "-") if "effect_timer" in columns else None
    )
    item_dict["sensor_range"] = (
        item.get_default("SensorRange", "-") if "sensor_range" in columns else None
    )
    item_dict["part_type"] = (
        Translate.get("Tooltip_weapon_" + item.part_type)
        if "part_type" in columns
        else None
    )
    item_dict["weight_mod"] = (
        (item.weight_modifier or "-") if "weight_mod" in columns else None
    )
    item_dict["aiming_time"] = (
        (item.aiming_time_modifier or "-") if "aiming_time" in columns else None
    )
    item_dict["function"] = get_function(item) if "function" in columns else None
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    item_dict["notes"] = notes if notes else None

    return item_dict


def find_table_type(item_id):
    global all_item_data

    item = Item(item_id)
    table_type = None

    if item.item_type == "weapon":
        skill = item.categories
        if skill:
            # Melee
            # Remove "Improvised" from list if more than 1
            if "Improvised" in skill and len(skill) > 1:
                skill = [cat for cat in skill if cat != "Improvised"]
                if len(skill) > 1:
                    echo.write(f"WARNING: More than 1 skill ({','.join(skill)})")
            table_type = skill[0]
        elif item.subcategory == "Firearm":
            # Firearm
            table_type = "handgun"
            if item.requires_equipped_both_hands:
                table_type = "rifle"
                if int(item.projectile_count) > 1:
                    table_type = "shotgun"
        elif item.raw_display_category == "Explosives":
            # Explosives
            table_type = "explosive"
    elif item.item_type == "weaponpart":
        # Weapon parts
        table_type = "weapon_part"
    elif item.item_id in box_types:
        # Ammo (box & carton)
        table_type = box_types[item.item_id].get("type")
    elif item.tags:
        tags = item.tags
        # Ammo (rounds)
        if any(tag.lower() == "ammo" for tag in tags):
            table_type = "round"
        elif any(tag.lower() in {"pistolmagazine", "riflemagazine"} for tag in tags):
            # Magazine
            table_type = "magazine"

    if table_type:
        all_item_data[item.item_id] = {"TableType": table_type}


def find_items():
    """Finds all weapon related items and gets their table type."""
    global all_item_data
    for item_id in Item.all():
        find_table_type(item_id)


def find_boxes():
    global box_types

    AMMO_RECIPES = {
        "OpenBoxOfShotgunShells": "box",
        "OpenBoxOfBullets50": "box",
        "OpenBoxOfBullets20": "box",
        "OpenCartonOfBullets": "carton",
    }

    for recipe_id in AMMO_RECIPES:
        recipe = CraftRecipe(recipe_id)
        output = recipe.outputs[0]

        mapper = output.mapper
        count = output.count
        items = output.items

        if mapper == "ammoTypes":
            item_mappers = recipe.item_mappers.get(mapper, {})
            for key, value in item_mappers.items():
                box_types[value] = {
                    "type": AMMO_RECIPES.get(recipe_id),
                    "contents": key,
                    "quantity": count,
                }

        elif items:
            box_types[recipe.inputs[0].items[0]] = {
                "type": AMMO_RECIPES.get(recipe_id),
                "contents": items[0],
                "quantity": count,
            }


def main():
    global table_map
    global table_type_map
    Language.get()

    table_map, column_headings, table_type_map = table_helper.get_table_data(
        TABLE_PATH, "type_map"
    )
    find_boxes()

    with tqdm(
        total=0,
        desc="Preparing items",
        bar_format=PBAR_FORMAT,
        unit=" items",
        leave=False,
    ) as pbar:
        find_items()

        pbar.total = len(all_item_data)
        pbar.desc = "Generating tables"
        pbar.refresh()

        generated_data = {}

        for item_id in all_item_data:
            item_data = all_item_data.get(item_id, {})
            table_type = item_data.get("TableType")
            pbar.set_postfix_str(f"Generating: {table_type} ({item_id[:30]})")
            if table_type is not None:
                new_item = generate_data(item_id, table_type)

                note = new_item.pop("notes", None)

                if table_type not in generated_data:
                    generated_data[table_type] = (
                        [{"notes": [note]}] if note else [{"notes": []}]
                    )
                else:
                    if note:
                        if (
                            generated_data[table_type]
                            and "notes" in generated_data[table_type][0]
                        ):
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
        table_helper.create_tables(
            "weapon_item_list",
            generated_data,
            columns=column_headings,
            table_map=mapped_table,
            suppress=True,
            bot_flag_type="weapon_item_list",
            combine_tables=False,
        )


if __name__ == "__main__":
    main()
