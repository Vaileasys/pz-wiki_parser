import os
from tqdm import tqdm
from scripts.objects.vehicle import Vehicle
from scripts.objects.item import Item
from scripts.core.file_loading import write_file
from scripts.utils.util import link
from scripts.utils.echo import echo_success
from scripts.core.language import Translate, Language
from scripts.core.constants import PBAR_FORMAT

TABLE_HEADER = '{| class="wikitable theme-red sortable mw-collapsible" data-expandtext="{{int:show}}" data-collapsetext="{{int:hide}}"'
TABLE_CAPTION = '|+ style="min-width:300px;" | Parts list'
TABLE_HEADINGS = (
    '! Part',
    '! Category',
    '! Knowledge',
    '! Skill',
    '! Tools',
    '! Items'
    )
REL_DIR = os.path.join("vehicle", "mechanics")

def process_vehicle(vehicle_id):
    vehicle = Vehicle(vehicle_id)

    rows = []
    for part, part_data in vehicle.get_parts_data().items():
        if "*" in part or part_data.get("category") == "nodisplay":
            continue

        skills = vehicle.get_part_install(part).get("skills", {})
        if part == "Engine":
            skills["Mechanics"] = vehicle.get_engine_repair_level()
        skill_list = []
        if skills:
            for skill, level in skills.items():
                skill_list.append(f'[[{Translate.get("IGUI_perks_" + skill)}]] {level}')
        if not skill_list:
            skill_list = ['style="text-align:center;"| -']

        RECIPE_MAGS = ["Base.MechanicMag1", "Base.MechanicMag2", "Base.MechanicMag3"]
        recipes = vehicle.get_part_install(part).get("recipes")
        knowledge = 'style="text-align:center;"| -'
        for recipe_mag in RECIPE_MAGS:
            item = Item(recipe_mag)
            if recipes in item.get("TeachedRecipes"):
                knowledge_link = link(item.get_page(), Translate.get(f"Recipe_{recipes.replace(' ', '_')}", default=recipes))
                knowledge = f'{item.get_icon()} {knowledge_link}'
                break

        tools_dict = vehicle.get_part_install(part).get("items", {})
        if part == "Engine":
            tools_dict["1"] = {"type": "Base.Wrench"} # From `ISVehicleMechanics.onRepairEngine`
        tools = []
        for _, item_data in tools_dict.items():
            if "type" in item_data:
                item = Item(item_data.get("type"))
                item_link = link(item.get_page(), item.get_name())
                item_icon = item.get_icon()
                tools.append(f"{item_icon} {item_link}")
            elif "tags" in item_data:
                tag = item_data.get("tags")
                tag_link = link(f"{tag} (tag)")
                tag_template = f'{{{{Tag {tag}}}}}'
                tools.append(f'{tag_template} {tag_link}')
        tools = "<br>".join(tools)
        if not tools:
            tools = 'style="text-align:center;"| -'
        
        mechanic_id = vehicle.get_mechanic_type()
        items_list = part_data.get("itemType", [])
        if part == "Engine":
            items_list.append("Base.EngineParts") # From `ISVehicleMechanics.onRepairEngine`
        items = []
        for value in items_list:
            is_specific_item = False if part_data.get("specificItem") is False or part == "Engine" else True
            if is_specific_item:
                item_id = value + str(mechanic_id)
            else:
                item_id = value
            item = Item(item_id)
            item_link = link(item.get_page(), item.get_name())
            item_icon = item.get_icon()
            items.append(f"{item_icon} {item_link}")
        if not items:
            items.append('style="text-align:center;"| -')

        row = (
            Translate.get("IGUI_VehiclePart" + part),                                   # Part
            Translate.get("IGUI_VehiclePartCat" + part_data.get("category", "Other")),  # Category
            knowledge,                                                                  # Knowledge
            "<br>".join(skill_list),                                                    # Skill
            tools,                                                                      # Tools
            "<br>".join(items)                                                          # Items
        )
        rows.append(row)

    return rows


def generate_table(vehicle_id, rows):
    vehicle = Vehicle(vehicle_id)
    content = []
    mechanic_overlay = vehicle.get_mechanics_overlay()
    if mechanic_overlay:
        content.append(f"[[File:{mechanic_overlay}base.png|thumb|Vehicle mechanics UI for the {vehicle.get_name()}.]]")
    content.append('<div class="scroll-x">')
    content.append(TABLE_HEADER)
    content.append(TABLE_CAPTION)
    content.extend(TABLE_HEADINGS)

    rows.sort(key=lambda x: x[1]) # Sort by 'Category' (index 1)
    for row in rows:
        content.append('|-')
        for cell in row:
            content.append(f'| {cell}')
    
    content.append('|}')
    content.append('</div>')
    return content



def main():
    Language.get()
    with tqdm(total=Vehicle.count(), desc="Generating vehicle mechanics", bar_format=PBAR_FORMAT, unit=" vehicles", leave=False) as pbar:
        for vehicle_id in Vehicle.keys():
            pbar.set_postfix_str(f"Processing: {vehicle_id[:30]}")
            
            if Vehicle(vehicle_id).get_parts():
                rows = process_vehicle(vehicle_id)
                content = generate_table(vehicle_id, rows)
                rel_path = os.path.join(REL_DIR, vehicle_id + ".txt")
                output_dir = write_file(content, rel_path, suppress=True)

            pbar.update(1)
    
    echo_success(f"Vehicle part files saved to '{output_dir}'")

if __name__ == "__main__":
    main()