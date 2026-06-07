[Previous Folder](../navbox/navbox.md) | [Previous File](farming.md) | [Next File](fixing.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# fish.py

Parses and represents fish data from Project Zomboid's fishing system.

Extracts fish properties from the game's Lua files.
Fish instances can be created using item IDs and provide structured access to attributes.

Cached data is automatically stored and reused between sessions.

## Classes

### `Fish`

Represents a single fish type defined in the game’s fishing system.

#### Class Methods

##### [`_parse()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L79)

Parses fish data from the provided Lua file and caches it.

Extracts entries from the 'Fishing.fishes' table and indexes them by item type.

##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L99)

Loads fish data from the cache, re-parsing the Lua file if the data is outdated.

<ins>**Returns:**</ins>
  - **dict**:
      - _Mapping of item ID to fish data._

##### [`fix_item_id(item_id: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L122)

Attempts to fix a partial item_id by assuming the 'Base' module first,
then falling back to a full search through parsed fishes data.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _Either a full item_id ('Module.Item') or just an item name._

<ins>**Returns:**</ins>
  - **str**:
      - _The best-guess full item_id._

##### [`all() -> dict[str, 'Fish']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L153)

Returns all known fish instances.

<ins>**Returns:**</ins>
  - **dict[str, Fish]**:
      - _Mapping of item ID to Fish instance._

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L165)

Returns the total number of fish types parsed.

<ins>**Returns:**</ins>
  - **int**:
      - _Number of unique fish types._

##### [`exists(item_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L177)

Checks if a fish with the given item id exists in the parsed data.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if found, False otherwise._

#### Object Methods

##### [`__new__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L51)

Ensures only one Fish instance exists per item ID.

##### [`__init__(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L65)

Initialise the Fish instance with its data if not already initialised.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L188)

Returns a raw value from the fish data.

<ins>**Args:**</ins>
  - **key (str)**:
      - _Key to look up._
  - **default**:
      - _Value to return if key is missing._

<ins>**Returns:**</ins>
  - **Any**:
      - _Value from the raw data or default._

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L250)

#### Properties

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L202)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L206)

##### [`item_type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L210)

##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L214)

##### [`max_length`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L219)

##### [`trophy_length`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L223)

##### [`max_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L227)

##### [`trophy_weight`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L231)

##### [`is_predator`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L235)

##### [`lures`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L239)

##### [`size_data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L243)

##### [`has_sizes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/fish.py#L247)


[Previous Folder](../navbox/navbox.md) | [Previous File](farming.md) | [Next File](fixing.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
