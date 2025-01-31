import os
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core import utility, translate
from scripts.core.constants import PBAR_FORMAT

# Used for getting table values
TABLE_DICT = {
    "generic": ('icon', 'name', 'weight', 'body_location', 'item_id'),
    "normal": ('icon', 'name', 'weight', 'body_location', 'body_part', 'fabric', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "back": ('icon', 'name', 'weight', 'body_location', 'body_part', 'extra_slots', 'fabric', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "torso": ('icon', 'name', 'weight', 'body_location', 'body_part', 'have_holes', 'fabric', 'move_speed', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "legs": ('icon', 'name', 'weight', 'body_location', 'body_part', 'fabric', 'move_speed', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "eyes": ('icon', 'name', 'weight', 'body_location', 'body_part', 'fall_chance', 'scratch_def', 'item_id',),
    "head": ('icon', 'name', 'weight', 'body_location', 'body_part', 'fall_chance', 'have_holes', 'fabric', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "shoes": ('icon', 'name', 'weight', 'body_location', 'body_part', 'stomp_power', 'fabric', 'move_speed', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "belt": ('icon', 'name', 'weight', 'body_location', 'body_part', 'extra_slots', 'fabric', 'move_speed', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "wrist": ('icon', 'name', 'weight', 'body_location', 'display_time', 'sound_radius', 'item_id'),
    "all": ('icon', 'name', 'weight', 'body_location', 'body_part', 'display_time', 'sound_radius', 'extra_slots', 'fall_chance', 'stomp_power', 'have_holes', 'fabric', 'move_speed', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
}

# Map table values with their headings
COLUMNS_DICT = {
    "icon": "! Icon",
    "name": "! Name",
    "weight": "! [[File:Status_HeavyLoad.png|32px|link=|Encumbrance]]",
    "body_location": "! [[File:UI_BodyPart.png|32px|link=|Body location]]",
    "body_part": "! [[File:UI_BodyPart.png|32px|link=|Body part(s)]]",
    "display_time": "! [[File:AlarmClock.png|28px|link=|Displays time]]",
    "sound_radius": "! [[File:UI_Noise.png|28px|link=|Sound radius]]",
    "extra_slots": "! Extra slots",
#    "fall_chance": "! [[File:Image.png|32px|link=|Fall chance]]",
    "fall_chance": "! Fall chance",
#    "have_holes": "! [[File:Image.png|32px|link=|Can get holes]]",
    "have_holes": "! Can get holes",
    "fabric": "! [[File:SewingBox.png|link=|Fabric type]]",
    "stomp_power": "! [[File:UI_Stomp.png|32px|link=|Stomp power]]",
    "move_speed": "! [[File:UI_Speed.png|link=|Movement speed]]",
    "attack_speed": "! [[File:UI_AttackSpeed.png|link=|Attack speed]]",
    "bite_def": "! [[File:UI_Protection_Bite.png|link=|Bite defense]]",
    "scratch_def": "! [[File:UI_Protection_Scratch.png|link=|Scratch defense]]",
    "bullet_def": "! [[File:UI_Protection_Bullet.png|link=|Bullet defense]]",
    "neck_def": "! [[File:UI_Protection_Neck.png|32px|link=|Neck protection modifier]]",
    "insulation": "! [[File:UI_Protection_Heat.png|link=|Insulation]]",
    "wind_def": "! [[File:UI_Protection_Wind.png|link=|Wind resistance]]",
    "water_def": "! [[File:UI_Protection_Wet.png|link=|Water resistance]]",
    "item_id": "! Item ID",
}

# Table/section based on body_location
BODY_LOCATION_DICT = {
    "Armor": {
        "body_location": {'Calf_Left', 'Calf_Left_Texture', 'Calf_Right', 'Calf_Right_Texture', 'ShoulderpadLeft', 'ShoulderpadRight', 'Thigh_Right', 'Thigh_Left', 'Cuirass', 'Gorget', 'TorsoExtraVestBullet', 'ForeArm_Right', 'ForeArm_Left', 'Elbow_Right', 'Elbow_Left', 'ShoulderpadLeft', 'ShoulderpadRight', 'SportShoulderpad', 'SportShoulderpadOnTop', 'LeftArm', 'RightArm', 'Knee_Right', 'Knee_Left', 'Codpiece'},
        "table": 'torso',
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

# Taken from 'BloodClothingType.class' init() - updated Build 42.0.2
BODY_PART_DICT = {
    "Apron": ["Torso_Upper", "Torso_Lower", "UpperLeg_L", "UpperLeg_R"],
    "ShirtNoSleeves": ["Torso_Upper", "Torso_Lower", "Back"],
    "JumperNoSleeves": ["Torso_Upper", "Torso_Lower", "Back"],
    "Shirt": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R"],
    "ShirtLongSleeves": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R"],
    "Jumper": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R"],
    "Jacket": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R", "Neck"],
    "LongJacket": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R", "Neck", "Groin", "UpperLeg_L", "UpperLeg_R"],
    "ShortsShort": ["Groin", "UpperLeg_L", "UpperLeg_R"],
    "Trousers": ["Groin", "UpperLeg_L", "UpperLeg_R", "LowerLeg_L", "LowerLeg_R"],
    "Shoes": ["Foot_L", "Foot_R"],
    "FullHelmet": ["Head"],
    "Bag": ["Back"],
    "Hands": ["Hand_L", "Hand_R"],
    "Hand_L": ["Hand_L"],
    "Hand_R": ["Hand_R"],
    "Head": ["Head"],
    "Neck": ["Neck"],
    "Groin": ["Groin"],
    "UpperBody": ["Torso_Upper"],
    "LowerBody": ["Torso_Lower"],
    "LowerLegs": ["LowerLeg_L", "LowerLeg_R"],
    "LowerLeg_L": ["LowerLeg_L"],
    "LowerLeg_R": ["LowerLeg_R"],
    "UpperLegs": ["UpperLeg_L", "UpperLeg_R"],
    "UpperLeg_L": ["UpperLeg_L"],
    "UpperLeg_R": ["UpperLeg_R"],
    "UpperArms": ["UpperArm_L", "UpperArm_R"],
    "UpperArm_L": ["UpperArm_L"],
    "UpperArm_R": ["UpperArm_R"],
    "LowerArms": ["ForeArm_L", "ForeArm_R"],
    "ForeArm_L": ["ForeArm_L"],
    "ForeArm_R": ["ForeArm_R"],
}

# Taken from 'BodyPartType.class' getDisplayName() - updated Build 42.0.2
BODY_PART_TRANSLATIONS = {
    "Hand_L": "Left_Hand",
    "Hand_R": "Right_Hand",
    "ForeArm_L": "Left_Forearm",
    "ForeArm_R": "Right_Forearm",
    "UpperArm_L": "Left_Upper_Arm",
    "UpperArm_R": "Right_Upper_Arm",
    "Torso_Upper": "Upper_Torso",
    "Torso_Lower": "Lower_Torso",
    "Head": "Head",
    "Neck": "Neck",
    "Groin": "Groin",
    "UpperLeg_L": "Left_Thigh",
    "UpperLeg_R": "Right_Thigh",
    "LowerLeg_L": "Left_Shin",
    "LowerLeg_R": "Right_Shin",
    "Foot_L": "Left_Foot",
    "Foot_R": "Right_Foot",
    "Back": "Back",
    "Unknown": "Unknown_Body_Part"
}

# Map fabric types to an item id
FABRIC_TYPE = {
    "Cotton": 'Base.RippedSheets',
    "Denim": 'Base.DenimStrips',
    "Leather": 'Base.LeatherStrips',
}

TABLE_HEADER ='{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"'


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

    if "body_part" in columns:
        body_parts_list = utility.get_body_parts(item_data, True, "-")
        item["body_part"] = '<br>'.join(body_parts_list)

    if "display_time" in columns:
        if item_data.get("Type") == 'AlarmClockClothing':
            item["display_time"] = 'True'
        else:
            item["display_time"] = '-'

    if "sound_radius" in columns:
        item["sound_radius"] = item_data.get("SoundRadius", '-')

    if "extra_slots" in columns:
        extra_slots = item_data.get("AttachmentsProvided", ['-'])
        if isinstance(extra_slots, list):
            extra_slots = "<br>".join(extra_slots)
        else:
            extra_slots = str(extra_slots)
        item["extra_slots"] = extra_slots

    if "fall_chance" in columns:
        item["fall_chance"] = utility.convert_to_percentage(item_data.get("ChanceToFall", '-'), True, True)

    if "stomp_power" in columns:
        item["stomp_power"] = utility.convert_to_percentage(item_data.get("StompPower", '-'), True)

    if "have_holes" in columns:
        can_have_holes = item_data.get("CanHaveHoles", '-').lower()
        if can_have_holes == 'true':
            item["have_holes"] = "[[File:UI_Tick.png|link=|Can get holes]]"
        elif can_have_holes == 'false':
            item["have_holes"] = "[[File:UI_Cross.png|link=|Cannot get holes]]"
        else:
            item["have_holes"] = '-'


    if "fabric" in columns:
        fabric_id = FABRIC_TYPE.get(item_data.get("FabricType"))
        if fabric_id is None:
            fabric = "-"
        else:
            fabric = utility.get_icon(fabric_id, True)
        item["fabric"] = fabric

    if "move_speed" in columns:
        item["move_speed"] = utility.convert_to_percentage(item_data.get("RunSpeedModifier", '-'), False)

    if "attack_speed" in columns:
        item["attack_speed"] = utility.convert_to_percentage(item_data.get("CombatSpeedModifier", '-'), False)

    if "bite_def" in columns:
        item["bite_def"] = utility.convert_to_percentage(item_data.get("BiteDefense", '-'), True, True)

    if "scratch_def" in columns:
        item["scratch_def"] = utility.convert_to_percentage(item_data.get("ScratchDefense", '-'), True, True)

    if "bullet_def" in columns:
        item["bullet_def"] = utility.convert_to_percentage(item_data.get("BulletDefense", '-'), True, True)

    if "neck_def" in columns:
        item["neck_def"] = utility.convert_to_percentage(item_data.get("NeckProtectionModifier", '-'), True)

    if "insulation" in columns:
        item["insulation"] = utility.convert_to_percentage(item_data.get("Insulation", '-'), True)

    if "wind_def" in columns:
        item["wind_def"] = utility.convert_to_percentage(item_data.get("WindResistance", '-'), True)

    if "water_def" in columns:
        item["water_def"] = utility.convert_to_percentage(item_data.get("WaterResistance", '-'), True)

    if "item_id" in columns:
        item["item_id"] = f"{{{{ID|{item_id}}}}}"
    
    return heading, item


def get_items():
    blacklist = ("MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_")
    clothing_dict = {}
    parsed_item_data = item_parser.get_item_data()

    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=constants.PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f"Processing: {item_data.get("Type", "Unknown")} ({item_id[:30]})")
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
            file.write(f"<!--BOT_FLAG-start-{heading.replace(" ", "_")}. DO NOT REMOVE-->")
            file.write(f"{TABLE_HEADER}\n")
            file.write(f"{table_headings}\n")

            sorted_items = sorted(items, key=lambda x: x['name'])
            for item in sorted_items:
                row = '\n| '.join([value for key, value in item.items()])
                file.write(f"|-\n| {row}\n")

            file.write("|}")
            file.write(f"<!--BOT_FLAG-end-{heading.replace(" ", "_")}. DO NOT REMOVE-->")


def main():
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