import os
import json
from scripts.core import translate
from scripts.parser import fluid_parser

#TODO: add translations

HEADER = """{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"
! Name
! Color
! style="width: 50px;" | [[File:Moodle_Icon_Tired.png|link=|Fatigue]]
! [[File:Moodle_Icon_Hungry.png|link=|Hunger]]
! [[File:Moodle_Icon_Stressed.png|link=|Stress]]
! [[File:Moodle_Icon_Thirsty.png|link=|Thirst]]
! [[File:Moodle_Icon_Unhappy.png|link=|Unhappiness]]
! [[File:Fire_01_1.png|32px|link=Nutrition#Calories|Calories]]
! [[File:Wheat.png|32px|link=Nutrition#Carbohydrates|Carbohydrates]]
! [[File:Butter.png|32px|link=Nutrition#Fat|Fat]]
! [[File:Steak.png|32px|link=Nutrition#Proteins|Proteins]]
! [[File:WhiskeyFull.png|32px|link=Alcohol|Alcohol]]
! style="width: 50px;" | [[File:SkullPoison.png|link=|Poison]]
! Fluid ID
|-"""


# Write fluid data to file
def write_fluids_to_file(items, file_name):
    language_code = translate.get_language_code()
    output_dir = os.path.join("output", language_code, "item_list")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{file_name}.txt")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(HEADER)
        for item in items:
            for value in item.values():
                # Replace '0' with '-'
                value = '-' if value == 0 or value == '0' or value == 'None' else value
                file.write(f"\n| {value}")
            file.write(f"\n|-")
        file.write("\n|}")

    print(f"Fluids written to: {output_file}")


# Get fluid data for table
def get_fluids():
    fluids = []

    # Load color_reference.json to get rgb values
    with open("resources/color_reference.json", "r") as f:
        color_reference = json.load(f)

    for fluid_id, fluid_data in fluid_parser.get_fluid_data().items():
        fluid_id = f"Base.{fluid_id}" # Assume fluid ID is in the 'Base' module
        print(fluid_id)

        display_name = fluid_data.get('DisplayName', 'Fluid')
        display_name_prefix = "Fluid_Name_"
        if display_name.startswith(display_name_prefix):
            display_name = display_name[len(display_name_prefix):]

        name = translate.get_translation(display_name, 'FluidID')
        if translate.language_code != "en":
            name_en = translate.get_translation(display_name, 'FluidID', 'en')
            name = f"[[{name_en} (fluid)/{translate.language_code}|{name}]]"
        else:
            name = f"[[{name} (fluid)|{name}]]"


        print(name)

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
            "fatigue_change": properties_data.get('fatigueChange', '-'),
            "hunger_change": properties_data.get('hungerChange', '-'),
            "stress_change": properties_data.get('stressChange', '-'),
            "thirst_change": properties_data.get('thirstChange', '-'),
            "unhappy_change": properties_data.get('unhappyChange', '-'),
            "calories": properties_data.get('calories', '-'),
            "carbohydrates": properties_data.get('carbohydrates', '-'),
            "lipids": properties_data.get('lipids', '-'),
            "proteins": properties_data.get('proteins', '-'),
            "alcohol": properties_data.get('alcohol', '-'),
            # No fluids with the following data yet
#            "flu_reduction": properties_data.get('fluReduction', '-'),
#            "pain_reduction": properties_data.get('painReduction', '-'),
#            "endurance_change": properties_data.get('enduranceChange', '-'),
#            "food_sickness_reduction": properties_data.get('foodSicknessReduction', '-'),
            "poison": poison,
            "fluid_id": fluid_id
        }
        print("----")

        fluids.append(fluid_values)

    write_fluids_to_file(fluids, 'fluid_list')


def main():
    get_fluids()


if __name__ == "__main__":
    main()