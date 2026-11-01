"""Generate the material navbox from MaterialGroups."""

from pathlib import Path
from scripts.items.groups.material_groups import MaterialGroups, is_material_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "material.json"
TABLE_NAME = "Materials"


def build_material_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_material_item(item):
            continue
        group_id = MaterialGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Material item does not have a page: {item.item_id}")
        navbox.add_item(MaterialGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or MaterialGroups.get_section_order())
    return navbox


def generate_material_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_material_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved material navbox: {path}")
    return path


def main() -> None:
    generate_material_navbox()


if __name__ == "__main__":
    main()

