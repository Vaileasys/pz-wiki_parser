[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_recmedia_transcript.md) | [Next Folder](groups/ammo_groups.md) | [Back to Index](../../index.md)

# item_tags.py

## Functions

### [`_get_language_code()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L17)

Lazy-load language code to avoid import-time prompts.

### [`_get_output_tags_dir()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L24)

Lazy-load output tags directory to avoid import-time prompts.

### [`write_tag_image()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L36)

Write each tag's item icons for `cycle-img`.

### [`write_tag_table()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L62)

Write a wikitable showing all tags and corresponding items.

### [`write_tag_list()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L90)

Write each tag item as an item_list.

### [`get_see_also(all_filenames, reference_filename)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L120)

Get 3 similarly named filenames and include in 'see also'

### [`write_article(tag, item_content, see_also_list, dest_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L142)

### [`get_item_list(source_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L183)

### [`generate_article_modding()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L205)

### [`generate_article_templates()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L230)

### [`get_tag_data() -> dict[str, list[dict[str, str]]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L255)

Retrieve tag data, generating it if not already.

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary with keys as tag names, and values that are lists of items._
  - **Each item is a dictionary with the following data**:
  - **- 'item_id'**:
      - _item's unique ID, including the module (Base)._
  - **- 'icon'**:
      - _item's icon._
  - **- 'name'**:
      - _item's display name as it appears in-game._
  - **- 'page'**:
      - _item's page name as it is on the wiki._

### [`generate_tags_dict()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L272)

Generate a tags dictionary, mapping them to their associated items.

### [`run_function(option: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L365)

### [`display_menu(menu, is_root = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L399)

### [`nav_menu(menu, is_root = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L412)

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L427)

## Classes

### `Tag`

#### Class Methods

##### [`load() -> dict[str, list[dict[str, str]]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L310)

##### [`exists(tag: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L316)

#### Object Methods

##### [`__init__(tag: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L319)

#### Properties

##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L324)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L330)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L334)

##### [`template`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L338)


[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_recmedia_transcript.md) | [Next Folder](groups/ammo_groups.md) | [Back to Index](../../index.md)
