"""Generate the literature navbox from LiteratureGroups."""

from pathlib import Path

from scripts.core.language import Translate
from scripts.items.groups.literature_groups import LiteratureGroups, is_literature_item
from scripts.items.lists.item_list_literature import get_region
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.parser import stash_parser
from scripts.utils import echo

OUTPUT_FILENAME = "literature.json"
TABLE_NAME = "Literature"


def build_literature_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_literature_item(item):
            continue
        group_id = LiteratureGroups.find_type(item)
        if not item.has_page:
            echo.warning(f"Literature item does not have a page: {item.item_id}")
        navbox.add_item(LiteratureGroups.get_display_name(group_id), item.page)

    for region_data in stash_parser.get_stash_data().values():
        for map_id, map_data in region_data.items():
            group_id = LiteratureGroups.find_type(
                Item(map_data["item"]), special_data={"map_id": map_id}
            )
            custom_name = map_data.get("customName", "Stash_AnnotedMap")
            item_name = Translate.get(custom_name, "")
            page_name = f"{item_name} ({get_region(map_id)})"
            navbox.add_item(LiteratureGroups.get_display_name(group_id), page_name)

    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or LiteratureGroups.get_section_order())
    return navbox


def generate_literature_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_literature_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved literature navbox: {path}")
    return path


def main() -> None:
    generate_literature_navbox()


if __name__ == "__main__":
    main()

