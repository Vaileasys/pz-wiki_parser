import os
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from scripts.core.language import Language
from scripts.core.cache import load_cache
from scripts.core.constants import RESOURCE_DIR, OUTPUT_DIR
from scripts.utils.echo import echo_info, echo_warning

SPRITE_WIDTH = 128
SPRITE_HEIGHT = 256

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


def parse_grid_position(position_string: str) -> tuple[int, int]:
    """
    position_string is "row,column" (first = vertical index, second = horizontal index).
    Returns (column_index, row_index).
    """
    try:
        row_index, column_index = map(int, position_string.split(","))
        return column_index, row_index
    except Exception:
        return 0, 0


def build_output_name(sprite_identifier_list: list[str]) -> str:
    """
    Combine multiple sprite identifiers into a single output name.
    The first identifier is taken as the base, and subsequent ones append their suffix.
    """
    base_identifier = sprite_identifier_list[0]
    additional_suffixes = [identifier.rsplit("_", 1)[-1] for identifier in sprite_identifier_list[1:]]
    return "+".join([base_identifier, *additional_suffixes])


def composite_sprites(facing_direction: str, sprite_entries_list: list[dict], output_base_name: str, progress_bar) -> None:
    """
    Composite multiple sprite images into a single image for a given facing direction.
    """
    # Sort entries by grid coordinates
    sprite_entries_list.sort(key=lambda entry_item: (entry_item["grid"][1], entry_item["grid"][0]))

    # Extract grid coordinates an compute
    grid_coordinates_list = [entry_item["grid"] for entry_item in sprite_entries_list]
    column_indices = [column for column, _ in grid_coordinates_list]
    row_indices = [row for _, row in grid_coordinates_list]
    minimum_column_index = min(column_indices)
    minimum_row_index = min(row_indices)

    horizontal_offset_x, horizontal_offset_y = SPRITE_HORIZONTAL_OFFSETS[facing_direction]
    vertical_offset_x, vertical_offset_y = SPRITE_VERTICAL_OFFSETS[facing_direction]

    # Compute absolute positions
    absolute_position_coordinates = [
        (
            (column - minimum_column_index) * horizontal_offset_x
            + (row - minimum_row_index) * vertical_offset_x,
            (column - minimum_column_index) * horizontal_offset_y
            + (row - minimum_row_index) * vertical_offset_y
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
    for sprite_entry, position_offset in zip(sprite_entries_list, absolute_position_coordinates):
        sprite_identifier = sprite_entry["sprite"]
        image_filename = f"{sprite_identifier}.png"
        image_file_path = os.path.join(SPRITE_IMAGES_DIRECTORY, image_filename)
        if not os.path.isfile(image_file_path):
            echo_warning(f"Missing sprite: {sprite_identifier}")
            has_missing_sprites = True
            continue

        sprite_image = Image.open(image_file_path).convert("RGBA")
        x_offset, y_offset = position_offset
        canvas_draw_x = x_offset - minimum_x_position
        canvas_draw_y = y_offset - minimum_y_position
        composite_canvas.alpha_composite(sprite_image, (canvas_draw_x, canvas_draw_y))

    if has_missing_sprites:
        echo_warning(f"Skipping {output_base_name} ({facing_direction}) due to missing pieces")
        progress_bar.update(1)
        return

    # Save composited image
    output_directory = os.path.join(OUTPUT_IMAGES_BASE_PATH, FACING_TO_FOLDER.get(facing_direction, facing_direction))
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, f"{output_base_name}.png")
    composite_canvas.save(output_file_path)
    progress_bar.update(1)


def main() -> None:
    named_furniture_data = load_cache(NAMED_FURNITURE_CACHE_PATH, "named furniture")
    stitching_tasks_list: list[tuple[str, list[dict], str]] = []

    for variant_group in named_furniture_data.values():
        sprites_by_facing: dict[str, list[dict]] = {}
        for sprite_variant_data in variant_group.values():
            generic_properties = sprite_variant_data.get("properties", {}).get("generic", {})
            sprite_identifier = sprite_variant_data.get("sprite")
            facing_direction = generic_properties.get("Facing", "E")
            grid_position_string = generic_properties.get("SpriteGridPos", "0,0")

            if sprite_identifier:
                grid_coordinates = parse_grid_position(grid_position_string)
                sprites_by_facing.setdefault(facing_direction, []).append({
                    "sprite": sprite_identifier,
                    "grid": grid_coordinates
                })

        for facing_direction, sprite_entries_list in sprites_by_facing.items():
            if len(sprite_entries_list) < 2:
                continue

            sorted_sprite_entries = sorted(
                sprite_entries_list,
                key=lambda entry_item: (entry_item["grid"][1], entry_item["grid"][0])
            )
            sprite_identifier_list = [entry_item["sprite"] for entry_item in sorted_sprite_entries]
            output_base_name = build_output_name(sprite_identifier_list)
            stitching_tasks_list.append((facing_direction, sorted_sprite_entries, output_base_name))

    echo_info(f"Stitching {len(stitching_tasks_list)} multi-sprite tiles across all facings…")
    with tqdm(total=len(stitching_tasks_list), desc="Stitching", unit="tile") as progress_bar:
        with ThreadPoolExecutor(max_workers=THREAD_POOL_MAX_WORKERS) as thread_pool:
            for facing_direction, sorted_sprite_entries, output_base_name in stitching_tasks_list:
                thread_pool.submit(
                    composite_sprites,
                    facing_direction,
                    sorted_sprite_entries,
                    output_base_name,
                    progress_bar
                )


if __name__ == "__main__":
    main()
