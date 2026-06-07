[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_fixing.md) | [Next File](item_infobox.md) | [Next Folder](groups/ammo_groups.md) | [Back to Index](../../index.md)

# item_groups.py

Shared item grouping framework.

Defines a small metadata model and base class for assigning items to named
groups, such as weapon types, ammo types, food categories, or clothing sections.
Group subclasses provide the actual classification logic while this module
handles display names, category lookups, ordering, and validation.

## Classes

### `GroupInfo`

Metadata for a single item group.

Attributes:
    type_id: Internal group identifier used for lookups.
    display_name: Display label used in generated output. Defaults to type_id.
    category: Optional parent category for grouping related types.
    display_order: Sort order used when generating ordered sections.
    metadata: Extra group-specific values for specialised use cases.

#### Object Methods

##### [`__post_init__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L32)

Fill missing display values after initialisation.

Sets display_name to type_id when no explicit display name was provided.

### `ItemGroups`

Base class for item grouping systems.

Subclasses define available groups with GROUPS and implement classify()
to assign items to one of those group IDs. Shared helper methods provide
consistent access to labels, categories, ordering, and validation.

#### Class Methods

##### [`classify(item, **kwargs) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L59)

Classify an item into a group type.

<ins>**Args:**</ins>
  - **item**:
      - _Item object to classify._
  - ****kwargs**:
      - _Optional context required by subclass logic._

<ins>**Returns:**</ins>
  - **The matching group type ID, or None if the item does not belong to any group.**:

##### [`find_type(item, **kwargs) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L73)

Classify an item using the subclass rules.

<ins>**Args:**</ins>
  - **item**:
      - _Item object to classify._
  - ****kwargs**:
      - _Optional context passed through to classify()._

<ins>**Returns:**</ins>
  - **The matching group type ID, or None if no group applies.**:

##### [`get_group_info(type_id: str) -> GroupInfo`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L87)

Get metadata for a group type.

<ins>**Args:**</ins>
  - **type_id**:
      - _Group type ID to look up._

<ins>**Returns:**</ins>
  - **The matching GroupInfo object, or None if the type ID is not defined.**:

##### [`get_display_name(type_id: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L100)

Get the display label for a group type.

<ins>**Args:**</ins>
  - **type_id**:
      - _Group type ID to look up._

<ins>**Returns:**</ins>
  - **The group's display name, or type_id if the group is not defined.**:

##### [`get_type_to_display_map() -> dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L114)

Get all group type IDs mapped to their display labels.

<ins>**Returns:**</ins>
  - **Dictionary mapping each type ID to its display name.**:

##### [`get_section_order(include_unordered: bool = False) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L124)

Get group display labels sorted by display order.

<ins>**Args:**</ins>
  - **include_unordered**:
      - _Whether to include groups using the default_
  - **unordered display value.**:

<ins>**Returns:**</ins>
  - **Ordered list of group display names.**:

##### [`get_types_by_category(category: str) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L146)

Get all group type IDs in a category.

<ins>**Args:**</ins>
  - **category**:
      - _Category name to look up._

<ins>**Returns:**</ins>
  - **List of type IDs in the category. Returns an empty list if the**:
  - **category is not found.**:

##### [`get_all_type_ids() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L168)

Get every group type ID defined by the class.

<ins>**Returns:**</ins>
  - **List of all type IDs in GROUPS.**:

##### [`get_all_categories() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L178)

Get every category used by the grouping class.

<ins>**Returns:**</ins>
  - **Sorted list of category names.**:

##### [`validate_type_id(type_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L193)

Check whether a group type ID is defined.

<ins>**Args:**</ins>
  - **type_id**:
      - _Group type ID to check._

<ins>**Returns:**</ins>
  - **True if the type ID exists in GROUPS, otherwise False.**:

##### [`get_groups_by_order() -> list[tuple[str, GroupInfo]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_groups.py#L206)

Get all groups sorted by display order.

<ins>**Returns:**</ins>
  - **List of (type_id, GroupInfo) tuples sorted by display_order.**:


[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_fixing.md) | [Next File](item_infobox.md) | [Next Folder](groups/ammo_groups.md) | [Back to Index](../../index.md)
