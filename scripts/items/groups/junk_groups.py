"""Junk grouping shared by junk lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_junk_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("junk"))


class JunkGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "dung": GroupInfo("dung", "Dung", "junk", 1),
        "smoking": GroupInfo("smoking", "Smoking", "junk", 2),
        "literature": GroupInfo("literature", "Literature", "junk", 3),
        "broken": GroupInfo("broken", "Broken items", "junk", 4),
        "other": GroupInfo("other", "Other", "junk", 5),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.is_dung:
            return "dung"
        if (
            item.custom_context_menu == "Smoke"
            or item.has_tag("Smokable", "Tobacco", "ChewingTobacco", "RollingPaper")
            or item.id_type in ("CigarettePack", "CanPipe", "CigaretteCarton")
        ):
            return "smoking"
        if item.item_type == "literature":
            return "literature"
        if "broken" in item.id_type.casefold():
            return "broken"
        return "other"

