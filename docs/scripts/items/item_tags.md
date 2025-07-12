[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_literature_titles.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)

# item_tags.py

## Functions

### [`write_tag_image()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L22)

Write each tag's item icons for `cycle-img`.

### [`write_tag_table()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L48)

Write a wikitable showing all tags and corresponding items.

### [`write_tag_list()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L76)

Write each tag item as an item_list.

### [`get_see_also(all_filenames, reference_filename)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L106)

Get 3 similarly named filenames and include in 'see also'

### [`write_article(tag, item_content, see_also_list, dest_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L128)
### [`get_item_list(source_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L169)
### [`generate_article_modding()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L191)
### [`generate_article_templates()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L216)
### [`get_tag_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L241)

Retrieve tag data, generating it if not already.


<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary with keys as tag names, and values that are lists of items.
      - Each item is a dictionary with the following data:
        - 'item_id': item's unique ID, including the module (Base).
        - 'icon': item's icon.
        - 'name': item's display name as it appears in-game.
        - 'page': item's page name as it is on the wiki.

### [`generate_tags_dict()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L258)

Generate a tags dictionary, mapping them to their associated items.

### [`run_function(option: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L351)
### [`display_menu(menu, is_root)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L385)
### [`nav_menu(menu, is_root)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L398)
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L413)

## Classes

### `Tag`
#### Class Methods
##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L296)
##### [`exists(tag: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L302)
#### Object Methods
##### [`__init__(tag: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L305)
#### Properties
##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L310)
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L316)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L320)
##### [`template`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L324)


[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_literature_titles.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)
