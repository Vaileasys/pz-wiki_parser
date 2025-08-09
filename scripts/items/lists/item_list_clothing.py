import os
from tqdm import tqdm
from scripts.objects.item import Item
from scripts.objects.attachment import HotbarSlot
from scripts.core.constants import PBAR_FORMAT, TABLES_DIR
from scripts.utils import table_helper
from scripts.utils.util import convert_int, convert_percentage, tick, cross

TABLE_PATH = os.path.join(TABLES_DIR, "clothing_table.json")

table_types = {}
body_location_map = {}


def get_body_location(body_location: str):
    """Gets the section and table for a BodyLocation"""
    for key, value in body_location_map.items():
        if body_location in value['body_location']:
            # return body location heading and table header
            return key, value['table']
    
    # Default to 'Other'
    heading = 'Other'
    table = body_location_map[heading]['table']
    return heading, table


def generate_data(item: Item):
    """Gets the item's properties based on the BodyLocation as defined for its table"""
    notes = None
    body_location = body_location = item.body_location or item.can_be_equipped
    heading, table_key = get_body_location(body_location.location_id)
    columns = table_types.get(table_key, table_types["generic"])

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None    
    item_dict["weight"] = convert_int(item.weight) if "weight" in columns else None

    if "body_location" in columns:
        body_location = item.body_location or item.can_be_equipped
        item_dict["body_location"] = body_location.wiki_link if body_location else '-'

    if "display_time" in columns:
        if item.type == 'AlarmClockClothing':
            item_dict["display_time"] = 'True'
        else:
            item_dict["display_time"] = '-'

    item_dict["sound_radius"] = (item.sound_radius or "-") if "sound_radius" in columns else None

    if "extra_slots" in columns:
        if item.attachments_provided:
            hotbar_attachments = []

            for slot_id in item.attachments_provided:
                slot = HotbarSlot(slot_id)
                hotbar_attachments.append(slot.wiki_link)
            attachments_provided = "<br>".join(hotbar_attachments)
        else:
            attachments_provided = '-'
        item_dict["extra_slots"] = attachments_provided
    
    item_dict["fall_chance"] = convert_percentage(item.chance_to_fall, True, True, default='-') if "fall_chance" in columns else None
    item_dict["stomp_power"] = convert_percentage(item.stomp_power, True, default='-') if "stomp_power" in columns else None
    item_dict["move_speed"] = convert_percentage(item.run_speed_modifier, False, default='-') if "move_speed" in columns else None
    item_dict["attack_speed"] = convert_percentage(item.combat_speed_modifier, False, default='-') if "attack_speed" in columns else None
    item_dict["body_part"] = '<br>'.join(item.get_body_parts(default="-")) if "body_part" in columns else None
    item_dict["bite_def"] = convert_percentage(item.bite_defense, True, True, default='-') if "bite_def" in columns else None
    item_dict["scratch_def"] = convert_percentage(item.scratch_defense, True, True, default='-') if "scratch_def" in columns else None
    item_dict["bullet_def"] = convert_percentage(item.bullet_defense, True, True, default='-') if "bullet_def" in columns else None

    if "neck_def" in columns:
        neck_protection = "-"
        if item.blood_location and "Neck" in item.get_body_parts(do_link=False):
            modifier = item.neck_protection_modifier
            neck_protection = convert_percentage(modifier, True)
        item_dict["neck_def"] = neck_protection

    item_dict["insulation"] = convert_percentage(item.insulation, True, default='-') if "insulation" in columns else None
    item_dict["wind_def"] = convert_percentage(item.wind_resistance, True, default='-') if "wind_def" in columns else None
    item_dict["water_def"] = convert_percentage(item.water_resistance, True, default='-') if "water_def" in columns else None
    
    if "fabric" in columns:
        fabric_id = item.get_fabric()
        if fabric_id:
            fabric = Item(fabric_id).icon
        else:
            fabric = "-"
        item_dict["fabric"] = fabric

    if "have_holes" in columns:
        if item.body_location.location_id == "Shoes":
            have_holes = '-'
        elif item.can_have_holes:
            have_holes = tick(text="Can get holes")
        else:
            have_holes = cross(text="Cannot get holes")
        item_dict["have_holes"] = have_holes

    item_dict["condition_max"] = item.condition_max if "condition_max" in columns else None

    if "condition_lower_chance" in columns:
        is_chance_based = not item.can_have_holes or item.body_location.location_id == "Shoes"

        if is_chance_based:
            lower_chance = convert_percentage(1 / int(item.condition_lower_chance_one_in), True)
        else:
            lower_chance = "-"
        if not item.body_location.location_id:
            notes = "Note: Clothing that can get holes only lose condition when a hole is added, which depends on the body part hit and whether it already has a hole. There is no fixed 'chance' like in other items."
        item_dict["condition_lower_chance"] = lower_chance

    if "condition_loss" in columns:
        if item.can_have_holes and len(item.get_body_parts()) > 0:
            per_hole_loss = int(max(1, item.condition_max / len(item.get_body_parts())))
            condition_loss = f"-{per_hole_loss}"
        else:
            condition_loss = "-1"
        item_dict["condition_loss"] = condition_loss

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    item_dict["notes"] = notes if notes else None

    return heading, item_dict


def find_items():
    blacklist = ("MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_")
    clothing_items = {}

    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id in Item.all():
            item = Item(item_id)
            pbar.set_postfix_str(f'Processing: {item.type} ({item_id[:30]})')
            if item.has_category("clothing"):
                # filter out blacklisted items and 'Reverse' variants
                if not item.id_type.startswith(blacklist) and not item.id_type.endswith("_Reverse"):
                    if item.obsolete:
                        continue
                    table_type, new_item = generate_data(item)

                    note = new_item.pop("notes", None)

                    # add heading to dict if it hasn't been added yet.
                    if table_type not in clothing_items:
                        clothing_items[table_type] = [{"notes": [note]}] if note else [{"notes": []}]
                    else:
                        if note:
                            if clothing_items[table_type] and "notes" in clothing_items[table_type][0]:
                                if note not in clothing_items[table_type][0]["notes"]:
                                    clothing_items[table_type][0]["notes"].append(note)
                            else:
                                clothing_items[table_type].insert(0, {"notes": [note]})

                    clothing_items[table_type].append(new_item)
            pbar.update(1)

    return clothing_items


def main():
    global table_types
    global body_location_map
    table_types, column_headings, body_location_map = table_helper.get_table_data(TABLE_PATH, "body_locations")
    
    clothing_items = find_items()

    table_map = {
        key: table_types[value["table"]]
        for key, value in body_location_map.items()
    }
    table_helper.create_tables("clothing_item_list", clothing_items, columns=column_headings, table_map=table_map, suppress=True, bot_flag_type="clothing_item_list", combine_tables=False)


if __name__ == "__main__":
    main()