[Previous Folder](../tools/compare_item_lists.md) | [Previous File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# utility.py

## Functions

### [`get_item_data_from_id(item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L23)
### [`fix_item_id(item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L29)

_Checks if an item_id is formatted correctly (i.e., 'module.item_name'). _

### [`get_clothing_xml_value(item_data, xml_value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L57)
### [`get_model(item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L92)
### [`get_body_parts(item_data, link, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L151)

_Gets body parts for an item and returns as a list._

### [`get_skill_type_mapping(item_data, item_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L206)
### [`get_burn_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L247)

_Returns burn time data from camping_fuel.lua._

### [`get_burn_time(item_id, item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L273)
### [`save_cache(data: dict, data_file: str, data_dir, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L346)
### [`load_cache(cache_file, cache_name, get_version, backup_old, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L351)
### [`clear_cache(cache_path, cache_name, suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L360)
### [`get_name(item_id, item_data, language)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L366)

_Gets an item name if it has a special case, otherwise translates the DisplayName._

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

### [`get_item_id_data(suppress)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L456)

_Loads item_id_dictionary.csv into memory, mapping each page name to a list of item IDs found in its infobox._

### [`get_page(item_id, name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L499)
### [`find_icon(item_id, all_icons)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L511)

_Retrieves the icon associated with a given item_id. Can return a single icon (string) (default) or multiple icons (list),_

### [`get_icon(item_id, format, all_icons, cycling, custom_name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L637)

_Retrieves the icon(s) associated with a given item_id, with optional formatting and cycling through multiple icons._

### [`get_guid(item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L712)
### [`get_fluid_name(fluid_data, lang)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L722)
### [`get_recipe(recipe_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/utility.py#L735)


[Previous Folder](../tools/compare_item_lists.md) | [Previous File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
