[Previous Folder](../navbox/navbox.md) | [Previous File](vehicle.md) | [Next File](zone.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# vehicle_part.py

Vehicle part access.

Defines the base VehiclePart class and its many subclasses (e.g. seats, doors, windows),
along with tools for mapping items to parts, resolving install/uninstall data,
and structuring vehicle components for each vehicle definition.

Includes:
- VehiclePart and subclasses for part-specific logic
- VehicleParts manager for handling all parts on a vehicle
- VehiclePartItem for linking items to parts
- PartInstallUninstall helper for install/uninstall requirements

## Functions

### [`get_vehicle_part_class(part_name: str) -> type['VehiclePart']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L19)

Returns the appropriate VehiclePart subclass based on part name prefix.
Defaults to VehiclePart.

## Classes

### `VehiclePartItem`

Item subclass that links items to vehicle parts.

Adds access to all parts that use this item, along with install/uninstall data.

#### Class Methods

##### [`build_item_part_map()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L69)

##### [`has_part(item_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L79)

##### [`from_item(item: 'Item') -> 'VehiclePartItem'`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L85)

Promote the existing Item object to a VehiclePartItem.

#### Properties

##### [`vehicle_parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L98)

##### [`install`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L102)

##### [`uninstall`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L109)

### `VehiclePart`

Base class for a single vehicle part, holding parsed data and common properties
like install/uninstall info, durability, etc.

Used as the parent class for more specific part types.

#### Object Methods

##### [`__init__(part_type: str, vehicle_id: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L123)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L208)

#### Properties

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L129)

##### [`common_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L136)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L142)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L148)

##### [`common_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L154)

##### [`position`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L160)

##### [`container`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L169)

##### [`table`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L173)

##### [`install`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L177)

##### [`uninstall`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L181)

##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L185)

##### [`mechanic_area`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L189)

##### [`area`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L193)

##### [`category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L197)

##### [`durability`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L201)

##### [`mechanic_require_key`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L205)

### `VehicleSeat`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L214)

##### [`seat_position`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L218)

### `VehicleDoor`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L223)

### `VehicleTrunkDoor`

### `VehicleTire`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L232)

##### [`wheel`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L236)

##### [`model`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L240)

##### [`content_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L244)

### `VehicleBrake`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L249)

### `VehicleSuspension`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L254)

### `VehicleEngine`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L259)

### `VehicleBattery`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L264)

### `VehicleMuffler`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L269)

### `VehicleGasTank`

#### Properties

##### [`condition_affects_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L274)

##### [`content_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L278)

### `VehicleRadio`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L283)

### `VehicleGloveBox`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L288)

### `VehicleWindow`

#### Properties

##### [`is_windshield`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L293)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L297)

##### [`parent`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L309)

##### [`window`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L313)

##### [`openable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L317)

### `VehicleHeadlight`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L322)

### `VehicleLightbar`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L329)

### `VehicleHeater`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L334)

### `VehiclePassengerCompartment`

### `VehicleEngineDoor`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L343)

### `VehicleHoodOrnament`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L348)

### `VehicleTruckBed`

#### Properties

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L354)

##### [`condition_affects_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L358)

##### [`capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L362)

### `PartInstallUninstall`

Helper class to handle install/uninstall data for vehicle parts.

#### Object Methods

##### [`__init__(key: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L368)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L372)

Get a value from the install/uninstall data.

##### [`get_item_objects() -> list[Item | Tag]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L403)

Convert items list to a list of item/tag objects

#### Properties

##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L377)

Convert items dict to a sorted list

##### [`formatted_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L388)

##### [`skills`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L423)

##### [`traits`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L426)

##### [`professions`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L429)

##### [`door`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L432)

##### [`time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L435)

##### [`recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L438)

##### [`require_empty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L441)

##### [`require_installed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L444)

##### [`require_uninstalled`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L447)

##### [`test`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L450)

##### [`complete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L453)

### `VehicleParts`

Holds and processes all parts for a single vehicle, including wildcard merging
and access to common components like seats, door, etc.

#### Object Methods

##### [`__init__(parts_raw: dict, vehicle: 'Vehicle')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L500)

##### [`_build_part(name: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L517)

##### [`all() -> list[VehiclePart]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L533)

##### [`get(name: str) -> VehiclePart | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L536)

##### [`parts_starting_with(prefix: str) -> list[VehiclePart]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L539)

#### Properties

##### [`seats`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L543)

##### [`doors`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L547)

##### [`trunk_door`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L551)

##### [`engine`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L555)

##### [`battery`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L559)

##### [`muffler`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L563)

##### [`gas_tank`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L567)

##### [`heater`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L571)

##### [`engine_door`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L575)

##### [`lightbar`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L579)

##### [`passenger_compartment`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L583)

##### [`glove_box`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L587)

##### [`radio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L591)

##### [`truck_bed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L595)

##### [`headlights`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L599)

##### [`windows`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L603)

##### [`windshields`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L607)

##### [`tires`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L611)

##### [`brakes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L615)

##### [`suspensions`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L619)

##### [`hood_ornaments`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L623)


[Previous Folder](../navbox/navbox.md) | [Previous File](vehicle.md) | [Next File](zone.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
