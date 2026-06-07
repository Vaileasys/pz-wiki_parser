[Previous Folder](../navbox/navbox.md) | [Previous File](components.md) | [Next File](evolved_recipe.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# craft_recipe.py

## Classes

### `CraftRecipeInput`

#### Object Methods

##### [`__init__(data: dict, recipe: 'CraftRecipe')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L10)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L38)

#### Properties

##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L15)

##### [`count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L19)

Return formatted count: 'min-max' string for variable counts, int for fixed counts.

##### [`mode`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L27)

##### [`flags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L31)

##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L35)

### `CraftRecipeOutput`

#### Object Methods

##### [`__init__(data: dict, recipe: 'CraftRecipe')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L43)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L63)

#### Properties

##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L48)

##### [`mapper`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L52)

##### [`count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L56)

Return formatted count: 'min-max' string for variable counts, int for fixed counts.

### `CraftRecipe`

#### Class Methods

##### [`_load_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L94)

Load recipe data only once and store in class-level cache.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L99)

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L105)

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L111)

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L117)

#### Object Methods

##### [`__new__(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L71)

##### [`__init__(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L82)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L122)

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L125)

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L128)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L131)

##### [`has_tag(tag: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L136)

Check if the recipe has a specific tag.

<ins>**Args:**</ins>
  - **tag (str)**:
      - _The tag name to check._

<ins>**Returns:**</ins>
  - **bool**:
      - _True if the tag is present, False otherwise._

#### Properties

##### [`input_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L149)

Return a list of item IDs used as inputs for this recipe.

Includes normal inputs and items linked via tags.

##### [`output_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L186)

Return a list of item IDs produced by this recipe.

Includes normal outputs and mapped outputs.

##### [`script_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L214)

##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L218)

##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L222)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L226)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L239)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L253)

##### [`category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L283)

##### [`category_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L287)

##### [`inputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L297)

##### [`outputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L302)

##### [`item_mappers`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L307)

##### [`time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L311)

##### [`timed_action`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L315)

##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L319)

##### [`need_to_be_learned`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L323)

##### [`allow_batch_craft`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L327)

##### [`on_create`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L331)

##### [`on_test`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L335)

##### [`on_can_perform`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L339)

##### [`tooltip`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L343)

##### [`skill_required`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L357)

##### [`auto_learn_all`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L361)

##### [`auto_learn_any`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L365)

##### [`xp_award`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L369)

##### [`meta_recipe`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L373)

##### [`is_entity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L382)

##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L386)

##### [`on_add_to_menu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L393)

##### [`sprite_outputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L397)

##### [`skill_base_health`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L401)


[Previous Folder](../navbox/navbox.md) | [Previous File](components.md) | [Next File](evolved_recipe.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
