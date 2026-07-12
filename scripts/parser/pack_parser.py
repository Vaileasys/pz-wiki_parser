"""
Parser for .pack texture atlas files.

This module reads pack data and returns structured metadata.
"""

from dataclasses import asdict, dataclass, field
from pathlib import Path
import re
import struct

PNG_SIG = b"\x89PNG\r\n\x1a\n"
PZPK_SIG = b"PZPK"
END_OF_IMAGE = b"\xef\xbe\xad\xde"
SPRITE_FMT = "<8I"
SPRITE_SIZE = struct.calcsize(SPRITE_FMT)
NAME_RE = re.compile(rb"[A-Za-z0-9_\-/\.]{3,128}")


class PackParserError(Exception):
    """Raised when a .pack file cannot be parsed safely."""


@dataclass(slots=True)
class SpriteEntry:
    """Metadata for one sub-texture/sprite entry."""

    name: str
    x_pos: int
    y_pos: int
    width: int
    height: int
    x_offset: int
    y_offset: int
    total_width: int
    total_height: int
    valid: bool = True
    extracted_path: str | None = None

    @classmethod
    def from_values(cls, name: str, values: tuple[int, ...]) -> "SpriteEntry":
        return cls(name, *(int(value) for value in values))

    @classmethod
    def from_dict(cls, data: dict) -> "SpriteEntry":
        fields = {
            "name": data["name"],
            "x_pos": data["x_pos"],
            "y_pos": data["y_pos"],
            "width": data["width"],
            "height": data["height"],
            "x_offset": data["x_offset"],
            "y_offset": data["y_offset"],
            "total_width": data["total_width"],
            "total_height": data["total_height"],
            "valid": data.get("valid", True),
            "extracted_path": data.get("extracted_path"),
        }
        return cls(**fields)

    def to_dict(self) -> dict:
        return asdict(self)

    def values(self) -> tuple[int, int, int, int, int, int, int, int]:
        return (
            self.x_pos,
            self.y_pos,
            self.width,
            self.height,
            self.x_offset,
            self.y_offset,
            self.total_width,
            self.total_height,
        )


@dataclass(slots=True)
class PackSheet:
    """Metadata for one texture sheet inside a pack."""

    index: int
    name: str
    has_alpha: bool | None
    version: int | None
    format: str
    image_length: int | None
    png_start: int
    png_end: int
    meta_start: int
    meta_end: int
    sheet_width: int
    sheet_height: int
    sprites: list[SpriteEntry] = field(default_factory=list)
    parser: str = "structured"

    @classmethod
    def from_dict(cls, data: dict) -> "PackSheet":
        sheet = dict(data)
        sheet["sprites"] = [SpriteEntry.from_dict(item) for item in data.get("sprites", [])]
        return cls(**sheet)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["sprites"] = [sprite.to_dict() for sprite in self.sprites]
        return data


@dataclass(slots=True)
class Pack:
    """Parsed .pack metadata and original bytes."""

    sheets: list[PackSheet]
    version: int | None
    format: str
    parser: str
    path: Path | None = None
    fallback_reason: str | None = None
    data: bytes = field(default=b"", repr=False)

    @classmethod
    def from_metadata(cls, data: dict, path: Path | None = None) -> "Pack":
        sheets = [PackSheet.from_dict(item) for item in data.get("sheets", [])]
        version = data.get("version")
        if version is None and sheets:
            version = sheets[0].version
        return cls(
            sheets=sheets,
            version=version,
            format=data.get("format") or (sheets[0].format if sheets else "pzpk"),
            parser=data.get("parser", "metadata"),
            path=path,
            fallback_reason=data.get("fallback_reason"),
        )

    def to_metadata(self) -> dict:
        return {
            "parser": self.parser,
            "version": self.version,
            "format": self.format,
            "source": str(self.path) if self.path else None,
            "fallback_reason": self.fallback_reason,
            "sheets": [sheet.to_dict() for sheet in self.sheets],
        }

    def png_bytes(self, sheet: PackSheet) -> bytes:
        if not self.data:
            raise PackParserError("Pack does not contain source bytes.")
        return self.data[sheet.png_start:sheet.png_end]


def read_u32(data: bytes, pos: int) -> tuple[int, int]:
    """Read a little-endian uint32."""
    if pos + 4 > len(data):
        raise PackParserError(f"Expected uint32 at offset {pos}, but reached end of file.")
    return struct.unpack_from("<I", data, pos)[0], pos + 4


def read_i32(data: bytes, pos: int) -> tuple[int, int]:
    """Read a little-endian int32."""
    if pos + 4 > len(data):
        raise PackParserError(f"Expected int32 at offset {pos}, but reached end of file.")
    return struct.unpack_from("<i", data, pos)[0], pos + 4


def read_string(data: bytes, pos: int) -> tuple[str, int]:
    """Read a length-prefixed ASCII string."""
    length, pos = read_u32(data, pos)
    end = pos + length

    if length > 4096 or end > len(data):
        raise PackParserError(f"String at offset {pos} exceeds file size: length={length}.")

    return data[pos:end].decode("ascii", "replace"), end


def get_png_end(data: bytes, start: int) -> int:
    """Return the byte offset immediately after a PNG image."""
    if data[start:start + len(PNG_SIG)] != PNG_SIG:
        raise PackParserError(f"Expected PNG signature at offset {start}.")

    pos = start + len(PNG_SIG)
    while pos + 8 <= len(data):
        chunk_len = struct.unpack_from(">I", data, pos)[0]
        chunk_type = data[pos + 4:pos + 8]
        next_pos = pos + 8 + chunk_len + 4

        if next_pos > len(data):
            raise PackParserError(f"PNG chunk at offset {pos} exceeds file size.")
        if chunk_type == b"IEND":
            return next_pos

        pos = next_pos

    raise PackParserError(f"PNG at offset {start} has no IEND chunk.")


def get_png_size(data: bytes, start: int) -> tuple[int, int]:
    """Read width and height from a PNG IHDR chunk."""
    if data[start:start + len(PNG_SIG)] != PNG_SIG:
        raise PackParserError(f"Expected PNG signature at offset {start}.")

    ihdr_pos = start + len(PNG_SIG)
    if data[ihdr_pos + 4:ihdr_pos + 8] != b"IHDR":
        raise PackParserError(f"Expected PNG IHDR chunk at offset {ihdr_pos}.")

    width = struct.unpack_from(">I", data, ihdr_pos + 8)[0]
    height = struct.unpack_from(">I", data, ihdr_pos + 12)[0]
    return width, height


def extract_png_ranges(data: bytes) -> list[tuple[int, int]]:
    """Find embedded PNG byte ranges in pack data."""
    ranges: list[tuple[int, int]] = []
    pos = 0

    while True:
        start = data.find(PNG_SIG, pos)
        if start == -1:
            break

        end = get_png_end(data, start)
        ranges.append((start, end))
        pos = end

    return ranges


def read_pzpk_png_range(data: bytes, pos: int) -> tuple[int, int, int, int]:
    """Read a PZPK length-prefixed PNG range."""
    image_length, pos = read_u32(data, pos)
    png_start = pos
    png_end = pos + image_length

    if image_length == 0 or png_end > len(data):
        raise PackParserError(f"PNG buffer at offset {pos} exceeds file size: length={image_length}.")
    if data[png_start:png_start + len(PNG_SIG)] != PNG_SIG:
        raise PackParserError(f"Expected PNG signature at offset {png_start}.")

    return png_start, png_end, png_end, image_length


def read_pack_header(data: bytes) -> tuple[int, int, int, bool]:
    """Read the pack header."""
    if data[:4] == PZPK_SIG:
        version, pos = read_i32(data, 4)
        if version != 1:
            raise PackParserError(f"Unsupported .pack file version: {version}.")
        sheet_count, pos = read_u32(data, pos)
        return sheet_count, pos, version, True

    sheet_count, pos = read_u32(data, 0)
    return sheet_count, pos, 0, False


def read_sheet_image(data: bytes, pos: int, is_pzpk: bool) -> tuple[int, int, int, int | None]:
    """Read a sheet image range."""
    if is_pzpk:
        return read_pzpk_png_range(data, pos)

    png_start = pos
    png_end = get_png_end(data, png_start)
    next_pos = png_end

    if data[next_pos:next_pos + 4] == END_OF_IMAGE:
        next_pos += 4

    return png_start, png_end, next_pos, None


def is_valid_sprite(values: tuple[int, ...], sheet_width: int, sheet_height: int) -> bool:
    """Check whether sprite metadata is inside sensible bounds."""
    x_pos, y_pos, width, height, x_offset, y_offset, total_width, total_height = values

    if not (0 <= x_pos < sheet_width and 0 <= y_pos < sheet_height):
        return False
    if not (1 <= width <= sheet_width and 1 <= height <= sheet_height):
        return False
    if x_pos + width > sheet_width or y_pos + height > sheet_height:
        return False
    if not (1 <= total_width <= 4096 and 1 <= total_height <= 4096):
        return False
    if total_width < width or total_height < height:
        return False
    if x_offset + width > total_width or y_offset + height > total_height:
        return False

    return True


def parse_structured_pack(data: bytes, path: Path | None = None) -> Pack:
    """Parse a pack using the structured metadata format."""
    sheet_count, pos, version, is_pzpk = read_pack_header(data)

    if not (1 <= sheet_count <= 512):
        raise PackParserError(f"Unreasonable sheet count: {sheet_count}.")

    sheets: list[PackSheet] = []
    pack_format = "PZPK" if is_pzpk else "legacy"

    for sheet_index in range(sheet_count):
        if data[pos:pos + 4] == END_OF_IMAGE:
            pos += 4

        meta_start = pos
        sheet_name, pos = read_string(data, pos)
        sprite_count, pos = read_u32(data, pos)
        has_alpha_value, pos = read_i32(data, pos)
        has_alpha = has_alpha_value != 0

        if not (0 <= sprite_count <= 100000):
            raise PackParserError(f"Unreasonable sprite count at sheet {sheet_index}: {sprite_count}.")

        sprites: list[SpriteEntry] = []
        for _ in range(sprite_count):
            sprite_name, pos = read_string(data, pos)

            if pos + SPRITE_SIZE > len(data):
                raise PackParserError(f"Sprite metadata for {sprite_name!r} exceeds file size.")

            values = struct.unpack_from(SPRITE_FMT, data, pos)
            pos += SPRITE_SIZE
            sprites.append(SpriteEntry.from_values(sprite_name, values))

        meta_end = pos
        png_start, png_end, pos, image_length = read_sheet_image(data, pos, is_pzpk)
        sheet_width, sheet_height = get_png_size(data, png_start)

        for sprite in sprites:
            sprite.valid = is_valid_sprite(sprite.values(), sheet_width, sheet_height)

        sheets.append(PackSheet(
            index=sheet_index,
            name=sheet_name,
            has_alpha=has_alpha,
            version=version,
            format=pack_format,
            image_length=image_length,
            png_start=png_start,
            png_end=png_end,
            meta_start=meta_start,
            meta_end=meta_end,
            sheet_width=sheet_width,
            sheet_height=sheet_height,
            sprites=sprites,
            parser="structured",
        ))

    if pos != len(data):
        raise PackParserError(f"Structured parser left {len(data) - pos} trailing byte(s).")

    return Pack(sheets=sheets, version=version, format=pack_format, parser="structured", path=path, data=data)


def scan_sheet_meta(data: bytes, meta_start: int, meta_end: int, sheet_width: int, sheet_height: int) -> list[SpriteEntry]:
    """Scan a metadata range for sprite names followed by sprite values."""
    seg = data[meta_start:meta_end]
    sprites: list[tuple[int, SpriteEntry]] = []
    seen: set[tuple[str, int, int, int, int]] = set()

    for match in NAME_RE.finditer(seg):
        raw_name = match.group(0)
        name = raw_name.decode("ascii", "ignore")
        name_end = meta_start + match.end()

        for align in range(-1, 5):
            pos = name_end + align
            if pos < meta_start or pos + SPRITE_SIZE > meta_end:
                continue

            values = struct.unpack_from(SPRITE_FMT, data, pos)
            if not is_valid_sprite(values, sheet_width, sheet_height):
                continue

            fixed_name = name[:-1] if align == -1 else name
            if len(fixed_name) < 3:
                continue

            key = (fixed_name, values[0], values[1], values[2], values[3])
            if key in seen:
                continue

            sprites.append((pos, SpriteEntry.from_values(fixed_name, values)))
            seen.add(key)
            break

    sprites.sort(key=lambda item: (item[0], item[1].name))
    return [sprite for _, sprite in sprites]


def parse_scanned_pack(data: bytes, path: Path | None = None) -> Pack:
    """Parse a pack by scanning around embedded PNG ranges."""
    pngs = extract_png_ranges(data)
    if not pngs:
        raise PackParserError("No embedded PNG sheets found.")

    sheets: list[PackSheet] = []

    for index, (png_start, png_end) in enumerate(pngs):
        sheet_width, sheet_height = get_png_size(data, png_start)
        meta_start = 0 if index == 0 else pngs[index - 1][1]

        if data[meta_start:meta_start + 4] == END_OF_IMAGE:
            meta_start += 4

        meta_end = png_start
        sprites = scan_sheet_meta(data, meta_start, meta_end, sheet_width, sheet_height)

        sheets.append(PackSheet(
            index=index,
            name=f"sheet_{index}",
            has_alpha=None,
            version=None,
            format="scanned",
            image_length=None,
            png_start=png_start,
            png_end=png_end,
            meta_start=meta_start,
            meta_end=meta_end,
            sheet_width=sheet_width,
            sheet_height=sheet_height,
            sprites=sprites,
            parser="scanned",
        ))

    return Pack(sheets=sheets, version=None, format="scanned", parser="scanned", path=path, data=data)


def parse_pack(data: bytes, path: Path | None = None, fallback: bool = True) -> Pack:
    """Parse a pack using structured mode, then scanned mode if needed."""
    try:
        return parse_structured_pack(data, path)
    except PackParserError as error:
        if not fallback:
            raise

        pack = parse_scanned_pack(data, path)
        pack.fallback_reason = str(error)
        return pack


def parse_pack_file(path: str | Path, fallback: bool = True) -> Pack:
    """Read and parse a pack file."""
    pack_path = Path(path)
    return parse_pack(pack_path.read_bytes(), pack_path, fallback=fallback)
