"""Memento grouping shared by memento lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_memento_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("memento"))


class MementoGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "clothing": GroupInfo("clothing", "Clothing", "memento", 1),
        "literature": GroupInfo("literature", "Literature", "memento", 2),
        "container": GroupInfo("container", "Containers", "memento", 3),
        "fluid_container": GroupInfo(
            "fluid_container", "Fluid containers", "memento", 4
        ),
        "specimen": GroupInfo("specimen", "Specimens", "memento", 5),
        "dice": GroupInfo("dice", "Dice", "memento", 6),
        "other": GroupInfo("other", "Other", "memento", 7),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.item_type in ("clothing", "alarmclockclothing"):
            return "clothing"
        if item.item_type == "literature":
            return "literature"
        if item.item_type == "container":
            return "container"
        if item.fluid_container:
            return "fluid_container"
        if "Specimen" in item.id_type:
            return "specimen"
        if item.has_tag("Dice"):
            return "dice"
        return "other"

