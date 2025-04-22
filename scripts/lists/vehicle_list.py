from objects.vehicle import Vehicle
from scripts.core.file_loading import write_file
from scripts.utils.util import format_link

def generate_table(data):
    content = []
    content.append('{| class="wikitable theme-red sortable" style="text-align: center;"')
#    content.append("! Name\n! Variants\n!Type\n!Mass\n!Engine force\n!Engine loudness\n!Max speed\n!Braking force\n! Vehicle ID")
    content.append("! Name")
    content.append("! Type")
    content.append("! Mass")
    content.append("! Engine force")
    content.append("! Engine quality")
    content.append("! Engine loudness")
    content.append("! Max speed")
    content.append("! Braking force")
    content.append("! Suspesion compression")
    content.append("! Suspension damping")
    content.append("! Wheel friction")
    content.append("! Front health")
    content.append("! Rear health")
    content.append("! Seats")
    content.append("! Passenger protection")
    content.append("! Vehicle ID")
    for vehicle in data:
        vehicle_id = vehicle.get('vehicle_id')
        name = vehicle.get('name')
        page = vehicle.get('page')
        link = format_link(name, page)
        content.append(f'|-\n| {link}')
        raw_variants = vehicle.get('variants')
        variants = []
        if raw_variants:
            for variant_id in raw_variants:
                variant_veh = Vehicle(variant_id)
                if variant_veh.is_burnt or variant_veh.is_smashed:
                    continue
                variant = f"{variant_veh.get_name()}"

                variants.append(variant)
            if not variants:
                variants = ["-"]
        else:
            variants = ["-"]
#        content.append(f"| {'<br>'.join(variants)}")
        content.append(f'| style="white-space:nowrap" | {vehicle.get("type")}')
        content.append(f'| {vehicle.get("weight")}')
        content.append(f'| {vehicle.get("engine_force")}')
        content.append(f'| {vehicle.get("engine_quality")}')
        content.append(f'| {vehicle.get("engine_loudness")}')
        content.append(f'| {vehicle.get("max_speed")}')
        content.append(f'| {vehicle.get("braking_force")}')
        content.append(f'| {vehicle.get("suspension_compression")}')
        content.append(f'| {vehicle.get("suspension_damping")}')
        content.append(f'| {vehicle.get("wheel_friction")}')
        content.append(f'| {vehicle.get("front_end_health")}')
        content.append(f'| {vehicle.get("rear_end_health")}')
        content.append(f'| {vehicle.get("seats")}')
        content.append(f'| {vehicle.get("passenger_protection")}')
        content.append(f'| {vehicle_id}')
    content.append("|}")
    return content

def generate_data():
    vehicles = Vehicle.all()

    all_vehicle_data = []
    all_trailer_data = []
    for vehicle_id in vehicles:
        vehicle = Vehicle(vehicle_id)
#        if not vehicle.is_parent:
#            continue
        
        vehicle_data = {}
        vehicle_data["vehicle_id"] = vehicle_id
        vehicle = Vehicle(vehicle_id)
        vehicle_data["name"] = vehicle.get_name()
        vehicle_data["page"] = vehicle.get_page()
        vehicle_data["variants"] = vehicle.get_variants() if vehicle.get_variants() else None
        vehicle_data["type"] = vehicle.get_vehicle_type()
        vehicle_data["weight"] = vehicle.get_mass()
        vehicle_data["engine_force"] = vehicle.get_engine_force()
        vehicle_data["engine_quality"] = vehicle.get_engine_quality()
        vehicle_data["engine_loudness"] = vehicle.get_engine_loudness()
        vehicle_data["max_speed"] = vehicle.get_max_speed()
        vehicle_data["braking_force"] = vehicle.get_braking_force()
        vehicle_data["suspension_compression"] = vehicle.get_suspension_compression()
        vehicle_data["suspension_damping"] = vehicle.get_suspension_damping()
        vehicle_data["wheel_friction"] = vehicle.get_wheel_friction()
        vehicle_data["front_end_health"] = vehicle.get_front_end_health()
        vehicle_data["rear_end_health"] = vehicle.get_rear_end_health()
        vehicle_data["seats"] = vehicle.get_seats()
        vehicle_data["passenger_protection"] = vehicle.get_player_damage_protection()
#        vehicle_data["doors"] = vehicle.get_doors()
#        vehicle_data["trunk"] = vehicle.get_trunk()
#        vehicle_data["glove_box"] = vehicle.get_glove_box()

        if vehicle.get_type() == "trailer":
            all_trailer_data.append(vehicle_data)
        else:
            all_vehicle_data.append(vehicle_data)
    
    return sorted(all_vehicle_data, key=lambda x: x["name"] or ""), sorted(all_trailer_data, key=lambda x: x["name"] or "")

def main():
    vehicle_data, trailer_data = generate_data()
    content = generate_table(vehicle_data)
    trailer_content = generate_table(trailer_data)
    content.extend(trailer_content)
    write_file(content)

if __name__ == "__main__":
    main()
