[Previous Folder](../navbox/navbox.md) | [Previous File](forage.md) | [Next File](outfit.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# item.py

The `Item` class is a centralised way to access and manipulate data from the parsed script data.
Some properties will return another object, so properties can be strung together.
E.g., `item.blood_location.body_parts.wiki_links` returns a list of body parts as formatted links for an item.

Instances are cached and reused automatically by item ID.

## Classes

### `Item`

Represents a single parsed game item.

Offers attribute-style access to raw values, translations,
default handling, icon/model discovery, and logic for derived values
like burn time or skill books. Also wraps component data
such as durability or fluid container info.

#### Class Methods

##### [`_load_items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L409)

Loads and normalises item script data into the class-level cache.

All dictionary keys are lowercased to ensure consistent access.

##### [`_generate_item_keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L419)

Generates and caches ItemKeys for all loaded items.

##### [`_parse_foraging_penalties()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L454)

Extracts clothing penalties from 'forageSystem.lua' and cache.

##### [`fix_item_id(item_id: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L469)

Attempts to fix a partial item_id by assuming the 'Base' module first,
then falling back to a full search through parsed item data.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _Either a full item_id ('Module.Item') or just an item name._

<ins>**Returns:**</ins>
  - **str**:
      - _The best-guess full item_id._

##### [`get_id_from_key(item_key: str) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L502)

Retrieves the full item ID corresponding to a given ItemKey.

<ins>**Args:**</ins>
  - **item_key (str)**:
      - _The ItemKey to look up._

<ins>**Returns:**</ins>
  - **str**:
      - _The corresponding full item ID, or None if not found._

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L523)

Return all items as a dictionary of {item_id: Item}.

##### [`items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L530)

Return an iterable of (item_id, Item) pairs.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L535)

Return all item IDs as a keys view.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L542)

Return all Item instances as a generator.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L549)

Return the total number of loaded items.

##### [`get_icon_cache()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L556)

Return the cached list of item icon filenames.

##### [`load_burn_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L566)

Load and cache burn time data from camping_fuel.lua.

##### [`exists(item_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L589)

#### Static Methods

##### [`_lower_keys(data: dict) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L394)

Converts the keys of a dictionary to lowercase.

<ins>**Args:**</ins>
  - **data (dict)**:
      - _Dictionary to normalise._

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary with all top-level keys lowercased._

#### Object Methods

##### [`__new__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L335)

Return an existing Item instance if one already exists for the given ID.

Fixes partial IDs like 'Axe' to 'Base.Axe' before checking or creating the instance.

##### [`__init__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L353)

Initialise the Item instance with its data if not already initialised.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L381)

Allow dictionary-style access to item data (e.g., item["DisplayName"]).

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L385)

Allow 'in' checks for item data keys (e.g., "EvolvedRecipe" in item).

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L389)

Return a string representation of the Item showing name, ID, type, and source path.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L598)

Retrieve the value for a given key from item data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
  - **default (any, optional)**:
      - _Fallback if the key is missing._

<ins>**Returns:**</ins>
  - **any**:
      - _The value from data or the provided default._

##### [`_find_name(language: str = None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L613)

Determines the display name of the item, handling special cases and translations.

<ins>**Args:**</ins>
  - **language (str, optional)**:
      - _Language code (e.g., 'en'). If None, uses the active language._

<ins>**Returns:**</ins>
  - **str**:
      - _The resolved item name, including special case titles, vehicle part names, or translated display names._

##### [`_find_icon()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L705)

Detects and sets the item's icon(s), checking CSV overrides, item properties, and icon variants.

##### [`_format_icon(format: bool = False, all_icons: bool = False, cycling: bool = False, custom_name: str = None) -> str | list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L809)

Formats the item's icon(s) for display or wiki markup, with optional cycling or custom names.

<ins>**Args:**</ins>
  - **format (bool, optional)**:
      - _Whether to return wiki-formatted markup._
  - **all_icons (bool, optional)**:
      - _Whether to include all icon variants._
  - **cycling (bool, optional)**:
      - _Whether to wrap icons in a cycling image span._
  - **custom_name (str, optional)**:
      - _Custom display name for the icon._

<ins>**Returns:**</ins>
  - **str or list[str]**:
      - _Formatted wiki markup or raw icon filename(s)._

##### [`_calculate_burn_time()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L863)

Calculate and store the burn time for this item based on weight, category, tags, and fuel data.

##### [`calculate_weight(trait: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L959)

##### [`get_default(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L975)

Retrieve the value for a key using the class default if no explicit default is provided.

<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
  - **default (any, optional)**:
      - _Explicit fallback (overrides class default if provided)._

<ins>**Returns:**</ins>
  - **any**:
      - _The value from data or the determined default._

##### [`get_component(key: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L991)

Retrieve a sprecific component dict from the item data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _The component key to look up._

<ins>**Returns:**</ins>
  - **dict**:
      - _The subcomponent data or an empty dict if missing._

##### [`get_icon(format: bool = True, all_icons: bool = True, cycling: bool = True, custom_name: str = None) -> str | list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1003)

Returns the item's icon(s), either as raw filenames or formatted wiki markup.

<ins>**Args:**</ins>
  - **format (bool, optional)**:
      - _Whether to return wiki-formatted markup. Defaults to True._
  - **all_icons (bool, optional)**:
      - _Whether to include all icon variants. Defaults to True._
  - **cycling (bool, optional)**:
      - _Whether to wrap icons in a cycling image span. Defaults to True._
  - **custom_name (str, optional)**:
      - _Custom display name for the icon. Defaults to None._

<ins>**Returns:**</ins>
  - **str or list[str]**:
      - _Formatted wiki markup or raw icon filename(s)._

##### [`get_skill(raw: bool = False, get_all: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1038)

Returns the skill(s) associated with the item.

<ins>**Args:**</ins>
  - **raw (bool)**:
      - _If True, returns the raw skill name(s) as string(s) instead of Skill objects._
  - **get_all (bool)**:
      - _If True, returns a list of all associated skills. Otherwise returns only the primary one._

<ins>**Returns:**</ins>
  - **Skill | list[Skill] | str | list[str] | None**:
      - _A single Skill or skill name, a list of Skills or names,_
  - **or None if no valid skill is found.**:

##### [`get_body_parts(do_link: bool = True, raw_id: bool = False, default = None) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1088)

Returns a list of body parts based on the item's `BloodLocation`.

<ins>**Args:**</ins>
  - **do_link (bool)**:
      - _If True, returns wiki-linked names. Otherwise returns plain names._
  - **raw_id (bool)**:
      - _If True, returns internal body part ids._
  - **default (Any)**:
      - _Value to return if no blood location data is found._

<ins>**Returns:**</ins>
  - **list[str] | Any**:
      - _A list of body part names or links, or the provided default value if no data is found._

##### [`get_recipes() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1111)

##### [`get_fabric() -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1124)

Returns the item id for the item's fabric type.

##### [`has_tag(*tags: str | list[str]) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1135)

Check if the item has any of the given tags.

<ins>**Args:**</ins>
  - ***tags (str | list[str])**:
      - _One or more tags to check. Can be individual strings or a list of strings._

<ins>**Returns:**</ins>
  - **bool**:
      - _True if any of the tags are present, False otherwise._

##### [`has_tags(*tags: str | list[str]) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1161)

Check if the item has all of the given tags.

<ins>**Args:**</ins>
  - ***tags (str | list[str])**:
      - _Tags to check. Accepts multiple strings or a list of strings._

<ins>**Returns:**</ins>
  - **bool**:
      - _True if all tags are present, False otherwise._

##### [`has_category(*categories: str | list[str]) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1186)

Check if the item has any of the given categories.

<ins>**Args:**</ins>
  - ***categories (str | list[str])**:
      - _One or more category names to check. Can be individual strings or a list._

<ins>**Returns:**</ins>
  - **bool**:
      - _True if any of the categories are present, False otherwise._

##### [`name(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1274)

##### [`name_en(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1292)

#### Properties

##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1214)

##### [`script_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1218)

##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1222)

##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1226)

##### [`item_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1230)

##### [`module`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1234)

##### [`id_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1238)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1242)

##### [`has_page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1254)

##### [`translation_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1260)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1264)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1280)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1296)

##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1302)

##### [`icons`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1306)

##### [`item_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1313)

##### [`item_key`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1317)

##### [`raw_display_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1325)

##### [`display_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1329)

##### [`display_category_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1337)

##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1352)

##### [`always_welcome_gift`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1356)

##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1360)

##### [`guid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1364)

##### [`raw_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1369)

##### [`icons_for_texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1373)

##### [`static_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1377)

##### [`world_static_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1381)

##### [`physics_object`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1385)

##### [`placed_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1389)

##### [`weapon_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1393)

##### [`eat_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1397)

##### [`swing_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1401)

##### [`idle_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1405)

##### [`run_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1409)

##### [`static_models_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1413)

##### [`world_static_models_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1417)

##### [`primary_anim_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1421)

##### [`secondary_anim_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1425)

##### [`world_object_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1429)

##### [`read_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1433)

##### [`scale_world_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1437)

##### [`use_world_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1441)

##### [`weapon_sprites_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1445)

##### [`color_blue`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1449)

##### [`color_green`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1453)

##### [`color_red`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1457)

##### [`icon_color_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1461)

##### [`icon_fluid_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1465)

##### [`dig_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1469)

##### [`pour_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1473)

##### [`place_multiple_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1478)

##### [`place_one_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1482)

##### [`cooking_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1486)

##### [`swing_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1490)

##### [`close_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1494)

##### [`open_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1498)

##### [`put_in_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1502)

##### [`break_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1506)

##### [`door_hit_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1510)

##### [`drop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1514)

##### [`hit_floor_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1518)

##### [`hit_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1522)

##### [`aim_release_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1526)

##### [`bring_to_bear_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1530)

##### [`click_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1534)

##### [`eject_ammo_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1538)

##### [`eject_ammo_start_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1542)

##### [`eject_ammo_stop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1546)

##### [`equip_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1550)

##### [`custom_eat_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1554)

##### [`impact_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1558)

##### [`insert_ammo_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1562)

##### [`insert_ammo_start_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1566)

##### [`insert_ammo_stop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1570)

##### [`damaged_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1574)

##### [`unequip_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1578)

##### [`rack_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1582)

##### [`npc_sound_boost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1586)

##### [`sound_parameter`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1590)

##### [`sound_map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1594)

##### [`fill_from_dispenser_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1598)

##### [`fill_from_lake_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1602)

##### [`fill_from_tap_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1606)

##### [`fill_from_toilet_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1610)

##### [`weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1615)

##### [`capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1619)

##### [`weight_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1623)

##### [`accept_item_function`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1627)

##### [`weight_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1631)

##### [`weapon_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1635)

##### [`max_item_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1639)

##### [`weight_empty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1643)

##### [`evolved_recipe`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1648)

##### [`evolved_recipe_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1652)

##### [`researchable_recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1656)

##### [`teached_recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1662)

##### [`sharpness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1666)

##### [`head_condition`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1670)

##### [`head_condition_lower_chance_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1674)

##### [`condition_lower_chance_one_in`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1680)

##### [`can_attach`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1684)

##### [`can_detach`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1688)

##### [`condition_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1692)

##### [`replace_on_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1696)

##### [`replace_on_use_on`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1700)

##### [`consolidate_option`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1704)

##### [`use_delta`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1708)

##### [`use_while_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1712)

##### [`use_self`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1716)

##### [`replace_on_deplete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1720)

##### [`remove_on_broken`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1724)

##### [`without_drainable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1728)

##### [`with_drainable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1732)

##### [`ticks_per_equip_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1736)

##### [`can_be_reused`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1740)

##### [`head_condition_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1744)

##### [`disappear_on_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1748)

##### [`cant_be_consolided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1752)

##### [`use_while_unequipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1756)

##### [`equipped_no_sprint`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1760)

##### [`protect_from_rain_when_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1764)

##### [`replace_on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1768)

##### [`item_after_cleaning`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1772)

##### [`can_barricade`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1776)

##### [`keep_on_deplete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1780)

##### [`chance_to_spawn_damaged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1784)

##### [`metal_value`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1788)

##### [`food_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1793)

##### [`days_fresh`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1797)

##### [`days_totally_rotten`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1801)

##### [`hunger_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1805)

##### [`thirst_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1809)

##### [`calories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1813)

##### [`carbohydrates`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1817)

##### [`lipids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1821)

##### [`proteins`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1825)

##### [`is_cookable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1829)

##### [`minutes_to_cook`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1833)

##### [`minutes_to_burn`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1837)

##### [`remove_unhappiness_when_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1841)

##### [`bad_cold`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1845)

##### [`bad_in_microwave`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1849)

##### [`dangerous_uncooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1853)

##### [`good_hot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1857)

##### [`cant_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1861)

##### [`cant_be_frozen`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1865)

##### [`animal_feed_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1869)

##### [`packaged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1873)

##### [`spice`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1877)

##### [`canned_food`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1881)

##### [`replace_on_rotten`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1885)

##### [`eat_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1889)

##### [`remove_negative_effect_on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1893)

##### [`unhappy_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1898)

##### [`boredom_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1902)

##### [`stress_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1906)

##### [`reduce_food_sickness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1910)

##### [`endurance_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1914)

##### [`poison_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1918)

##### [`medical`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1922)

##### [`alcoholic`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1926)

##### [`bandage_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1930)

##### [`can_bandage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1934)

##### [`alcohol_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1938)

##### [`reduce_infection_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1942)

##### [`fatigue_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1946)

##### [`flu_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1950)

##### [`herbalist_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1954)

##### [`pain_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1958)

##### [`explosion_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1963)

##### [`explosion_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1967)

##### [`explosion_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1971)

##### [`knockdown_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1975)

##### [`max_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1979)

##### [`max_hit_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1983)

##### [`max_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1987)

##### [`min_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1991)

##### [`minimum_swing_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1995)

##### [`swing_amount_before_impact`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1999)

##### [`swing_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2003)

##### [`trigger_explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2007)

##### [`can_be_placed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2011)

##### [`can_be_remote`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2015)

##### [`explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2019)

##### [`sensor_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2023)

##### [`alarm_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2027)

##### [`sound_radius`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2031)

##### [`reload_time_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2035)

##### [`mount_on`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2039)

##### [`part_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2043)

##### [`attachment_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2047)

##### [`base_speed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2051)

##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2055)

##### [`crit_dmg_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2059)

##### [`critical_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2063)

##### [`door_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2067)

##### [`knock_back_on_no_death`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2071)

##### [`min_angle`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2075)

##### [`min_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2079)

##### [`push_back_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2083)

##### [`splat_blood_on_no_death`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2087)

##### [`splat_number`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2091)

##### [`subcategory`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2095)

##### [`tree_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2099)

##### [`weapon_length`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2103)

##### [`projectile_spread_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2107)

##### [`max_range_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2111)

##### [`angle_falloff`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2115)

##### [`have_chamber`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2119)

##### [`insert_all_bullets_reload`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2123)

##### [`projectile_spread`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2127)

##### [`projectile_weight_center`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2131)

##### [`rack_after_shoot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2135)

##### [`range_falloff`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2139)

##### [`other_hand_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2143)

##### [`other_hand_require`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2147)

##### [`fire_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2151)

##### [`fire_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2155)

##### [`noise_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2159)

##### [`aiming_time_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2163)

##### [`hit_chance_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2167)

##### [`noise_duration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2171)

##### [`recoil_delay_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2175)

##### [`remote_controller`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2179)

##### [`remote_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2183)

##### [`manually_remove_spent_rounds`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2187)

##### [`explosion_duration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2191)

##### [`smoke_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2195)

##### [`count_`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2199)

##### [`ammo_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2203)

##### [`can_stack`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2216)

##### [`gun_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2220)

##### [`max_ammo`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2224)

##### [`aiming_perk_crit_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2228)

##### [`aiming_perk_hit_chance_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2232)

##### [`aiming_perk_min_angle_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2236)

##### [`aiming_perk_range_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2240)

##### [`aiming_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2244)

##### [`ammo_box`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2248)

##### [`fire_mode`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2252)

##### [`fire_mode_possibilities`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2256)

##### [`cyclic_rate_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2260)

##### [`hit_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2264)

##### [`is_aimed_firearm`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2268)

##### [`jam_gun_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2272)

##### [`magazine_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2276)

##### [`min_sight_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2280)

##### [`max_sight_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2284)

##### [`model_weapon_part`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2288)

##### [`multiple_hit_condition_affected`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2292)

##### [`piercing_bullets`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2296)

##### [`projectile_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2300)

##### [`ranged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2304)

##### [`recoil_delay`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2308)

##### [`reload_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2312)

##### [`requires_equipped_both_hands`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2316)

##### [`share_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2320)

##### [`shell_fall_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2324)

##### [`sound_gain`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2328)

##### [`sound_volume`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2332)

##### [`splat_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2336)

##### [`stop_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2340)

##### [`to_hit_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2344)

##### [`two_hand_weapon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2348)

##### [`use_endurance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2352)

##### [`weapon_reload_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2356)

##### [`clip_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2360)

##### [`damage_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2364)

##### [`damage_make_hole`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2368)

##### [`hit_angle_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2372)

##### [`endurance_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2376)

##### [`low_light_bonus`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2380)

##### [`always_knockdown`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2384)

##### [`aiming_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2388)

##### [`is_aimed_hand_weapon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2392)

##### [`cant_attack_with_lowest_endurance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2396)

##### [`close_kill_move`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2400)

##### [`body_location`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2405)

##### [`clothing_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2410)

##### [`can_be_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2417)

##### [`run_speed_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2422)

##### [`blood_location`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2426)

##### [`can_have_holes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2434)

##### [`chance_to_fall`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2438)

##### [`insulation`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2442)

##### [`wind_resistance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2446)

##### [`fabric_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2450)

##### [`scratch_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2454)

##### [`discomfort_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2458)

##### [`water_resistance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2462)

##### [`bite_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2466)

##### [`attachment_replacement`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2470)

##### [`clothing_item_extra`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2474)

##### [`clothing_item_extra_option`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2478)

##### [`replace_in_second_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2482)

##### [`replace_in_primary_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2486)

##### [`corpse_sickness_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2490)

##### [`hearing_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2494)

##### [`neck_protection_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2498)

##### [`visual_aid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2502)

##### [`vision_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2506)

##### [`attachments_provided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2510)

##### [`combat_speed_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2514)

##### [`bullet_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2518)

##### [`stomp_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2522)

##### [`tooltip`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2527)

##### [`custom_context_menu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2531)

##### [`clothing_extra_submenu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2535)

##### [`on_create`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2542)

##### [`on_break`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2546)

##### [`on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2550)

##### [`on_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2554)

##### [`accept_media_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2559)

##### [`media_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2563)

##### [`base_volume_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2567)

##### [`is_high_tier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2571)

##### [`is_portable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2575)

##### [`is_television`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2579)

##### [`max_channel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2583)

##### [`mic_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2587)

##### [`min_channel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2591)

##### [`no_transmit`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2595)

##### [`transmit_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2599)

##### [`two_way`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2603)

##### [`uses_battery`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2607)

##### [`require_in_hand_or_inventory`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2611)

##### [`activated_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2615)

##### [`light_distance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2619)

##### [`light_strength`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2623)

##### [`torch_cone`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2627)

##### [`torch_dot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2631)

##### [`vehicle_part_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2636)

##### [`brake_force`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2640)

##### [`engine_loudness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2644)

##### [`condition_lower_standard`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2648)

##### [`condition_lower_offroad`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2652)

##### [`suspension_damping`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2656)

##### [`suspension_compression`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2660)

##### [`wheel_friction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2664)

##### [`vehicle_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2668)

##### [`max_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2672)

##### [`mechanics_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2676)

##### [`condition_affects_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2680)

##### [`can_be_write`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2685)

##### [`page_to_write`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2689)

##### [`map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2693)

##### [`lvl_skill_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2697)

##### [`num_levels_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2701)

##### [`number_of_pages`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2705)

##### [`skill_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2709)

##### [`is_dung`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2719)

##### [`survival_gear`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2723)

##### [`fishing_lure`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2727)

##### [`trap`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2731)

##### [`padlock`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2735)

##### [`digital_padlock`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2739)

##### [`can_store_water`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2743)

##### [`is_water_source`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2747)

##### [`wet`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2751)

##### [`cosmetic`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2755)

##### [`obsolete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2759)

##### [`fire_fuel_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2764)

##### [`rain_factor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2768)

##### [`wet_cooldown`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2772)

##### [`origin_x`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2776)

##### [`origin_y`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2780)

##### [`origin_z`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2784)

##### [`item_when_dry`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2788)

##### [`spawn_with`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2792)

##### [`make_up_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2796)

##### [`shout_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2800)

##### [`shout_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2804)

##### [`components`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2810)

Returns a list of component keys defined for the item.

##### [`fluid_container`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2815)

Returns the item's FluidContainer component.

##### [`durability`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2822)

Returns the item's Durability component.

##### [`skill`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2831)

Returns the primary skill associated with the item, if any.

##### [`weight_full`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2840)

Returns the item's total weight when full, whether with fluids or items.
Rounded to 2 decimal places, returns an int if no remainder.

##### [`weapons`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2860)

##### [`burn_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2881)

Returns the burn time the item provides.

##### [`should_burn`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2890)

Returns True if the item is expected to burn.
Based on game logic from `ISCampingMenu.shouldBurn()`.

##### [`is_tinder`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2909)

Returns whether the item is valid tinder.
Based on game logic from `ISCampingMenu.isValidTinder()`.
Returns None if the item shouldn't burn.

##### [`models`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2948)

Returns a list of model texture filenames for this item.
Finds the correct model names based on clothing textures or static model values, and formats them as `<Name>_Model.png`.

##### [`skill_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3022)

XP multiplier based on the skill book and training level.
Returns 1 if no skill book is set.

##### [`foraging_penalty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3033)

##### [`body_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3051)

##### [`vehicle_type_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3055)

##### [`item_categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3068)

##### [`units`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3076)

##### [`material_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3080)

##### [`material`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3138)

##### [`foraging`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3152)

##### [`vehicle_part`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3159)

Return a VehiclePartItem view of this item if it is used
in any vehicle part; otherwise None.

##### [`vehicle_part_types`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3184)

##### [`fish`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L3195)


[Previous Folder](../navbox/navbox.md) | [Previous File](forage.md) | [Next File](outfit.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
