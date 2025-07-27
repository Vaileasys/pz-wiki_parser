import os
from scripts.utils import lua_helper, util, echo
from scripts.core.language import Translate
from scripts.core.cache import save_cache, load_cache
from scripts.core.constants import DATA_DIR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.objects.item import Item
    from scripts.objects.animal import Animal, AnimalBreed

class AnimalPart:
    _raw_data: dict = None
    _meat_data: dict = None
    _animals_data: dict = None
    _instances = {}
    _data_file = "parsed_animal_parts_data.json"

    def __new__(cls, parts_id: str):
        """Ensures only one part instance exists per parts ID."""
        if not cls._animals_data:
            cls.load()

        if parts_id in cls._instances:
            return cls._instances[parts_id]

        instance = super().__new__(cls)
        cls._instances[parts_id] = instance
        return instance

    def __init__(self, parts_id: str):
        """Initialise the part instance with its data if not already initialised."""
        if hasattr(self, 'animal_id'):
            return

        if AnimalPart._animals_data is None:
           AnimalPart.load()

        self.parts_id = parts_id
        self._data = self._animals_data.get(parts_id, {})

    @staticmethod
    def _convert_meat_variants(raw_data: dict, prefix: str = "IGUI_AnimalMeat_") -> None:
        """Convert variants list to dict using 'extraName' with prefix stripped as keys."""
        for category in raw_data.values():
            for item_data in category.values():
                variants = item_data.get("variants", [])
                if isinstance(variants, list):
                    variant_dict = {}
                    for variant in variants:
                        extra_name = variant.get("extraName")
                        if extra_name and extra_name.startswith(prefix):
                            key = extra_name.removeprefix(prefix)
                            variant_dict[key] = variant
                    item_data["variants"] = variant_dict

    @staticmethod
    def _split_commas(obj):
        """Recursively split strings with commas into lists."""
        if isinstance(obj, dict):
            return {k: AnimalPart._split_commas(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [AnimalPart._split_commas(v) for v in obj]
        elif isinstance(obj, str) and "," in obj:
            return [s.strip() for s in obj.split(",")]
        return obj

    @classmethod
    def _parse(cls):

        lua_runtime = lua_helper.load_lua_file("AnimalPartsDefinitions.lua")
        parsed_data = lua_helper.parse_lua_tables(lua_runtime)

        cls._raw_data:dict = parsed_data.get("AnimalPartsDefinitions")

        # Split any values separated by a comma into a list
        cls._raw_data = cls._split_commas(cls._raw_data)

        # Convert list of variants to dict
        cls._convert_meat_variants(cls._raw_data)

        save_cache(cls._raw_data, cls._data_file)

        return cls._raw_data


    @classmethod
    def load(cls, attribute: str = None):
        """
        Loads animal part data from the cache, re-parsing the Lua file if outdated.

        Args:
            attribute (str, optional): The name of a specific class attribute to return,
                                    such as "_meat_data" or "_animals_data".

        Returns:
            dict: The full animal data by default, or the specified attribute if provided.
        """
        from scripts.core.version import Version
        if cls._raw_data is None:
            path = os.path.join(DATA_DIR, cls._data_file)

            data, version = load_cache(path, cache_name="animal parts", get_version=True)

            # Re-parse if outdated
            if version != Version.get():
                data = cls._parse()

            cls._raw_data = data
            cls._meat_data = cls._raw_data.get("meat")
            cls._animals_data = cls._raw_data.get("animals")
        
        if attribute is not None and hasattr(cls, attribute):
            return getattr(cls, attribute)

        return cls._animals_data
    
    @classmethod
    def all(cls) -> dict[str, "AnimalPart"]:
        """
        Returns all known animal part instances.

        Returns:
            dict[str, AnimalPart]: Mapping of breed ID to animal part instance.
        """
        if not cls._animals_data:
            cls.load()
        return {id: cls(id) for id in cls._animals_data}
    
    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of Animal types parsed.

        Returns:
            int: Number of unique Animal types.
        """
        if not cls._animals_data:
            cls.load()
        return len(cls._animals_data)
    
    @classmethod
    def exists(cls, animal_id: str) -> bool:
        """
        Checks if a Animal with the given id exists in the parsed data.

        Returns:
            bool: True if found, False otherwise.
        """
        if not cls._animals_data:
            cls.load()
        return animal_id in cls._animals_data
    
    @classmethod
    def get_breeds(cls, item_id: str) -> "list[AnimalBreed]":
        breeds = []
        for part_id, parts in cls.all().items():
            if item_id in parts.all_parts:
                breeds.append(parts.breed)
        
        return breeds
    
    def get(self, key: str, default=None):
        """
        Returns a raw value from the animal part data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)

    @property
    def is_valid(self) -> bool:
        return self.parts_id in AnimalPart._animals_data

    @property
    def data(self) -> dict:
        return self._data
    
    @property
    def skull(self) -> "Item | None":
        from scripts.objects.item import Item
        item = Item(self.get("skull"))
        return item if item.valid else None
    
    @property
    def leather(self) -> "Item | None":
        from scripts.objects.item import Item
        item = Item(self.get("leather"))
        return item if item.valid else None
    
    @property
    def head(self) -> "Item | None":
        from scripts.objects.item import Item
        item = Item(self.get("head"))
        return item if item.valid else None
    
    @property
    def parts(self) -> dict[dict[str, str|int]]:
        return self.get("parts", {})
    
    @property
    def part_items(self) -> list[str]:
        if not hasattr(self, "_parts_items"):
            self._parts_items = []
            for item in self.parts:
                self._parts_items.append(item.get("item"))
        return self._parts_items
    
    @property
    def bones(self) -> dict[dict[str, str|int]]:
        return self.get("bones", {})
    
    @property
    def bone_items(self) -> list[str]:
        if not hasattr(self, "_bone_items"):
            self._bone_items = []
            for item in self.bones:
                self._bone_items.append(item.get("item"))
        return self._bone_items
    
    @property
    def no_skeleton(self) -> bool:
        return self.get("noSkeleton", False)
    
    @property
    def all_parts(self) -> list[str]:
        if not hasattr(self, "_all_parts"):
            parts = set()
            for part, value in self.data.items():
                if isinstance(value, str):
                    parts.add(value)
                elif isinstance(value, list):
                    for item in value:
                        item_id = item.get("item")
                        if item_id:
                            parts.add(item_id)
            self._all_parts = list(parts)

        return self._all_parts
    
    @property
    def animal(self) -> "Animal":
        from scripts.objects.animal import Animal
        if not hasattr(self, "_animal"):
            for _, animal in Animal.all().items():
                for breed in animal.breeds:
                    if self.parts_id == breed.parts_id:
                        self._animal = animal
                        self._breed = breed
        return self._animal
    
    @property
    def breed(self) -> "AnimalBreed":
        if not hasattr(self, "_breed"):
            self.animal # Runs the animal property which populates self._breed
        return self._breed

    def __repr__(self):
        return f"<AnimalPart {self.parts_id}>"


class AnimalMeat:
    _meat_data: dict = AnimalPart.load("_meat_data")
    _instances = {}

    def __new__(cls, item_id: str):
        """Ensures only one meat instance exists per item ID."""
        if item_id in cls._instances:
            return cls._instances[item_id]

        instance = super().__new__(cls)
        cls._instances[item_id] = instance
        return instance

    def __init__(self, item_id: str):
        """Initialise the meat instance with its data if not already initialised."""
        if hasattr(self, 'item_id'):
            return

        self.item_id = item_id
        self._data = self._meat_data.get(item_id, {})

    @classmethod
    def all(cls) -> dict[str, "AnimalPart"]:
        """
        Returns all known meat instances.

        Returns:
            dict[str, AnimalMeat]: Mapping of meat to animal part instance.
        """
        return {id: cls(id) for id in cls._meat_data}
    
    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of Animal types parsed.

        Returns:
            int: Number of unique Animal types.
        """
        return len(cls._meat_data)
    
    @classmethod
    def exists(cls, animal_id: str) -> bool:
        """
        Checks if a Animal with the given id exists in the parsed data.

        Returns:
            bool: True if found, False otherwise.
        """
        return animal_id in cls._meat_data
    
    def get(self, key: str, default=None):
        """
        Returns a raw value from the animal part data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)

    def get_display_name(self, cut: "AnimalMeatVariant") -> int:
        """Returns the display name for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'"""
        return f"{self.get_base_name(cut)} {self.get_extra_name(cut)}"

    def get_base_name(self, cut: "AnimalMeatVariant") -> str:
        """Returns the base name for a specific cut, translating it. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'"""
        return Translate.get(cut.base_name, default=cut.type)

    def get_extra_name(self, cut: "AnimalMeatVariant") -> str:
        """Returns the extra name for a specific cut, translating it. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'"""
        return Translate.get(cut.extra_name, default=cut)

    def get_link(self, cut: "AnimalMeatVariant") -> str:
        """Returns the wiki link for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'"""
        return util.link(self.item.page, self.get_display_name(cut))

    def get_base_chance(self, cut: "AnimalMeatVariant") -> int:
        """Returns the base chance for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'"""
        return cut.base_chance

    def get_hunger_boost(self, cut: "AnimalMeatVariant") -> int:
        """Returns the hunger boost for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'"""
        return cut.hunger_boost

    def get_hunger(self, cut: "AnimalMeatVariant") -> int:
        """Returns the base hunger for a specific cut. E.g., 'PrimeCut', 'MediumCut', 'PoorCut'"""
        return self.item.hunger_change * self.get_hunger_boost(cut)


    @property
    def is_valid(self) -> bool: return self.item_id in AnimalPart._meat_data
    @property
    def data(self) -> dict: return self._data
    @property
    def variants(self) -> list["AnimalMeatVariant"]:
        return [
            AnimalMeatVariant(cut, data)
            for cut, data in self.get("variants", {}).items()
        ]
    
    @property
    def item(self) -> "Item":
        from scripts.objects.item import Item
        return Item(self.item_id)

    @property
    def name_prime(self) -> str: return self.get_display_name("PrimeCut")
    @property
    def name_medium(self) -> str: return self.get_display_name("MediumCut")
    @property
    def name_poor(self) -> str: return self.get_display_name("PoorCut")
    
    @property
    def base_name_prime(self) -> str: return self.get_base_name("PrimeCut")
    @property
    def base_name_medium(self) -> str: return self.get_base_name("MediumCut")
    @property
    def base_name_poor(self) -> str: return self.get_base_name("PoorCut")

    @property
    def extra_name_prime(self) -> str: return self.get_extra_name("PrimeCut")
    @property
    def extra_name_medium(self) -> str: return self.get_extra_name("MediumCut")
    @property
    def extra_name_poor(self) -> str: return self.get_extra_name("PoorCut")

    # These are the base hunger, and is not guaranteed. More common to get less than this value.
    # This can go up or down based on animal stats (size, meat ratio) and how it's obtained (e.g., from ground).
    @property
    def hunger_prime(self) -> str: return self.get_hunger("PrimeCut")
    @property
    def hunger_medium(self) -> str: return self.get_hunger("MediumCut")
    @property
    def hunger_poor(self) -> str: return self.get_hunger("PoorCut")

    @property
    def animals(self) -> list[str]:
        if not hasattr(self, "_animals"):
            animals = set()
            for parts_id, animal_parts in AnimalPart.all().items():
                for part in animal_parts.parts:
                    if self.item_id == part.get("item"):
                        animals.add(parts_id)
            
            self._animals = list(animals)
        return self._animals
    
    def __repr__(self):
        return f"<AnimalMeat {self.item_id}>"


class AnimalMeatVariant:
    def __init__(self, cut_type: str, data: dict):
        self.type = cut_type
        self.data = data
    
    @property
    def base_chance(self) -> int: return self.data.get("baseChance", 100)
    @property
    def extra_name(self) -> int: return self.data.get("extraName")
    @property
    def hunger_boost(self) -> int: return self.data.get("hungerBoost", 1)
    @property
    def base_name(self) -> int: return self.data.get("baseName")
    @property
    def item(self) -> "Item":
        from scripts.objects.item import Item
        return Item(self.data.get("item"))
    @property
    def name(self) -> str:
        from scripts.core.language import Translate
        return f"{Translate.get(self.base_name)} {Translate.get(self.extra_name)}"
    @property
    def wiki_link(self) -> str:
        return util.link(self.item.page, self.name)
    
    def __repr__(self):
        return f"<AnimalMeatVariant {self.type}>"




if __name__ == "__main__":

    ## ---------- AnimalPart ---------- ##

    # Initialise the animal part
    animal_part = AnimalPart("lambfriesian")
    
    # Get an animal or breed from the animal part
    animal = animal_part.animal
    breed = animal_part.breed
    print(f"Animal: {animal.name}")
    print(f"Breed: {breed.breed_name}")

    # Get all animal part item IDs
    print("Items:")
    for part in animal_part.all_parts:
        print("  " + part)

    ## ---------- AnimalMeat ---------- ##

    # Initialise the animal meat using an item ID
    meat = AnimalMeat("Base.Steak")

    # Get the full name of a specific cut
    print(f"\nMeat: {meat.name_prime}") # can also use `meat.get_display_name(cut)` where `cut` is something like "PrimeCut"

    # Get all `part_id` with this meat (`part_id` is `animal_id + breed_id`)
    print("Animals:")
    for part_id in meat.animals:
        print("  " + part_id)
    
    # From that we can get the animal_part
    animal_part = AnimalPart(part_id)
    # Then loop back to the animal and breed (as above)
    animal = animal_part.animal
    breed = animal_part.breed
    
