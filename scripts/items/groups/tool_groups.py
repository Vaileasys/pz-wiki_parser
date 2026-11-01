"""Tool grouping shared by tool lists and navboxes."""

from __future__ import annotations

import re
import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_tool_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("tool"))


class ToolGroups(ItemGroups):
    """Group tools into every crafting category in which they are used."""

    GROUPS: dict[str, GroupInfo] = {}
    _context_loaded = False
    _item_categories: dict[str, frozenset[str]] = {}
    _category_to_group: dict[str, str] = {}

    @staticmethod
    def _normalise_type_id(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_") or "other"

    @classmethod
    def _ensure_context_loaded(cls) -> None:
        if cls._context_loaded:
            return

        from scripts.objects.craft_recipe import CraftRecipe

        item_categories: dict[str, set[str]] = {}
        all_categories = {"Cooking", "Farming", "Fishing", "Medical", "Other"}
        for recipe in CraftRecipe.values():
            category = recipe.category
            if not category:
                continue
            all_categories.add(category)
            for item_id in recipe.input_items:
                item_categories.setdefault(item_id, set()).add(category)

        ordered_categories = sorted(
            all_categories,
            key=lambda value: (value.casefold() == "other", value.casefold()),
        )
        groups: dict[str, GroupInfo] = {}
        category_to_group: dict[str, str] = {}
        for display_order, category in enumerate(ordered_categories, start=1):
            group_id = cls._normalise_type_id(category)
            category_to_group[category] = group_id
            groups[group_id] = GroupInfo(
                group_id, category, "tool", display_order
            )

        cls.GROUPS = groups
        cls._category_to_group = category_to_group
        cls._item_categories = {
            item_id: frozenset(categories)
            for item_id, categories in item_categories.items()
        }
        cls._context_loaded = True

    @classmethod
    def get_categories(cls, item: "Item") -> list[str]:
        cls._ensure_context_loaded()
        categories = set(cls._item_categories.get(item.item_id, ()))
        if item.has_category("fishing"):
            categories.add("Fishing")
        if item.has_category("cooking"):
            categories.add("Cooking")
        if item.has_category("gardening"):
            categories.add("Farming")
        if item.has_category("medical"):
            categories.add("Medical")
        return sorted(categories, key=str.casefold) if categories else ["Other"]

    @classmethod
    def get_group_ids(cls, item: "Item") -> list[str]:
        cls._ensure_context_loaded()
        return [cls._category_to_group[category] for category in cls.get_categories(item)]

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        return cls.get_group_ids(item)[0]

