[Previous Folder](../tools/batch_processor.md) | [Previous File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# utility.py

## Functions

### [`get_item_data_from_id(item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L22)

### [`fix_item_id(item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L31)

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

### [`get_clothing_xml_value(item_data, xml_value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L59)

### [`get_model(item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L98)

### [`get_body_parts(item_data, link = True, default = '')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L160)

Gets body parts for an item and returns as a list.

:returns: Translated body parts.
:rtype: body_parts (list)

### [`get_skill_type_mapping(item_data, item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L221)

### [`get_burn_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L264)

Returns burn time data from camping_fuel.lua.

### [`get_burn_time(item_id, item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L292)

### [`save_cache(data: dict, data_file: str, data_dir = DATA_DIR, suppress = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L382)

### [`load_cache(cache_file, cache_name = 'data', get_version = False, backup_old = False, suppress = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L389)

### [`clear_cache(cache_path = DATA_DIR, cache_name = None, suppress = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L414)

### [`get_name(item_id, item_data: dict = {}, language = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L422)

Gets an item name if it has a special case, otherwise translates the DisplayName.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _Item ID for the item to get the name for._
  - **item_data (dict, optional)**:
      - _The item properties to get the DisplayName from. Default will get the data based on the item ID, adds more overhead._
  - **language (str, optional)**:
      - _The language code to use when translating. Defaults to selected language code._

<ins>**Returns:**</ins>
  - **str**:
      - _The items name as it is displayed in-game._

### [`get_item_id_data(suppress = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L516)

Loads item_id_dictionary.csv into memory, mapping each page name to a list of item IDs found in its infobox.

:param suppress (bool, optional): Suppress print statements. Defaults to False.

:return: Returns all page names and the item IDs in the page's infobox.
:rtype: item_id_dict_data (dict)

### [`get_page(item_id, name = 'Unknown')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L561)

### [`find_icon(item_id, all_icons = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L573)

Retrieves the icon associated with a given item_id. Can return a single icon (string) (default) or multiple icons (list),
depending on the 'get_all_icons' parameter.

:param item_id (str): The ID of the item for which to retrieve the icon.
:param get_all_icons (bool, optional): If True, returns all icon variants as a list. If False (default), returns only the first icon as a string.

:return: The icon (or list of icons) associated with the item_id. Returns the default icon ("Question_On") if no specific icon is found.
:rtype: icon (list[str])

### [`get_icon(item_id, format = False, all_icons = False, cycling = False, custom_name = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L720)

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

### [`get_guid(item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L794)

### [`get_fluid_name(fluid_data, lang = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L804)


[Previous Folder](../tools/batch_processor.md) | [Previous File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
