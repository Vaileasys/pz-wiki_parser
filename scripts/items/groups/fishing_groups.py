"""Fishing grouping shared by fishing lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_fishing_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("fishing"))


class FishingGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "tackle": GroupInfo("tackle", "Tackle", "fishing", 1),
        "gear": GroupInfo("gear", "Gear", "fishing", 2),
        "fish": GroupInfo("fish", "Fish", "fishing", 3),
        "other": GroupInfo("other", "Other", "fishing", 4),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if (
            item.has_tag("FishingHook", "FishingLine")
            or item.fishing_lure
            or item.id_type in ("Bobber", "FishingHookBox")
        ):
            return "tackle"
        if item.has_tag("FishingSpear", "FishingRod", "FishingNet") or (
            item.id_type in ("FishingRodBreak", "BrokenFishingNet")
        ):
            return "gear"
        if item.fish:
            return "fish"
        return "other"

