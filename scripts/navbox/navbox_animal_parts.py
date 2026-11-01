"""Generate the animal-parts navbox from AnimalPartGroups."""

from pathlib import Path

from scripts.items.groups.animal_part_groups import AnimalPartGroups
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo


OUTPUT_FILENAME = "animal_parts.json"
TABLE_NAME = "Animal parts"


def build_animal_parts_navbox(
    section_order: list[str] | None = None,
) -> Navbox:
    """Build a navbox containing grouped animal-part item pages."""
    navbox = Navbox(TABLE_NAME)

    for item_id in AnimalPartGroups.get_item_ids():
        item = Item(item_id)
        if not item.valid:
            echo.warning(f"Skipping invalid animal-part item: {item_id}")
            continue

        group_id = AnimalPartGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Animal-part item does not have a page: {item.item_id}")

        navbox.add_item(AnimalPartGroups.get_display_name(group_id), item.page)

    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(
        section_order or AnimalPartGroups.get_section_order()
    )
    return navbox


def generate_animal_parts_navbox(
    output_dir: str | Path | None = None,
    section_order: list[str] | None = None,
) -> Path:
    """Generate and save the animal-parts navbox JSON file."""
    navbox = build_animal_parts_navbox(section_order=section_order)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved animal-parts navbox: {path}")
    return path


def main() -> None:
    generate_animal_parts_navbox()


if __name__ == "__main__":
    main()
