import os
from scripts.objects.profession import Occupation, Trait
from scripts.core.cache import load_cache
from scripts.core.constants import CACHE_DIR
from scripts.parser import distribution_parser
from scripts.objects.item import Item
from scripts.utils import util
from scripts.core.cache import save_cache, load_cache
from scripts.utils.lua_helper import load_lua_file, parse_lua_tables, lua_to_python
from scripts.core.version import Version
from scripts.core.language import Translate

DISTRIBUTIONS_DIR = os.path.join(CACHE_DIR, "distributions")
FORAGING_CACHE_FILE = "foraging.json"
FORAGING_CACHE_PATH = os.path.join(DISTRIBUTIONS_DIR, FORAGING_CACHE_FILE)


class ForagingItem:
    _instances = {}
    _foraging = None

    def __new__(cls, item_id: str):
        if item_id not in cls._instances:
            cls._instances[item_id] = super().__new__(cls)
        return cls._instances[item_id]

    def __init__(self, item_id: str):
        self._id = item_id
        self._data: dict = self.load().get(item_id, {})

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
    def all(cls) -> dict[str, "ForagingItem"]:
        """Return all foraging instances as a dictionary of {foraging_id: Item}."""
        return {item_id: cls(item_id) for item_id in cls.load()}
    
    @classmethod
    def items(cls) -> dict[str, "ForagingItem"]:
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
    
    def has_category(self, *category_ids: str | list[str]) -> bool:
        """
        Check if the foraging item is in any of the given categories.

        Args:
            *category_ids (str | list[str]): One or more category IDs. Can be individual strings or lists of strings.

        Returns:
            bool: True if the item is in at least one of the categories.
        """
        if not self.categories:
            return False

        # Flatten input
        flat_ids = []
        for cid in category_ids:
            if isinstance(cid, list):
                flat_ids.extend(cid)
            else:
                flat_ids.append(cid)

        return any(cid in self.categories for cid in flat_ids)

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
        return f"<ForagingItem {self._id}>"


class ForageCategory:
    _instances = {}
    _categories = None

    def __new__(cls, category: str):
        if category not in cls._instances:
            cls._instances[category] = super().__new__(cls)
        return cls._instances[category]

    def __init__(self, category: str):
        self._id = category
        self._data:dict = self.load().get(category, {})

    @classmethod
    def load(cls) -> dict:
        if cls._categories is None:
            cls._categories = ForageSystem.get_categories()
        return cls._categories

    @classmethod
    def all(cls) -> dict[str, "ForageCategory"]:
        """Return all foraging categories as a dictionary of {category_id: ForageCategory}."""
        return {category_id: cls(category_id) for category_id in cls.load()}
    
    @classmethod
    def count(cls) -> int:
        """Returns the number of foraging categories loaded."""
        return len(cls.load())

    @classmethod
    def exists(cls, category: str) -> bool:
        return category in cls.load()
    
    def get(self, key: str, default=None):
        """Returns the raw value from this category's data."""
        return self._data.get(key, default)

    @property
    def id(self) -> str:
        return self._id

    @property
    def valid(self) -> bool:
        return self.exists(self._id)

    @property
    def type_category(self) -> str | None:
        return self._data.get("typeCategory")
    
    @property
    def name(self) -> str:
        return Translate.get(f"IGUI_SearchMode_Categories_{self.get("name")}", default=util.split_camel_case(self._id))
    
    @property
    def name_en(self) -> str:
        if not hasattr(self, "_name_en"):
            self._name_en = Translate.get(f"IGUI_SearchMode_Categories_{self.get('name')}", lang_code="en", default=util.split_camel_case(self._id))
        return self._name_en
    
    @property
    def page(self) -> str: #dummy for later use if needed
        if not hasattr(self, "_page"):
            self._page = self.name_en
        return self._page
    
    @property
    def wiki_link(self) -> str:
        if not hasattr(self, "_wiki_link"):
            self._wiki_link = util.link(self.page, self.name)
        return self._page

    @property
    def icon_raw(self) -> str:
        return f"pinIcon{self.id}"

    @property
    def icon(self) -> str | None:
        return f"[[File:{self.icon_raw}.png|{self.name}|link={self.name}]]" if self.icon_raw else f"[[File:pinIconUnknown.png|link={self.page}|{self.name}]]"

    @property
    def is_hidden(self) -> bool:
        return self._data.get("categoryHidden", False)

    @property
    def identify_perk(self) -> str | None:
        return self._data.get("identifyCategoryPerk")

    @property
    def identify_level(self) -> str | None:
        return self._data.get("identifyCategoryLevel")

    @property
    def zones(self) -> dict[str, int]:
        return self._data.get("zones", {})
    
    @property
    def traits(self) -> list[Trait]:
        return ForageSkill.get_traits(self._id)

    @property
    def occupations(self) -> list[Occupation]:
        return ForageSkill.get_occupations(self._id)

    @property
    def sprite_affinity(self) -> str | None:
        return self._data.get("spriteAffinities")

    @property
    def focus_chance_min(self) -> float | None:
        return self._data.get("focusChanceMin")

    @property
    def focus_chance_max(self) -> float | None:
        return self._data.get("focusChanceMax")

    @property
    def valid_floors(self) -> list[str] | None:
        return self._data.get("validFloors")

    @property
    def chance_to_create_icon(self) -> list[str] | None:
        return self._data.get("chanceToCreateIcon")

    @property
    def chance_to_move_icon(self) -> list[str] | None:
        return self._data.get("chanceToMoveIcon")

    @property
    def has_rained_chance(self) -> int | None:
        return self._data.get("hasRainedChance")

    @property
    def rain_chance(self) -> int | None:
        return self._data.get("rainChance")

    @property
    def snow_chance(self) -> int | None:
        return self._data.get("snowChance")

    @property
    def night_chance(self) -> int | None:
        return self._data.get("nightChance")
    
    @property
    def items(self) -> list[ForagingItem]:
        """Returns all ForagingItem instances assigned to this category."""

        return [
            item for item in ForagingItem.all().values()
            if item.type == self._id
        ]

    def __repr__(self) -> str:
        return f"<ForageCategory {self._id}>"


class ForageZone:
    _instances = {}
    _zones = None

    def __new__(cls, zone: str):
        if zone not in cls._instances:
            cls._instances[zone] = super().__new__(cls)
        return cls._instances[zone]

    def __init__(self, zone: str):
        self._id = zone
        self._data:dict = self.load().get(zone, {})

    @classmethod
    def load(cls) -> dict:
        if cls._zones is None:
            cls._zones = ForageSystem.get_zones()
        return cls._zones
    
    @classmethod
    def all(cls) -> dict[str, "ForageZone"]:
        """Return all foraging zones as a dictionary of {zone_id: ForageZone}."""
        return {zone_id: cls(zone_id) for zone_id in cls.load()}

    @classmethod
    def exists(cls, zone: str) -> bool:
        return zone in cls.load()
    
    def get(self, key: str, default=None):
        """Returns the raw value from this zone's data."""
        return self._data.get(key, default)

    @property
    def id(self) -> str:
        return self._id

    @property
    def data(self) -> str:
        return self.data

    @property
    def valid(self) -> bool:
        return self.exists(self._id)

    @property
    def contains_biomes(self) -> dict["ForageZone", float]:
        if not hasattr(self, "_contains_biomes"):
            raw = self._data.get("containsBiomes", {})
            self._contains_biomes = {ForageZone(z): w for z, w in raw.items()}
        return self._contains_biomes
    
    @property
    def name(self) -> str:
        return Translate.get(f"IGUI_SearchMode_Zone_Names_{self.get("name")}") or self._id

    @property
    def density_min(self) -> float | None:
        return self._data.get("densityMin")

    @property
    def density_max(self) -> float | None:
        return self._data.get("densityMax")

    @property
    def refill_percent(self) -> int | None:
        return self._data.get("refillPercent")

    @property
    def abundance_setting(self) -> str | None:
        return self._data.get("abundanceSetting")

    def __repr__(self) -> str:
        return f"<ForageZone {self._id}>"


class ForageSkill:
    _instances = {}
    _skills = None
    _category_map = None

    def __new__(cls, zone: str):
        if zone not in cls._instances:
            cls._instances[zone] = super().__new__(cls)
        return cls._instances[zone]

    def __init__(self, zone: str):
        self._id = zone
        self._data:dict = self.load().get(zone, {})

    @classmethod
    def load(cls) -> dict:
        if cls._skills is None:
            cls._skills = ForageSystem.get_skills()
        return cls._skills
    
    @classmethod
    def all(cls) -> dict[str, "ForageSkill"]:
        """Return all foraging skills as a dictionary of {skill_id: ForageSkill}."""
        return {skill_id: cls(skill_id) for skill_id in cls.load()}

    @classmethod
    def exists(cls, zone: str) -> bool:
        return zone in cls.load()
    
    @classmethod
    def _build_category_map(cls):
        cls._category_map = {"trait": {}, "occupation": {}}
        
        for skill in cls.all().values():
            if not skill.type or skill.type not in cls._category_map:
                continue

            for category in skill.specialisations:
                mapping = cls._category_map[skill.type]
                mapping.setdefault(category.id, []).append(skill.id)

        save_cache(cls._category_map, "forage_category_map.json")

    @classmethod
    def get_traits(cls, category_id: str) -> list[Trait]:
        if cls._category_map is None:
            cls._build_category_map()
        Trait.load() # Ensure Trait data is loaded
        ids = cls._category_map["trait"].get(category_id, [])
        return [Trait(trait_id) for trait_id in ids if Trait.exists(trait_id)]

    @classmethod
    def get_occupations(cls, category_id: str) -> list[Occupation]:
        if cls._category_map is None:
            cls._build_category_map()
        Occupation.load() # Ensure Occupation data is loaded
        ids = cls._category_map["occupation"].get(category_id, [])
        return [Occupation(occ_id) for occ_id in ids if Occupation.exists(occ_id)]
    
    def get(self, key: str, default=None):
        """Returns the raw value from this skill's data."""
        return self._data.get(key, default)

    @property
    def id(self) -> str:
        return self._id

    @property
    def data(self) -> str:
        return self.data

    @property
    def valid(self) -> bool:
        return self.exists(self._id)

    @property
    def type(self) -> float | None:
        return self._data.get("type")
    
    @property
    def object(self) -> Trait | Occupation | None:
        """Returns the Trait or Occupation object associated with this skill."""
        if self.type == "occupation":
            return Occupation(self._id)
        elif self.type == "trait":
            return Trait(self._id)
        return None
    
    @property
    def name(self) -> str:
        if not hasattr(self, "_name"):
            self._name = self.object.name if self.object else None
        return self._name or self.get("name") or self._id

    @property
    def weather_effect(self) -> float | None:
        return self._data.get("weatherEffect")

    @property
    def darkness_effect(self) -> int | None:
        return self._data.get("darknessEffect")

    @property
    def specialisations(self) -> dict[ForageCategory, float]:
        if not hasattr(self, "_specialisations"):
            raw = self._data.get("specialisations", {})
            if raw:
                self._specialisations = {ForageCategory(z): float(w) for z, w in raw.items()}
            else:
                self._specialisations = {}
        return self._specialisations

    @property
    def vision_bonus(self) -> str | None:
        return self._data.get("visionBonus")

    def __repr__(self) -> str:
        return f"<ForageSkill {self._id}>"


class ForageSystem:
    _data = None

    @classmethod
    def _parse_forage_system(cls) -> dict:
        inject = """
        function require(module) return {} end
        Events = setmetatable({}, {
            __index = function()
                return { Add = function() end, Remove = function() end }
            end
        })
        """
        lua_runtime = load_lua_file("forageSystem.lua", inject_lua=inject)
        parsed_data = parse_lua_tables(lua_runtime, tables=["forageSystem"])
        save_cache(parsed_data, "forage_system.json")
        return parsed_data

    @classmethod
    def _parse_forage_categories(cls):
        inject = """
        forageSystem = {
            spriteAffinities = setmetatable({}, {
                __index = function(_, key)
                    return key  -- return the field name as a string
                end
            })
        }

        function require(module)
            return forageSystem
        end
        """

        lua_runtime = load_lua_file("forageCategories.lua", inject_lua=inject)

        category_defs = lua_runtime.eval("forageSystem.categoryDefinitions")
        parsed_data = {"categoryDefinitions": lua_to_python(category_defs)}
        save_cache(parsed_data, "forage_categories.json")
        return parsed_data


    @classmethod
    def _parse_zones(cls) -> dict:
        inject = """
        function require(module) return {} end
        forageSystem = {}
        """

        lua_runtime = load_lua_file("forageZones.lua", inject_lua=inject)
        zone_defs = lua_runtime.eval("forageSystem.zoneDefinitions")
        parsed = {"zoneDefinitions": lua_to_python(zone_defs)}
        save_cache(parsed, "forage_zones.json")
        return parsed


    @classmethod
    def _parse_skills(cls) -> dict:
        inject = """
        function require(module) return {} end
        forageSystem = {}
        """

        lua_runtime = load_lua_file("forageSkills.lua", inject_lua=inject)
        skill_defs = lua_runtime.eval("forageSystem.forageSkillDefinitions")
        parsed = {"forageSkillDefinitions": lua_to_python(skill_defs)}
        save_cache(parsed, "forage_skills.json")
        return parsed


    @classmethod
    def _parse(cls):
        system = cls._parse_forage_system()
        categories = cls._parse_forage_categories()
        zones = cls._parse_zones()
        skills = cls._parse_skills()

        forage_system = system.get("forageSystem", {})
        category_definitions = categories.get("categoryDefinitions", {})
        zone_definitions = zones.get("zoneDefinitions", {})
        skill_definitions = skills.get("forageSkillDefinitions", {})

        clean_forage_system = {
            k: v for k, v in forage_system.items()
            if not (isinstance(v, str) and v.startswith("<Lua function"))
        }

        combined = {
            **clean_forage_system,
            "categoryDefinitions": category_definitions,
            "zoneDefinitions": zone_definitions,
            "forageSkillDefinitions": skill_definitions
        }

        save_cache(combined, "parsed_foraging.json")

    @classmethod
    def load(cls) -> dict:
        if cls._data is not None:
            return cls._data

        path = os.path.join(CACHE_DIR, "parsed_foraging.json")

        data, version = load_cache(path, cache_name="foraging", get_version=True)

        # Re-parse if outdated
        if version != Version.get():
            data = cls._parse()

        cls._data = data or {}
        return cls._data
    
    @classmethod
    def get(cls, value, default) -> dict:
        """Returns a value from the foraging data, or a default if not found."""
        return cls.load().get(value, default)

    @classmethod
    def get_categories(cls) -> dict[str, dict]:
        """Returns all foraging category definitions."""
        return cls.load().get("categoryDefinitions", {})

    @classmethod
    def get_zones(cls) -> dict[str, dict]:
        """Returns all forage zone definitions (e.g., Forest, DeepForest)."""
        return cls.load().get("zoneDefinitions", {})

    @classmethod
    def get_skills(cls) -> dict[str, dict]:
        """Returns all forage skill definitions (e.g., PlantScavenging, Trapping)."""
        return cls.load().get("forageSkillDefinitions", {})

    @classmethod
    def get_sprite_affinities(cls) -> dict[str, list[str]]:
        """Returns sprite affinity groupings (e.g., genericPlants → list of tile names)."""
        return cls.load().get("spriteAffinities", {})

    @classmethod
    def get_seed_table(cls) -> dict[str, dict]:
        """Returns seed drop info (item → { type, amount, chance })."""
        return cls.load().get("seedTable", {})

    @classmethod
    def get_world_sprites(cls) -> dict[str, list[list[str]]]:
        """Returns grouped world sprite names for placement (e.g., bushes, wildPlants)."""
        return cls.load().get("worldSprites", {})

    @classmethod
    def get_abundance_settings(cls) -> dict[str, list[int]]:
        """Returns abundance modifiers for game difficulty presets."""
        return cls.load().get("abundanceSettings", {})

    @classmethod
    def get_clothing_penalties(cls) -> dict[str, float | int]:
        """Returns vision penalties caused by clothing on specific body locations."""
        return cls.load().get("clothingPenalties", {})

    @classmethod
    def get_zone_density_multi(cls) -> float | None:
        return cls.load().get("zoneDensityMulti")

    @classmethod
    def get_aim_multiplier(cls) -> float | None:
        return cls.load().get("aimMultiplier")

    @classmethod
    def get_max_icons_per_zone(cls) -> int | None:
        return cls.load().get("maxIconsPerZone")

    @classmethod
    def get_min_vision_radius(cls) -> float | None:
        return cls.load().get("minVisionRadius")

    @classmethod
    def get_max_vision_radius(cls) -> float | None:
        return cls.load().get("maxVisionRadius")

    @classmethod
    def get_vision_radius_cap(cls) -> float | None:
        return cls.load().get("visionRadiusCap")

    @classmethod
    def get_dark_vision_radius(cls) -> float | None:
        return cls.load().get("darkVisionRadius")

    @classmethod
    def get_fatigue_penalty(cls) -> float | None:
        return cls.load().get("fatiguePenalty")

    @classmethod
    def get_exhaustion_penalty_max(cls) -> float | None:
        return cls.load().get("exhaustionPenaltyMax")

    @classmethod
    def get_panic_penalty_max(cls) -> float | None:
        return cls.load().get("panicPenaltyMax")

    @classmethod
    def get_light_penalty_max(cls) -> float | None:
        return cls.load().get("lightPenaltyMax")

    @classmethod
    def get_clothing_penalty_max(cls) -> float | None:
        return cls.load().get("clothingPenaltyMax")

    @classmethod
    def get_effect_reduction_max(cls) -> float | None:
        return cls.load().get("effectReductionMax")

    @classmethod
    def get_hunger_bonus_max(cls) -> float | None:
        return cls.load().get("hungerBonusMax")

    @classmethod
    def get_body_penalty_max(cls) -> float | None:
        return cls.load().get("bodyPenaltyMax")

    @classmethod
    def get_endurance_penalty(cls) -> float | None:
        return cls.load().get("endurancePenalty")

    @classmethod
    def get_sneak_multiplier(cls) -> float | None:
        return cls.load().get("sneakMultiplier")

    @classmethod
    def get_level_xp_modifier(cls) -> float | None:
        return cls.load().get("levelXPModifier")

    @classmethod
    def get_global_xp_modifier(cls) -> float | None:
        return cls.load().get("globalXPModifier")

    @classmethod
    def get_level_bonus(cls) -> float | None:
        return cls.load().get("levelBonus")

    @classmethod
    def get_month_malus(cls) -> float | None:
        return cls.load().get("monthMalus")

    @classmethod
    def get_month_bonus(cls) -> float | None:
        return cls.load().get("monthBonus")

    @classmethod
    def get_light_penalty_cutoff(cls) -> float | None:
        return cls.load().get("lightPenaltyCutoff")

if __name__ == "__main__":
    #print(ForageSystem.load())
    print(ForagingItem("Leech").has_category("Insects"))
    print(ForagingItem("Leech").categories)