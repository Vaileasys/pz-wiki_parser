"""Camping item grouping shared by camping lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_camping_item(item: "Item") -> bool:
    """Return whether an item belongs in camping outputs."""
    return bool(item.valid and item.has_category("camping"))


class CampingGroups(ItemGroups):
    """Classify tents, sleeping bags, fire starters, and other camping items."""

    GROUPS: dict[str, GroupInfo] = {
        "tent": GroupInfo("tent", "Tents", "camping", 1),
        "sleeping_bag": GroupInfo(
            "sleeping_bag", "Sleeping bags", "camping", 2
        ),
        "fire_starter": GroupInfo(
            "fire_starter", "Fire starters", "camping", 3
        ),
        "other": GroupInfo("other", "Other", "camping", 4),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        """Return the camping group ID for an item."""
        item_id = (item.item_id or "").casefold()

        if "tent" in item_id:
            return "tent"
        if "sleepingbag" in item_id:
            return "sleeping_bag"
        if item.has_tag("StartFire") or item.id_type == "PercedWood":
            return "fire_starter"
        return "other"
