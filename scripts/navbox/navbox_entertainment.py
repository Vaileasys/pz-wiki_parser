"""Generate the entertainment navbox from EntertainmentGroups."""

from pathlib import Path
from scripts.items.groups.entertainment_groups import EntertainmentGroups, is_entertainment_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "entertainment.json"
TABLE_NAME = "Entertainment"


def build_entertainment_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_entertainment_item(item):
            continue
        group_id = EntertainmentGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Entertainment item does not have a page: {item.item_id}")
        navbox.add_item(EntertainmentGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or EntertainmentGroups.get_section_order())
    return navbox


def generate_entertainment_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_entertainment_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved entertainment navbox: {path}")
    return path


def main() -> None:
    generate_entertainment_navbox()


if __name__ == "__main__":
    main()

