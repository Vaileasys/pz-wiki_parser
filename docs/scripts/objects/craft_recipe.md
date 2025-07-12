[Previous Folder](../lists/attachment_list.md) | [Previous File](components.md) | [Next File](evolved_recipe.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# craft_recipe.py

## Classes

### `CraftRecipeInput`
#### Object Methods
##### [`__init__(data: dict, recipe: 'CraftRecipe')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L10)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L34)
#### Properties
##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L15)
##### [`count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L19)
##### [`mode`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L23)
##### [`flags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L27)
##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L31)

### `CraftRecipeOutput`
#### Object Methods
##### [`__init__(data: dict, recipe: 'CraftRecipe')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L39)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L55)
#### Properties
##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L44)
##### [`mapper`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L48)
##### [`count`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L52)

### `CraftRecipe`
#### Class Methods
##### [`_load_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L86)

Load recipe data only once and store in class-level cache.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L91)
##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L97)
##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L103)
##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L109)
#### Object Methods
##### [`__new__(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L63)
##### [`__init__(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L74)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L114)
##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L117)
##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L120)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L123)
##### [`has_tag(tag: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L128)

Check if the recipe has a specific tag.


<ins>**Args:**</ins>
  - **tag (str)**:
      - _The tag name to check._

<ins>**Returns:**</ins>
  - **bool:**
      - True if the tag is present, False otherwise.

#### Properties
##### [`input_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L141)

Return a list of item IDs used as inputs for this recipe.

Includes normal inputs and items linked via tags.

##### [`output_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L178)

Return a list of item IDs produced by this recipe.

Includes normal outputs and mapped outputs.

##### [`script_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L206)
##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L210)
##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L214)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L218)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L227)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L233)
##### [`category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L263)
##### [`category_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L267)
##### [`inputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L277)
##### [`outputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L282)
##### [`item_mappers`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L287)
##### [`time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L291)
##### [`timed_action`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L295)
##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L299)
##### [`need_to_be_learned`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L303)
##### [`allow_batch_craft`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L307)
##### [`on_create`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L311)
##### [`on_test`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L315)
##### [`on_can_perform`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L319)
##### [`tooltip`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L323)
##### [`skill_required`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L330)
##### [`auto_learn_all`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L334)
##### [`auto_learn_any`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L338)
##### [`xp_award`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L342)
##### [`meta_recipe`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L346)
##### [`is_entity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L355)
##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L359)
##### [`on_add_to_menu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L366)
##### [`sprite_outputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L370)
##### [`skill_base_health`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L374)


[Previous Folder](../lists/attachment_list.md) | [Previous File](components.md) | [Next File](evolved_recipe.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
