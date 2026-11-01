"""Generate the fuel navbox from FuelGroups."""

from pathlib import Path
from scripts.items.groups.fuel_groups import FuelGroups, is_fuel_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "fuel.json"
TABLE_NAME = "Fuel"


def build_fuel_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_fuel_item(item):
            continue
        group_id = FuelGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Fuel item does not have a page: {item.item_id}")
        navbox.add_item(FuelGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or FuelGroups.get_section_order())
    return navbox


def generate_fuel_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_fuel_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved fuel navbox: {path}")
    return path


def main() -> None:
    generate_fuel_navbox()


if __name__ == "__main__":
    main()

