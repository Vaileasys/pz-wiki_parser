#!/usr/bin/env python3
"""
Project Zomboid Wiki Tile Stitcher

This script is responsible for combining multiple sprite tiles into composite images
for the Project Zomboid Wiki. It handles multi-tile furniture and objects that span
multiple grid cells, combining their individual sprites into a single cohesive image
while maintaining proper positioning and orientation.

The script processes sprites based on their facing direction (North, South, East, West)
and grid positions, using threading for improved performance.

This script supports both:
- Furniture tiles (from named_furniture.json with explicit SpriteGridPos)
- Entity tiles (from parsed_entity_data.json with spriteOutputs lists)
"""

import os
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from scripts.core.language import Language
from scripts.core.cache import load_cache
from scripts.core.constants import RESOURCE_DIR, OUTPUT_DIR, CACHE_DIR
from scripts.utils import echo

SPRITE_WIDTH = 128
SPRITE_HEIGHT = 256

# Offsets for furniture tiles
SPRITE_HORIZONTAL_OFFSETS = {
    "E": (-64, 32),
    "N": (-64, 32),
    "S": (-64, 32),
    "W": (-64, 32),
}

SPRITE_VERTICAL_OFFSETS = {
    "E": (64, 32),
    "N": (64, 32),
    "S": (64, 32),
    "W": (64, 32),
}

# Offsets for entity tiles (North has different Y offset)
ENTITY_HORIZONTAL_OFFSETS = {
    "E": (-64, 32),
    "N": (-64, -32),  # North: negative Y offset to go downward
    "S": (-64, 32),
    "W": (-64, 32),
}

ENTITY_VERTICAL_OFFSETS = {
    "E": (64, 32),
    "N": (64, -32),  # North: negative Y offset to go downward
    "S": (64, 32),
    "W": (64, 32),
}

FACING_TO_FOLDER = {
    "S": "South",
    "E": "East",
    "N": "North",
    "W": "West",
}

THREAD_POOL_MAX_WORKERS = (os.cpu_count() / 2) or 2

LANGUAGE_CODE = Language.get()

CACHE_FILENAME = "named_furniture.json"
NAMED_FURNITURE_CACHE_PATH = os.path.join("data", CACHE_FILENAME)

SPRITE_IMAGES_DIRECTORY = os.path.join(RESOURCE_DIR, "tile_images")
OUTPUT_IMAGES_BASE_PATH = os.path.join(OUTPUT_DIR, LANGUAGE_CODE, "tiles", "images")
OUTPUT_ENTITY_IMAGES_BASE_PATH = os.path.join(
    OUTPUT_DIR, LANGUAGE_CODE, "tiles", "entity_images_stitched"
)


def parse_grid_position(position_string: str) -> tuple[int, int]:
    """
    Parse a grid position string into column and row indices.

    Args:
        position_string (str): A string in the format "row,column" where both values are integers.

    Returns:
        tuple[int, int]: A tuple containing (column_index, row_index).
        Returns (0, 0) if the parsing fails.
    """
    try:
        row_index, column_index = map(int, position_string.split(","))
        return column_index, row_index
    except Exception:
        return 0, 0


def build_output_name(sprite_identifier_list: list[str]) -> str:
    """
    Generate an output filename by combining multiple sprite identifiers.

    Args:
        sprite_identifier_list (list[str]): List of sprite identifiers to combine.

    Returns:
        str: Combined filename where the first identifier is the base and subsequent
             ones are appended as suffixes, joined with '+'.
    """
    base_identifier = sprite_identifier_list[0]
    additional_suffixes = [
        identifier.rsplit("_", 1)[-1] for identifier in sprite_identifier_list[1:]
    ]
    return "+".join([base_identifier, *additional_suffixes])


def build_entity_output_name(sprite_identifier_list: list[str]) -> str:
    """
    Generate an output filename for entity sprites by joining all identifiers with '+'.

    Args:
        sprite_identifier_list (list[str]): List of sprite identifiers to combine.

    Returns:
        str: Combined filename where all identifiers are joined with '+'.
    """
    return "+".join(sprite_identifier_list)


def extract_entity_stitching_tasks(
    entity_data: dict,
) -> list[tuple[str, list[dict], str]]:
    """
    Extract stitching tasks from entity data.

    Args:
        entity_data (dict): Dictionary of entity definitions from parsed_entity_data.json.

    Returns:
        list[tuple[str, list[dict], str]]: List of stitching tasks in the format
            (facing_direction, sprite_entries_list, output_base_name).
    """
    stitching_tasks_list: list[tuple[str, list[dict], str]] = []

    for entity_name, entity_def in entity_data.items():
        sprite_outputs = entity_def.get("spriteOutputs", {})

        for facing_direction, sprite_list in sprite_outputs.items():
            # Filter out False/None values from sprite list
            sprite_list = [s for s in sprite_list if s and isinstance(s, str)]
            
            if not sprite_list or len(sprite_list) < 2:
                continue

            # For North-facing sprites, reverse the order for proper visual alignment
            # Other directions (West, South, East) use original order
            processing_list = (
                list(reversed(sprite_list)) if facing_direction == "N" else sprite_list
            )

            # Assign grid positions (0,0), (1,0), (2,0), etc.
            sprite_entries_list = []
            for idx, sprite_identifier in enumerate(processing_list):
                sprite_entries_list.append(
                    {
                        "sprite": sprite_identifier,
                        "grid": (idx, 0),  # Horizontal arrangement
                    }
                )

            # Output name always uses original order (not reversed)
            output_base_name = build_entity_output_name(sprite_list)
            stitching_tasks_list.append(
                (facing_direction, sprite_entries_list, output_base_name)
            )

    return stitching_tasks_list


def composite_sprites(
    facing_direction: str,
    sprite_entries_list: list[dict],
    output_base_name: str,
    progress_bar,
    output_images_path: str = None,
    horizontal_offsets: dict = None,
    vertical_offsets: dict = None,
) -> None:
    """
    Create a composite image by combining multiple sprite images for a specific facing direction.

    Args:
        facing_direction (str): The direction the sprite is facing ('N', 'S', 'E', or 'W').
        sprite_entries_list (list[dict]): List of sprite entries containing sprite IDs and grid positions.
        output_base_name (str): Base name for the output file.
        progress_bar: tqdm progress bar instance for tracking progress.
        output_images_path (str, optional): Base path for output images. Defaults to OUTPUT_IMAGES_BASE_PATH.
        horizontal_offsets (dict, optional): Horizontal offset values. Defaults to SPRITE_HORIZONTAL_OFFSETS.
        vertical_offsets (dict, optional): Vertical offset values. Defaults to SPRITE_VERTICAL_OFFSETS.

    The function handles:
        - Sorting sprites by grid position
        - Computing canvas size based on sprite positions
        - Compositing sprites onto a single image
        - Saving the resulting image to the appropriate directory
    """
    if output_images_path is None:
        output_images_path = OUTPUT_IMAGES_BASE_PATH
    if horizontal_offsets is None:
        horizontal_offsets = SPRITE_HORIZONTAL_OFFSETS
    if vertical_offsets is None:
        vertical_offsets = SPRITE_VERTICAL_OFFSETS

    # Sort entries by grid coordinates
    sprite_entries_list.sort(
        key=lambda entry_item: (entry_item["grid"][1], entry_item["grid"][0])
    )

    # Extract grid coordinates an compute
    grid_coordinates_list = [entry_item["grid"] for entry_item in sprite_entries_list]
    column_indices = [column for column, _ in grid_coordinates_list]
    row_indices = [row for _, row in grid_coordinates_list]
    minimum_column_index = min(column_indices)
    minimum_row_index = min(row_indices)

    horizontal_offset_x, horizontal_offset_y = horizontal_offsets[facing_direction]
    vertical_offset_x, vertical_offset_y = vertical_offsets[facing_direction]

    # Compute absolute positions
    absolute_position_coordinates = [
        (
            (column - minimum_column_index) * horizontal_offset_x
            + (row - minimum_row_index) * vertical_offset_x,
            (column - minimum_column_index) * horizontal_offset_y
            + (row - minimum_row_index) * vertical_offset_y,
        )
        for column, row in grid_coordinates_list
    ]

    # Determine canvas size
    x_positions = [x for x, _ in absolute_position_coordinates]
    y_positions = [y for _, y in absolute_position_coordinates]
    minimum_x_position = min(x_positions)
    maximum_x_position = max(x_positions)
    minimum_y_position = min(y_positions)
    maximum_y_position = max(y_positions)

    canvas_width = (maximum_x_position - minimum_x_position) + SPRITE_WIDTH
    canvas_height = (maximum_y_position - minimum_y_position) + SPRITE_HEIGHT

    composite_canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
    has_missing_sprites = False

    # Composite each sprite onto the canvas
    for sprite_entry, position_offset in zip(
        sprite_entries_list, absolute_position_coordinates
    ):
        sprite_identifier = sprite_entry["sprite"]
        image_filename = f"{sprite_identifier}.png"
        image_file_path = os.path.join(SPRITE_IMAGES_DIRECTORY, image_filename)
        if not os.path.isfile(image_file_path):
            echo.warning(f"Missing sprite: {sprite_identifier}")
            has_missing_sprites = True
            continue

        sprite_image = Image.open(image_file_path).convert("RGBA")
        x_offset, y_offset = position_offset
        canvas_draw_x = x_offset - minimum_x_position
        canvas_draw_y = y_offset - minimum_y_position
        composite_canvas.alpha_composite(sprite_image, (canvas_draw_x, canvas_draw_y))

    if has_missing_sprites:
        echo.warning(
            f"Skipping {output_base_name} ({facing_direction}) due to missing pieces"
        )
        progress_bar.update(1)
        return

    # Save composited image
    output_directory = os.path.join(
        output_images_path, FACING_TO_FOLDER.get(facing_direction, facing_direction)
    )
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, f"{output_base_name}.png")
    composite_canvas.save(output_file_path)
    progress_bar.update(1)


def stitch_furniture_tiles() -> None:
    """
    Process furniture tiles from named_furniture cache and create composite images.
    """
    named_furniture_data = load_cache(NAMED_FURNITURE_CACHE_PATH, "named furniture")
    stitching_tasks_list: list[tuple[str, list[dict], str]] = []

    for variant_group in named_furniture_data.values():
        sprites_by_facing: dict[str, list[dict]] = {}
        for sprite_variant_data in variant_group.values():
            generic_properties = sprite_variant_data.get("properties", {}).get(
                "generic", {}
            )
            sprite_identifier = sprite_variant_data.get("sprite")
            facing_direction = generic_properties.get("Facing", "E")
            grid_position_string = generic_properties.get("SpriteGridPos", "0,0")

            if sprite_identifier:
                grid_coordinates = parse_grid_position(grid_position_string)
                sprites_by_facing.setdefault(facing_direction, []).append(
                    {"sprite": sprite_identifier, "grid": grid_coordinates}
                )

        for facing_direction, sprite_entries_list in sprites_by_facing.items():
            if len(sprite_entries_list) < 2:
                continue

            sorted_sprite_entries = sorted(
                sprite_entries_list,
                key=lambda entry_item: (entry_item["grid"][1], entry_item["grid"][0]),
            )
            sprite_identifier_list = [
                entry_item["sprite"] for entry_item in sorted_sprite_entries
            ]
            output_base_name = build_output_name(sprite_identifier_list)
            stitching_tasks_list.append(
                (facing_direction, sorted_sprite_entries, output_base_name)
            )

    echo.info(
        f"Stitching {len(stitching_tasks_list)} multi-sprite furniture tiles across all facings…"
    )
    with tqdm(
        total=len(stitching_tasks_list), desc="Stitching furniture", unit="tile"
    ) as progress_bar:
        with ThreadPoolExecutor(max_workers=THREAD_POOL_MAX_WORKERS) as thread_pool:
            for (
                facing_direction,
                sorted_sprite_entries,
                output_base_name,
            ) in stitching_tasks_list:
                thread_pool.submit(
                    composite_sprites,
                    facing_direction,
                    sorted_sprite_entries,
                    output_base_name,
                    progress_bar,
                )


def stitch_entity_tiles() -> None:
    """
    Process entity tiles from parsed_entity_data cache and create composite images.
    """
    entity_cache_path = os.path.join(CACHE_DIR, "parsed_entity_data.json")
    entity_data = load_cache(entity_cache_path, "entity")

    if not entity_data:
        echo.warning("No entity data found, skipping entity tile stitching")
        return

    stitching_tasks_list = extract_entity_stitching_tasks(entity_data)

    if not stitching_tasks_list:
        echo.info("No multi-sprite entity tiles found to stitch")
        return

    echo.info(
        f"Stitching {len(stitching_tasks_list)} multi-sprite entity tiles across all facings…"
    )
    with tqdm(
        total=len(stitching_tasks_list), desc="Stitching entities", unit="tile"
    ) as progress_bar:
        with ThreadPoolExecutor(max_workers=THREAD_POOL_MAX_WORKERS) as thread_pool:
            for (
                facing_direction,
                sprite_entries_list,
                output_base_name,
            ) in stitching_tasks_list:
                thread_pool.submit(
                    composite_sprites,
                    facing_direction,
                    sprite_entries_list,
                    output_base_name,
                    progress_bar,
                    OUTPUT_ENTITY_IMAGES_BASE_PATH,
                    ENTITY_HORIZONTAL_OFFSETS,
                    ENTITY_VERTICAL_OFFSETS,
                )


def stitch_entity_sprites_for_lang(lang_code: str = None) -> None:
    """
    Convenience function to stitch entity sprites. Can be called from other scripts.

    Args:
        lang_code (str, optional): Language code (currently unused but kept for API compatibility).
    """
    stitch_entity_tiles()


def main() -> None:
    """
    Main execution function for the tile stitcher.

    Processes both furniture and entity caches to identify multi-tile objects and creates
    composite images for each valid combination. Uses multi-threading to improve
    performance when processing multiple sprites.
    """
    echo.info("Starting tile stitching process…")

    # Stitch furniture tiles
    try:
        stitch_furniture_tiles()
    except Exception as exc:
        echo.error(f"Failed to stitch furniture tiles: {exc}")

    # Stitch entity tiles
    try:
        stitch_entity_tiles()
    except Exception as exc:
        echo.error(f"Failed to stitch entity tiles: {exc}")

    echo.success("Tile stitching completed")


if __name__ == "__main__":
    main()
