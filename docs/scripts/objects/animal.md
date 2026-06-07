[Previous Folder](../navbox/navbox.md) | [Next File](animal_gene.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# animal.py

## Functions

### [`animal_report(animal_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1163)

## Classes

### `Animal`

Represents a single animal entry.

#### Class Methods

##### [`_parse()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L58)

Parses Animal data from the provided Lua file and caches it.

##### [`_parse_avatar()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L110)

Parse animal avatar data.

##### [`load(attribute: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L132)

Loads Animal data from the cache, re-parsing the Lua file if the data is outdated.

<ins>**Returns:**</ins>
  - **dict**:
      - _Raw Animal data._

##### [`load_avatar()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L163)

##### [`all() -> dict[str, 'Animal']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L179)

Returns all known Animal instances.

<ins>**Returns:**</ins>
  - **dict[str, Animal]**:
      - _Mapping of item ID to Animal instance._

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L191)

Returns the total number of Animal types parsed.

<ins>**Returns:**</ins>
  - **int**:
      - _Number of unique Animal types._

##### [`exists(animal_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L203)

Checks if a Animal with the given id exists in the parsed data.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if found, False otherwise._

#### Object Methods

##### [`__new__(animal_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L29)

Ensures only one Animal instance exists per animal ID.

##### [`__init__(animal_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L42)

Initialise the Animal instance with its data if not already initialised.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L214)

Returns a raw value from the animal data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Key to look up._
  - **default**:
      - _Value to return if key is missing._

<ins>**Returns:**</ins>
  - **Any**:
      - _Value from the raw data or default._

##### [`get_avatar(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L227)

Returns a raw value from the animal avatar data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Key to look up._
  - **default**:
      - _Value to return if key is missing._

<ins>**Returns:**</ins>
  - **Any**:
      - _Value from the raw data or default._

##### [`_translate_month(month: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L240)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L746)

#### Properties

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L245)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L249)

##### [`avatar_data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L253)

##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L257)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L262)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L266)

##### [`corpse_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L270)

##### [`corpse_name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L274)

##### [`skeleton_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L278)

##### [`skeleton_name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L282)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L286)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L290)

##### [`group`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L295)

##### [`group_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L297)

##### [`group_name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L300)

##### [`group_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L302)

##### [`base_encumbrance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L304)

##### [`trailer_base_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L306)

##### [`carcass_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L308)

##### [`min_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L318)

##### [`max_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L320)

##### [`min_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L322)

##### [`max_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L324)

##### [`animal_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L326)

##### [`corpse_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L328)

##### [`collision_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L330)

##### [`texture_skeleton_bloody`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L332)

##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L334)

##### [`icon_all`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L343)

##### [`icon_dead`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L349)

##### [`icon_dead_all`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L358)

##### [`icon_skeleton`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L364)

##### [`icon_skeleton_all`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L373)

##### [`model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L379)

##### [`model_all`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L390)

##### [`hunger_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L401)

##### [`thirst_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L403)

##### [`hunger_boost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L405)

##### [`thirst_boost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L407)

##### [`health_loss_multiplier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L409)

##### [`max_blood`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L411)

##### [`min_blood`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L413)

##### [`min_body_part`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L415)

##### [`daily_water`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L417)

##### [`daily_hunger`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L431)

##### [`can_be_pet`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L444)

##### [`can_thump`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L446)

##### [`can_be_picked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L448)

##### [`always_flee_humans`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L450)

##### [`flee_zombies`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L452)

##### [`stress_under_rain`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L454)

##### [`stress_above_ground`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L456)

##### [`can_climb_fences`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L458)

##### [`sit_randomly`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L460)

##### [`dont_attack_other_male`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L462)

##### [`can_be_fed_by_hand`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L464)

##### [`feed_by_hand_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L466)

##### [`knockdown_attack`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L472)

##### [`eat_grass`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L474)

##### [`can_do_laceration`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L476)

##### [`can_be_attached`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L478)

##### [`can_be_transported`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L480)

##### [`attack_dist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L482)

##### [`attack_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L484)

##### [`attack_if_stressed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L486)

##### [`attack_back`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L488)

##### [`base_dmg`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L490)

##### [`thirst_hunger_trigger`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L492)

##### [`enter_hutch_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L494)

##### [`exit_hutch_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L496)

##### [`idle_type_nbr`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L498)

##### [`eating_type_nbr`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L500)

##### [`sitting_type_nbr`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L502)

##### [`periodic_run`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L504)

##### [`male`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L506)

##### [`female`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L508)

##### [`baby`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L510)

##### [`gender`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L512)

##### [`udder`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L517)

##### [`wild`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L519)

##### [`eat_from_mother`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L521)

##### [`need_mom`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L523)

##### [`can_climb_stairs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L525)

##### [`add_tracking_xp`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L527)

##### [`wild_flee_time_until_dead_timer`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L529)

##### [`spotting_dist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L531)

##### [`can_be_alerted`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L533)

##### [`can_be_domesticated`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L535)

##### [`litter_eat_together`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L537)

##### [`genes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L541)

##### [`stages`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L544)

##### [`stage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L547)

##### [`breeds`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L550)

##### [`mating_period_start`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L559)

##### [`mating_period_month_start`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L561)

##### [`mating_period_end`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L563)

##### [`mating_period_month_end`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L565)

##### [`min_age`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L567)

##### [`max_age`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L570)

##### [`min_age_for_baby`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L573)

##### [`baby_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L575)

##### [`mate`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L577)

##### [`baby_nbr`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L579)

##### [`pregnant_period`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L581)

##### [`time_before_next_pregnancy`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L583)

##### [`can_be_milked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L585)

##### [`min_milk`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L587)

##### [`max_milk`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L589)

##### [`min_baby`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L591)

##### [`max_baby`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L593)

##### [`eggs_per_day`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L595)

##### [`egg_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L597)

##### [`fertilized_time_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L601)

##### [`time_to_hatch`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L604)

##### [`model_script`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L608)

##### [`anim_set`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L610)

##### [`texture_skinned`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L612)

##### [`texture_skeleton`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L614)

##### [`texture_skeleton_bloody`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L616)

##### [`body_model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L618)

##### [`body_model_skel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L620)

##### [`body_model_skel_no_head`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L622)

##### [`body_model_headless`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L624)

##### [`rope_bone`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L626)

##### [`shadow_w`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L628)

##### [`shadow_fm`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L630)

##### [`shadow_bm`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L632)

##### [`idle_emote_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L634)

##### [`sounds`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L638)

##### [`idle_sound_radius`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L640)

##### [`idle_sound_volume`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L642)

##### [`dung`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L646)

##### [`dung_chance_per_day`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L656)

##### [`min_enclosure_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L658)

##### [`eat_type_trough`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L660)

##### [`hutches`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L666)

##### [`food_types`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L673)

##### [`lured_possible_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L717)

##### [`wander_mul`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L723)

##### [`max_wool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L725)

##### [`min_clutch_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L727)

##### [`max_clutch_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L729)

##### [`lay_egg_period_start`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L731)

##### [`lay_egg_period_month_start`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L733)

##### [`ranch_zones`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L736)

##### [`can_be_hooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L742)

### `AnimalBreed`

#### Class Methods

##### [`exists(animal_id: str, breed_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L817)

Checks if a animal breed with the given ids exists in the parsed data.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if found, False otherwise._

##### [`build_full_breed_ids()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L833)

##### [`get_full_breed_ids() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L840)

##### [`key_exists(full_breed_id) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L846)

##### [`from_key(full_breed_id) -> 'AnimalBreed'`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L850)

##### [`all() -> 'dict[str, AnimalBreed]'`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L863)

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L867)

#### Static Methods

##### [`fix_texture(texture: str | list) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L780)

Checks for an existing case-incensitive texture in the game files, and corrects the casing.

#### Object Methods

##### [`__new__(animal_id: str, breed_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L755)

Ensures only one instance exists per animal breed.

##### [`__init__(animal_id: str, breed_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L766)

Initialise the breed instance with its data if not already initialised.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L870)

Returns a raw value from the animal breed data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Key to look up._
  - **default**:
      - _Value to return if key is missing._

<ins>**Returns:**</ins>
  - **Any**:
      - _Value from the raw data or default._

##### [`format_icon(image: str, page: str, name: str, default: str = None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L883)

##### [`format_models(image: list[str] | str, page: str, name: str, default: str = None) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L888)

##### [`get_name(stage: str = None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L901)

##### [`get_link(stage: str = None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L909)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1159)

#### Properties

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L914)

##### [`animal`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L918)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L922)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L926)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L930)

##### [`breed_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L934)

##### [`breed_name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L938)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L942)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L946)

##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L950)

##### [`icons`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L954)

##### [`icon_file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L960)

##### [`icon_files`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L969)

##### [`icon_dead`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L975)

##### [`icon_dead_file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L979)

##### [`icon_skeleton`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L988)

##### [`icon_skeleton_file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L992)

##### [`inv_icon_male`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1001)

##### [`inv_icon_female`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1003)

##### [`inv_icon_baby`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1005)

##### [`inv_icon_male_dead`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1007)

##### [`inv_icon_female_dead`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1009)

##### [`inv_icon_baby_dead`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1011)

##### [`inv_icon_male_skel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1013)

##### [`inv_icon_female_skel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1015)

##### [`inv_icon_baby_skel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1017)

##### [`texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1020)

##### [`texture_male`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1022)

##### [`texture_baby`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1024)

##### [`rotten_texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1026)

##### [`models`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1029)

##### [`model_files`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1033)

##### [`parts_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1055)

##### [`parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1058)

##### [`milk_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1062)

##### [`wool_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1066)

##### [`feather_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1070)

##### [`max_feather`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1074)

##### [`actual_min_milk_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1078)

Lowest possible udder capacity (breed.minMilk × gene.min).

##### [`actual_min_milk_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1082)

Highest possible minimum udder capacity (breed.minMilk × gene.max)

##### [`actual_max_milk_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1086)

Lowest possible maximum udder capacity (breed.maxMilk × gene.min)

##### [`actual_max_milk_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1090)

Highest possible udder capacity (breed.maxMilk × gene.max)

##### [`actual_max_wool_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1095)

Lowest possible wool capacity (breed.maxWool × gene.min)

##### [`actual_max_wool_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1099)

Highest possible wool capacity (breed.maxWool × gene.max)

##### [`forced_genes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1108)

##### [`min_milk`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1111)

##### [`max_milk`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1117)

##### [`milk_inc`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1123)

##### [`meat_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1129)

##### [`min_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1135)

##### [`max_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1141)

##### [`max_wool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1147)

##### [`wool_inc`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal.py#L1153)


[Previous Folder](../navbox/navbox.md) | [Next File](animal_gene.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
