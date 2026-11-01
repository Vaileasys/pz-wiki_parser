"""Medical grouping shared by medical lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_medical_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("medical"))


class MedicalGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "bandage": GroupInfo("bandage", "Bandages", "medical", 1),
        "disinfectant": GroupInfo("disinfectant", "Disinfectants", "medical", 2),
        "herb": GroupInfo("herb", "Herbs", "medical", 3),
        "poultice": GroupInfo("poultice", "Poultices", "medical", 4),
        "pharmaceutical": GroupInfo(
            "pharmaceutical", "Pharmaceuticals", "medical", 5
        ),
        "package": GroupInfo("package", "Packages", "medical", 6),
        "tools": GroupInfo("tools", "Tools", "medical", 7),
        "other": GroupInfo("other", "Other", "medical", 8),
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        if item.can_bandage:
            return "bandage"
        if item.alcohol_power or item.fluid_container.has_fluid("Alcohol"):
            return "disinfectant"
        if item.food_type == "Herb" or item.has_tag(
            "Comfrey", "HerbalTea", "Plantain", "WildGarlic"
        ):
            return "herb"
        if any(marker in item.id_type for marker in ("Cataplasm", "Poultice")):
            return "poultice"
        if item.has_tag("Pills") or item.item_type == "food":
            return "pharmaceutical"
        if item.item_type == "container" or "Box" in item.id_type:
            return "package"
        if item.has_tag(
            "RemoveBullet",
            "RemoveGlass",
            "Scissors",
            "Sharpenable",
            "MortarPestle",
        ) or "Needle" in item.id_type:
            return "tools"
        return "other"

