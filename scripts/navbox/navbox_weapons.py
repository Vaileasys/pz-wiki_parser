from pathlib import Path

from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

from scripts.items.lists import item_list_weapon
from scripts.items.groups.weapon_groups import WeaponGroups


OUTPUT_FILENAME = "weapons.json"



def reset_weapon_list_state():
    item_list_weapon.box_types.clear()
    item_list_weapon.table_map.clear()
    item_list_weapon.table_type_map.clear()
    item_list_weapon.all_item_data.clear()


def prepare_weapon_item_data():
    reset_weapon_list_state()

    item_list_weapon.find_boxes()
    item_list_weapon.find_items()

    return item_list_weapon.all_item_data


def build_weapon_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox("Weapons")

    weapon_data = prepare_weapon_item_data()
    
    # Get type-to-display mapping from WeaponGroups
    type_to_display = WeaponGroups.get_type_to_display_map()

    for item_id, item_data in weapon_data.items():
        table_type = item_data.get("TableType")

        if not table_type:
            echo.warning(f"Skipping weapon item with no table type: {item_id}")
            continue

        item = Item(item_id)

        if not item.valid:
            echo.warning(f"Skipping invalid weapon item: {item_id}")
            continue

        page_name = item.page

        if not item.has_page:
            echo.warning(f"Weapon item does not have a page: {item_id}")

        # Use centralized type-to-display mapping
        section_name = type_to_display.get(table_type, table_type)
        navbox.add_item(section_name, page_name)

    navbox.sort(sections=False, items=True)

    # Use centralized section ordering if not provided
    if section_order is None:
        section_order = WeaponGroups.get_section_order()
    navbox.sort_sections_by_order(section_order)

    return navbox


def generate_weapon_navbox(
    output_dir: str | Path | None = None,
    section_order: list[str] | None = None,
) -> Path:
    navbox = build_weapon_navbox(section_order=section_order)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)

    echo.success(f"Saved weapon navbox: {path}")
    return path


def main():
    generate_weapon_navbox()


if __name__ == "__main__":
    main()