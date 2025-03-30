from tqdm import tqdm
from scripts.core import translate
from scripts.utils import utility, util, table_helper
from scripts.parser import item_parser, recipe_parser, script_parser
from scripts.core.constants import OUTPUT_PATH, RESOURCE_PATH, PBAR_FORMAT

language_code = "en"
OUTPUT_DIR = f'{OUTPUT_PATH}/{language_code}/item_list/ammo/'
TABLE_PATH = f"{RESOURCE_PATH}/tables/weapon_table.json"

box_types = {}
all_items = {}
table_map = {}
table_type_map = {}

def check_fixing(item_id):
    """ Check if it can be fixed """
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

#    utility.save_cache(item_data, f"{item_id}_data.json")

    return item_data


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
    item["name"] = utility.format_link(item_name, utility.get_page(item_id, item_name)) if "name" in columns else None
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
        item["equipped"] = translate.get_wiki_translation(equipped)
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
    item["hit_chance"] = item_data.get('HitChance', '-') + '%' if "hit_chance" in columns else None
    item["hit_chance_mod"] = '+' + item_data.get('AimingPerkHitChanceModifier', '-') + '%' if "hit_chance_mod" in columns else None
    if "crit_chance" in columns:
        item["crit_chance"] = item_data.get("CriticalChance") + "%" if item_data.get("CriticalChance") is not None else "-"
    if "crit_multiplier" in columns:
        item["crit_multiplier"] = item_data.get("CritDmgMultiplier") + "×" if item_data.get("CritDmgMultiplier") is not None else "-"
    if "crit_chance_mod" in columns:
        item["crit_chance_mod"] = "+" + item_data.get("AimingPerkCritModifier") + "%" if item_data.get("AimingPerkCritModifier") is not None else "-"
    item["sound_radius"] = item_data.get('SoundRadius', '-') if "sound_radius" in columns else None
    item["knockback"] = item_data.get('PushBackMod', '-') if "knockback" in columns else None
    if "condition_max" in columns or "condition_lower_chance" in columns:
        condition_max = item_data.get("ConditionMax", '0')
        condition_lower_chance = item_data.get("ConditionLowerChanceOneIn", '0')
        item["condition_max"] = condition_max if "condition_max" in columns else None
        item["condition_lower_chance"] = condition_lower_chance if "condition_max" in columns else None
        item["condition_average"] = str(int(condition_max) * int(condition_lower_chance)) if "condition_max" in columns and "condition_lower_chance" in columns else None
    item["repairable"] = translate.get_wiki_translation(check_fixing(item_id)) if "repairable" in columns else None
    if "magazine" in columns:
        item["magazine"] = utility.get_icon(item_data.get("Magazine"), True, True, True) if item_data.get("Magazine") else "-"
    if "weapon" in columns:
        if table_type == "magazine":
            item["weapon"] = utility.get_icon(item_data.get("GunType"), True, True, True) if item_data.get("GunType") is not None else "-"
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
    item["item_id"] = item_id if "item_id" in columns else None

    # Remove any values that are None
    item = {k: v for k, v in item.items() if v is not None}
    # temp for testing
#    for key in item:
#        item[key] = f"{key}: {item[key]}"

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
                    util.echo(f"WARNING: More than 1 skill ({','.join(skill)})")
            table_type = skill[0]
        elif item_data.get("SubCategory") == "Firearm":
            # Firearm
            table_type = "handgun"
            if item_data.get("RequiresEquippedBothHands", "").lower() == "true":
                table_type = "rifle"
                if int(item_data.get("ProjectileCount")) > 1:
                    table_type = "shotgun"
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

    recipes_data = recipe_parser.get_recipe_data()["recipes"]
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
    
#    utility.save_cache(box_types, "box_types.json")


def main():
    global language_code
    global table_map
    global all_items
    global table_type_map
    language_code = translate.get_language_code()
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