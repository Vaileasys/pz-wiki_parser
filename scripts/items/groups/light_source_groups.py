"""Light-source grouping shared by item lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_light_source_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("light_source"))


class LightSourceGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "light_source": GroupInfo(
            "light_source", "Light sources", "light_source", 1
        ),
        "other": GroupInfo("other", "Other", "light_source", 2),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.light_distance and item.light_strength:
            return "light_source"
        return "other"

