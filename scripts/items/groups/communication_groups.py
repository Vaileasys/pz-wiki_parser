"""Communication grouping shared by item lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_communication_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("communication"))


class CommunicationGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "television": GroupInfo("television", "Televisions", "communication", 1),
        "two_way": GroupInfo("two_way", "Two-way radios", "communication", 2),
        "radio": GroupInfo("radio", "Radios", "communication", 3),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.is_television:
            return "television"
        if item.two_way:
            return "two_way"
        return "radio"

