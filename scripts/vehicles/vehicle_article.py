import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.objects.vehicle import Vehicle
from scripts.objects.item import Item
from scripts.vehicles import vehicle_infobox, vehicle_parts, vehicle_list2, vehicle_spawns
from scripts.core.file_loading import load_file, write_file
from scripts.core.constants import VEHICLE_DIR, PBAR_FORMAT
from scripts.core.version import Version
from scripts.utils.util import link
from scripts.utils.echo import echo_success
from scripts.parser.outfit_parser import get_outfits, translate_outfit_name

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
    outfits_data = get_outfits()
    def check_outfit_exists(outfit):
        """Checks if an outfit exists and append a formatted bullet link."""
        outfits = []
        if outfits_data.get("FemaleOutfits", {}).get(outfit):
            outfits.append("* " + link(translate_outfit_name(outfit) + " (female)"))
        if outfits_data.get("MaleOutfits", {}).get(outfit):
            outfits.append("* " + link(translate_outfit_name(outfit) + " (male)"))
        return outfits

    content = []

    # Lightbar
    if vehicle.get_has_lightbar():
        content.append("===Lightbar===")
        content.append(f"The {vehicle.get_name()} features a {link('lightbar')}, which includes a siren.")
    
    # Key Rings
    key_rings = vehicle.get_special_key_ring()
    if key_rings:
        content.append("===Key rings===")
        content.append(f"One of the following key rings can spawn along with the vehicle:")
        for item_type in key_rings:
            item = Item(item_type)
            content.append(f"* {item.get_icon()} {item.get_link()}")

    # Outfits
    zombie_types = vehicle.get_zombie_type()
    if zombie_types:
        content.append("===Outfits===")
        content.append(f"The vehicle will spawn with zombies in the following outfits:")
        for outfit in zombie_types:
            content.extend(check_outfit_exists(outfit))

    return content


def generate_mechanics(vehicle: Vehicle):
    DISMANTLING = "{vehicle_type} " + f"vehicles can be dismantled with a {link('Welder Mask', 'welder mask')} and {link('Propane Torch', 'propane torch')}, providing some metal {link('Material', 'materials')}, destroying the vehicle. A higher {link('welding')} skill will yield more usable materials."
    content = ["{{Main|Mechanics}}"]
    if vehicle.is_burnt:
        content.append("A burnt vehicle cannot be salvaged for parts, and the mechanics menu will display no useful information.")
    else:
        content.append("Vehicles can be salvaged for parts or repaired using replacement parts.")

    if vehicle.is_burnt or vehicle.is_wreck:
        vehicle_type = "Burnt" if vehicle.is_burnt else "Wrecked"
        content.extend(["\n===Dismantling===", DISMANTLING.format(vehicle_type=vehicle_type)])
    if not vehicle.is_burnt:
        content.extend(["\n===Parts===", "The table below shows a list of parts this vehicle can have and the requirements to install/uninstall."])
        content.extend(load_file(rel_path=os.path.join("mechanics", vehicle.vehicle_id + ".txt"), root_path=VEH_DIR))

    return content


def generate_location(vehicle: Vehicle):
    content = []
    content.extend(load_file(rel_path=os.path.join("vehicle_spawns", vehicle.vehicle_id + ".txt"), root_path=VEH_DIR))

    return content


def generate_see_also(vehicle: Vehicle):
    content = ["Mechanic", "Vehicle Knowledge"]
    if vehicle.is_burnt or vehicle.is_wreck:
        content.append("Vehicle")
    else:
        content.extend(["Vehicle Key", "Car Wreck"])
    content = sorted(content)
    content = [f"*{{{{ll|{page}}}}}" for page in content]
    return content


def load_modules():
    vehicle_infobox.main(pre_choice="1")
    vehicle_parts.main()
    vehicle_list2.main()
    vehicle_spawns.main()

def process_vehicle(vehicle_id):
    if vehicle_id in VEHICLE_BLACKLIST:
        return
    
    vehicle = Vehicle(vehicle_id)
    parent_id = vehicle.get_parent().vehicle_id
    if vehicle.is_trailer:
        parent_id = "Base.Trailer"

    header_content = generate_header(vehicle)
    infobox_content = load_file(rel_path=os.path.join("infoboxes", vehicle_id + ".txt"), root_path=VEH_DIR)
    intro_content = generate_intro(vehicle)
    overview_content = generate_overview(vehicle)
    mechanics_content = generate_mechanics(vehicle)
    location_content = generate_location(vehicle)
    variants_content = load_file(rel_path=os.path.join("lists", "vehicles_by_model", parent_id + ".txt"), root_path=VEH_DIR)
    see_also_content = generate_see_also(vehicle)

    content = []

    content.extend(header_content)
    content.append("{{Autogenerated|B42}}")
    content.extend(infobox_content)
    content.extend(intro_content)

    if overview_content:
        content.append("\n==Overview==")
        content.extend(overview_content)

    if mechanics_content:
        content.append("\n==Mechanics==")
        content.extend(mechanics_content)
    
    if location_content:
        content.append("\n==Location==")
        content.extend(location_content)

    if variants_content:
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