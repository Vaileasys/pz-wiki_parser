import os
from scripts.parser import script_parser
from scripts.core.file_loading import get_script_path
from scripts.core.language import Language, Translate
from scripts.core.page_manager import get_pages
from scripts.core import logger
from scripts.utils.util import link
from scripts.core.cache import load_json

class Fluid:
    _fluids = None # Shared cache for all fluids
    _color_reference = None # Shared color reference cache
    _instances = {}

    def __new__(cls, fluid_id: str, mix_ratio=None, color=None):
        """Returns an existing Fluid instance if one already exists for the given ID.
        If overrides are provided, returns a new instance"""
        if cls._fluids is None:
            cls._load_fluids()

        fluid_id = cls.fix_fluid_id(fluid_id)

        # If no overrides, reuse shared instance
        if mix_ratio is None and color is None:
            if fluid_id in cls._instances:
                return cls._instances[fluid_id]

            instance = super().__new__(cls)
            cls._instances[fluid_id] = instance
            return instance

        # If overrides, always create fresh instance
        return super().__new__(cls)

    def __init__(self, fluid_id: str, mix_ratio=None, color=None):
        """Initialises the fluid’s data if it hasn’t been initialised yet."""
        if hasattr(self, 'fluid_id'):
            return

        if Fluid._fluids is None:
            Fluid._load_fluids()

        fluid_id = self.fix_fluid_id(fluid_id)

        self.fluid_id = fluid_id
        self.data = Fluid._fluids.get(fluid_id, {})

        id_parts = fluid_id.split(".", 1)
        self._module = id_parts[0]
        self._id_type = id_parts[1] if len(id_parts) == 2 else None

        self._name = None # Translated name
        self._name_en = None # English name
        self._page = None # Wiki page
        self._wiki_link = None # Wiki link

        self._color = color
        self._mix_ratio = mix_ratio

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key):
        return key in self.data

    def __repr__(self):
        return f'<Fluid {self.fluid_id}>'

    @classmethod
    def _load_fluids(cls):
        """Load fluid data only once and store in class-level cache."""
        cls._fluids = script_parser.extract_script_data("fluid")

    @classmethod
    def _load_color_reference(cls):
        if cls._color_reference is None:
            cls._color_reference = load_json(os.path.join("resources", "color_reference.json"))

    @classmethod
    def fix_fluid_id(cls, fluid_id: str) -> str:
        """
        Fixes a partial fluid_id by assuming 'Base' first, then fallback to search.
        """
        if '.' in fluid_id:
            return fluid_id

        base_guess = f"Base.{fluid_id}"
        if cls._fluids is None:
            cls._load_fluids()

        if base_guess in cls._fluids:
            return base_guess

        # Fallback: full search
        for full_id in cls._fluids:
            if full_id.endswith(f".{fluid_id}"):
                return full_id

        logger.write(f"No Fluid ID found for '{fluid_id}'")
        return fluid_id

    @classmethod
    def all(cls):
        """Return all fluids as a dictionary of {fluid_id: Fluid}."""
        if cls._fluids is None:
            cls._load_fluids()
        return {fluid_id: cls(fluid_id) for fluid_id in cls._fluids}

    @classmethod
    def keys(cls):
        if cls._fluids is None:
            cls._load_fluids()
        return cls._fluids.keys()

    @classmethod
    def values(cls):
        if cls._fluids is None:
            cls._load_fluids()
        return (cls(fluid_id) for fluid_id in cls._fluids)

    @classmethod
    def count(cls):
        if cls._fluids is None:
            cls._load_fluids()
        return len(cls._fluids)

    @classmethod
    def exists(cls, fluid_id: str) -> bool:
        if cls._fluids is None:
            cls._load_fluids()

        fluid_id = cls.fix_fluid_id(fluid_id)
        return fluid_id in cls._fluids

    ## ------------------------- Dict-like Methods ------------------------- ##

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    ## ------------------------- Properties ------------------------- ##

    # --- Base Properties --- #

    @property
    def valid(self) -> bool:
        return bool(self.data)

    @property
    def script_type(self) -> str:
        return self.data.get("ScriptType")

    @property
    def file(self):
        return self.data.get("SourceFile")

    @property
    def path(self):
        return get_script_path(self.file, prefer="fluid")

    @property
    def module(self):
        return self._module

    @property
    def id_type(self):
        return self._id_type

    @property
    def page(self):
        if self._page is None:
            pages = get_pages(self.fluid_id, id_type="fluid_id")
            self._page = pages[0] if pages else self.name_en
        return self._page

    @property
    def display_name(self):
        return self.get("DisplayName", "Fluid_Name_" + self.id_type)

    @property
    def name(self):
        if self._name is None:
            name = Translate.get(self.display_name, "Fluid_Name_Fluid")
            if self._id_type == "TaintedWater":
                tainted_water = Translate.get("IGUI_ItemNameTaintedWater")
                name = tainted_water.replace("%1", name)
            self._name = name
        return self._name

    @property
    def name_en(self):
        if self._name_en is None:
            name = Translate.get(self.display_name, lang_code="en")
            if self._id_type == "TaintedWater":
                tainted_water = Translate.get("IGUI_ItemNameTaintedWater", lang_code="en")
                name = tainted_water.replace("%1", name)
            self._name_en = name
        return self._name_en

    @property
    def wiki_link(self):
        if self._wiki_link is None:
            self._wiki_link = link(self.page, self.name)
        return self._wiki_link
    
    @property
    def mix_ratio(self):
        """Return the fluid’s relative mix ratio (defaults to 1.0 if not set)."""
        return self._mix_ratio if self._mix_ratio is not None else 1.0
    
    # --- Properties --- #

    @property
    def properties(self):
        """Return the 'Properties' block or an empty dict."""
        return self.data.get("Properties", {})

    @property
    def fatigue_change(self):
        return self.properties.get("fatigueChange", 0)

    @property
    def hunger_change(self):
        return self.properties.get("hungerChange", 0)

    @property
    def stress_change(self):
        return self.properties.get("stressChange", 0)

    @property
    def thirst_change(self):
        return self.properties.get("thirstChange", 0)

    @property
    def unhappy_change(self):
        return self.properties.get("unhappyChange", 0)

    @property
    def calories(self):
        return self.properties.get("calories", 0)

    @property
    def carbohydrates(self):
        return self.properties.get("carbohydrates", 0)

    @property
    def lipids(self):
        return self.properties.get("lipids", 0)

    @property
    def proteins(self):
        return self.properties.get("proteins", 0)

    @property
    def alcohol(self):
        return self.properties.get("alcohol", 0)

    @property
    def flu_reduction(self):
        return self.properties.get("fluReduction", 0)

    @property
    def pain_reduction(self):
        return self.properties.get("painReduction", 0)

    @property
    def endurance_change(self):
        return self.properties.get("enduranceChange", 0)

    @property
    def food_sickness_reduction(self):
        return self.properties.get("foodSicknessReduction", 0)
    
    # --- Poison --- #

    @property
    def poison(self):
        """Return a FluidPoison object wrapping the 'Poison' block."""
        if not hasattr(self, '_poison'):
            self._poison = FluidPoison(self.data.get("Poison", {}))
        return self._poison
    
    # --- Color --- #

    @property
    def color_reference(self):
        return self.data.get('ColorReference', None)

    @property
    def color(self):
        """Return the fluid color as [R, G, B] integers (0–255)."""
        if self._color:
            rgb_values = self._color
        else:
            Fluid._load_color_reference()

            color_ = self.color_reference or self.data.get('Color', [0.0, 0.0, 0.0])
            
            if isinstance(color_, str):
                rgb_values = Fluid._color_reference["colors"].get(color_, [0.0, 0.0, 0.0])
            else:
                rgb_values = color_

        color_rgb = [int(c * 255) for c in rgb_values]
        return color_rgb

    @property
    def r(self):
        return self.color[0]

    @property
    def g(self):
        return self.color[1]

    @property
    def b(self):
        return self.color[2]

    @property
    def rgb(self):
        """Return the fluid color as a wiki RGB template string, e.g., '{{rgb|140, 198, 0}}'."""
        rgb_values = self.color
        return f"{{{{rgb|{rgb_values[0]}, {rgb_values[1]}, {rgb_values[2]}}}}}"
    
    # --- Categories --- #

    @property
    def categories(self):
        """Return the fluid's category list, or empty if none."""
        return self.data.get("Categories", [])

    @property
    def blend_whitelist(self):
        """Return FluidBlendList for BlendWhiteList (empty if missing)."""
        if not hasattr(self, '_blend_whitelist'):
            blend_data = self.data.get("BlendWhiteList")
            self._blend_whitelist = FluidBlendList(blend_data or {})
        return self._blend_whitelist

    @property
    def blend_blacklist(self):
        """Return FluidBlendList for BlendBlackList (empty if missing)."""
        if not hasattr(self, '_blend_blacklist'):
            blend_data = self.data.get("BlendBlackList")
            self._blend_blacklist = FluidBlendList(blend_data or {})
        return self._blend_blacklist


class FluidPoison:
    def __init__(self, poison_data: dict):
        self.data = poison_data or {}

    @property
    def max_effect(self):
        return self.data.get("maxEffect", "None")

    @property
    def min_amount(self):
        return self.data.get("minAmount", 0)

    @property
    def dilute_ratio(self):
        return self.data.get("diluteRatio", 0)


class FluidBlendList:
    def __init__(self, blend_data: dict):
        self.data = blend_data or {}

    @property
    def whitelist(self):
        return self.data.get("whitelist", False)

    @property
    def blacklist(self):
        return self.data.get("blacklist", False)

    @property
    def fluids(self):
        return self.data.get("fluids", [])

    @property
    def categories(self):
        return self.data.get("categories", [])


if __name__ == "__main__":
    Language.get()

    fluid = Fluid("Base.Acid")
    print(f'Page: {fluid.page}')
