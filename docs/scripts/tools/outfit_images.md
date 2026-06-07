[Previous Folder](../tiles/entity_article.md) | [Previous File](manual_tile_stitcher.md) | [Next File](page_name_checker.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)

# outfit_images.py

## Functions

### [`is_green_pixel(pixel_rgb)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/outfit_images.py#L27)

Check if a pixel is green using conservative tolerance-based detection.
Returns True if the pixel should be considered greenscreen.

### [`process_outfit_image(input_path: Path, output_path: Path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/outfit_images.py#L52)

Process a single outfit image:
1. Crop to specified coordinates
2. Remove green background pixels using tolerance-based detection
3. Save with maximum lossless compression

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/outfit_images.py#L104)

Main function to process all outfit images


[Previous Folder](../tiles/entity_article.md) | [Previous File](manual_tile_stitcher.md) | [Next File](page_name_checker.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)
