import os

from scripts.objects.item import Item
from scripts.objects.vehicle import Vehicle
from scripts.objects.vehicle_part import VehiclePart
from scripts.core import file_loading, constants
from scripts.utils import echo

test_dir = os.path.join(constants.OUTPUT_LANG_DIR, "tests")

def list_feed_types():
    """Generates a list of animal feed types."""
    feed_types = {}
    for item_id, item in Item.items():
        if item.animal_feed_type:
            if item.animal_feed_type not in feed_types:
                feed_types[item.animal_feed_type] = []
            feed_types[item.animal_feed_type].append(item_id)

    content = []
    for feed_type, items in feed_types.items():
        content.append(f"== {feed_type} ==")
        content.extend(items)
        content.append("")

    file_loading.write_file(content, rel_path="feed_types.txt", root_path=test_dir)


def list_vehicle_parts():
    """Generates a list of vehicle parts grouped by vehicle type."""
    grouped = {}

    # Group vehicles by type
    for vehicle_id, vehicle in Vehicle.all().items():
        if not vehicle.parts.all() or vehicle.is_burnt or vehicle.is_wreck:
            continue

        vehicle_type = vehicle.get_vehicle_type()
        if vehicle_type not in grouped:
            grouped[vehicle_type] = []
        grouped[vehicle_type].append((vehicle_id, vehicle))

    content = []

    # Format content to be written
    for vehicle_type in sorted(grouped):
        content.append(f"== {vehicle_type} ==")

        vehicles: list[tuple[str, Vehicle]] = grouped[vehicle_type]
        for vehicle_id, vehicle in sorted(vehicles, key=lambda x: x[0]):
            content.append(f"=== [[{vehicle.page}|{vehicle_id}]] ===")

            for part in sorted(vehicle.parts.all(), key=lambda p: p.wiki_link.lower()):
                content.append(f"* {part.wiki_link}")

                if part.install.skills:
                    skills_str = ", ".join(f"{k} {v}" for k, v in part.install.skills.items())
                    magazine = f" ({part.install.recipes})" if part.install.recipes else ""
                    content.append(f"** Install: {skills_str}{magazine}")

                if part.uninstall.skills:
                    skills_str = ", ".join(f"{k} {v}" for k, v in part.uninstall.skills.items())
                    magazine = f" ({part.uninstall.recipes})" if part.uninstall.recipes else ""
                    content.append(f"** Uninstall: {skills_str}{magazine}")

            content.append("")

    file_loading.write_file(content, rel_path="vehicle_parts.txt", root_path=test_dir)


def main():
    echo.info("Running 'test' module...")
    list_vehicle_parts()


if __name__ == "__main__":
    main()