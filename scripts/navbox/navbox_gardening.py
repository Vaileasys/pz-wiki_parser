"""Generate the gardening navbox from GardeningGroups."""

from pathlib import Path
from scripts.items.groups.gardening_groups import GardeningGroups, is_gardening_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "gardening.json"
TABLE_NAME = "Gardening"


def build_gardening_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_gardening_item(item):
            continue
        group_id = GardeningGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Gardening item does not have a page: {item.item_id}")
        navbox.add_item(GardeningGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or GardeningGroups.get_section_order())
    return navbox


def generate_gardening_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_gardening_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved gardening navbox: {path}")
    return path


def main() -> None:
    generate_gardening_navbox()


if __name__ == "__main__":
    main()

