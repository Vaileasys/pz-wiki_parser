[Previous Folder](../lists/body_locations_list.md) | [Previous File](components.md) | [Next File](fluid.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# craft_recipe.py

## Classes

### `CraftRecipe`
#### Class Methods
##### [`_load_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L35)

Load recipe data only once and store in class-level cache.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L40)
##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L46)
##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L52)
##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L58)
#### Object Methods
##### [`__new__(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L12)
##### [`__init__(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L23)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L63)
##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L66)
##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L69)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L72)
##### [`has_tag(tag: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L77)

Check if the recipe has a specific tag.


<ins>**Args:**</ins>
  - **tag (str)**:
      - _The tag name to check._

<ins>**Returns:**</ins>
  - **bool:**
      - True if the tag is present, False otherwise.

#### Properties
##### [`script_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L92)
##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L96)
##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L100)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L104)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L110)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L116)
##### [`category`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L153)
##### [`inputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L157)
##### [`outputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L161)
##### [`item_mappers`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L165)
##### [`time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L169)
##### [`timed_action`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L173)
##### [`tags`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L177)
##### [`need_to_be_learned`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L181)
##### [`allow_batch_craft`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L185)
##### [`on_create`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L189)
##### [`on_test`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L193)
##### [`on_can_perform`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L197)
##### [`tooltip`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L201)
##### [`skill_required`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L208)
##### [`auto_learn_all`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L212)
##### [`auto_learn_any`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L216)
##### [`xp_award`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L220)
##### [`meta_recipe`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L224)
##### [`is_entity`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L233)
##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L237)
##### [`on_add_to_menu`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L244)
##### [`sprite_outputs`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L248)
##### [`skill_base_health`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/craft_recipe.py#L252)


[Previous Folder](../lists/body_locations_list.md) | [Previous File](components.md) | [Next File](fluid.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
