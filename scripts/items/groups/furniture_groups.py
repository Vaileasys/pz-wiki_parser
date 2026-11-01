"""Grouping helpers for the tile-backed furniture list and navbox."""

from __future__ import annotations

from scripts.items.item_groups import GroupInfo, ItemGroups


class FurnitureGroups(ItemGroups):
    """Classify a representative furniture tile using the list rules."""

    GROUPS: dict[str, GroupInfo] = {
        "appliances": GroupInfo("appliances", "Appliances", "furniture", 1),
        "plumbing": GroupInfo("plumbing", "Plumbing", "furniture", 2),
        "comfort": GroupInfo("comfort", "Comfort", "furniture", 3),
        "tables": GroupInfo("tables", "Tables", "furniture", 4),
        "storage": GroupInfo("storage", "Storage", "furniture", 5),
        "workstations": GroupInfo(
            "workstations", "Workstations", "furniture", 6
        ),
        "floors": GroupInfo("floors", "Floors", "furniture", 7),
        "decorations": GroupInfo(
            "decorations", "Decorations", "furniture", 8
        ),
        "signs": GroupInfo("signs", "Signs", "furniture", 9),
        "trash": GroupInfo("trash", "Trash", "furniture", 10),
        "plants": GroupInfo("plants", "Plants", "furniture", 11),
        "miscellaneous": GroupInfo(
            "miscellaneous", "Miscellaneous", "furniture", 12
        ),
    }

    _DISPLAY_TO_TYPE = {
        group.display_name: type_id for type_id, group in GROUPS.items()
    }

    @staticmethod
    def is_included(tile: dict) -> bool:
        """Return whether a representative tile is not blacklisted."""
        from scripts.lists.furniture_list import _is_blacklisted

        return not _is_blacklisted(tile)

    @classmethod
    def classify(cls, tile: dict, **kwargs) -> str:
        """Return the first matching top-level furniture category."""
        from scripts.lists.furniture_list import CATEGORIES, _matches

        generic = tile.get("properties", {}).get("generic", {})

        for display_name, subcategories in CATEGORIES.items():
            if isinstance(subcategories, dict):
                for subsection_name, rules in subcategories.items():
                    if display_name == "Comfort" and subsection_name == "Beds":
                        custom_name = str(generic.get("CustomName", "")).casefold()
                        if generic.get("BedType") is not None and (
                            "bed" in custom_name or "mattress" in custom_name
                        ):
                            return cls._DISPLAY_TO_TYPE[display_name]

                    if any(_matches(tile, rule) for rule in rules):
                        return cls._DISPLAY_TO_TYPE[display_name]
            elif any(_matches(tile, rule) for rule in subcategories):
                return cls._DISPLAY_TO_TYPE[display_name]

        return "miscellaneous"
