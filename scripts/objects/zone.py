import os
from collections import defaultdict
from scripts.core.cache import save_cache, load_cache
from scripts.utils import echo, util, lua_helper
from scripts.core.constants import CACHE_DIR
from scripts.core.version import Version


class Zone:
    """
    Handle zone data as one class:
    - Zone._parse() builds { zone_type: { name: [entries...] } }
    - Zone.load() loads from cache (re-parse if version mismatch)
    - Zone(zone_type) -> a handle for that type (returns nested dict)
    - Zone(zone_type, name) -> a handle for that name group (returns list)
    """
    _raw_data = None                       # { zone_type: { name: [entries...] } }
    _instances = {}                        # { (zone_type, name): Zone }
    _data_file = "parsed_zone_data.json"   # cache file

    def __new__(cls, zone_type, name=None):
        if cls._raw_data is None:
            cls.load()
        key = (zone_type, name)
        if key in cls._instances:
            return cls._instances[key]
        inst = super().__new__(cls)
        cls._instances[key] = inst
        return inst

    def __init__(self, zone_type, name=None):
        # prevent re-init on cached instances
        if hasattr(self, "zone_type"):
            return
        if Zone._raw_data is None:
            Zone.load()

        self.zone_type = zone_type
        self.name = name  # None = whole type, "" = unnamed group
        type_dict = Zone._raw_data.get(zone_type, {})
        if self.name is None:
            # handle for the entire zone type (nested dict)
            self._data = type_dict
        else:
            # handle for a specific group (list)
            self._data = type_dict.get(name, [])

    # ---- Class methods ----
    @classmethod
    def _parse(cls):
        """Parse objects.lua -> nested dict, then save cache."""
        lua_runtime = lua_helper.load_lua_file(lua_files="objects.lua", prefer="Muldraugh, KY", media_type="maps")
        parsed = lua_helper.parse_lua_tables(lua_runtime)
        objects = parsed.get("objects", [])
        out = {}

        for entry in objects:
            ztype = entry.get("type", "Unknown")

            if ztype == "Animal":
                props_dict = entry.get("properties") or {}
                group_key = props_dict.get("AnimalType")
                if not group_key:
                    group_key = entry.get("name", "Unknown")
            else:
                group_key = entry.get("name", "Unknown")

            out.setdefault(ztype, {}).setdefault(group_key, []).append(entry)

        cls._raw_data = out
        save_cache(cls._raw_data, cls._data_file)
        return cls._raw_data

    @classmethod
    def load(cls):
        """Load from cache, re-parse if version mismatch."""
        if cls._raw_data is not None:
            return cls._raw_data

        path = os.path.join(CACHE_DIR, cls._data_file)
        data, version = load_cache(path, cache_name="zones", get_version=True)

        if version != Version.get():
            data = cls._parse()

        cls._raw_data = data or {}
        return cls._raw_data

    @classmethod
    def types(cls):
        """List available zone types."""
        if cls._raw_data is None:
            cls.load()
        return list(cls._raw_data.keys())

    @classmethod
    def names_for(cls, zone_type, include_empty=True):
        """List name groups for a given zone type."""
        if cls._raw_data is None:
            cls.load()
        d = cls._raw_data.get(zone_type, {})
        names = list(d.keys())
        if not include_empty:
            names = [n for n in names if n]
        return names

    @classmethod
    def exists(cls, zone_type, name=None):
        if cls._raw_data is None:
            cls.load()
        if name is None:
            return zone_type in cls._raw_data
        return name in cls._raw_data.get(zone_type, {})

    # ---- Instance ----
    def all(self):
        """
        If self.name is None -> return nested dict {name: [entries...]} for the zone type.
        If self.name is set  -> return the list of entries for that group.
        """
        return self._data

    def flat(self):
        """Flatten to a single list (only meaningful for type handles)."""
        if self.name is not None:
            # already a list
            return list(self._data)
        out = []
        for lst in self._data.values():
            out.extend(lst)
        return out

    def dump(self, filename=None):
        """Dump to JSON file."""
        if filename is None:
            base = util.split_camel_case(self.zone_type).lower().replace(" ", "_") or "general"
            if self.name is None:
                filename = f"{base}_zones.json"
            else:
                suffix = self.name or "unnamed"
                filename = f"{base}_{suffix}_zones.json"

        if self.name is None:
            payload = self._data
        else:
            payload = {self.name: self._data}

        save_cache(payload, filename)

    # ---- Utility ----
    @staticmethod
    def coord(data: dict[str, int], rlink=True):
        """Return centre coords as wikilink or plain string."""
        x = data.get("x", 0)
        y = data.get("y", 0)
        w = data.get("width", 0)
        h = data.get("height", 0)
        cx = int(x + (w / 2))
        cy = int(y + (h / 2))
        s = f"{cx}x{cy}"
        if not rlink:
            return s
        return f"[https://b42map.com/?{s} {s}]"


class RanchZone:
    """Represents a single ranch zone entry."""
    _raw_data = None
    _instances = {}
    _data_file = "parsed_ranch_zone_data.json"
    _animal_index: dict[str, list[str]] | None = None
    

    def __new__(cls, id: str):
        """Ensures only one RanchZone instance exists per RanchZone ID."""
        if not cls._raw_data:
            cls.load()

        if id in cls._instances:
            return cls._instances[id]

        instance = super().__new__(cls)
        cls._instances[id] = instance
        return instance

    def __init__(self, id: str):
        """Initialises RanchZone instance if not already initialised."""
        if hasattr(self, 'id'):
            return

        if RanchZone._raw_data is None:
           RanchZone.load()

        self.id = id
        self._data = self._raw_data.get(id, {})
        self.is_list = "possibleDef" in self._data


    @classmethod
    def _parse(cls):
        """
        Parses RanchZoneDefinitions.lua to extract ranch zone data and caches it.
        """
        lua_runtime = lua_helper.load_lua_file("RanchZoneDefinitions.lua")
        parsed_data = lua_helper.parse_lua_tables(lua_runtime)

        cls._raw_data = parsed_data.get("RanchZoneDefinitions", {}).get("type", {})
        save_cache(cls._raw_data, cls._data_file)

        cls._animal_index = None

        return cls._raw_data

    @classmethod
    def load(cls):
        """
        Loads RanchZone data from the cache, re-parsing the Lua file if the data is outdated.

        Returns:
            dict: Raw RanchZone data.
        """
        if cls._raw_data is not None:
            return cls._raw_data
        
        path = os.path.join(CACHE_DIR, cls._data_file)

        data, version = load_cache(path, cache_name="ranch zone", get_version=True)

        # Re-parse if outdated
        if version != Version.get():
            data = cls._parse()

        cls._raw_data = data or {}
        cls._animal_index = None
        return cls._raw_data
    
    @classmethod
    def all(cls) -> dict[str, "RanchZone"]:
        """
        Returns all known RanchZone instances.

        Returns:
            dict[str, RanchZone]: Mapping of item ID to RanchZone instance.
        """
        if not cls._raw_data:
            cls.load()
        return {id: cls(id) for id in cls._raw_data}
    
    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of RanchZone types parsed.

        Returns:
            int: Number of unique RanchZone types.
        """
        if not cls._raw_data:
            cls.load()
        return len(cls._raw_data)
    
    @classmethod
    def exists(cls, id: str) -> bool:
        """
        Checks if a RanchZone with the given id exists in the parsed data.

        Returns:
            bool: True if found, False otherwise.
        """
        if not cls._raw_data:
            cls.load()
        return id in cls._raw_data

    @classmethod
    def animal_index(cls) -> dict[str, list[str]]:
        """
        Return a mapping of all maleType and femaleType values to the list of corresponding ranch zones.
        """
        if cls._animal_index is not None:
            return cls._animal_index

        if not cls._raw_data:
            cls.load()

        from scripts.objects.animal import Animal

        raw = cls._raw_data or {}
        mapping: dict[str, list[str]] = defaultdict(list)

        def process_id(def_id: str, parents: set[str], visiting: set[str]):
            if not def_id or def_id in visiting:
                return
            node = raw.get(def_id)
            if not isinstance(node, dict):
                return

            if "possibleDef" in node:
                visiting.add(def_id)
                new_parents = set(parents)
                new_parents.add(def_id)
                for ref in (node.get("possibleDef") or []):
                    process_id(ref, new_parents, visiting)
                visiting.remove(def_id)
                return

            male_ok = (node.get("maxMaleNb") or 0) > 0
            female_ok = (node.get("maxFemaleNb") or 0) > 0
            chance_baby = (node.get("chanceForBaby") or 0) != 0

            mt = (node.get("maleType") or "").strip()
            ft = (node.get("femaleType") or "").strip()

            if male_ok and mt:
                mapping[mt].append(def_id)
                mapping[mt].extend(parents)

            if female_ok and ft:
                mapping[ft].append(def_id)
                mapping[ft].extend(parents)

            if chance_baby and Animal and ft:
                try:
                    baby_label = getattr(Animal(ft), "baby_type", None)
                except Exception:
                    baby_label = None
                if baby_label:
                    baby_label = str(baby_label).strip()
                    if baby_label:
                        mapping[baby_label].append(def_id)
                        mapping[baby_label].extend(parents)

        for def_id in raw.keys():
            process_id(def_id, parents=set(), visiting=set())

        cls._animal_index = {k: sorted(set(v)) for k, v in mapping.items()}
        if cls._animal_index:
            save_cache(cls._animal_index, "ranch_animal_index.json")
        return cls._animal_index


    def get(self, key: str, default=None):
        """
        Returns a raw value from the RanchZone data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)

    @property
    def is_valid(self) -> bool:
        return self.id in self._raw_data
    
    @property
    def data(self) -> dict:
        return self._data
    
    @property
    def type(self) -> str:
        return self.get("type", "")
    
    @property
    def possible_def(self) -> list[str]:
        return self.get("possibleDef", []) if self.is_list else []
    
    @property
    def def_list(self) -> list["RanchZone"]:
        return [RanchZone(d) for d in self.possible_def] if self.is_list else []
    
    @property
    def global_name(self) -> str:
        return self.data.get("globalName", "").strip() if not self.is_list else ""
    
    @property
    def chance(self) -> int:
        return self.data.get("chance", 0) if not self.is_list else 0
    
    @property
    def female_type(self) -> str:
        return self.data.get("femaleType", "") if not self.is_list else ""
    @property
    def male_type(self) -> str:
        return self.data.get("maleType", "") if not self.is_list else ""
    
    @property
    def min_female_nb(self) -> int:
        return self.data.get("minFemaleNb", 0) if not self.is_list else 0
    @property
    def max_female_nb(self) -> int:
        return self.data.get("maxFemaleNb", 0) if not self.is_list else 0
    @property
    def min_male_nb(self) -> int:
        return self.data.get("minMaleNb", 0) if not self.is_list else 0
    @property
    def max_male_nb(self) -> int:
        return self.data.get("maxMaleNb", 0) if not self.is_list else 0
    
    @property
    def forced_breed(self) -> str | None:
        return self.data.get("forcedBreed") if not self.is_list else None
    
    @property
    def chance_for_baby(self) -> int:
        return self.data.get("chanceForBaby", 0) if not self.is_list else 0
    
    @property
    def male_chance(self) -> int:
        return self.data.get("maleChance", 0) if not self.is_list else 0

    def __repr__(self):
        return f"<RanchZone {self.id}>"


if __name__ == "__main__":
#    zone = Zone("Ranch")
#    zone.dump()

#    ranch = RanchZone.load()

    RanchZone.animal_index()