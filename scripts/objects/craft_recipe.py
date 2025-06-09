from scripts.utils import echo
from scripts.parser import script_parser
from scripts.core.file_loading import get_script_path
from scripts.core.language import Translate
from scripts.utils.util import link, to_bool


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
        if self._name is None:
            self._name = Translate.get(self.recipe_id, default=Translate.get("Recipe_" + self.recipe_id))
        return self._name

    @property
    def name_en(self):
        if self._name_en is None:
            self._name_en = Translate.get(self.recipe_id, lang_code="en")
        return self._name_en

    @property
    def wiki_link(self):
        from scripts.objects.item import Item
        if self._wiki_link is not None:
            return self._wiki_link

        # Try to resolve an item from outputs
        try:
            if self.outputs:
                output = self.outputs[0]

                if "items" in output:
                    product_id = output["items"][0]

                elif "mapper" in output:
                    mapper = output["mapper"]
                    mapper_data = self.item_mappers.get(mapper, {})

                    product_id = mapper_data.get("default")
                    if product_id is None and mapper_data:
                        product_id = next(iter(mapper_data.values()))

                else:
                    product_id = None

                if product_id:
                    item = Item(product_id)
                    self._wiki_link = link(item.page, self.name)
                    return self._wiki_link

        except Exception as e:
            echo.warning(f"Failed to resolve wiki_link for {self.recipe_id}: {e}")

        # Fallback to using the recipe name itself
        self._wiki_link = self.name
        return self._wiki_link

    @property
    def category(self):
        return self.data.get("category", "")

    @property
    def inputs(self):
        return self.data.get("inputs", {})

    @property
    def outputs(self):
        return self.data.get("outputs", {})

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
        if not hasattr(self, "_tooltip"):
            tooltip = self.data.get("ToolTip")
            self._tooltip = Translate.get(tooltip) if tooltip else None
        return self._tooltip

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
    recipe = CraftRecipe("MakeBoneForearmArmor")
    outputs = recipe.meta_recipe
    print(recipe.name)