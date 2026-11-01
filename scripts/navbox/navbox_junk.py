"""Generate the junk navbox from JunkGroups."""

from pathlib import Path
from scripts.items.groups.junk_groups import JunkGroups, is_junk_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "junk.json"
TABLE_NAME = "Junk"


def build_junk_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_junk_item(item):
            continue
        group_id = JunkGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Junk item does not have a page: {item.item_id}")
        navbox.add_item(JunkGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or JunkGroups.get_section_order())
    return navbox


def generate_junk_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_junk_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved junk navbox: {path}")
    return path


def main() -> None:
    generate_junk_navbox()


if __name__ == "__main__":
    main()

