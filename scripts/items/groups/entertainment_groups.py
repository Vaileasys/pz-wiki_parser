"""Entertainment grouping shared by item lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_entertainment_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("entertainment"))


class EntertainmentGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "entertainment": GroupInfo(
            "entertainment", "Entertainment", "entertainment", 1
        ),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        return "entertainment"

