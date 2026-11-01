"""Generate the light-source navbox from LightSourceGroups."""

from pathlib import Path
from scripts.items.groups.light_source_groups import LightSourceGroups, is_light_source_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "light_source.json"
TABLE_NAME = "Light sources"


def build_light_source_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_light_source_item(item):
            continue
        group_id = LightSourceGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Light-source item does not have a page: {item.item_id}")
        navbox.add_item(LightSourceGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or LightSourceGroups.get_section_order())
    return navbox


def generate_light_source_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_light_source_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved light-source navbox: {path}")
    return path


def main() -> None:
    generate_light_source_navbox()


if __name__ == "__main__":
    main()

