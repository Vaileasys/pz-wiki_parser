[Previous Folder](../tools/update_icons.md) | [Next File](color.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

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

### [`is_ammo(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L16)

Return True if the item is considered ammunition.

### [`is_clothing(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L21)

Return True if the item is clothing.

### [`is_container(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L26)

Return True if the item is a container.

### [`is_fluid_container(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L30)
### [`is_food(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L33)

Return True if the item is food or marked as food.

### [`is_fuel(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L38)

Return True if the item can be used as burnable fuel.

### [`is_animal_part(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L42)

Return True if the item is an animal part.

### [`is_appearance(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L46)

Return True if the item is used to modify player appearance.

### [`is_camping(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L53)

Return True if the item is used for camping.

### [`is_communication(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L57)

Return True if the item is a communication appliance.

### [`is_cooking(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L61)

Return True if the item is a cooking utensil.

### [`is_corpse(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L65)

Return True if the item is a corpse.

### [`is_entertainment(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L69)

Return True if the item is an electronic.

### [`is_electronics(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L75)

Return True if the item is an electronic.

### [`is_fire_source(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L80)

Return True if the item can be used to start a fire.

### [`is_literature(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L86)

Return True if the item is a book, map, or other literature.

### [`is_fishing(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L91)

Return True if the item is used in fishing.

### [`is_gardening(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L97)

Return True if the item is used in gardening.

### [`is_household(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L103)

Return True if the item is categorised as a household item.

### [`is_instrument(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L108)

Return True if the item is an instrument.

### [`is_junk(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L113)

Return True if the item is classified as junk.

### [`is_light_source(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L118)

Return True if the item is classified as light source.

### [`is_material(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L124)

Return True if the item is classified as a material.

### [`is_medical(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L130)

Return True if the item is used in or related to first aid.

### [`is_memento(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L136)

Return True if the item is classified as a memento.

### [`is_security(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L142)

Return True if the item is classified as security.

### [`is_sport(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L146)

Return True if the item is classified as sport.

### [`is_tool(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L150)

Return True if the item is classified as a tool.

### [`is_trapping(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L168)

Return True if the item is classified as a trap.

### [`is_vehicle_maintenance(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L172)

Return True if the item is used for vehicle maintenance.

### [`is_weapon(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L176)

Return True if the item is a weapon.

### [`is_weapon_part(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L180)

Return True if the item is a weapon part.

### [`is_debug(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L184)

Return True if the item is a weapon.

### [`find_categories(obj: object)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L228)

Determine categories for an object using a list of check functions. Option to return only one (default) or all.


<ins>**Args:**</ins>
  - **obj (object)**:
      - _The object to evaluate (typically an Item)._
  - **do_all (bool, optional)**:
      - _If True, return all matching categories. If False (default), return only the first match._
  - **checks (list[tuple], optional)**:
      - _A list of (function, category_name) pairs to check against._
      - _Each function should return a bool when passed `obj`._

<ins>**Returns:**</ins>
  - **list[str]:**
      - A list of category names. Returns a single-element list if do_all is False,
      - or multiple category names if do_all is True. Returns an empty list if no match is found.

### [`find_all_categories(obj: object)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/categories.py#L250)

Return all category names that match the given object.

This is a shorthand for calling `find_categories` with `do_all=True`.

<ins>**Args:**</ins>
  - **obj (object)**:
      - _The object to evaluate (typically an Item)._
  - **checks (list[tuple], optional)**:
      - _A list of (function, category_name) pairs to check against._

<ins>**Returns:**</ins>
  - **list[str]:**
      - A list of all category names that match.



[Previous Folder](../tools/update_icons.md) | [Next File](color.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
