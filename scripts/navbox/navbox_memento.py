"""Generate the memento navbox from MementoGroups."""

from pathlib import Path
from scripts.items.groups.memento_groups import MementoGroups, is_memento_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "memento.json"
TABLE_NAME = "Mementos"


def build_memento_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_memento_item(item):
            continue
        group_id = MementoGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Memento item does not have a page: {item.item_id}")
        navbox.add_item(MementoGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or MementoGroups.get_section_order())
    return navbox


def generate_memento_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_memento_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved memento navbox: {path}")
    return path


def main() -> None:
    generate_memento_navbox()


if __name__ == "__main__":
    main()

