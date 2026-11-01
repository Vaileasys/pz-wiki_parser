"""Generate the food navbox from the shared FoodGroups classifier."""

from pathlib import Path

from scripts.items.groups.food_groups import FoodGroups, include_in_food_groups
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo


OUTPUT_FILENAME = "food.json"
TABLE_NAME = "Food"


def build_food_navbox(section_order: list[str] | None = None) -> Navbox:
    """Build a navbox containing the grouped food item pages."""
    navbox = Navbox(TABLE_NAME)

    for item in Item.values():
        if not item.valid:
            echo.warning(f"Skipping invalid food item: {item.item_id}")
            continue
        if not include_in_food_groups(item):
            continue

        group_id = FoodGroups.find_type(item)
        page_name = item.page

        if not item.has_page:
            echo.warning(f"Food item does not have a page: {item.item_id}")

        navbox.add_item(FoodGroups.get_display_name(group_id), page_name)

    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(
        section_order or FoodGroups.get_section_order()
    )
    return navbox


def generate_food_navbox(
    output_dir: str | Path | None = None,
    section_order: list[str] | None = None,
) -> Path:
    """Generate and save the food navbox JSON file."""
    navbox = build_food_navbox(section_order=section_order)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved food navbox: {path}")
    return path


def main() -> None:
    generate_food_navbox()


if __name__ == "__main__":
    main()
