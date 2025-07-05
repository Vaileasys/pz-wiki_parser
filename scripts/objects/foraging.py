import os
from scripts.core.cache import load_cache
from scripts.core.constants import DATA_DIR
from scripts.parser import distribution_parser
from scripts.objects.item import Item
from scripts.utils import util

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

    def _translate_month(self, month: int):
        from scripts.core.language import Translate
        return Translate.get(f"Sandbox_StartMonth_option{month}")

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
    def skill(self) -> int:
        return self._data.get("skill", 0)

    @property
    def xp(self) -> int:
        return self._data.get("xp", 1)

    @property
    def perks(self) -> list[str]:
        return self._data.get("perks", ["PlantScavenging"])

    @property
    def zones(self) -> dict:
        zones_default = {
            "Forest": 1,
            "DeepForest": 1,
            "Vegitation": 1,
            "FarmLand": 1,
            "Farm": 1,
            "TrailerPark": 1,
            "TownZone": 1,
            "Nav": 1,
            "ForagingNav": 1
        }
        return self._data.get("zones", zones_default)

    @property
    def categories(self) -> list[str]:
        if not hasattr(self, "_categories"):
            raw = self._data.get("categories", {"1": "Junk"})
            self._categories = list(raw.values()) if isinstance(raw, dict) else []
        return self._categories

    @property
    def min_count(self) -> int:
        return self._data.get("minCount", 1)

    @property
    def max_count(self) -> int:
        return self._data.get("maxCount", 1)
    
    @property
    def spawn_funcs(self) -> dict:
        return self._data.get("spawnFuncs", {})

    def _get_month_links(self, months):
        month_links = []

        for month in months:
            if month in (12, 1, 2):
                anchor = "Winter"
            elif month in (3, 4, 5):
                anchor = "Spring"
            elif month in (6, 7, 8):
                anchor = "Summer"
            elif month in (9, 10, 11):
                anchor = "Autumn"
            else:
                anchor = "Seasons"
        
            month_links.append(util.link("Weather", self._translate_month(month), anchor=anchor))

        return month_links

    @property
    def months_raw(self) -> list[int]:
        if not hasattr(self, "_months_raw"):
            raw = self._data.get("months")
            values = raw.values() if isinstance(raw, dict) else [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            self._months_raw = sorted(set(values))
        return self._months_raw

    @property
    def months(self) -> list[int]:
        return self._get_month_links(self.months_raw)

    @property
    def bonus_months_raw(self) -> list[int]:
        if not hasattr(self, "_bonus_months_raw"):
            raw = self._data.get("bonsuMonths", {})
            values = raw.values() if isinstance(raw, dict) else []
            self._bonus_months_raw = sorted(set(values))
        return self._bonus_months_raw

    @property
    def bonus_months(self) -> list[int]:
        return self._get_month_links(self.bonus_months_raw)

    @property
    def malus_months_raw(self) -> list[int]:
        if not hasattr(self, "_malus_months_raw"):
            raw = self._data.get("malusMonths", {})
            values = raw.values() if isinstance(raw, dict) else []
            self._malus_months_raw = sorted(set(values))
        return self._malus_months_raw

    @property
    def malus_months(self) -> list[int]:
        return self._get_month_links(self.malus_months_raw)

    @property
    def day_chance(self) -> int:
        return self._data.get("dayChance", 0)

    @property
    def night_chance(self) -> int:
        return self._data.get("nightChance", 0)

    @property
    def snow_chance(self) -> int:
        return self._data.get("snowChance", 0)

    @property
    def rain_chance(self) -> int:
        return self._data.get("rainChance", 0)

    @property
    def item_size_modifier(self) -> float:
        return self._data.get("itemSizeModifier", 0.0)

    @property
    def is_item_override_size(self) -> bool:
        return self._data.get("isItemOverrideSize", False)

    @property
    def force_outside(self) -> bool:
        return self._data.get("forceOutside", True)

    @property
    def can_be_above_floor(self) -> bool:
        return self._data.get("canBeAboveFloor", False)

    @property
    def poison_chance(self) -> int:
        return self._data.get("poisonChance", 0)

    @property
    def poison_power_min(self) -> int:
        return self._data.get("poisonPowerMin", 0)

    @property
    def poison_power_max(self) -> int:
        return self._data.get("poisonPowerMax", 0)

    @property
    def poison_detection_level(self) -> int:
        return self._data.get("poisonDetectionLevel", 0)

    @property
    def alt_world_texture(self) -> str | None:
        return self._data.get("altWorldTexture")

    def __repr__(self) -> str:
        return f"<Foraging {self._id}>"