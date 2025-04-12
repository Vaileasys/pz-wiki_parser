import os
import json
from scripts.core.language import Language, Translate
from scripts.parser import fluid_parser
from scripts.utils import utility
from scripts.utils.echo import echo_success

#TODO: add translations

HEADER = """{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"
! <<name>>
! <<color>>
! [[File:Status_Hunger_32.png|32px|link=|<<hunger>>]]
! [[File:Status_Thirst_32.png|32px|link=|<<thirst>>]]
! [[File:Fire_01_1.png|32px|link=|<<calories>>]]
! [[File:Wheat.png|32px|link=|<<carbohydrates>>]]
! [[File:Butter.png|32px|link=|<<fat>>]]
! [[File:Steak.png|32px|link=|<<proteins>>]]
! [[File:SkullPoison.png|link=|<<poison>>]]
! [[File:Mood_Drunk_32.png|32px|link=|<<alcohol>>]]
! [[File:Mood_Sleepy_32.png|32px|link=|<<fatigue>>]]
! [[File:Mood_Stressed_32.png|32px|link=|<<stress>>]]
! [[File:Mood_Sad_32.png|32px|link=|<<unhappiness>>]]
! <<fluid_id>>
|-"""


# Write fluid data to file
def write_fluids_to_file(items, file_name):
    language_code = Language.get()
    output_dir = os.path.join("output", language_code, "item_list")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{file_name}.txt")
    with open(output_file, "w", encoding="utf-8") as file:
        translated_header = Translate.get_wiki(HEADER)
        bot_flag_start = f'<!--BOT_FLAG-start-{file_name.replace(" ", "_")}. DO NOT REMOVE-->'
        bot_flag_end = f'<!--BOT_FLAG-end-{file_name.replace(" ", "_")}. DO NOT REMOVE-->'
        file.write(bot_flag_start + translated_header)
        for item in items:
            for value in item.values():
                # Replace '0' with '-'
                value = '-' if value == 0 or value == '0' or value == 'None' else value
                file.write(f"\n| {value}")
            file.write(f"\n|-")
        file.write("\n|}" + bot_flag_end)

    echo_success(f"Fluids written to: {output_file}")


# Get fluid data for table
def get_fluids():
    fluids = []

    # Load color_reference.json to get rgb values
    with open("resources/color_reference.json", "r") as f:
        color_reference = json.load(f)

    for fluid_id, fluid_data in fluid_parser.get_fluid_data().items():
        fluid_id = f"Base.{fluid_id}" # Assume fluid ID is in the 'Base' module

        name = utility.get_fluid_name(fluid_data)
        if Language.get() != "en":
            name_en = utility.get_fluid_name(fluid_data, "en")
            name = f"[[{name_en} (fluid)/{Language.get()}|{name}]]"
        else:
            name = f"[[{name} (fluid)|{name}]]"

        color = fluid_data.get('ColorReference', fluid_data.get('Color', [0.0, 0.0, 0.0])),

        if len(color) > 1:
            rgb_values = color
        # lookup color_reference for RGB values
        else:
            rgb_values = color_reference["colors"].get(color[0], [0.0, 0.0, 0.0])

        color_rgb = [int(c * 255) for c in rgb_values]
        color_str = f"{{{{rgb|{color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]}}}}}"

        if 'Properties' in fluid_data:
            properties_data = fluid_data['Properties']

        if 'Poison' in fluid_data:
            poison_data = fluid_data['Poison']
            poison = poison_data.get('maxEffect', '-')
        else:
            poison = '-'

        fluid_values = {
            "name": name,
            "color": color_str,
            "hunger_change": properties_data.get('hungerChange', '-'),
            "thirst_change": properties_data.get('thirstChange', '-'),
            "calories": properties_data.get('calories', '-'),
            "carbohydrates": properties_data.get('carbohydrates', '-'),
            "lipids": properties_data.get('lipids', '-'),
            "proteins": properties_data.get('proteins', '-'),
            "poison": poison,
            "alcohol": properties_data.get('alcohol', '-'),
            "fatigue_change": properties_data.get('fatigueChange', '-'),
            "stress_change": properties_data.get('stressChange', '-'),
            "unhappy_change": properties_data.get('unhappyChange', '-'),
            # No fluids with the following data yet
#            "flu_reduction": properties_data.get('fluReduction', '-'),
#            "pain_reduction": properties_data.get('painReduction', '-'),
#            "endurance_change": properties_data.get('enduranceChange', '-'),
#            "food_sickness_reduction": properties_data.get('foodSicknessReduction', '-'),
            "fluid_id": fluid_id
        }

        fluids.append(fluid_values)

    write_fluids_to_file(fluids, 'fluid')


def main():
    get_fluids()


if __name__ == "__main__":
    main()