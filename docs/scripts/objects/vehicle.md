[Previous Folder](../lists/body_locations_list.md) | [Previous File](item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# vehicle.py

## Classes

### `Vehicle`
#### Class Methods
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L109)

_Return all vehicles as a dictionary of {vehicle_id: Vehicle}._
##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L116)

_Return all vehicle IDs._
##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L123)

_Return all vehicle instances._
##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L130)

_Return the number of loaded vehicles._
##### [`get_model_data(model_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L137)

_Return model data for a given model_id._
##### [`fix_vehicle_id(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L144)

_Attempts to fix a partial vehicle_id by assuming the 'Base' module first,_

<ins>**Args:**</ins>
  - **vehicle_id (str)**:
      - _Either a full vehicle_id ('Module.Vehicle') or just a vehicle name._

<ins>**Returns:**</ins>
  - **str:**
      - The best-guess full vehicle_id.
##### [`_load_vehicles()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L174)

_Load vehicle data only once and store in class-level cache._
##### [`_load_models()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L179)

_Load vehicle models and store them in a class-level cache._
##### [`_load_mechanics_overlay()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L189)

_Load mechanics overlay from LUA table._
##### [`format_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L477)
#### Object Methods
##### [`__new__(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L25)

_Returns an existing Vehicle instance if one already exists for the given ID._
##### [`__init__(vehicle_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L45)

_Sets up the vehicle's data if it hasn’t been initialised yet._
##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L96)

_Allows 'vehicle["DisplayName"]'_
##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L100)

_Allows 'in' checks. e.g. '"EvolvedRecipe" in vehicle'_
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L104)

_Overview of the vehicle when called directly: Vehicle(vehicle_id)_
##### [`setup_vehicle()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L196)

_Initialise vehicle values._
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L207)

_Safely get a value from vehicle data with an optional default._
##### [`get_file()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L213)

_Return the source file for this vehicle._
##### [`get_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L217)

_Return the full path of the source file._
##### [`get_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L221)

_Return the translated name of the vehicle._
##### [`find_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L227)
##### [`find_is_trailer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L248)

_Determine whether the vehicle is a trailer_
##### [`get_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L255)

_Return the parent as a Vehicle object, or None if this is the root or unknown._
##### [`find_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L263)

_Finds the parent vehicle, based on the 3D model._
##### [`get_full_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L302)

_Return the full parent as a Vehicle object, or self if this is the root or unknown._
##### [`find_full_parent()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L310)

_Finds the vehicle type, the parent make/model._
##### [`get_children()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L341)
##### [`find_children()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L346)
##### [`get_page()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L359)

_Return the wiki page for this vehicle._
##### [`find_page()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L365)
##### [`get_link()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L375)

_Return the wiki page for this vehicle._
##### [`get_variants()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L381)

_Returns a list of vehicle_ids that use this vehicle as their parent._
##### [`find_variants()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L387)

_Finds and caches all vehicles whose parent matches this vehicle_id._
##### [`get_manufacturer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L394)

_Returns the vehicles manufacturer_
##### [`get_lore_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L400)

_Returns the vehicles lore model_
##### [`find_manufacturer()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L406)

_Finds and caches the vehicle manufacturer based on the name._
##### [`get_mechanic_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L424)

_Return the mechanic type ID for this vehicle._
##### [`get_vehicle_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L428)

_Return the translated mechanic type name._
##### [`find_vehicle_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L434)
##### [`get_model()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L440)

_Return the rendered 3D model wiki file name as PNG._
##### [`find_all_models()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L457)

_Return all the rendered 3D models including that of all children._
##### [`get_mesh_id()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L493)

_Return the internal model ID._
##### [`get_mesh_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L499)

_Return the file path to the vehicle mesh._
##### [`find_mesh_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L505)
##### [`get_texture_path()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L508)

_Return the texture path for the vehicle skin._
##### [`get_car_model_name()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L514)

_Return the in-game display name from carModelName, if defined._
##### [`get_mass()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L521)

_Return the vehicle mass, defaulting to 800.0._
##### [`get_zombie_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L525)

_Return a list of zombie types allowed to spawn in the vehicle._
##### [`get_special_key_ring()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L534)

_Return possible special key ring types defined for the vehicle._
##### [`get_special_key_chance()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L543)

_Return the chance percentage of the vehicle spawning with a special key ring._
##### [`get_engine_repair_level()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L547)

_Return the engine repair level required._
##### [`get_player_damage_protection()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L551)

_Return the player damage protection value._
##### [`get_wheels()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L555)

_Return the wheels in the vehicle._
##### [`get_doors()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L561)

_Return the doors in the vehicle._
##### [`get_seats()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L572)

_Return the number of seats in the vehicle._
##### [`get_wheel_friction()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L578)

_Return the vehicle's wheel friction value._
##### [`get_braking_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L583)

_Return the vehicle's braking force._
##### [`get_max_speed()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L588)

_Return the vehicle's max speed._
##### [`get_roll_influence()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L592)

_Return the roll influence value._
##### [`get_is_small_vehicle()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L596)

_Return whether the vehicle is small._
##### [`get_stopping_movement_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L600)

_Return the stopping force applied when idle._
##### [`get_animal_trailer_size()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L604)

_Return the trailer's animal capacity._
##### [`get_attachments()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L608)

_Return the attachment points available._
##### [`get_offroad_efficiency()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L612)

_Return the offroad driving efficiency._
##### [`get_has_lightbar()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L616)

_Return whether the vehicle has a lightbar._
##### [`get_has_siren()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L622)

_Return whether the vehicle has a siren._
##### [`find_lightbar()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L628)

_Detect if the vehicle has a lightbar siren._
##### [`get_has_reverse_beeper()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L635)

_Return whether the vehicle has a reverse beeper._
##### [`get_front_end_health()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L642)

_Return the vehicle's front-end health._
##### [`get_rear_end_health()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L646)

_Return the vehicle's rear-end health._
##### [`get_engine_force()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L651)

_Return the engine force._
##### [`get_engine_power()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L655)

_Returns the engine power in horsepower (hp)._
##### [`get_engine_quality()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L659)

_Return the engine quality._
##### [`get_engine_loudness()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L663)

_Return how loud the engine is._
##### [`get_engine_rpm_type()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L667)

_Return the engine RPM type._
##### [`get_steering_increment()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L672)

_Return how fast the steering changes._
##### [`get_steering_clamp()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L676)

_Return the steering limit angle._
##### [`get_suspension_stiffness()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L681)

_Return the suspension stiffness._
##### [`get_suspension_compression()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L685)

_Return the suspension compression rate._
##### [`get_suspension_damping()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L690)

_Return the suspension damping rate._
##### [`get_max_suspension_travel_cm()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L695)

_Return the max suspension travel in cm._
##### [`get_suspension_rest_length()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L699)

_Return the rest length of the suspension._
##### [`get_parts_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L704)

_Return parts data with wildcard templates merged into specific parts._
##### [`get_parts()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L736)

_Return a list of part names._
##### [`get_part(part)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L740)

_Return part data, allowing fuzzy lookup with '*'._
##### [`get_part_table(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L753)

_Return the part table if present, or the base data._
##### [`get_part_install(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L766)

_Return install data for a given part._
##### [`get_part_uninstall(part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L771)

_Return uninstall data for a given part._
##### [`get_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L776)

_Return recipes that need to be known to remove parts._
##### [`find_part_recipe()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L782)

_Find and cache install/uninstall recipes from parts._
##### [`find_part_capacity(part_data: dict, part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L804)

_Determine part capacity from part container or fallback itemType._
##### [`get_glove_box_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L822)
##### [`find_glove_box_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L827)
##### [`get_trunk_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L835)
##### [`find_trunk_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L840)
##### [`get_seat_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L858)
##### [`find_seat_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L863)
##### [`get_total_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L873)
##### [`calculate_total_capacity()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L878)
##### [`get_mechanics_overlay()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/vehicle.py#L885)

_Return mechanics overlay._


[Previous Folder](../lists/body_locations_list.md) | [Previous File](item.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
