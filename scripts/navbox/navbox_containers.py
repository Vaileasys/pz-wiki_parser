"""Generate the containers navbox from ContainerGroups."""

from pathlib import Path

from scripts.items.groups.container_groups import (
    ContainerGroups,
    is_container_item,
)
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo


OUTPUT_FILENAME = "containers.json"
TABLE_NAME = "Containers"


def build_containers_navbox(section_order: list[str] | None = None) -> Navbox:
    """Build a navbox containing grouped container item pages."""
    navbox = Navbox(TABLE_NAME)

    for item in Item.values():
        if not is_container_item(item):
            continue

        group_id = ContainerGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Container item does not have a page: {item.item_id}")

        navbox.add_item(ContainerGroups.get_display_name(group_id), item.page)

    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(
        section_order or ContainerGroups.get_section_order()
    )
    return navbox


def generate_containers_navbox(
    output_dir: str | Path | None = None,
    section_order: list[str] | None = None,
) -> Path:
    """Generate and save the containers navbox JSON file."""
    navbox = build_containers_navbox(section_order=section_order)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved containers navbox: {path}")
    return path


def main() -> None:
    generate_containers_navbox()


if __name__ == "__main__":
    main()
