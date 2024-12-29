import os
import shutil
import json
from scripts.parser import fluid_parser
from scripts.core import translate, logging_file, version, utility
print(f"Current Working Directory: {os.getcwd()}")


# Get a fluid's data
def get_fluid():
    while True:
        query_fluid_id = input("Enter a fluid id\n> ")
        for fluid_id, fluid_data in fluid_parser.get_fluid_data().items():
            if fluid_id == query_fluid_id:
                return fluid_data, fluid_id
        print(f"No fluid found for '{query_fluid_id}', please try again.")


# Get a fluid's infobox parameters and write to the output file
def write_to_output(fluid_data, fluid_id, output_dir):
    try:
        # Load color_reference.json to get rgb values
        with open("resources/color_reference.json", "r") as f:
            color_reference = json.load(f)

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{fluid_id}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("{{Infobox fluid")

            name = utility.get_fluid_name(fluid_data)
            # Special case for TaintedWater
            if fluid_id == "TaintedWater":
                # Get translation for tainted water string
                tainted_water = translate.get_translation("ItemNameTaintedWater", 'IGUI')
                name = tainted_water.replace("%1", name)

            color = fluid_data.get('ColorReference', fluid_data.get('Color', [0.0, 0.0, 0.0])),

            if len(color) > 1:
                rgb_values = color
            # lookup color_reference for RGB values
            else:
                rgb_values = color_reference["colors"].get(color[0], [0.0, 0.0, 0.0])

            color_rgb = [int(c * 255) for c in rgb_values]
            fluid_color = f"{color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]}"

            properties_data = {}
            if 'Properties' in fluid_data:
                properties_data = fluid_data['Properties']

            poison_data = {}
            if 'Poison' in fluid_data:
                poison_data = fluid_data['Poison']
            poison_max_effect = poison_data.get('maxEffect')
            if poison_max_effect == "None" or None:
                poison_max_effect = ''

            blend_whitelist_data = {}
            blend_whitelist = ''
            if 'BlendWhiteList' in fluid_data:
                blend_whitelist_data = fluid_data['BlendWhiteList']
                if isinstance(blend_whitelist_data, dict): # Fix for 'Test' being a string and not a dict
                    if blend_whitelist_data['whitelist']:
                        blend_whitelist = '<br>'.join(blend_whitelist_data['categories'])
                else: blend_whitelist_data = {}

            blend_blacklist_data = {}
            blend_blacklist = ''
            if 'BlendBlackList' in fluid_data:
                blend_blacklist_data = fluid_data['BlendBlackList']
                if isinstance(blend_blacklist_data, dict): # Fix for 'Test' being a string and not a dict
                    if blend_blacklist_data['blacklist']:
                        blend_blacklist = '<br>'.join(blend_blacklist_data['categories'])
                else: blend_blacklist_data = {}

            parameters = {
                "name": name,
                "categories": '<br>'.join(fluid_data.get('Categories', '')),
                "blend_whitelist": blend_whitelist,
                "blend_blacklist": blend_blacklist,
                "unhappy_change": properties_data.get('unhappyChange', ''),
                "stress_change": properties_data.get('stressChange', ''),
                "fatigue_change": properties_data.get('fatigueChange', ''),
                "endurance_change": properties_data.get('enduranceChange', ''),
                "flu_reduction": properties_data.get('fluReduction', ''),
                "pain_reduction": properties_data.get('painReduction', ''),
                "sick_reduction": properties_data.get('foodSicknessReduction', ''),
                "hunger_change": properties_data.get('hungerChange', ''),
                "thirst_change": properties_data.get('thirstChange', ''),
                "calories": properties_data.get('calories', ''),
                "carbohydrates": properties_data.get('carbohydrates', ''),
                "proteins": properties_data.get('proteins', ''),
                "lipids": properties_data.get('lipids', ''),
                "alcohol": properties_data.get('alcohol', ''),
                "poison_max_effect": poison_max_effect,
                "poison_min_amount": poison_data.get('minAmount', ''),
                "poison_dilute_ratio": poison_data.get('diluteRatio', ''),
                "fluid_color": fluid_color,
                "fluid_color_ref": fluid_data.get('ColorReference', ''),
                "fluid_id": f"Base.{fluid_id}",
                "infobox_version": version.get_version()
            }

            for key, value in parameters.items():
                if value:
                    file.write(f"\n|{key}={value}")

            file.write("\n}}")
    except Exception as e:
        logging_file.log_to_file(f"Error writing file {fluid_id}.txt: {e}", True)


def process_fluid(fluid_data, fluid_id, output_dir):
    write_to_output(fluid_data, fluid_id, output_dir)


def automatic_extraction(output_dir):
    # Create 'output_dir'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for fluid_id, fluid_data in fluid_parser.get_fluid_data().items():
        process_fluid(fluid_data, fluid_id, output_dir)


def main():
    language_code = translate.get_language_code()
    output_dir = f'output/{language_code}/fluid_infoboxes'

    while True:
        choice = input("1: Automatic\n2: Manual\nQ: Quit\n> ").strip().lower()
        if choice == '1':
            automatic_extraction(output_dir)
            print(f"Extraction complete, the files can be found in {output_dir}.")
            return
        elif choice == '2':
            fluid_data, fluid_id = get_fluid()
            process_fluid(fluid_data, fluid_id, output_dir)
            print(f"Extraction complete, the file can be found in {output_dir}.")
            return
        elif choice == 'q':
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
