"""Food item grouping shared by the food list and food navbox.

The group IDs intentionally match the table keys historically produced by
``item_list_food.py``.  Keeping the classification here gives list and navbox
generation one source of truth while leaving their output formatting separate.
"""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


CRAFT_RECIPE_BLACKLIST = frozenset(
    {
        "SlicePumpkin",
        "SliceWatermelon",
        "SmashPumpkin",
        "SmashWatermelon",
        "OpenPackOfBuns",
        "OpenCandyPackage",
        "OpenMacAndCheese",
        "PutEggsInCarton",
        "OpenEggCarton",
    }
)

MISCELLANEOUS_FOOD_TYPES = frozenset(
    {
        "catfood",
        "cheese",
        "chocolate",
        "cocoa",
        "coffee",
        "dogfood",
        "noexplicit",
        "nut",
        "oil",
        "seed",
        "stock",
        "sugar",
        "tea",
        "thickener",
    }
)


def is_food_item(item: "Item") -> bool:
    """Return whether an item is defined or displayed as food."""
    return item.item_type == "food" or item.get("DisplayCategory") == "Food"


def include_in_food_groups(item: "Item") -> bool:
    """Return whether a food item belongs in the grouped list and navbox.

    These exclusions are the same ones previously applied inline by the food
    item-list generator.  Nutrition output remains broader and is therefore
    still based on :func:`is_food_item` alone.
    """
    if not is_food_item(item):
        return False

    name = item.name_en or ""

    if item.has_tag("Smokable", "Feather"):
        return False
    if (
        any(value in name for value in ("Head", "Animal"))
        and "Sunflower" not in name
    ):
        return False
    if any(value in name for value in ("Dung", "Droppings")):
        return False

    foraging_item = item.foraging
    if (
        foraging_item
        and foraging_item.has_category("MedicinalPlants", "Medical")
        and not item.hunger_change
    ):
        return False

    return item.eat_type != "pipe"


class FoodGroups(ItemGroups):
    """Classify food using recipe, FoodType, and foraging information."""

    GROUPS: dict[str, GroupInfo] = {
        "fruit": GroupInfo("fruit", "Fruit", "fresh", 1),
        "vegetable": GroupInfo("vegetable", "Vegetables", "fresh", 2),
        "grains": GroupInfo("grains", "Grains", "ingredient", 3),
        "meat": GroupInfo("meat", "Meat", "fresh", 4),
        "seafood": GroupInfo("seafood", "Seafood", "fresh", 5),
        "game": GroupInfo("game", "Game", "fresh", 6),
        "egg": GroupInfo("egg", "Eggs", "fresh", 7),
        "insect": GroupInfo("insect", "Insects", "fresh", 8),
        "candy": GroupInfo("candy", "Candy", "other", 9),
        "herb": GroupInfo("herb", "Herbs", "ingredient", 10),
        "spice": GroupInfo("spice", "Spices", "ingredient", 11),
        "plant": GroupInfo("plant", "Plants", "ingredient", 12),
        "canned": GroupInfo("canned", "Canned food", "preserved", 13),
        "pickled": GroupInfo("pickled", "Pickled food", "preserved", 14),
        "prepared": GroupInfo("prepared", "Prepared food", "prepared", 15),
        "evolved_recipes_base": GroupInfo(
            "evolved_recipes_base", "Evolved recipe bases", "prepared", 16
        ),
        "evolved_recipes": GroupInfo(
            "evolved_recipes", "Evolved recipe results", "prepared", 17
        ),
        "miscellaneous": GroupInfo(
            "miscellaneous", "Miscellaneous", "other", 18
        ),
    }

    CATEGORY_GROUPS: dict[str, list[str]] = {
        "fresh": [
            "fruit",
            "vegetable",
            "meat",
            "seafood",
            "game",
            "egg",
            "insect",
        ],
        "ingredient": ["grains", "herb", "spice", "plant"],
        "preserved": ["canned", "pickled"],
        "prepared": ["prepared", "evolved_recipes_base", "evolved_recipes"],
        "other": ["candy", "miscellaneous"],
    }

    _context_loaded = False
    _evolved_result_ids: frozenset[str] = frozenset()
    _evolved_base_ids: frozenset[str] = frozenset()
    _recipe_product_ids: frozenset[str] = frozenset()

    @staticmethod
    def _item_ids(item: "Item") -> set[str]:
        """Return the full and short IDs used by parsed recipe data."""
        return {item_id for item_id in (item.item_id, item.id_type) if item_id}

    @classmethod
    def _ensure_context_loaded(cls) -> None:
        """Build recipe-derived lookup sets once for the current process."""
        if cls._context_loaded:
            return

        from scripts.objects.craft_recipe import CraftRecipe
        from scripts.objects.evolved_recipe import EvolvedRecipe
        from scripts.utils import echo

        recipe_products: set[str] = set()
        evolved_results: set[str] = set()
        evolved_bases: set[str] = set()

        for recipe_id, recipe in CraftRecipe.all().items():
            if recipe_id in CRAFT_RECIPE_BLACKLIST or recipe.category != "Cooking":
                continue
            recipe_products.update(recipe.output_items)

        for recipe in EvolvedRecipe.values():
            result = recipe.result_item
            if result and result.valid:
                evolved_results.update(cls._item_ids(result))
            else:
                echo.warning(
                    f"EvolvedRecipe with invalid result item: {recipe.recipe_id}"
                )

            base = recipe.base_item
            if base and base.valid:
                evolved_bases.update(cls._item_ids(base))
            else:
                echo.warning(
                    f"EvolvedRecipe with invalid base item: {recipe.recipe_id}"
                )

        cls._recipe_product_ids = frozenset(recipe_products)
        cls._evolved_result_ids = frozenset(evolved_results)
        cls._evolved_base_ids = frozenset(evolved_bases)
        cls._context_loaded = True

    @classmethod
    def reset_context(cls) -> None:
        """Clear recipe-derived state so it is rebuilt on the next lookup."""
        cls._context_loaded = False
        cls._evolved_result_ids = frozenset()
        cls._evolved_base_ids = frozenset()
        cls._recipe_product_ids = frozenset()

    @classmethod
    def get_recipe_product_ids(cls) -> list[str]:
        """Return sorted cooking-recipe product IDs used for classification."""
        cls._ensure_context_loaded()
        return sorted(cls._recipe_product_ids)

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        """Return the food group ID for an item.

        The priority deliberately preserves the former ``find_table_type``
        behaviour used by the food item list.
        """
        cls._ensure_context_loaded()

        item_ids = cls._item_ids(item)
        item_type_id = item.id_type or ""
        display_name = item.name_en or ""

        if item_ids & cls._evolved_result_ids:
            return "evolved_recipes"
        if item_ids & cls._evolved_base_ids:
            return "evolved_recipes_base"
        if "Canned" in display_name or "Can of Food" in display_name:
            return "canned"
        if "Jar of" in display_name and item_type_id.startswith("Canned"):
            return "pickled"

        food_type = (item.food_type or "").casefold()
        from scripts.objects.forage import ForagingItem

        foraging_item = ForagingItem(item_type_id)

        if food_type == "egg" or item_type_id == "EggCarton":
            return "egg"
        if food_type == "candy" or item_type_id in {
            "CandyPackage",
            "Lollipop",
            "MintCandy",
            "Gum",
            "Chocolate",
        }:
            return "candy"
        if food_type == "herb" or foraging_item.has_category("WildHerbs"):
            return "herb"
        if (
            food_type
            in {
                "vegetable",
                "vegetables",
                "mushroom",
                "greens",
                "hotpepper",
                "bean",
            }
            or foraging_item.has_category("Vegetables", "Mushrooms")
            or item_type_id in {"Squash", "PumpkinSliced", "PumpkinSmashed"}
        ):
            return "vegetable"
        if food_type in {"fruits", "citrus", "berry"} or foraging_item.has_category(
            "Berries", "Fruits"
        ):
            return "fruit"
        if food_type in {
            "meat",
            "poultry",
            "bacon",
            "beef",
            "sausage",
            "venison",
        } or item_type_id == "HotdogPack":
            return "meat"
        if (
            food_type in {"seafood", "fish", "roe"}
            or item.has_tag("FishMeat")
            or "Fish" in display_name
            or item_type_id == "Mussels"
        ):
            return "seafood"
        if food_type == "insect" or foraging_item.has_category(
            "Insects", "FishBait"
        ):
            return "insect"
        if food_type == "game" or "Dead" in display_name:
            return "game"
        if item_ids & cls._recipe_product_ids:
            return "prepared"
        if food_type in {"bread", "pasta", "rice"} or item_type_id in {
            "BunsHamburger",
            "BunsHotdog",
        }:
            return "grains"
        if item.spice:
            return "spice"
        if (
            foraging_item.has_category("WildPlants")
            or any(
                value in item_type_id
                for value in (
                    "Sheaf",
                    "Rippled",
                    "Tuft",
                    "Hemp",
                    "Hops",
                    "Dried",
                )
            )
        ):
            return "plant"

        if food_type and food_type not in MISCELLANEOUS_FOOD_TYPES:
            from scripts.utils import echo

            echo.warning(
                f"FoodType '{item.food_type}' is not mapped for "
                f"'{item.item_id}'; adding item to 'Miscellaneous'."
            )

        return "miscellaneous"
