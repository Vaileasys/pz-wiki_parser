"""Generate the fishing navbox from FishingGroups."""

from pathlib import Path
from scripts.items.groups.fishing_groups import FishingGroups, is_fishing_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "fishing.json"
TABLE_NAME = "Fishing"


def build_fishing_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_fishing_item(item):
            continue
        group_id = FishingGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Fishing item does not have a page: {item.item_id}")
        navbox.add_item(FishingGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or FishingGroups.get_section_order())
    return navbox


def generate_fishing_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_fishing_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved fishing navbox: {path}")
    return path


def main() -> None:
    generate_fishing_navbox()


if __name__ == "__main__":
    main()

