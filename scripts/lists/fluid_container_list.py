""" This is a temporary list for items that are used as fluid containers.

This will be fleshed out more with translations and the new list system once completed.
"""

import os
from scripts.core import translate, utility
from scripts.parser import item_parser

HEADER = """{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"
! Icon
! Name
! Container name
! Weight
! Capacity
! Spawned fluid(s)
! Item ID
|-"""

FLUID_COLORS = {

}

def write_items_to_file(items, file_name):
    language_code = translate.get_language_code()
    output_dir = os.path.join("output", language_code, "item_list")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{file_name}.txt")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(HEADER)
        for item in items:
            for value in item.values():
                file.write(f"\n| {value}")
            file.write(f"\n|-")
        file.write("\n|}")

    print(f"Item names written to (output_file)")

def get_items():
    fluid_containers = []
    fluid_items = []
    i = 0 # fluid containers
    j = 0 # fluid containers with a fluid
    for item_id, item_data in item_parser.get_item_data().items():
        if 'capacity' in item_data:
            display_name = translate.get_translation(item_id, 'DisplayName')
            page_name = utility.get_page(item_id, display_name)
            item_link = utility.format_link(display_name, page_name)
            icon = utility.get_icon(item_id, True, True, True)

            fluid_capacity_ml = float(item_data.get('capacity', 0)) * 1000
            fluid_capacity = f"{str(int(fluid_capacity_ml))}mL"
            fluids_list = "-"
            if "fluids" in item_data:
                fluids_list = []
                for fluid in item_data.get("fluids", []):
                    fluid_id = fluid.get("FluidID", "-")
#                    liquid_count = fluid.get("LiquidCount", 0)
                    colors = fluid.get("Color", [])

                    # Convert liquid_count to mL
#                    liquid_count_str = f"{int(fluid_capacity_ml * float(liquid_count))}mL"

                    if not colors:
#                        fluids_list.append(f"{liquid_count_str} × {fluid_id}")
                        fluids_list.append(fluid_id)
                        continue

                    # Convert colors to RGB format
                    print(f"{item_id}: {colors}")
                    if isinstance(colors, str):
                        colors_str = colors
                    else:
                        colors_str = "RGB: " + ", ".join([f"{color:.2f}" for color in colors])

                    # Append the formatted string
#                    fluids_list.append(f"{liquid_count_str} × {fluid_id} ({colors_str})")
                    fluids_list.append(f"{fluid_id} ({colors_str})")

                fluids_list = "<br>".join(fluids_list)
                
            item = {
                "icon": icon,
                "name": item_link,
                "ContainerName": item_data.get('ContainerName', '-'),
                "weight": item_data.get('Weight', '1'),
                "capacity": fluid_capacity,
                "fluids": fluids_list,
                "item_id": item_id,
            }

            fluid_containers.append(item)

            i = i +1

            if 'fluids' in item_data:
#                fluid_items.append(item_id)
                j = j +1
    print(f"Found {i} items that are a fluid container")
    print(f"Found {j} items with a fluid")
    write_items_to_file(fluid_containers, 'fluid_list')
#    write_items_to_file(fluid_items, 'fluid_items_list')
        

def main():
    get_items()

if __name__ == "__main__":
    main()