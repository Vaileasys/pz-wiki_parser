"""Generate the weapon navbox."""

from pathlib import Path
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

from scripts.items.groups.ammo_groups import AmmoGroups
from scripts.items.groups.weapon_groups import WeaponGroups
from scripts.items.item_groups import ItemGroups


OUTPUT_FILENAME = "weapons.json"

GROUP_CLASSES: tuple[type[ItemGroups], ...] = (
    WeaponGroups,
    AmmoGroups,
)

SECTION_ORDER = [
    *WeaponGroups.get_section_order(),
    *AmmoGroups.get_section_order(),
]


def get_item_section(item: Item) -> str | None:
    """Return the display section for a weapon-related item."""
    for group_class in GROUP_CLASSES:
        type_id = group_class.find_type(item)
        if type_id is not None:
            return group_class.get_display_name(type_id)

    return None


def build_weapon_navbox(section_order: list[str] | None = None) -> Navbox:
    """Build a navbox containing weapons, ammunition, and weapon parts."""
    navbox = Navbox("Weapons")

    for item in Item.values():
        if not item.valid:
            echo.warning(f"Skipping invalid weapon item: {item.item_id}")
            continue

        section_name = get_item_section(item)
        if section_name is None:
            continue

        page_name = item.page
        if not item.has_page:
            echo.warning(f"Weapon item does not have a page: {item.item_id}")

        navbox.add_item(section_name, page_name)

    navbox.sort(sections=False, items=True)

    if section_order is None:
        section_order = SECTION_ORDER
    navbox.sort_sections_by_order(section_order)

    return navbox


def generate_weapon_navbox(
    output_dir: str | Path | None = None,
    section_order: list[str] | None = None,
) -> Path:
    """Generate and save the weapon navbox JSON file."""
    navbox = build_weapon_navbox(section_order=section_order)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)

    echo.success(f"Saved weapon navbox: {path}")
    return path


def main():
    generate_weapon_navbox()


if __name__ == "__main__":
    main()