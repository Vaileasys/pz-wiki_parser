[Previous Folder](../lists/body_locations_list.md) | [Previous File](fluid.md) | [Next File](vehicle.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# item.py

This module provides the Item class, which represents individual game items 
parsed from the script files. It includes logic for accessing 
item properties, managing defaults, resolving translations, determining icons, 
and calculating derived details like burn time or weight.

Main components:
- Item data access and caching
- Property wrappers with fallback defaults
- Icon resolution and wiki formatting
- Burn time calculation
- Inferred and component-based properties

## Classes

### `Item`

Represents an item, providing access to its properties, components, 

icons, translations, and behaviours.
This class handles:
- Retrieving script properties and defaults.
- Managing cached item data and instances.
- Calculating derived properties like burn time or full weight.
- Providing wiki integration helpers (e.g., icon formatting, page links).
- Supporting item components such as FluidContainer and Durability.
Acts as the primary interface for item-related data across the parsing system.

#### Class Methods
##### [`_load_items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L373)

Load item data only once and store in class-level cache.

##### [`fix_item_id(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L378)

Attempts to fix a partial item_id by assuming the 'Base' module first,

then falling back to a full search through parsed item data.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _Either a full item_id ('Module.Item') or just an item name._

<ins>**Returns:**</ins>
  - **str:**
      - The best-guess full item_id.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L408)

Return all items as a dictionary of {item_id: Item}.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L415)

Return all item IDs as a keys view.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L422)

Return all Item instances as a generator.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L429)

Return the total number of loaded items.

##### [`get_icon_cache()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L436)

Return the cached list of item icon filenames.

##### [`load_burn_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L444)

Load and cache burn time data from camping_fuel.lua.

#### Object Methods
##### [`__new__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L315)

Return an existing Item instance if one already exists for the given ID.

Fixes partial IDs like 'Axe' to 'Base.Axe' before checking or creating the instance.

##### [`__init__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L333)

Initialise the Item instance with its data if not already initialised.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L356)

Allow dictionary-style access to item data (e.g., item["DisplayName"]).

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L360)

Allow 'in' checks for item data keys (e.g., "EvolvedRecipe" in item).

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L364)

Return a string representation of the Item showing name, ID, type, and source path.

##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L466)

Retrieve the value for a given key from item data.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
  - **default (any, optional)**:
      - _Fallback if the key is missing._

<ins>**Returns:**</ins>
  - **any:**
      - The value from data or the provided default.

##### [`get_default(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L481)

Retrieve the value for a key using the class default if no explicit default is provided.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
  - **default (any, optional)**:
      - _Explicit fallback (overrides class default if provided)._

<ins>**Returns:**</ins>
  - **any:**
      - The value from data or the determined default.

##### [`get_component(key: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L495)

Retrieve a sprecific component dict from the item data.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The component key to look up._

<ins>**Returns:**</ins>
  - **dict:**
      - The subcomponent data or an empty dict if missing.

##### [`has_tag(tag: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L507)

Check if the item has a specific tag.


<ins>**Args:**</ins>
  - **tag (str)**:
      - _The tag name to check._

<ins>**Returns:**</ins>
  - **bool:**
      - True if the tag is present, False otherwise.

##### [`find_name(language: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L521)

Determines the display name of the item, handling special cases and translations.


<ins>**Args:**</ins>
  - **language (str, optional)**:
      - _Language code (e.g., 'en'). If None, uses the active language._

<ins>**Returns:**</ins>
  - **str:**
      - The resolved item name, including special case titles, vehicle part names, or translated display names.

##### [`get_icon(format: bool, all_icons: bool, cycling: bool, custom_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L593)

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

##### [`_find_icon()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L620)

Detects and sets the item's icon(s), checking CSV overrides, item properties, and icon variants.

##### [`_format_icon(format: bool, all_icons: bool, cycling: bool, custom_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L706)

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

##### [`calculate_burn_time()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L754)

Calculate and store the burn time for this item based on weight, category, tags, and fuel data.

#### Properties
##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L832)
##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L836)
##### [`item_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L840)
##### [`module`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L844)
##### [`id_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L848)
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L852)
##### [`has_page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L864)
##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L870)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L874)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L880)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L886)
##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L892)
##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L899)
##### [`display_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L901)
##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L910)
##### [`always_welcome_gift`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L912)
##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L914)
##### [`raw_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L918)
##### [`icons_for_texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L920)
##### [`static_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L922)
##### [`world_static_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L924)
##### [`physics_object`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L926)
##### [`placed_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L928)
##### [`weapon_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L930)
##### [`eat_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L932)
##### [`swing_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L934)
##### [`idle_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L936)
##### [`run_anim`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L938)
##### [`static_models_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L940)
##### [`world_static_models_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L942)
##### [`primary_anim_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L944)
##### [`secondary_anim_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L946)
##### [`world_object_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L948)
##### [`read_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L950)
##### [`scale_world_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L952)
##### [`use_world_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L954)
##### [`weapon_sprites_by_index`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L956)
##### [`color_blue`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L958)
##### [`color_green`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L960)
##### [`color_red`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L962)
##### [`icon_color_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L964)
##### [`icon_fluid_mask`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L966)
##### [`dig_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L968)
##### [`pour_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L970)
##### [`place_multiple_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L974)
##### [`place_one_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L976)
##### [`cooking_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L978)
##### [`swing_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L980)
##### [`close_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L982)
##### [`open_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L984)
##### [`put_in_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L986)
##### [`break_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L988)
##### [`door_hit_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L990)
##### [`drop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L992)
##### [`hit_floor_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L994)
##### [`hit_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L996)
##### [`aim_release_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L998)
##### [`bring_to_bear_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1000)
##### [`click_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1002)
##### [`eject_ammo_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1004)
##### [`eject_ammo_start_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1006)
##### [`eject_ammo_stop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1008)
##### [`equip_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1010)
##### [`custom_eat_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1012)
##### [`impact_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1014)
##### [`insert_ammo_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1016)
##### [`insert_ammo_start_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1018)
##### [`insert_ammo_stop_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1020)
##### [`damaged_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1022)
##### [`unequip_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1024)
##### [`rack_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1026)
##### [`npc_sound_boost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1028)
##### [`sound_parameter`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1030)
##### [`sound_map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1032)
##### [`fill_from_dispenser_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1034)
##### [`fill_from_lake_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1036)
##### [`fill_from_tap_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1038)
##### [`fill_from_toilet_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1040)
##### [`weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1044)
##### [`capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1046)
##### [`weight_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1048)
##### [`accept_item_function`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1050)
##### [`weight_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1052)
##### [`weapon_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1054)
##### [`max_item_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1056)
##### [`weight_empty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1058)
##### [`evolved_recipe`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1062)
##### [`researchable_recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1064)
##### [`teached_recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1066)
##### [`sharpness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1068)
##### [`head_condition`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1070)
##### [`head_condition_lower_chance_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1072)
##### [`condition_lower_chance_one_in`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1074)
##### [`evolved_recipe_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1076)
##### [`can_attach`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1078)
##### [`can_detach`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1080)
##### [`condition_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1082)
##### [`replace_on_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1084)
##### [`replace_on_use_on`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1086)
##### [`consolidate_option`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1088)
##### [`use_delta`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1090)
##### [`use_while_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1092)
##### [`use_self`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1094)
##### [`replace_on_deplete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1096)
##### [`remove_on_broken`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1098)
##### [`without_drainable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1100)
##### [`with_drainable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1102)
##### [`ticks_per_equip_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1104)
##### [`can_be_reused`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1106)
##### [`head_condition_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1108)
##### [`disappear_on_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1110)
##### [`cant_be_consolided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1112)
##### [`use_while_unequipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1114)
##### [`equipped_no_sprint`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1116)
##### [`protect_from_rain_when_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1118)
##### [`replace_on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1120)
##### [`item_after_cleaning`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1122)
##### [`can_barricade`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1124)
##### [`keep_on_deplete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1126)
##### [`chance_to_spawn_damaged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1128)
##### [`metal_value`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1130)
##### [`food_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1134)
##### [`days_fresh`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1136)
##### [`days_totally_rotten`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1138)
##### [`hunger_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1140)
##### [`thirst_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1142)
##### [`calories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1144)
##### [`carbohydrates`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1146)
##### [`lipids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1148)
##### [`proteins`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1150)
##### [`is_cookable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1152)
##### [`minutes_to_cook`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1154)
##### [`minutes_to_burn`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1156)
##### [`remove_unhappiness_when_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1158)
##### [`bad_cold`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1160)
##### [`bad_in_microwave`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1162)
##### [`dangerous_uncooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1164)
##### [`good_hot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1166)
##### [`cant_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1168)
##### [`cant_be_frozen`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1170)
##### [`animal_feed_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1172)
##### [`packaged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1174)
##### [`spice`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1176)
##### [`canned_food`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1178)
##### [`replace_on_rotten`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1180)
##### [`eat_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1182)
##### [`remove_negative_effect_on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1184)
##### [`unhappy_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1188)
##### [`boredom_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1190)
##### [`stress_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1192)
##### [`reduce_food_sickness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1194)
##### [`endurance_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1196)
##### [`poison_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1198)
##### [`medical`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1200)
##### [`alcoholic`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1202)
##### [`bandage_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1204)
##### [`can_bandage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1206)
##### [`alcohol_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1208)
##### [`reduce_infection_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1210)
##### [`fatigue_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1212)
##### [`flu_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1214)
##### [`herbalist_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1216)
##### [`pain_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1218)
##### [`explosion_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1222)
##### [`explosion_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1224)
##### [`explosion_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1226)
##### [`knockdown_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1228)
##### [`max_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1230)
##### [`max_hit_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1232)
##### [`max_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1234)
##### [`min_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1236)
##### [`minimum_swing_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1238)
##### [`swing_amount_before_impact`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1240)
##### [`swing_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1242)
##### [`trigger_explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1244)
##### [`can_be_placed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1246)
##### [`can_be_remote`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1248)
##### [`explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1250)
##### [`sensor_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1252)
##### [`alarm_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1254)
##### [`sound_radius`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1256)
##### [`reload_time_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1258)
##### [`mount_on`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1260)
##### [`part_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1262)
##### [`attachment_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1264)
##### [`base_speed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1266)
##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1268)
##### [`crit_dmg_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1270)
##### [`critical_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1272)
##### [`door_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1274)
##### [`knock_back_on_no_death`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1276)
##### [`min_angle`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1278)
##### [`min_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1280)
##### [`push_back_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1282)
##### [`splat_blood_on_no_death`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1284)
##### [`splat_number`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1286)
##### [`sub_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1288)
##### [`tree_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1290)
##### [`weapon_length`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1292)
##### [`projectile_spread_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1294)
##### [`max_range_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1296)
##### [`angle_falloff`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1298)
##### [`have_chamber`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1300)
##### [`insert_all_bullets_reload`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1302)
##### [`projectile_spread`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1304)
##### [`projectile_weight_center`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1306)
##### [`rack_after_shoot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1308)
##### [`range_falloff`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1310)
##### [`other_hand_use`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1312)
##### [`other_hand_require`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1314)
##### [`fire_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1316)
##### [`fire_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1318)
##### [`noise_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1320)
##### [`aiming_time_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1322)
##### [`hit_chance_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1324)
##### [`noise_duration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1326)
##### [`recoil_delay_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1328)
##### [`remote_controller`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1330)
##### [`remote_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1332)
##### [`manually_remove_spent_rounds`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1334)
##### [`explosion_duration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1336)
##### [`smoke_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1338)
##### [`trigger_explosion_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1340)
##### [`count_`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1342)
##### [`ammo_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1344)
##### [`can_stack`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1346)
##### [`gun_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1348)
##### [`max_ammo`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1350)
##### [`aiming_perk_crit_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1352)
##### [`aiming_perk_hit_chance_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1354)
##### [`aiming_perk_min_angle_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1356)
##### [`aiming_perk_range_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1358)
##### [`aiming_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1360)
##### [`ammo_box`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1362)
##### [`fire_mode`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1364)
##### [`fire_mode_possibilities`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1366)
##### [`cyclic_rate_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1368)
##### [`hit_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1370)
##### [`is_aimed_firearm`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1372)
##### [`jam_gun_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1374)
##### [`magazine_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1376)
##### [`min_sight_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1378)
##### [`max_sight_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1380)
##### [`model_weapon_part`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1382)
##### [`multiple_hit_condition_affected`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1384)
##### [`piercing_bullets`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1386)
##### [`projectile_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1388)
##### [`ranged`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1390)
##### [`recoil_delay`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1392)
##### [`reload_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1394)
##### [`requires_equipped_both_hands`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1396)
##### [`share_damage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1398)
##### [`shell_fall_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1400)
##### [`sound_gain`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1402)
##### [`sound_volume`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1404)
##### [`splat_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1406)
##### [`stop_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1408)
##### [`to_hit_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1410)
##### [`two_hand_weapon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1412)
##### [`use_endurance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1414)
##### [`weapon_reload_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1416)
##### [`clip_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1418)
##### [`damage_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1420)
##### [`damage_make_hole`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1422)
##### [`hit_angle_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1424)
##### [`endurance_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1426)
##### [`low_light_bonus`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1428)
##### [`always_knockdown`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1430)
##### [`crit_dmg_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1432)
##### [`aiming_mod`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1434)
##### [`is_aimed_hand_weapon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1436)
##### [`cant_attack_with_lowest_endurance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1438)
##### [`close_kill_move`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1440)
##### [`body_location`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1444)
##### [`clothing_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1446)
##### [`can_be_equipped`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1448)
##### [`run_speed_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1450)
##### [`blood_location`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1452)
##### [`can_have_holes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1454)
##### [`chance_to_fall`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1456)
##### [`insulation`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1458)
##### [`wind_resistance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1460)
##### [`fabric_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1462)
##### [`scratch_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1464)
##### [`discomfort_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1466)
##### [`water_resistance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1468)
##### [`bite_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1470)
##### [`attachment_replacement`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1472)
##### [`clothing_item_extra`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1474)
##### [`clothing_item_extra_option`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1476)
##### [`replace_in_second_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1478)
##### [`replace_in_primary_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1480)
##### [`corpse_sickness_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1482)
##### [`hearing_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1484)
##### [`neck_protection_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1486)
##### [`visual_aid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1488)
##### [`vision_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1490)
##### [`attachments_provided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1492)
##### [`combat_speed_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1494)
##### [`bullet_defense`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1496)
##### [`stomp_power`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1498)
##### [`tooltip`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1502)
##### [`custom_context_menu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1504)
##### [`clothing_extra_submenu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1506)
##### [`on_create`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1510)
##### [`on_break`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1512)
##### [`on_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1514)
##### [`on_eat`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1516)
##### [`accept_media_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1520)
##### [`media_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1522)
##### [`base_volume_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1524)
##### [`is_high_tier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1526)
##### [`is_portable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1528)
##### [`is_television`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1530)
##### [`max_channel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1532)
##### [`mic_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1534)
##### [`min_channel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1536)
##### [`no_transmit`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1538)
##### [`transmit_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1540)
##### [`two_way`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1542)
##### [`uses_battery`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1544)
##### [`require_in_hand_or_inventory`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1546)
##### [`activated_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1548)
##### [`light_distance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1550)
##### [`light_strength`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1552)
##### [`torch_cone`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1554)
##### [`torch_dot`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1556)
##### [`vehicle_part_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1560)
##### [`brake_force`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1562)
##### [`engine_loudness`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1564)
##### [`condition_lower_standard`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1566)
##### [`condition_lower_offroad`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1568)
##### [`suspension_damping`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1570)
##### [`suspension_compression`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1572)
##### [`wheel_friction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1574)
##### [`vehicle_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1576)
##### [`max_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1578)
##### [`mechanics_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1580)
##### [`condition_affects_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1582)
##### [`can_be_write`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1586)
##### [`page_to_write`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1588)
##### [`map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1590)
##### [`lvl_skill_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1592)
##### [`num_levels_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1594)
##### [`number_of_pages`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1596)
##### [`skill_trained`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1598)
##### [`is_dung`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1602)
##### [`survival_gear`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1604)
##### [`fishing_lure`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1606)
##### [`trap`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1608)
##### [`padlock`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1610)
##### [`digital_padlock`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1612)
##### [`can_store_water`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1614)
##### [`is_water_source`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1616)
##### [`wet`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1618)
##### [`cosmetic`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1620)
##### [`fire_fuel_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1624)
##### [`rain_factor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1626)
##### [`wet_cooldown`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1628)
##### [`origin_x`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1630)
##### [`origin_y`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1632)
##### [`origin_z`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1634)
##### [`item_when_dry`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1636)
##### [`spawn_with`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1638)
##### [`make_up_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1640)
##### [`shout_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1642)
##### [`shout_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1644)
##### [`components`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1649)
##### [`fluid_container`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1653)
##### [`durability`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1659)
##### [`weight_full`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1667)
##### [`burn_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1683)
##### [`should_burn`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1689)

Checks if an item 'should burn', not that it 'can burn'.

##### [`is_tinder`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/item.py#L1703)


[Previous Folder](../lists/body_locations_list.md) | [Previous File](fluid.md) | [Next File](vehicle.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
