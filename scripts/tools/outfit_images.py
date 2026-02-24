from pathlib import Path
from PIL import Image
from scripts.core.constants import RESOURCE_DIR, OUTPUT_DIR
from scripts.utils import echo
from tqdm import tqdm

# Input and output directories
OUTFIT_PARSER_DIR = Path(RESOURCE_DIR) / "OutfitParser"
OUTPUT_IMAGES_DIR = Path(OUTPUT_DIR) / "en" / "outfits" / "images"

CROP_BOX = (317, 26, 1122, 1413)


GREEN_TOLERANCE = {
    "red_max": 30,
    "green_min": 180,
    "blue_max": 30,
}

GREEN_TOLERANCE_LOOSE = {
    "red_max": 60,
    "green_min": 120,
    "blue_max": 60,
}


def is_green_pixel(pixel_rgb):
    """
    Check if a pixel is green using conservative tolerance-based detection.
    Returns True if the pixel should be considered greenscreen.
    """
    r, g, b = pixel_rgb

    if (
        r <= GREEN_TOLERANCE["red_max"]
        and g >= GREEN_TOLERANCE["green_min"]
        and b <= GREEN_TOLERANCE["blue_max"]
    ):
        return True

    if (
        r <= GREEN_TOLERANCE_LOOSE["red_max"]
        and g >= GREEN_TOLERANCE_LOOSE["green_min"]
        and b <= GREEN_TOLERANCE_LOOSE["blue_max"]
    ):
        if g > r and g > b:
            return True

    return False


def process_outfit_image(input_path: Path, output_path: Path):
    """
    Process a single outfit image:
    1. Crop to specified coordinates
    2. Remove green background pixels using tolerance-based detection
    3. Save with maximum lossless compression
    """
    try:
        # Open image
        with Image.open(input_path) as img:
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            img_width, img_height = img.size
            crop_left, crop_top, crop_right, crop_bottom = CROP_BOX

            if crop_right > img_width or crop_bottom > img_height:
                echo.warning(
                    f"Image {input_path.name} is smaller than crop area ({img_width}x{img_height}), skipping crop"
                )
                cropped_img = img
            else:
                cropped_img = img.crop(CROP_BOX)

            pixels = cropped_img.load()

            width, height = cropped_img.size
            for x in range(width):
                for y in range(height):
                    pixel_rgb = pixels[x, y][:3]
                    if is_green_pixel(
                        pixel_rgb
                    ):
                        pixels[x, y] = (0, 255, 0, 0)

            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save with lossless compression
            cropped_img.save(
                output_path,
                "PNG",
                optimize=True,
                compress_level=9,
            )

        echo.success(f"Processed: {input_path.name} -> {output_path.name}")

    except Exception as e:
        echo.error(f"Failed to process {input_path.name}: {str(e)}")


def main():
    """
    Main function to process all outfit images
    """
    echo.info("Starting outfit image processing...")

    OUTPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    png_files = list(OUTFIT_PARSER_DIR.glob("*.png"))

    if not png_files:
        echo.warning(f"No PNG files found in {OUTFIT_PARSER_DIR}")
        return

    echo.info(f"Found {len(png_files)} PNG files to process")

    processed_count = 0
    error_count = 0

    for input_file in tqdm(png_files, desc="Processing outfit images", unit="images"):
        original_name = input_file.name
        if original_name.lower().endswith("female.png"):
            output_name = (
                original_name[:-10] + "Female.png"
            )
        elif original_name.lower().endswith("male.png"):
            output_name = (
                original_name[:-8] + "Male.png"
            )
        else:
            output_name = original_name

        output_file = OUTPUT_IMAGES_DIR / output_name

        try:
            process_outfit_image(input_file, output_file)
            processed_count += 1
        except Exception as e:
            echo.error(f"Failed to process {input_file.name}: {str(e)}")
            error_count += 1

    if error_count == 0:
        echo.success(
            f"Processing complete! All {processed_count} images processed successfully"
        )
    else:
        echo.warning(
            f"Processing complete! {processed_count} successful, {error_count} failed"
        )


if __name__ == "__main__":
    main()
