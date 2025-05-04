from scripts.objects.vehicle import Vehicle
from scripts.core.file_loading import write_file
from scripts.utils.util import format_link
from scripts.core.constants import VEHICLE_DIR

def generate_table(data):
    content = []

    for vtype in sorted(data.keys()):
        content.append(f"=={vtype}==")
        content.append('{| class="wikitable theme-red sortable" style="text-align: center;"')
        content.append("! Model")
        content.append("! Name")
        content.append("! Vehicle ID")

        for vehicle in data[vtype]:
            content.append("|-")
            content.append("| " + vehicle.get('model'))
            content.append("| " + vehicle.get('link'))
            content.append("| " + vehicle.get('vehicle_id'))

        content.append("|}\n")

    return content

def generate_data():
    vehicles_data = {}
    vehicles = Vehicle.all()

    for vehicle_id in vehicles:
        vehicle = Vehicle(vehicle_id)
        name = vehicle.get_name()
        page = vehicle.get_page()
        link = format_link(name, page)

        vtype = "Trailer" if vehicle.is_trailer else vehicle.get_full_parent().get_name()

        if vtype not in vehicles_data:
            vehicles_data[vtype] = []

        processed_vehicle = {
            "name": name,
            "link": link,
            "model": f'[[File:{vehicle.get_model()}|128x128px]]',
            "vehicle_id": vehicle_id
        }

        vehicles_data[vtype].append(processed_vehicle)

    for vtype in vehicles_data:
        vehicles_data[vtype] = sorted(vehicles_data[vtype], key=lambda x: x["name"] or "")

    return vehicles_data

def main():
    vehicle_data = generate_data()
    content = generate_table(vehicle_data)
    write_file(content, rel_path="vehicle_list.txt", root_path=VEHICLE_DIR)

if __name__ == "__main__":
    main()
