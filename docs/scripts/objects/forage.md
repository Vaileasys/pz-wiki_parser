[Previous Folder](../lists/attachment_list.md) | [Previous File](fluid.md) | [Next File](item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# forage.py

## Classes

### `ForagingItem`
#### Class Methods
##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L32)

Loads the foraging data from cache, otherwise parses it with the distribution parser.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L46)

Return all foraging instances as a dictionary of {foraging_id: Item}.

##### [`items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L51)

Return an iterable of (id, instance) pairs.

##### [`exists(foraging_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L56)

Returns True if the foraging ID exists in the foraging data.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L61)

Returns the number of foraging entries loaded.

#### Object Methods
##### [`__new__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L22)
##### [`__init__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L27)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L65)

Returns the raw value from this item's foraging data.

##### [`_translate_month(month: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L69)
##### [`_get_month_links(months)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L135)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L242)
#### Properties
##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L74)
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L78)
##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L82)
##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L86)
##### [`skill`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L90)
##### [`xp`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L94)
##### [`perks`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L98)
##### [`zones`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L102)
##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L117)
##### [`min_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L124)
##### [`max_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L128)
##### [`spawn_funcs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L132)
##### [`months_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L155)
##### [`months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L163)
##### [`bonus_months_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L167)
##### [`bonus_months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L175)
##### [`malus_months_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L179)
##### [`malus_months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L187)
##### [`day_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L191)
##### [`night_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L195)
##### [`snow_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L199)
##### [`rain_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L203)
##### [`item_size_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L207)
##### [`is_item_override_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L211)
##### [`force_outside`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L215)
##### [`can_be_above_floor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L219)
##### [`poison_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L223)
##### [`poison_power_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L227)
##### [`poison_power_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L231)
##### [`poison_detection_level`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L235)
##### [`alt_world_texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L239)

### `ForageCategory`
#### Class Methods
##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L260)
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L266)

Return all foraging categories as a dictionary of {category_id: ForageCategory}.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L271)

Returns the number of foraging categories loaded.

##### [`exists(category: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L276)
#### Object Methods
##### [`__new__(category: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L250)
##### [`__init__(category: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L255)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L279)

Returns the raw value from this category's data.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L398)
#### Properties
##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L284)
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L288)
##### [`type_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L292)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L296)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L300)
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L306)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L312)
##### [`icon_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L318)
##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L322)
##### [`is_hidden`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L326)
##### [`identify_perk`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L330)
##### [`identify_level`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L334)
##### [`zones`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L338)
##### [`traits`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L342)
##### [`occupations`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L346)
##### [`sprite_affinity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L350)
##### [`focus_chance_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L354)
##### [`focus_chance_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L358)
##### [`valid_floors`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L362)
##### [`chance_to_create_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L366)
##### [`chance_to_move_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L370)
##### [`has_rained_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L374)
##### [`rain_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L378)
##### [`snow_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L382)
##### [`night_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L386)
##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L390)

Returns all ForagingItem instances assigned to this category.


### `ForageZone`
#### Class Methods
##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L416)
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L422)

Return all foraging zones as a dictionary of {zone_id: ForageZone}.

##### [`exists(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L427)
#### Object Methods
##### [`__new__(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L406)
##### [`__init__(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L411)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L430)

Returns the raw value from this zone's data.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L473)
#### Properties
##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L435)
##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L439)
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L443)
##### [`contains_biomes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L447)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L454)
##### [`density_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L458)
##### [`density_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L462)
##### [`refill_percent`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L466)
##### [`abundance_setting`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L470)

### `ForageSkill`
#### Class Methods
##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L492)
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L498)

Return all foraging skills as a dictionary of {skill_id: ForageSkill}.

##### [`exists(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L503)
##### [`_build_category_map()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L507)
##### [`get_traits(category_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L521)
##### [`get_occupations(category_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L529)
#### Object Methods
##### [`__new__(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L482)
##### [`__init__(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L487)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L536)

Returns the raw value from this skill's data.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L593)
#### Properties
##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L541)
##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L545)
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L549)
##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L553)
##### [`object`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L557)

Returns the Trait or Occupation object associated with this skill.

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L566)
##### [`weather_effect`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L572)
##### [`darkness_effect`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L576)
##### [`specialisations`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L580)
##### [`vision_bonus`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L590)

### `ForageSystem`
#### Class Methods
##### [`_parse_forage_system()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L601)
##### [`_parse_forage_categories()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L616)
##### [`_parse_zones()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L640)
##### [`_parse_skills()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L654)
##### [`_parse()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L668)
##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L694)
##### [`get(value, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L710)

Returns a value from the foraging data, or a default if not found.

##### [`get_categories()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L715)

Returns all foraging category definitions.

##### [`get_zones()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L720)

Returns all forage zone definitions (e.g., Forest, DeepForest).

##### [`get_skills()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L725)

Returns all forage skill definitions (e.g., PlantScavenging, Trapping).

##### [`get_sprite_affinities()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L730)

Returns sprite affinity groupings (e.g., genericPlants → list of tile names).

##### [`get_seed_table()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L735)

Returns seed drop info (item → { type, amount, chance }).

##### [`get_world_sprites()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L740)

Returns grouped world sprite names for placement (e.g., bushes, wildPlants).

##### [`get_abundance_settings()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L745)

Returns abundance modifiers for game difficulty presets.

##### [`get_clothing_penalties()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L750)

Returns vision penalties caused by clothing on specific body locations.

##### [`get_zone_density_multi()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L755)
##### [`get_aim_multiplier()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L759)
##### [`get_max_icons_per_zone()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L763)
##### [`get_min_vision_radius()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L767)
##### [`get_max_vision_radius()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L771)
##### [`get_vision_radius_cap()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L775)
##### [`get_dark_vision_radius()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L779)
##### [`get_fatigue_penalty()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L783)
##### [`get_exhaustion_penalty_max()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L787)
##### [`get_panic_penalty_max()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L791)
##### [`get_light_penalty_max()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L795)
##### [`get_clothing_penalty_max()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L799)
##### [`get_effect_reduction_max()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L803)
##### [`get_hunger_bonus_max()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L807)
##### [`get_body_penalty_max()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L811)
##### [`get_endurance_penalty()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L815)
##### [`get_sneak_multiplier()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L819)
##### [`get_level_xp_modifier()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L823)
##### [`get_global_xp_modifier()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L827)
##### [`get_level_bonus()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L831)
##### [`get_month_malus()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L835)
##### [`get_month_bonus()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L839)
##### [`get_light_penalty_cutoff()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L843)


[Previous Folder](../lists/attachment_list.md) | [Previous File](fluid.md) | [Next File](item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
