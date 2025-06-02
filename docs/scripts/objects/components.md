[Previous Folder](../lists/body_locations_list.md) | [Next File](fluid.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# components.py

Provides the FluidContainer and Durability classes for managing components 
related to fluid handling and durability.

- FluidContainer holds information about an item’s fluid types, capacities, 
  mixing ratios, and special behaviour (e.g., random fluid selection).
- Durability tracks an item’s material and maximum hit points, supporting 
  durability-based mechanics.

These classes serve as lightweight wrappers over raw component data, offering 
convenient property access and helper methods.

## Classes

### `FluidContainer`

Represents the FluidContainer component of an item or entity, holding information 

about contained fluids, capacities, and mixing proportions.

#### Object Methods
##### [`__init__(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L22)

Initialize a FluidContainer with raw component data.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _FluidContainer data dictionary._

##### [`__bool__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L31)

Allow FluidContainer to evaluate as False if empty, True if data exists.

#### Properties
##### [`container_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L36)

Return the translated container name.

##### [`rain_factor`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L43)

Return the rain collection factor (float).

##### [`capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L48)

Return the container’s fluid capacity (int).

##### [`custom_drink_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L53)

Return the custom drink sound, if defined (str or None).

##### [`fluids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L58)

Return a list of Fluid objects, including mix ratios and optional colors.

##### [`fluid_proportions`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L85)

Return the raw list of fluid proportions (list of floats).

##### [`fluid_map`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L99)

Return a dictionary mapping Fluid objects to normalised proportions.

If PickRandomFluid is True, all fluids are given equal weighting (1.0).

##### [`pick_random_fluid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L122)

Return whether the container picks a random fluid (bool).

##### [`initial_percent_min`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L127)

Return the minimum initial fill percentage (float).

##### [`initial_percent_max`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L132)

Return the maximum initial fill percentage (float).


### `Durability`

Represents the Durability component of an item, including material type 

and maximum hit points.

#### Object Methods
##### [`__init__(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L142)

Initialize a Durability object with raw component data.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Durability data dictionary._

##### [`__bool__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L151)

Allow Durability to evaluate as False if empty, True if data exists.

#### Properties
##### [`material`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L156)

Return the material type (str), defaults to 'Default'.

##### [`max_hit_points`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/components.py#L161)

Return the maximum hit points (int), defaults to 0.



[Previous Folder](../lists/body_locations_list.md) | [Next File](fluid.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
