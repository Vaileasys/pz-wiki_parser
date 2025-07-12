[Previous Folder](../lists/attachment_list.md) | [Previous File](farming.md) | [Next File](fluid.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# fixing.py

Provides access to parsed "fixing" data from Project Zomboid scripts.

This module defines the `Fixing` class, which represents a repair recipe.
It includes logic for resolving fixing entries based on item IDs, loading fixer data, and exposing relevant
attributes like required items, condition modifiers, and skill requirements.

Classes:
    - Fixing: Represents a fixing definition, including required items and fixers.
    - GlobalItem: Represents a global item required across all fixer attempts.
    - Fixer: Represents a fixer item and its associated skill requirements.

## Classes

### `Fixing`

Represents a fixing entry for an item, containing data about how it can be repaired.

This class lazily loads all fixing definitions from parsed script data and provides
a caching mechanism to avoid duplicate instances. A Fixing object can be accessed using
either a fixing ID, item ID or Item object.
Properties:
- fixing_id (str): The internal ID of the fixing.
- valid (bool): Whether the fixing entry contains valid data.
- script_type (str): Optional script type associated with the fixing.
- file (str): The script file name where the fixing is defined.
- path (str): The resolved file path for the fixing source.
- module (str): The module prefix of the fixing ID.
- id_type (str): The item identifier portion of the fixing ID.
- requires (list[Item]): List of required items for the fix.
- condition_modifier (float): Modifier applied to the item’s condition after repair.
- global_items (list[GlobalItem]): Shared global items required by the fixing.
- fixers (list[Fixer]): Fixer items, with optional skill requirements.

#### Class Methods
##### [`_load_fixings()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L45)

Load and cache all fixing data from script files if not already loaded.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L50)

Return a dictionary of all fixings, mapped by their fixing ID.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L57)

Return an iterable of all available fixing IDs.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L64)

Return a generator of all Fixing instances.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L71)

Return the number of available fixing definitions.

##### [`exists(fixing_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L78)

Check if a fixing with the given ID exists.

#### Object Methods
##### [`__new__(key: str | Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L84)

Create or return a cached Fixing instance based on a string ID or Item object.

Supports matching by fixing ID, item ID, or an Item object.

##### [`__init__(_: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L136)

Initialise the Fixing instance with resolved fixing ID.


<ins>**Raises:**</ins>
  - **RuntimeError:**
      - If resolving the fixing ID fails.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L157)

Allow dictionary-style access to internal data.

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L161)

Check if a key exists in the fixing data.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L165)

Return a readable string representation of the Fixing instance.

##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L169)

Get a value from the fixing data with an optional default.

#### Properties
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L174)

Return True if the fixing entry contains valid data.

##### [`script_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L179)

Return the script type defined for the fixing, if any.

##### [`file`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L184)

Return the source script file name for the fixing.

##### [`path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L189)

Return the resolved file path of the fixing script.

##### [`module`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L194)

Return the module name (prefix) of the fixing ID.

##### [`id_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L199)

Return the item identifier part of the fixing ID.

##### [`requires`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L204)

Return a list of required Item objects for this fixing.

##### [`condition_modifier`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L209)

Return the condition modifier value for the fixing.

##### [`global_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L214)

Return a list of GlobalItem objects required by the fixing.

##### [`fixers`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L222)

Return a list of Fixer objects that can be used for repair.


### `GlobalItem`

Represents a global item required across all fixing attempts.

Properties:
- item_id (str): The item ID of the required global item.
- amount (int): Quantity required for the fixing.
- item (Item): The wrapped `Item` object.

#### Object Methods
##### [`__init__(item_id: str, amount: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L236)

Initialise a GlobalItem with its ID and required amount.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L241)

Return a string representation of the GlobalItem instance.

#### Properties
##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L246)

Return the Item object associated with this global item ID.


### `Fixer`

Represents a fixer item used to repair something, with optional skill requirements.

Properties:
- item_id (str): The fixer item’s ID.
- amount (int): Quantity of the fixer required.
- skill_requirements (dict[str, int]): Required skills and their levels.
- item (Item): The wrapped `Item` object.
- skills (list[Skill]): Skill objects required for the fixer.

#### Object Methods
##### [`__init__(item_id: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L262)

Initialise a Fixer with its ID, amount, and skill requirements.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L268)

Return a string representation of the Fixer instance.

##### [`get_skill_level(skill: Skill | str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L272)

Return the required level for the given skill.


<ins>**Args:**</ins>
  - **skill (Skill | str)**:
      - _The skill object or perk ID to check._

<ins>**Returns:**</ins>
  - **int:**
      - The level required for the given skill, or 0 if not required.

#### Properties
##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L286)

Return the Item object associated with this fixer.

##### [`skills`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fixing.py#L291)

Return a list of Skill objects required by this fixer.



[Previous Folder](../lists/attachment_list.md) | [Previous File](farming.md) | [Next File](fluid.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
