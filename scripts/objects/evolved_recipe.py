"""
Evolved Recipe module.

This module defines the `EvolvedRecipe` class, which parses and represents customisable cooking recipes
from the game’s script files. It supports loading all evolved recipes, accessing recipe properties,
and linking them to compatible items and their effects.
"""

from scripts.core.file_loading import get_script_path
from scripts.core.language import Translate
from scripts.parser import script_parser
from scripts.objects.item import Item
from scripts.utils.util import link

class EvolvedRecipe:
    """
    Represents an evolved recipe parsed from Project Zomboid script files.

    Each recipe is uniquely identified by its ID and provides access to associated script
    data, result items, ingredients, and localisation metadata. Recipes are loaded once and
    cached for re-use.

    Args:
        recipe_id (str): The recipe identifier. This may be either a full ID (e.g., "Base.Soup")
                         or a short ID (e.g., "Soup"). The module prefix is stripped automatically.

    Example:
        soup = EvolvedRecipe("Soup")
        soup.name -> 'Soup'
        soup.result_item.name -> 'Pot of Soup'

    Class Methods:
        - EvolvedRecipe.all() → dict of all recipes
        - EvolvedRecipe.exists("Soup") → check if a recipe exists
        - EvolvedRecipe.keys() / values() / count() → like dict access

    Notes:
        The underlying script data is parsed from `evolvedrecipe` script blocks,
        and item links are created based on references from the `Item` class.
    """
    _recipes = None
    _instances = {}

    def __new__(cls, recipe_id: str):
        """Create or return a cached instance of an EvolvedRecipe by ID."""
        if cls._recipes is None:
            cls._load_evolved_recipes()

        if recipe_id in cls._instances:
            return cls._instances[recipe_id]

        instance = super().__new__(cls)
        cls._instances[recipe_id] = instance
        return instance
    
    def __init__(self, recipe_id: str):
        """Initialise an EvolvedRecipe instance using the provided recipe ID."""
        if hasattr(self, "recipe_id"):
            return
        
        if '.' in recipe_id:
            self.recipe_id = recipe_id.split('.', 1)
        else:
            self.recipe_id = recipe_id

        self.data:dict = EvolvedRecipe._recipes.get(recipe_id, {})
        
        self._items_list = {}

    def __getitem__(self, key):
        """Allow dict-style access to the internal data. Equivalent to `self.data[key]` or `self.data.get(key)`."""
        return self.data[key]

    def __contains__(self, key):
        """Check if a key exists in the internal data. Equivalent to `key in self.data`."""
        return key in self.data

    def __repr__(self):
        return f'<EvolvedRecipe {self.recipe_id}>'

    @classmethod
    def _load_evolved_recipes(cls):
        """Internal method to load all evolved recipes from script data and map associated items."""
        raw_data = script_parser.extract_script_data("evolvedrecipe")
        cls._recipes = {}
        for full_id, data in raw_data.items():
            if full_id == "version":
                continue
            id_type = full_id.split(".", 1)[-1]
            cls._recipes[id_type] = data

        for item in Item.all().values():
            for recipe_id, value in item.evolved_recipe.items():
                hunger, cooked = value
                recipe = cls(recipe_id)

                recipe._items_list[item.item_id] = {
                    "item": item,
                    "hunger": hunger,
                    "cooked": cooked,
                    "spice": item.spice
                }

    @classmethod
    def all(cls):
        """Return all evolved recipes as a dictionary of `{recipe_id: EvolvedRecipe}`. Similar to `dict.items()` in behaviour."""
        if cls._recipes is None:
            cls._load_evolved_recipes()
        return {recipe_id: EvolvedRecipe(recipe_id) for recipe_id in cls._recipes}

    @classmethod
    def keys(cls):
        """Return all evolved recipe IDs. Mirrors `dict.keys()` for available recipe entries."""
        if cls._recipes is None:
            cls._load_evolved_recipes()
        return cls._recipes.keys()

    @classmethod
    def values(cls):
        """Yield all `EvolvedRecipe` instances. Mirrors `dict.values()` for available recipe entries."""
        if cls._recipes is None:
            cls._load_evolved_recipes()
        return (EvolvedRecipe(recipe_id) for recipe_id in cls._recipes)

    @classmethod
    def count(cls):
        """Return the number of loaded evolved recipes. Equivalent to `len(dict)` on the full recipe mapping."""
        if cls._recipes is None:
            cls._load_evolved_recipes()
        return len(cls._recipes)

    @classmethod
    def exists(cls, recipe_id: str) -> bool:
        """Check if a given recipe ID exists in the loaded data. Similar to checking `recipe_id in dict`."""
        if cls._recipes is None:
            cls._load_evolved_recipes()
        return recipe_id in cls._recipes

    ## ------------------------- Instance Methods ------------------------- ##

    def get(self, key: str, default=None):
        """
        Return a value from the internal data dictionary. Equivalent to `self.data.get(key, default)`.

        Args:
            key (str): The key to retrieve from the internal recipe data.
            default (Any, optional): The value to return if the key is not found. Defaults to None.

        Returns:
            Any: The value associated with the key, or the default if not present.
        """
        return self.data.get(key, default)

    ## ------------------------- Properties ------------------------- ##

    @property
    def valid(self) -> bool:
        return bool(self.data)

    @property
    def script_type(self) -> str:
        return self.get("ScriptType")

    @property
    def file(self):
        return self.get("SourceFile")

    @property
    def path(self):
        return get_script_path(self.file, prefer="evolvedrecipe")

    @property
    def page(self):
        if not hasattr(self, "_page"):
            self._page = self.result_item.page
        return self._page

    @property
    def original_name(self):
        return self.get("Name")

    @property
    def display_name(self):
        return "ContextMenu_EvolvedRecipe_" + self.recipe_id

    @property
    def name(self):
        if not hasattr(self, "_name"):
            self._name = Translate.get(self.display_name)
        return self._name

    @property
    def name_en(self):
        if not hasattr(self, "_name_en"):
            self._name_en = Translate.get(self.display_name, lang_code="en")
        return self._name_en

    @property
    def wiki_link(self):
        if not hasattr(self, "_wiki_link"):
            self._wiki_link = link(self.page, self.name)
        return self._wiki_link
    
    @property
    def max_items(self):
        return self.get("MaxItems", 0)

    @property
    def result_item(self) -> Item | None:
        result = self.get("ResultItem")
        return Item(result) if result and Item.exists(result) else None

    @property
    def base_item(self) -> Item | None:
        base = self.get("BaseItem")
        return Item(base) if base and Item.exists(base) else None

    @property
    def cookable(self) -> bool:
        return self.get("Cookable", False)

    @property
    def add_ingredient_if_cooked(self) -> bool:
        return self.get("AddIngredientIfCooked", False)

    @property
    def can_add_spices_empty(self) -> bool:
        return self.get("CanAddSpicesEmpty", False)

    @property
    def add_sound(self) -> str:
        return self.get("AddIngredientSound")

    @property
    def hidden(self) -> bool:
        return self.get("Hidden", False)

    @property
    def allow_frozen(self) -> bool:
        return self.get("AllowFrozenItem", False)

    @property
    def template(self) -> str:
        return self.get("Template")

    @property
    def minimum_water(self) -> float:
        return self.get("MinimumWater", 0.0)
    
    @property
    def items_list(self) -> dict:
        """
        Return a dictionary of items that can be used in this evolved recipe.

        Each key is an item ID (str), and each value is a dictionary containing:
            - "item" (Item): The `Item` object reference.
            - "hunger" (float | int): The hunger value contributed when added.
            - "cooked" (bool): Whether the item is only valid when cooked.
            - "spice" (bool): Whether the item is a spice.

        Returns:
            dict[str, dict[str, Item | float | bool]]: Items compatible with this recipe.
        """
        return self._items_list

print(EvolvedRecipe("Soup").result_item.name)