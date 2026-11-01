"""Generate the medical navbox from MedicalGroups."""

from pathlib import Path
from scripts.items.groups.medical_groups import MedicalGroups, is_medical_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "medical.json"
TABLE_NAME = "Medical"


def build_medical_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_medical_item(item):
            continue
        group_id = MedicalGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Medical item does not have a page: {item.item_id}")
        navbox.add_item(MedicalGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or MedicalGroups.get_section_order())
    return navbox


def generate_medical_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_medical_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved medical navbox: {path}")
    return path


def main() -> None:
    generate_medical_navbox()


if __name__ == "__main__":
    main()

