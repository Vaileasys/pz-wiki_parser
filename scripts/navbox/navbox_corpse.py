"""Generate the corpse navbox from CorpseGroups."""

from pathlib import Path
from scripts.items.groups.corpse_groups import CorpseGroups, is_corpse_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "corpse.json"
TABLE_NAME = "Corpses"


def build_corpse_navbox(section_order: list[str] | None = None) -> Navbox:
    from scripts.objects.animal import Animal

    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_corpse_item(item) or item.item_id == "Base.CorpseAnimal":
            continue
        group_id = CorpseGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Corpse item does not have a page: {item.item_id}")
        navbox.add_item(CorpseGroups.get_display_name(group_id), item.page)

    animal_item = Item("Base.CorpseAnimal")
    group_id = CorpseGroups.find_type(animal_item, stage="dead")
    for animal in Animal.all().values():
        for breed in animal.breeds:
            navbox.add_item(
                CorpseGroups.get_display_name(group_id),
                breed.page,
                breed.get_name("dead"),
            )

    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or CorpseGroups.get_section_order())
    return navbox


def generate_corpse_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_corpse_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved corpse navbox: {path}")
    return path


def main() -> None:
    generate_corpse_navbox()


if __name__ == "__main__":
    main()
