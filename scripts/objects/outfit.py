"""
Provides cached access to parsed Project Zomboid outfit data.

The Outfit class wraps male/female outfit definitions, resolves wiki page names,
and exposes common outfit properties such as GUIDs, item lists, sex availability,
and navbox grouping.
"""

import scripts.parser.outfit_parser as outfit_parser
from scripts.core import cache, page_manager
from scripts.core.version import Version
from scripts.utils import echo


class Outfit:
    """Represents a single outfit definition from the parsed outfit cache."""
    
    _data: dict | None = None
    _page_dict: dict | None = None
    _instances: dict[str, "Outfit"] = {}

    def __new__(cls, outfit_id: str):
        """
        Create or reuse an Outfit instance.

        Args:
            outfit_id: Outfit ID.
        """
        if cls._data is None:
            cls.load()

        if outfit_id in cls._instances:
            return cls._instances[outfit_id]

        instance = super().__new__(cls)
        cls._instances[outfit_id] = instance
        return instance

    def __init__(self, outfit_id: str):
        """
        Initialise the outfit instance.

        Args:
            outfit_id: Outfit ID.
        """
        if hasattr(self, "_outfit_id"):
            return

        self._outfit_id = outfit_id

    @classmethod
    def load(cls, force: bool = False):
        """
        Load outfit data from cache, regenerating if outdated.

        Args:
            force: Reload data even if already loaded.
        """
        if cls._data is not None and not force:
            return cls._data

        cached_data, cache_version = cache.load_cache("outfits.json", get_version=True)

        if cache_version == Version.get():
            echo.info("Outfit cache is up to date")
            cls._data = cached_data
        else:
            echo.info("Regenerating outfit cache...")
            outfit_parser.main()
            cls._data, _ = cache.load_cache("outfits.json", get_version=True)

        echo.success(
            f"Loaded {len(cls._data.get('FemaleOutfits', {}))} female outfits, "
            f"{len(cls._data.get('MaleOutfits', {}))} male outfits"
        )

        return cls._data

    @classmethod
    def load_pages(cls, force: bool = False):
        """
        Load flattened page data used for outfit page lookup.

        Args:
            force: Reload page data even if already loaded.
        """
        if cls._page_dict is not None and not force:
            return cls._page_dict

        page_manager.init()
        cls._page_dict = page_manager.get_flattened_page_dict()
        return cls._page_dict

    @classmethod
    def all(cls) -> dict[str, "Outfit"]:
        """Return all outfits keyed by outfit ID."""
        if cls._data is None:
            cls.load()

        outfit_ids = set()
        outfit_ids.update(cls._data.get("MaleOutfits", {}).keys())
        outfit_ids.update(cls._data.get("FemaleOutfits", {}).keys())

        return {
            outfit_id: cls(outfit_id)
            for outfit_id in sorted(outfit_ids, key=str.casefold)
        }

    @classmethod
    def values(cls):
        """Return all outfit instances."""
        return cls.all().values()

    @classmethod
    def keys(cls):
        """Return all outfit IDs."""
        return cls.all().keys()

    @property
    def outfit_id(self) -> str:
        """Outfit ID."""
        return self._outfit_id

    @property
    def male_data(self) -> dict:
        """Male outfit data."""
        return self._data.get("MaleOutfits", {}).get(self.outfit_id, {})

    @property
    def female_data(self) -> dict:
        """Female outfit data."""
        return self._data.get("FemaleOutfits", {}).get(self.outfit_id, {})

    @property
    def has_male(self) -> bool:
        """Whether the outfit has a male definition."""
        return bool(self.male_data)

    @property
    def has_female(self) -> bool:
        """Whether the outfit has a female definition."""
        return bool(self.female_data)

    @property
    def sex(self) -> str:
        """Sex availability: Both, Male, Female, or blank."""
        if self.has_male and self.has_female:
            return "Both"

        if self.has_male:
            return "Male"

        if self.has_female:
            return "Female"

        return ""

    @property
    def navbox_section(self) -> str:
        """Navbox section name for this outfit."""
        if self.sex == "Both":
            return "Unisex outfits"

        if self.sex == "Male":
            return "Male outfits"

        if self.sex == "Female":
            return "Female outfits"

        return "Outfits"

    @property
    def page(self) -> str:
        """Wiki page name for this outfit, falling back to outfit ID."""
        page_dict = self.load_pages()

        for page_name, page_data in page_dict.items():
            outfit_ids = page_data.get("outfit_id")

            if not outfit_ids:
                continue

            if isinstance(outfit_ids, str):
                outfit_ids = [outfit_ids]

            if self.outfit_id in outfit_ids:
                return page_name

        return self.outfit_id

    @property
    def guids(self) -> list[str]:
        """All GUIDs for this outfit."""
        guids = []

        if self.male_guid:
            guids.append(self.male_guid)

        if self.female_guid:
            guids.append(self.female_guid)

        return guids

    @property
    def male_guid(self) -> str:
        """Male outfit GUID."""
        return self.male_data.get("GUID", "")

    @property
    def female_guid(self) -> str:
        """Female outfit GUID."""
        return self.female_data.get("GUID", "")

    @property
    def male_items(self) -> dict:
        """Items used by the male outfit definition."""
        return self.male_data.get("Items", {})

    @property
    def female_items(self) -> dict:
        """Items used by the female outfit definition."""
        return self.female_data.get("Items", {})

    @property
    def valid(self) -> bool:
        """Whether the outfit has male or female data."""
        return self.has_male or self.has_female

    def __repr__(self):
        """Return debug representation."""
        return f"<Outfit {self.outfit_id}>"