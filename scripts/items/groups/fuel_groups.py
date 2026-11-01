"""Fuel grouping shared by fuel lists and navboxes."""

from __future__ import annotations

import re
import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_fuel_item(item: "Item") -> bool:
    return bool(item.valid and item.burn_time)


class FuelGroups(ItemGroups):
    """Classify fuels while preserving the legacy table headings."""

    GROUPS: dict[str, GroupInfo] = {
        "literature": GroupInfo(
            "literature", "Literature", "fuel", 1,
            metadata={"table_type": "Literature"},
        ),
        "miscellaneous": GroupInfo(
            "miscellaneous", "Miscellaneous", "fuel", 2,
            metadata={"table_type": "Miscellaneous"},
        ),
    }
    _next_order = 3

    @staticmethod
    def _normalise_type_id(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_") or "other"

    @classmethod
    def _ensure_type_group(cls, item_type: str) -> str:
        group_id = cls._normalise_type_id(item_type)
        if group_id not in cls.GROUPS:
            cls.GROUPS[group_id] = GroupInfo(
                group_id,
                item_type.replace("_", " ").capitalize(),
                "fuel",
                cls._next_order,
                metadata={"table_type": item_type},
            )
            cls._next_order += 1
        return group_id

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.item_type == "map":
            return "literature"
        if item.item_type in ("food", "drainable", "normal", "moveable"):
            return "miscellaneous"
        return cls._ensure_type_group(item.item_type or "other")

    @classmethod
    def get_table_type(cls, group_id: str) -> str:
        group = cls.get_group_info(group_id)
        return group.metadata.get("table_type", group_id) if group else group_id

