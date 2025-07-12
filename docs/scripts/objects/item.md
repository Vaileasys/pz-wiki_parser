[Previous Folder](../lists/attachment_list.md) | [Previous File](forage.md) | [Next File](profession.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

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

#### Static Methods
##### [`_lower_keys(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L388)

Converts the keys of a dictionary to lowercase.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Dictionary to normalise._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary with all top-level keys lowercased.

#### Class Methods
##### [`_load_items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L401)

Loads and normalises item script data into the class-level cache.

All dictionary keys are lowercased to ensure consistent access.

##### [`_parse_foraging_penalties()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L411)

Extracts clothing penalties from 'forageSystem.lua' and cache.

##### [`fix_item_id(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L420)

Attempts to fix a partial item_id by assuming the 'Base' module first,

then falling back to a full search through parsed item data.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _Either a full item_id ('Module.Item') or just an item name._

<ins>**Returns:**</ins>
  - **str:**
      - The best-guess full item_id.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L453)

Return all items as a dictionary of {item_id: Item}.

##### [`items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L460)

Return an iterable of (item_id, Item) pairs.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L465)

Return all item IDs as a keys view.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L472)

Return all Item instances as a generator.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L479)

Return the total number of loaded items.

##### [`get_icon_cache()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L486)

Return the cached list of item icon filenames.

##### [`load_burn_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L494)

Load and cache burn time data from camping_fuel.lua.

##### [`exists(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L515)
#### Object Methods
##### [`__new__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L332)

Return an existing Item instance if one already exists for the given ID.

Fixes partial IDs like 'Axe' to 'Base.Axe' before checking or creating the instance.

##### [`__init__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L350)

Initialise the Item instance with its data if not already initialised.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L375)

Allow dictionary-style access to item data (e.g., item["DisplayName"]).

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L379)

Allow 'in' checks for item data keys (e.g., "EvolvedRecipe" in item).

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L383)

Return a string representation of the Item showing name, ID, type, and source path.

##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L524)

Retrieve the value for a given key from item data.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
  - **default (any, optional)**:
      - _Fallback if the key is missing._

<ins>**Returns:**</ins>
  - **any:**
      - The value from data or the provided default.

##### [`_find_name(language: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L539)

Determines the display name of the item, handling special cases and translations.


<ins>**Args:**</ins>
  - **language (str, optional)**:
      - _Language code (e.g., 'en'). If None, uses the active language._

<ins>**Returns:**</ins>
  - **str:**
      - The resolved item name, including special case titles, vehicle part names, or translated display names.

##### [`_find_icon()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L611)

Detects and sets the item's icon(s), checking CSV overrides, item properties, and icon variants.

##### [`_format_icon(format: bool, all_icons: bool, cycling: bool, custom_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L697)

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
  - **str or list[str]:**
      - Formatted wiki markup or raw icon filename(s).

##### [`_calculate_burn_time()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L746)

Calculate and store the burn time for this item based on weight, category, tags, and fuel data.

##### [`calculate_weight(trait: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L819)
##### [`get_default(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L836)

Retrieve the value for a key using the class default if no explicit default is provided.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
  - **default (any, optional)**:
      - _Explicit fallback (overrides class default if provided)._

<ins>**Returns:**</ins>
  - **any:**
      - The value from data or the determined default.

##### [`get_component(key: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L852)

Retrieve a sprecific component dict from the item data.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The component key to look up._

<ins>**Returns:**</ins>
  - **dict:**
      - The subcomponent data or an empty dict if missing.

##### [`get_icon(format: bool, all_icons: bool, cycling: bool, custom_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L864)

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
  - **str or list[str]:**
      - Formatted wiki markup or raw icon filename(s).

##### [`get_skill(raw: bool, get_all: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L891)

Returns the skill(s) associated with the item.


<ins>**Args:**</ins>
  - **raw (bool)**:
      - _If True, returns the raw skill name(s) as string(s) instead of Skill objects._
  - **get_all (bool)**:
      - _If True, returns a list of all associated skills. Otherwise returns only the primary one._

<ins>**Returns:**</ins>
  - Skill | list[Skill] | str | list[str] | None: A single Skill or skill name, a list of Skills or names,
  - or None if no valid skill is found.

##### [`get_body_parts(do_link: bool, raw_id: bool, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L939)

Returns a list of body parts based on the item's `BloodLocation`.


<ins>**Args:**</ins>
  - **do_link (bool)**:
      - _If True, returns wiki-linked names. Otherwise returns plain names._
  - **raw_id (bool)**:
      - _If True, returns internal body part ids._
  - **default (Any)**:
      - _Value to return if no blood location data is found._

<ins>**Returns:**</ins>
  - list[str] | Any: A list of body part names or links, or the provided default value if no data is found.

##### [`get_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L960)
##### [`get_fabric()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L972)

Returns the item id for the item's fabric type.

##### [`has_tag()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L984)

Check if the item has any of the given tags.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **bool:**
      - True if any of the tags are present, False otherwise.

##### [`has_tags()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1007)

Check if the item has all of the given tags.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **bool:**
      - True if all tags are present, False otherwise.

##### [`has_category()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1029)

Check if the item has any of the given categories.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **bool:**
      - True if any of the categories are present, False otherwise.

##### [`name(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1112)
##### [`name_en(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1121)
#### Properties
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1057)
##### [`script_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1061)
##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1065)
##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1069)
##### [`item_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1073)
##### [`module`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1077)
##### [`id_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1081)
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1085)
##### [`has_page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1097)
##### [`translation_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1103)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1107)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1116)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1125)
##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1131)
##### [`icons`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1135)
##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1142)
##### [`display_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1144)
##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1149)
##### [`raw_display_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1151)
##### [`always_welcome_gift`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1153)
##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1155)
##### [`guid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1157)
##### [`raw_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1161)
##### [`icons_for_texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1163)
##### [`static_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1165)
##### [`world_static_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1167)
##### [`physics_object`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1169)
##### [`placed_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1171)
##### [`weapon_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1173)
##### [`eat_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1175)
##### [`swing_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1177)
##### [`idle_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1179)
##### [`run_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1181)
##### [`static_models_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1183)
##### [`world_static_models_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1185)
##### [`primary_anim_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1187)
##### [`secondary_anim_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1189)
##### [`world_object_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1191)
##### [`read_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1193)
##### [`scale_world_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1195)
##### [`use_world_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1197)
##### [`weapon_sprites_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1199)
##### [`color_blue`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1201)
##### [`color_green`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1203)
##### [`color_red`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1205)
##### [`icon_color_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1207)
##### [`icon_fluid_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1209)
##### [`dig_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1211)
##### [`pour_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1213)
##### [`place_multiple_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1217)
##### [`place_one_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1219)
##### [`cooking_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1221)
##### [`swing_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1223)
##### [`close_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1225)
##### [`open_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1227)
##### [`put_in_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1229)
##### [`break_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1231)
##### [`door_hit_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1233)
##### [`drop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1235)
##### [`hit_floor_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1237)
##### [`hit_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1239)
##### [`aim_release_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1241)
##### [`bring_to_bear_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1243)
##### [`click_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1245)
##### [`eject_ammo_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1247)
##### [`eject_ammo_start_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1249)
##### [`eject_ammo_stop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1251)
##### [`equip_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1253)
##### [`custom_eat_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1255)
##### [`impact_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1257)
##### [`insert_ammo_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1259)
##### [`insert_ammo_start_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1261)
##### [`insert_ammo_stop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1263)
##### [`damaged_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1265)
##### [`unequip_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1267)
##### [`rack_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1269)
##### [`npc_sound_boost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1271)
##### [`sound_parameter`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1273)
##### [`sound_map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1275)
##### [`fill_from_dispenser_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1277)
##### [`fill_from_lake_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1279)
##### [`fill_from_tap_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1281)
##### [`fill_from_toilet_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1283)
##### [`weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1287)
##### [`capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1289)
##### [`weight_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1291)
##### [`accept_item_function`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1293)
##### [`weight_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1295)
##### [`weapon_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1297)
##### [`max_item_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1299)
##### [`weight_empty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1301)
##### [`evolved_recipe`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1305)
##### [`evolved_recipe_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1307)
##### [`researchable_recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1309)
##### [`teached_recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1311)
##### [`sharpness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1313)
##### [`head_condition`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1315)
##### [`head_condition_lower_chance_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1317)
##### [`condition_lower_chance_one_in`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1319)
##### [`can_attach`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1321)
##### [`can_detach`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1323)
##### [`condition_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1325)
##### [`replace_on_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1327)
##### [`replace_on_use_on`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1329)
##### [`consolidate_option`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1331)
##### [`use_delta`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1333)
##### [`use_while_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1335)
##### [`use_self`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1337)
##### [`replace_on_deplete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1339)
##### [`remove_on_broken`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1341)
##### [`without_drainable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1343)
##### [`with_drainable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1345)
##### [`ticks_per_equip_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1347)
##### [`can_be_reused`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1349)
##### [`head_condition_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1351)
##### [`disappear_on_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1353)
##### [`cant_be_consolided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1355)
##### [`use_while_unequipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1357)
##### [`equipped_no_sprint`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1359)
##### [`protect_from_rain_when_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1361)
##### [`replace_on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1363)
##### [`item_after_cleaning`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1365)
##### [`can_barricade`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1367)
##### [`keep_on_deplete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1369)
##### [`chance_to_spawn_damaged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1371)
##### [`metal_value`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1373)
##### [`food_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1377)
##### [`days_fresh`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1379)
##### [`days_totally_rotten`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1381)
##### [`hunger_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1383)
##### [`thirst_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1385)
##### [`calories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1387)
##### [`carbohydrates`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1389)
##### [`lipids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1391)
##### [`proteins`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1393)
##### [`is_cookable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1395)
##### [`minutes_to_cook`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1397)
##### [`minutes_to_burn`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1399)
##### [`remove_unhappiness_when_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1401)
##### [`bad_cold`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1403)
##### [`bad_in_microwave`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1405)
##### [`dangerous_uncooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1407)
##### [`good_hot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1409)
##### [`cant_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1411)
##### [`cant_be_frozen`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1413)
##### [`animal_feed_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1415)
##### [`packaged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1417)
##### [`spice`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1419)
##### [`canned_food`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1421)
##### [`replace_on_rotten`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1423)
##### [`eat_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1425)
##### [`remove_negative_effect_on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1427)
##### [`unhappy_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1431)
##### [`boredom_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1433)
##### [`stress_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1435)
##### [`reduce_food_sickness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1437)
##### [`endurance_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1439)
##### [`poison_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1441)
##### [`medical`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1443)
##### [`alcoholic`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1445)
##### [`bandage_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1447)
##### [`can_bandage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1449)
##### [`alcohol_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1451)
##### [`reduce_infection_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1453)
##### [`fatigue_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1455)
##### [`flu_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1457)
##### [`herbalist_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1459)
##### [`pain_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1461)
##### [`explosion_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1465)
##### [`explosion_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1467)
##### [`explosion_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1469)
##### [`knockdown_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1471)
##### [`max_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1473)
##### [`max_hit_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1475)
##### [`max_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1477)
##### [`min_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1479)
##### [`minimum_swing_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1481)
##### [`swing_amount_before_impact`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1483)
##### [`swing_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1485)
##### [`trigger_explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1487)
##### [`can_be_placed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1489)
##### [`can_be_remote`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1491)
##### [`explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1493)
##### [`sensor_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1495)
##### [`alarm_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1497)
##### [`sound_radius`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1499)
##### [`reload_time_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1501)
##### [`mount_on`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1503)
##### [`part_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1505)
##### [`attachment_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1507)
##### [`base_speed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1509)
##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1511)
##### [`crit_dmg_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1513)
##### [`critical_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1515)
##### [`door_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1517)
##### [`knock_back_on_no_death`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1519)
##### [`min_angle`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1521)
##### [`min_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1523)
##### [`push_back_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1525)
##### [`splat_blood_on_no_death`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1527)
##### [`splat_number`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1529)
##### [`subcategory`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1531)
##### [`tree_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1533)
##### [`weapon_length`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1535)
##### [`projectile_spread_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1537)
##### [`max_range_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1539)
##### [`angle_falloff`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1541)
##### [`have_chamber`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1543)
##### [`insert_all_bullets_reload`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1545)
##### [`projectile_spread`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1547)
##### [`projectile_weight_center`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1549)
##### [`rack_after_shoot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1551)
##### [`range_falloff`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1553)
##### [`other_hand_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1555)
##### [`other_hand_require`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1557)
##### [`fire_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1559)
##### [`fire_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1561)
##### [`noise_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1563)
##### [`aiming_time_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1565)
##### [`hit_chance_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1567)
##### [`noise_duration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1569)
##### [`recoil_delay_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1571)
##### [`remote_controller`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1573)
##### [`remote_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1575)
##### [`manually_remove_spent_rounds`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1577)
##### [`explosion_duration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1579)
##### [`smoke_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1581)
##### [`count_`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1583)
##### [`ammo_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1585)
##### [`can_stack`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1587)
##### [`gun_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1589)
##### [`max_ammo`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1591)
##### [`aiming_perk_crit_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1593)
##### [`aiming_perk_hit_chance_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1595)
##### [`aiming_perk_min_angle_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1597)
##### [`aiming_perk_range_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1599)
##### [`aiming_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1601)
##### [`ammo_box`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1603)
##### [`fire_mode`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1605)
##### [`fire_mode_possibilities`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1607)
##### [`cyclic_rate_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1609)
##### [`hit_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1611)
##### [`is_aimed_firearm`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1613)
##### [`jam_gun_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1615)
##### [`magazine_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1617)
##### [`min_sight_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1619)
##### [`max_sight_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1621)
##### [`model_weapon_part`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1623)
##### [`multiple_hit_condition_affected`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1625)
##### [`piercing_bullets`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1627)
##### [`projectile_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1629)
##### [`ranged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1631)
##### [`recoil_delay`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1633)
##### [`reload_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1635)
##### [`requires_equipped_both_hands`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1637)
##### [`share_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1639)
##### [`shell_fall_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1641)
##### [`sound_gain`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1643)
##### [`sound_volume`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1645)
##### [`splat_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1647)
##### [`stop_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1649)
##### [`to_hit_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1651)
##### [`two_hand_weapon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1653)
##### [`use_endurance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1655)
##### [`weapon_reload_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1657)
##### [`clip_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1659)
##### [`damage_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1661)
##### [`damage_make_hole`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1663)
##### [`hit_angle_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1665)
##### [`endurance_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1667)
##### [`low_light_bonus`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1669)
##### [`always_knockdown`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1671)
##### [`aiming_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1673)
##### [`is_aimed_hand_weapon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1675)
##### [`cant_attack_with_lowest_endurance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1677)
##### [`close_kill_move`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1679)
##### [`body_location`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1683)
##### [`clothing_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1687)
##### [`can_be_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1693)
##### [`run_speed_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1697)
##### [`blood_location`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1699)
##### [`can_have_holes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1706)
##### [`chance_to_fall`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1708)
##### [`insulation`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1710)
##### [`wind_resistance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1712)
##### [`fabric_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1714)
##### [`scratch_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1716)
##### [`discomfort_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1718)
##### [`water_resistance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1720)
##### [`bite_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1722)
##### [`attachment_replacement`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1724)
##### [`clothing_item_extra`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1726)
##### [`clothing_item_extra_option`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1728)
##### [`replace_in_second_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1730)
##### [`replace_in_primary_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1732)
##### [`corpse_sickness_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1734)
##### [`hearing_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1736)
##### [`neck_protection_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1738)
##### [`visual_aid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1740)
##### [`vision_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1742)
##### [`attachments_provided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1744)
##### [`combat_speed_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1746)
##### [`bullet_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1748)
##### [`stomp_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1750)
##### [`tooltip`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1754)
##### [`custom_context_menu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1756)
##### [`clothing_extra_submenu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1758)
##### [`on_create`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1762)
##### [`on_break`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1764)
##### [`on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1766)
##### [`on_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1768)
##### [`accept_media_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1772)
##### [`media_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1774)
##### [`base_volume_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1776)
##### [`is_high_tier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1778)
##### [`is_portable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1780)
##### [`is_television`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1782)
##### [`max_channel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1784)
##### [`mic_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1786)
##### [`min_channel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1788)
##### [`no_transmit`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1790)
##### [`transmit_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1792)
##### [`two_way`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1794)
##### [`uses_battery`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1796)
##### [`require_in_hand_or_inventory`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1798)
##### [`activated_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1800)
##### [`light_distance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1802)
##### [`light_strength`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1804)
##### [`torch_cone`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1806)
##### [`torch_dot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1808)
##### [`vehicle_part_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1812)
##### [`brake_force`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1814)
##### [`engine_loudness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1816)
##### [`condition_lower_standard`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1818)
##### [`condition_lower_offroad`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1820)
##### [`suspension_damping`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1822)
##### [`suspension_compression`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1824)
##### [`wheel_friction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1826)
##### [`vehicle_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1828)
##### [`max_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1830)
##### [`mechanics_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1832)
##### [`condition_affects_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1834)
##### [`can_be_write`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1838)
##### [`page_to_write`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1840)
##### [`map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1842)
##### [`lvl_skill_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1844)
##### [`num_levels_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1846)
##### [`number_of_pages`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1848)
##### [`skill_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1850)
##### [`is_dung`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1858)
##### [`survival_gear`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1860)
##### [`fishing_lure`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1862)
##### [`trap`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1864)
##### [`padlock`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1866)
##### [`digital_padlock`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1868)
##### [`can_store_water`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1870)
##### [`is_water_source`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1872)
##### [`wet`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1874)
##### [`cosmetic`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1876)
##### [`obsolete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1878)
##### [`fire_fuel_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1882)
##### [`rain_factor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1884)
##### [`wet_cooldown`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1886)
##### [`origin_x`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1888)
##### [`origin_y`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1890)
##### [`origin_z`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1892)
##### [`item_when_dry`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1894)
##### [`spawn_with`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1896)
##### [`make_up_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1898)
##### [`shout_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1900)
##### [`shout_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1902)
##### [`components`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1907)

Returns a list of component keys defined for the item.

##### [`fluid_container`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1912)

Returns the item's FluidContainer component.

##### [`durability`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1919)

Returns the item's Durability component.

##### [`skill`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1929)

Returns the primary skill associated with the item, if any.

##### [`weight_full`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1938)

Returns the item's total weight when full, whether with fluids or items.

Rounded to 2 decimal places, returns an int if no remainder.

##### [`weapons`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1958)
##### [`burn_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1980)

Returns the burn time the item provides.

##### [`should_burn`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1989)

Returns True if the item is expected to burn.

Based on game logic from `ISCampingMenu.shouldBurn()`.

##### [`is_tinder`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2006)

Returns whether the item is valid tinder.

Based on game logic from `ISCampingMenu.isValidTinder()`.
Returns None if the item shouldn't burn.

##### [`models`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2037)

Returns a list of model texture filenames for this item.

Finds the correct model names based on clothing textures or static model values, and formats them as `<Name>_Model.png`.

##### [`skill_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2104)

XP multiplier based on the skill book and training level.

Returns 1 if no skill book is set.

##### [`foraging_penalty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2115)
##### [`body_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2129)
##### [`vehicle_type_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2133)
##### [`item_categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2139)
##### [`units`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2146)
##### [`material_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2150)
##### [`material`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2179)
##### [`foraging`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2191)
##### [`vehicle_part`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2197)

Return a VehiclePartItem view of this item if it is used

in any vehicle part; otherwise None.

##### [`vehicle_part_types`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L2222)


[Previous Folder](../lists/attachment_list.md) | [Previous File](forage.md) | [Next File](profession.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
