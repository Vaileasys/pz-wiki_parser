[Previous Folder](../tools/update_icons.md) | [Previous File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# utility.py

## Functions

### [`get_item_data_from_id(item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L21)
### [`fix_item_id(item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L30)

Checks if an item_id is formatted correctly (i.e., 'module.item_name'). 

If not, it'll assume it's just the 'item_name' and search the parsed item data for its 'module'.
It will then return the full item_id.
:param item_id: The Item ID to check, which could be either in the format 'module.item_name' or just 'item_name' (without the module).
:type item_id: str
:returns: The correct item_id in the format 'module.item_name'. Otherwise it'll return the input string.
:rtype: item_id (str)
:example:
Given `item_id = "Cooked"` and `item_parser.get_item_data()` contains a key like `"Food.Cooked"`,
this function will return `"Food.Cooked"`.

### [`get_clothing_xml_value(item_data, xml_value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L58)
### [`get_model(item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L93)
### [`get_body_parts(item_data, link, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L152)

Gets body parts for an item and returns as a list.

:returns: Translated body parts.
:rtype: body_parts (list)

### [`get_skill_type_mapping(item_data, item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L207)
### [`get_burn_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L248)

Returns burn time data from camping_fuel.lua.

### [`get_burn_time(item_id, item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L274)
### [`save_cache(data: dict, data_file: str, data_dir, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L347)
### [`load_cache(cache_file, cache_name, get_version, backup_old, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L352)
### [`clear_cache(cache_path, cache_name, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L361)
### [`get_name(item_id, item_data: dict, language)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L367)

Gets an item name if it has a special case, otherwise translates the DisplayName.


<ins>**Args:**</ins>
  - **item_id (str)**:
      - _Item ID for the item to get the name for._
  - **item_data (dict, optional)**:
      - _The item properties to get the DisplayName from. Default will get the data based on the item ID, adds more overhead._
  - **language (str, optional)**:
      - _The language code to use when translating. Defaults to selected language code._

<ins>**Returns:**</ins>
  - **str:**
      - The items name as it is displayed in-game.

### [`get_item_id_data(suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L457)

Loads item_id_dictionary.csv into memory, mapping each page name to a list of item IDs found in its infobox.

:param suppress (bool, optional): Suppress print statements. Defaults to False.
:return: Returns all page names and the item IDs in the page's infobox.
:rtype: item_id_dict_data (dict)

### [`get_page(item_id, name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L500)
### [`find_icon(item_id, all_icons)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L512)

Retrieves the icon associated with a given item_id. Can return a single icon (string) (default) or multiple icons (list),

depending on the 'get_all_icons' parameter.
:param item_id (str): The ID of the item for which to retrieve the icon.
:param get_all_icons (bool, optional): If True, returns all icon variants as a list. If False (default), returns only the first icon as a string.
:return: The icon (or list of icons) associated with the item_id. Returns the default icon ("Question_On") if no specific icon is found.
:rtype: icon (list[str])

### [`get_icon(item_id, format, all_icons, cycling, custom_name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L638)

Retrieves the icon(s) associated with a given item_id, with optional formatting and cycling through multiple icons.

:param item_id: The ID of the item for which to retrieve the icon(s).
:type item_id: str
:param format: If True, formats the icon(s) with language-specific links, display names, and cycling support.
Defaults to False.
:type format: bool, optional
:param all_icons: If True, returns all icon variants for the item_id. If False, only the primary icon is returned.
Defaults to False.
:type all_icons: bool, optional
:param cycling: If True, formats the icons as a cycling image if there are multiple icons.
This option will force all_icons to be True. Defaults to False.
:type cycling: bool, optional
:return: The icon(s) associated with the item_id. If format is True, returns a formatted string. If format is False,
returns either a single icon (str).
:rtype: icon_result (str)

### [`get_guid(item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L713)
### [`get_fluid_name(fluid_data, lang)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L723)


[Previous Folder](../tools/update_icons.md) | [Previous File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
