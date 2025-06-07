[Previous Folder](../lists/body_locations_list.md) | [Previous File](fluid.md) | [Next File](skill.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

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
##### [`_load_items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L362)

Load item data only once and store in class-level cache.

##### [`fix_item_id(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L367)

Attempts to fix a partial item_id by assuming the 'Base' module first,

then falling back to a full search through parsed item data.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _Either a full item_id ('Module.Item') or just an item name._

<ins>**Returns:**</ins>
  - **str:**
      - The best-guess full item_id.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L397)

Return all items as a dictionary of {item_id: Item}.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L404)

Return all item IDs as a keys view.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L411)

Return all Item instances as a generator.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L418)

Return the total number of loaded items.

##### [`get_icon_cache()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L425)

Return the cached list of item icon filenames.

##### [`load_burn_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L433)

Load and cache burn time data from camping_fuel.lua.

#### Object Methods
##### [`__new__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L308)

Return an existing Item instance if one already exists for the given ID.

Fixes partial IDs like 'Axe' to 'Base.Axe' before checking or creating the instance.

##### [`__init__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L326)

Initialise the Item instance with its data if not already initialised.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L349)

Allow dictionary-style access to item data (e.g., item["DisplayName"]).

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L353)

Allow 'in' checks for item data keys (e.g., "EvolvedRecipe" in item).

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L357)

Return a string representation of the Item showing name, ID, type, and source path.

##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L455)

Retrieve the value for a given key from item data.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
  - **default (any, optional)**:
      - _Fallback if the key is missing._

<ins>**Returns:**</ins>
  - **any:**
      - The value from data or the provided default.

##### [`_find_name(language: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L470)

Determines the display name of the item, handling special cases and translations.


<ins>**Args:**</ins>
  - **language (str, optional)**:
      - _Language code (e.g., 'en'). If None, uses the active language._

<ins>**Returns:**</ins>
  - **str:**
      - The resolved item name, including special case titles, vehicle part names, or translated display names.

##### [`_find_icon()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L542)

Detects and sets the item's icon(s), checking CSV overrides, item properties, and icon variants.

##### [`_format_icon(format: bool, all_icons: bool, cycling: bool, custom_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L628)

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

##### [`_calculate_burn_time()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L677)

Calculate and store the burn time for this item based on weight, category, tags, and fuel data.

##### [`get_default(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L752)

Retrieve the value for a key using the class default if no explicit default is provided.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
  - **default (any, optional)**:
      - _Explicit fallback (overrides class default if provided)._

<ins>**Returns:**</ins>
  - **any:**
      - The value from data or the determined default.

##### [`get_component(key: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L766)

Retrieve a sprecific component dict from the item data.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The component key to look up._

<ins>**Returns:**</ins>
  - **dict:**
      - The subcomponent data or an empty dict if missing.

##### [`get_icon(format: bool, all_icons: bool, cycling: bool, custom_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L778)

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

##### [`get_skill(raw: bool, get_all: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L805)

Returns the skill(s) associated with the item.


<ins>**Args:**</ins>
  - **raw (bool)**:
      - _If True, returns the raw skill name(s) as string(s) instead of Skill objects._
  - **get_all (bool)**:
      - _If True, returns a list of all associated skills. Otherwise returns only the primary one._

<ins>**Returns:**</ins>
  - Skill | list[Skill] | str | list[str] | None: A single Skill or skill name, a list of Skills or names,
  - or None if no valid skill is found.

##### [`get_body_parts(do_link, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L850)

Returns a list of body parts based on the item's `BloodLocation`.


<ins>**Args:**</ins>
  - **do_link (bool)**:
      - _If True, returns wiki-linked names. Otherwise returns plain names._
  - **default (Any)**:
      - _Value to return if no blood location data is found._

<ins>**Returns:**</ins>
  - list[str] | Any: A list of body part names or links, or the provided default value if no data is found.

##### [`get_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L868)
##### [`has_tag(tag: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L882)

Check if the item has a specific tag.


<ins>**Args:**</ins>
  - **tag (str)**:
      - _The tag name to check._

<ins>**Returns:**</ins>
  - **bool:**
      - True if the tag is present, False otherwise.

#### Properties
##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L899)
##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L903)
##### [`item_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L907)
##### [`module`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L911)
##### [`id_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L915)
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L919)
##### [`has_page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L931)
##### [`translation_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L937)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L941)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L947)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L953)
##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L959)
##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L966)
##### [`display_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L968)
##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L973)
##### [`raw_display_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L975)
##### [`always_welcome_gift`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L977)
##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L979)
##### [`raw_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L983)
##### [`icons_for_texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L985)
##### [`static_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L987)
##### [`world_static_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L989)
##### [`physics_object`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L991)
##### [`placed_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L993)
##### [`weapon_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L995)
##### [`eat_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L997)
##### [`swing_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L999)
##### [`idle_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1001)
##### [`run_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1003)
##### [`static_models_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1005)
##### [`world_static_models_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1007)
##### [`primary_anim_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1009)
##### [`secondary_anim_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1011)
##### [`world_object_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1013)
##### [`read_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1015)
##### [`scale_world_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1017)
##### [`use_world_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1019)
##### [`weapon_sprites_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1021)
##### [`color_blue`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1023)
##### [`color_green`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1025)
##### [`color_red`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1027)
##### [`icon_color_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1029)
##### [`icon_fluid_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1031)
##### [`dig_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1033)
##### [`pour_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1035)
##### [`place_multiple_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1039)
##### [`place_one_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1041)
##### [`cooking_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1043)
##### [`swing_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1045)
##### [`close_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1047)
##### [`open_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1049)
##### [`put_in_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1051)
##### [`break_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1053)
##### [`door_hit_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1055)
##### [`drop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1057)
##### [`hit_floor_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1059)
##### [`hit_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1061)
##### [`aim_release_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1063)
##### [`bring_to_bear_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1065)
##### [`click_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1067)
##### [`eject_ammo_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1069)
##### [`eject_ammo_start_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1071)
##### [`eject_ammo_stop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1073)
##### [`equip_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1075)
##### [`custom_eat_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1077)
##### [`impact_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1079)
##### [`insert_ammo_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1081)
##### [`insert_ammo_start_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1083)
##### [`insert_ammo_stop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1085)
##### [`damaged_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1087)
##### [`unequip_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1089)
##### [`rack_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1091)
##### [`npc_sound_boost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1093)
##### [`sound_parameter`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1095)
##### [`sound_map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1097)
##### [`fill_from_dispenser_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1099)
##### [`fill_from_lake_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1101)
##### [`fill_from_tap_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1103)
##### [`fill_from_toilet_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1105)
##### [`weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1109)
##### [`capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1111)
##### [`weight_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1113)
##### [`accept_item_function`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1115)
##### [`weight_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1117)
##### [`weapon_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1119)
##### [`max_item_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1121)
##### [`weight_empty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1123)
##### [`evolved_recipe`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1127)
##### [`evolved_recipe_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1129)
##### [`researchable_recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1131)
##### [`teached_recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1133)
##### [`sharpness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1135)
##### [`head_condition`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1137)
##### [`head_condition_lower_chance_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1139)
##### [`condition_lower_chance_one_in`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1141)
##### [`can_attach`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1143)
##### [`can_detach`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1145)
##### [`condition_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1147)
##### [`replace_on_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1149)
##### [`replace_on_use_on`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1151)
##### [`consolidate_option`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1153)
##### [`use_delta`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1155)
##### [`use_while_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1157)
##### [`use_self`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1159)
##### [`replace_on_deplete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1161)
##### [`remove_on_broken`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1163)
##### [`without_drainable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1165)
##### [`with_drainable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1167)
##### [`ticks_per_equip_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1169)
##### [`can_be_reused`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1171)
##### [`head_condition_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1173)
##### [`disappear_on_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1175)
##### [`cant_be_consolided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1177)
##### [`use_while_unequipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1179)
##### [`equipped_no_sprint`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1181)
##### [`protect_from_rain_when_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1183)
##### [`replace_on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1185)
##### [`item_after_cleaning`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1187)
##### [`can_barricade`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1189)
##### [`keep_on_deplete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1191)
##### [`chance_to_spawn_damaged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1193)
##### [`metal_value`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1195)
##### [`food_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1199)
##### [`days_fresh`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1201)
##### [`days_totally_rotten`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1203)
##### [`hunger_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1205)
##### [`thirst_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1207)
##### [`calories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1209)
##### [`carbohydrates`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1211)
##### [`lipids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1213)
##### [`proteins`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1215)
##### [`is_cookable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1217)
##### [`minutes_to_cook`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1219)
##### [`minutes_to_burn`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1221)
##### [`remove_unhappiness_when_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1223)
##### [`bad_cold`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1225)
##### [`bad_in_microwave`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1227)
##### [`dangerous_uncooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1229)
##### [`good_hot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1231)
##### [`cant_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1233)
##### [`cant_be_frozen`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1235)
##### [`animal_feed_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1237)
##### [`packaged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1239)
##### [`spice`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1241)
##### [`canned_food`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1243)
##### [`replace_on_rotten`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1245)
##### [`eat_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1247)
##### [`remove_negative_effect_on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1249)
##### [`unhappy_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1253)
##### [`boredom_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1255)
##### [`stress_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1257)
##### [`reduce_food_sickness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1259)
##### [`endurance_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1261)
##### [`poison_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1263)
##### [`medical`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1265)
##### [`alcoholic`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1267)
##### [`bandage_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1269)
##### [`can_bandage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1271)
##### [`alcohol_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1273)
##### [`reduce_infection_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1275)
##### [`fatigue_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1277)
##### [`flu_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1279)
##### [`herbalist_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1281)
##### [`pain_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1283)
##### [`explosion_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1287)
##### [`explosion_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1289)
##### [`explosion_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1291)
##### [`knockdown_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1293)
##### [`max_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1295)
##### [`max_hit_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1297)
##### [`max_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1299)
##### [`min_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1301)
##### [`minimum_swing_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1303)
##### [`swing_amount_before_impact`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1305)
##### [`swing_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1307)
##### [`trigger_explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1309)
##### [`can_be_placed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1311)
##### [`can_be_remote`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1313)
##### [`explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1315)
##### [`sensor_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1317)
##### [`alarm_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1319)
##### [`sound_radius`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1321)
##### [`reload_time_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1323)
##### [`mount_on`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1325)
##### [`part_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1327)
##### [`attachment_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1329)
##### [`base_speed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1331)
##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1333)
##### [`crit_dmg_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1335)
##### [`critical_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1337)
##### [`door_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1339)
##### [`knock_back_on_no_death`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1341)
##### [`min_angle`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1343)
##### [`min_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1345)
##### [`push_back_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1347)
##### [`splat_blood_on_no_death`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1349)
##### [`splat_number`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1351)
##### [`subcategory`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1353)
##### [`tree_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1355)
##### [`weapon_length`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1357)
##### [`projectile_spread_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1359)
##### [`max_range_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1361)
##### [`angle_falloff`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1363)
##### [`have_chamber`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1365)
##### [`insert_all_bullets_reload`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1367)
##### [`projectile_spread`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1369)
##### [`projectile_weight_center`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1371)
##### [`rack_after_shoot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1373)
##### [`range_falloff`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1375)
##### [`other_hand_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1377)
##### [`other_hand_require`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1379)
##### [`fire_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1381)
##### [`fire_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1383)
##### [`noise_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1385)
##### [`aiming_time_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1387)
##### [`hit_chance_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1389)
##### [`noise_duration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1391)
##### [`recoil_delay_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1393)
##### [`remote_controller`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1395)
##### [`remote_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1397)
##### [`manually_remove_spent_rounds`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1399)
##### [`explosion_duration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1401)
##### [`smoke_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1403)
##### [`count_`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1405)
##### [`ammo_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1407)
##### [`can_stack`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1409)
##### [`gun_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1411)
##### [`max_ammo`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1413)
##### [`aiming_perk_crit_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1415)
##### [`aiming_perk_hit_chance_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1417)
##### [`aiming_perk_min_angle_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1419)
##### [`aiming_perk_range_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1421)
##### [`aiming_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1423)
##### [`ammo_box`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1425)
##### [`fire_mode`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1427)
##### [`fire_mode_possibilities`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1429)
##### [`cyclic_rate_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1431)
##### [`hit_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1433)
##### [`is_aimed_firearm`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1435)
##### [`jam_gun_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1437)
##### [`magazine_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1439)
##### [`min_sight_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1441)
##### [`max_sight_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1443)
##### [`model_weapon_part`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1445)
##### [`multiple_hit_condition_affected`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1447)
##### [`piercing_bullets`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1449)
##### [`projectile_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1451)
##### [`ranged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1453)
##### [`recoil_delay`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1455)
##### [`reload_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1457)
##### [`requires_equipped_both_hands`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1459)
##### [`share_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1461)
##### [`shell_fall_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1463)
##### [`sound_gain`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1465)
##### [`sound_volume`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1467)
##### [`splat_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1469)
##### [`stop_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1471)
##### [`to_hit_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1473)
##### [`two_hand_weapon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1475)
##### [`use_endurance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1477)
##### [`weapon_reload_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1479)
##### [`clip_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1481)
##### [`damage_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1483)
##### [`damage_make_hole`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1485)
##### [`hit_angle_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1487)
##### [`endurance_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1489)
##### [`low_light_bonus`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1491)
##### [`always_knockdown`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1493)
##### [`crit_dmg_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1495)
##### [`aiming_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1497)
##### [`is_aimed_hand_weapon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1499)
##### [`cant_attack_with_lowest_endurance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1501)
##### [`close_kill_move`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1503)
##### [`body_location`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1507)
##### [`clothing_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1511)
##### [`can_be_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1517)
##### [`run_speed_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1521)
##### [`blood_location`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1523)
##### [`can_have_holes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1530)
##### [`chance_to_fall`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1532)
##### [`insulation`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1534)
##### [`wind_resistance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1536)
##### [`fabric_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1538)
##### [`scratch_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1540)
##### [`discomfort_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1542)
##### [`water_resistance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1544)
##### [`bite_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1546)
##### [`attachment_replacement`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1548)
##### [`clothing_item_extra`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1550)
##### [`clothing_item_extra_option`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1552)
##### [`replace_in_second_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1554)
##### [`replace_in_primary_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1556)
##### [`corpse_sickness_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1558)
##### [`hearing_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1560)
##### [`neck_protection_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1562)
##### [`visual_aid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1564)
##### [`vision_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1566)
##### [`attachments_provided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1568)
##### [`combat_speed_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1570)
##### [`bullet_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1572)
##### [`stomp_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1574)
##### [`tooltip`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1578)
##### [`custom_context_menu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1580)
##### [`clothing_extra_submenu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1582)
##### [`on_create`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1586)
##### [`on_break`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1588)
##### [`on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1590)
##### [`on_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1592)
##### [`on_create`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1596)
##### [`on_break`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1598)
##### [`on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1600)
##### [`on_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1602)
##### [`accept_media_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1604)
##### [`media_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1606)
##### [`base_volume_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1608)
##### [`is_high_tier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1610)
##### [`is_portable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1612)
##### [`is_television`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1614)
##### [`max_channel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1616)
##### [`mic_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1618)
##### [`min_channel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1620)
##### [`no_transmit`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1622)
##### [`transmit_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1624)
##### [`two_way`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1626)
##### [`uses_battery`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1628)
##### [`require_in_hand_or_inventory`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1630)
##### [`activated_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1632)
##### [`light_distance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1634)
##### [`light_strength`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1636)
##### [`torch_cone`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1638)
##### [`torch_dot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1640)
##### [`vehicle_part_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1644)
##### [`brake_force`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1646)
##### [`engine_loudness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1648)
##### [`condition_lower_standard`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1650)
##### [`condition_lower_offroad`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1652)
##### [`suspension_damping`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1654)
##### [`suspension_compression`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1656)
##### [`wheel_friction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1658)
##### [`vehicle_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1660)
##### [`max_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1662)
##### [`mechanics_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1664)
##### [`condition_affects_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1666)
##### [`can_be_write`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1670)
##### [`page_to_write`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1672)
##### [`map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1674)
##### [`lvl_skill_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1676)
##### [`num_levels_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1678)
##### [`number_of_pages`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1680)
##### [`skill_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1682)
##### [`is_dung`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1690)
##### [`survival_gear`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1692)
##### [`fishing_lure`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1694)
##### [`trap`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1696)
##### [`padlock`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1698)
##### [`digital_padlock`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1700)
##### [`can_store_water`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1702)
##### [`is_water_source`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1704)
##### [`wet`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1706)
##### [`cosmetic`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1708)
##### [`fire_fuel_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1712)
##### [`rain_factor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1714)
##### [`wet_cooldown`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1716)
##### [`origin_x`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1718)
##### [`origin_y`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1720)
##### [`origin_z`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1722)
##### [`item_when_dry`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1724)
##### [`spawn_with`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1726)
##### [`make_up_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1728)
##### [`shout_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1730)
##### [`shout_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1732)
##### [`components`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1737)

Returns a list of component keys defined for the item.

##### [`fluid_container`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1742)

Returns the item's FluidContainer component.

##### [`durability`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1749)

Returns the item's Durability component.

##### [`skill`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1759)

Returns the primary skill associated with the item, if any.

##### [`weight_full`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1768)

Returns the item's total weight when full, whether with fluids or items.

Rounded to 2 decimal places, returns an int if no remainder.

##### [`burn_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1788)

Returns the burn time the item provides.

##### [`should_burn`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1797)

Returns True if the item is expected to burn.

Based on game logic from `ISCampingMenu.shouldBurn()`.

##### [`is_tinder`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1814)

Returns whether the item is valid tinder.

Based on game logic from `ISCampingMenu.isValidTinder()`.
Returns None if the item shouldn't burn.

##### [`models`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1842)

Returns a list of model texture filenames for this item.

Finds the correct model names based on clothing textures or static model values, and formats them as `<Name>_Model.png`.

##### [`skill_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1908)

XP multiplier based on the skill book and training level.

Returns 1 if no skill book is set.



[Previous Folder](../lists/body_locations_list.md) | [Previous File](fluid.md) | [Next File](skill.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
