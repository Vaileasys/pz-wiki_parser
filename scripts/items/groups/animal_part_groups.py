"""Animal-part grouping shared by animal-part lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


class AnimalPartGroups(ItemGroups):
    """Classify animal-derived items using tags and husbandry definitions."""

    GROUPS: dict[str, GroupInfo] = {
        "animal_skull": GroupInfo(
            "animal_skull", "Skulls", "animal_part", 1
        ),
        "animal_head": GroupInfo("animal_head", "Heads", "animal_part", 2),
        "feather": GroupInfo("feather", "Feathers", "animal_part", 3),
        "brain": GroupInfo("brain", "Brains", "animal_part", 4),
        "bone": GroupInfo("bone", "Bones", "animal_part", 5),
        "meat": GroupInfo("meat", "Meat", "animal_part", 6),
        "leather": GroupInfo("leather", "Leather", "animal_part", 7),
        "other": GroupInfo("other", "Other", "animal_part", 8),
    }

    _context_loaded = False
    _item_ids: frozenset[str] = frozenset()
    _definition_groups: dict[str, frozenset[str]] = {}

    @classmethod
    def _ensure_context_loaded(cls) -> None:
        """Build animal-definition lookup sets once for the current process."""
        if cls._context_loaded:
            return

        from scripts.objects.animal_part import AnimalPart
        from scripts.objects.item import Item

        item_ids: set[str] = set()
        definition_groups: dict[str, set[str]] = {
            "bone": set(),
            "leather": set(),
            "animal_head": set(),
            "animal_skull": set(),
        }

        for animal_part in AnimalPart.all().values():
            item_ids.update(animal_part.all_parts)
            definition_groups["bone"].update(animal_part.bone_items)

            for group_id, part_item in (
                ("leather", animal_part.leather),
                ("animal_head", animal_part.head),
                ("animal_skull", animal_part.skull),
            ):
                if part_item and part_item.valid:
                    definition_groups[group_id].add(part_item.item_id)

        for item_id, item in Item.items():
            if item.has_category("animal_part"):
                item_ids.add(item_id)

        cls._item_ids = frozenset(item_ids)
        cls._definition_groups = {
            group_id: frozenset(group_item_ids)
            for group_id, group_item_ids in definition_groups.items()
        }
        cls._context_loaded = True

    @classmethod
    def reset_context(cls) -> None:
        """Clear animal-definition state so it reloads on the next lookup."""
        cls._context_loaded = False
        cls._item_ids = frozenset()
        cls._definition_groups = {}

    @classmethod
    def get_item_ids(cls) -> list[str]:
        """Return every item ID included in animal-part outputs."""
        cls._ensure_context_loaded()
        return sorted(cls._item_ids, key=str.casefold)

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        """Return the animal-part group ID for an item."""
        from scripts.objects.animal_part import AnimalMeat

        cls._ensure_context_loaded()

        if item.has_tag("AnimalSkull"):
            return "animal_skull"
        if item.has_tag("AnimalHead"):
            return "animal_head"
        if item.has_tag("Feather"):
            return "feather"
        if item.has_tag("AnimalBrain"):
            return "brain"
        if item.has_tag("AnimalBone", "LargeAnimalBone"):
            return "bone"
        if (
            AnimalMeat.exists(item.item_id)
            or item.food_type in ("Poultry", "Game")
            or item.has_tag("Vermin")
        ):
            return "meat"

        for group_id in ("bone", "leather", "animal_head", "animal_skull"):
            if item.item_id in cls._definition_groups.get(group_id, ()):
                return group_id

        return "other"
