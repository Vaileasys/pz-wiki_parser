[Previous Folder](../tiles/entity_article.md) | [Previous File](generate_docs.md) | [Next File](outfit_images.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)

# manual_tile_stitcher.py

## Functions

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L442)

## Classes

### `SpriteItem`

Represents a sprite with its position and image.

#### Object Methods

##### [`__init__(sprite_name, x = 0, y = 0)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L30)

##### [`load_image()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L39)

Load the sprite image from disk.

##### [`get_photo_image()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L48)

Get PhotoImage for tkinter display.

### `ManualTileStitcher`

Main application for manual tile stitching.

#### Object Methods

##### [`__init__(root)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L58)

##### [`apply_dark_theme()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L78)

Apply dark theme to the application.

##### [`setup_ui()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L96)

Set up the user interface.

##### [`_remove_png_suffix(text)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L186)

Remove a trailing .png/.PNG extension from the provided text.

##### [`_normalize_expression(expression)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L192)

Normalize sprite expression text for consistent parsing.

##### [`_expand_expression_tokens(expression)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L198)

Expand shorthand expressions into full sprite names.

##### [`load_sprites()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L222)

Load sprites from the text input.

##### [`on_canvas_configure(event)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L273)

Handle canvas resize to update dimensions.

##### [`update_canvas()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L279)

Redraw all sprites on the canvas.

##### [`on_canvas_click(event)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L317)

Handle canvas click to select sprite and start dragging.

##### [`on_canvas_drag(event)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L342)

Handle dragging a sprite.

##### [`on_canvas_release(event)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L362)

Handle mouse release after dragging.

##### [`move_sprite(dx, dy)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L371)

Move the selected sprite by the given offset.

##### [`delete_selected_sprite()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L383)

Delete the currently selected sprite.

##### [`save_output()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/manual_tile_stitcher.py#L395)

Save the composite image to disk.


[Previous Folder](../tiles/entity_article.md) | [Previous File](generate_docs.md) | [Next File](outfit_images.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)
