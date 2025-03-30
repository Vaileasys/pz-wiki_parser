from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core import translate
from scripts.core.constants import PBAR_FORMAT, RESOURCE_PATH
from scripts.lists import hotbar_slots
from scripts.utils import utility, table_helper

TABLE_PATH = f"{RESOURCE_PATH}/tables/clothing_table.json"

hotbar_slot_data = {}
table_types = {}
body_location_map = {}


# Map fabric types to an item id
FABRIC_TYPE = {
    "Cotton": 'Base.RippedSheets',
    "Denim": 'Base.DenimStrips',
    "Leather": 'Base.LeatherStrips',
}


def get_body_location(body_location):
    """Gets the section and table for a BodyLocation"""
    for key, value in body_location_map.items():
        if body_location in value['body_location']:
            # return body location heading and table header
            return key, value['table']
    
    # Default to 'Other'
    heading = 'Other'
    table = body_location_map[heading]['table']
    return heading, table


def generate_data(item_data, item_id):
    """Gets the item's properties based on the BodyLocation as defined for its table"""
    body_location = item_data.get("BodyLocation", item_data.get("CanBeEquipped", 'Unknown'))
    heading, table_key = get_body_location(body_location)
    columns = table_types.get(table_key, table_types["generic"])
    language_code = translate.get_language_code()

    item_name = item_data.get("DisplayName", 'Unknown')
    page_name = utility.get_page(item_id, item_name)
    link = utility.format_link(item_name, page_name)
    icon = utility.get_icon(item_id, True, True, True)
    can_have_holes = item_data.get("CanHaveHoles", "true").lower() == "true"
    body_parts_list = utility.get_body_parts(item_data, True, "-")

    item = {}

    item["icon"] = icon if "icon" in columns else None
    item["name"] = link if "name" in columns else None    
    item["weight"] = item_data.get('Weight', '1') if "weight" in columns else None

    if "body_location" in columns:
        
        if language_code == 'en':
            item["body_location"] = f"[[BodyLocation#{body_location}|{body_location}]]"
        else:
            item["body_location"] = f"[[BodyLocation/{language_code}#{body_location}|{body_location}]]"

    if "display_time" in columns:
        if item_data.get("Type") == 'AlarmClockClothing':
            item["display_time"] = 'True'
        else:
            item["display_time"] = '-'

    item["sound_radius"] = item_data.get("SoundRadius", '-') if "sound_radius" in columns else None

    if "extra_slots" in columns:
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
            attachments_provided = '-'
        item["extra_slots"] = attachments_provided
    
    item["fall_chance"] = utility.convert_to_percentage(item_data.get("ChanceToFall", '-'), True, True) if "fall_chance" in columns else None
    item["stomp_power"] = utility.convert_to_percentage(item_data.get("StompPower", '-'), True) if "stomp_power" in columns else None
    item["move_speed"] = utility.convert_to_percentage(item_data.get("RunSpeedModifier", '-'), False) if "move_speed" in columns else None
    item["attack_speed"] = utility.convert_to_percentage(item_data.get("CombatSpeedModifier", '-'), False) if "attack_speed" in columns else None
    item["body_part"] = '<br>'.join(body_parts_list) if "body_part" in columns else None
    item["bite_def"] = utility.convert_to_percentage(item_data.get("BiteDefense", '-'), True, True) if "bite_def" in columns else None
    item["scratch_def"] = utility.convert_to_percentage(item_data.get("ScratchDefense", '-'), True, True) if "scratch_def" in columns else None
    item["bullet_def"] = utility.convert_to_percentage(item_data.get("BulletDefense", '-'), True, True) if "bullet_def" in columns else None

    if "neck_def" in columns:
        neck_protection = "-"
        if "Neck" in utility.get_body_parts(item_data, False):
            neck_protection = 1.0 - float(item_data.get("NeckProtectionModifier", 0))
            neck_protection = utility.convert_to_percentage(neck_protection, True)
        item["neck_def"] = neck_protection

    item["insulation"] = utility.convert_to_percentage(item_data.get("Insulation", '-'), True) if "insulation" in columns else None
    item["wind_def"] = utility.convert_to_percentage(item_data.get("WindResistance", '-'), True) if "wind_def" in columns else None
    item["water_def"] = utility.convert_to_percentage(item_data.get("WaterResistance", '-'), True) if "water_def" in columns else None
    
    if "fabric" in columns:
        fabric_id = FABRIC_TYPE.get(item_data.get("FabricType"))
        if fabric_id is None:
            fabric = "-"
        else:
            fabric = utility.get_icon(fabric_id, True)
        item["fabric"] = fabric

    if "have_holes" in columns:
        if not can_have_holes:
            item["have_holes"] = "[[File:UI_Cross.png|link=|Cannot get holes]]"
        else:
            item["have_holes"] = "[[File:UI_Tick.png|link=|Can get holes]]"

    item["condition_max"] = item_data.get("ConditionMax", '-') if "condition_max" in columns else None

    if "condition_lower_chance" in columns:
        lower_chance = item_data.get("ConditionLowerChanceOneIn", '-')
        # ConditionLowerChance does nothing if it's not Shoes and CanHaveHoles = True
        if item_data.get("BodyLocation") != "Shoes" and lower_chance != "-":
            if can_have_holes:
                lower_chance = "-"
        if lower_chance != "-":
            lower_chance = utility.convert_to_percentage(1 / int(lower_chance), True)

        item["condition_lower_chance"] = lower_chance

    if "condition_loss" in columns:
        condition_max = item_data.get("ConditionMax")
        if condition_max is not None:
            if can_have_holes:
                condition_loss = "-" + str(int(max(1, int(condition_max) / len(body_parts_list))))
            else:
                condition_loss = "-1"
        else:
            condition_loss = "-"
        item["condition_loss"] = condition_loss

    item["item_id"] = item_id if "item_id" in columns else None

    # Remove any values that are None
    item = {k: v for k, v in item.items() if v is not None}

    # Ensure column order is correct
    item = {key: item[key] for key in columns if key in item}

    # Add item_name for sorting
    item["item_name"] = item_name

    return heading, item


def find_items():
    blacklist = ("MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_")
    clothing_items = {}
    parsed_item_data = item_parser.get_item_data()

    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f'Processing: {item_data.get("Type", "Unknown")} ({item_id[:30]})')
            if item_data.get("Type") in ("Clothing", "AlarmClockClothing") or 'CanBeEquipped' in item_data:
                # filter out blacklisted items and 'Reverse' variants
                module, item_name = item_id.split('.')
                if not item_name.startswith(blacklist) and not item_name.endswith("_Reverse"):
                    if "OBSOLETE" in item_data:
                        continue
                    heading, item = generate_data(item_data, item_id)

                    # add heading to dict if it hasn't been added yet.
                    if heading not in clothing_items:
                        clothing_items[heading] = []

                    clothing_items[heading].append(item)
            pbar.update(1)
        pbar.bar_format = f"Items processed."

    return clothing_items


def main():
    global hotbar_slot_data
    global table_types
    global body_location_map
    table_types, column_headings, body_location_map = table_helper.get_table_data(TABLE_PATH, "body_locations")
    
    hotbar_slot_data = hotbar_slots.get_hotbar_slots()
    clothing_items = find_items()

#    utility.save_cache(clothing_items, "clothing_data.json")
    table_map = {
        key: table_types[value["table"]]
        for key, value in body_location_map.items()
    }
    table_helper.create_tables("clothing", clothing_items, columns=column_headings, table_map=table_map)


if __name__ == "__main__":
    main()