from scripts.utils import echo
from scripts.parser import script_parser
from scripts.core.file_loading import get_script_path
from scripts.core.language import Language, Translate
from scripts.objects.item import Item
from scripts.utils.util import link, to_bool


class CraftRecipeInput:
    def __init__(self, data: dict, recipe: "CraftRecipe"):
        self.data = data
        self.recipe = recipe

    @property
    def items(self) -> list[str]:
        return self.data.get("items")

    @property
    def count(self) -> int:
        return int(self.data.get("count", 1))

    @property
    def mode(self) -> int:
        return int(self.data.get("mode"))

    @property
    def flags(self) -> list[str]:
        return int(self.data.get("flags"))

    @property
    def tags(self) -> list[str]:
        return self.data.get("tags")

    def __repr__(self):
        return f"<CraftRecipeInput {recipe.recipe_id}>"


class CraftRecipeOutput:
    def __init__(self, data: dict, recipe: "CraftRecipe"):
        self.data = data
        self.recipe = recipe

    @property
    def items(self) -> list[str]:
        return self.data.get("items", [])

    @property
    def mapper(self) -> str | None:
        return self.data.get("mapper")

    @property
    def count(self) -> int:
        return int(self.data.get("count", 1))

    def __repr__(self):
        return f"<CraftRecipeOutput {recipe.recipe_id}>"


class CraftRecipe:
    _recipes = None
    _instances = {}

    def __new__(cls, recipe_id: str):
        if cls._recipes is None:
            cls._load_recipes()

        if recipe_id in cls._instances:
            return cls._instances[recipe_id]

        instance = super().__new__(cls)
        cls._instances[recipe_id] = instance
        return instance

    def __init__(self, recipe_id: str):
        if hasattr(self, "recipe_id"):
            return

        self.recipe_id = recipe_id
        self.data = self._recipes.get(recipe_id, {})

        self._name = None
        self._name_en = None
        self._wiki_link = None

    @classmethod
    def _load_recipes(cls):
        """Load recipe data only once and store in class-level cache."""
        cls._recipes = script_parser.extract_script_data("craftRecipe")

    @classmethod
    def all(cls):
        if cls._recipes is None:
            cls._load_recipes()
        return {rid: cls(rid) for rid in cls._recipes}

    @classmethod
    def keys(cls):
        if cls._recipes is None:
            cls._load_recipes()
        return cls._recipes.keys()

    @classmethod
    def values(cls):
        if cls._recipes is None:
            cls._load_recipes()
        return (cls(rid) for rid in cls._recipes)

    @classmethod
    def count(cls):
        if cls._recipes is None:
            cls._load_recipes()
        return len(cls._recipes)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key):
        return key in self.data

    def __repr__(self):
        return f"<CraftRecipe {self.recipe_id}>"

    ## ---------------- Object Methods ---------------- ##

    def has_tag(self, tag: str) -> bool:
        """
        Check if the recipe has a specific tag.

        Args:
            tag (str): The tag name to check.

        Returns:
            bool: True if the tag is present, False otherwise.
        """
        return tag in self.tags

    @property
    def input_items(self) -> list[str]:
        """
        Return a list of item IDs used as inputs for this recipe.

        Includes normal inputs and items linked via tags.
        """
        from scripts.items.item_tags import get_tag_data

        if not hasattr(self, "_input_items"):
            items = set()

            for input in self.inputs:
                if input.items:
                    for item in input.items:
                        if isinstance(item, str):
                            items.update(input.items)
                        elif isinstance(item, dict):
                            it = item.get("raw_item")
                            if it:
                                items.add()
                        else:
                            raise f"Error getting input items for {self.recipe_id}: 'input.items' is not a string or dict"

                if input.tags:
                    all_tags = get_tag_data()
                    for tag in input.tags:
                        tagged_items = all_tags.get(tag, [])
                        for item in tagged_items:
                            item_id = item.get("item_id")
                            if item_id:
                                items.add(item_id)

            self._input_items = list(items)

        return self._input_items

    @property
    def output_items(self) -> list[str]:
        """
        Return a list of item IDs produced by this recipe.

        Includes normal outputs and mapped outputs.
        """
        if not hasattr(self, "_output_items"):
            items = set()

            for output in self.outputs:
                if output.items:
                    items.update(output.items)

            if self.item_mappers:
                for mapper in self.item_mappers.values():
                    for key, value in mapper.items():
                        if key == "default":
                            items.add(value)
                        else:
                            items.add(key)

            self._output_items = list(items)

        return self._output_items

    ## ---------------- Properties ---------------- ##

    @property
    def script_type(self):
        return self.data.get("ScriptType", "Unknown")

    @property
    def file(self):
        return self.data.get("SourceFile")

    @property
    def path(self):
        return get_script_path(self.file, prefer=self.script_type)

    @property
    def name(self):
        current_lang = Language.get()
        if (
            not hasattr(self, "_name_cache")
            or self._name_cache.get("lang") != current_lang
        ):
            self._name_cache = {
                "lang": current_lang,
                "value": Translate.get(self.recipe_id, property_key="TeachedRecipes"),
            }
        return self._name_cache["value"]

    @property
    def name_en(self):
        if (
            not hasattr(self, "_name_en_cache")
            or self._name_en_cache.get("lang") != "en"
        ):
            self._name_en_cache = {
                "lang": "en",
                "value": Translate.get(
                    self.recipe_id, property_key="TeachedRecipes", lang_code="en"
                ),
            }
        return self._name_en_cache["value"]

    @property
    def wiki_link(self):
        if self._wiki_link is not None:
            return self._wiki_link

        try:
            if self.outputs:
                output = self.outputs[0]

                product_id = None
                if output.items:
                    product_id = output.items[0]

                elif output.mapper:
                    mapper_data = self.item_mappers.get(output.mapper, {})
                    product_id = mapper_data.get("default")
                    if product_id is None and mapper_data:
                        product_id = next(iter(mapper_data.values()))

                if product_id:
                    item = Item(product_id)
                    self._wiki_link = link(item.page, self.name)
                    return self._wiki_link

        except Exception as e:
            echo.warning(f"Failed to resolve wiki_link for {self.recipe_id}: {e}")

        self._wiki_link = self.name
        return self._wiki_link

    @property
    def category(self):
        return self.data.get("category", "Miscellaneous")

    @property
    def category_link(self):
        if not hasattr(self, "_category_link"):
            if self.category:
                self._category_link = link(f"{self.category} (crafting)", self.category)
            else:
                self._category_link = ""

        return self._category_link

    @property
    def inputs(self) -> list[CraftRecipeInput]:
        raw_inputs = self.data.get("inputs", [])
        return [CraftRecipeInput(input_data, self) for input_data in raw_inputs]

    @property
    def outputs(self) -> list[CraftRecipeOutput]:
        raw_outputs = self.data.get("outputs", [])
        return [CraftRecipeOutput(output_data, self) for output_data in raw_outputs]

    @property
    def item_mappers(self):
        return self.data.get("itemMappers", {})

    @property
    def time(self):
        return int(self.data.get("time", 50))

    @property
    def timed_action(self):
        return self.data.get("timedAction", "")

    @property
    def tags(self):
        return self.data.get("tags", [])

    @property
    def need_to_be_learned(self) -> bool:
        return to_bool(self.data.get("needToBeLearn", False))

    @property
    def allow_batch_craft(self) -> bool:
        return to_bool(self.data.get("AllowBatchCraft", False))

    @property
    def on_create(self) -> str | None:
        return self.data.get("OnCreate")

    @property
    def on_test(self) -> str | None:
        return self.data.get("OnTest")

    @property
    def on_can_perform(self) -> str | None:
        return self.data.get("OnCanPerform")

    @property
    def tooltip(self):
        current_lang = Language.get()
        if (
            not hasattr(self, "_tooltip_cache")
            or self._tooltip_cache.get("lang") != current_lang
        ):
            tooltip = self.data.get("ToolTip")
            self._tooltip_cache = {
                "lang": current_lang,
                "value": Translate.get(tooltip) if tooltip else None,
            }
        return self._tooltip_cache["value"]

    @property
    def skill_required(self) -> list[dict]:
        return self.data.get("SkillRequired", [])

    @property
    def auto_learn_all(self) -> list[dict]:
        return self.data.get("AutoLearnAll", [])

    @property
    def auto_learn_any(self) -> list[str]:
        return self.data.get("AutoLearnAny", [])

    @property
    def xp_award(self) -> list[dict]:
        return self.data.get("xpAward", [])

    @property
    def meta_recipe(self) -> "CraftRecipe|None":
        if not hasattr(self, "_meta_recipe"):
            meta_recipe = self.data.get("MetaRecipe")
            self._meta_recipe = CraftRecipe(meta_recipe) if meta_recipe else None
        return self._meta_recipe

    ## ----------------- Entity Properties ----------------- ##

    @property
    def is_entity(self) -> bool:
        return self.script_type.lower() == "entity"

    @property
    def icon(self) -> str | None:
        if self.outputs:
            output = self.outputs[0]
            return output.get("icon")
        return None

    @property
    def on_add_to_menu(self):
        return self.data.get("OnAddToMenu")

    @property
    def sprite_outputs(self) -> dict:
        return self.data.get("spriteOutputs", {})

    @property
    def skill_base_health(self) -> float | None:
        return self.data.get("skillBaseHealth")


if __name__ == "__main__":
    recipe = CraftRecipe("MakeForearmBulletproofVestArmor")
    print(recipe.output_items)
    inputs = recipe.inputs
    # for input in inputs:
    #    print(input.items)
