[Previous Folder](../lists/attachment_list.md) | [Previous File](trap.md) | [Next File](vehicle_part.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# vehicle.py

## Classes

### `Vehicle`
#### Class Methods
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L110)

Return all vehicles as a dictionary of {vehicle_id: Vehicle}.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L117)

Return all vehicle IDs.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L124)

Return all vehicle instances.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L131)

Return the number of loaded vehicles.

##### [`get_model_data(model_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L138)

Return model data for a given model_id.

##### [`fix_vehicle_id(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L145)

Attempts to fix a partial vehicle_id by assuming the 'Base' module first,

then falling back to a full search through parsed vehicle data.

<ins>**Args:**</ins>
  - **vehicle_id (str)**:
      - _Either a full vehicle_id ('Module.Vehicle') or just a vehicle name._

<ins>**Returns:**</ins>
  - **str:**
      - The best-guess full vehicle_id.

##### [`_load_vehicles()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L175)

Load vehicle data only once and store in class-level cache.

##### [`_load_models()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L180)

Load vehicle models and store them in a class-level cache.

##### [`_load_mechanics_overlay()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L190)

Load mechanics overlay from LUA table.

##### [`format_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L478)
#### Object Methods
##### [`__new__(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L26)

Returns an existing Vehicle instance if one already exists for the given ID.

Fixes partial IDs like 'Van' to 'Base.Van' before checking or creating the instance.

##### [`__init__(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L46)

Sets up the vehicle's data if it hasn’t been initialised yet.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L97)

Allows 'vehicle["DisplayName"]'

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L101)

Allows 'in' checks. e.g. '"EvolvedRecipe" in vehicle'

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L105)

Overview of the vehicle when called directly: Vehicle(vehicle_id)

##### [`setup_vehicle()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L197)

Initialise vehicle values.

##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L208)

Safely get a value from vehicle data with an optional default.

##### [`get_file()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L214)

Return the source file for this vehicle.

##### [`get_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L218)

Return the full path of the source file.

##### [`get_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L222)

Return the translated name of the vehicle.

##### [`find_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L228)
##### [`find_is_trailer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L249)

Determine whether the vehicle is a trailer

##### [`get_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L256)

Return the parent as a Vehicle object, or None if this is the root or unknown.

##### [`find_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L264)

Finds the parent vehicle, based on the 3D model.

##### [`get_full_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L303)

Return the full parent as a Vehicle object, or self if this is the root or unknown.

##### [`find_full_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L311)

Finds the vehicle type, the parent make/model.

##### [`get_children()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L342)
##### [`find_children()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L347)
##### [`get_page()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L360)

Return the wiki page for this vehicle.

##### [`find_page()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L366)
##### [`get_link()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L376)

Return the wiki page for this vehicle.

##### [`get_variants()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L382)

Returns a list of vehicle_ids that use this vehicle as their parent.

##### [`find_variants()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L388)

Finds and caches all vehicles whose parent matches this vehicle_id.

##### [`get_manufacturer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L395)

Returns the vehicles manufacturer

##### [`get_lore_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L401)

Returns the vehicles lore model

##### [`find_manufacturer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L407)

Finds and caches the vehicle manufacturer based on the name.

##### [`get_mechanic_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L425)

Return the mechanic type ID for this vehicle.

##### [`get_vehicle_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L429)

Return the translated mechanic type name.

##### [`find_vehicle_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L435)
##### [`get_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L441)

Return the rendered 3D model wiki file name as PNG.

##### [`find_all_models()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L458)

Return all the rendered 3D models including that of all children.

##### [`get_mesh_id()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L494)

Return the internal model ID.

##### [`get_mesh_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L500)

Return the file path to the vehicle mesh.

##### [`find_mesh_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L506)
##### [`get_texture_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L509)

Return the texture path for the vehicle skin.

##### [`get_car_model_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L515)

Return the in-game display name from carModelName, if defined.

##### [`get_mass()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L522)

Return the vehicle mass, defaulting to 800.0.

##### [`get_zombie_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L526)

Return a list of zombie types allowed to spawn in the vehicle.

##### [`get_special_key_ring()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L535)

Return possible special key ring types defined for the vehicle.

##### [`get_special_key_chance()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L544)

Return the chance percentage of the vehicle spawning with a special key ring.

##### [`get_engine_repair_level()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L548)

Return the engine repair level required.

##### [`get_player_damage_protection()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L552)

Return the player damage protection value.

##### [`get_wheels()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L556)

Return the wheels in the vehicle.

##### [`get_doors()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L562)

Return the doors in the vehicle.

##### [`get_seats()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L573)

Return the number of seats in the vehicle.

##### [`get_wheel_friction()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L579)

Return the vehicle's wheel friction value.

##### [`get_braking_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L584)

Return the vehicle's braking force.

##### [`get_max_speed()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L589)

Return the vehicle's max speed.

##### [`get_roll_influence()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L593)

Return the roll influence value.

##### [`get_is_small_vehicle()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L597)

Return whether the vehicle is small.

##### [`get_stopping_movement_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L601)

Return the stopping force applied when idle.

##### [`get_animal_trailer_size()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L605)

Return the trailer's animal capacity.

##### [`get_attachments()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L609)

Return the attachment points available.

##### [`get_offroad_efficiency()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L613)

Return the offroad driving efficiency.

##### [`get_has_lightbar()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L617)

Return whether the vehicle has a lightbar.

##### [`get_has_siren()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L623)

Return whether the vehicle has a siren.

##### [`find_lightbar()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L629)

Detect if the vehicle has a lightbar siren.

##### [`get_has_reverse_beeper()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L636)

Return whether the vehicle has a reverse beeper.

##### [`get_front_end_health()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L643)

Return the vehicle's front-end health.

##### [`get_rear_end_health()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L647)

Return the vehicle's rear-end health.

##### [`get_engine_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L652)

Return the engine force.

##### [`get_engine_power()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L656)

Returns the engine power in horsepower (hp).

##### [`get_engine_quality()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L660)

Return the engine quality.

##### [`get_engine_loudness()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L664)

Return how loud the engine is.

##### [`get_engine_rpm_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L668)

Return the engine RPM type.

##### [`get_steering_increment()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L673)

Return how fast the steering changes.

##### [`get_steering_clamp()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L677)

Return the steering limit angle.

##### [`get_suspension_stiffness()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L682)

Return the suspension stiffness.

##### [`get_suspension_compression()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L686)

Return the suspension compression rate.

##### [`get_suspension_damping()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L691)

Return the suspension damping rate.

##### [`get_max_suspension_travel_cm()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L696)

Return the max suspension travel in cm.

##### [`get_suspension_rest_length()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L700)

Return the rest length of the suspension.

##### [`get_parts_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L705)

Return parts data with wildcard templates merged into specific parts.

##### [`get_parts()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L737)

Return a list of part names.

##### [`get_part(part)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L741)

Return part data, allowing fuzzy lookup with '*'.

##### [`get_part_table(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L754)

Return the part table if present, or the base data.

##### [`get_part_install(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L767)

Return install data for a given part.

##### [`get_part_uninstall(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L772)

Return uninstall data for a given part.

##### [`get_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L777)

Return recipes that need to be known to remove parts.

##### [`find_part_recipe()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L783)

Find and cache install/uninstall recipes from parts.

##### [`find_part_capacity(part_data: dict, part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L805)

Determine part capacity from part container or fallback itemType.

##### [`get_glove_box_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L823)
##### [`find_glove_box_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L828)
##### [`get_trunk_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L836)
##### [`find_trunk_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L841)
##### [`get_seat_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L859)
##### [`find_seat_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L864)
##### [`get_total_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L874)
##### [`calculate_total_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L879)
##### [`get_mechanics_overlay()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L886)

Return mechanics overlay.

#### Properties
##### [`parts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L895)

Return a list of part names.



[Previous Folder](../lists/attachment_list.md) | [Previous File](trap.md) | [Next File](vehicle_part.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
