"""Generate the communication navbox from CommunicationGroups."""

from pathlib import Path
from scripts.items.groups.communication_groups import CommunicationGroups, is_communication_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "communication.json"
TABLE_NAME = "Communication"


def build_communication_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_communication_item(item):
            continue
        group_id = CommunicationGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Communication item does not have a page: {item.item_id}")
        navbox.add_item(CommunicationGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or CommunicationGroups.get_section_order())
    return navbox


def generate_communication_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_communication_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved communication navbox: {path}")
    return path


def main() -> None:
    generate_communication_navbox()


if __name__ == "__main__":
    main()

