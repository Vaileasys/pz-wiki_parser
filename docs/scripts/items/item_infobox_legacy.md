[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_infobox.md) | [Next File](item_lists.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)

# item_infobox_legacy.py

## Functions

### [`generate_clothing_penalties()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L29)

Extracts clothing penalties from 'forageSystem.lua' and stores in memory as 'clothing_penalties'.

### [`get_item()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L38)
### [`get_item_ids(item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L47)
### [`get_descriptor(item_ids: list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L62)
### [`enumerate_params(parameters)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L95)
### [`remove_descriptor(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L110)

Removes the descriptor from the end of string.

### [`get_any_property(items: dict, script_param: bool | str | int | float | list, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L117)

Gets the first property value that isn't None and returns it.

Used for items with multiple variants.

### [`get_param_values(items: dict, script_param: str, rstring: bool, default: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L137)

Gets the script parameter values for a list of items.

:param items: dict - A dictionary where keys are item IDs and values are item data dictionaries.
:param script_param: str - The key for the script parameter to retrieve values from each item.
:param rstring: bool, optional - If True, returns a string with values joined by "<br>", otherwise returns a list. Default is False.
:param default: str, optional - The default value to use if the script parameter is not found in an item. Default is None.
:return: list or str - A list of unique parameter values or a string if rstring is True.

### [`generate_infobox(item_id, item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L164)
### [`process_item(item_id, item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L494)
### [`automatic_extraction()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L515)
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_infobox_legacy.py#L530)


[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_infobox.md) | [Next File](item_lists.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)
