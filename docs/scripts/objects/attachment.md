[Previous Folder](../lists/attachment_list.md) | [Next File](body_location.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# attachment.py

Hotbar slot and attachment parsing from ISHotbarAttachDefinition.lua.

This module parses and structures hotbar attachment slot data,
providing access to slot definitions, associated item mappings,
and attachment point metadata. It includes:

- `HotbarSlot`: Represents each hotbar slot with access to animation sets,
  attachments, item compatibility, and wiki utilities.
- `HotbarSlotItems`: A wrapper for item compatibility within a slot, exposing
  items grouped by AttachmentType, AttachmentsProvided, and AttachmentReplacement.
- `AttachmentType`: Represents global attachment points used across slots,
  mapping back to slot usage and associated items.

Parsed data is cached for performance and reused across components.

## Classes

### `HotbarSlot`

Represents a hotbar slot definition parsed from the game files.

Provides access to slot metadata and items.

#### Class Methods
##### [`_load_slots()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L33)

Load and process all hotbar slot data from ISHotbarAttachDefinition.lua.

This includes identifying relevant item associations.

##### [`_parse_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L71)

Parse raw Lua data into a cleaned hotbar slot dictionary.


<ins>**Returns:**</ins>
  - **dict:**
      - A mapping of slot_id to slot metadata.

##### [`_find_all_items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L94)

Populate internal item lists for type, provided, and replacement keys.

##### [`_find_slot_items(slot: str, slot_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L109)

Find all items that match a slot's attachment rules.


<ins>**Args:**</ins>
  - **slot (str)**:
      - _The slot ID._
  - **slot_data (dict)**:
      - _The raw slot data._

<ins>**Returns:**</ins>
  - **dict:**
      - The updated slot data with item associations.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L145)

Return all hotbar slots.


<ins>**Returns:**</ins>
  - **dict[str, HotbarSlot]:**
      - A dictionary of slot_id to HotbarSlot instances.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L156)

Return all available slot IDs.


<ins>**Returns:**</ins>
  - **KeysView:**
      - The slot ID keys.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L167)

Return all HotbarSlot instances.


<ins>**Returns:**</ins>
  - **Generator[HotbarSlot]:**
      - A generator of HotbarSlot instances.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L178)

Return the total number of hotbar slots.


<ins>**Returns:**</ins>
  - **int:**
      - The number of slots.

##### [`exists(slot_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L189)

Check if a slot exists.


<ins>**Args:**</ins>
  - **slot_id (str)**:
      - _The slot ID to check._

<ins>**Returns:**</ins>
  - **bool:**
      - True if the slot exists, otherwise False.

##### [`get_attachment_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L203)

Return the full attachment type structure generated during slot parsing.


<ins>**Returns:**</ins>
  - **dict:**
      - Mapping of attachment_id to metadata, slots, and item IDs.

#### Object Methods
##### [`__new__(slot_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L213)
##### [`__init__(slot_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L219)

Initialise a HotbarSlot instance.


<ins>**Args:**</ins>
  - **slot_id (str)**:
      - _The ID of the slot to load._

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L235)
##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L238)

Return a value from the raw slot data.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The key to look up._
      - _default: A fallback value._

<ins>**Returns:**</ins>
  - **Any:**
      - The corresponding value or default.

#### Properties
##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L252)

Access the items associated with this hotbar slot.


<ins>**Returns:**</ins>
  - **HotbarSlotItems:**
      - A dict-like wrapper for item compatibility.

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L262)

Return a wiki-formatted link to this slot's display name.

##### [`wiki_link_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L267)

Return a wiki-formatted link using the slot ID as both label and anchor.


### `HotbarSlotItems`

Wrapper around hotbar slot item data, providing both property access

and dict-like behaviour.

#### Object Methods
##### [`__init__(data: dict[str, list[str]])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L276)

Initialise the item wrapper.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _A dictionary of attachment type lists._

##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L300)

Get a list of items by raw key.


<ins>**Args:**</ins>
  - **key (str)**:
      - _The internal item key._
      - _default: A fallback if the key is missing._

<ins>**Returns:**</ins>
  - **list[str]:**
      - A list of item IDs.

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L313)
##### [`__iter__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L316)
##### [`__len__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L319)
##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L322)
##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L325)
#### Properties
##### [`attachments`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L286)

Items with a matching AttachmentType.

##### [`provided`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L291)

Items that provide this slot via AttachmentsProvided.

##### [`replaced`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L296)

Items that replace this slot via AttachmentReplacement.


### `AttachmentType`

Represents an attachment point across all hotbar slots.

Groups metadata and related items under a specific attachment ID.

#### Class Methods
##### [`_load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L364)

Load parsed attachment data from HotbarSlot.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L374)

Return all attachment types as a dictionary.


<ins>**Returns:**</ins>
  - **dict[str, AttachmentType]:**
      - Mapping of attachment_id to instance.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L385)

Return all attachment type IDs.


<ins>**Returns:**</ins>
  - **KeysView[str]:**
      - The attachment IDs.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L396)

Return all AttachmentType instances.


<ins>**Returns:**</ins>
  - **Generator[AttachmentType]:**
      - Generator of all instances.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L407)

Return the total number of attachment types.


<ins>**Returns:**</ins>
  - **int:**
      - Count of known attachment types.

##### [`exists(attachment_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L418)

Check if an attachment ID exists in the parsed data.


<ins>**Args:**</ins>
  - **attachment_id (str)**:
      - _The attachment ID to check._

<ins>**Returns:**</ins>
  - **bool:**
      - True if the attachment exists, False otherwise.

#### Object Methods
##### [`__new__(attachment_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L336)

Ensure a shared instance per attachment_id.


<ins>**Args:**</ins>
  - **attachment_id (str)**:
      - _The ID of the attachment point._

<ins>**Returns:**</ins>
  - **AttachmentType:**
      - A shared instance of the attachment type.

##### [`__init__(attachment_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L351)

Initialise the AttachmentType instance with parsed data.


<ins>**Args:**</ins>
  - **attachment_id (str)**:
      - _The ID of the attachment point._

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L431)

Return a debug representation of the attachment.


<ins>**Returns:**</ins>
  - **str:**
      - A string in the format <AttachmentType attachment_id>.

#### Properties
##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L441)

Whether this AttachmentType instance corresponds to known data.

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L446)

The display name of this attachment (from HotbarSlot).

##### [`slots`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L451)

List of hotbar slot IDs that use this attachment type.

##### [`items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L456)

List of item IDs that use this attachment via AttachmentType.

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L461)

Return a wiki-formatted link to this attachment type's display name.

##### [`wiki_link_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/attachment.py#L466)

Return a wiki-formatted link using the attachment ID as both label and anchor.



[Previous Folder](../lists/attachment_list.md) | [Next File](body_location.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
