[Previous Folder](../tiles/entity_article.md) | [Previous File](outfit_images.md) | [Next File](update_icons.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)

# page_name_checker.py

Page name checker tool.

Compares item page names with their actual item names and outputs differences to JSON.
This helps identify items where the wiki page name doesn't match the in-game item name.

## Functions

### [`get_output_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/page_name_checker.py#L16)

Get the output file path for the page name checker results.

### [`check_page_names()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/page_name_checker.py#L21)

Check all items for differences between page names and item names.

For pages with multiple item IDs: if the first item's name matches the page name,
all items from that page are excluded from results.

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary with item IDs as keys and page_name/item_name as values._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/page_name_checker.py#L115)

Entry point for the page name checker tool.

Checks all items for differences between their wiki page names and in-game item names,
then outputs the results to a JSON file.


[Previous Folder](../tiles/entity_article.md) | [Previous File](outfit_images.md) | [Next File](update_icons.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)
