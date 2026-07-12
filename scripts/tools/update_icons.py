"""Update the icon name resource and extract newly discovered icons.

Pack icons are located through the sprite index and extracted directly from the
Project Zomboid `texturepacks` directory.
"""

from pathlib import Path
import shutil
import sys

from scripts.core import config_manager as config
from scripts.core.cache import load_cache, save_cache
from scripts.core.constants import OUTPUT_DIR, RESOURCE_DIR
from scripts.sprites.sprite_extractor import extract_indexed_sprites
from scripts.sprites.sprite_indexer import get_preferred_sprite, get_sprite_index
from scripts.utils import echo


RESOURCES_DIR = Path(RESOURCE_DIR)
NEW_TEXTURES_DIR = Path(OUTPUT_DIR) / "new_textures"
TEXTURES_JSON = "texture_names.json"
TEXTURES_JSON_PATH = RESOURCES_DIR / TEXTURES_JSON

ICON_CATEGORIES = {
    "Item": {
        "index_key": "items",
        "prefix": "Item_",
    },
    "Build": {
        "index_key": "builds",
        "prefix": "Build_",
    },
}


def load_existing_textures() -> dict:
    """Load the existing texture name resource."""
    if TEXTURES_JSON_PATH.exists():
        return load_cache(TEXTURES_JSON_PATH, suppress=True)
    return {}


def _ensure_png(name: str) -> str:
    """Return a filename ending in ``.png``."""
    return name if name.casefold().endswith(".png") else f"{name}.png"


def _stored_name(category: str, source_name: str) -> str:
    """Return the filename format stored in ``texture_names.json``."""
    file_name = _ensure_png(Path(source_name).name)

    if category == "Item" and file_name.casefold().startswith("item_"):
        file_name = file_name[len("Item_"):]

    return file_name


def _category_for_filename(file_name: str) -> str | None:
    """Return the supported icon category for a loose texture filename."""
    name = file_name.casefold()

    if name.startswith("item_"):
        return "Item"
    if name.startswith("build_"):
        return "Build"

    return None


def _source_score(source: dict) -> tuple[int, int]:
    """Return a sortable preference score for an icon source."""
    if source["kind"] == "file":
        return 3, 0

    sprite = source["sprite"]
    status_score = 2 if sprite.get("source_status") == "normal" else 1
    return status_score, int(sprite.get("priority", 0))


def _add_source(
    sources: dict[str, dict[str, dict]],
    category: str,
    stored_name: str,
    source: dict,
) -> None:
    """Add or replace the preferred source for one stored filename."""
    key = stored_name.casefold()
    source["stored_name"] = stored_name

    existing = sources[category].get(key)
    if existing is None or _source_score(source) > _source_score(existing):
        sources[category][key] = source


def _collect_pack_sources(index: dict, sources: dict[str, dict[str, dict]]) -> None:
    """Add preferred Item and Build sprites from the pack index."""
    for category, settings in ICON_CATEGORIES.items():
        index_key = settings["index_key"]
        seen_names: set[str] = set()

        for sprite_id in index.get("ui", {}).get(index_key, []):
            sprite = index.get("sprites", {}).get(sprite_id)
            if sprite is None:
                continue

            name_key = sprite["name"].casefold()
            if name_key in seen_names:
                continue
            seen_names.add(name_key)

            preferred = get_preferred_sprite(
                index,
                sprite["name"],
                domain="ui",
                category=index_key,
            )
            if preferred is None:
                continue

            stored_name = _stored_name(category, preferred["file_name"])
            _add_source(
                sources,
                category,
                stored_name,
                {
                    "kind": "pack",
                    "sprite": preferred,
                },
            )


def _collect_loose_sources(sources: dict[str, dict[str, dict]]) -> None:
    """Add loose Item and Build textures from ``media/textures``."""
    textures_dir = Path(config.get_game_directory()) / "media" / "textures"
    if not textures_dir.is_dir():
        echo.warning(f"Texture directory not found: '{textures_dir}'")
        return

    for texture_path in textures_dir.glob("*.png"):
        category = _category_for_filename(texture_path.name)
        if category is None:
            continue

        stored_name = _stored_name(category, texture_path.name)
        _add_source(
            sources,
            category,
            stored_name,
            {
                "kind": "file",
                "path": texture_path,
            },
        )


def collect_icon_sources(index: dict) -> dict[str, dict[str, dict]]:
    """Return the preferred current source for every Item and Build icon."""
    sources = {category: {} for category in ICON_CATEGORIES}
    _collect_pack_sources(index, sources)
    _collect_loose_sources(sources)
    return sources


def find_new_icons(
    textures_data: dict,
    sources: dict[str, dict[str, dict]],
) -> dict[str, list[dict]]:
    """Find source records not yet present in ``texture_names.json``."""
    new_sources: dict[str, list[dict]] = {}

    for category in ICON_CATEGORIES:
        existing_names = {
            name.casefold()
            for name in textures_data.get(category, [])
        }
        category_new = [
            source
            for key, source in sorted(
                sources[category].items(),
                key=lambda item: item[0],
            )
            if key not in existing_names
        ]

        if category_new:
            new_sources[category] = category_new

    return new_sources


def _add_extracted_names(
    textures_data: dict,
    new_textures: dict[str, list[str]],
) -> None:
    """Add successfully written filenames to the texture-name resource."""
    for category, files in new_textures.items():
        existing = textures_data.setdefault(category, [])
        existing_names = {name.casefold() for name in existing}

        for file_name in files:
            if file_name.casefold() not in existing_names:
                existing.append(file_name)
                existing_names.add(file_name.casefold())

        existing.sort(key=str.casefold)


def _prepare_new_texture_dir() -> None:
    """Clear output from the previous update run."""
    if NEW_TEXTURES_DIR.exists():
        shutil.rmtree(NEW_TEXTURES_DIR)
    NEW_TEXTURES_DIR.mkdir(parents=True, exist_ok=True)


def extract_new_icons(new_sources: dict[str, list[dict]]) -> dict[str, list[str]]:
    """Copy or extract all newly discovered icons."""
    _prepare_new_texture_dir()
    new_textures: dict[str, list[str]] = {}

    for category, category_sources in new_sources.items():
        destination = NEW_TEXTURES_DIR / category
        destination.mkdir(parents=True, exist_ok=True)

        pack_records: list[dict] = []
        output_names: dict[str, str] = {}
        output_files: list[str] = []

        for source in category_sources:
            stored_name = source["stored_name"]
            output_files.append(stored_name)

            if source["kind"] == "file":
                shutil.copy2(source["path"], destination / stored_name)
                continue

            sprite = source["sprite"]
            pack_records.append(sprite)
            output_names[sprite["id"]] = stored_name

        if pack_records:
            summary = extract_indexed_sprites(
                pack_records,
                destination,
                output_names=output_names,
            )

            if summary.skipped_missing:
                echo.warning(
                    f"{summary.skipped_missing} indexed {category.lower()} "
                    "sprite(s) could not be located."
                )
            if summary.skipped_invalid or summary.skipped_bounds:
                echo.warning(
                    f"Skipped {summary.skipped_invalid + summary.skipped_bounds} "
                    f"invalid {category.lower()} sprite(s)."
                )

        written_files = sorted(
            (
                file_name
                for file_name in output_files
                if (destination / file_name).is_file()
            ),
            key=str.casefold,
        )

        if written_files:
            new_textures[category] = written_files

        echo.success(
            f"{len(written_files)} new {category.lower()} texture(s) written "
            f"to '{destination}'."
        )

    return new_textures


def _reset_loaded_item_icon_cache() -> None:
    """Reset Item's icon list when it is already loaded in this process."""
    item_module = sys.modules.get("scripts.objects.item")
    item_class = getattr(item_module, "Item", None) if item_module else None

    if item_class is not None:
        item_class._icon_cache_files = None


def update_icons() -> dict[str, list[str]]:
    """Update texture names and extract only newly discovered icons."""
    index = get_sprite_index()
    textures_data = load_existing_textures()
    sources = collect_icon_sources(index)
    new_sources = find_new_icons(textures_data, sources)
    new_textures = extract_new_icons(new_sources)
    _add_extracted_names(textures_data, new_textures)

    save_cache(textures_data, TEXTURES_JSON, RESOURCES_DIR, suppress=True)
    save_cache(new_textures, "new_textures.json", suppress=True)
    _reset_loaded_item_icon_cache()

    if not new_textures:
        echo.info("No new Item or Build textures found.")
    else:
        total = sum(len(files) for files in new_textures.values())
        echo.success(
            f"Icon update complete: {total} new texture(s) extracted."
        )

    return new_textures


def main() -> None:
    """Run the icon update workflow."""
    update_icons()


if __name__ == "__main__":
    main()
