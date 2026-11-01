"""Generate the electronics navbox from ElectronicsGroups."""

from pathlib import Path
from scripts.items.groups.electronics_groups import ElectronicsGroups, is_electronics_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "electronics.json"
TABLE_NAME = "Electronics"


def build_electronics_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_electronics_item(item):
            continue
        group_id = ElectronicsGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Electronics item does not have a page: {item.item_id}")
        navbox.add_item(ElectronicsGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or ElectronicsGroups.get_section_order())
    return navbox


def generate_electronics_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_electronics_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved electronics navbox: {path}")
    return path


def main() -> None:
    generate_electronics_navbox()


if __name__ == "__main__":
    main()

