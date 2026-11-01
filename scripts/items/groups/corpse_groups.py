"""Corpse grouping shared by corpse lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_corpse_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("corpse"))


class CorpseGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "corpse": GroupInfo("corpse", "Corpses", "corpse", 1),
        "animal_dead": GroupInfo("animal_dead", "Dead animals", "corpse", 2),
        "animal_skeleton": GroupInfo(
            "animal_skeleton", "Animal skeletons", "corpse", 3
        ),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.item_id == "Base.CorpseAnimal":
            stage = kwargs.get("stage") or "dead"
            return f"animal_{stage}"
        return "corpse"

