[Previous Folder](../lists/attachment_list.md) | [Previous File](craft_recipe.md) | [Next File](farming.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# evolved_recipe.py

Evolved Recipe module.

This module defines the `EvolvedRecipe` class, which parses and represents customisable cooking recipes
from the game’s script files. It supports loading all evolved recipes, accessing recipe properties,
and linking them to compatible items and their effects.

## Classes

### `EvolvedRecipe`

Represents an evolved recipe parsed from Project Zomboid script files.

Each recipe is uniquely identified by its ID and provides access to associated script
data, result items, ingredients, and localisation metadata. Recipes are loaded once and
cached for re-use.

<ins>**Args:**</ins>
  - **recipe_id (str)**:
      - _The recipe identifier. This may be either a full ID (e.g., "Base.Soup")_
      - _or a short ID (e.g., "Soup"). The module prefix is stripped automatically._
      - _Example:_
      - _soup = EvolvedRecipe("Soup")_
      - _soup.name -> 'Soup'_
      - _soup.result_item.name -> 'Pot of Soup'_
      - _Class Methods:_
        - EvolvedRecipe.all() → dict of all recipes
        - EvolvedRecipe.exists("Soup") → check if a recipe exists
        - EvolvedRecipe.keys() / values() / count() → like dict access
      - _Notes:_
      - _The underlying script data is parsed from `evolvedrecipe` script blocks,_
      - _and item links are created based on references from the `Item` class._

#### Class Methods
##### [`_load_evolved_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L83)

Internal method to load all evolved recipes from script data and map associated items.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L106)

Return all evolved recipes as a dictionary of `{recipe_id: EvolvedRecipe}`. Similar to `dict.items()` in behaviour.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L113)

Return all evolved recipe IDs. Mirrors `dict.keys()` for available recipe entries.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L120)

Yield all `EvolvedRecipe` instances. Mirrors `dict.values()` for available recipe entries.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L127)

Return the number of loaded evolved recipes. Equivalent to `len(dict)` on the full recipe mapping.

##### [`exists(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L134)

Check if a given recipe ID exists in the loaded data. Similar to checking `recipe_id in dict`.

#### Object Methods
##### [`__new__(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L45)

Create or return a cached instance of an EvolvedRecipe by ID.

##### [`__init__(recipe_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L57)

Initialise an EvolvedRecipe instance using the provided recipe ID.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L71)

Allow dict-style access to the internal data. Equivalent to `self.data[key]` or `self.data.get(key)`.

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L75)

Check if a key exists in the internal data. Equivalent to `key in self.data`.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L79)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L142)

Return a value from the internal data dictionary. Equivalent to `self.data.get(key, default)`.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to retrieve from the internal recipe data._
  - **default (Any, optional)**:
      - _The value to return if the key is not found. Defaults to None._

<ins>**Returns:**</ins>
  - **Any:**
      - The value associated with the key, or the default if not present.

#### Properties
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L158)
##### [`script_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L162)
##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L166)
##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L170)
##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L174)
##### [`original_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L184)
##### [`display_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L188)
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L192)
##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L198)
##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L204)
##### [`max_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L210)
##### [`result_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L214)
##### [`base_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L219)
##### [`cookable`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L224)
##### [`add_ingredient_if_cooked`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L228)
##### [`can_add_spices_empty`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L232)
##### [`add_sound`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L236)
##### [`hidden`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L240)
##### [`allow_frozen`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L244)
##### [`template`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L248)
##### [`minimum_water`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L252)
##### [`items_list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/evolved_recipe.py#L256)

Return a dictionary of items that can be used in this evolved recipe.

Each key is an item ID (str), and each value is a dictionary containing:
- "item" (Item): The `Item` object reference.
- "hunger" (float | int): The hunger value contributed when added.
- "cooked" (bool): Whether the item is only valid when cooked.
- "spice" (bool): Whether the item is a spice.

<ins>**Returns:**</ins>
  - dict[str, dict[str, Item | float | bool]]: Items compatible with this recipe.



[Previous Folder](../lists/attachment_list.md) | [Previous File](craft_recipe.md) | [Next File](farming.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
