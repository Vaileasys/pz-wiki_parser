"""Generate the tool navbox from ToolGroups."""

from pathlib import Path
from scripts.items.groups.tool_groups import ToolGroups, is_tool_item
from scripts.navbox.navbox import Navbox
from scripts.objects.item import Item
from scripts.utils import echo

OUTPUT_FILENAME = "tool.json"
TABLE_NAME = "Tools"


def build_tool_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox(TABLE_NAME)
    for item in Item.values():
        if not is_tool_item(item):
            continue
        if not item.has_page:
            echo.warning(f"Tool item does not have a page: {item.item_id}")
        for group_id in ToolGroups.get_group_ids(item):
            navbox.add_item(ToolGroups.get_display_name(group_id), item.page)
    navbox.sort(sections=False, items=True)
    navbox.sort_sections_by_order(section_order or ToolGroups.get_section_order())
    return navbox


def generate_tool_navbox(output_dir: str | Path | None = None) -> Path:
    path = build_tool_navbox().save(OUTPUT_FILENAME, output_dir=output_dir)
    echo.success(f"Saved tool navbox: {path}")
    return path


def main() -> None:
    generate_tool_navbox()


if __name__ == "__main__":
    main()

