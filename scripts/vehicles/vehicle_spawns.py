import os
import copy
from scripts.core.cache import save_cache, load_cache
from scripts.utils.lua_helper import load_lua_file, parse_lua_tables, LUA_EVENTS
from scripts.core.file_loading import write_file
from scripts.utils import echo
from scripts.parser.zone_parser import get_zone_data, get_coord
from scripts.core.constants import VEHICLE_DIR
from scripts.objects.vehicle import Vehicle

DEF_CACHE_FILE = "vehicle_zone_def_data.json"
PROF_CACHE_FILE = "vehicle_profession_data.json"
FILTER = (
    "trafficjam", "trafficjams", "trafficjamn", "trafficjamw", "trafficjame", "trafficjamne",
    "rtrafficjame", "rtrafficjams", "rtrafficjamn", "rtrafficjamw", "rtrafficjamns",
    "", "good", "bad", "badsss", "junkyard", "medium", "burnt"
    )

_zone_defs = {}
_vehicle_zones = {}
_profession_vehicles = {}


## ------------------------- Vehicle Spawns ------------------------- ##

def generate_vehicle_data():
    """Generates spawn location and rate per vehicle."""
    for vehicle_id, zones in _vehicle_zones.items():
        vehicle_id = Vehicle.fix_vehicle_id(vehicle_id)
        content = []
        content.append('<div class="list-columns">')
        for zone, zone_data in zones.items():
            spawn_rate = zone_data.get('spawnRate', 16)
            spawn_chance = zone_data.get('spawnChance', 0)
            actual_spawn = (spawn_rate * spawn_chance) / 100
            content.append(f"*{zone} ({actual_spawn:.2f}%)")
        content.append('</div>\n')
        write_file(content, rel_path=vehicle_id + ".txt", root_path=os.path.join(VEHICLE_DIR, "vehicle_spawns"), suppress=True)


## ------------------------- Vehicle Parking Zones ------------------------- ##

def generate_zone_data(spawn_data: dict, output_dict: dict) -> dict:
    for name, data_list in spawn_data.items():
        if name not in output_dict:
            output_dict[name] = []

        for data in data_list:
            coords = get_coord(data)
            
            output_dict[name].append(coords)

    return output_dict


def construct_zone_list(data):
    content_data = {}
    for name, coords in data.items():
        name = "generic" if not name else name
        content_data[name] = []

#        if name in FILTER:
#            echo.debug(f"Skipping '{name}' due to filter match.")
#            continue

        content = []
        content.append('<div class="list-columns">')
        content.extend([f"* {coord}" for coord in coords])
        content.append('</div>\n')

        content_data[name].extend(content)

    return content_data


def generate_zone_article(data):
    for name, location_content in data.items():
        content = []
        content.append("==Locations==")
        content.extend(location_content)

        vehicles = get_zone_defs().get(name.lower(), {}).get("vehicles", {})
        if not vehicles:
            echo.warning(f"Couldn't find a vehicle zone def for '{name}'")
        
        vehicles_content = []
        for vehicle_id, veh_data in vehicles.items():
            vehicle = Vehicle(vehicle_id)
            if vehicle is None:
                continue
            veh_name = vehicle.get_link()
            veh_spawn_chance = veh_data.get("spawnChance", 0)
            vehicles_content.append(f"* {veh_name} ({vehicle_id}) ({veh_spawn_chance}%)")
        
        if vehicles_content:
            content.append("==Vehicles==")
            content.extend(vehicles_content)


        write_file(content, rel_path=name + ".txt", root_path=os.path.join(VEHICLE_DIR, "vehicle_parking_stalls"))

## ------------------------- Util ------------------------- ##

def restructure_zone_defs():
    """Rearrange zone definitions to be structured by vehicle."""
    global _vehicle_zones
    zone_defs = copy.deepcopy(get_zone_defs())

    for zone, zone_data in zone_defs.items():
        vehicles = zone_data.pop("vehicles", {})
        other_data = {key: value for key, value in zone_data.items()}

        for vehicle, vehicle_info in vehicles.items():
            if vehicle not in _vehicle_zones:
                _vehicle_zones[vehicle] = {}

            _vehicle_zones[vehicle][zone] = {**vehicle_info, **other_data}

    save_cache(_vehicle_zones, "restructured_vehicle_data.json")

    return _vehicle_zones


## ------------------------- Parsers ------------------------- ##

def get_zone_defs():
    if not _zone_defs:
        parse_zone_defs()
    return _zone_defs

def parse_zone_defs():
    """Parses tables in VehicleZoneDefinition.lua"""
    global _zone_defs

    lua_runtime = load_lua_file(lua_files="VehicleZoneDefinition.lua", media_type="lua")
    _zone_defs = parse_lua_tables(lua_runtime)

    _zone_defs = _zone_defs.get("VehicleZoneDistribution", {})

    save_cache(_zone_defs, DEF_CACHE_FILE)

    return _zone_defs


def get_profession_vehicles():
    if not _profession_vehicles:
        parse_profession_vehicles()
    return _profession_vehicles

def parse_profession_vehicles():
    """Parses tables in ProfessionVehicles.lua"""
    global _profession_vehicles

    lua_runtime = load_lua_file(lua_files="ProfessionVehicles.lua", media_type="lua", prefer="Vehicles", inject_lua=LUA_EVENTS)
    _profession_vehicles = parse_lua_tables(lua_runtime, tables=["ProfessionVehicles"])

    save_cache(_profession_vehicles, PROF_CACHE_FILE)


## ------------------------- Init ------------------------- ##

def main():
    zone_coords = get_zone_data("ParkingStall")
    parse_zone_defs()
    restructure_zone_defs()
    generate_vehicle_data()
    parse_profession_vehicles()

    content_data = {}
    content_data = generate_zone_data(zone_coords, content_data)
    content_data = construct_zone_list(content_data)
    generate_zone_article(content_data)


if __name__ == "__main__":
    main()