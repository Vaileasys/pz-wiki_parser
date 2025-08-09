import os
from scripts.utils import lua_helper, util, media_helper
from scripts.core.cache import save_cache, load_cache
from scripts.core.language import Translate
from scripts.core.constants import CACHE_DIR
from scripts.core import page_manager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.objects.item import Item

class RecMedia:
    """Represents a single recorded media entry."""
    _raw_data = None
    _instances = {}
    _data_file = "parsed_recmedia_data.json"
    

    def __new__(cls, guid: str):
        """Ensures only one RecMedia instance exists per recorded media ID."""
        if not cls._raw_data:
            cls.load()

        if guid in cls._instances:
            return cls._instances[guid]

        instance = super().__new__(cls)
        cls._instances[guid] = instance
        return instance

    def __init__(self, guid: str):
        """Initialise the RecMedia instance with its data if not already initialised."""
        if hasattr(self, 'id'):
            return

        if RecMedia._raw_data is None:
           RecMedia.load()

        self.id = guid
        self._data = self._raw_data.get(guid, {})
        self._has_page = None # Page defined (bool)

    @classmethod
    def _parse(cls):
        """
        Parses RecMedia data from the provided Lua file and caches it.
        """
        lua_runtime = lua_helper.load_lua_file("recorded_media.lua")
        parsed_data = lua_helper.parse_lua_tables(lua_runtime)

        cls._raw_data = parsed_data.get("RecMedia", {})
        save_cache(cls._raw_data, cls._data_file)

        return cls._raw_data

    @classmethod
    def load(cls):
        """
        Loads RecMedia data from the cache, re-parsing the Lua file if the data is outdated.

        Returns:
            dict: Raw RecMedia data.
        """
        from scripts.core.version import Version
        if cls._raw_data is not None:
            return cls._raw_data
        
        path = os.path.join(CACHE_DIR, cls._data_file)

        data, version = load_cache(path, cache_name="recorded media", get_version=True)

        # Re-parse if outdated
        if version != Version.get():
            data = cls._parse()

        cls._raw_data = data or {}
        return cls._raw_data
    
    @classmethod
    def all(cls) -> dict[str, "RecMedia"]:
        """
        Returns all known RecMedia instances.

        Returns:
            dict[str, RecMedia]: Mapping of item ID to RecMedia instance.
        """
        if not cls._raw_data:
            cls.load()
        return {id: cls(id) for id in cls._raw_data}
    
    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of RecMedia types parsed.

        Returns:
            int: Number of unique RecMedia types.
        """
        if not cls._raw_data:
            cls.load()
        return len(cls._raw_data)
    
    @classmethod
    def exists(cls, rec_media_id: str) -> bool:
        """
        Checks if a RecMedia with the given id exists in the parsed data.

        Returns:
            bool: True if found, False otherwise.
        """
        if not cls._raw_data:
            cls.load()
        return rec_media_id in cls._raw_data
    
    @classmethod
    def get_media_items(cls) -> "list[Item]":
        if not hasattr(cls, "_media_items"):
            from scripts.objects.item import Item
            cls._media_items = []
            for _, item in Item.items():
                if item.media_category:
                    cls._media_items.append(item)
        return cls._media_items

    @classmethod
    def get_item_dict(cls) -> dict[str, list["RecMedia"]]:
        if not hasattr(cls, "_media_item_dict"):
            # Group RecMedia by category
            media_by_category = {}
            for media in cls.all().values():
                if media.category:
                    media_by_category.setdefault(media.category, []).append(media.id)

            # Only loop through items with media_category
            cls._media_item_dict = {}
            for item in cls.get_media_items():
                category = item.media_category
                if category in media_by_category:
                    cls._media_item_dict[item.item_id] = media_by_category[category]
            
            # For testing
            save_cache(cls._media_item_dict, "media_item_dict.json")

        return cls._media_item_dict
    
    @classmethod
    def get_page_dict(cls) -> dict[str, str]:
        if not hasattr(cls, "_page_dict"):
            cls._page_dict = {}
            for media in cls.all().values():
                page = media.page
                if page:
                    cls._page_dict[page] = media.id

            # For testing
            save_cache(cls._page_dict, "recmedia_page_dict.json")

        return cls._page_dict


    @classmethod
    def get_id_from_page(cls, page: str) -> str | None:
        page_dict = cls.get_page_dict()
        return page_dict.get(page)


    def get(self, key: str, default=None):
        """
        Returns a raw value from the RecMedia data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)
    
    def get_speaker_lines(self) -> list[tuple[str, "RecMediaLine"]]:
        """
        Returns a list of (speaker, RecMediaLine) tuples based on color-coded speaker identity.
        """
        speaker_map = {}
        speaker_counter = 1
        result = []

        for line in self.lines:
            color = line.color
            if color not in speaker_map:
                speaker_map[color] = f"Speaker {speaker_counter}"
                speaker_counter += 1

            speaker = speaker_map[color]
            result.append((speaker, line))

        return result

    @property
    def is_valid(self) -> bool:
        return self.id in self._raw_data
    
    @property
    def data(self) -> dict:
        return self._data
    
    @property
    def item(self) -> "Item":
        from scripts.objects.item import Item
        return Item(self.id)
    
    @property
    def name(self) -> str:
        return Translate.get(self.get("itemDisplayName"))
    
    @property
    def name_en(self) -> str:
        return Translate.get(self.get("itemDisplayName"), lang_code="en")
    
    @property
    def page(self) -> str: # TODO: get from page dict
        if not hasattr(self, "_page") or self._has_page is None:
            pages = page_manager.get_pages(query_id=self.id, id_type="rm_guid")
            if pages:
                self._page = pages[0]
                self._has_page = True
            else:
                self._page = Translate.get(self.title_id, "en")
                if self.category == "Retail-VHS" and self.subtitle_id:
                    self._page += " " + Translate.get(self.subtitle_id, "en")
                self._has_page = False

        return self._page
    
    @property
    def wiki_link(self) -> str:
        return util.link(self.page, self.name)
    
    @property
    def title_id(self) -> str:
        return self.get("title")
    
    @property
    def title(self) -> str:
        return Translate.get(self.title_id)
    
    @property
    def subtitle_id(self) -> str:
        return self.get("subtitle")
    
    @property
    def subtitle(self) -> str:
        return Translate.get(self.subtitle_id)
    
    @property
    def author_id(self) -> str:
        return self.get("author")
    
    @property
    def author(self) -> str:
        return Translate.get(self.author_id)
    
    @property
    def extra_id(self) -> str:
        return self.get("extra")
    
    @property
    def extra(self) -> str:
        return Translate.get(self.extra_id)
    
    @property
    def category(self) -> str:
        return self.get("category")
    
    @property
    def spawning(self) -> int:
        return int(self.get("spawning", 0))
    
    @property
    def lines(self) -> list["RecMediaLine"]:
        return [RecMediaLine(line) for line in self.get("lines", [])]

    def __repr__(self):
        return f"<RecMedia {self.id}>"
    

class RecMediaLine:
    """Represents a single line of recorded media content."""

    def __init__(self, data: dict):
        self.data = data

    @property
    def text_id(self) -> str:
        return self.data.get("text", "")

    @property
    def text(self) -> str:
        from scripts.core.language import Translate
        return Translate.get(self.text_id).replace("[img=music]", "♫")

    @property
    def color(self) -> tuple[float, float, float]:
        return (
            self.data.get("r", 0.0),
            self.data.get("g", 0.0),
            self.data.get("b", 0.0)
        )

    @property
    def codes(self) -> dict[str, str | int | float]:
        return media_helper.parse_code_effects(self.data.get("codes", ""))

    def __repr__(self):
        return f"<RecMediaLine text_id={self.text_id!r}>"

if __name__ == "__main__":
    recmedia = RecMedia("f74df7fc-20ae-4600-b2d2-f504d9355440")
    print(f"name: {recmedia.name}")
    print(f"title: {recmedia.title}")
    print(f"subtitle: {recmedia.subtitle}")
    print(f"author: {recmedia.author}")
    print(f"extra: {recmedia.extra}")
    print(f"category: {recmedia.category}")
    print(f"lines:")
    for speaker, line in recmedia.get_speaker_lines():
        codes = [f"{media_helper.get_code_name(code)}: {util.format_positive(value)}"
                 for code, value in line.codes.items()]

        print(f"  {speaker}: {line.text} ({', '.join(codes)})")
    #media_items = RecMedia.get_media_items()
    #print("\n".join([item.item_id for item in media_items]))

    #RecMedia.get_item_dict()