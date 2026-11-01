"""Cooking grouping shared by cooking lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_cooking_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("cooking"))


class CookingGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "mixing_utensil": GroupInfo(
            "mixing_utensil", "Mixing utensils", "cooking", 1
        ),
        "knife": GroupInfo("knife", "Knives", "cooking", 2),
        "can_bottle_opener": GroupInfo(
            "can_bottle_opener", "Can and bottle openers", "cooking", 3
        ),
        "evolved_recipe": GroupInfo(
            "evolved_recipe", "Evolved recipe containers", "cooking", 4
        ),
        "other": GroupInfo("other", "Other", "cooking", 5),
    }

    _context_loaded = False
    _evolved_recipe_links: dict[str, tuple[str, ...]] = {}

    @classmethod
    def _ensure_context_loaded(cls) -> None:
        if cls._context_loaded:
            return

        from scripts.objects.evolved_recipe import EvolvedRecipe

        links: dict[str, list[str]] = {}
        for recipe in EvolvedRecipe.values():
            base_item = recipe.base_item
            if base_item and base_item.valid:
                links.setdefault(base_item.item_id, []).append(recipe.wiki_link)

        cls._evolved_recipe_links = {
            item_id: tuple(sorted(values, key=str.casefold))
            for item_id, values in links.items()
        }
        cls._context_loaded = True

    @classmethod
    def get_evolved_recipe_links(cls, item_id: str) -> list[str]:
        cls._ensure_context_loaded()
        return list(cls._evolved_recipe_links.get(item_id, ()))

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        cls._ensure_context_loaded()
        tags = {tag.casefold() for tag in (item.tags or ())}
        if "mixingutensil" in tags:
            return "mixing_utensil"
        if tags & {"dullknife", "sharpknife", "meatcleaver", "pizzacutter"}:
            return "knife"
        if tags & {"bottleopener", "canopener"}:
            return "can_bottle_opener"
        if item.item_id in cls._evolved_recipe_links:
            return "evolved_recipe"
        return "other"

