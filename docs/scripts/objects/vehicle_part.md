[Previous Folder](../lists/attachment_list.md) | [Previous File](vehicle.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

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

### [`get_vehicle_part_class(part_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L19)

Returns the appropriate VehiclePart subclass based on part name prefix.

Defaults to VehiclePart.


## Classes

### `VehiclePartItem`

Item subclass that links items to vehicle parts.

Adds access to all parts that use this item, along with install/uninstall data.

#### Class Methods
##### [`build_item_part_map()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L69)
##### [`has_part(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L79)
##### [`from_item(item: 'Item')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L85)

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
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L353)
##### [`condition_affects_capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L357)
##### [`capacity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L361)

### `PartInstallUninstall`

Helper class to handle install/uninstall data for vehicle parts.

#### Object Methods
##### [`__init__(key: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L369)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L373)

Get a value from the install/uninstall data.

##### [`get_item_objects()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L404)

Convert items list to a list of item/tag objects

#### Properties
##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L378)

Convert items dict to a sorted list

##### [`formatted_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L389)
##### [`skills`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L424)
##### [`traits`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L427)
##### [`professions`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L430)
##### [`door`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L433)
##### [`time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L436)
##### [`recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L439)
##### [`require_empty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L442)
##### [`require_installed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L445)
##### [`require_uninstalled`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L448)
##### [`test`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L451)
##### [`complete`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L454)

### `VehicleParts`

Holds and processes all parts for a single vehicle, including wildcard merging

and access to common components like seats, door, etc.

#### Object Methods
##### [`__init__(parts_raw: dict, vehicle: 'Vehicle')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L501)
##### [`_build_part(name: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L518)
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L534)
##### [`get(name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L537)
##### [`parts_starting_with(prefix: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L540)
#### Properties
##### [`seats`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L544)
##### [`doors`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L548)
##### [`trunk_door`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L552)
##### [`engine`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L556)
##### [`battery`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L560)
##### [`muffler`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L564)
##### [`gas_tank`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L568)
##### [`heater`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L572)
##### [`engine_door`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L576)
##### [`lightbar`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L580)
##### [`passenger_compartment`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L584)
##### [`glove_box`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L588)
##### [`radio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L592)
##### [`truck_bed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L596)
##### [`headlights`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L600)
##### [`windows`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L604)
##### [`windshields`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L608)
##### [`tires`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L612)
##### [`brakes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L616)
##### [`suspensions`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L620)
##### [`hood_ornaments`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle_part.py#L624)


[Previous Folder](../lists/attachment_list.md) | [Previous File](vehicle.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
