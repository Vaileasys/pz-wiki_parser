from scripts.objects.vehicle import Vehicle
from scripts.utils import table_helper
from scripts.utils.util import format_link, convert_int
from scripts.core.constants import RESOURCE_PATH, PBAR_FORMAT

TABLE_PATH = f"{RESOURCE_PATH}/tables/vehicle_table.json"
VEHICLE_BLACKLIST = ["Base.SportsCar_ez", "Base.ModernCar_Martin"]

table_map = {}

def generate_data(vehicle_id, table_type):
    vehicle = Vehicle(vehicle_id)
    
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")
    
    vehicle_data = {}

    name = vehicle.get_name()
    page = vehicle.get_page()
    link = format_link(name, page)

    vehicle_data["model"] = vehicle.get_model(is_single=False, do_format=True) if "model" in columns else None
    vehicle_data["name"] = link if "name" in columns else None
    vehicle_data["type"] = vehicle.get_vehicle_type() if "type" in columns else None
    vehicle_data["mass"] = convert_int(vehicle.get_mass()) if "mass" in columns else None
    vehicle_data["engine_force"] = convert_int(vehicle.get_engine_force()) if "engine_force" in columns else None
    vehicle_data["engine_quality"] = vehicle.get_engine_quality() if "engine_quality" in columns else None
    vehicle_data["engine_loudness"] = vehicle.get_engine_loudness() if "engine_loudness" in columns else None
    vehicle_data["max_speed"] = convert_int(vehicle.get_max_speed()) if "max_speed" in columns else None
    vehicle_data["suspension_stiffness"] = convert_int(vehicle.get_suspension_stiffness()) if "suspension_stiffness" in columns else None
    vehicle_data["front_health"] = vehicle.get_front_end_health() if "front_health" in columns else None
    vehicle_data["rear_health"] = vehicle.get_rear_end_health() if "rear_health" in columns else None
    vehicle_data["seats"] = vehicle.get_seats() if "seats" in columns else None
    vehicle_data["protection"] = convert_int(vehicle.get_player_damage_protection()) if "protection" in columns else None
    if "trunk_capacity" in columns:
        trunk_capacities = list(vehicle.get_trunk_capacity().values())
        trunk_capacities = [str(capacity) for capacity in trunk_capacities]
        if not trunk_capacities:
            trunk_capacities = ["-"]
        vehicle_data["trunk_capacity"] = " / ".join(trunk_capacities)
    if "animal_trailer_size" in columns:
        animal_trailer_size = convert_int(vehicle.get_animal_trailer_size()) if vehicle.get_animal_trailer_size() > 0 else "-"
        vehicle_data["animal_trailer_size"] = animal_trailer_size
    vehicle_data["vehicle_id"] = vehicle_id if "vehicle_id" in columns else None

    # Remove any values that are None
    vehicle_data = {k: v for k, v in vehicle_data.items() if v is not None}

    # Ensure column order is correct
    vehicle_data = {key: vehicle_data[key] for key in columns if key in vehicle_data}

    # Add item_name for sorting
    vehicle_data["item_name"] = name if "name" in columns else None

    return vehicle_data


def find_table_type(vehicle: Vehicle):
    if vehicle.is_trailer:
        table_type = "trailer"
#    elif vehicle.is_burnt:
#        table_type = "burnt"
#    elif vehicle.is_wreck:
#        table_type = "wrecked"
    else:
        table_type = "vehicle"

    return table_type


def find_vehicles():
    all_vehicle_data = {}
    vehicles = Vehicle.all()

    for vehicle_id in vehicles:
        # Skip blacklisted vehicles
        if vehicle_id in VEHICLE_BLACKLIST:
            continue
        
        vehicle = Vehicle(vehicle_id)

        # Skip vehicles that aren't parents
        if not vehicle.is_parent:
            continue

        table_type = find_table_type(vehicle)
        vehicle_data = generate_data(vehicle_id, table_type)

        if table_type not in all_vehicle_data:
            all_vehicle_data[table_type] = []
        
        all_vehicle_data[table_type].append(vehicle_data)

    return all_vehicle_data

def main():
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)
    all_vehicle_data = find_vehicles()
    table_helper.create_tables("vehicle", all_vehicle_data, table_map=table_map, columns=column_headings)

if __name__ == "__main__":
    main()
