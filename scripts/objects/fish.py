"""
Parses and represents fish data from Project Zomboid's fishing system.

Extracts fish properties from the game's Lua files.
Fish instances can be created using item IDs and provide structured access to attributes.

Cached data is automatically stored and reused between sessions.
"""
import os
from scripts.utils.lua_helper import load_lua_file, parse_lua_tables
from scripts.core.cache import save_cache, load_cache
from scripts.core.constants import CACHE_DIR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.objects.item import Item

LUA_STUB = """
Events = {
    OnGameStart = { Add = function(_) end },
    OnServerStarted = { Add = function(_) end }
}

function getText(text)
    return text
end

ZombRand = function(max)
    return 0
end

ZombRandFloat = function(min, max)
    return min
end

getScriptManager = function()
    return {
        FindItem = function(_) return { getDisplayName = function() return "Fish" end } end
    }
end
"""

class Fish:
    """Represents a single fish type defined in the game’s fishing system."""
    _fishes = None
    _raw_data = None
    _instances = {}
    _data_file = "parsed_fishing_data.json"
    _fish_data_file = "parsed_fish_data.json"

    def __new__(cls, item_id: str):
        """Ensures only one Fish instance exists per item ID."""
        if not cls._fishes:
            cls.load()

        item_id = cls.fix_item_id(item_id)

        if item_id in cls._instances:
            return cls._instances[item_id]

        instance = super().__new__(cls)
        cls._instances[item_id] = instance
        return instance

    def __init__(self, item_id: str):
        """Initialise the Fish instance with its data if not already initialised."""
        if hasattr(self, 'item_id'):
            return

        if Fish._fishes is None:
           Fish.load()

        item_id = self.fix_item_id(item_id)

        self.item_id = item_id
        self._data = self._fishes.get(item_id, {})

    @classmethod
    def _parse(cls):
        """
        Parses fish data from the provided Lua file and caches it.

        Extracts entries from the 'Fishing.fishes' table and indexes them by item type.
        """

        lua_runtime = load_lua_file("fishing_properties.lua", inject_lua=LUA_STUB)
        cls._raw_data = parse_lua_tables(lua_runtime, tables="Fishing")
        save_cache(cls._raw_data, cls._data_file)

        fishes = cls._raw_data.get("Fishing", {}).get("fishes", [])

        # Index fish by itemType
        cls._fishes = {fish["itemType"]: fish for fish in fishes if "itemType" in fish}
        save_cache(cls._fishes, cls._fish_data_file)

        return cls._raw_data

    @classmethod
    def load(cls):
        """
        Loads fish data from the cache, re-parsing the Lua file if the data is outdated.

        Returns:
            dict: Mapping of item ID to fish data.
        """
        from scripts.core.version import Version
        if cls._fishes is not None:
            return cls._fishes
        
        path = os.path.join(CACHE_DIR, cls._fish_data_file)

        data, version = load_cache(path, cache_name="fishing", get_version=True)

        # Re-parse if outdated
        if version != Version.get():
            data = cls._parse()

        cls._fishes = data or {}
        return cls._fishes

    @classmethod
    def fix_item_id(cls, item_id: str) -> str:
        """
        Attempts to fix a partial item_id by assuming the 'Base' module first,
        then falling back to a full search through parsed fishes data.

        Args:
            item_id (str): Either a full item_id ('Module.Item') or just an item name.

        Returns:
            str: The best-guess full item_id.
        """
        if not cls._fishes:
            cls.load()

        if item_id is None:
            return ""

        if '.' in item_id:
            return item_id

        base_guess = f"Base.{item_id}"
        if base_guess in cls._fishes:
            return base_guess

        for full_id in cls._fishes:
            if full_id.endswith(f".{item_id}"):
                return full_id

        return item_id
    
    @classmethod
    def all(cls) -> dict[str, "Fish"]:
        """
        Returns all known fish instances.

        Returns:
            dict[str, Fish]: Mapping of item ID to Fish instance.
        """
        if not cls._fishes:
            cls.load()
        return {item_id: cls(item_id) for item_id in cls._fishes}
    
    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of fish types parsed.

        Returns:
            int: Number of unique fish types.
        """
        if not cls._fishes:
            cls.load()
        return len(cls._fishes)
    
    @classmethod
    def exists(cls, item_id: str) -> bool:
        """
        Checks if a fish with the given item id exists in the parsed data.

        Returns:
            bool: True if found, False otherwise.
        """
        if not cls._fishes:
            cls.load()
        return item_id in cls._fishes
    
    def get(self, key: str, default=None):
        """
        Returns a raw value from the fish data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)

    @property
    def is_valid(self) -> bool:
        return self.item_id in self._fishes
    
    @property
    def data(self) -> dict:
        return self._data

    @property
    def item_type(self) -> str:
        return self.get("itemType")
    
    @property
    def item(self) -> "Item":
        from scripts.objects.item import Item
        return Item(self.item_type)

    @property
    def max_length(self) -> float | None:
        return self.get("maxLength")

    @property
    def trophy_length(self) -> float | None:
        return self.get("trophyLength")

    @property
    def max_weight(self) -> float | None:
        return self.get("maxWeight")

    @property
    def trophy_weight(self) -> float | None:
        return self.get("trophyWeight")

    @property
    def is_predator(self) -> bool:
        return self.get("isPredator", False)

    @property
    def lures(self) -> dict[str, float]:
        return self.get("lure", {})

    @property
    def size_data(self) -> dict:
        return self.get("fishesSizeData", {})

    @property
    def has_sizes(self) -> bool:
        return self.get("isHaveDifferentSizes", False)

    def __repr__(self):
        return f"<Fish {self.item_type}>"


if __name__ == "__main__":
    # Intialise fish instance
    fish = Fish("Base.LargemouthBass")
    # Call a fish property
    print("Trophy weight:", fish.trophy_weight)

    # Get all of a fishes data
    fish_data = fish.data
    # Get a specific attribute from the data (better to call the property if there is one)
    trophy_weight = fish.get("trophyWeight")

    # Initialise item instance
    item = fish.item # or Item(fish.item_id)
    # call an item property
    print("Item name:", item.name)

    # Get all fish instances
    # key = item_id, value = Fish object
    all_fish = Fish.all()
    # Can then be iterated through like a normal dict
    for item_id, fish in all_fish.items():
        print(fish.item.name)
    
    # Get all the raw fishing data, not just the fish data:
    all_data = Fish.load()
    #print(all_data) #leave this example commented since it's a lot of data