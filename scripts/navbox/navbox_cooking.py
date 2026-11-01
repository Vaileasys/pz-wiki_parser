"""Generate the cooking navbox from CookingGroups."""

from pathlib import Path
from scripts.items.groups.cooking_groups import CookingGroups, is_cooking_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "cooking.json"
TABLE_NAME = "Cooking"


def build_cooking_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_cooking_item(item):
            continue
        group_id = CookingGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Cooking item does not have a page: {item.item_id}")
        navbox.add_item(CookingGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or CookingGroups.get_section_order())
    return navbox


def generate_cooking_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_cooking_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved cooking navbox: {path}")
    return path


def main() -> None:
    generate_cooking_navbox()


if __name__ == "__main__":
    main()

