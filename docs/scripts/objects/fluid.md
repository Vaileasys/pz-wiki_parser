[Previous Folder](../lists/body_locations_list.md) | [Previous File](components.md) | [Next File](item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# fluid.py

## Classes

### `Fluid`
#### Class Methods
##### [`_load_fluids()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L68)

Load fluid data only once and store in class-level cache.

##### [`_load_color_reference()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L73)
##### [`fix_fluid_id(fluid_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L78)

Fixes a partial fluid_id by assuming 'Base' first, then fallback to search.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L101)

Return all fluids as a dictionary of {fluid_id: Fluid}.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L108)
##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L114)
##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L120)
#### Object Methods
##### [`__new__(fluid_id: str, mix_ratio, color)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L15)

Returns an existing Fluid instance if one already exists for the given ID.

If overrides are provided, returns a new instance

##### [`__init__(fluid_id: str, mix_ratio, color)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L35)

Initialises the fluid’s data if it hasn’t been initialised yet.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L58)
##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L61)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L64)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L127)
#### Properties
##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L135)
##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L139)
##### [`module`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L143)
##### [`id_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L147)
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L151)
##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L158)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L162)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L172)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L182)
##### [`mix_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L188)

Return the fluid’s relative mix ratio (defaults to 1.0 if not set).

##### [`properties`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L195)

Return the 'Properties' block or an empty dict.

##### [`fatigue_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L200)
##### [`hunger_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L204)
##### [`stress_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L208)
##### [`thirst_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L212)
##### [`unhappy_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L216)
##### [`calories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L220)
##### [`carbohydrates`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L224)
##### [`lipids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L228)
##### [`proteins`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L232)
##### [`alcohol`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L236)
##### [`flu_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L240)
##### [`pain_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L244)
##### [`endurance_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L248)
##### [`food_sickness_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L252)
##### [`poison`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L258)

Return a FluidPoison object wrapping the 'Poison' block.

##### [`color_reference`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L267)
##### [`color`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L271)

Return the fluid color as [R, G, B] integers (0–255).

##### [`rgb`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L289)

Return the fluid color as a wiki RGB template string, e.g., '{{rgb|140, 198, 0}}'.

##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L297)

Return the fluid's category list, or empty if none.

##### [`blend_whitelist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L302)

Return FluidBlendList for BlendWhiteList (empty if missing).

##### [`blend_blacklist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L310)

Return FluidBlendList for BlendBlackList (empty if missing).


### `FluidPoison`
#### Object Methods
##### [`__init__(poison_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L319)
#### Properties
##### [`max_effect`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L323)
##### [`min_amount`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L327)
##### [`dilute_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L331)

### `FluidBlendList`
#### Object Methods
##### [`__init__(blend_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L336)
#### Properties
##### [`whitelist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L340)
##### [`blacklist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L344)
##### [`fluids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L348)
##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L352)


[Previous Folder](../lists/body_locations_list.md) | [Previous File](components.md) | [Next File](item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
