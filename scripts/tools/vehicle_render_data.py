# Outputs a JSON file with rendering data (mesh and texture) to be used in blender project.

from scripts.objects.vehicle import Vehicle
from scripts.core.cache import save_json
from scripts.utils.echo import echo_success
from scripts.core.constants import OUTPUT_PATH

PATH = f"{OUTPUT_PATH}/vehicle_render_data.json"

def main():
    vehicles = Vehicle.all()
    vehicle_mesh_data = {}

    for vehicle in vehicles:
        vehicle_mesh_data[vehicle] = {}
        vehicle_mesh_data[vehicle]["mesh"] = Vehicle(vehicle).get_mesh_path()
        vehicle_mesh_data[vehicle]["texture"] = Vehicle(vehicle).get_texture_path()

    save_json(PATH, vehicle_mesh_data)
    echo_success(f"JSON file saved to '{PATH}'")

if __name__ == "__main__":
    main()