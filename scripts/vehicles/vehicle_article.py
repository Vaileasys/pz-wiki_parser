import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.objects.vehicle import Vehicle
from scripts.objects.item import Item
from scripts.vehicles import vehicle_infobox, vehicle_parts, vehicle_list2
from scripts.core.file_loading import read_file, write_file
from scripts.core.constants import VEHICLE_DIR, PBAR_FORMAT
from scripts.core.version import Version
from scripts.utils.util import link
from scripts.utils.echo import echo_success

VEH_DIR = VEHICLE_DIR.format(language_code=Language.get())

VEHICLE_BLACKLIST = ["Base.SportsCar_ez", "Base.ModernCar_Martin"]

def generate_header(vehicle: Vehicle):
    header = "{{{{Header|Project Zomboid|Vehicles|{category}}}}}"
    page_version = f"{{{{Page version|{Version.get()}}}}}"

    if vehicle.is_trailer:
        category = "Trailers"
    else:
        vehicle_type = vehicle.get_vehicle_type().capitalize()
        category = vehicle_type + " vehicles"
    header = header.format(category=category)

    return [header, page_version]

def generate_intro(vehicle: Vehicle):
    name = vehicle.get_name()
    parent_link = "[[trailer]]" if vehicle.is_trailer else vehicle.get_parent().get_link()
    damage = ""
    car_wreck_link = link("Car Wreck", "car wreck")
    if vehicle.is_burnt:
        name = name[0].lower() + name[1:]
        type_link = car_wreck_link
    elif vehicle.is_wreck:
        name = name[0].lower() + name[1:]
        type_link = car_wreck_link

        for side in ("front", "rear", "left", "right"):
            if vehicle.vehicle_id.lower().endswith(side):
                break
        side = side + " side" if side in ("left", "right") else side
        damage = f", with damage to the {side}"
    else:
        type_link = link("vehicle")

    return [f"A '''{name}''' is a {type_link} in {link('Project Zomboid')}. It is a [[#Variants|variant]] of the {parent_link}{damage}."]

def generate_overview(vehicle: Vehicle):
    content = []

    if vehicle.get_has_lightbar():
        content.append(f"The {vehicle.get_name()} features a {link('lightbar')}, which includes a siren.")
    
    key_rings = vehicle.get_special_key_ring()
    if key_rings:
        key_ring_list = []
        for item_type in key_rings:
            item = Item(item_type)
            key_ring_list.append(f"{item.get_icon()} {item.get_link()}")

        if len(key_ring_list) > 1:
            content.append(f"\nOne of the following key rings can spawn along with the vehicle:")
            for key_ring in key_ring_list:
                content.append(f"*{key_ring}")
        else:
            content.append(f"\nThe following key ring can spawn along with the vehicle: {key_ring_list[0]}")

    zombie_types = vehicle.get_zombie_type()
    if zombie_types:
        outfits = []
        for outfit in zombie_types:
            outfits.append(link(outfit + " (outfit)"), outfit)

        if len(outfits) > 1:
            content.append(f"\nThe vehicle will spawn with zombies in the following outfits:")
            for outfit in outfits:
                content.append(f"* {outfit}")
        else:
            content.append(f"\nThe vehicle will spawn with zombies in the following outfit: {outfits[0]}")

    return content

def generate_mechanics(vehicle: Vehicle):
    DISMANTLING = "{vehicle_type} " + f"vehicles can be dismantled with a {link('Welder Mask', 'welder mask')} and {link('Propane Torch', 'propane torch')}, providing some metal {link('Material', 'materials')}, destroying the vehicle. A higher {link('metalworking')} skill will yield more usable materials."
    content = ["{{Main|Mechanics}}"]
    if vehicle.is_burnt:
        content.append("A burnt vehicle cannot be salvaged for parts, and the mechanics menu will display no useful information.")
    else:
        content.append("Vehicles can be salvaged for parts or repaired using replacement parts.")

    if vehicle.is_burnt or vehicle.is_wreck:
        vehicle_type = "Burnt" if vehicle.is_burnt else "Wrecked"
        content.extend(["\n===Dismantling===", DISMANTLING.format(vehicle_type=vehicle_type)])
    if not vehicle.is_burnt:
        content.extend(["\n===Parts===", "The below table shows a list of parts this vehicle can have and the requirements to install/uninstall."])
        content.extend(load_file(rel_path=os.path.join("mechanics", vehicle.vehicle_id + ".txt")))

    return content

def generate_see_also():
    return ["*{{ll|Vehicle Key}}", "*{{ll|Mechanic}}", "*{{ll|Vehicle Knowledge}}"]

def load_file(rel_path):
    path = os.path.join(VEH_DIR, rel_path)
    file_str = read_file(path)
    return file_str.splitlines()

def load_modules():
    vehicle_infobox.main(pre_choice="1")
    vehicle_parts.main()
    vehicle_list2.main()

def process_vehicle(vehicle_id):
    
    if vehicle_id in VEHICLE_BLACKLIST:
        return
    
    vehicle = Vehicle(vehicle_id)
    parent_id = vehicle.get_parent().vehicle_id
    if vehicle.is_trailer:
        parent_id = "Base.Trailer"

    header_content = generate_header(vehicle)
    infobox_content = load_file(rel_path=os.path.join("infoboxes", vehicle_id + ".txt"))
    intro_content = generate_intro(vehicle)
    overview_content = generate_overview(vehicle)
    mechanics_content = generate_mechanics(vehicle)
    variants_content = load_file(rel_path=os.path.join("lists", "vehicles_by_model", parent_id + ".txt"))
    see_also_content = generate_see_also()

    content = []

    content.extend(header_content)
    content.append("{{Autogenerated|B42}}")
    content.extend(infobox_content)
    content.extend(intro_content)

    content.append("\n==Overview==")
    content.extend(overview_content)

    content.append("\n==Mechanics==")
    content.extend(mechanics_content)

    content.append("\n==Variants==")
    content.extend(variants_content)

    content.append("\n==See also==")
    content.extend(see_also_content)

    content.append("\n{{Navbox vehicles}}")

    rel_path = vehicle_id + ".txt"
    write_file(content, rel_path=rel_path, root_path=output_dir, suppress=True)


def main():
    global output_dir
    output_dir = os.path.join(VEH_DIR, "articles")
    load_modules()
    with tqdm(total=Vehicle.count(), desc="Generating vehicle articles", bar_format=PBAR_FORMAT, unit=" vehicles", leave=False) as pbar:
        for vehicle_id in Vehicle.all():
            pbar.set_postfix_str(f"Processing: {vehicle_id[:30]}")
            process_vehicle(vehicle_id)
            pbar.update(1)

    echo_success(f"Article files saved to '{output_dir}'")

if __name__ == "__main__":
    main()