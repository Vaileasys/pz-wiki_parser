"""Generate the clothing navbox from ClothingGroups."""

from pathlib import Path

from scripts.items.groups.clothing_groups import (
    ClothingGroups,
    get_wearable_location_id,
    is_wearable_item,
)
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo


OUTPUT_FILENAME = "clothing.json"
TABLE_NAME = "Clothing"


def build_clothing_navbox(section_order: list[str] | None = None) -> Navbox:
    """Build the clothing navbox, including Tails as its own section."""
    navbox = Navbox(TABLE_NAME)

    for item in Item.values():
        if not is_wearable_item(item):
            continue

        group_id = ClothingGroups.find_type(item)
        if group_id is None:
            continue

        location_id = get_wearable_location_id(item)
        if (
            group_id == ClothingGroups.DEFAULT_GROUP_ID
            and location_id
            and not ClothingGroups.is_known_body_location(location_id)
        ):
            echo.warning(
                f"Clothing body location '{location_id}' is not mapped for "
                f"'{item.item_id}'; adding item to 'Other'."
            )

        page_name = item.page
        if not item.has_page:
            echo.warning(f"Clothing item does not have a page: {item.item_id}")

        navbox.add_item(ClothingGroups.get_display_name(group_id), page_name)

    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(
        section_order or ClothingGroups.get_section_order()
    )
    return navbox


def generate_clothing_navbox(
    output_dir: str | Path | None = None,
    section_order: list[str] | None = None,
) -> Path:
    """Generate and save the clothing navbox JSON file."""
    navbox = build_clothing_navbox(section_order=section_order)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved clothing navbox: {path}")
    return path


def main() -> None:
    generate_clothing_navbox()


if __name__ == "__main__":
    main()
