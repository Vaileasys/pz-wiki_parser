"""Generate the household navbox from HouseholdGroups."""

from pathlib import Path
from scripts.items.groups.household_groups import HouseholdGroups, is_household_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "household.json"
TABLE_NAME = "Household"


def build_household_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_household_item(item):
            continue
        group_id = HouseholdGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Household item does not have a page: {item.item_id}")
        navbox.add_item(HouseholdGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or HouseholdGroups.get_section_order())
    return navbox


def generate_household_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_household_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved household navbox: {path}")
    return path


def main() -> None:
    generate_household_navbox()


if __name__ == "__main__":
    main()

