"""Generate the camping navbox from CampingGroups."""

from pathlib import Path

from scripts.items.groups.camping_groups import CampingGroups, is_camping_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo


OUTPUT_FILENAME = "camping.json"
TABLE_NAME = "Camping"


def build_camping_navbox(section_order: list[str] | None = None) -> Navbox:
    """Build a navbox containing grouped camping item pages."""
    navbox = Navbox(TABLE_NAME)

    for item in Item.values():
        if not is_camping_item(item):
            continue

        group_id = CampingGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Camping item does not have a page: {item.item_id}")

        navbox.add_item(CampingGroups.get_display_name(group_id), item.page)

    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(
        section_order or CampingGroups.get_section_order()
    )
    return navbox


def generate_camping_navbox(
    output_dir: str | Path | None = None,
    section_order: list[str] | None = None,
) -> Path:
    """Generate and save the camping navbox JSON file."""
    navbox = build_camping_navbox(section_order=section_order)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved camping navbox: {path}")
    return path


def main() -> None:
    generate_camping_navbox()


if __name__ == "__main__":
    main()
