import os
from scripts.utils import lua_helper, util
from scripts.core.cache import save_cache, load_cache
from scripts.core.constants import CACHE_DIR

class AnimalGene:
    _raw_data: dict | None = None
    _genes_data: dict | None = None
    _instances: dict[str, "AnimalGene"] = {}
    _data_file = "parsed_animal_genes_data.json"

    def __new__(cls, gene_id: str):
        if not cls._genes_data:
            cls.load()
        if gene_id in cls._instances:
            return cls._instances[gene_id]
        inst = super().__new__(cls)
        cls._instances[gene_id] = inst
        return inst

    def __init__(self, gene_id: str):
        if hasattr(self, "gene_id"):
            return
        if AnimalGene._genes_data is None:
            AnimalGene.load()
        self.gene_id = gene_id
        self._data:dict = AnimalGene._genes_data.get(gene_id, {})

    @classmethod
    def from_forced_gene(cls, gene_id: str, data: dict) -> "AnimalGene":
        """
        Create/update a gene with an explicit range and mark it as forced.

        Accepts {"min": x, "max": y} or {"minValue": x, "maxValue": y}.
        """
        # Ensure class data is loaded so normal instances behave consistently
        if cls._genes_data is None:
            cls.load()

        # Reuse the singleton instance for this gene_id
        inst = cls(gene_id)

        # Extract values with flexible keys
        min_v = data.get("min", data.get("minValue"))
        max_v = data.get("max", data.get("maxValue"))
        if min_v is None or max_v is None:
            raise ValueError("from_forced_gene requires 'min'/'max' or 'minValue'/'maxValue'.")

        # Ensure numeric
        min_v = float(min_v)
        max_v = float(max_v)

        # Overwrite/augment the instance data
        base = inst._data if isinstance(inst._data, dict) else {}
        inst._data = {
            **base,
            "minValue": min_v,
            "maxValue": max_v,
            "forcedValues": True,
        }
        inst._is_forced = True
        return inst

    # ----- parse/load -----

    @staticmethod
    def _split_commas(obj: object):
        if isinstance(obj, dict):
            return {k: AnimalGene._split_commas(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [AnimalGene._split_commas(v) for v in obj]
        if isinstance(obj, str) and "," in obj:
            return [s.strip() for s in obj.split(",")]
        return obj

    @classmethod
    def _parse(cls) -> dict:
        lua_runtime = lua_helper.load_lua_file("AnimalGenomeDefinitions.lua")
        parsed = lua_helper.parse_lua_tables(lua_runtime)
        data: dict = parsed.get("AnimalGenomeDefinitions", {})
        data = cls._split_commas(data)
        save_cache(data, cls._data_file)
        return data

    @classmethod
    def load(cls, attribute: str | None = None):
        """Load from cache, re-parse if version changed."""
        from scripts.core.version import Version
        if cls._raw_data is None:
            path = os.path.join(CACHE_DIR, cls._data_file)
            data, version = load_cache(path, cache_name="animal genes", get_version=True)
            if version != Version.get():
                data = cls._parse()

            # Normalise lists
            genes = data.get("genes", {})
            for k, v in genes.items():
                if isinstance(v, list):
                    genes[k] = {}

            cls._raw_data = data
            cls._genes_data = (cls._raw_data or {}).get("genes", {}) or {}
        if attribute is not None and hasattr(cls, attribute):
            return getattr(cls, attribute)
        return cls._genes_data

    # ----- lookups -----

    @classmethod
    def all(cls) -> dict[str, "AnimalGene"]:
        if not cls._genes_data:
            cls.load()
        return {gid: cls(gid) for gid in cls._genes_data}

    @classmethod
    def count(cls) -> int:
        if not cls._genes_data:
            cls.load()
        return len(cls._genes_data)

    @classmethod
    def exists(cls, gene_id: str) -> bool:
        if not cls._genes_data:
            cls.load()
        return gene_id in cls._genes_data

    # ----- accessors -----

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    @property
    def data(self) -> dict:
        return self._data

    @property
    def is_valid(self) -> bool:
        return self.gene_id in (AnimalGene._genes_data or {})
    
    @property
    def name(self) -> str:
        if not hasattr(self, "_name"):
            self._name = util.split_camel_case(self.gene_id).capitalize()
        return self._name

    @property
    def has_range(self) -> bool:
        return "minValue" in self._data or "maxValue" in self._data

    @property
    def min_value(self) -> float:
        return self._data.get("minValue", 0.2)

    @property
    def max_value(self) -> float:
        return self._data.get("maxValue", 0.6)
    
    @property
    def is_forced(self) -> bool:
        # True only when created via from_forced_gene
        return getattr(self, "_is_forced", False)

    @property
    def forced_values(self) -> bool:
        return bool(self._data.get("forcedValues", False))

    @property
    def dominance(self) -> str:
        return "Dominant" if self.forced_values else "Random"

    @property
    def ratio(self) -> dict:
        return self._data.get("ratio", {}) or {}

    def clamp(self, value: float) -> float:
        """Clamp to [minValue, maxValue] when provided."""
        lo = self.min_value
        hi = self.max_value
        if lo is not None and value < lo:
            return lo
        if hi is not None and value > hi:
            return hi
        return value

    def __repr__(self):
        return f"<AnimalGene {self.gene_id}>"


class AnimalGeneticDisorder:
    _disorders_data: dict | None = None
    _instances: dict[str, "AnimalGeneticDisorder"] = {}

    def __new__(cls, disorder_id: str):
        if not cls._disorders_data:
            cls.load()
        if disorder_id in cls._instances:
            return cls._instances[disorder_id]
        inst = super().__new__(cls)
        cls._instances[disorder_id] = inst
        return inst

    def __init__(self, disorder_id: str):
        if hasattr(self, "disorder_id"):
            return
        if AnimalGeneticDisorder._disorders_data is None:
            AnimalGeneticDisorder.load()
        self.disorder_id = disorder_id
        self._value = AnimalGeneticDisorder._disorders_data.get(disorder_id)

    @classmethod
    def load(cls):
        """Load disorders from AnimalGene data."""
        if cls._disorders_data is None:
            raw = AnimalGene.load(attribute="_raw_data")
            cls._disorders_data = (raw or {}).get("geneticDisorder", {}) or {}
        return cls._disorders_data

    @classmethod
    def all(cls) -> dict[str, "AnimalGeneticDisorder"]:
        if not cls._disorders_data:
            cls.load()
        return {k: cls(k) for k in cls._disorders_data}

    @classmethod
    def count(cls) -> int:
        if not cls._disorders_data:
            cls.load()
        return len(cls._disorders_data)

    @classmethod
    def exists(cls, disorder_id: str) -> bool:
        if not cls._disorders_data:
            cls.load()
        return disorder_id in cls._disorders_data

    @property
    def is_valid(self) -> bool:
        return self.disorder_id in (AnimalGeneticDisorder._disorders_data or {})

    @property
    def value(self) -> str | None:
        """Raw value (mirrors the key in current data)."""
        return self._value

    def __repr__(self):
        return f"<AnimalGeneticDisorder {self.disorder_id}>"