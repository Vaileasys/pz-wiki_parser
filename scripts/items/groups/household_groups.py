"""Household grouping shared by household lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_household_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("household"))


class HouseholdGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "writing": GroupInfo("writing", "Writing", "household", 1),
        "cleaning": GroupInfo("cleaning", "Cleaning", "household", 2),
        "other": GroupInfo("other", "Other", "household", 3),
    }

    @staticmethod
    def _replacement_has_cleaning_tag(item_id: str | None) -> bool:
        if not item_id:
            return False
        from scripts.objects.item import Item

        replacement = Item(item_id)
        return bool(replacement.valid and replacement.has_tag("CleanStains"))

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.has_tag("Write", "Eraser"):
            return "writing"
        if (
            item.has_tag("CleanStains")
            or cls._replacement_has_cleaning_tag(item.item_when_dry)
            or cls._replacement_has_cleaning_tag(item.replace_on_deplete)
            or item.id_type == "Soap2"
            or item.fluid_container.has_fluid("Bleach", "CleaningLiquid")
        ):
            return "cleaning"
        return "other"

