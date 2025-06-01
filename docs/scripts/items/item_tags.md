[Previous Folder](../fluids/fluid_article.md) | [Previous File](item_infobox.md) | [Next Folder](../lists/body_locations_list.md) | [Back to Index](../../index.md)

# item_tags.py

## Functions

### [`write_tag_image()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L24)

_Write each tag's item icons for `cycle-img`._
### [`write_tag_table()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L50)

_Write a wikitable showing all tags and corresponding items._
### [`write_tag_list()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L78)

_Write each tag item as an item_list._
### [`get_see_also(all_filenames, reference_filename)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L108)

_Get 3 similarly named filenames and include in 'see also'_
### [`write_article(tag, item_content, see_also_list, dest_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L130)
### [`get_item_list(source_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L171)
### [`generate_article_modding()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L193)
### [`generate_article_templates()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L218)
### [`get_tag_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L243)

_Retrieve tag data, generating it if not already._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary with keys as tag names, and values that are lists of items.
      - Each item is a dictionary with the following data:
      - - 'item_id': item's unique ID, including the module (Base).
      - - 'icon': item's icon.
      - - 'name': item's display name as it appears in-game.
      - - 'page': item's page name as it is on the wiki.
### [`generate_tags_dict()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L260)

_Generate a tags dictionary, mapping them to their associated items._
### [`run_function(option: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L316)
### [`display_menu(menu, is_root)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L350)
### [`nav_menu(menu, is_root)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L363)
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_tags.py#L378)


[Previous Folder](../fluids/fluid_article.md) | [Previous File](item_infobox.md) | [Next Folder](../lists/body_locations_list.md) | [Back to Index](../../index.md)
