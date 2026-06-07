[Previous Folder](../navbox/navbox.md) | [Previous File](trap.md) | [Next File](vehicle_part.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# vehicle.py

## Classes

### `Vehicle`

#### Class Methods

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L106)

Return all vehicles as a dictionary of {vehicle_id: Vehicle}.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L113)

Return all vehicle IDs.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L120)

Return all vehicle instances.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L127)

Return the number of loaded vehicles.

##### [`get_model_data(model_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L134)

Return model data for a given model_id.

##### [`fix_vehicle_id(vehicle_id: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L141)

Attempts to fix a partial vehicle_id by assuming the 'Base' module first,
then falling back to a full search through parsed vehicle data.

<ins>**Args:**</ins>
  - **vehicle_id (str)**:
      - _Either a full vehicle_id ('Module.Vehicle') or just a vehicle name._

<ins>**Returns:**</ins>
  - **str**:
      - _The best-guess full vehicle_id._

##### [`_load_vehicles()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L171)

Load vehicle data only once and store in class-level cache.

##### [`_load_models()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L176)

Load vehicle models and store them in a class-level cache.

##### [`_load_mechanics_overlay()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L186)

Load mechanics overlay from LUA table.

#### Object Methods

##### [`__new__(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L27)

Returns an existing Vehicle instance if one already exists for the given ID.

Fixes partial IDs like 'Van' to 'Base.Van' before checking or creating the instance.

##### [`__init__(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L47)

Sets up the vehicle's data if it hasn’t been initialised yet.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L93)

Allows 'vehicle["DisplayName"]'

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L97)

Allows 'in' checks. e.g. '"EvolvedRecipe" in vehicle'

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L101)

Overview of the vehicle when called directly: Vehicle(vehicle_id)

##### [`setup_vehicle()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L193)

Initialise vehicle values.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L204)

Safely get a value from vehicle data with an optional default.

##### [`get_file() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L210)

Return the source file for this vehicle.

##### [`get_path() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L214)

Return the full path of the source file.

##### [`get_name() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L218)

Return the translated name of the vehicle.

##### [`find_name(lang_code: str = None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L224)

##### [`find_is_trailer() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L248)

Determine whether the vehicle is a trailer

##### [`get_parent() -> 'Vehicle' | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L255)

Return the parent as a Vehicle object, or None if this is the root or unknown.

##### [`find_parent() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L263)

Finds the parent vehicle, based on the 3D model.

##### [`get_full_parent() -> 'Vehicle' | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L303)

Return the full parent as a Vehicle object, or self if this is the root or unknown.

##### [`find_full_parent() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L311)

Finds the vehicle type, the parent make/model.

##### [`get_children() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L342)

##### [`find_children() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L347)

##### [`get_page() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L360)

Return the wiki page for this vehicle.

##### [`find_page() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L366)

##### [`get_link() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L376)

Return the wiki page for this vehicle.

##### [`get_variants() -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L382)

Returns a list of vehicle_ids that use this vehicle as their parent.

##### [`find_variants() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L388)

Finds and caches all vehicles whose parent matches this vehicle_id.

##### [`get_manufacturer() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L395)

Returns the vehicles manufacturer

##### [`get_lore_model() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L401)

Returns the vehicles lore model

##### [`find_manufacturer() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L407)

Finds and caches the vehicle manufacturer based on the name.

##### [`get_mechanic_type() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L425)

Return the mechanic type ID for this vehicle.

##### [`get_vehicle_type() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L429)

Return the translated mechanic type name.

##### [`find_vehicle_type() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L435)

##### [`get_model(*, do_format = True) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L441)

Return the rendered 3D model wiki file name as PNG.

##### [`get_models(*, do_format = True) -> str | list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L448)

Return the rendered 3D models as PNGs.

##### [`find_all_models() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L455)

Return all the rendered 3D models including that of all children.

##### [`format_model(*, is_single: bool = False) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L475)

##### [`get_mesh_id() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L497)

Return the internal model ID.

##### [`get_mesh_path() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L503)

Return the file path to the vehicle mesh.

##### [`find_mesh_path() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L509)

##### [`get_texture_path() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L512)

Return the texture path for the vehicle skin.

##### [`get_car_model_name() -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L518)

Return the in-game display name from carModelName, if defined.

##### [`get_mass() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L525)

Return the vehicle mass, defaulting to 800.0.

##### [`get_zombie_type() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L529)

Return a list of zombie types allowed to spawn in the vehicle.

##### [`get_special_key_ring() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L538)

Return possible special key ring types defined for the vehicle.

##### [`get_special_key_chance() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L547)

Return the chance percentage of the vehicle spawning with a special key ring.

##### [`get_engine_repair_level() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L551)

Return the engine repair level required.

##### [`get_player_damage_protection() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L555)

Return the player damage protection value.

##### [`get_wheels() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L559)

Return the wheels in the vehicle.

##### [`get_doors() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L565)

Return the doors in the vehicle.

##### [`get_seats() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L576)

Return the number of seats in the vehicle.

##### [`get_wheel_friction() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L582)

Return the vehicle's wheel friction value.

##### [`get_braking_force() -> int | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L587)

Return the vehicle's braking force.

##### [`get_max_speed() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L592)

Return the vehicle's max speed.

##### [`get_roll_influence() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L596)

Return the roll influence value.

##### [`get_is_small_vehicle() -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L600)

Return whether the vehicle is small.

##### [`get_stopping_movement_force() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L604)

Return the stopping force applied when idle.

##### [`get_animal_trailer_size() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L608)

Return the trailer's animal capacity.

##### [`get_attachments() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L612)

Return the attachment points available.

##### [`get_offroad_efficiency() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L616)

Return the offroad driving efficiency.

##### [`get_has_lightbar() -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L620)

Return whether the vehicle has a lightbar.

##### [`get_has_siren() -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L626)

Return whether the vehicle has a siren.

##### [`find_lightbar() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L632)

Detect if the vehicle has a lightbar siren.

##### [`get_has_reverse_beeper()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L639)

Return whether the vehicle has a reverse beeper.

##### [`get_front_end_health() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L646)

Return the vehicle's front-end health.

##### [`get_rear_end_health() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L650)

Return the vehicle's rear-end health.

##### [`get_engine_force() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L655)

Return the engine force.

##### [`get_engine_power() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L659)

Returns the engine power in horsepower (hp).

##### [`get_engine_quality() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L663)

Return the engine quality.

##### [`get_engine_loudness() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L667)

Return how loud the engine is.

##### [`get_engine_rpm_type() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L671)

Return the engine RPM type.

##### [`get_steering_increment() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L676)

Return how fast the steering changes.

##### [`get_steering_clamp() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L680)

Return the steering limit angle.

##### [`get_suspension_stiffness() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L685)

Return the suspension stiffness.

##### [`get_suspension_compression() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L689)

Return the suspension compression rate.

##### [`get_suspension_damping() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L694)

Return the suspension damping rate.

##### [`get_max_suspension_travel_cm() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L699)

Return the max suspension travel in cm.

##### [`get_suspension_rest_length() -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L703)

Return the rest length of the suspension.

##### [`get_parts_data() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L708)

Return parts data with wildcard templates merged into specific parts.

##### [`get_parts() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L744)

Return a list of part names.

##### [`get_part(part) -> dict | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L748)

Return part data, allowing fuzzy lookup with '*'.

##### [`get_part_table(part: str) -> dict | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L761)

Return the part table if present, or the base data.

##### [`get_part_install(part: str) -> dict | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L774)

Return install data for a given part.

##### [`get_part_uninstall(part: str) -> dict | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L779)

Return uninstall data for a given part.

##### [`get_recipes() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L784)

Return recipes that need to be known to remove parts.

##### [`find_part_recipe() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L790)

Find and cache install/uninstall recipes from parts.

##### [`find_part_capacity(part_data: dict, part: str = None) -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L812)

Determine part capacity from part container or fallback itemType.

##### [`get_glove_box_capacity() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L830)

##### [`find_glove_box_capacity() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L835)

##### [`get_trunk_capacity() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L843)

##### [`find_trunk_capacity() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L848)

##### [`get_seat_capacity() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L866)

##### [`find_seat_capacity() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L871)

##### [`get_total_capacity() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L881)

##### [`calculate_total_capacity() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L886)

##### [`get_mechanics_overlay()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L893)

Return mechanics overlay.

#### Properties

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L913)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L919)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L925)

Return the wiki page for this vehicle.

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L938)

Return the wiki link for this vehicle.

##### [`parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L945)

Return a list of part names.


[Previous Folder](../navbox/navbox.md) | [Previous File](trap.md) | [Next File](vehicle_part.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
