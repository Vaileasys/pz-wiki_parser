import os
from scripts.core.language import Translate
from scripts.utils.lua_helper import load_lua_file, lua_to_python
from scripts.core.cache import save_cache, load_cache
from scripts.utils import echo, util
from scripts.core.constants import LUA_STUB_PATH, CACHE_DIR
from scripts.core.file_loading import read_file
from scripts.core.version import Version

def parse_main_creation_methods(func: str, expression: str = None, name: str = None, suppress: bool = False) -> dict:
    if name is None:
        name = func

    stub_path = os.path.join(LUA_STUB_PATH, "TraitFactory_stub.lua")
    inject_lua = read_file(stub_path)

    inject_lua = inject_lua

    runtime = load_lua_file("MainCreationMethods.lua", inject_lua=inject_lua)
    
    try:
        runtime.eval(f"BaseGameCharacterDetails.{func}()")
    except Exception as e:
        echo.warning(f"{func}() failed: {e}")

    if func == "DoTraits":
        parsed_data = lua_to_python(runtime.eval("TraitFactory._traits"))
    elif func == "DoProfessions":
        parsed_data = lua_to_python(runtime.eval("ProfessionFactory._profs"))
    else:
        parsed_data = lua_to_python(runtime.eval(expression)) if expression else {}
    

    save_cache(parsed_data, f"{name}", suppress=suppress)

    return parsed_data


class Occupation:
    _instances = {}
    _occupations = None
    _data_file = "parsed_occupation_data.json"

    def __new__(cls, occupation: str):
        if occupation not in cls._instances:
            cls._instances[occupation] = super().__new__(cls)
        return cls._instances[occupation]

    def __init__(self, occupation: str):
        self._id = occupation
        self._data:dict = self.load().get(occupation, {})

    @classmethod
    def _parse(cls) -> dict:
        if cls._occupations is None:
            cls._occupations = parse_main_creation_methods(func="DoProfessions", name=cls._data_file)
        return cls._occupations
    
    @classmethod
    def load(cls) -> dict:
        if cls._occupations is not None:
            return cls._occupations

        path = os.path.join(CACHE_DIR, cls._data_file)

        data, version = load_cache(path, cache_name="occupations", get_version=True)

        # Re-parse if outdated
        if version != Version.get():
            data = cls._parse()

        cls._occupations = data or {}
        return cls._occupations
    
    @classmethod
    def all(cls):
        """Return all occupations as a dictionary of Occupation instances."""
        if cls._occupations is None:
            cls.load()
        return {occ_id: cls(occ_id) for occ_id in cls._occupations}

    @classmethod
    def keys(cls):
        """Return all occupation keys."""
        if cls._occupations is None:
            cls.load()
        return cls._occupations.keys()

    @classmethod
    def values(cls):
        """Yield Occupation instances for all occupations."""
        if cls._occupations is None:
            cls.load()
        return (cls(occ_id) for occ_id in cls._occupations)
    
    @classmethod
    def count(cls):
        """Return the number of defined occupations."""
        if cls._occupations is None:
            cls.load()
        return len(cls._occupations)

    @classmethod
    def exists(cls, trait: str) -> bool:
        return trait in cls._occupations
    
    def get(self, key: str, default=None):
        return self._data.get(key, default)

    @property
    def id(self) -> str:
        return self._id

    @property
    def data(self) -> str:
        return self._data

    @property
    def valid(self) -> bool:
        return self.exists(self._id)

    @property
    def name(self) -> str:
        if not hasattr(self, "_name"):
            self._name = Translate.get(f"{self.get('name')}", lang_code="en")
        return self._name

    @property
    def name_en(self) -> str:
        if not hasattr(self, "_name_en"):
            self._name_en = Translate.get(f"{self.get("name")}", lang_code="en")
        return self._name_en

    @property
    def page(self) -> str: #dummy for later use if needed
        return self.name_en
    
    @property
    def wiki_link(self) -> str:
        return util.link(self.page, self.name)
    
    @property
    def icon(self) -> str:
        if not hasattr(self, "_icon"):
            raw = self.get("icon")
            if raw:
                self._icon = f"[[File:{raw}.png|{self.page}|link={self.name}]]"
            else:
                self._icon = ""

        return self._icon

    @property
    def cost(self) -> int:
        return self.get("cost", 0)

    @property
    def is_free(self) -> bool:
        return self.get("isFree", False)

    @property
    def free_traits(self) -> list[str]:
        return self.get("freeTraits", [])

    @property
    def xp_boosts(self) -> list[str]:
        return self.get("xpBoosts", [])

    @property
    def recipes(self) -> list[str]:
        return self.get("recipes", [])

    def __repr__(self) -> str:
        return f"<Occupation {self._id}>"


class Trait:
    _instances = {}
    _traits = None
    _data_file = "parsed_traits_data.json"

    def __new__(cls, trait: str):
        if trait not in cls._instances:
            cls._instances[trait] = super().__new__(cls)
        return cls._instances[trait]

    def __init__(self, trait: str):
        self._id = trait
        self._data:dict = self.load().get(trait, {})

    @classmethod
    def _parse(cls) -> dict:
        if cls._traits is None:
            cls._traits = parse_main_creation_methods(func="DoTraits", name=cls._data_file)
        return cls._traits
    
    @classmethod
    def load(cls) -> dict:
        if cls._traits is not None:
            return cls._traits

        path = os.path.join(CACHE_DIR, cls._data_file)

        data, version = load_cache(path, cache_name="traits", get_version=True)

        # Re-parse if outdated
        if version != Version.get():
            data = cls._parse()

        cls._traits = data or {}
        return cls._traits
    
    @classmethod
    def all(cls):
        """Return all traits as a dictionary of Trait instances."""
        if cls._traits is None:
            cls.load()
        return {trait_id: cls(trait_id) for trait_id in cls._traits}
    
    @classmethod
    def keys(cls):
        """Return all trait keys."""
        if cls._traits is None:
            cls.load()
        return cls._traits.keys()

    @classmethod
    def values(cls):
        """Yield Trait instances for all traits."""
        if cls._traits is None:
            cls.load()
        return (cls(occ_id) for occ_id in cls._traits)
    
    @classmethod
    def count(cls):
        """Return the number of defined traits."""
        if cls._traits is None:
            cls.load()
        return len(cls._traits)

    @classmethod
    def exists(cls, trait: str) -> bool:
        return trait in cls._traits
    
    def get(self, key: str, default=None):
        return self._data.get(key, default)

    @property
    def id(self) -> str:
        return self._id

    @property
    def data(self) -> str:
        return self._data

    @property
    def valid(self) -> bool:
        return self.exists(self._id)

    @property
    def name(self) -> str:
        return Translate.get(f"{self.get("name")}") or self._id

    @property
    def name_en(self) -> str:
        if not hasattr(self, "_name_en"):
            self._name_en = Translate.get(f"{self.get("name")}", lang_code="en")
        return self._name_en

    @property
    def page(self) -> str: #dummy for later use if needed
        return self.name_en
    
    @property
    def wiki_link(self) -> str:
        return util.link(self.page, self.name)
    
    @property
    def icon(self) -> str:
        if not hasattr(self, "_icon"):
            #TODO: Confirm this is how trait icons are obtained
            self._icon = f"[[File:Trait_{self.id.lower()}.png|{self.page}|link={self.name}]]"

        return self._icon

    @property
    def desc(self) -> str:
        return Translate.get(f"{self.get("desc")}")

    @property
    def cost(self) -> int:
        return self.get("cost", 0)

    @property
    def is_free(self) -> bool:
        return self.get("isFree", False)

    @property
    def free_traits(self) -> list[str]:
        return self.get("freeTraits", [])

    @property
    def xp_boosts(self) -> list[str]:
        return self.get("xpBoosts", [])

    @property
    def recipes(self) -> list[str]:
        return self.get("recipes", [])

    def __repr__(self) -> str:
        return f"<Trait {self._id}>"
