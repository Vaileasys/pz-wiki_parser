[Previous Folder](../fluids/fluid_article.md) | [Previous File](item_infobox.md) | [Next Folder](../lists/body_locations_list.md) | [Back to Index](../../index.md)

# item_tags.py

## Functions

### [`write_tag_image()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L23)

Write each tag's item icons for `cycle-img`.

### [`write_tag_table()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L49)

Write a wikitable showing all tags and corresponding items.

### [`write_tag_list()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L77)

Write each tag item as an item_list.

### [`get_see_also(all_filenames, reference_filename)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L107)

Get 3 similarly named filenames and include in 'see also'

### [`write_article(tag, item_content, see_also_list, dest_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L129)
### [`get_item_list(source_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L170)
### [`generate_article_modding()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L192)
### [`generate_article_templates()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L217)
### [`get_tag_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L242)

Retrieve tag data, generating it if not already.


<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary with keys as tag names, and values that are lists of items.
      - Each item is a dictionary with the following data:
        - 'item_id': item's unique ID, including the module (Base).
        - 'icon': item's icon.
        - 'name': item's display name as it appears in-game.
        - 'page': item's page name as it is on the wiki.

### [`generate_tags_dict()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L259)

Generate a tags dictionary, mapping them to their associated items.

### [`run_function(option: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L315)
### [`display_menu(menu, is_root)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L349)
### [`nav_menu(menu, is_root)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L362)
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L377)


[Previous Folder](../fluids/fluid_article.md) | [Previous File](item_infobox.md) | [Next Folder](../lists/body_locations_list.md) | [Back to Index](../../index.md)
