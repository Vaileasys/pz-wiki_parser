"""Generate the accessories navbox from AccessoryGroups."""

from pathlib import Path

from scripts.items.groups.clothing_groups import (
    AccessoryGroups,
    is_wearable_item,
)
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo


OUTPUT_FILENAME = "accessories.json"
TABLE_NAME = "Accessories"


def build_accessories_navbox(section_order: list[str] | None = None) -> Navbox:
    """Build the accessories navbox using the wiki accessory sections."""
    navbox = Navbox(TABLE_NAME)

    for item in Item.values():
        if not is_wearable_item(item):
            continue

        group_id = AccessoryGroups.find_type(item)
        if group_id is None:
            continue

        page_name = item.page
        if not item.has_page:
            echo.warning(f"Accessory item does not have a page: {item.item_id}")

        navbox.add_item(AccessoryGroups.get_display_name(group_id), page_name)

    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(
        section_order or AccessoryGroups.get_section_order()
    )
    return navbox


def generate_accessories_navbox(
    output_dir: str | Path | None = None,
    section_order: list[str] | None = None,
) -> Path:
    """Generate and save the accessories navbox JSON file."""
    navbox = build_accessories_navbox(section_order=section_order)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved accessories navbox: {path}")
    return path


def main() -> None:
    generate_accessories_navbox()


if __name__ == "__main__":
    main()
