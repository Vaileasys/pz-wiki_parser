"""
Vehicle part access.

Defines the base VehiclePart class and its many subclasses (e.g. seats, doors, windows),
along with tools for mapping items to parts, resolving install/uninstall data,
and structuring vehicle components for each vehicle definition.

Includes:
- VehiclePart and subclasses for part-specific logic
- VehicleParts manager for handling all parts on a vehicle
- VehiclePartItem for linking items to parts
- PartInstallUninstall helper for install/uninstall requirements
"""
from scripts.utils import util
from scripts.objects.item import Item
from scripts.items.item_tags import Tag
from typing import TYPE_CHECKING

def get_vehicle_part_class(part_name: str) -> type["VehiclePart"]:
    """
    Returns the appropriate VehiclePart subclass based on part name prefix.
    Defaults to VehiclePart.
    """
    if part_name.startswith("Seat"):
        return VehicleSeat
    if part_name.startswith("Tire"):
        return VehicleTire
    if part_name.startswith("GasTank"):
        return VehicleGasTank
    if part_name.startswith("Window") or part_name.startswith("Windshield"):
        return VehicleWindow
    if part_name == "TruckBed":
        return VehicleTruckBed
    #TODO: finish defining classes
    return VehiclePart


class VehiclePartItem(Item):
    """
    Item subclass that links items to vehicle parts.

    Adds access to all parts that use this item, along with install/uninstall data.
    """
    _item_to_parts: dict[str, list["VehiclePart"]] = {}

    ## ------------------------- Class Methods ------------------------- ##

    @classmethod
    def build_item_part_map(cls):
        from scripts.objects.vehicle import Vehicle
        all_vehicles = Vehicle.all()
        cls._item_to_parts.clear()
        for vehicle_id, vehicle in all_vehicles.items():
            for part in vehicle.parts.all():
                for id_ in part.items:
                    cls._item_to_parts.setdefault(id_, []).append(part)

    @classmethod
    def has_part(cls, item_id: str) -> bool:
        if not cls._item_to_parts:
            cls.build_item_part_map()
        return item_id in cls._item_to_parts

    @classmethod
    def from_item(cls, item: "Item") -> "VehiclePartItem":
        """
        Promote the existing Item object to a VehiclePartItem.
        """
        if not cls._item_to_parts:
            cls.build_item_part_map()
        if isinstance(item, cls):
            return item
        item.__class__ = cls
        return item

    ## ------------------------- Properties ------------------------- ##
    @property
    def vehicle_parts(self) -> list["VehiclePart"]:
        return self._item_to_parts.get(self.part_item_id, [])

    @property
    def install(self) -> "PartInstallUninstall | None":
        for p in self.vehicle_parts:
            if p.install:
                return p.install
        return None

    @property
    def uninstall(self) -> "PartInstallUninstall | None":
        for p in self.vehicle_parts:
            if p.uninstall:
                return p.uninstall
        return None


class VehiclePart:
    """
    Base class for a single vehicle part, holding parsed data and common properties
    like install/uninstall info, durability, etc.

    Used as the parent class for more specific part types.
    """
    def __init__(self, part_type: str, vehicle_id: str, data: dict):
        self.part_type = part_type
        self.vehicle_id = vehicle_id
        self.data = data

    @property
    def container(self) -> dict:
        return self.data.get("container", {})

    @property
    def table(self) -> dict:
        return self.data.get("table", {})

    @property
    def install(self) -> "PartInstallUninstall":
        return PartInstallUninstall("install", self.data.get("install", {}) or self.table.get("install", {}))

    @property
    def uninstall(self) -> "PartInstallUninstall":
        return PartInstallUninstall("uninstall", self.data.get("uninstall", {}) or self.table.get("uninstall", {}))

    @property
    def items(self) -> list[str]:
        return self.data.get("itemType", [])
    
    @property
    def mechanic_area(self) -> str | None:
        return self.data.get("mechanicArea")
    
    @property
    def area(self) -> str | None:
        return self.data.get("area")
    
    @property
    def category(self) -> str | None:
        return self.data.get("category")
    
    @property
    def durability(self) -> int:
        return int(self.data.get("durability", 0))
    
    @property
    def mechanic_require_key(self) -> bool:
        return float(self.data.get("mechanicRequireKey", False))

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.part_type} vehicle={self.vehicle_id}>"


class VehicleSeat(VehiclePart):
    @property
    def seat_position(self) -> str | None:
        return self.container.get("seat")

class VehicleDoor(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleTrunkDoor(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleTire(VehiclePart):
    @property
    def wheel(self) -> str| None:
        return self.data.get("wheel")
    
    @property
    def model(self) -> dict:
        return self.data.get("model", {})
    
    @property
    def content_type(self) -> str | None:
        return int(self.data.get("contentType"))
    
class VehicleBrake(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleSuspension(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleEngine(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleBattery(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleMuffler(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleGasTank(VehiclePart):
    @property
    def condition_affects_capacity(self) -> bool:
        return self.container.get("conditionAffectsCapacity", False)
    
    @property
    def content_type(self) -> str | None:
        return int(self.data.get("contentType"))

class VehicleRadio(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleGloveBox(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleWindow(VehiclePart):
    @property
    def parent(self) -> str | None:
        return self.window.get("parent")
    
    @property
    def window(self) -> dict:
        return self.data.get("window", {})

    @property
    def openable(self) -> bool:
        return self.window.get("openable", False)

class VehicleHeadlight(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleTaillight(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleLightbar(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleHeater(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehiclePassengerCompartment(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleEngineDoor(VehiclePart):
    #TODO: fill with part specific methods/properties
    pass

class VehicleTruckBed(VehiclePart):
    @property
    def condition_affects_capacity(self) -> bool:
        return self.container.get("conditionAffectsCapacity", False)
    
    @property
    def capacity(self) -> bool:
        return self.container.get("capacity", False)

#TODO add Trailer Truck Bed


class PartInstallUninstall:
    """Helper class to handle install/uninstall data for vehicle parts."""
    def __init__(self, key: str, data: dict):
        self.type = key
        self.data = data
    
    def get(self, key: str, default=None):
        """Get a value from the install/uninstall data."""
        return self.data.get(key, default)

    @property
    def items(self) -> list[dict]:
        """Convert items dict to a sorted list"""
        items = self.data.get("items", {})
        if isinstance(items, dict):
            try:
                return [items[key] for key in sorted(items, key=int)]
            except ValueError:
                return list(items.values())
        return []
    
    @property
    def formatted_items(self) -> list[str]:
        if not hasattr(self, "_formatted_items"):
            items = []
            objs = self.get_item_objects()
            for obj in objs:
                if isinstance(obj, Tag):
                    items.append(f"{obj.template}{obj.wiki_link}")
                elif isinstance(obj, Item):
                    items.append(f"{obj.icon}{obj.wiki_link}")
            
            self._formatted_items = items
        
        return self._formatted_items

    
    def get_item_objects(self) -> list[Item | Tag]:
        """Convert items list to a list of item/tag objects"""
        if not hasattr(self, "_item_objects"):
            item_objects = set()
            for item_entry in self.items:

                tags = item_entry.get("tags")
                if tags:
                    item_objects.add(Tag(tags))
                
                items = item_entry.get("type")
                if items:
                    item_objects.add(Item(items))

            self._item_objects = list(item_objects)

        return self._item_objects
        

    @property
    def skills(self) -> dict[str, dict]: return self.data.get("skills", {})

    @property
    def traits(self) -> str | None: return self.data.get("traits")

    @property
    def professions(self) -> str | None: return self.data.get("professions")

    @property
    def door(self) -> str | None: return self.data.get("door")

    @property
    def time(self) -> int: return self.data.get("time", [])

    @property
    def recipes(self) -> list[str]: return self.data.get("recipes", [])

    @property
    def require_empty(self) -> bool: return self.data.get("requireEmpty", False)

    @property
    def require_installed(self) -> list[str]: return self.data.get("requireInstalled", [])

    @property
    def require_uninstalled(self) -> list[str]: return self.data.get("requireUninstalled", [])

    @property # lua function
    def test(self) -> str | None: return self.data.get("test")

    @property # lua function
    def complete(self) -> str | None: return self.data.get("complete")


if TYPE_CHECKING:
    from scripts.objects.vehicle import Vehicle

class VehicleParts:
    """
    Holds and processes all parts for a single vehicle, including wildcard merging
    and access to common components like seats, door, etc.
    """

    def __init__(self, parts_raw: dict, vehicle: "Vehicle"):
        self.vehicle = vehicle
        self.vehicle_id = vehicle.vehicle_id
        self._raw = parts_raw
        self._wildcards = {
            k[:-1]: v for k, v in parts_raw.items() if k.endswith("*")
        }
        self._true_parts = {
            k: v for k, v in parts_raw.items() if not k.endswith("*")
        }

        # Cache of all processed parts
        self._parts = {
            name: self._build_part(name, data)
            for name, data in self._true_parts.items()
        }

    def _build_part(self, name: str, data: dict):
        # Apply wildcard defaults
        for prefix, base in self._wildcards.items():
            if name.startswith(prefix):
                data = util.deep_merge(base, data)
                break

        # Use subclass based on name
        cls = get_vehicle_part_class(name)
        return cls(name, self.vehicle_id, data)

    def all(self) -> list[VehiclePart]:
        return list(self._parts.values())

    def get(self, name: str) -> VehiclePart | None:
        return self._parts.get(name)

    def parts_starting_with(self, prefix: str) -> list[VehiclePart]:
        return [p for p in self._parts.values() if p.part_type.startswith(prefix)]

    @property
    def seats(self) -> list[VehicleSeat]:
        return [p for p in self.parts_starting_with("Seat") if isinstance(p, VehicleSeat)]

    @property
    def doors(self) -> list[VehicleDoor]:
        return [p for p in self.parts_starting_with("Door") if isinstance(p, VehicleDoor)]
    
    @property
    def trunk_door(self) -> VehicleTrunkDoor | None:
        return self.get("TrunkDoor")

    @property
    def engine(self) -> VehicleEngine | None:
        return self.get("Engine")

    @property
    def battery(self) -> VehicleBattery | None:
        return self.get("Battery")

    @property
    def muffler(self) -> VehicleMuffler | None:
        return self.get("Muffler")

    @property
    def gas_tank(self) -> VehicleGasTank | None:
        return self.get("GasTank")

    @property
    def heater(self) -> VehicleHeater | None:
        return self.get("Heater")

    @property
    def engine_door(self) -> VehicleEngineDoor | None:
        return self.get("EngineDoor")

    @property
    def lightbar(self) -> VehicleLightbar | None:
        return self.get("lightbar")

    @property
    def passenger_compartment(self) -> VehiclePassengerCompartment | None:
        return self.get("PassengerCompartment")

    @property
    def glove_box(self) -> VehicleGloveBox | None:
        return self.get("GloveBox")

    @property
    def radio(self) -> VehicleRadio | None:
        return self.get("Radio")

    @property
    def truck_bed(self) -> VehicleTruckBed | None:
        return self.get("TruckBed") or self.get("TruckBedOpen")

    @property
    def headlights(self) -> list[VehicleHeadlight]:
        return [p for p in self.parts_starting_with("Headlight") if isinstance(p, VehicleHeadlight)]

    @property
    def taillights(self) -> list[VehicleTaillight]:
        return [p for p in self.parts_starting_with("HeadlightRear") if isinstance(p, VehicleTaillight)]

    @property
    def windows(self) -> list[VehicleWindow]:
        return [p for p in self.parts_starting_with("Window") if isinstance(p, VehicleWindow)]

    @property
    def windshields(self) -> list[VehicleWindow]:
        return [p for p in self.parts_starting_with("Windshield") if isinstance(p, VehicleWindow)]

    @property
    def tires(self) -> list[VehicleTire]:
        return [p for p in self.parts_starting_with("Tire") if isinstance(p, VehicleTire)]

    @property
    def brakes(self) -> list[VehicleBrake]:
        return [p for p in self.parts_starting_with("Brake") if isinstance(p, VehicleBrake)]

    @property
    def suspensions(self) -> list[VehicleSuspension]:
        return [p for p in self.parts_starting_with("Suspension") if isinstance(p, VehicleSuspension)]
