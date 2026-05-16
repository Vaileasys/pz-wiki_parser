"""
Provides access to randomized story outfit usage data.

OutfitStory loads parsed randomized story data and provides helpers for finding
which stories reference a given outfit ID.
"""

from scripts.objects.outfit import Outfit
from scripts.parser import outfit_story_parser


class OutfitStory:
    """Provides cached lookup for outfit usage in randomized stories."""
    _data: dict | None = None

    @classmethod
    def load(cls, force: bool = False) -> dict:
        """
        Load outfit story data.

        Args:
            force: Reload data even if already loaded.
        """
        if cls._data is not None and not force:
            return cls._data

        cls._data = outfit_story_parser.parse_outfit_stories(
            Outfit.load(),
            force_regenerate=force,
        )

        return cls._data

    @classmethod
    def all(cls) -> dict:
        """Return all outfit story data."""
        return cls.load()

    @classmethod
    def get(cls, outfit_id: str) -> list[dict]:
        """
        Return stories that reference an outfit ID.

        Args:
            outfit_id: Outfit ID to search for.
        """
        data = cls.load()
        return data.get("outfit_to_stories", {}).get(outfit_id, [])

    @classmethod
    def has(cls, outfit_id: str) -> bool:
        """
        Check whether an outfit appears in any story.

        Args:
            outfit_id: Outfit ID to check.
        """
        return bool(cls.get(outfit_id))

    @classmethod
    def story_types(cls) -> dict:
        """Return story data grouped by story type."""
        data = cls.load()
        return data.get("story_types", {})

    @classmethod
    def outfit_to_stories(cls) -> dict:
        """Return story data grouped by outfit ID."""
        data = cls.load()
        return data.get("outfit_to_stories", {})