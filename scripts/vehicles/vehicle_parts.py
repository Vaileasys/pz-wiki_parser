import os
from scripts.objects.vehicle import Vehicle
from scripts.objects.item import Item
from scripts.core.file_loading import write_file
from scripts.utils.util import format_link
from scripts.core.language import Translate

TABLE_HEADER = '{| class="wikitable theme-red"'
TABLE_HEADINGS = (
    '! Part',
    '! Knowledge',
    '! Skill',
    '! Tools',
    '! Items'
    )
REL_DIR = os.path.join("vehicle", "maintenance")

def process_vehicle(vehicle_id):
    vehicle = Vehicle(vehicle_id)
    content = []
    mechanic_overlay = vehicle.get_mechanics_overlay()
    if mechanic_overlay:
        content.append(f"[[File:{mechanic_overlay}base.png|thumb|Vehicle mechanics UI for the {vehicle.get_name()}.]]")
    content.append(TABLE_HEADER)
    content.extend(TABLE_HEADINGS)
    for part, part_data in vehicle.get_parts_data().items():
        if "*" in part or part_data.get("category") == "nodisplay":
            continue

        skills = vehicle.get_part_install(part).get("skills", {})
        if part == "Engine":
            skills["Mechanics"] = vehicle.get_engine_repair_level()
        skill_list = []
        if skills:
            for skill, level in skills.items():
                skill_list.append(f'{Translate.get("IGUI_perks_" + skill)} {level}')
        if not skill_list:
            skill_list = ['style="text-align:center;"| -']

        RECIPE_MAGS = ["Base.MechanicMag1", "Base.MechanicMag2", "Base.MechanicMag3"]
        recipes = vehicle.get_part_install(part).get("recipes")
        knowledge = 'style="text-align:center;"| -'
        for recipe_mag in RECIPE_MAGS:
            item = Item(recipe_mag)
            if recipes in item.get("TeachedRecipes"):
                knowledge_link = format_link(Translate.get(f"Recipe_{recipes.replace(' ', '_')}", default=recipes), item.get_page())
                knowledge = f'{item.get_icon()} {knowledge_link}'
                break

        tools_dict = vehicle.get_part_install(part).get("items", {})
        if part == "Engine":
            tools_dict["1"] = {"type": "Base.Wrench"} # From `ISVehicleMechanics.onRepairEngine`
        tools = []
        for _, item_data in tools_dict.items():
            if "type" in item_data:
                item = Item(item_data.get("type"))
                item_link = format_link(item.get_name(), item.get_page())
                item_icon = item.get_icon()
                tools.append(f"{item_icon} {item_link}")
            elif "tags" in item_data:
                tag = item_data.get("tags")
                tag_link = format_link(f"{tag} (tag)")
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
            item_link = format_link(item.get_name(), item.get_page())
            item_icon = item.get_icon()
            items.append(f"{item_icon} {item_link}")
        if not items:
            items.append('style="text-align:center;"| -')

        content.append(f'|-')
        content.append(f'| {Translate.get("IGUI_VehiclePart" + part)}')
        content.append(f'| {knowledge}') # knowledge
        content.append(f'| {"<br>".join(skill_list)}') # skill
        content.append(f'| {tools}') # tools
        content.append(f'| {"<br>".join(items)}') # items
    content.append('|}')

    return content

def main():
    for vehicle_id in Vehicle.keys():
        content = process_vehicle(vehicle_id)
        rel_path = os.path.join(REL_DIR, vehicle_id)
        write_file(content, rel_path)

if __name__ == "__main__":
    main()