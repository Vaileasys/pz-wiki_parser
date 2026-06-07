[Previous Folder](../navbox/navbox.md) | [Previous File](fluid.md) | [Next File](item.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# forage.py

## Classes

### `ForagingItem`

#### Class Methods

##### [`load() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L33)

Loads the foraging data from cache, otherwise parses it with the distribution parser.

##### [`all() -> dict[str, 'ForagingItem']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L48)

Return all foraging instances as a dictionary of {foraging_id: Item}.

##### [`items() -> dict[str, 'ForagingItem']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L53)

Return an iterable of (id, instance) pairs.

##### [`exists(foraging_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L58)

Returns True if the foraging ID exists in the foraging data.

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L63)

Returns the number of foraging entries loaded.

#### Object Methods

##### [`__new__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L23)

##### [`__init__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L28)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L67)

Returns the raw value from this item's foraging data.

##### [`_translate_month(month: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L71)

##### [`has_category(*category_ids: str | list[str]) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L75)

Check if the foraging item is in any of the given categories.

<ins>**Args:**</ins>
  - ***category_ids (str | list[str])**:
      - _One or more category IDs. Can be individual strings or lists of strings._

<ins>**Returns:**</ins>
  - **bool**:
      - _True if the item is in at least one of the categories._

##### [`_get_month_links(months)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L160)

##### [`__repr__() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L267)

#### Properties

##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L99)

##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L103)

##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L107)

##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L111)

##### [`skill`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L115)

##### [`xp`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L119)

##### [`perks`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L123)

##### [`zones`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L127)

##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L142)

##### [`min_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L149)

##### [`max_count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L153)

##### [`spawn_funcs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L157)

##### [`months_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L180)

##### [`months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L188)

##### [`bonus_months_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L192)

##### [`bonus_months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L200)

##### [`malus_months_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L204)

##### [`malus_months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L212)

##### [`day_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L216)

##### [`night_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L220)

##### [`snow_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L224)

##### [`rain_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L228)

##### [`item_size_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L232)

##### [`is_item_override_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L236)

##### [`force_outside`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L240)

##### [`can_be_above_floor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L244)

##### [`poison_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L248)

##### [`poison_power_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L252)

##### [`poison_power_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L256)

##### [`poison_detection_level`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L260)

##### [`alt_world_texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L264)

### `ForageCategory`

#### Class Methods

##### [`load() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L285)

##### [`all() -> dict[str, 'ForageCategory']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L291)

Return all foraging categories as a dictionary of {category_id: ForageCategory}.

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L296)

Returns the number of foraging categories loaded.

##### [`exists(category: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L301)

#### Object Methods

##### [`__new__(category: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L275)

##### [`__init__(category: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L280)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L304)

Returns the raw value from this category's data.

##### [`__repr__() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L423)

#### Properties

##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L309)

##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L313)

##### [`type_category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L317)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L321)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L325)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L331)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L337)

##### [`icon_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L343)

##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L347)

##### [`is_hidden`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L351)

##### [`identify_perk`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L355)

##### [`identify_level`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L359)

##### [`zones`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L363)

##### [`traits`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L367)

##### [`occupations`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L371)

##### [`sprite_affinity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L375)

##### [`focus_chance_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L379)

##### [`focus_chance_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L383)

##### [`valid_floors`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L387)

##### [`chance_to_create_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L391)

##### [`chance_to_move_icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L395)

##### [`has_rained_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L399)

##### [`rain_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L403)

##### [`snow_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L407)

##### [`night_chance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L411)

##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L415)

Returns all ForagingItem instances assigned to this category.

### `ForageZone`

#### Class Methods

##### [`load() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L441)

##### [`all() -> dict[str, 'ForageZone']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L447)

Return all foraging zones as a dictionary of {zone_id: ForageZone}.

##### [`exists(zone: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L452)

#### Object Methods

##### [`__new__(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L431)

##### [`__init__(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L436)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L455)

Returns the raw value from this zone's data.

##### [`__repr__() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L498)

#### Properties

##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L460)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L464)

##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L468)

##### [`contains_biomes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L472)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L479)

##### [`density_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L483)

##### [`density_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L487)

##### [`refill_percent`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L491)

##### [`abundance_setting`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L495)

### `ForageSkill`

#### Class Methods

##### [`load() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L517)

##### [`all() -> dict[str, 'ForageSkill']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L523)

Return all foraging skills as a dictionary of {skill_id: ForageSkill}.

##### [`exists(zone: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L528)

##### [`_build_category_map()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L532)

##### [`get_traits(category_id: str) -> list[Trait]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L546)

##### [`get_occupations(category_id: str) -> list[Occupation]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L554)

#### Object Methods

##### [`__new__(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L507)

##### [`__init__(zone: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L512)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L561)

Returns the raw value from this skill's data.

##### [`__repr__() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L618)

#### Properties

##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L566)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L570)

##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L574)

##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L578)

##### [`object`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L582)

Returns the Trait or Occupation object associated with this skill.

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L591)

##### [`weather_effect`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L597)

##### [`darkness_effect`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L601)

##### [`specialisations`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L605)

##### [`vision_bonus`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L615)

### `ForageSystem`

#### Class Methods

##### [`_parse_forage_system() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L626)

##### [`_parse_forage_categories()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L641)

##### [`_parse_zones() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L665)

##### [`_parse_skills() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L679)

##### [`_parse()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L707)

##### [`load() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L733)

##### [`get(value, default) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L749)

Returns a value from the foraging data, or a default if not found.

##### [`get_categories() -> dict[str, dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L754)

Returns all foraging category definitions.

##### [`get_zones() -> dict[str, dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L759)

Returns all forage zone definitions (e.g., Forest, DeepForest).

##### [`get_skills() -> dict[str, dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L764)

Returns all forage skill definitions (e.g., PlantScavenging, Trapping).

##### [`get_sprite_affinities() -> dict[str, list[str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L769)

Returns sprite affinity groupings (e.g., genericPlants → list of tile names).

##### [`get_seed_table() -> dict[str, dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L774)

Returns seed drop info (item → { type, amount, chance }).

##### [`get_world_sprites() -> dict[str, list[list[str]]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L779)

Returns grouped world sprite names for placement (e.g., bushes, wildPlants).

##### [`get_abundance_settings() -> dict[str, list[int]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L784)

Returns abundance modifiers for game difficulty presets.

##### [`get_clothing_penalties() -> dict[str, float | int]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L789)

Returns vision penalties caused by clothing on specific body locations.

##### [`get_zone_density_multi() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L794)

##### [`get_aim_multiplier() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L798)

##### [`get_max_icons_per_zone() -> int | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L802)

##### [`get_min_vision_radius() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L806)

##### [`get_max_vision_radius() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L810)

##### [`get_vision_radius_cap() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L814)

##### [`get_dark_vision_radius() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L818)

##### [`get_fatigue_penalty() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L822)

##### [`get_exhaustion_penalty_max() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L826)

##### [`get_panic_penalty_max() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L830)

##### [`get_light_penalty_max() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L834)

##### [`get_clothing_penalty_max() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L838)

##### [`get_effect_reduction_max() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L842)

##### [`get_hunger_bonus_max() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L846)

##### [`get_body_penalty_max() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L850)

##### [`get_endurance_penalty() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L854)

##### [`get_sneak_multiplier() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L858)

##### [`get_level_xp_modifier() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L862)

##### [`get_global_xp_modifier() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L866)

##### [`get_level_bonus() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L870)

##### [`get_month_malus() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L874)

##### [`get_month_bonus() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L878)

##### [`get_light_penalty_cutoff() -> float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/forage.py#L882)


[Previous Folder](../navbox/navbox.md) | [Previous File](fluid.md) | [Next File](item.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
