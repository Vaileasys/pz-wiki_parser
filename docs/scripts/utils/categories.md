[Previous Folder](../tools/batch_processor.md) | [Next File](color.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# categories.py

Category checks.

This module defines a series of category check functions used to classify an object based on their type,
tags, or other properties. The `find_categories` and `find_all_categories` functions evaluate an item against
a predefined list of checks and return matching category names.

Typical usage:
    categories = find_categories(item)              # First matching category
    all_categories = find_all_categories(item)      # All matching categories

Used by the wiki parser to automatically organise and filter item data.

## Functions

### [`get_cat_link(display_category: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L99)

Returns a formatted link string for a given display category.

Translates the raw DisplayCategory value, splits it by "/", and converts each
part into a wiki link using `display_category_map`. Falls back to plain text
if a link can't be found.

<ins>**Args:**</ins>
  - **display_category (str)**:
      - _The raw DisplayCategory value from item data._

<ins>**Returns:**</ins>
  - **str**:
      - _A slash-separated string of wiki links or plain text._

### [`is_ammo(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L141)

Return True if the item is considered ammunition.

### [`is_clothing(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L148)

Return True if the item is clothing.

### [`is_container(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L153)

Return True if the item is a container.

### [`is_fluid_container(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L162)

### [`is_food(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L166)

Return True if the item is food or marked as food.

### [`is_fuel(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L171)

Return True if the item can be used as burnable fuel.

### [`is_animal_part(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L176)

Return True if the item is an animal part.

### [`is_appearance(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L181)

Return True if the item is used to modify player appearance.

### [`is_camping(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L194)

Return True if the item is used for camping.

### [`is_communication(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L199)

Return True if the item is a communication appliance.

### [`is_cooking(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L204)

Return True if the item is a cooking utensil.

### [`is_corpse(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L209)

Return True if the item is a corpse.

### [`is_entertainment(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L214)

Return True if the item is an electronic.

### [`is_electronics(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L222)

Return True if the item is an electronic.

### [`is_fire_source(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L229)

Return True if the item can be used to start a fire.

### [`is_literature(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L238)

Return True if the item is a book, map, or other literature.

### [`is_fishing(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L245)

Return True if the item is used in fishing.

### [`is_gardening(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L257)

Return True if the item is used in gardening.

### [`is_household(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L267)

Return True if the item is categorised as a household item.

### [`is_instrument(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L275)

Return True if the item is an instrument.

### [`is_junk(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L283)

Return True if the item is classified as junk.

### [`is_light_source(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L288)

Return True if the item is classified as light source.

### [`is_material(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L297)

Return True if the item is classified as a material.

### [`is_medical(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L313)

Return True if the item is used in or related to first aid.

### [`is_memento(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L322)

Return True if the item is classified as a memento.

### [`is_security(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L345)

Return True if the item is classified as security.

### [`is_sport(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L350)

Return True if the item is classified as sport.

### [`is_tool(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L355)

Return True if the item is classified as a tool.

### [`is_trapping(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L428)

Return True if the item is classified as a trap.

### [`is_vehicle_maintenance(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L433)

Return True if the item is used for vehicle maintenance.

### [`is_weapon(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L441)

Return True if the item is a weapon.

### [`is_weapon_part(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L446)

Return True if the item is a weapon part.

### [`is_debug(item: Item) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L451)

Return True if the item is a weapon.

### [`find_categories(obj: object, *, do_all: bool = False, checks: list[tuple] = ITEM_CHECKS) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L500)

Determine categories for an object using a list of check functions. Option to return only one (default) or all.

<ins>**Args:**</ins>
  - **obj (object)**:
      - _The object to evaluate (typically an Item)._
  - **do_all (bool, optional)**:
      - _If True, return all matching categories. If False (default), return only the first match._
  - **checks (list[tuple], optional)**:
      - _A list of (function, category_name) pairs to check against._
  - **Each function should return a bool when passed `obj`.**:

<ins>**Returns:**</ins>
  - **list[str]**:
      - _A list of category names. Returns a single-element list if do_all is False,_
  - **or multiple category names if do_all is True. Returns an empty list if no match is found.**:

### [`find_all_categories(obj: object, *, checks: list[tuple] = ITEM_CHECKS) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L525)

Return all category names that match the given object.
This is a shorthand for calling `find_categories` with `do_all=True`.

<ins>**Args:**</ins>
  - **obj (object)**:
      - _The object to evaluate (typically an Item)._
  - **checks (list[tuple], optional)**:
      - _A list of (function, category_name) pairs to check against._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _A list of all category names that match._


[Previous Folder](../tools/batch_processor.md) | [Next File](color.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
