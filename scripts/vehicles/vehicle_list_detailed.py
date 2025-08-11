import os
from scripts.objects.vehicle import Vehicle
from scripts.utils import table_helper
from scripts.utils.util import link, convert_int
from scripts.core.constants import RESOURCE_DIR, PBAR_FORMAT, VEHICLE_DIR
from scripts.core.cache import save_cache

TABLE_PATH = f"{RESOURCE_DIR}/tables/vehicle_table.json"
VEHICLE_BLACKLIST = ["Base.SportsCar_ez", "Base.ModernCar_Martin"]

table_map = {}

def check_dash(value, vehicle: Vehicle, burnt=False, wreck=False):
    """Checks if the value should be a dash instead of None or the usual returned value."""
    is_burnt = vehicle.is_burnt
    is_wreck = vehicle.is_wreck

    if burnt and is_burnt:
        return "-"
    elif wreck and is_wreck:
        return "-"
    else:
        return value

def generate_data(vehicle: Vehicle, table_type, section_type="vehicle"):
    
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")
    
    vehicle_data = {}

    model = vehicle.get_models() if section_type == "vehicle" else vehicle.get_model()
    name = vehicle.wiki_link if section_type == "parent" else link(vehicle.page)

    vehicle_data["model"] = model if "model" in columns else None
    vehicle_data["name"] = name if "name" in columns else None
    vehicle_data["type"] = vehicle.get_vehicle_type() if "type" in columns else None
    vehicle_data["mass"] = convert_int(vehicle.get_mass()) if "mass" in columns else None
    vehicle_data["engine_power"] = check_dash(convert_int(vehicle.get_engine_power()), vehicle, True, True) if "engine_power" in columns else None
    vehicle_data["engine_quality"] = check_dash(vehicle.get_engine_quality(), vehicle, True, True) if "engine_quality" in columns else None
    vehicle_data["engine_loudness"] = check_dash(vehicle.get_engine_loudness(), vehicle, True, True) if "engine_loudness" in columns else None
    vehicle_data["max_speed"] = check_dash(convert_int(vehicle.get_max_speed()), vehicle, True, True) if "max_speed" in columns else None
    vehicle_data["suspension_stiffness"] = check_dash(convert_int(vehicle.get_suspension_stiffness()), vehicle, True, True) if "suspension_stiffness" in columns else None
    vehicle_data["seats"] = check_dash(vehicle.get_seats(), vehicle, True, False) if "seats" in columns else None
    vehicle_data["protection"] = check_dash(convert_int(vehicle.get_player_damage_protection()), vehicle, True, True) if "protection" in columns else None
    vehicle_data["glove_box_capacity"] = check_dash(convert_int(vehicle.get_glove_box_capacity()), vehicle, True, False) if "glove_box_capacity" in columns else None
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
            vehicle_data["lightbar"] = '[[File:UI_Tick.png|link=|Has lightbar and siren]]'
        else:
            vehicle_data["lightbar"] = '[[File:UI_Cross.png|link=|No lightbar and siren]]'


    vehicle_data["vehicle_id"] = vehicle.vehicle_id if "vehicle_id" in columns else None

    # Remove any values that are None
    vehicle_data = {k: v for k, v in vehicle_data.items() if v is not None}

    # Ensure column order is correct
    vehicle_data = {key: vehicle_data[key] for key in columns if key in vehicle_data}

    # Add item_name for sorting
    vehicle_data["item_name"] = vehicle.name if "name" in columns else None

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

    for vehicle_id, vehicle in Vehicle.all().items():
        # Skip blacklisted vehicles
        if vehicle_id in VEHICLE_BLACKLIST:
            continue

        # Skip vehicles that aren't parents
        if not vehicle.is_parent and section_type == "vehicle":
            continue
        if section_type != "parent" and (vehicle.is_burnt or vehicle.is_wreck):
            continue

        table_type = find_table_type(vehicle, section_type)
        vehicle_data = generate_data(vehicle, table_type, section_type)

        if table_type not in all_vehicle_data:
            all_vehicle_data[table_type] = []
        
        all_vehicle_data[table_type].append(vehicle_data)

    return all_vehicle_data

def main():
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)

    all_vehicle_data = find_vehicles("vehicle")
    all_vehicle_data_parent = find_vehicles("parent")

    veh_type = os.path.join("lists", "vehicle_list")
    veh_type_parent = os.path.join("lists", "vehicle_variants")

    PARENT_HEADER = '{| class="wikitable theme-red sortable sticky-column mw-collapsible" style="text-align: center;" data-expandtext="{{int:show}}" data-collapsetext="{{int:hide}}"'
    PARENT_CAPTION = 'style="min-width:300px;" | Variants list'

    table_helper.create_tables(
        veh_type,
        all_vehicle_data,
        table_map=table_map,
        columns=column_headings,
        root_path=VEHICLE_DIR,
        bot_flag_type="vehicle_list",
        suppress=True,
        combine_tables=False
        )
    table_helper.create_tables(
        veh_type_parent,
        all_vehicle_data_parent,
        table_map=table_map,
        table_header=PARENT_HEADER,
        caption=PARENT_CAPTION,
        columns=column_headings,
        root_path=VEHICLE_DIR,
        bot_flag_type="vehicle_variants",
        suppress=True,
        combine_tables=False
        )

if __name__ == "__main__":
    main()
