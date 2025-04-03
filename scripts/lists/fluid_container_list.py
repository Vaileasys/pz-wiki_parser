""" This is a temporary list for items that are used as fluid containers.

This will be fleshed out more with translations and the new list system once completed.
"""

import os
import json
from scripts.core import translate
from scripts.parser import item_parser, fluid_parser
from scripts.utils import utility, util

HEADER = """{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"
! Icon
! Name
! Container name
! [[File:Status_HeavyLoad_32.png|32px|link=|Weight]] (empty)
! Capacity
! [[File:Status_HeavyLoad_32.png|32px|link=|Weight]] (full)
! Spawned fluid(s)
! Item ID
|-"""

def write_items_to_file(items, file_name):
    language_code = translate.get_language_code()
    output_dir = os.path.join("output", language_code, "item_list")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{file_name}.txt")
    with open(output_file, "w", encoding="utf-8") as file:
        bot_flag_start = f'<!--BOT_FLAG-start-{file_name.replace(" ", "_")}. DO NOT REMOVE-->'
        bot_flag_end = f'<!--BOT_FLAG-end-{file_name.replace(" ", "_")}. DO NOT REMOVE-->'
        file.write(bot_flag_start + HEADER)
        for item in items:
            del item['item_name'] # Delete 'item_name' as it was only used for sorting
            for value in item.values():
                file.write(f"\n| {value}")
            file.write(f"\n|-")
        file.write("\n|}" + bot_flag_end)

    print(f"Item names written to {output_file}")

def get_items():
    fluid_containers = []
    parsed_fluid_data = fluid_parser.get_fluid_data()
    i = 0 # fluid containers
    j = 0 # fluid containers with a fluid

    with open("resources/color_reference.json", "r") as f:
        color_reference = json.load(f)

    for item_id, item_data in item_parser.get_item_data().items():
        if 'capacity' in item_data:
            display_name = translate.get_translation(item_id, 'DisplayName')
            page_name = utility.get_page(item_id, display_name)
            item_link = util.format_link(display_name, page_name)
            icon = utility.get_icon(item_id, True, True, True)
            container_name = item_data.get('ContainerName', '-')
            container_name = translate.get_translation(container_name, 'ContainerName')

            fluid_capacity_ml = float(item_data.get('capacity', 0)) * 1000
            fluid_capacity = int(fluid_capacity_ml)
            weight = float(item_data.get('Weight', 1))
            weight_ml = (fluid_capacity / 1000) + weight
            if weight_ml.is_integer():
                weight_ml = int(weight_ml)
            else:
                weight_ml = round(weight_ml, 1)
            if weight.is_integer():
                weight = int(weight)
            else:
                weight = round(weight, 1)

            fluids_list = "-"
            if "fluids" in item_data:
                fluids_list = []
                for fluid in item_data.get("fluids", []):
                    fluid_id = fluid.get("FluidID", None)
                    fluid_data = parsed_fluid_data[fluid_id]
                    if fluid_id is not None:
                        fluid_name = utility.get_fluid_name(fluid_data)
                        fluid_name_en = utility.get_fluid_name(fluid_data, 'en')
                        if translate.language_code != "en":
                            fluid_name = f"[[{fluid_name_en} (fluid)/{translate.language_code}|{fluid_name}]]"
                        else:
                            fluid_name = f"[[{fluid_name_en} (fluid)|{fluid_name}]]"
                    else:
                        fluid_name = "-"
#                    liquid_count = fluid.get("LiquidCount", 0)
                    colors = fluid.get("Color", [])

                    # Convert liquid_count to mL
#                    liquid_count_str = f"{int(fluid_capacity_ml * float(liquid_count))}mL"

                    # Get the fluid color from the fluid_id
                    if not colors and fluid_id:
                        if fluid_data['ColorReference']:
                            colors = fluid_data['ColorReference']
                        elif fluid_data['Color']:
                            colors = fluid_data['Color']
                        else:
                            colors = [0.0, 0.0, 0.0]

                    # lookup color_reference for RGB values
                    if isinstance(colors, str):
                        # Colour references found in 'Colors.class'
                        rgb_values = color_reference["colors"].get(colors, [0.0, 0.0, 0.0])
                    else:
                        rgb_values = colors

                    colors_rgb = [int(c * 255) for c in rgb_values]
                    colors_str = f"{{{{rgb|{colors_rgb[0]}, {colors_rgb[1]}, {colors_rgb[2]}}}}}"


                    # Append the formatted string
#                    fluids_list.append(f"{liquid_count_str} × {fluid_name} ({colors_str})")
                    fluids_list.append(f"{fluid_name} {colors_str}")

                fluids_list = "<br>".join(fluids_list)

            item = {
                "icon": icon,
                "item_link": item_link,
                "ContainerName": container_name,
                "weight": str(weight),
                "capacity": str(fluid_capacity) + "mL",
                "weight_ml": str(weight_ml),
                "fluids": fluids_list,
                "item_id": item_id,
                "item_name": display_name
            }

            fluid_containers.append(item)


            i = i +1

            if 'fluids' in item_data:
                j = j +1
    
    # Sort by the item_name
    fluid_containers.sort(key=lambda e: e['item_name'])

    print(f"Found {i} items that are a fluid container")
    print(f"Found {j} items with a fluid")
    write_items_to_file(fluid_containers, 'fluid_container')
        

def main():
    get_items()

if __name__ == "__main__":
    main()