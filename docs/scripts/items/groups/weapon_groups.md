[Previous Folder](../item_article.md) | [Previous File](ammo_groups.md) | [Next Folder](../lists/item_list_animal_part.md) | [Back to Index](../../../index.md)

# weapon_groups.py

Weapon item grouping and classification.

Classifies weapons by melee skill, firearm type, explosives, and weapon parts,
then exposes their display names, categories, and ordering for generated
navboxes, lists, and item data.

## Classes

### `WeaponGroups`

Item grouping rules for weapons and weapon-related items.

Defines the recognised weapon groups, their display labels, parent
categories, and display order. Classification is based on weapon skill
categories, firearm properties, display category, or item type.

#### Class Methods

##### [`classify(item: Item, **kwargs) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/groups/weapon_groups.py#L58)

Classify an item as a weapon group type.

Weapons with skill categories are grouped by their primary skill, with
"Improvised" ignored when another skill is present. Firearms are grouped
as handguns, rifles, or shotguns based on equipment and projectile data.
Explosives and weapon parts are handled by display category or item type.

<ins>**Args:**</ins>
  - **item**:
      - _Item object to classify._
  - ****kwargs**:
      - _Additional context accepted for API compatibility._

<ins>**Returns:**</ins>
  - **Weapon group type ID, or None if the item is not weapon-related.**:


[Previous Folder](../item_article.md) | [Previous File](ammo_groups.md) | [Next Folder](../lists/item_list_animal_part.md) | [Back to Index](../../../index.md)
