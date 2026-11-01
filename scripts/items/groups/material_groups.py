"""Material grouping shared by material lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_material_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("material"))


class MaterialGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        group_id: GroupInfo(group_id, display_name, "material", order)
        for order, (group_id, display_name) in enumerate(
            (
                ("tool_head", "Tool heads"),
                ("leather", "Leather"),
                ("denim", "Denim"),
                ("paint", "Paint"),
                ("wallpaper", "Wallpaper"),
                ("iron", "Iron"),
                ("steel", "Steel"),
                ("copper", "Copper"),
                ("clay", "Clay"),
                ("brass", "Brass"),
                ("silver", "Silver"),
                ("gold", "Gold"),
                ("aluminum", "Aluminum"),
                ("glass", "Glass"),
                ("stone", "Stone"),
                ("cotton", "Cotton"),
                ("fibre", "Fibre"),
                ("repair", "Repair materials"),
                ("bone", "Bone"),
                ("wood", "Wood"),
                ("charcoal", "Charcoal"),
                ("other", "Other"),
            ),
            start=1,
        )
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        item_id = item.id_type
        if item.has_tag("ToolHead", "SawBlade") or (
            ("Head" in item_id or "Blade" in item_id) and "Broken" not in item_id
        ):
            return "tool_head"
        if (
            item.has_tag(
                "LeatherCrudeLarge",
                "LeatherCrudeWetLarge",
                "LeatherCrudeTannedLarge",
                "LeatherCrudeMedium",
                "LeatherCrudeWetMedium",
                "LeatherCrudeTannedMedium",
                "LeatherCrudeSmall",
                "LeatherCrudeWetSmall",
                "LeatherCrudeTannedSmall",
                "LeatherFurLarge",
                "LeatherFurWetLarge",
                "LeatherFurTannedLarge",
                "LeatherFurMedium",
                "LeatherFurWetMedium",
                "LeatherFurTannedMedium",
                "LeatherFurSmall",
                "LeatherFurWetSmall",
                "LeatherFurTannedSmall",
                "LeatherFullLarge",
                "LeatherFullMedium",
                "LeatherFullSmall",
            )
            or "Leather" in item_id
            or item.fabric_type == "Leather"
            or "Hide" in item_id
        ):
            return "leather"
        if "Denim" in item_id:
            return "denim"
        if item.get("DisplayCategory") == "Paint":
            return "paint"
        if item.has_tag("Wallpaper"):
            return "wallpaper"
        if "Iron" in item_id or "Hematite" in item_id or item.has_tag(
            "SmeltableIronLarge",
            "SmeltableIronMedium",
            "SmeltableIronMediumPlus",
            "SmeltableIronSmall",
        ):
            return "iron"
        if "Steel" in item_id or item.has_tag(
            "SmeltableSteelLarge",
            "SmeltableSteelMedium",
            "SmeltableSteelMediumPlus",
            "SmeltableSteelSmall",
        ):
            return "steel"
        if "Copper" in item_id or "Malachite" in item_id:
            return "copper"
        if (
            "Clay" in item_id or "Ceramic" in item_id or "Unfired" in item_id
        ) and "CrucibleWith" not in item_id:
            return "clay"
        if "Brass" in item_id:
            return "brass"
        if "Silver" in item_id:
            return "silver"
        if "Gold" in item_id:
            return "gold"
        if "Aluminum" in item_id or item.has_tag("Aluminum", "ScrapAluminum"):
            return "aluminum"
        if "Glass" in item_id:
            return "glass"
        if (
            "Stone" in item_id
            or "Limestone" in item_id
            or "Quicklime" in item_id
            or item.has_tag("Stone", "Limestone")
        ):
            return "stone"
        if "Sheet" in item_id or "Cotton" in item_id:
            return "cotton"
        if (
            item.has_tag("Thread", "HeavyThread", "Twine")
            or "Flax" in item_id
            or "Hemp" in item_id
            or "Burlap" in item_id
            or "Dogbane" in item_id
            or "String" in item_id
            or "Rope" in item_id
            or "Yarn" in item_id
            or "WoolRaw" in item_id
            or "CheeseCloth" in item_id
        ):
            return "fibre"
        if item.has_tag("Glue", "Tape", "FiberglassTape", "Epoxy") or (
            "Zipties" in item_id
        ):
            return "repair"
        if item.has_tag("AnimalBone", "LargeAnimalBone") or "Bone" in item_id:
            return "bone"
        if (
            "Wood" in item_id
            or "Twigs" in item_id
            or "Firewood" in item_id
            or "LogStack" in item_id
            or "Branch" in item_id
            or "Plank" in item_id
            or item.has_tag(
                "WoodHandle",
                "Log",
                "LongStick",
                "MakeWoodCharcoalLarge",
                "MakeWoodCharcoalSmall",
                "MakeWoodCharcoalMedium",
            )
        ):
            return "wood"
        if item.has_tag("Charcoal"):
            return "charcoal"
        return "other"

