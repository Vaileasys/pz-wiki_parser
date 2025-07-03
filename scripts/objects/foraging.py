import os
from scripts.core.cache import load_cache
from scripts.core.constants import DATA_DIR
from scripts.parser import distribution_parser
from scripts.objects.item import Item

DISTRIBUTIONS_DIR = os.path.join(DATA_DIR, "distributions")
FORAGING_CACHE_FILE = "foraging.json"
FORAGING_CACHE_PATH = os.path.join(DISTRIBUTIONS_DIR, FORAGING_CACHE_FILE)


class Foraging:
    _instances = {}
    _foraging = None

    def __new__(cls, item_id: str):
        if item_id not in cls._instances:
            cls._instances[item_id] = super().__new__(cls)
        return cls._instances[item_id]

    def __init__(self, item_id: str):
        self._id = item_id
        self._data = self.load().get(item_id, {})

    @classmethod
    def load(cls) -> dict:
        """Loads the foraging data from cache, otherwise parses it with the distribution parser."""
        if cls._foraging is not None:
            return cls._foraging

        if not os.path.exists(FORAGING_CACHE_PATH):
            forage_definitions_path = os.path.join("resources", "lua", "forageDefinitions.lua")
            distribution_parser.parse_foraging(forage_definitions_path, DISTRIBUTIONS_DIR)

        cls._foraging = load_cache(FORAGING_CACHE_PATH) or {}
        print(FORAGING_CACHE_PATH)
        return cls._foraging

    @classmethod
    def all(cls) -> dict[str, "Foraging"]:
        """Return all foraging instances as a dictionary of {foraging_id: Item}."""
        return {item_id: cls(item_id) for item_id in cls.load()}
    
    @classmethod
    def items(cls) -> dict[str, "Foraging"]:
        """Return an iterable of (id, instance) pairs."""
        return cls.all().items()
    
    @classmethod
    def exists(cls, foraging_id: str) -> bool:
        """Returns True if the foraging ID exists in the foraging data."""
        return foraging_id in cls.load()
    
    @classmethod
    def count(cls) -> int:
        """Returns the number of foraging entries loaded."""
        return len(cls.load())
    
    def get(self, key: str, default=None):
        """Returns the raw value from this item's foraging data."""
        return self._data.get(key, default)

    def _translate_months(self, months: list):
        from scripts.core.language import Translate
        return [Translate.get(f"Sandbox_StartMonth_option{m}") for m in months]

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def valid(self) -> bool:
        return self.exists(self._id)

    @property
    def type(self) -> str | None:
        return self._data.get("type")

    @property
    def item(self) -> Item | None:
        return Item(self.type) if Item.exists(self.type) else None

    @property
    def skill(self) -> int | None:
        return self._data.get("skill")

    @property
    def xp(self) -> int | None:
        return self._data.get("xp")

    @property
    def zones(self) -> dict | None:
        return self._data.get("zones")

    @property
    def categories(self) -> list[str]:
        if not hasattr(self, "_categories"):
            raw = self._data.get("categories", {})
            self._categories = list(raw.values()) if isinstance(raw, dict) else []
        return self._categories

    @property
    def min_count(self) -> int | None:
        return self._data.get("minCount")

    @property
    def max_count(self) -> int | None:
        return self._data.get("maxCount")
    
    @property
    def spawn_funcs(self) -> dict:
        return self._data.get("spawnFuncs", {})

    @property
    def months(self) -> list[int]:
        raw = self._data.get("months", {})
        return self._translate_months(sorted(set(raw.values()))) if isinstance(raw, dict) else []

    @property
    def bonus_months(self) -> list[int]:
        raw = self._data.get("bonusMonths", {})
        return self._translate_months(sorted(set(raw.values()))) if isinstance(raw, dict) else []

    @property
    def malus_months(self) -> list[int]:
        raw = self._data.get("malusMonths", {})
        return self._translate_months(sorted(set(raw.values()))) if isinstance(raw, dict) else []

    @property
    def day_chance(self) -> int | None:
        return self._data.get("dayChance")

    @property
    def night_chance(self) -> int | None:
        return self._data.get("nightChance")

    @property
    def snow_chance(self) -> int | None:
        return self._data.get("snowChance")

    @property
    def rain_chance(self) -> int | None:
        return self._data.get("rainChance")

    @property
    def item_size_modifier(self) -> float | None:
        return self._data.get("itemSizeModifier")

    @property
    def is_item_override_size(self) -> bool:
        return self._data.get("isItemOverrideSize", False)

    @property
    def force_outside(self) -> bool:
        return self._data.get("forceOutside", False)

    @property
    def can_be_above_floor(self) -> bool:
        return self._data.get("canBeAboveFloor", False)

    @property
    def poison_chance(self) -> int | None:
        return self._data.get("poisonChance")

    @property
    def poison_power_min(self) -> int | None:
        return self._data.get("poisonPowerMin")

    @property
    def poison_power_max(self) -> int | None:
        return self._data.get("poisonPowerMax")

    @property
    def poison_detection_level(self) -> int | None:
        return self._data.get("poisonDetectionLevel")

    @property
    def alt_world_texture(self) -> str | None:
        return self._data.get("altWorldTexture")

    def __repr__(self) -> str:
        return f"<Foraging {self._id}>"