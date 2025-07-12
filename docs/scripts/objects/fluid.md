[Previous Folder](../lists/attachment_list.md) | [Previous File](fixing.md) | [Next File](forage.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# fluid.py

## Classes

### `Fluid`
#### Class Methods
##### [`_load_fluids()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L70)

Load fluid data only once and store in class-level cache.

##### [`_load_color_reference()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L75)
##### [`fix_fluid_id(fluid_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L80)

Fixes a partial fluid_id by assuming 'Base' first, then fallback to search.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L103)

Return all fluids as a dictionary of {fluid_id: Fluid}.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L110)
##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L116)
##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L122)
##### [`exists(fluid_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L128)
#### Object Methods
##### [`__new__(fluid_id: str, mix_ratio, color)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L15)

Returns an existing Fluid instance if one already exists for the given ID.

If overrides are provided, returns a new instance

##### [`__init__(fluid_id: str, mix_ratio, color)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L35)

Initialises the fluid’s data if it hasn’t been initialised yet.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L60)
##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L63)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L66)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L137)
#### Properties
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L145)
##### [`script_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L149)
##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L153)
##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L157)
##### [`module`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L161)
##### [`id_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L165)
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L169)
##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L176)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L180)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L190)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L200)
##### [`mix_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L206)

Return the fluid’s relative mix ratio (defaults to 1.0 if not set).

##### [`properties`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L213)

Return the 'Properties' block or an empty dict.

##### [`fatigue_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L218)
##### [`hunger_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L222)
##### [`stress_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L226)
##### [`thirst_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L230)
##### [`unhappy_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L234)
##### [`calories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L238)
##### [`carbohydrates`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L242)
##### [`lipids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L246)
##### [`proteins`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L250)
##### [`alcohol`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L254)
##### [`flu_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L258)
##### [`pain_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L262)
##### [`endurance_change`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L266)
##### [`food_sickness_reduction`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L270)
##### [`poison`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L276)

Return a FluidPoison object wrapping the 'Poison' block.

##### [`color_reference`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L285)
##### [`color`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L289)

Return the fluid color as [R, G, B] integers (0–255).

##### [`r`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L307)
##### [`g`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L311)
##### [`b`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L315)
##### [`rgb`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L319)

Return the fluid color as a wiki RGB template string, e.g., '{{rgb|140, 198, 0}}'.

##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L327)

Return the fluid's category list, or empty if none.

##### [`blend_whitelist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L332)

Return FluidBlendList for BlendWhiteList (empty if missing).

##### [`blend_blacklist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L340)

Return FluidBlendList for BlendBlackList (empty if missing).


### `FluidPoison`
#### Object Methods
##### [`__init__(poison_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L349)
#### Properties
##### [`max_effect`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L353)
##### [`min_amount`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L357)
##### [`dilute_ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L361)

### `FluidBlendList`
#### Object Methods
##### [`__init__(blend_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L366)
#### Properties
##### [`whitelist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L370)
##### [`blacklist`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L374)
##### [`fluids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L378)
##### [`categories`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fluid.py#L382)


[Previous Folder](../lists/attachment_list.md) | [Previous File](fixing.md) | [Next File](forage.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
