"""
Extract sprites and cache metadata from Project Zomboid .pack files.

Pack parsing is handled by ``scripts.parser.pack_parser``.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import io
import json
import re

from PIL import Image
from tqdm.auto import tqdm

from scripts.core.constants import CACHE_DIR, OUTPUT_DIR, PBAR_FORMAT
from scripts.core.config_manager import get_game_directory
from scripts.parser.pack_parser import Pack, PackSheet, SpriteEntry, parse_pack_file
from scripts.utils import color


PACK_METADATA_DIR = Path(CACHE_DIR) / "pack_metadata"
SPRITE_OUTPUT_DIR = Path(OUTPUT_DIR) / "sprites"

WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


@dataclass(slots=True)
class SpriteExtractionSummary:
    """Counters for one completed sprite extraction."""

    extracted: int = 0
    skipped_existing: int = 0
    skipped_invalid: int = 0
    skipped_bounds: int = 0
    skipped_missing: int = 0


def _safe_stem(name: str, fallback: str) -> str:
    """Return a Windows-safe filename or directory name."""
    stem = re.sub(r"[^A-Za-z0-9_\-.]", "_", name).strip().strip(".")

    if not stem or not stem.strip("._-"):
        stem = fallback

    if stem.upper() in WINDOWS_RESERVED_NAMES:
        stem = f"{stem}_"

    return stem[:180]


def _sheet_image(pack: Pack, sheet: PackSheet) -> Image.Image:
    """Load one embedded pack sheet as an RGBA image."""
    with Image.open(io.BytesIO(pack.png_bytes(sheet))) as image:
        return image.convert("RGBA")


def _sprite_output_path(
    sprites_dir: Path,
    pack: Pack,
    sheet: PackSheet,
    sprite: SpriteEntry,
    fallback: str,
    folder_level: int,
) -> Path:
    """Return the output path for one sprite.

    Folder levels:
        0: output/sprites/<sprite>.png
        1: output/sprites/<pack>/<sprite>.png
        2: output/sprites/<pack>/<sheet>/<sprite>.png
    """
    output_dir = sprites_dir

    if folder_level >= 1:
        pack_name = pack.path.stem if pack.path is not None else "pack"
        output_dir /= _safe_stem(pack_name, "pack")

    if folder_level >= 2:
        output_dir /= _safe_stem(sheet.name, f"sheet_{sheet.index}")

    sprite_name = _safe_stem(sprite.name, fallback)
    return output_dir / f"{sprite_name}.png"


def _relative_output_path(path: Path) -> str:
    """Return a portable output path for metadata."""
    try:
        return path.relative_to(Path(OUTPUT_DIR)).as_posix()
    except ValueError:
        return path.as_posix()


def _write_json(path: Path, data: dict) -> None:
    """Write JSON atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary_path.replace(path)


def extract_sprites(
    pack: Pack,
    folder_level: int = 2,
    overwrite: bool = True,
) -> SpriteExtractionSummary:
    """Extract every valid sprite from one parsed pack."""
    if folder_level not in {0, 1, 2}:
        raise ValueError("folder_level must be 0, 1, or 2.")

    SPRITE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = SpriteExtractionSummary()
    sprite_total = sum(len(sheet.sprites) for sheet in pack.sheets)
    pack_name = pack.path.stem if pack.path is not None else "pack"

    progress = tqdm(total=sprite_total, desc=pack_name, unit="sprite", leave=False, bar_format=PBAR_FORMAT)

    for sheet in pack.sheets:
        image = _sheet_image(pack, sheet)
        progress.set_postfix_str(sheet.name or f"sheet_{sheet.index}")

        try:
            for entry_index, sprite in enumerate(sheet.sprites):
                if not sprite.valid:
                    summary.skipped_invalid += 1
                    progress.update(1)
                    continue

                x2 = sprite.x_pos + sprite.width
                y2 = sprite.y_pos + sprite.height

                if not (
                    0 <= sprite.x_pos < image.width
                    and 0 <= sprite.y_pos < image.height
                    and sprite.x_pos < x2 <= image.width
                    and sprite.y_pos < y2 <= image.height
                ):
                    summary.skipped_bounds += 1
                    progress.update(1)
                    continue

                if (
                    sprite.total_width <= 0
                    or sprite.total_height <= 0
                    or sprite.x_offset + sprite.width > sprite.total_width
                    or sprite.y_offset + sprite.height > sprite.total_height
                ):
                    summary.skipped_bounds += 1
                    progress.update(1)
                    continue

                fallback = f"sheet_{sheet.index}_entry_{entry_index:05d}"
                sprite_path = _sprite_output_path(
                    SPRITE_OUTPUT_DIR,
                    pack,
                    sheet,
                    sprite,
                    fallback,
                    folder_level,
                )

                if sprite_path.exists() and not overwrite:
                    summary.skipped_existing += 1
                    sprite.extracted_path = _relative_output_path(sprite_path)
                    progress.update(1)
                    continue

                sprite_path.parent.mkdir(parents=True, exist_ok=True)

                crop = image.crop(
                    (sprite.x_pos, sprite.y_pos, x2, y2)
                )
                output_image = Image.new(
                    "RGBA",
                    (sprite.total_width, sprite.total_height),
                    (0, 0, 0, 0),
                )
                output_image.paste(
                    crop,
                    (sprite.x_offset, sprite.y_offset),
                )
                output_image.save(sprite_path, format="PNG")

                sprite.extracted_path = _relative_output_path(sprite_path)
                summary.extracted += 1
                progress.update(1)
        finally:
            image.close()

    progress.close()
    return summary


def write_pack_metadata(pack: Pack) -> Path:
    """Write metadata for one parsed pack."""
    if pack.path is None:
        raise ValueError(
            "Cannot write metadata without a source pack path."
        )

    pack_name = _safe_stem(pack.path.stem, "pack")
    metadata_path = PACK_METADATA_DIR / f"{pack_name}.json"

    _write_json(metadata_path, pack.to_metadata())
    return metadata_path


def extract_pack_sprites(
    pack_path: str | Path,
    folder_level: int = 2,
) -> None:
    """Parse one pack, extract its sprites, and write its metadata."""
    pack_path = Path(pack_path)

    if not pack_path.is_file():
        raise FileNotFoundError(f"Pack file not found: {pack_path}")

    pack = parse_pack_file(pack_path)
    extract_sprites(pack, folder_level=folder_level)
    write_pack_metadata(pack)


def extract_indexed_sprites(
    sprite_records: list[dict],
    output_dir: str | Path,
    *,
    output_names: dict[str, str] | None = None,
    overwrite: bool = True,
) -> SpriteExtractionSummary:
    """Extract selected sprites using the sprite index.

    Args:
        sprite_records: Sprite records from ``sprite_index["sprites"]``.
        output_dir: Flat output directory for the selected images.
        output_names: Optional mapping of sprite ID to destination filename.
        overwrite: Replace existing files when True.
    """
    records = list(sprite_records)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_names = output_names or {}

    summary = SpriteExtractionSummary()
    if not records:
        return summary

    texturepacks_dir = Path(get_game_directory()) / "media" / "texturepacks"
    records_by_pack: dict[str, list[dict]] = defaultdict(list)

    for record in records:
        pack_file = record.get("pack_file")
        if not pack_file:
            summary.skipped_missing += 1
            continue
        records_by_pack[pack_file].append(record)

    progress = tqdm(
        total=len(records),
        desc="Extracting indexed sprites",
        unit="sprite",
        bar_format=PBAR_FORMAT,
    )

    try:
        for pack_file, pack_records in records_by_pack.items():
            pack_path = texturepacks_dir / pack_file
            if not pack_path.is_file():
                summary.skipped_missing += len(pack_records)
                progress.update(len(pack_records))
                continue

            pack = parse_pack_file(pack_path)
            sheets = {sheet.index: sheet for sheet in pack.sheets}
            records_by_sheet: dict[int, list[dict]] = defaultdict(list)

            for record in pack_records:
                records_by_sheet[record.get("sheet_index", -1)].append(record)

            for sheet_index, sheet_records in records_by_sheet.items():
                sheet = sheets.get(sheet_index)
                if sheet is None:
                    summary.skipped_missing += len(sheet_records)
                    progress.update(len(sheet_records))
                    continue

                image = _sheet_image(pack, sheet)
                try:
                    for record in sheet_records:
                        entry_index = record.get("entry_index", -1)
                        sprite = None

                        if 0 <= entry_index < len(sheet.sprites):
                            candidate = sheet.sprites[entry_index]
                            if candidate.name.casefold() == str(record.get("name", "")).casefold():
                                sprite = candidate

                        if sprite is None:
                            wanted_name = str(record.get("name", "")).casefold()
                            sprite = next(
                                (
                                    candidate
                                    for candidate in sheet.sprites
                                    if candidate.name.casefold() == wanted_name
                                ),
                                None,
                            )

                        if sprite is None:
                            summary.skipped_missing += 1
                            progress.update(1)
                            continue

                        if not sprite.valid:
                            summary.skipped_invalid += 1
                            progress.update(1)
                            continue

                        x2 = sprite.x_pos + sprite.width
                        y2 = sprite.y_pos + sprite.height

                        if not (
                            0 <= sprite.x_pos < image.width
                            and 0 <= sprite.y_pos < image.height
                            and sprite.x_pos < x2 <= image.width
                            and sprite.y_pos < y2 <= image.height
                            and sprite.total_width > 0
                            and sprite.total_height > 0
                            and sprite.x_offset + sprite.width <= sprite.total_width
                            and sprite.y_offset + sprite.height <= sprite.total_height
                        ):
                            summary.skipped_bounds += 1
                            progress.update(1)
                            continue

                        output_name = output_names.get(
                            record.get("id", ""),
                            record.get("file_name") or f"{sprite.name}.png",
                        )
                        output_name = Path(output_name).name
                        suffix = Path(output_name).suffix or ".png"
                        stem = _safe_stem(Path(output_name).stem, "sprite")
                        output_path = output_dir / f"{stem}{suffix}"

                        if output_path.exists() and not overwrite:
                            summary.skipped_existing += 1
                            progress.update(1)
                            continue

                        crop = image.crop((sprite.x_pos, sprite.y_pos, x2, y2))
                        output_image = Image.new(
                            "RGBA",
                            (sprite.total_width, sprite.total_height),
                            (0, 0, 0, 0),
                        )
                        output_image.paste(crop, (sprite.x_offset, sprite.y_offset))
                        output_image.save(output_path, format="PNG")
                        output_image.close()
                        crop.close()

                        summary.extracted += 1
                        progress.update(1)
                finally:
                    image.close()
    finally:
        progress.close()

    return summary


def extract_all_sprites(folder_level: int = 2) -> None:
    """Extract sprites from every Project Zomboid texture pack.

    Folder levels:
        0: completely flat
        1: pack folder
        2: pack folder and spritesheet folder
    """
    if folder_level not in {0, 1, 2}:
        raise ValueError("folder_level must be 0, 1, or 2.")

    game_dir = Path(get_game_directory())
    texturepacks_dir = game_dir / "media" / "texturepacks"

    if not texturepacks_dir.is_dir():
        raise FileNotFoundError(
            f"Texture pack directory not found: {texturepacks_dir}"
        )

    pack_files = sorted(
        (
            path
            for path in texturepacks_dir.iterdir()
            if path.is_file() and path.suffix.lower() == ".pack"
        ),
        key=lambda path: path.name.casefold(),
    )

    if not pack_files:
        raise FileNotFoundError(
            f"No .pack files found in: {texturepacks_dir}"
        )

    for pack_path in tqdm(pack_files, desc="Texture packs", unit="pack", bar_format=PBAR_FORMAT):
        extract_pack_sprites(pack_path, folder_level=folder_level)


def main() -> None:
    """Extract all sprites using pack and spritesheet folders."""
    print("Which folder structure would you like for the extracted sprites?")
    print("0: Completely flat (duplicates will be overwritten)")
    print("1: Pack folder")
    print(f"2: Pack folder and spritesheet folder {color.warning('[default]')}")

    user_input = input("> ").strip()
    folder_level = int(user_input) if user_input in {"0", "1", "2"} else 2

    extract_all_sprites(folder_level=folder_level)


if __name__ == "__main__":
    main()
