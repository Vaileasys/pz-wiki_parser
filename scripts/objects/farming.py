import math
from scripts.core.language import Translate
from scripts.utils import lua_helper
from scripts.core.cache import save_cache, load_cache
from scripts.core.version import Version
from scripts.objects.item import Item

class Farming:
    _farming_definitions = None # raw parsed Lua data
    _crop_data = None # structured, merged per crop

    @classmethod
    def _parse_farming_definitions(cls):
        if cls._farming_definitions is not None:
            return cls._farming_definitions

        RAW_CACHE_FILE = "farming_definitions_raw.json"
        CACHE_LABEL = "farming definitions"

        raw_data, cache_version = load_cache(RAW_CACHE_FILE, CACHE_LABEL, get_version=True, suppress=True)

        if cache_version != Version.get() or not raw_data:
            lua_runtime = lua_helper.load_lua_file(
                [
                    "farming_vegetableconf.lua",
                    "farming_vegetableconf_herbs.lua",
                    "farming_vegetableconf_herbs_sprites.lua",
                    "farming_vegetableconf_vegetables.lua",
                    "farming_vegetableconf_vegetables_sprites.lua"
                ],
                inject_lua="farming_vegetableconf = farming_vegetableconf or {}"
            )
            raw_data = lua_helper.parse_lua_tables(lua_runtime)
            save_cache(raw_data, RAW_CACHE_FILE)

        cls._farming_definitions = raw_data
        return raw_data

    @classmethod
    def _load_farming_definitions(cls):
        if cls._crop_data is not None:
            return cls._crop_data

        raw_data = cls._parse_farming_definitions()
        farming_conf = raw_data.get("farming_vegetableconf", {})
        props = farming_conf.get("props", {})
        sprite_fields = ["sprite", "dyingSprite", "unhealthySprite", "deadSprite", "trampledSprite"]

        structured_data = {}
        for crop_id, crop_data in props.items():
            merged = dict(crop_data)

            for sprite_field in sprite_fields:
                sprite_dict = farming_conf.get(sprite_field, {})
                if crop_id in sprite_dict:
                    merged[sprite_field] = sprite_dict[crop_id]

            structured_data[crop_id] = merged

        cls._crop_data = structured_data
        return structured_data

    @classmethod
    def from_item(cls, item: Item | str) -> "Farming | None":
        item_id = item.item_id if isinstance(item, Item) else item

        for crop_id, data in cls._load_farming_definitions().items():
            if (
                item_id == data.get("seedName") or
                item_id == data.get("specialSeed") or
                item_id == data.get("vegetableName") or
                item_id in data.get("seedTypes", [])
            ):
                return cls(crop_id)

        return None
    
    @classmethod
    def from_recipe(cls, recipe: str | list[str]) -> "Farming | None":
        recipes = [recipe] if isinstance(recipe, str) else recipe

        for crop_id, data in cls._load_farming_definitions().items():
            crop_recipe = data.get("seasonRecipe")
            if crop_recipe and crop_recipe in recipes:
                return cls(crop_id)

        return None

    def __init__(self, crop: str):
        self._crop = crop
        self._data = self._load_farming_definitions().get(crop, {})

    def get_sprite(self, sprite=None, dim="32x32px") -> str:
        from scripts.core.language import Language

        if sprite is None:
            sprite = self.sprite
        elif hasattr(self, sprite):
            sprite = getattr(self, sprite)

        if not isinstance(sprite, list):
            sprite = [sprite]

        images = [
            f"[[File:{frame}.png|{dim}|link={self.crop} (crop){Language.get_subpage()}|{self.crop}]]"
            for frame in sprite
        ]

        return f'<span class="cycle-img">{"".join(images)}</span>'

    ## ------------------ Core Properties ------------------ ##

    @property
    def crop(self) -> str:
        return self._crop

    @property
    def data(self) -> dict:
        return self._data

    @property
    def icon(self) -> str | None:
        return self._data.get("icon")

    @property
    def texture(self) -> str | None:
        return self._data.get("texture")

    @property
    def season_recipe(self) -> str | None:
        return self._data.get("seasonRecipe")

    @property
    def seed_name(self) -> Item | None:
        seed = Item(self._data.get("seedName"))
        if seed:
            return seed.name
        return None

    @property
    def seed_item(self) -> Item | None:
        if self.seed_types:
            return self.seed_types[0]
        return Item(self._data.get("seedName"))

    @property
    def vegetable_item(self) -> Item | None:
        return Item(self._data.get("vegetableName"))

    @property
    def special_seed(self) -> Item | None:
        return Item(self._data.get("specialSeed"))

    @property
    def seed_types(self) -> list[Item]:
        return [Item(seed) for seed in self._data.get("seedTypes", [])]

    ## ------------------ Sprites ------------------ ##

    @property
    def sprite(self) -> list[str]:
        return self._data.get("sprite", [])

    @property
    def dying_sprite(self) -> list[str]:
        return self._data.get("dyingSprite", [])

    @property
    def unhealthy_sprite(self) -> list[str]:
        return self._data.get("unhealthySprite", [])

    @property
    def dead_sprite(self) -> list[str]:
        return self._data.get("deadSprite", [])

    @property
    def trampled_sprite(self) -> list[str]:
        return self._data.get("trampledSprite", [])
    
    ## ------------------ Growth Stats ------------------ ##

    @property
    def time_to_grow(self) -> int | None:
        return self._data.get("timeToGrow")

    @property
    def grow_time_days(self) -> int | None:
        return math.floor((self.time_to_grow * self.harvest_level) / 24)

    @property
    def full_grown_stage(self) -> int | None:
        return self._data.get("fullGrown")

    @property
    def mature_stage(self) -> int | None:
        return self._data.get("mature")

    @property
    def harvest_level(self) -> int | None:
        return self._data.get("harvestLevel")

    @property
    def water_needed_raw(self) -> int | None:
        return self._data.get("waterNeeded")

    @property
    def water_needed(self) -> int | None:
        return self.water_needed_raw * 20

    @property
    def water_level(self) -> int | None:
        return self.water_level
    
    @property
    def rot_time(self) -> int | None:
        return self._data.get("rotTime")

    @property
    def grow_back(self) -> int | None:
        return self._data.get("growBack")

    @property
    def harvest_position(self) -> str | None:
        return self._data.get("harvestPosition")
    
    ## ------------------ Months ------------------ ##

    @property
    def sow_month_num(self) -> list[int]:
        return self._data.get("sowMonth", [])

    @property
    def sow_months(self) -> list[int]:
        return (Translate.get(f"Farming_Month_{m}") for m in self.sow_month_num)

    @property
    def best_month_num(self) -> list[int]:
        return self._data.get("bestMonth", [])

    @property
    def best_months(self) -> list[int]:
        return (Translate.get(f"Farming_Month_{m}") for m in self.best_month_num) if self.best_month_num else []

    @property
    def risk_month_num(self) -> list[int]:
        return self._data.get("riskMonth", [])

    @property
    def risk_months(self) -> list[int]:
        return (Translate.get(f"Farming_Month_{m}") for m in self.risk_month_num) if self.risk_month_num else []

    @property
    def bad_month_num(self) -> list[int]:
        return self._data.get("badMonth", [])

    @property
    def bad_months(self) -> list[int]:
        return (Translate.get(f"Farming_Month_{m}") for m in self.bad_month_num) if self.bad_month_num else []
    
    ## ------------------ Yield ------------------ ##
    
    @property
    def min_veg(self) -> int | None:
        return self._data.get("minVeg")

    @property
    def max_veg(self) -> int | None:
        return self._data.get("maxVeg")

    @property
    def min_veg_authorized(self) -> int | None:
        return self._data.get("minVegAutorized")

    @property
    def max_veg_authorized(self) -> int | None:
        return self._data.get("maxVegAutorized")
    
    ## ------------------ Flags ------------------ ##
    
    @property
    def is_flower(self) -> bool:
        return bool(self._data.get("isFlower"))

    @property
    def moth_food(self) -> bool:
        return bool(self._data.get("mothFood"))

    @property
    def moth_bane(self) -> bool:
        return bool(self._data.get("mothBane"))

    @property
    def aphids_bane(self) -> bool:
        return bool(self._data.get("aphidsBane"))

    @property
    def rabbit_bane(self) -> bool:
        return bool(self._data.get("rabbitBane"))

    @property
    def cold_hardy(self) -> bool:
        return bool(self._data.get("coldHardy"))

    @property
    def slugs_proof(self) -> bool:
        return bool(self._data.get("slugsProof"))

    @property
    def scythe_harvest(self) -> bool:
        return bool(self._data.get("scytheHarvest"))