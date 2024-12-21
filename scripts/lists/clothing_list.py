import os
from scripts.parser import item_parser
from scripts.core import utility, translate

# used for getting table values
table_dict = {
    "generic": ('icon', 'name', 'weight', 'body_location', 'item_id'),
    "normal": ('icon', 'name', 'weight', 'body_location', 'fabric', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "torso": ('icon', 'name', 'weight', 'body_location', 'fabric', 'move_speed', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "legs": ('icon', 'name', 'weight', 'body_location', 'fabric', 'move_speed', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "eyes": ('icon', 'name', 'weight', 'body_location', 'fall_chance', 'have_holes', 'item_id',),
    "head": ('icon', 'name', 'weight', 'body_location', 'fall_chance', 'have_holes', 'fabric', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'neck_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "shoes": ('icon', 'name', 'weight', 'body_location', 'stomp_power', 'fabric', 'move_speed', 'attack_speed', 'bite_def', 'scratch_def', 'bullet_def', 'insulation', 'wind_def', 'water_def', 'item_id',),
    "belt": ('icon', 'name', 'weight', 'body_location', 'extra_slots', 'item_id',),
    "wrist": ('icon', 'name', 'weight', 'body_location', 'display_time', 'sound_radius', 'item_id')
}

# map table values with their headings
columns_dict = {
    "icon": "! Icon",
    "name": "! Name",
    "weight": "! [[File:Moodle_Icon_HeavyLoad.png|link=|Encumbrance]]",
    "body_location": "! [[File:UI BodyPart.png|32px|link=|Body location]]",
    "extra_slots": "! Extra slots",
    "fall_chance": "! [[File:Image.png|32px|link=|Fall chance]]",
    "have_holes": "! [[File:Image.png|32px|link=|Can have holes]]",
    "fabric": "! [[File:SewingBox.png|link=|Fabric type]]",
    "stomp_power": "! [[File:UI Stomp.png|32px|link=|Stomp power]]",
    "move_speed": "! [[File:UI Speed.png|link=|Movement speed]]",
    "attack_speed": "! [[File:UI AttackSpeed.png|link=|Attack speed]]",
    "bite_def": "! [[File:UI Bite Protect.png|link=|Bite defense]]",
    "scratch_def": "! [[File:UI Scratch Protect.png|link=|Scratch defense]]",
    "bullet_def": "! [[File:UI Bullet Protect.png|link=|Bullet defense]]",
    "neck_def": "! [[File:UI Neck Protect.png|32px|link=|Neck protection modifier]]",
    "insulation": "! [[File:UI Heat Protect.png|link=|Insulation]]",
    "wind_def": "! [[File:UI Wind Protect.png|link=|Wind resistance]]",
    "water_def": "! [[File:UI Wet Protect.png|link=|Water resistance]]",
    "display_time": "! [[File:AlarmClock.png|28px|link=|Displays time]]",
    "sound_radius": "! [[File:UI_Noise.png|28px|link=|Sound radius]]",
    "item_id": "! Item ID",
}

# table/section based on body_location
body_location_dict = {
    "Long underwear": {
        "body_location": ('Legs1', 'Torso1Legs1'),
        "table": 'torso',
    },
    "Tank top": {
        "body_location": ('TankTop',),
        "table": 'torso',
    },
    "T-shirt": {
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
        "body_location": ('Jacket', 'Jacket_Bulky', 'JacketHat_Bulky'),
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
        "body_location": ('TorsoExtra', 'TorsoExtraVest'),
        "table": 'torso',
    },
    "Legs": {
        "body_location": ('Pants', 'Skirt'),
        "table": 'legs',
    },
    "Dresses": {
        "body_location": ('Dress',),
        "table": 'torso',
    },
    "Boilersuits": {
        "body_location": ('Boilersuit',),
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
        "body_location": ('Underwear',),
        "table": 'generic',
    },
    "Underwear top": {
        "body_location": ('UnderwearTop',),
        "table": 'generic',
    },
    "Underwear bottom": {
        "body_location": ('UnderwearBottom',),
        "table": 'generic',
    },
    "Underwear extra 1": {
        "body_location": ('UnderwearExtra1',),
        "table": 'generic',
    },
    "Underwear extra 2": {
        "body_location": ('UnderwearExtra2',),
        "table": 'generic',
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
    "Scarves": {
        "body_location": ('Scarf',),
        "table": 'normal',
    },
    "Gloves": {
        "body_location": ('Hands',),
        "table": 'normal',
    },
    "Belts": {
        "body_location": ('Belt', 'BeltExtra', 'AmmoStrap'),
        "table": 'belt',
    },
    "Neck": {
        "body_location": ('Neck',),
        "table": 'generic',
    },
    "Necklace": {
        "body_location": ('Necklace',),
        "table": 'generic',
    },
    "Long necklace": {
        "body_location": ('Necklace_Long',),
        "table": 'generic',
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
        "table": 'generic',
    }
}

fabric_type = {
    "Cotton": 'Base.RippedSheets',
    "Denim": 'Base.DenimStrips',
    "Leather": 'Base.LeatherStrips',
}

table_header ='{| class="wikitable theme-red sortable" style="text-align: center;"'


def combine_clothing_files():
    """
    Combines all .txt files from the clothing directory into a single file.
    """
    lc = translate.get_language_code().upper()
    clothing_dir = f'output/{lc}/item_list/clothing/'
    output_file = f'output/{lc}/item_list/clothing_list.txt'

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Open the output file to write
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in sorted(os.listdir(clothing_dir)):
            if filename.endswith('.txt'):
                file_path = os.path.join(clothing_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n')

    print(f"Combined files written to {output_file}")


def convert_to_percentage(value, start_zero=True, percentage=False):
    if not value or value == '-':
        return '-'
    
    try:
        value = float(value)
    except ValueError:
        return '-'
    
    if not percentage:
        if not start_zero:
            value -= 1
        value *= 100

    value = int(round(value))
    
    return f"{value}%"


def get_body_location(body_location):
    for key, value in body_location_dict.items():
        if body_location in value['body_location']:
            # return body location heading and table header
            return key, value['table']
        
    return 'Other', 'generic'


def process_item(item_data, item_id):
    body_location = item_data.get("BodyLocation", 'Unknown')
    heading, table_key = get_body_location(body_location)
    columns = table_dict.get(table_key, table_dict["generic"])
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
            item["body_location"] = f"[[Body location#{body_location}|{body_location}]]"
        else:
            item["body_location"] = f"[[Body location/{language_code}#{body_location}|{body_location}]]"

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
        item["fall_chance"] = convert_to_percentage(item_data.get("ChanceToFall", '-'), True, True)

    if "stomp_power" in columns:
        item["stomp_power"] = convert_to_percentage(item_data.get("StompPower", '-'), True)

    if "have_holes" in columns:
        item["have_holes"] = item_data.get("CanHaveHoles", '-').capitalize()

    if "fabric" in columns:
        fabric_id = fabric_type.get(item_data.get("FabricType"))
        if fabric_id is None:
            fabric = "-"
        else:
            fabric = utility.get_icon(fabric_id, True)
        item["fabric"] = fabric

    if "move_speed" in columns:
        item["move_speed"] = convert_to_percentage(item_data.get("RunSpeedModifier", '-'), False)

    if "attack_speed" in columns:
        item["attack_speed"] = convert_to_percentage(item_data.get("CombatSpeedModifier", '-'), False)

    if "bite_def" in columns:
        item["bite_def"] = convert_to_percentage(item_data.get("BiteDefense", '-'), True, True)

    if "scratch_def" in columns:
        item["scratch_def"] = convert_to_percentage(item_data.get("ScratchDefense", '-'), True, True)

    if "bullet_def" in columns:
        item["bullet_def"] = convert_to_percentage(item_data.get("BulletDefense", '-'), True, True)

    if "neck_def" in columns:
        item["neck_def"] = convert_to_percentage(item_data.get("NeckProtectionModifier", '-'), True)

    if "insulation" in columns:
        item["insulation"] = convert_to_percentage(item_data.get("Insulation", '-'), True)

    if "wind_def" in columns:
        item["wind_def"] = convert_to_percentage(item_data.get("WindResistance", '-'), True)

    if "water_def" in columns:
        item["water_def"] = convert_to_percentage(item_data.get("WaterResistance", '-'), True)

    if "item_id" in columns:
        item["item_id"] = f"{{{{ID|{item_id}}}}}"
    
    return heading, item


def get_items():
    blacklist = ("MakeUp_", "ZedDmg_", "Wound_", "Bandage_", "F_Hair_", "M_Hair_", "M_Beard_")
    clothing_dict = {}

    for item_id, item_data in item_parser.get_item_data().items():
        if item_data.get("Type") in ("Clothing", "AlarmClockClothing"):
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

    write_items_to_file(clothing_dict)


# write to file
def write_items_to_file(clothing_dict):
    language_code = translate.get_language_code()
    output_dir = f'output/{language_code.upper()}/item_list/clothing/'
    os.makedirs(output_dir, exist_ok=True)
    
    for heading, items in clothing_dict.items():
        table_key = body_location_dict[heading]['table']
        columns = table_dict.get(table_key, table_dict["generic"])

        # build the table heading based on values
        table_headings = []
        for col in columns:
            mapped_heading = columns_dict.get(col, col)
            table_headings.append(mapped_heading)
        table_headings = "\n".join(table_headings)

        output_path = os.path.join(output_dir, f"{heading}.txt")
        with open(output_path, 'w', encoding='utf-8') as file:
            # write wiki heading and table headings
            file.write(f"=={heading}==\n")
            file.write(f"{table_header}\n")
            file.write(f"{table_headings}\n")

            sorted_items = sorted(items, key=lambda x: x['name'])
            for item in sorted_items:
                row = '\n| '.join([value for key, value in item.items()])
                file.write(f"|-\n| {row}\n")

            file.write("|}")


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