# Generates a list of BloodLocation values for the modding article

from pathlib import Path
import json
from scripts.core.language import Language, Translate
from scripts.core.constants import (RESOURCE_PATH, OUTPUT_PATH)
from scripts.utils.echo import echo_warning, echo_success

language_code = Language.get()

JSON_DIR = Path(RESOURCE_PATH)
JSON_FILE = "blood_location.json"

OUTPUT_DIR = Path(OUTPUT_PATH) / language_code.lower()
OUTPUT_FILE = "blood_location_list.txt"

display_name_data = {}
blood_location_data = {}

TABLE_HEADER = [
    '{| class="wikitable theme-blue"',
    '! BloodLocation',
    '! Body part(s)',
    '! Visual'
    ]


def get_image(blood_location):
    image_map = {
        "ShirtNoSleeves": "Torso",
        "JumperNoSleeves": "Torso",
        "ShirtLongSleeves": "Jumper",
        "FullHelmet": "Head",
        "Bag": "None",
        "UpperBody": "Torso_Upper",
        "LowerBody": "Torso_Lower",
    }

    image_ref = image_map.get(blood_location, blood_location)

    return f"[[File:BodyPart_{image_ref}.png|62px|{blood_location}]]"


def get_part_id(blood_location):
    part_map = {
        "UpperBody": "Torso_Upper",
        "LowerBody": "Torso_Lower",
        "Bag": "Back"
    }

    return part_map.get(blood_location, blood_location)


def get_display_name(body_part):
    display_name = display_name_data.get(body_part)

    # Check if something is wrong with the data.
    if display_name is None:
        display_name = display_name_data.get("MAX")
        if display_name is None:
            echo_warning(f"No display name found for '{body_part}': Is the data empty?")
        else:
            echo_warning(f"No display name found for '{body_part}': Please check the body_part.")

    return display_name


def generate_content():
    content = TABLE_HEADER

    for blood_location, body_parts in blood_location_data.items():
        content.append(f'|- id="{get_part_id(blood_location)}"')
        content.append(f'| <code>{blood_location}</code>')

        body_parts_new = []
        for body_part in body_parts:
            display_name = get_display_name(body_part)
            name = Translate.get(display_name)
            link = f"[[#{body_part}|{name}]]"
            body_parts_new.append(link)
        content.append("| " + "<br>".join(body_parts_new))

        location_image = get_image(blood_location)
        content.append(f'| style="text-align: center;" | {location_image}')

    content.append("|}")

    return content


def write_to_file(content):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / OUTPUT_FILE
    with open(output_path, "w") as file:
        file.write("\n".join(content))
    echo_success(f"File written to '{output_path}'")


def init_data():
    global blood_location_data
    global display_name_data
    json_path = JSON_DIR / JSON_FILE
    with open(json_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    # Taken from 'BloodClothingType.class'
    blood_location_data = json_data.get("BloodLocation")
    # Taken from 'BodyPartType.class'
    display_name_data = json_data.get("DisplayName")


def main():
    init_data()
    content = generate_content()
    write_to_file(content)


if __name__ == "__main__":
    main()
