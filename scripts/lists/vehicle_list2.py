from scripts.objects.vehicle import Vehicle
from scripts.utils import table_helper
from scripts.utils.util import format_link, convert_int
from scripts.core.constants import RESOURCE_PATH, PBAR_FORMAT
from scripts.core.cache import save_cache

TABLE_PATH = f"{RESOURCE_PATH}/tables/vehicle_table.json"
VEHICLE_BLACKLIST = ["Base.SportsCar_ez", "Base.ModernCar_Martin"]

table_map = {}

def generate_data(vehicle_id, table_type, section_type="vehicle"):
    vehicle = Vehicle(vehicle_id)
    
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")
    
    vehicle_data = {}

    model = vehicle.get_model(is_single=False, do_format=True) if section_type == "vehicle" else vehicle.get_model(do_format=True)

    name = vehicle.get_name()
    page = vehicle.get_page()
    link = format_link(name, page)

    vehicle_data["model"] = model if "model" in columns else None
    vehicle_data["name"] = link if "name" in columns else None
    vehicle_data["type"] = vehicle.get_vehicle_type() if "type" in columns else None
    vehicle_data["mass"] = convert_int(vehicle.get_mass()) if "mass" in columns else None
    vehicle_data["engine_power"] = convert_int(vehicle.get_engine_power()) if "engine_power" in columns else None
    vehicle_data["engine_quality"] = vehicle.get_engine_quality() if "engine_quality" in columns else None
    vehicle_data["engine_loudness"] = vehicle.get_engine_loudness() if "engine_loudness" in columns else None
    vehicle_data["max_speed"] = convert_int(vehicle.get_max_speed()) if "max_speed" in columns else None
    vehicle_data["suspension_stiffness"] = convert_int(vehicle.get_suspension_stiffness()) if "suspension_stiffness" in columns else None
    vehicle_data["seats"] = vehicle.get_seats() if "seats" in columns else None
    vehicle_data["protection"] = convert_int(vehicle.get_player_damage_protection()) if "protection" in columns else None
    vehicle_data["glove_box_capacity"] = convert_int(vehicle.get_glove_box_capacity()) if "glove_box_capacity" in columns else None
    if "trunk_capacity" in columns:
        trunk_capacities = list(vehicle.get_trunk_capacity().values())
        trunk_capacities = [str(capacity) for capacity in trunk_capacities]
        if not trunk_capacities:
            trunk_capacities = ["-"]
        vehicle_data["trunk_capacity"] = " / ".join(trunk_capacities)
    if "total_capacity" in columns:
        capacity = vehicle.get_total_capacity()
        vehicle_data["total_capacity"] = "-" if capacity == 0 else int(capacity)
    else:
        vehicle_data["total_capacity"] = None
    if "animal_trailer_size" in columns:
        animal_trailer_size = convert_int(vehicle.get_animal_trailer_size()) if vehicle.get_animal_trailer_size() > 0 else "-"
        vehicle_data["animal_trailer_size"] = animal_trailer_size
    if "lightbar" in columns:
        if vehicle.get_has_lightbar():
            vehicle_data["lightbar"] = '[[File:UI Tick.png|link=|Has lightbar and siren]]'
        else:
            vehicle_data["lightbar"] = '[[File:UI Cross.png|link=|No lightbar and siren]]'


    vehicle_data["vehicle_id"] = vehicle_id if "vehicle_id" in columns else None

    # Remove any values that are None
    vehicle_data = {k: v for k, v in vehicle_data.items() if v is not None}

    # Ensure column order is correct
    vehicle_data = {key: vehicle_data[key] for key in columns if key in vehicle_data}

    # Add item_name for sorting
    vehicle_data["item_name"] = name if "name" in columns else None

    return vehicle_data


def find_table_type(vehicle: Vehicle, section_type: str):
    if section_type == "vehicle":
        if vehicle.is_trailer:
            table_type = "trailer"
        else:
            table_type = "vehicle"
    elif section_type == "parent":
        if vehicle.is_trailer:
            table_type = "Base.Trailer"
        else:
            table_type = vehicle.get_parent().vehicle_id

    return table_type


def find_vehicles(section_type: str):
    all_vehicle_data = {}
    vehicles = Vehicle.all()

    for vehicle_id in vehicles:
        # Skip blacklisted vehicles
        if vehicle_id in VEHICLE_BLACKLIST:
            continue
        
        vehicle = Vehicle(vehicle_id)

        # Skip vehicles that aren't parents
        if (not vehicle.is_parent and section_type == "vehicle") or vehicle.is_burnt or vehicle.is_wreck:
            continue

        table_type = find_table_type(vehicle, section_type)
        vehicle_data = generate_data(vehicle_id, table_type, section_type)

        if table_type not in all_vehicle_data:
            all_vehicle_data[table_type] = []
        
        all_vehicle_data[table_type].append(vehicle_data)

    return all_vehicle_data

def main():
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)
    all_vehicle_data = find_vehicles("vehicle")
    all_vehicle_data_parent = find_vehicles("parent")
    table_helper.create_tables("vehicle", all_vehicle_data, table_map=table_map, columns=column_headings)
    table_helper.create_tables("vehicle_parent", all_vehicle_data_parent, table_map=table_map, columns=column_headings)

if __name__ == "__main__":
    main()
