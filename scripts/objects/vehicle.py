from __future__ import annotations
from scripts.parser import script_parser
from scripts.core.file_loading import get_script_path
from scripts.core import logger
from scripts.core.language import Translate
from scripts.utils.echo import echo_warning
from scripts.core.cache import save_json

class Vehicle:
    _vehicles = None # Shared cache for all vehicles
    _instances = {}
    _vehicle_models = None
    MANUFACTURERS = (
            "Chevalier",
            "Dash",
            "Franklin",
            "Masterson",
            "Mercia Lang"
        )

    def __new__(cls, vehicle_id: str):
        """Returns an existing Vehicle instance if one already exists for the given ID.
        
        Fixes partial IDs like 'Van' to 'Base.Van' before checking or creating the instance."""
        if cls._vehicles is None:
            cls._load_vehicles()

        vehicle_id = cls.fix_vehicle_id(vehicle_id)

        if vehicle_id in cls._instances:
            return cls._instances[vehicle_id]

        instance = super().__new__(cls)
        cls._instances[vehicle_id] = instance
        return instance

    def __init__(self, vehicle_id: str):
        """Sets up the vehicle's data if it hasn’t been initialised yet."""
        if hasattr(self, 'vehicle_id'):
            return

        if Vehicle._vehicles is None:
            Vehicle._load_vehicles()

        vehicle_id = self.fix_vehicle_id(vehicle_id)

        self.vehicle_id = vehicle_id
        self.data = Vehicle._vehicles.get(vehicle_id, {})

        self.module, self.id_type = vehicle_id.split(".", 1)

        self.name = None # English name
        self.page = None # Wiki page
        self.model = self.id_type + "_Model.png"

        self.mesh_id = None
        self.mesh_path = None

        self.parent_id = None # inferred by the game
        self.full_parent_id = None # lore based (external assumption)
        self.is_parent = None
        self.is_full_parent = None
        self.is_trailer = None # assigned during setup
        self.variants = None
        self.manufacturer = None
        self.lore_model = None
        self.page = None
        self.is_burnt = True if "Burnt" in self.vehicle_id else False
        self.is_smashed = True if "Smashed" in self.vehicle_id else False
        self.vehicle_type = None
        self.has_siren = None
        self.recipes = None

        self.setup_vehicle()
    
    def __getitem__(self, key):
        """Allows 'vehicle["DisplayName"]'"""
        return self.data[key]
    
    def __contains__(self, key):
        """Allows 'in' checks. e.g. '"EvolvedRecipe" in vehicle'"""
        return key in self.data
    
    def __repr__(self):
        """Overview of the vehicle when called directly: Vehicle(vehicle_id)"""
        name = self.get_name()
        vehicle_parent = self.parent_id
        source = fr"{self.get_path()}"

        return (f'<Vehicle: {name} ({self.vehicle_id}) — {vehicle_parent}, "{source}">')
    
    @classmethod
    def all(cls):
        """Return all vehicles as a dictionary of {vehicle_id: Vehicle}."""
        if cls._vehicles is None:
            cls._load_vehicles()
        return {vehicle_id: cls(vehicle_id) for vehicle_id in cls._vehicles}
    
    @classmethod
    def keys(cls):
        """Return all vehicle IDs."""
        if cls._vehicles is None:
            cls._load_vehicles()
        return cls._vehicles.keys()

    @classmethod
    def values(cls):
        """Return all vehicle instances."""
        if cls._vehicles is None:
            cls._load_vehicles()
        return (cls(vehicle_id) for vehicle_id in cls._vehicles)
    
    @classmethod
    def count(cls):
        """Return the number of loaded vehicles."""
        if cls._vehicles is None:
            cls._load_vehicles()
        return len(cls._vehicles)
    
    @classmethod
    def get_model_data(cls, model_id):
        """Return model data for a given model_id."""
        if cls._vehicle_models is None:
            cls._load_models()
        return cls._vehicle_models.get(model_id)

    @classmethod
    def fix_vehicle_id(cls, vehicle_id: str) -> str:
        """
        Attempts to fix a partial vehicle_id by assuming the 'Base' module first,
        then falling back to a full search through parsed vehicle data.

        Args:
            vehicle_id (str): Either a full vehicle_id ('Module.Vehicle') or just a vehicle name.

        Returns:
            str: The best-guess full vehicle_id.
        """
        if '.' in vehicle_id:
            return vehicle_id

        base_guess = f"Base.{vehicle_id}"
        if cls._vehicles is None:
            cls._load_vehicles()

        if base_guess in cls._vehicles:
            return base_guess

        # Fallback: full search
        for full_id in cls._vehicles:
            if full_id.endswith(f".{vehicle_id}"):
                return full_id

        logger.write(f"No Vehicle ID found for '{vehicle_id}'")
        return vehicle_id

    @classmethod
    def _load_vehicles(cls):
        """Load vehicle data only once and store in class-level cache."""
        cls._vehicles = script_parser.extract_script_data("vehicle")


    @classmethod
    def _load_models(cls):
        """Load vehicle models and store them in a class-level cache."""
        all_models = script_parser.extract_script_data("model")
        cls._vehicle_models = {}
        for model_id, model_data in all_models.items():
            id_type = model_id.split(".", 1)[1]
            if id_type.startswith("Vehicles_") or id_type.startswith("Vehicle_"):
                cls._vehicle_models[id_type] = model_data


    def setup_vehicle(self):
        """Initialise vehicle values."""
        if self.parent_id is None:
            self.find_parent()
        if self.full_parent_id is None:
            self.find_full_parent()
        if self.is_trailer is None:
            self.find_is_trailer()

    ## ------------------------- Dict-like Methods ------------------------- ##

    def get(self, key: str, default=None):
        """Safely get a value from vehicle data with an optional default."""
        return self.data.get(key, default)

    def keys(self):
        """Return all data keys for this vehicle."""
        return self.data.keys()
    
    ## ------------------------- Core Properties ------------------------- ##
    
    def get_file(self) -> str:
        """Return the source file for this vehicle."""
        return self.data.get("SourceFile")
    
    def get_path(self) -> str:
        """Return the full path of the source file."""
        return get_script_path(self.get_file(), prefer="vehicle")
    
    def get_name(self) -> str:
        """Return the translated name of the vehicle."""
        if self.name is None:
            self.find_name()
        return self.name
    
    def find_name(self) -> str:
        car_name = self.get("carModelName", self.id_type) or self.id_type
        name = Translate.get("IGUI_VehicleName" + car_name, lang_code="en")
        if "Burnt" in car_name:
            unburnt = car_name.replace("Burnt", "")
            unburnt_name = Translate.get("IGUI_VehicleName" + unburnt, lang_code="en")
            if unburnt_name != "IGUI_VehicleName" + unburnt:
                name = unburnt_name
            burnt_template = Translate.get("IGUI_VehicleNameBurntCar", lang_code="en")
            name = burnt_template.replace("%1", name)
        self.name = name

    def find_is_trailer(self) -> None:
        """Determine whether the vehicle is a trailer"""
        if self.id_type.startswith("Trailer"):
            self.is_trailer = True
        else:
            self.is_trailer = False

    def get_parent(self) -> "Vehicle" | None:
        """Return the parent as a Vehicle object, or None if this is the root or unknown."""
        if self.parent_id is None:
            self.find_parent()
        if self.is_parent or self.parent_id == "Unknown":
            return self
        return Vehicle(self.parent_id)

    def find_parent(self) -> None:
        """Finds the parent vehicle, based on the 3D model."""
        VEHICLE_MAP = {
            "Car": "CarNormal",
            "LuxuryCar": "CarLuxury",
            "CarSmall02": "SmallCar02",
            "CarSmall": "SmallCar",
            "NormalCarPolice": "CarNormal",
            "PickUp": "PickUpTruck",
            "Ambulance": "VanAmbulance",
        }
        self.is_parent = False
        self.parent_id = self.get_mesh_id()

        # Remove prefixes/suffixes
        TOKENS = ["Vehicle_", "Vehicles_", "_NoRandom", "_Burnt", "Burnt", "Front", "Rear", "Right", "Left", "Smashed", "Lights"]
        for token in TOKENS:
            self.parent_id = self.parent_id.replace(token, "")

        if self.parent_id in VEHICLE_MAP:
            self.parent_id = VEHICLE_MAP.get(self.parent_id)

        # If it resolves to itself, ignore
        if self.parent_id == self.id_type:
            self.parent_id = self.vehicle_id
            self.is_parent = True
            return None

        # Check if the resolved name exists as a valid Vehicle
        self.parent_id = Vehicle.fix_vehicle_id(self.parent_id)
        
        if self.parent_id not in Vehicle._vehicles:
            echo_warning(f"[{self.vehicle_id}] No vehicle found for '{self.parent_id}'")
            self.parent_id = "Unknown"
            return
        
        if Vehicle(self.parent_id).parent_id != self.parent_id:
            self.parent_id = Vehicle(self.parent_id).parent_id
    
    def get_full_parent(self) -> "Vehicle" | None:
        """Return the full parent as a Vehicle object, or self if this is the root or unknown."""
        if self.full_parent_id is None:
            self.find_full_parent()
        if self.is_full_parent:
            return self
        return Vehicle(self.full_parent_id)

    def find_full_parent(self) -> None:
        """Finds the vehicle type, the parent make/model."""
        TYPE_MAP = {
#            "": "Base.CarLuxury", # Mercia Lang 4000
            "Base.CarTaxi": "Base.CarNormal", # Chevalier Nyala
#            "": "Base.CarStationWagon", # Chevalier Cerise Wagon
            "Base.ModernCar_Martin": "Base.ModernCar", # Dash Elite
#            "": "Base.ModernCar02", # Chevalier Primani
#            "": "Base.OffRoad", # Dash Rancher
#            "": "Base.PickUpVan", # Dash Bulldriver
#            "": "Base.PickUpTruck", # Chevalier D6
#            "": "Base.SUV", # Franklin All-Terrain
#            "": "Base.SmallCar", # Chevalier Dart
#            "": "Base.SmallCar02", # Masterson Horizon
            "Base.SportsCar_ez": "Base.SportsCar", # Chevalier Cossette
#            "": "Base.StepVan", # Chevalier Step Van
#            "": "Base.Trailer", # Trailer
#            "": "Base.TrailerAdvert", # Trailer
#            "": "Base.Trailer_Horsebox", # Horse Trailer
#            "": "Base.Trailer_Livestock", # Livestock Trailer
            "Base.VanAmbulance": "Base.Van", # Franklin Valuline
            "Base.VanRadio": "Base.Van",
            "Base.VanSeats": "Base.Van",
        }
        self.is_full_parent = False
        parent = self.parent_id
        self.full_parent_id = parent if parent not in TYPE_MAP else TYPE_MAP.get(parent)
        
        if self.full_parent_id == self.vehicle_id:
            self.is_full_parent = True

    def get_page(self) -> str:
        """Return the wiki page for this vehicle."""
        if self.page is None:
            self.find_page()
        return self.page

    def find_page(self) -> None:
        parent_id = self.parent_id
        if parent_id is None:
            self.page = self.get_name()
        else:
            self.page = Vehicle(parent_id).get_name()

    def get_variants(self) -> list:
        """Returns a list of vehicle_ids that use this vehicle as their parent."""
        if self.variants is None:
            self.find_variants()
        return self.variants

    def find_variants(self) -> None:
        """Finds and caches all vehicles whose parent matches this vehicle_id."""
        self.variants = []
        for vehicle in Vehicle.values():
            if vehicle.parent_id == self.vehicle_id and vehicle.vehicle_id != self.vehicle_id:
                self.variants.append(vehicle.vehicle_id)

    def get_manufacturer(self) -> str:
        """Returns the vehicles manufacturer"""
        if self.manufacturer is None:
            self.find_manufacturer()
        return self.manufacturer
    
    def get_lore_model(self) -> str:
        """Returns the vehicles lore model"""
        if self.lore_model is None:
            self.find_manufacturer()
        return self.lore_model
    
    def find_manufacturer(self) -> None:
        """Finds and caches the vehicle manufacturer based on the name."""
        parent_id = self.get_full_parent().vehicle_id
        if parent_id is None:
            parent_id = self.vehicle_id
            name = self.get_name()
        else:
            name = Vehicle(parent_id).get_name()
        manufacturer = "Unknown"
        model = name
        for token in Vehicle.MANUFACTURERS:
            if token in name:
                manufacturer = token
                model = name.replace(token, "").strip()
                break
        self.manufacturer = manufacturer
        self.lore_model = model

    def get_mechanic_type(self) -> int:
        """Return the mechanic type ID for this vehicle."""
        return int(self.get("mechanicType", 0))
    
    def get_vehicle_type(self) -> str:
        """Return the translated mechanic type name."""
        if self.vehicle_type is None:
            self.find_vehicle_type()
        return self.vehicle_type

    def find_vehicle_type(self) -> None:
        vehicle_type = str(self.get_mechanic_type())
        self.vehicle_type = Translate.get("IGUI_VehicleType_" + vehicle_type, lang_code="en")

    ## ------------------------- Texture & Model ------------------------- ##

    def get_model(self) -> str:
        """Return the rendered 3D model wiki file name as PNG."""
        return self.model

    def get_mesh_id(self) -> str:
        """Return the internal model ID."""
        if self.mesh_id is None:
            self.mesh_id = self.get("model", {}).get("file")
        return self.mesh_id
    
    def get_mesh_path(self) -> str:
        """Return the file path to the vehicle mesh."""
        if self.mesh_path is None:
            self.find_mesh_path()
        return self.mesh_path

    def find_mesh_path(self) -> None:
        self.mesh_path = Vehicle.get_model_data(self.get_mesh_id()).get("mesh")

    def get_texture_path(self) -> str:
        """Return the texture path for the vehicle skin."""
        return self.get("skin", {}).get("texture")

    ## ------------------------- Properties ------------------------- ##

    def get_car_model_name(self) -> str | None:
        """Return the in-game display name from carModelName, if defined."""
        name = self.get("carModelName")
        if name:
            return Translate.get("IGUI_VehicleName" + name)
        return None

    def get_mass(self) -> float:
        """Return the vehicle mass, defaulting to 800.0."""
        return float(self.get("mass", 800.0))
    
    def get_zombie_type(self) -> list[str]:
        """	Return a list of zombie types allowed to spawn in the vehicle."""
        value = self.get("zombieType")
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return [str(value)]
    
    def get_special_key_ring(self) -> list[str]:
        """Return possible special key ring types defined for the vehicle."""
        value = self.get("specialKeyRing")
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return [str(value)]
    
    def get_special_key_chance(self) -> int:
        """Return the chance percentage of the vehicle spawning with a special key ring."""
        return int(self.get("specialKeyRingChance", 0))
    
    def get_engine_repair_level(self) -> int:
        """Return the engine repair level required."""
        return int(self.get("engineRepairLevel", 0))
    
    def get_player_damage_protection(self) -> float:
        """Return the player damage protection value."""
        return float(self.get("playerDamageProtection", 0.0))
    
    def get_seats(self) -> int:
        """Return the number of seats in the vehicle."""
        return int(self.get("seats", 2))
    
    def get_wheel_friction(self) -> float:
        """Return the vehicle's wheel friction value."""
        return float(self.get("wheelFriction", 800.0))
    
    def get_braking_force(self) -> int | None:
        """Return the vehicle's braking force."""
        return float(self.get("brakingForce", 0.0))
    
    def get_max_speed(self) -> float:
        """Return the vehicle's max speed."""
        return float(self.get("maxSpeed", 20.0))
    
    def get_roll_influence(self) -> float:
        """Return the roll influence value."""
        return float(self.get("rollInfluence", 0.1))
    
    def get_is_small_vehicle(self) -> bool:
        """Return whether the vehicle is small."""
        return self.get("isSmallVehicle", True)
    
    def get_stopping_movement_force(self) -> float:
        """Return the stopping force applied when idle."""
        return float(self.get("stoppingMovementForce", 1.0))
    
    def get_animal_trailer_size(self) -> float:
        """Return the trailer's animal capacity."""
        return float(self.get("animalTrailerSize", 0.0))
    
    def get_attachments(self) -> list[str]:
        """Return the attachment points available."""
        return list(self.get("attachment", {}).keys())
    
    def get_offroad_efficiency(self) -> float:
        """Return the offroad driving efficiency."""
        return float(self.get("offroadEfficiency", 1.0))
    
    def get_has_siren(self) -> bool:
        """Return whether the vehicle has a siren."""
        if self.has_siren is None:
            self.find_has_siren()
        return self.has_siren

    def find_has_siren(self) -> bool:
        """Detect if the vehicle has a lightbar siren."""
        has_siren = self.get("lightbar", {}).get("soundSiren")
        if has_siren:
            self.has_siren = True
        else:
            self.has_siren = False
    
    # ---- Health ---- #
    def get_front_end_health(self) -> int:
        """Return the vehicle's front-end health."""
        return int(self.get("frontEndHealth", 100))
    
    def get_rear_end_health(self) -> int:
        """Return the vehicle's rear-end health."""
        return int(self.get("rearEndHealth", 100))
    
    # ---- Engine ---- #
    def get_engine_force(self) -> float:
        """Return the engine force."""
        return float(self.get("engineForce", 3000.0))
    
    def get_engine_quality(self) -> int:
        """Return the engine quality."""
        return int(self.get("engineQuality", 100))
    
    def get_engine_loudness(self) -> int:
        """Return how loud the engine is."""
        return int(self.get("engineLoudness", 100))
    
    def get_engine_rpm_type(self) -> str:
        """Return the engine RPM type."""
        return str(self.get("engineRPMType", "jeep"))
    
    # ---- Steering ---- #
    def get_steering_increment(self) -> float:
        """Return how fast the steering changes."""
        return float(self.get("steeringIncrement", 0.04))
    
    def get_steering_clamp(self) -> float:
        """Return the steering limit angle."""
        return float(self.get("steeringClamp", 0.9))
    
    # ---- Suspension ---- #
    def get_suspension_stiffness(self) -> float:
        """Return the suspension stiffness."""
        return float(self.get("suspensionStiffness", 20.0))
    
    def get_suspension_compression(self) -> float:
        """Return the suspension compression rate."""
        return float(self.get("suspensionCompression", 4.4))
    
    def get_suspension_damping(self) -> float:
        """Return the suspension damping rate."""
        return float(self.get("suspensionDamping", 2.3))
    
    def get_max_suspension_travel_cm(self) -> int:
        """Return the max suspension travel in cm."""
        return float(self.get("maxSuspensionTravelCm", 500.0))
    
    def get_suspension_rest_length(self) -> float:
        """Return the rest length of the suspension."""
        return float(self.get("suspensionRestLength", 0.6))

    # ---- Parts ---- #
    def get_parts_data(self) -> dict:
        """Return the raw parts data dictionary."""
        return self.get("part", {})

    def get_parts(self) -> list[str]:
        """Return a list of part names."""
        return list(self.get("part", {}).keys())
    
    def get_part(self, part) -> dict | None:
        """Return part data, allowing fuzzy lookup with '*'."""
        parts_data = self.get_parts_data()
        if part in parts_data:
            data = parts_data[part]
            return data
        elif part + "*" in parts_data:
            data = parts_data[part + "*"]
            return data
        else:
            echo_warning(f"Part '{part}' couldn't be found for '{self.vehicle_id}'.")
            return None

    def get_part_table(self, part: str) -> dict | None:
        """Return the part table if present, or the base data."""
        parts_data = self.get_parts_data()

        data = parts_data.get(part) or parts_data.get(part + "*")

        if data is not None:
            # Return just "table" if it exists
            return data["table"] if "table" in data else data

        echo_warning(f"Part '{part}' couldn't be found for '{self.vehicle_id}'.")
        return None
    
    def get_part_install(self, part: str) -> dict | None:
        """Return install data for a given part."""
        part_data = self.get_part_table(part)
        return part_data.get("install", {})
    
    def get_part_uninstall(self, part: str) -> dict | None:
        """Return uninstall data for a given part."""
        part_data = self.get_part_table(part)
        return part_data.get("uninstall", {})
    
    def get_recipes(self) -> list[str]:
        """Return recipes that need to be known to remove parts."""
        if self.recipes is None:
            self.find_part_recipe()
        return self.recipes
    
    def find_part_recipe(self) -> None:
        """Find and cache install/uninstall recipes from parts."""
        parts_data = self.get_parts_data()
        recipes_set = set()

        for part_name, part_info in parts_data.items():
            # Get the install/uninstall recipe paths
            table = part_info.get("table", part_info)
            install = table.get("install", {})
            uninstall = table.get("uninstall", {})
            recipe_install = install.get("recipes")
            recipe_uninstall = uninstall.get("recipes")

            if recipe_install is None and recipe_uninstall is None:
                continue
            if recipe_install:
                recipes_set.add(recipe_install)
            if recipe_uninstall:
                recipes_set.add(recipe_uninstall)

        self.recipes = list(recipes_set) if len(recipes_set) == 1 else []


if __name__ == "__main__":
    vehicles = Vehicle.all()
    vehicle_mesh_data = {}
    for vehicle, vehicle_data in vehicles.items():
        vehicle_mesh_data[vehicle] = {}
        vehicle_mesh_data[vehicle]["mesh"] = Vehicle(vehicle).get_mesh_path()
        vehicle_mesh_data[vehicle]["texture"] = Vehicle(vehicle).get_texture_path()
    path = "output/output.json"
    save_json(path, vehicle_mesh_data)
    print(f"JSON file saved to '{path}'")
