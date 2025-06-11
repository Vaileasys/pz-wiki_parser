"""
Provides access to parsed "fixing" data from Project Zomboid scripts.

This module defines the `Fixing` class, which represents a repair recipe.
It includes logic for resolving fixing entries based on item IDs, loading fixer data, and exposing relevant
attributes like required items, condition modifiers, and skill requirements.

Classes:
    - Fixing: Represents a fixing definition, including required items and fixers.
    - GlobalItem: Represents a global item required across all fixer attempts.
    - Fixer: Represents a fixer item and its associated skill requirements.
"""

from scripts.parser import script_parser
from scripts.core.file_loading import get_script_path
from scripts.objects.item import Item
from scripts.objects.skill import Skill


class Fixing:
    """
    Represents a fixing entry for an item, containing data about how it can be repaired.

    This class lazily loads all fixing definitions from parsed script data and provides
    a caching mechanism to avoid duplicate instances. A Fixing object can be accessed using
    either a fixing ID, item ID or Item object.

    Properties:
        - fixing_id (str): The internal ID of the fixing.
        - valid (bool): Whether the fixing entry contains valid data.
        - script_type (str): Optional script type associated with the fixing.
        - file (str): The script file name where the fixing is defined.
        - path (str): The resolved file path for the fixing source.
        - module (str): The module prefix of the fixing ID.
        - id_type (str): The item identifier portion of the fixing ID.
        - requires (list[Item]): List of required items for the fix.
        - condition_modifier (float): Modifier applied to the item’s condition after repair.
        - global_items (list[GlobalItem]): Shared global items required by the fixing.
        - fixers (list[Fixer]): Fixer items, with optional skill requirements.
    """
    _fixings = None
    _instances = {}

    @classmethod
    def _load_fixings(cls):
        """Load and cache all fixing data from script files if not already loaded."""
        cls._fixings = script_parser.extract_script_data("fixing")

    @classmethod
    def all(cls):
        """Return a dictionary of all fixings, mapped by their fixing ID."""
        if cls._fixings is None:
            cls._load_fixings()
        return {fixing_id: cls(fixing_id) for fixing_id in cls._fixings}

    @classmethod
    def keys(cls):
        """Return an iterable of all available fixing IDs."""
        if cls._fixings is None:
            cls._load_fixings()
        return cls._fixings.keys()

    @classmethod
    def values(cls):
        """Return a generator of all Fixing instances."""
        if cls._fixings is None:
            cls._load_fixings()
        return (cls(fixing_id) for fixing_id in cls._fixings)
    
    @classmethod
    def count(cls) -> int:
        """Return the number of available fixing definitions."""
        if cls._fixings is None:
            cls._load_fixings()
        return len(cls._fixings)

    @classmethod
    def exists(cls, fixing_id: str) -> bool:
        """Check if a fixing with the given ID exists."""
        if cls._fixings is None:
            cls._load_fixings()
        return fixing_id in cls._fixings

    def __new__(cls, key: str | Item):
        """
        Create or return a cached Fixing instance based on a string ID or Item object.
        Supports matching by fixing ID, item ID, or an Item object.
        """
        if cls._fixings is None:
            cls._load_fixings()

        fixing_id = None

        if isinstance(key, str):
            normalized_key = key.replace(" ", "_")

            if key in cls._fixings:
                fixing_id = key
            elif f"Base.{normalized_key}" in cls._fixings:
                fixing_id = f"Base.{normalized_key}"
            else:
                item = Item(key)
                item_id = item.item_id
                fixing_id = next(
                    (
                        fid
                        for fid, data in cls._fixings.items()
                        if any(Item(req).item_id == item_id for req in data.get("Require", []))
                    ),
                    None
                )
        else:
            # Given an Item object
            item_id = key.item_id
            fixing_id = next(
                (
                    fid
                    for fid, data in cls._fixings.items()
                    if any(Item(req).item_id == item_id for req in data.get("Require", []))
                ),
                None
            )

        # Fallback to using the raw input key if no match found
        if fixing_id is None:
            fixing_id = str(key).replace(" ", "_")

        if fixing_id in cls._instances:
            return cls._instances[fixing_id]

        instance = super().__new__(cls)
        cls._instances[fixing_id] = instance
        instance._resolved_fixing_id = fixing_id
        return instance

    def __init__(self, _: str = None):
        """
        Initialise the Fixing instance with resolved fixing ID.

        Raises:
            RuntimeError: If resolving the fixing ID fails.
        """
        if hasattr(self, "fixing_id"):
            return

        fixing_id = getattr(self, "_resolved_fixing_id", None)
        if fixing_id is None:
            raise RuntimeError("Fixing ID was not set before __init__.")

        self.fixing_id = fixing_id
        self.data = Fixing._fixings.get(fixing_id, {})

        parts = fixing_id.split(".", 1)
        self._module = parts[0]
        self._id_type = parts[1] if len(parts) == 2 else None

    def __getitem__(self, key):
        """Allow dictionary-style access to internal data."""
        return self.data[key]

    def __contains__(self, key):
        """Check if a key exists in the fixing data."""
        return key in self.data

    def __repr__(self):
        """Return a readable string representation of the Fixing instance."""
        return f"<Fixing {self.fixing_id}>"

    def get(self, key: str, default=None):
        """Get a value from the fixing data with an optional default."""
        return self.data.get(key, default)

    @property
    def valid(self) -> bool:
        """Return True if the fixing entry contains valid data."""
        return bool(self.data)

    @property
    def script_type(self) -> str:
        """Return the script type defined for the fixing, if any."""
        return self.data.get("ScriptType")

    @property
    def file(self) -> str:
        """Return the source script file name for the fixing."""
        return self.data.get("SourceFile")

    @property
    def path(self) -> str:
        """Return the resolved file path of the fixing script."""
        return get_script_path(self.file, prefer="fixing")

    @property
    def module(self) -> str:
        """Return the module name (prefix) of the fixing ID."""
        return self._module

    @property
    def id_type(self) -> str:
        """Return the item identifier part of the fixing ID."""
        return self._id_type

    @property
    def requires(self) -> list[Item]:
        """Return a list of required Item objects for this fixing."""
        return [Item(item_id) for item_id in self.data.get("Require", [])]

    @property
    def condition_modifier(self) -> float:
        """Return the condition modifier value for the fixing."""
        return float(self.data.get("ConditionModifier", 1.0))

    @property
    def global_items(self):
        """Return a list of GlobalItem objects required by the fixing."""
        return [
            GlobalItem(item_id, amount)
            for item_id, amount in self.data.get("GlobalItem", {}).items()
        ]

    @property
    def fixers(self):
        """Return a list of Fixer objects that can be used for repair."""
        return [Fixer(item_id, data) for item_id, data in self.data.get("Fixer", {}).items()]


class GlobalItem:
    """
    Represents a global item required across all fixing attempts.

    Properties:
        - item_id (str): The item ID of the required global item.
        - amount (int): Quantity required for the fixing.
        - item (Item): The wrapped `Item` object.
    """
    def __init__(self, item_id: str, amount: int):
        """Initialise a GlobalItem with its ID and required amount."""
        self.item_id = item_id
        self.amount = amount

    def __repr__(self):
        """Return a string representation of the GlobalItem instance."""
        return f"<GlobalItem {self.item_id}>"

    @property
    def item(self):
        """Return the Item object associated with this global item ID."""
        return Item(self.item_id)
    

class Fixer:
    """
    Represents a fixer item used to repair something, with optional skill requirements.

    Properties:
        - item_id (str): The fixer item’s ID.
        - amount (int): Quantity of the fixer required.
        - skill_requirements (dict[str, int]): Required skills and their levels.
        - item (Item): The wrapped `Item` object.
        - skills (list[Skill]): Skill objects required for the fixer.
    """
    def __init__(self, item_id: str, data: dict):
        """Initialise a Fixer with its ID, amount, and skill requirements."""
        self.item_id = item_id
        self.amount:int = data.get("Amount", 1)
        self.skill_requirements:dict[str, int] = data.get("Skill", {})

    def __repr__(self):
        """Return a string representation of the Fixer instance."""
        return f"<Fixer {self.item_id}>"
    
    def get_skill_level(self, skill: Skill | str) -> int:
        """
        Return the required level for the given skill.

        Args:
            skill (Skill | str): The skill object or perk ID to check.

        Returns:
            int: The level required for the given skill, or 0 if not required.
        """
        skill_id = skill.perk_id if isinstance(skill, Skill) else str(skill)
        return self.skill_requirements.get(skill_id, 0)

    @property
    def item(self):
        """Return the Item object associated with this fixer."""
        return Item(self.item_id)

    @property
    def skills(self):
        """Return a list of Skill objects required by this fixer."""
        return [Skill(perk_id) for perk_id in self.skill_requirements]
    

if __name__ == "__main__":
    from scripts.core.language import Language
    Language.get()

    # Some general usage
#    fixing = Fixing("Base.Fix_Trunk_Welding")

#    required_items = fixing.requires
#    print("\nItems")
#    for item in required_items:
#        print(item.wiki_link)
    
#    global_items = fixing.global_items
#    print("\nRequired items")
#    for global_item in global_items:
#        print(f"{global_item.item.wiki_link} {global_item.amount}")

#    fixers = fixing.fixers
#    print("\nFixers")
#    for fixer in fixers:
#        print(f"{fixer.item.wiki_link}")
#        skills = fixer.skills
#        for skill in skills:
#            print(skill.wiki_link + f" {fixer.get_skill_level(skill)}")


    fixing = Fixing("Base.Shotgun")
    print(fixing)
    
    # Possible inputs for the same Fixing instance
    # NOTE: Some items can have multiple fixing recipes, using the item id will only work for the first recipe it encounters
    a = Fixing("Base.Shotgun")
    b = Fixing("Shotgun")
    c = Fixing("Base.Fix_Shotgun")
    d = Fixing("Fix_Shotgun")
    e = Fixing("Fix Shotgun")
    print(a is b and b is c and c is d and d is e) # Will be true if all instances are the same