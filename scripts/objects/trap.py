from scripts.core.cache import load_cache, save_cache
from scripts.objects.item import Item
from scripts.utils import lua_helper, echo
from scripts.core.version import Version
from scripts.core.language import Language

class Trap(Item):
    """
    Subclass of Item for traps. Adds trap-specific data from TrapDefinition.lua.
    """

    _trap_definitions = None  # class-level cache

    @classmethod
    def _load_trap_definitions(cls):
        if cls._trap_definitions is not None:
            return cls._trap_definitions

        RAW_CACHE_FILE = "trap_definitions_raw.json"
        TRAP_CACHE_FILE = "trap_definitions.json"
        CACHE_LABEL = "trap definitions"

        raw_data, cache_version = load_cache(RAW_CACHE_FILE, CACHE_LABEL, get_version=True, suppress=True)

        # Regenerate raw data if missing or out of date
        if cache_version != Version.get() or not raw_data:
            lua_runtime = lua_helper.load_lua_file("TrapDefinition.lua")
            raw_data = lua_helper.parse_lua_tables(lua_runtime)
            save_cache(raw_data, RAW_CACHE_FILE)

        trap_definitions = {
            trap.get("type"): trap
            for trap in raw_data.get("Traps", [])
            if "type" in trap
        }

        save_cache(trap_definitions, TRAP_CACHE_FILE)
        cls._trap_definitions = trap_definitions
        return cls._trap_definitions

    @classmethod
    def from_item(cls, item: Item) -> "Item | Trap":
        return cls(item) if item.trap else item
        

    def __init__(self, item: Item):
        self._item = item
        self._trap_data = self._load_trap_definitions().get(item.item_id, {})

    def __getattr__(self, name):
        return getattr(self._item, name)
    
    def get_sprite(self, sprite=None, dim="32x32px"):
        if sprite is None:
            sprite = self.sprite
        elif hasattr(self, sprite):
            sprite = getattr(self, sprite)
        
        return f"[[File:{sprite}.png|{dim}|link={self.page}{Language.get_subpage()}|{self.name}]]"

    @property
    def trap_strength(self) -> int | None:
        return self._trap_data.get("trapStrength")

    @property
    def destroy_items(self) -> list[str]:
        destroy = self._trap_data.get("destroyItem", [])
        return destroy if isinstance(destroy, list) else [destroy]

    @property
    def sprite(self) -> str | None:
        return self._trap_data.get("sprite")

    @property
    def closed_sprite(self) -> str | None:
        return self._trap_data.get("closedSprite")

    @property
    def north_sprite(self) -> str | None:
        return self._trap_data.get("northSprite")

    @property
    def north_closed_sprite(self) -> str | None:
        return self._trap_data.get("northClosedSprite")

    @property
    def trap_data(self) -> dict:
        return self._trap_data
    
    @property
    def animals(self) -> dict[str, "TrapAnimal"]:
        return {
            animal.type: animal
            for animal in TrapAnimal.all().values()
            if self.item_id in animal.traps
        }

    @property
    def animal_items(self) -> list[Item]:
        return [animal.item for animal in self.animals]

    @property
    def animal_chances(self) -> dict[str, int]:
        return {
            animal.type: animal.traps[self.item_id]
            for animal in TrapAnimal.all().values()
            if self.item_id in animal.traps
        }


class TrapAnimal:
    _animal_trap_definitions = None

    @classmethod
    def _load_animal_definitions(cls):
        if cls._animal_trap_definitions is not None:
            return cls._animal_trap_definitions

        RAW_CACHE_FILE = "trap_definitions_raw.json"
        CACHE_FILE = "animal_trap_definitions.json"
        CACHE_LABEL = "animal trap definitions"

        raw_data, cache_version = load_cache(RAW_CACHE_FILE, CACHE_LABEL, get_version=True, suppress=True)

        # Regenerate raw data if missing or out of date
        if cache_version != Version.get() or not raw_data:
            lua_runtime = lua_helper.load_lua_file("TrapDefinition.lua")
            raw_data = lua_helper.parse_lua_tables(lua_runtime)
            save_cache(raw_data, RAW_CACHE_FILE)

        animal_definitions = {
            animal["type"]: animal
            for animal in raw_data.get("TrapAnimals", [])
            if "type" in animal
        }

        save_cache(animal_definitions, CACHE_FILE)
        cls._animal_trap_definitions = animal_definitions
        return cls._animal_trap_definitions

    @classmethod
    def all(cls) -> dict[str, "TrapAnimal"]:
        return {
            animal_type: cls(animal_type)
            for animal_type in cls._load_animal_definitions().keys()
        }

    def __init__(self, animal_type: str):
        self._animal_type = animal_type
        self._data = self._load_animal_definitions().get(animal_type, {})

    @property
    def animal_data(self) -> dict:
        return self._data

    @property
    def type(self) -> str:
        return self._data.get("type")

    @property
    def item(self) -> Item:
        return Item(self._data.get("item"))

    @property
    def traps(self) -> dict[str, int]:
        return self._data.get("traps", {})

    @property
    def baits(self) -> dict[str, int]:
        return self._data.get("baits", {})

    @property
    def zone(self) -> dict[str, int]:
        return self._data.get("zone", {})

    @property
    def min_size(self) -> int | None:
        return self._data.get("minSize")

    @property
    def max_size(self) -> int | None:
        return self._data.get("maxSize")

    @property
    def min_hour(self) -> int | None:
        return self._data.get("minHour")

    @property
    def max_hour(self) -> int | None:
        return self._data.get("maxHour")

    @property
    def can_be_alive(self) -> bool:
        return self._data.get("canBeAlive", False)

    @property
    def alive_animals(self) -> list[str]:
        return self._data.get("aliveAnimals", [])

    @property
    def alive_breed(self) -> list[str]:
        return self._data.get("aliveBreed", [])

    @property
    def strength(self) -> int | None:
        return self._data.get("strength")
