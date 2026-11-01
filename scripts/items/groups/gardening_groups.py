"""Gardening grouping shared by gardening lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_gardening_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("gardening"))


class GardeningGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "seed": GroupInfo("seed", "Seeds", "gardening", 1),
        "seed_packet": GroupInfo("seed_packet", "Seed packets", "gardening", 2),
        "plant": GroupInfo("plant", "Plants", "gardening", 3),
        "tool": GroupInfo("tool", "Tools", "gardening", 4),
        "other": GroupInfo("other", "Other", "gardening", 5),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.has_tag("isSeed"):
            return "seed"
        if item.teached_recipes:
            return "seed_packet"
        if item.item_type in ("moveable", "food"):
            return "plant"
        if item.has_tag("TakeDirt", "TakeDung", "DigPlow", "Scythe", "CutPlant"):
            return "tool"
        return "other"

