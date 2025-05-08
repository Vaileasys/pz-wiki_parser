import os
import shutil
from scripts.core import logger
from scripts.objects.vehicle import Vehicle
from scripts.objects.item import Item
from scripts.core.version import Version
from scripts.core.language import Language, Translate
from scripts.core.file_loading import write_file
from scripts.utils.echo import echo_warning, echo_success
from scripts.core.constants import VEHICLE_DIR
from scripts.utils.util import convert_int, link

ROOT_DIR = os.path.join(VEHICLE_DIR.format(language_code=Language.get()), "infoboxes")


def get_vehicle():
    while True:
        query_id = input("Enter a vehicle id\n> ")
        query_id = Vehicle.fix_vehicle_id(query_id)
        if query_id in Vehicle.keys():
            return query_id
        echo_warning(f"No vehicle found for '{query_id}', please try again.")


def enumerate_params(parameters):
    new_parameters = {}
    for key, value in parameters.items():
        # Remove key-value pairs if they have no value
        if not value:
            continue
        if isinstance(value, list):
            new_parameters[key] = value[0]
            for i, v in enumerate(value[1:], start=2):
                new_parameters[f"{key}{i}"] = v
        else:
            new_parameters[key] = value
    return new_parameters

def check_zero(value: int|float) -> int|float|None:
    """Returns None if the value is zero."""
    return None if float(value) == 0.0 else value

def generate_data(vehicle_id:str):
    try:
        vehicle = Vehicle(vehicle_id)

        manufacturer = vehicle.get_manufacturer()
        if manufacturer is not None and manufacturer != "Unknown":
            manufacturer = link(manufacturer)

        trunk_types_raw = vehicle.get_trunk_capacity().keys()
        trunk_types = []
        trunk_open = f' ({Translate.get("IGUI_Open")})' if "TruckBedOpen" in vehicle.get_trunk_capacity() else ""
        for trunk_type in trunk_types_raw:
            trunk_type = Translate.get("IGUI_VehiclePart" + trunk_type)
            trunk_types.append(trunk_type + trunk_open)

        trunk_capacities = list(vehicle.get_trunk_capacity().values())
        trunk_capacities = [str(capacity) for capacity in trunk_capacities]

        key_rings_raw = vehicle.get_special_key_ring()
        key_rings = []
        for key_ring in key_rings_raw:
            key_ring_name = Item(key_ring).get_icon()
            key_rings.append(key_ring_name)

        parameters = {
            "name": vehicle.get_name(),
            "image": vehicle.get_model(),
            "manufacturer": manufacturer,
            "base_model": vehicle.get_full_parent().get_link() if not vehicle.is_trailer and vehicle.get_full_parent().vehicle_id != vehicle_id else None,
            "vehicle_type": vehicle.get_vehicle_type(),
#            "service": vehicle.get_service(),
#            "business": vehicle.get_business(),
            "seats": vehicle.get_seats(),
            "doors": len(vehicle.get_doors()),
            "wheels": len(vehicle.get_wheels()),
            "trunk_type": "<br>".join(trunk_types),
            "lightbar": vehicle.get_has_lightbar(),
            "weight": convert_int(vehicle.get_mass()),
            "occupant_protection": check_zero(convert_int(vehicle.get_player_damage_protection())),
            "glove_box_capacity": vehicle.get_glove_box_capacity() if not vehicle.is_burnt else None,
            "trunk_capacity": " / ".join(trunk_capacities) if not vehicle.is_burnt else None,
            "total_storage": vehicle.get_total_capacity() if not vehicle.is_burnt else None,
            "animal_size": check_zero(convert_int(vehicle.get_animal_trailer_size())),
            "engine_power": f"{vehicle.get_engine_power()} hp" if not vehicle.is_trailer and not vehicle.is_burnt and not vehicle.is_wreck else None,
            "engine_loudness": vehicle.get_engine_loudness() if not vehicle.is_trailer and not vehicle.is_burnt and not vehicle.is_wreck else None,
            "engine_quality": vehicle.get_engine_quality() if not vehicle.is_trailer and not vehicle.is_burnt and not vehicle.is_wreck else None,
            "top_speed": convert_int(vehicle.get_max_speed()) if not vehicle.is_trailer and not vehicle.is_burnt and not vehicle.is_wreck else None,
            "roll_influence": convert_int(vehicle.get_roll_influence()) if not vehicle.is_burnt and not vehicle.is_wreck else None,
            "suspension_stiffness": convert_int(vehicle.get_suspension_stiffness()) if not vehicle.is_burnt and not vehicle.is_wreck else None,
            "offroad_efficiency": convert_int(vehicle.get_offroad_efficiency()) if not vehicle.is_burnt and not vehicle.is_wreck else None,
            "mesh": vehicle.get_mesh_path().split("/")[-1],
            "vehicle_id": vehicle_id,
        }

        parameters = enumerate_params(parameters)
        parameters["infobox_version"] = Version.get()

        return parameters
    except Exception as e:
        logger.write(f"Error generating data for {vehicle_id}", True, exception=e, category="error")


def process_vehicle(vehicle_id):
    parameters = generate_data(vehicle_id)
    if parameters is not None:
        vehicle_id = parameters.get("vehicle_id")
        rel_path = f'{vehicle_id}.txt'
        content = []

        # Generate infobox
        content.append("{{Infobox vehicle")
        for key, value in parameters.items():
            content.append(f"|{key}={value}")
        content.append("}}")

        write_file(content, rel_path=rel_path, root_path=ROOT_DIR, suppress=True)


def automatic_extraction():
    # Create 'output_dir'
    if os.path.exists(ROOT_DIR):
        shutil.rmtree(ROOT_DIR)
    os.makedirs(ROOT_DIR)

    for vehicle_id in Vehicle.keys():
        process_vehicle(vehicle_id)


def main(pre_choice:str=None):
    """
    :param pre_choice: str - Automatically sets a choice without querying the user.
    """
    # Call early
    Language.get()

    while True:
        options = ("1", "2", "q")
        if str(pre_choice).lower() not in options:
            choice = input("1: Automatic\n2: Manual\nQ: Quit\n> ").strip().lower()
        else:
            choice = str(pre_choice).lower()

        if choice == '1':
            automatic_extraction()
            echo_success(f"Extraction complete, the files can be found in '{ROOT_DIR}'.")
            break
        elif choice == '2':
            vehicle_id = get_vehicle()
            process_vehicle(vehicle_id)
            echo_success(f"Extraction complete, the file can be found in '{ROOT_DIR}'.")
            break
        elif choice == 'q':
            break
        else:
            echo_warning("Invalid choice.")


if __name__ == "__main__":
    main()
