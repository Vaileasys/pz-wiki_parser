"""Generate a page-to-navbox index from generated navbox JSON files."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from scripts.core.constants import NAVBOX_DIR
from scripts.core.language import Language
from scripts.utils import echo


OUTPUT_FILENAME = "page_navboxes.json"


def get_navbox_output_dir(output_dir: str | Path | None = None) -> Path:
    """Return the navbox output directory for the active language."""
    if output_dir is not None:
        return Path(output_dir)

    return Path(NAVBOX_DIR.format(language_code=Language.get()))


def discover_navbox_files(output_dir: str | Path | None = None) -> list[Path]:
    """Find generated navbox JSON files, excluding the page index itself."""
    navbox_dir = get_navbox_output_dir(output_dir)

    if not navbox_dir.exists():
        return []

    return sorted(
        (
            path
            for path in navbox_dir.glob("*.json")
            if path.name != OUTPUT_FILENAME
        ),
        key=lambda path: path.name.casefold(),
    )


def extract_page_name(navbox_item: object) -> str:
    """Extract the target page from a navbox item, removing any display label."""
    if not isinstance(navbox_item, str):
        return ""

    page_name, _, _label = navbox_item.partition("|")
    return page_name.strip()


def load_navbox_pages(path: str | Path) -> set[str]:
    """Load all target page names from one generated navbox JSON file."""
    navbox_path = Path(path)

    try:
        with navbox_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not load navbox JSON '{navbox_path}': {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Navbox JSON '{navbox_path}' must contain an object.")

    sections = data.get("sections")
    if not isinstance(sections, list):
        raise ValueError(f"Navbox JSON '{navbox_path}' has no valid 'sections' list.")

    pages: set[str] = set()

    for section in sections:
        if not isinstance(section, dict):
            raise ValueError(f"Navbox JSON '{navbox_path}' contains an invalid section.")

        item_list = section.get("item_list")
        if not isinstance(item_list, list):
            raise ValueError(
                f"Navbox JSON '{navbox_path}' contains a section with no valid "
                "'item_list'."
            )

        for item in item_list:
            page_name = extract_page_name(item)
            if page_name:
                pages.add(page_name)

    return pages


def build_page_navbox_index(navbox_paths: Iterable[str | Path]) -> dict[str, list[str]]:
    """Build a mapping of wiki page names to the navboxes shown on each page."""
    page_navboxes: defaultdict[str, set[str]] = defaultdict(set)

    for path in navbox_paths:
        navbox_path = Path(path)
        navbox_id = navbox_path.stem.strip()

        if not navbox_id:
            raise ValueError(f"Could not determine navbox ID from '{navbox_path}'.")

        for page_name in load_navbox_pages(navbox_path):
            page_navboxes[page_name].add(navbox_id)

    return {
        page_name: sorted(navbox_ids, key=str.casefold)
        for page_name, navbox_ids in sorted(
            page_navboxes.items(),
            key=lambda entry: entry[0].casefold(),
        )
    }


def generate_page_navbox_index(
    output_dir: str | Path | None = None,
    navbox_paths: Iterable[str | Path] | None = None,
) -> Path:
    """Generate and save the page-to-navbox JSON index."""
    navbox_dir = get_navbox_output_dir(output_dir)
    navbox_dir.mkdir(parents=True, exist_ok=True)

    paths = (
        [Path(path) for path in navbox_paths]
        if navbox_paths is not None
        else discover_navbox_files(navbox_dir)
    )

    page_navboxes = build_page_navbox_index(paths)
    output_path = navbox_dir / OUTPUT_FILENAME

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(page_navboxes, file, ensure_ascii=False, indent=2)
        file.write("\n")

    page_count = len(page_navboxes)
    navbox_count = len(paths)
    page_label = "page" if page_count == 1 else "pages"
    navbox_label = "navbox" if navbox_count == 1 else "navboxes"

    echo.success(
        f"Saved page navbox index: {output_path} "
        f"({page_count} {page_label}, {navbox_count} {navbox_label})"
    )
    return output_path


def main() -> None:
    """Generate the page-to-navbox index from existing navbox outputs."""
    generate_page_navbox_index()


if __name__ == "__main__":
    main()
