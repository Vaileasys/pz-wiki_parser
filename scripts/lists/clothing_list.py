import os
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core import utility, translate
from scripts.core.constants import PBAR_FORMAT
from scripts.lists import hotbar_slots

# Used for getting table values
TABLE_DICT = {
    "generic": ('icon', 'name', 'weight', 'body_location', 'item_id'),
    "normal": ('icon', 'name', 'weight', 'body_location', 'attack_speed', 'body_part', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'fabric', 'have_holes', 'item_id',),
    "armor": ('icon', 'name', 'weight', 'body_location', 'move_speed', 'attack_speed', 'body_part', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'have_holes', 'condition_max', 'condition_lower_chance', 'condition_loss', 'item_id',),
    "back": ('icon', 'name', 'weight', 'body_location', 'extra_slots', 'attack_speed', 'body_part', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'fabric', 'item_id',),
    "torso": ('icon', 'name', 'weight', 'body_location', 'move_speed', 'attack_speed', 'body_part', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'fabric', 'have_holes', 'item_id',),
    "legs": ('icon', 'name', 'weight', 'body_location', 'move_speed', 'attack_speed', 'body_part', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'fabric', 'have_holes', 'item_id',),
    "eyes": ('icon', 'name', 'weight', 'body_location', 'fall_chance', 'body_part', 'scratch_def', 'item_id',),
    "head": ('icon', 'name', 'weight', 'body_location', 'fall_chance', 'attack_speed', 'body_part', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'fabric', 'have_holes', 'item_id',),
    "shoes": ('icon', 'name', 'weight', 'body_location', 'stomp_power', 'move_speed', 'body_part', 'bite_def', 'scratch_def', 'insulation', 'wind_def', 'water_def', 'condition_max', 'condition_lower_chance', 'item_id',),
    "belt": ('icon', 'name', 'weight', 'body_location', 'extra_slots', 'move_speed', 'attack_speed', 'body_part', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'fabric', 'item_id',),
    "wrist": ('icon', 'name', 'weight', 'body_location', 'display_time', 'sound_radius', 'item_id'),
    "all": ('icon', 'name', 'weight', 'body_location', 'display_time', 'sound_radius', 'extra_slots', 'fall_chance', 'stomp_power', 'move_speed', 'attack_speed', 'body_part', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'fabric', 'have_holes', 'condition_max', 'condition_lower_chance', 'condition_loss', 'item_id',),
}

# Map table values with their headings
COLUMNS_DICT = {
    "icon": "! Icon",
    "name": "! Name",
    "weight": "! [[File:Status_HeavyLoad_32.png|32px|link=|Encumbrance]]",
    "body_location": "! [[File:UI_BodyLocation.png|32px|link=|Body location]]",
    "display_time": "! [[File:AlarmClock.png|28px|link=|Displays time]]",
    "sound_radius": "! [[File:UI_Noise.png|28px|link=|Sound radius]]",
#    "extra_slots": "! [[File:Image.png|32px|link=|Hotbar slots]]",
    "extra_slots": "! Hotbar slots",
#    "fall_chance": "! [[File:Image.png|32px|link=|Fall chance]]",
    "fall_chance": "! Fall chance",
    "stomp_power": "! [[File:UI_Stomp.png|32px|link=|Stomp power]]",
    "move_speed": "! [[File:UI_Speed.png|link=|Movement speed]]",
    "attack_speed": "! [[File:UI_AttackSpeed.png|link=|Attack speed]]",
    "body_part": "! [[File:UI_BodyPart.png|32px|link=|Body parts protected]]",
    "bite_def": "! [[File:UI_Protection_Bite.png|link=|Bite defense]]",
    "scratch_def": "! [[File:UI_Protection_Scratch.png|link=|Scratch defense]]",
    "bullet_def": "! [[File:UI_Protection_Bullet.png|link=|Bullet defense]]",
    "neck_def": "! [[File:UI_Protection_Neck.png|32px|link=|Neck protection]]",
    "insulation": "! [[File:UI_Protection_Heat.png|link=|Insulation]]",
    "wind_def": "! [[File:UI_Protection_Wind.png|link=|Wind resistance]]",
    "water_def": "! [[File:UI_Protection_Wet.png|link=|Water resistance]]",
    "fabric": "! [[File:SewingBox.png|link=|Fabric type]]",
    "have_holes": "! [[File:UI_Holes.png|link=|Can get holes]]",
    "condition_max": "! [[File:UI_Condition_Max.png|link=|Max condition]]",
    "condition_lower_chance": "! [[File:UI_Condition_Chance.png|link=|Condition lower chance]]",
    "condition_loss": "! [[File:UI_Condition_Sub.png|link=|Condition loss]]",
    "item_id": "! Item ID",
}

# Table/section based on body_location
BODY_LOCATION_DICT = {
    "Armor": {
        "body_location": {'Calf_Left', 'Calf_Left_Texture', 'Calf_Right', 'Calf_Right_Texture', 'ShoulderpadLeft', 'ShoulderpadRight', 'Thigh_Right', 'Thigh_Left', 'Cuirass', 'Gorget', 'TorsoExtraVestBullet', 'ForeArm_Right', 'ForeArm_Left', 'Elbow_Right', 'Elbow_Left', 'ShoulderpadLeft', 'ShoulderpadRight', 'SportShoulderpad', 'SportShoulderpadOnTop', 'LeftArm', 'RightArm', 'Knee_Right', 'Knee_Left', 'Codpiece'},
        "table": 'armor',
    },
    "Long underwear": {
        "body_location": ('Legs1', 'Torso1Legs1'),
        "table": 'torso',
    },
    "Tank tops": {
        "body_location": ('TankTop',),
        "table": 'torso',
    },
    "T-shirts": {
        "body_location": ('Tshirt',),
        "table": 'torso',
    },
    "Short sleeve shirts": {
        "body_location": ('ShortSleeveShirt',),
        "table": 'torso',
    },
    "Shirts": {
        "body_location": ('Shirt',),
        "table": 'torso',
    },
    "Sweaters": {
        "body_location": ('Sweater', 'SweaterHat'),
        "table": 'torso',
    },
    "Jackets": {
        "body_location": ('Jacket', 'Jacket_Bulky', 'JacketHat_Bulky', 'Jersey'),
        "table": 'torso',
    },
    "Suit jackets": {
        "body_location": ('JacketSuit', 'Jacket_Down', 'JacketHat'),
        "table": 'torso',
    },
    "Full tops": {
        "body_location": ('BathRobe', 'FullTop'),
        "table": 'torso',
    },
    "Outer torso": {
        "body_location": ('TorsoExtra', 'TorsoExtraVest', 'VestTexture'),
        "table": 'torso',
    },
    "Pants": {
        "body_location": ('Pants', 'ShortPants'),
        "table": 'legs',
    },
    "Skirts and shorts": {
        "body_location": ('Skirt', 'ShortsShort', 'LongSkirt'),
        "table": 'legs',
    },
    "Dresses": {
        "body_location": ('Dress', 'LongDress'),
        "table": 'torso',
    },
    "Boilersuits": {
        "body_location": ('Boilersuit', 'PantsExtra',),
        "table": 'torso',
    },
    "Full suits": {
        "body_location": ('FullSuitHead', 'FullSuit'),
        "table": 'torso',
    },
    "Socks": {
        "body_location": ('Socks',),
        "table": 'legs',
    },
    "Shoes": {
        "body_location": ('Shoes',),
        "table": 'shoes',
    },
    "Underwear": {
        "body_location": ('Underwear', 'Codpiece'),
        "table": 'generic',
    },
    "Underwear top": {
        "body_location": ('UnderwearTop',),
        "table": 'generic',
    },
    "Underwear bottom": {
        "body_location": ('UnderwearBottom',),
        "table": 'legs',
    },
    "Underwear extra 1": {
        "body_location": ('UnderwearExtra1',),
        "table": 'generic',
    },
    "Underwear extra 2": {
        "body_location": ('UnderwearExtra2',),
        "table": 'generic'
    },
    "Tails": {
        "body_location": ('Tail',),
        "table": 'generic',
    },
    "Eyewear": {
        "body_location": ('Eyes', 'LeftEye', 'RightEye'),
        "table": 'eyes',
    },
    "Masks": {
        "body_location": ('Mask', 'MaskEyes', 'MaskFull'),
        "table": 'head',
    },
    "Headwear": {
        "body_location": ('FullHat', 'Hat', 'MaskFull'),
        "table": 'head',
    },
    "Gloves": {
        "body_location": ('Hands', 'HandsLeft', 'HandsRight'),
        "table": 'normal',
    },
    "Belts": {
        "body_location": ('Belt', 'BeltExtra', 'AmmoStrap', 'SCBA', 'SCBAnotank', 'AnkleHolster', 'Webbing', 'ShoulderHolster', 'FannyPackFront', 'FannyPackBack'),
        "table": 'belt',
    },
    "Back": {
        "body_location": ('Back',),
        "table": 'back',
    },
    "Neck": {
        "body_location": ('Neck', 'Scarf',),
        "table": 'head',
    },
    "Necklace": {
        "body_location": ('Necklace',),
        "table": 'generic',
    },
    "Long necklace": {
        "body_location": ('Necklace_Long',),
        "table": 'torso',
    },
    "Nose": {
        "body_location": ('Nose',),
        "table": 'generic',
    },
    "Ears": {
        "body_location": ('Ears', 'EarTop'),
        "table": 'generic',
    },
    "Fingers": {
        "body_location": ('Right_MiddleFinger', 'Left_MiddleFinger', 'Right_RingFinger', 'Left_RingFinger'),
        "table": 'generic',
    },
    "Wrists": {
        "body_location": ('RightWrist', 'LeftWrist'),
        "table": 'wrist',
    },
    "Belly": {
        "body_location": ('BellyButton',),
        "table": 'generic',
    },
    "Other": {
        "body_location": ('Unknown',),
        "table": 'normal',
    }
}

# Map sections to the correct position
SECTION_DICT = {
    'Clothing': {
        'Armor': None,
        'Tank tops': None,
        'T-shirts': None,
        'Short sleeve shirts': None,
        'Shirts': None,
        'Sweaters': None,
        'Jackets': None,
        'Suit jackets': None,
        'Full tops': None,
        'Outer torso': None,
        'Dresses': None,
        'Boilersuits': None,
        'Full suits': None,
        'Pants': None,
        'Skirts and shorts': None,
        'Socks': None,
        'Shoes': None,
        'Underwear': [
            'Underwear', 'Underwear top', 'Underwear bottom', 'Underwear extra 1', 'Underwear extra 2', 'Tails', 'Long underwear'
        ],
        'Other': None,
    },
    'Accessory': {
        'Headwear': None,
        'Eyewear': None,
        'Masks': None,
        'Neck': None,
        'Necklace': None,
        'Long necklace': None,
        'Nose': None,
        'Ears': None,
        'Gloves': None,
        'Wrists': None,
        'Fingers': None,
        'Belts': None,
        'Back': None,
        'Belly': None,
    }
}

# Map fabric types to an item id
FABRIC_TYPE = {
    "Cotton": 'Base.RippedSheets',
    "Denim": 'Base.DenimStrips',
    "Leather": 'Base.LeatherStrips',
}

TABLE_HEADER ='{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"'

hotbar_slot_data = {}

# Combines txt files based on their position in SECTION_DICT
def combine_clothing_files():
    language_code = translate.get_language_code()
    clothing_dir = f'output/{language_code}/item_list/clothing/'
    output_file = f'output/{language_code}/item_list/clothing_list.txt'

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    file_dict = {}

    # Get the file name and its contents
    for file in os.listdir(clothing_dir):
        if file.endswith('.txt'):
            file_name = file[:-4]
            file_path = os.path.join(clothing_dir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_dict[file_name] = f.read()

    # Lookup a the file name in SECTION_DICT and write the section and its contents
    with open(output_file, 'w', encoding='utf-8') as output_f:
        for section, items in SECTION_DICT.items():
            output_f.write(f"==={section}===\n")

            for key, value in items.items():
                # Nested sections
                if isinstance(value, list):
                    output_f.write(f"===={key}====\n")
                    for subkey in value:
                        content = file_dict.get(subkey, None)
                        if content is not None:
                            output_f.write(f"====={subkey}=====\n")
                            output_f.write(f"{content}\n\n")
                        else:
                            print(f"Skipping '{subkey}': No content found.")
                else:
                    content = file_dict.get(key, None)
                    if content is not None:
                        output_f.write(f"===={key}====\n")
                        output_f.write(f"{content}\n\n")
                    else:
                        print(f"Skipping '{key}': No content found.")

    print(f"Combined files written to {output_file}")


# Gets the section and table for a BodyLocation
def get_body_location(body_location):
    for key, value in BODY_LOCATION_DICT.items():
        if body_location in value['body_location']:
            # return body location heading and table header
            return key, value['table']
    
    # Default to 'Other'
    heading = 'Other'
    table = BODY_LOCATION_DICT[heading]['table']
    return heading, table


# Gets the item's properties based on the BodyLocation as defined for its table
def process_item(item_data, item_id):
    body_location = item_data.get("BodyLocation", item_data.get("CanBeEquipped", 'Unknown'))
    heading, table_key = get_body_location(body_location)
    columns = TABLE_DICT.get(table_key, TABLE_DICT["generic"])
    language_code = translate.get_language_code()

    name = item_data.get("DisplayName", 'Unknown')
    page_name = utility.get_page(item_id, name)
    link = utility.format_link(name, page_name)
    icon = utility.get_icon(item_id, True, True, True)
    can_have_holes = item_data.get("CanHaveHoles", "true").lower() == "true"

    item = {}

    if "icon" in columns:
        item["icon"] = icon

    if "name" in columns:
        item["name"] = link

    if "weight" in columns:
        item["weight"] = item_data.get('Weight', '1')

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

    if "sound_radius" in columns:
        item["sound_radius"] = item_data.get("SoundRadius", '-')

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

    if "fall_chance" in columns:
        item["fall_chance"] = utility.convert_to_percentage(item_data.get("ChanceToFall", '-'), True, True)

    if "stomp_power" in columns:
        item["stomp_power"] = utility.convert_to_percentage(item_data.get("StompPower", '-'), True)

    if "move_speed" in columns:
        item["move_speed"] = utility.convert_to_percentage(item_data.get("RunSpeedModifier", '-'), False)

    if "attack_speed" in columns:
        item["attack_speed"] = utility.convert_to_percentage(item_data.get("CombatSpeedModifier", '-'), False)

    body_parts_list = utility.get_body_parts(item_data, True, "-")
    if "body_part" in columns:
        item["body_part"] = '<br>'.join(body_parts_list)

    if "bite_def" in columns:
        item["bite_def"] = utility.convert_to_percentage(item_data.get("BiteDefense", '-'), True, True)

    if "scratch_def" in columns:
        item["scratch_def"] = utility.convert_to_percentage(item_data.get("ScratchDefense", '-'), True, True)

    if "bullet_def" in columns:
        item["bullet_def"] = utility.convert_to_percentage(item_data.get("BulletDefense", '-'), True, True)

    if "neck_def" in columns:
        neck_protection = "-"
        if "Neck" in utility.get_body_parts(item_data, False):
            neck_protection = 1.0 - float(item_data.get("NeckProtectionModifier", 0))
            neck_protection = utility.convert_to_percentage(neck_protection, True)
        item["neck_def"] = neck_protection

    if "insulation" in columns:
        item["insulation"] = utility.convert_to_percentage(item_data.get("Insulation", '-'), True)

    if "wind_def" in columns:
        item["wind_def"] = utility.convert_to_percentage(item_data.get("WindResistance", '-'), True)

    if "water_def" in columns:
        item["water_def"] = utility.convert_to_percentage(item_data.get("WaterResistance", '-'), True)
    
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

    if "condition_max" in columns:
        item["condition_max"] = item_data.get("ConditionMax", '-')

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

    if "item_id" in columns:
        item["item_id"] = f"{{{{ID|{item_id}}}}}"
    
    return heading, item


def get_items():
    blacklist = ("MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_")
    clothing_dict = {}
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
                    heading, item = process_item(item_data, item_id)

                    # add heading to dict if it hasn't been added yet.
                    if heading not in clothing_dict:
                        clothing_dict[heading] = []

                    clothing_dict[heading].append(item)
            pbar.update(1)
        pbar.bar_format = f"Items processed."
    write_items_to_file(clothing_dict)


# write to file
def write_items_to_file(clothing_dict):
    language_code = translate.get_language_code()
    output_dir = f'output/{language_code}/item_list/clothing/'
    os.makedirs(output_dir, exist_ok=True)
    
    for heading, items in clothing_dict.items():
        table_key = BODY_LOCATION_DICT[heading]['table']
        columns = TABLE_DICT.get(table_key, TABLE_DICT["generic"])

        # build the table heading based on values
        table_headings = []
        for col in columns:
            mapped_heading = COLUMNS_DICT.get(col, col)
            table_headings.append(mapped_heading)
        table_headings = "\n".join(table_headings)

        output_path = os.path.join(output_dir, f"{heading}.txt")
        with open(output_path, 'w', encoding='utf-8') as file:
            # write wiki heading and table headings
#            file.write(f"=={heading}==\n")
            file.write(f'<!--BOT_FLAG-start-{heading.replace(" ", "_")}. DO NOT REMOVE-->')
            file.write(f"{TABLE_HEADER}\n")
            file.write(f"{table_headings}\n")

            sorted_items = sorted(items, key=lambda x: x['name'])
            for item in sorted_items:
                row = '\n| '.join([value for key, value in item.items()])
                file.write(f"|-\n| {row}\n")

            file.write("|}")
            file.write(f'<!--BOT_FLAG-end-{heading.replace(" ", "_")}. DO NOT REMOVE-->')


def main():
    global hotbar_slot_data
    hotbar_slot_data = hotbar_slots.get_hotbar_slots()
    get_items()
    while True:
        user_input = input("Want to merge list files? (Y/N)\n> ").lower()
        
        if user_input == "n":
            break
        elif user_input == "y":
            combine_clothing_files()
            break

if __name__ == "__main__":
    main()