import os
from scripts.parser import item_parser
from scripts.core.language import Language
from scripts.utils import utility

# Dictionary for body part combinations. This is used in 'Template:Body_part' to display the image and body parts.
BODY_PARTS_DICT = {
    "FullBody": [
        "Back", "Foot_L", "Foot_R", "ForeArm_L", "ForeArm_R", "Groin", "Hand_L", "Hand_R",
        "Head", "LowerLeg_L", "LowerLeg_R", "Neck", "Torso_Lower", "Torso_Upper",
        "UpperArm_L", "UpperArm_R", "UpperLeg_L", "UpperLeg_R"
    ],
    "FullLegs": [
        "Back", "ForeArm_L", "ForeArm_R", "Groin", "LowerLeg_L", "LowerLeg_R", 
        "Torso_Lower", "Torso_Upper", "UpperArm_L", "UpperArm_R", "UpperLeg_L", "UpperLeg_R"
    ],
    "LongJacket": [
        "Back", "ForeArm_L", "ForeArm_R", "Groin", "Neck", "Torso_Lower", "Torso_Upper",
        "UpperArm_L", "UpperArm_R", "UpperLeg_L", "UpperLeg_R"
    ],
    "JumperUp": [
        "Back", "ForeArm_L", "ForeArm_R", "Head", "Torso_Lower", "Torso_Upper", 
        "UpperArm_L", "UpperArm_R"
    ],
    "Jacket": [
        "Back", "ForeArm_L", "ForeArm_R", "Neck", "Torso_Lower", "Torso_Upper",
        "UpperArm_L", "UpperArm_R"
    ],
    "Jumper": [
        "Back", "ForeArm_L", "ForeArm_R", "Torso_Lower", "Torso_Upper", "UpperArm_L", "UpperArm_R"
    ],
    "ShirtLegsHead": [
        "Back", "Groin", "Head", "LowerLeg_L", "LowerLeg_R", "Torso_Lower", "Torso_Upper", 
        "UpperArm_L", "UpperArm_R", "UpperLeg_L", "UpperLeg_R"
    ],
    "ShirtLegs": [
        "Back", "Groin", "LowerLeg_L", "LowerLeg_R", "Torso_Lower", "Torso_Upper", 
        "UpperArm_L", "UpperArm_R", "UpperLeg_L", "UpperLeg_R"
    ],
    "Overalls": [
        "Back", "Groin", "LowerLeg_L", "LowerLeg_R", "Torso_Lower", "Torso_Upper", 
        "UpperLeg_L", "UpperLeg_R"
    ],
    "ShortsShirt": [
        "Back", "Groin", "Torso_Lower", "Torso_Upper", "UpperArm_L", "UpperArm_R", 
        "UpperLeg_L", "UpperLeg_R"
    ],
    "Shirt": [
        "Back", "Torso_Lower", "Torso_Upper", "UpperArm_L", "UpperArm_R"
    ],
    "Torso": [
        "Back", "Torso_Lower", "Torso_Upper"
    ],
    "Back": [
        "Back"
    ],
    "Socks": [
        "Foot_L", "Foot_R", "LowerLeg_L", "LowerLeg_R"
    ],
    "Shoes": [
        "Foot_L", "Foot_R"
    ],
    "Foot_L": [
        "Foot_L"
    ],
    "Foot_R": [
        "Foot_R"
    ],
    "ArmHand_L": [
        "ForeArm_L", "Hand_L", "UpperArm_L"
    ],
    "ForeArm_L": [
        "ForeArm_L"
    ],
    "ArmHand_R": [
        "ForeArm_R", "Hand_R", "UpperArm_R"
    ],
    "Arm_R": [
        "ForeArm_R", "UpperArm_R"
    ],
    "ForeArm_R": [
        "ForeArm_R"
    ],
    "Trousers": [
        "Groin", "LowerLeg_L", "LowerLeg_R", "UpperLeg_L", "UpperLeg_R"
    ],
    "ShortsShort": [
        "Groin", "UpperLeg_L", "UpperLeg_R"
    ],
    "Groin": [
        "Groin"
    ],
    "Hands": [
        "Hand_L", "Hand_R"
    ],
    "Hand_L": [
        "Hand_L"
    ],
    "Hand_R": [
        "Hand_R"
    ],
    "HeadNeck": [
        "Head", "Neck"
    ],
    "Head": [
        "Head"
    ],
    "UpperLegs": [
        "UpperLeg_L", "UpperLeg_R"
    ],
    "LowerLegs": [
        "LowerLeg_L", "LowerLeg_R"
    ],
    "Leg_L": [
        "LowerLeg_L", "UpperLeg_L"
    ],
    "LowerLeg_L": [
        "LowerLeg_L"
    ],
    "Leg_R": [
        "LowerLeg_R", "UpperLeg_R"
    ],
    "LowerLeg_R": [
        "LowerLeg_R"
    ],
    "Neck": [
        "Neck"
    ],
    "Apron": [
        "Torso_Lower", "Torso_Upper", "UpperLeg_L", "UpperLeg_R"
    ],
    "TorsoUpperArms": [
        "Torso_Upper", "UpperArm_L", "UpperArm_R"
    ],
    "UpperArms": [
        "UpperArm_L", "UpperArm_R"
    ],
    "LowerArms": [
        "ForeArm_L", "ForeArm_R"
    ],
    "Torso_Upper": [
        "Torso_Upper"
    ],
    "UpperArm_L": [
        "UpperArm_L"
    ],
    "UpperArm_R": [
        "UpperArm_R"
    ],
    "UpperLeg_L": [
        "UpperLeg_L"
    ],
    "UpperLeg_R": [
        "UpperLeg_R"
    ]
}

# Compares a body part list with the BODY_PARTS_DICT to get the correct key to be used in 'Template:Body_part'
def get_body_part_ref(search_list):
    for ref_key, ref_list in BODY_PARTS_DICT.items():
        if sorted(ref_list) == sorted(search_list):
            return ref_key
    return None


# Gets all items with 'BloodLocation' and passes them through 'get_item()'
def get_items():
    parsed_item_data = item_parser.get_item_data()
    data = {}
    for item_id, item_data in parsed_item_data.items():
        if 'BloodLocation' in item_data:
            data[item_id] = get_item(item_id)

    return data


# Gets body parts for an item
def get_item(item_id):
    parsed_item_data = item_parser.get_item_data()

    if item_id in parsed_item_data:
        item_data = parsed_item_data[item_id]
        if 'BloodLocation' in item_data:
            body_parts = utility.get_body_parts(item_data, False)

            return body_parts
    else:
        print(f"No data found for '{item_id}'")

    return


# Builds 'Template:Body_part' and writes it to a separate txt file for each item ID
def write_to_file(data):
    i = 0
    language_code = Language.get()
    output_dir = os.path.join("output", language_code, "body_parts")
    os.makedirs(output_dir, exist_ok=True)

    for item_id, body_parts in data.items():
        output_file = os.path.join(output_dir, f'{item_id}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            body_part_ref = get_body_part_ref(body_parts)
            file.write(f"{{{{Body part|id={item_id}|{body_part_ref}}}}}")
        
        i += 1

    print(f"{i} body part files created in '{output_dir}'")


def main():
    data = {}

    print("Running item_body_part...")

    while True:
        choice = input("1. Automatic - Generate for all items\n2. Manual - Generate for a specific item\nQ. Quit\n> ")
        if choice == "1":
            data = get_items()
            break
        
        elif choice == "2":
            item_id = input("Enter item ID\n> ")
        
            data[item_id] = get_item(item_id)
            break
        
        elif choice.lower() == "q":
            return

    write_to_file(data)


if __name__ == "__main__":
    main()