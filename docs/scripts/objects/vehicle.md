[Previous Folder](../lists/body_locations_list.md) | [Previous File](item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# vehicle.py

## Classes

### `Vehicle`
#### Class Methods
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L109)

Return all vehicles as a dictionary of {vehicle_id: Vehicle}.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L116)

Return all vehicle IDs.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L123)

Return all vehicle instances.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L130)

Return the number of loaded vehicles.

##### [`get_model_data(model_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L137)

Return model data for a given model_id.

##### [`fix_vehicle_id(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L144)

Attempts to fix a partial vehicle_id by assuming the 'Base' module first,

then falling back to a full search through parsed vehicle data.

<ins>**Args:**</ins>
  - **vehicle_id (str)**:
      - _Either a full vehicle_id ('Module.Vehicle') or just a vehicle name._

<ins>**Returns:**</ins>
  - **str:**
      - The best-guess full vehicle_id.

##### [`_load_vehicles()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L174)

Load vehicle data only once and store in class-level cache.

##### [`_load_models()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L179)

Load vehicle models and store them in a class-level cache.

##### [`_load_mechanics_overlay()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L189)

Load mechanics overlay from LUA table.

##### [`format_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L477)
#### Object Methods
##### [`__new__(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L25)

Returns an existing Vehicle instance if one already exists for the given ID.

Fixes partial IDs like 'Van' to 'Base.Van' before checking or creating the instance.

##### [`__init__(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L45)

Sets up the vehicle's data if it hasn’t been initialised yet.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L96)

Allows 'vehicle["DisplayName"]'

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L100)

Allows 'in' checks. e.g. '"EvolvedRecipe" in vehicle'

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L104)

Overview of the vehicle when called directly: Vehicle(vehicle_id)

##### [`setup_vehicle()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L196)

Initialise vehicle values.

##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L207)

Safely get a value from vehicle data with an optional default.

##### [`get_file()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L213)

Return the source file for this vehicle.

##### [`get_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L217)

Return the full path of the source file.

##### [`get_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L221)

Return the translated name of the vehicle.

##### [`find_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L227)
##### [`find_is_trailer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L248)

Determine whether the vehicle is a trailer

##### [`get_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L255)

Return the parent as a Vehicle object, or None if this is the root or unknown.

##### [`find_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L263)

Finds the parent vehicle, based on the 3D model.

##### [`get_full_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L302)

Return the full parent as a Vehicle object, or self if this is the root or unknown.

##### [`find_full_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L310)

Finds the vehicle type, the parent make/model.

##### [`get_children()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L341)
##### [`find_children()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L346)
##### [`get_page()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L359)

Return the wiki page for this vehicle.

##### [`find_page()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L365)
##### [`get_link()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L375)

Return the wiki page for this vehicle.

##### [`get_variants()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L381)

Returns a list of vehicle_ids that use this vehicle as their parent.

##### [`find_variants()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L387)

Finds and caches all vehicles whose parent matches this vehicle_id.

##### [`get_manufacturer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L394)

Returns the vehicles manufacturer

##### [`get_lore_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L400)

Returns the vehicles lore model

##### [`find_manufacturer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L406)

Finds and caches the vehicle manufacturer based on the name.

##### [`get_mechanic_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L424)

Return the mechanic type ID for this vehicle.

##### [`get_vehicle_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L428)

Return the translated mechanic type name.

##### [`find_vehicle_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L434)
##### [`get_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L440)

Return the rendered 3D model wiki file name as PNG.

##### [`find_all_models()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L457)

Return all the rendered 3D models including that of all children.

##### [`get_mesh_id()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L493)

Return the internal model ID.

##### [`get_mesh_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L499)

Return the file path to the vehicle mesh.

##### [`find_mesh_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L505)
##### [`get_texture_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L508)

Return the texture path for the vehicle skin.

##### [`get_car_model_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L514)

Return the in-game display name from carModelName, if defined.

##### [`get_mass()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L521)

Return the vehicle mass, defaulting to 800.0.

##### [`get_zombie_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L525)

Return a list of zombie types allowed to spawn in the vehicle.

##### [`get_special_key_ring()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L534)

Return possible special key ring types defined for the vehicle.

##### [`get_special_key_chance()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L543)

Return the chance percentage of the vehicle spawning with a special key ring.

##### [`get_engine_repair_level()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L547)

Return the engine repair level required.

##### [`get_player_damage_protection()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L551)

Return the player damage protection value.

##### [`get_wheels()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L555)

Return the wheels in the vehicle.

##### [`get_doors()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L561)

Return the doors in the vehicle.

##### [`get_seats()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L572)

Return the number of seats in the vehicle.

##### [`get_wheel_friction()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L578)

Return the vehicle's wheel friction value.

##### [`get_braking_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L583)

Return the vehicle's braking force.

##### [`get_max_speed()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L588)

Return the vehicle's max speed.

##### [`get_roll_influence()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L592)

Return the roll influence value.

##### [`get_is_small_vehicle()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L596)

Return whether the vehicle is small.

##### [`get_stopping_movement_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L600)

Return the stopping force applied when idle.

##### [`get_animal_trailer_size()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L604)

Return the trailer's animal capacity.

##### [`get_attachments()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L608)

Return the attachment points available.

##### [`get_offroad_efficiency()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L612)

Return the offroad driving efficiency.

##### [`get_has_lightbar()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L616)

Return whether the vehicle has a lightbar.

##### [`get_has_siren()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L622)

Return whether the vehicle has a siren.

##### [`find_lightbar()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L628)

Detect if the vehicle has a lightbar siren.

##### [`get_has_reverse_beeper()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L635)

Return whether the vehicle has a reverse beeper.

##### [`get_front_end_health()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L642)

Return the vehicle's front-end health.

##### [`get_rear_end_health()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L646)

Return the vehicle's rear-end health.

##### [`get_engine_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L651)

Return the engine force.

##### [`get_engine_power()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L655)

Returns the engine power in horsepower (hp).

##### [`get_engine_quality()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L659)

Return the engine quality.

##### [`get_engine_loudness()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L663)

Return how loud the engine is.

##### [`get_engine_rpm_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L667)

Return the engine RPM type.

##### [`get_steering_increment()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L672)

Return how fast the steering changes.

##### [`get_steering_clamp()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L676)

Return the steering limit angle.

##### [`get_suspension_stiffness()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L681)

Return the suspension stiffness.

##### [`get_suspension_compression()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L685)

Return the suspension compression rate.

##### [`get_suspension_damping()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L690)

Return the suspension damping rate.

##### [`get_max_suspension_travel_cm()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L695)

Return the max suspension travel in cm.

##### [`get_suspension_rest_length()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L699)

Return the rest length of the suspension.

##### [`get_parts_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L704)

Return parts data with wildcard templates merged into specific parts.

##### [`get_parts()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L736)

Return a list of part names.

##### [`get_part(part)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L740)

Return part data, allowing fuzzy lookup with '*'.

##### [`get_part_table(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L753)

Return the part table if present, or the base data.

##### [`get_part_install(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L766)

Return install data for a given part.

##### [`get_part_uninstall(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L771)

Return uninstall data for a given part.

##### [`get_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L776)

Return recipes that need to be known to remove parts.

##### [`find_part_recipe()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L782)

Find and cache install/uninstall recipes from parts.

##### [`find_part_capacity(part_data: dict, part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L804)

Determine part capacity from part container or fallback itemType.

##### [`get_glove_box_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L822)
##### [`find_glove_box_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L827)
##### [`get_trunk_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L835)
##### [`find_trunk_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L840)
##### [`get_seat_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L858)
##### [`find_seat_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L863)
##### [`get_total_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L873)
##### [`calculate_total_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L878)
##### [`get_mechanics_overlay()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L885)

Return mechanics overlay.



[Previous Folder](../lists/body_locations_list.md) | [Previous File](item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
