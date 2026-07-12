"""
Build a versioned index of sprites stored in Project Zomboid .pack files.

The generated index is used to locate sprites by name, category, pack, and spritesheet without extracting every image.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from tqdm import tqdm

from scripts.core.cache import load_cache, save_cache
from scripts.core.config_manager import get_game_directory
from scripts.core.constants import PBAR_FORMAT
from scripts.core.version import Version
from scripts.parser.pack_parser import Pack, SpriteEntry, parse_pack_file


SCHEMA_VERSION = 1
CACHE_FILE = "sprite_index.json"

PACK_PROFILES = {
    "ApCom": ("tiles", "1x", "tiles"),
    "ApCom_old": ("tiles", "1x", "tiles"),
    "ApComUI": ("ui", None, "mixed"),
    "B42ChunkCaching2x": ("tiles", "2x", "tiles"),
    "B42ChunkCaching2x.floor": ("tiles", "2x", "tiles"),
    "blair_temp": ("tiles", "2x", "tiles"),
    "Clock2x": ("tiles", "2x", "tiles"),
    "DepthMaps2x": ("tiles", "2x", "tiles"),
    "IconsMoveables": ("ui", None, "mixed"),
    "JumboTrees1x": ("tiles", "1x", "trees"),
    "JumboTrees2x": ("tiles", "2x", "trees"),
    "JumboTreesBigs2x": ("tiles", "2x", "trees"),
    "Mechanics": ("ui", None, "mixed"),
    "Overlays1x": ("tiles", "1x", "mixed_overlays"),
    "Overlays2x": ("tiles", "2x", "tile_overlays"),
    "Overlays2x.floor": ("tiles", "2x", "floor_overlays"),
    "RadioIcons": ("ui", None, "mixed"),
    "Tiles1x": ("tiles", "1x", "tiles"),
    "Tiles1x.floor": ("tiles", "1x", "floors"),
    "Tiles2x": ("tiles", "2x", "tiles"),
    "Tiles2x.floor": ("tiles", "2x", "floors"),
    "UI": ("ui", None, "mixed"),
    "UI2": ("ui", None, "mixed"),
    "WeatherFx": ("other", None, "other"),
}

UI_PREFIXES = {
    "item_": "items",
    "build_": "builds",
    "trait_": "traits",
    "profession_": "professions",
}

# These packs contain old or test copies.
# Their sprites remain indexed, but normal UI and tile packs are preferred during lookup.
LOW_PRIORITY_PACKS = {
    "ApCom",
    "ApCom_old",
    "ApComUI",
    "blair_temp",
    "RadioIcons",
}

# Higher numbers are preferred.
# Values only need to be ordered relative to one another.
PACK_PRIORITY = {
    # UI packs
    "UI2": 400,
    "UI": 390,
    "Mechanics": 380,
    "IconsMoveables": 370,

    # 2x tile packs
    "Tiles2x": 300,
    "Tiles2x.floor": 300,
    "Overlays2x": 300,
    "Overlays2x.floor": 300,
    "JumboTrees2x": 300,
    "JumboTreesBigs2x": 300,
    "B42ChunkCaching2x": 290,
    "B42ChunkCaching2x.floor": 290,
    "Clock2x": 290,
    "DepthMaps2x": 290,

    # 1x tile packs
    "Tiles1x": 200,
    "Tiles1x.floor": 200,
    "Overlays1x": 200,
    "JumboTrees1x": 200,

    # Other
    "WeatherFx": 100,

    # Old or test
    "RadioIcons": 20,
    "blair_temp": 20,
    "ApComUI": 10,
    "ApCom": 10,
    "ApCom_old": 0,
}


@dataclass(slots=True)
class SpriteIndex:
    """Location and classification of one sprite inside a texture pack."""

    id: str
    name: str
    file_name: str
    pack: str
    pack_file: str
    sheet: str
    sheet_index: int
    entry_index: int
    domain: str
    category: str
    scale: str | None
    priority: int
    source_status: str
    x: int
    y: int
    width: int
    height: int
    x_offset: int
    y_offset: int
    total_width: int
    total_height: int

    @classmethod
    def from_entry(
        cls,
        sprite_id: str,
        sprite: SpriteEntry,
        *,
        pack_name: str,
        pack_file: str,
        sheet_name: str,
        sheet_index: int,
        entry_index: int,
        domain: str,
        category: str,
        scale: str | None,
        priority: int,
        source_status: str,
    ) -> "SpriteIndex":
        """Create an index from parsed sprite metadata."""
        file_name = (
            sprite.name
            if sprite.name.casefold().endswith(".png")
            else f"{sprite.name}.png"
        )

        return cls(
            id=sprite_id,
            name=sprite.name,
            file_name=file_name,
            pack=pack_name,
            pack_file=pack_file,
            sheet=sheet_name,
            sheet_index=sheet_index,
            entry_index=entry_index,
            domain=domain,
            category=category,
            scale=scale,
            priority=priority,
            source_status=source_status,
            x=sprite.x_pos,
            y=sprite.y_pos,
            width=sprite.width,
            height=sprite.height,
            x_offset=sprite.x_offset,
            y_offset=sprite.y_offset,
            total_width=sprite.total_width,
            total_height=sprite.total_height,
        )

    def to_dict(self) -> dict:
        """Return a JSON-serialisable sprite record."""
        return asdict(self)


def _new_index() -> dict:
    """Return an empty sprite index structure."""
    return {
        "schema_version": SCHEMA_VERSION,
        "packs": {},
        "sprites": {},
        "by_name": {},
        "ui": {
            "items": [],
            "builds": [],
            "traits": [],
            "professions": [],
        },
        "tiles": {
            "1x": {
                "trees": [],
                "floors": [],
                "tiles": [],
                "tile_overlays": [],
                "floor_overlays": [],
            },
            "2x": {
                "trees": [],
                "floors": [],
                "tiles": [],
                "tile_overlays": [],
                "floor_overlays": [],
            },
        },
        "other": [],
        "unknown_packs": [],
        "counts": {
            "packs": 0,
            "sheets": 0,
            "sprites": 0,
            "invalid_sprites": 0,
        },
    }


def _get_pack_priority(pack_name: str, domain: str, scale: str | None) -> int:
    """Return the lookup priority for a pack."""
    if pack_name in PACK_PRIORITY:
        return PACK_PRIORITY[pack_name]

    if domain == "ui":
        return 350

    if domain == "tiles":
        return 250 if scale == "2x" else 150

    return 50


def _classify_sprite(pack_name: str, sprite_name: str) -> tuple[str, str | None, str]:
    """Return the domain, scale, and category for one sprite."""
    domain, scale, category = PACK_PROFILES.get(pack_name, ("other", None, "other"))

    if domain == "ui":
        name = sprite_name.casefold()

        for prefix, ui_category in UI_PREFIXES.items():
            if name.startswith(prefix):
                return domain, scale, ui_category

        return domain, scale, "other"

    if pack_name == "Overlays1x":
        if sprite_name.casefold().startswith("floors_"):
            return domain, scale, "floor_overlays"

        return domain, scale, "tile_overlays"

    return domain, scale, category


def _add_to_indexes(index: dict, sprite: SpriteIndex) -> None:
    """Store a sprite record and update its lookup indexes."""
    sprite_id = sprite.id
    index["sprites"][sprite_id] = sprite.to_dict()
    index["by_name"].setdefault(sprite.name.casefold(), []).append(sprite_id)

    if sprite.domain == "ui" and sprite.category in index["ui"]:
        index["ui"][sprite.category].append(sprite_id)
    elif (
        sprite.domain == "tiles"
        and sprite.scale in index["tiles"]
        and sprite.category in index["tiles"][sprite.scale]
    ):
        index["tiles"][sprite.scale][sprite.category].append(sprite_id)
    else:
        index["other"].append(sprite_id)


def _load_index_cache() -> dict | None:
    """Load the sprite cache when its version and schema are current."""
    index, cache_version = load_cache(
        CACHE_FILE,
        cache_name="sprite index",
        get_version=True,
        backup_old=True,
        suppress=True,
    )

    if not index:
        return None

    if cache_version != Version.get():
        return None

    if index.get("schema_version") != SCHEMA_VERSION:
        return None

    return index


def _save_index_cache(index: dict) -> None:
    """Save the sprite index through the shared cache service."""
    save_cache(index, CACHE_FILE, suppress=False)


def get_preferred_sprite(
    index: dict,
    name: str,
    *,
    domain: str | None = None,
    scale: str | None = None,
    category: str | None = None,
    include_legacy: bool = True,
) -> dict | None:
    """Return the preferred sprite record for a name.

    Args:
        index: Loaded sprite index.
        name: Sprite name, with or without a ``.png`` extension.
        domain: Optional domain filter, such as ``"ui"`` or ``"tiles"``.
        scale: Optional explicit tile scale, such as ``"1x"`` or ``"2x"``.
        category: Optional category filter, such as ``"items"`` or ``"trees"``.
        include_legacy: Include legacy entries in normal priority sorting.
    """
    lookup_name = name.casefold()
    if lookup_name.endswith(".png"):
        lookup_name = lookup_name[:-4]

    sprite_ids = index.get("by_name", {}).get(lookup_name, [])
    candidates = [
        index["sprites"][sprite_id]
        for sprite_id in sprite_ids
        if sprite_id in index.get("sprites", {})
    ]

    if domain is not None:
        candidates = [
            sprite
            for sprite in candidates
            if sprite.get("domain") == domain
        ]

    if scale is not None:
        candidates = [
            sprite
            for sprite in candidates
            if sprite.get("scale") == scale
        ]

    if category is not None:
        candidates = [
            sprite
            for sprite in candidates
            if sprite.get("category") == category
        ]

    if not candidates:
        return None

    if not include_legacy:
        normal_candidates = [
            sprite
            for sprite in candidates
            if sprite.get("source_status") == "normal"
        ]

        if normal_candidates:
            candidates = normal_candidates

    candidates.sort(
        key=lambda sprite: (
            -sprite.get("priority", 0),
            sprite.get("pack", "").casefold(),
            sprite.get("sheet_index", 0),
            sprite.get("entry_index", 0),
        )
    )
    return candidates[0]


def get_sprite_names(
    index: dict,
    sprite_ids: list[str],
    *,
    include_legacy: bool = True,
) -> set[str]:
    """Return normalised names for a list of indexed sprite IDs."""
    names: set[str] = set()

    for sprite_id in sprite_ids:
        sprite = index.get("sprites", {}).get(sprite_id)

        if sprite is None:
            continue

        if (
            not include_legacy
            and sprite.get("source_status") != "normal"
        ):
            continue

        names.add(sprite["name"].casefold())

    return names


def analyse_pack(pack: Pack, index: dict) -> None:
    """Add one parsed pack to an existing sprite index."""
    if pack.path is None:
        raise ValueError("Cannot analyse a pack without its source path.")

    pack_name = pack.path.stem
    pack_file = pack.path.name
    profile = PACK_PROFILES.get(pack_name)

    if profile is None:
        profile = ("other", None, "other")

        if pack_name not in index["unknown_packs"]:
            index["unknown_packs"].append(pack_name)

    pack_domain, pack_scale, pack_category = profile
    priority = _get_pack_priority(
        pack_name,
        pack_domain,
        pack_scale,
    )
    source_status = (
        "legacy"
        if pack_name in LOW_PRIORITY_PACKS
        else "normal"
    )

    pack_record = {
        "file_name": pack_file,
        "domain": pack_domain,
        "scale": pack_scale,
        "category": pack_category,
        "priority": priority,
        "source_status": source_status,
        "parser": pack.parser,
        "fallback_reason": pack.fallback_reason,
        "sheet_count": len(pack.sheets),
        "sprite_count": 0,
        "valid_sprite_count": 0,
        "invalid_sprite_count": 0,
        "sheets": {},
    }

    for sheet in pack.sheets:
        sheet_name = sheet.name or f"sheet_{sheet.index}"
        sheet_key = str(sheet.index)

        sheet_record = {
            "name": sheet_name,
            "index": sheet.index,
            "width": sheet.sheet_width,
            "height": sheet.sheet_height,
            "sprite_count": len(sheet.sprites),
            "valid_sprite_count": 0,
            "invalid_sprite_count": 0,
            "sprites": [],
        }

        pack_record["sprite_count"] += len(sheet.sprites)
        index["counts"]["sheets"] += 1

        for entry_index, entry in enumerate(sheet.sprites):
            if not entry.valid:
                sheet_record["invalid_sprite_count"] += 1
                pack_record["invalid_sprite_count"] += 1
                index["counts"]["invalid_sprites"] += 1
                continue

            sprite_id = f"{pack_name}/{sheet.index}/{entry_index}"
            domain, scale, category = _classify_sprite(pack_name, entry.name)

            sprite = SpriteIndex.from_entry(
                sprite_id,
                entry,
                pack_name=pack_name,
                pack_file=pack_file,
                sheet_name=sheet_name,
                sheet_index=sheet.index,
                entry_index=entry_index,
                domain=domain,
                category=category,
                scale=scale,
                priority=priority,
                source_status=source_status,
            )

            _add_to_indexes(index, sprite)

            sheet_record["sprites"].append(sprite_id)
            sheet_record["valid_sprite_count"] += 1
            pack_record["valid_sprite_count"] += 1
            index["counts"]["sprites"] += 1

        pack_record["sheets"][sheet_key] = sheet_record

    index["packs"][pack_name] = pack_record
    index["counts"]["packs"] += 1


def get_sprite_index(force: bool = False) -> dict:
    """Build or load the versioned Project Zomboid sprite index."""
    cached = _load_index_cache()

    if cached is not None and not force:
        return cached

    texturepacks_dir = (Path(get_game_directory()) / "media" / "texturepacks")

    if not texturepacks_dir.is_dir():
        raise FileNotFoundError(f"Texture pack directory not found: {texturepacks_dir}")

    pack_files = sorted(
        (
            path
            for path in texturepacks_dir.iterdir()
            if path.is_file() and path.suffix.casefold() == ".pack"
        ),
        key=lambda path: path.name.casefold(),
    )

    if not pack_files:
        raise FileNotFoundError(f"No .pack files found in: {texturepacks_dir}")

    index = _new_index()

    for pack_path in tqdm(pack_files, desc="Indexing texture packs", unit="pack", bar_format=PBAR_FORMAT):
        pack = parse_pack_file(pack_path)
        analyse_pack(pack, index)

    index["unknown_packs"].sort(key=str.casefold)
    _save_index_cache(index)

    return index


def analyse_sprites(force: bool = False) -> dict:
    """Compatibility wrapper for :func:`get_sprite_index`."""
    return get_sprite_index(force=force)


def main() -> None:
    """Rebuild the sprite index cache."""
    index = get_sprite_index(force=True)
    counts = index["counts"]

    print(f"Indexed {counts['sprites']} sprites from {counts['packs']} packs and {counts['sheets']} sheets.")

    if counts["invalid_sprites"]:
        print(f"Skipped {counts['invalid_sprites']} invalid sprite entries.")

    if index["unknown_packs"]:
        print("Unknown texture packs: " + ", ".join(index["unknown_packs"]))


if __name__ == "__main__":
    main()
