"""Literature grouping shared by literature lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_literature_item(item: "Item") -> bool:
    """Return whether an item belongs in literature outputs."""
    return bool(
        item.valid
        and (
            item.item_type in ("literature", "map")
            or item.raw_display_category == "Literature"
        )
    )


class LiteratureGroups(ItemGroups):
    """Classify books, maps, magazines, and other literature."""

    GROUPS: dict[str, GroupInfo] = {
        "maps": GroupInfo("maps", "Maps", "literature", 1),
        "annotated_maps": GroupInfo(
            "annotated_maps", "Annotated maps", "literature", 2
        ),
        "writable": GroupInfo("writable", "Writable", "literature", 3),
        "recipe_magazines": GroupInfo(
            "recipe_magazines", "Recipe magazines", "literature", 4
        ),
        "schematics": GroupInfo(
            "schematics", "Schematics", "literature", 5
        ),
        "skill_books": GroupInfo(
            "skill_books", "Skill books", "literature", 6
        ),
        "seed_packets": GroupInfo(
            "seed_packets", "Seed packets", "literature", 7
        ),
        "hollow_books": GroupInfo(
            "hollow_books", "Hollow books", "literature", 8
        ),
        "hardcover_books": GroupInfo(
            "hardcover_books", "Hardcover books", "literature", 9
        ),
        "leatherbound_books": GroupInfo(
            "leatherbound_books", "Leatherbound books", "literature", 10
        ),
        "paperback_books": GroupInfo(
            "paperback_books", "Paperback books", "literature", 11
        ),
        "magazines": GroupInfo("magazines", "Magazines", "literature", 12),
        "newspapers": GroupInfo("newspapers", "Newspapers", "literature", 13),
        "miscellaneous": GroupInfo(
            "miscellaneous", "Miscellaneous", "literature", 14
        ),
    }

    _TYPE_MAPPING = (
        ("ComicBook", "miscellaneous"),
        ("PhotoBook", "miscellaneous"),
        ("PictureBook", "miscellaneous"),
        ("HollowBook", "hollow_books"),
        ("HollowFancyBook", "hollow_books"),
        ("BookFancy", "leatherbound_books"),
        ("Book", "hardcover_books"),
        ("Magazine", "magazines"),
        ("HottieZ", "magazines"),
        ("HunkZ", "magazines"),
        ("Newspaper", "newspapers"),
        ("Paperback", "paperback_books"),
    )

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        """Return the literature group ID for an item or annotated map."""
        special_data = kwargs.get("special_data") or {}
        if "map_id" in special_data:
            return "annotated_maps"
        if item.item_type == "map":
            return "maps"
        if item.can_be_write:
            return "writable"

        display_category = item.raw_display_category or item.item_type
        if display_category == "SkillBook":
            schematic_markers = ("Schematic", "Recipe", "SewingPattern")
            if item.teached_recipes:
                return "recipe_magazines"
            if any(marker in (item.on_create or "") for marker in schematic_markers):
                return "schematics"
            if any(marker in item.item_id for marker in schematic_markers):
                return "schematics"
            return "skill_books"
        if display_category == "Gardening":
            return "seed_packets"

        for marker, group_id in cls._TYPE_MAPPING:
            if marker in item.item_id:
                return group_id
        return "miscellaneous"

