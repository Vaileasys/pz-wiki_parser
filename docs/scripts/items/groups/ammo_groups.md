[Previous Folder](../item_article.md) | [Next File](weapon_groups.md) | [Next Folder](../lists/item_list_animal_part.md) | [Back to Index](../../../index.md)

# ammo_groups.py

Ammunition item grouping and relationship discovery.

Classifies ammo-related items into rounds, boxes, cartons, and magazines,
then derives their containment hierarchy from crafting recipes. Also links
ammo types to compatible weapons and magazines for generated item data.

## Classes

### `AmmoGroups`

Item grouping rules for ammunition and magazines.

Defines recognised ammo groups, their display labels, parent categories,
and display order. Classification uses recipe-derived containment data
for boxes and cartons, and item tags for loose rounds and magazines.

#### Class Methods

##### [`get_box_types() -> dict[str, dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/groups/ammo_groups.py#L100)

Get cached ammo container relationship data.

Builds the mapping on first use, then reuses it for later classification
and relationship lookups.

<ins>**Returns:**</ins>
  - **Dictionary mapping ammo container item IDs to containment data.**:

##### [`classify(item: Item, **kwargs) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/groups/ammo_groups.py#L118)

Classify an item as an ammunition group type.

Boxes and cartons are identified from recipe-derived container data.
Loose rounds are identified by the Ammo tag, while magazines are identified
by pistol or rifle magazine tags.

<ins>**Args:**</ins>
  - **item**:
      - _Item object to classify._
  - ****kwargs**:
      - _Additional context accepted for API compatibility._

<ins>**Returns:**</ins>
  - **Ammo group type ID, or None if the item is not ammo-related.**:

#### Static Methods

##### [`build_box_types() -> dict[str, dict]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/groups/ammo_groups.py#L39)

Build ammo container relationships from crafting recipes.

Reads known unpacking recipes to map boxes and cartons to the item they
contain, along with the produced quantity. Supports direct recipe outputs
and item mapper based recipes.

<ins>**Returns:**</ins>
  - **Dictionary mapping ammo container item IDs to containment data.**:

##### [`build_ammo_data(item_id: str, ammo_type: str, all_item_data: dict[str, dict]) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/groups/ammo_groups.py#L161)

Build relationship data for an ammunition item.

Traces the ammo hierarchy between rounds, boxes, and cartons, then finds
compatible firearms and magazines by matching each item's ammo type.

<ins>**Args:**</ins>
  - **item_id**:
      - _Full item ID to analyse._
  - **ammo_type**:
      - _Ammo group type returned by classify()._
  - **all_item_data**:
      - _Item data dictionary to read from and update._

<ins>**Returns:**</ins>
  - **The item's data dictionary with related ammo, weapon, and magazine**:
  - **fields added where available.**:


[Previous Folder](../item_article.md) | [Next File](weapon_groups.md) | [Next Folder](../lists/item_list_animal_part.md) | [Back to Index](../../../index.md)
