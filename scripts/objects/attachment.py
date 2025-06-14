"""
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
"""
from scripts.utils import lua_helper, util
from scripts.core.cache import save_cache

class HotbarSlot:
    """
    Represents a hotbar slot definition parsed from the game files.
    Provides access to slot metadata and items.
    """
    _slots = None
    _attachments = {}

    _attachment_type_items: list[str] = []
    _attachments_provided_items: list[str] = []
    _attachment_replacement_items: list[str] = []

    @classmethod
    def _load_slots(cls):
        """
        Load and process all hotbar slot data from ISHotbarAttachDefinition.lua.
        This includes identifying relevant item associations.
        """
        if cls._slots is not None:
            return

        hotbar_data = cls._parse_data()
        cls._find_all_items()

        cls._slots = {}
        cls._attachments = {}

        for slot_id, slot_data in hotbar_data.items():
            cls._slots[slot_id] = cls._find_slot_items(slot_id, slot_data)

            for attachment_id, attachment_name in slot_data.get("attachments", {}).items():
                if attachment_id not in cls._attachments:
                    cls._attachments[attachment_id] = {
                        "AttachedLocation": attachment_name,
                        "AttachmentsProvided": [],
                        "Items": [],
                    }
                cls._attachments[attachment_id]["AttachmentsProvided"].append(slot_id)

        from scripts.objects.item import Item
        for item_id in cls._attachment_type_items:
            item = Item(item_id)
            attachment_id = item.get("AttachmentType")
            if attachment_id in cls._attachments:
                cls._attachments[attachment_id]["Items"].append(item_id)

        # Save both data sets
        save_cache(cls._slots, "hotbar_data.json")
        save_cache(cls._attachments, "attachment_data.json")

    @classmethod
    def _parse_data(cls) -> dict:
        """
        Parse raw Lua data into a cleaned hotbar slot dictionary.

        Returns:
            dict: A mapping of slot_id to slot metadata.
        """
        lua_runtime = lua_helper.load_lua_file("ISHotbarAttachDefinition.lua")
        raw = lua_helper.parse_lua_tables(lua_runtime)
        data = raw.get("ISHotbarAttachDefinition", {})

        if isinstance(data.get("replacements"), list):
            for item in data.pop("replacements"):
                if isinstance(item, dict) and "type" in item:
                    data[item.pop("type")] = item

        cleaned = {}
        for key, value in data.items():
            value = dict(value)
            cleaned[value.pop("type", key)] = value
        return cleaned

    @classmethod
    def _find_all_items(cls):
        """
        Populate internal item lists for type, provided, and replacement keys.
        """
        from scripts.objects.item import Item
        for item_id in Item.all():
            item = Item(item_id)
            if item.attachment_type:
                cls._attachment_type_items.append(item_id)
            if item.attachments_provided:
                cls._attachments_provided_items.append(item_id)
            if item.attachment_replacement:
                cls._attachment_replacement_items.append(item_id)

    @classmethod
    def _find_slot_items(cls, slot: str, slot_data: dict) -> dict:
        """
        Find all items that match a slot's attachment rules.

        Args:
            slot (str): The slot ID.
            slot_data (dict): The raw slot data.

        Returns:
            dict: The updated slot data with item associations.
        """
        from scripts.objects.item import Item
        slot_data["items"] = {
            "AttachmentType": [],
            "AttachmentsProvided": [],
            "AttachmentReplacement": []
        }

        for item_id in cls._attachment_type_items:
            item = Item(item_id)
            if item.get("AttachmentType") in slot_data.get("attachments", {}):
                slot_data["items"]["AttachmentType"].append(item_id)

        for item_id in cls._attachments_provided_items:
            item = Item(item_id)
            if slot in item.get("AttachmentsProvided", []):
                slot_data["items"]["AttachmentsProvided"].append(item_id)

        for item_id in cls._attachment_replacement_items:
            item = Item(item_id)
            if item.get("AttachmentReplacement") == slot:
                slot_data["items"]["AttachmentReplacement"].append(item_id)

        return slot_data

    @classmethod
    def all(cls) -> dict[str, "HotbarSlot"]:
        """
        Return all hotbar slots.

        Returns:
            dict[str, HotbarSlot]: A dictionary of slot_id to HotbarSlot instances.
        """
        cls._load_slots()
        return {slot_id: cls(slot_id) for slot_id in cls._slots}

    @classmethod
    def keys(cls):
        """
        Return all available slot IDs.

        Returns:
            KeysView: The slot ID keys.
        """
        cls._load_slots()
        return cls._slots.keys()

    @classmethod
    def values(cls):
        """
        Return all HotbarSlot instances.

        Returns:
            Generator[HotbarSlot]: A generator of HotbarSlot instances.
        """
        cls._load_slots()
        return (cls(slot_id) for slot_id in cls._slots)

    @classmethod
    def count(cls):
        """
        Return the total number of hotbar slots.

        Returns:
            int: The number of slots.
        """
        cls._load_slots()
        return len(cls._slots)

    @classmethod
    def exists(cls, slot_id: str) -> bool:
        """
        Check if a slot exists.

        Args:
            slot_id (str): The slot ID to check.

        Returns:
            bool: True if the slot exists, otherwise False.
        """
        cls._load_slots()
        return slot_id in cls._slots
    
    @classmethod
    def get_attachment_data(cls) -> dict[str, dict]:
        """
        Return the full attachment type structure generated during slot parsing.

        Returns:
            dict: Mapping of attachment_id to metadata, slots, and item IDs.
        """
        cls._load_slots()
        return cls._attachments

    def __new__(cls, slot_id: str):
        cls._load_slots()
        if slot_id not in cls._slots:
            raise KeyError(f"HotbarSlot '{slot_id}' not found.")
        return super().__new__(cls)

    def __init__(self, slot_id: str):
        """
        Initialise a HotbarSlot instance.

        Args:
            slot_id (str): The ID of the slot to load.
        """
        if hasattr(self, 'slot_id'):
            return
        self.slot_id = slot_id
        self._data = self._slots[slot_id]
        self.animset = self._data.get("animset")
        self.name = self._data.get("name")
        self.attachments = self._data.get("attachments", {})
        self.replacement = self._data.get("replacement", {})

    def __repr__(self):
        return f"<HotbarSlot {self.slot_id}>"

    def get(self, key: str, default=None):
        """
        Return a value from the raw slot data.

        Args:
            key (str): The key to look up.
            default: A fallback value.

        Returns:
            Any: The corresponding value or default.
        """
        return self._data.get(key, default)

    @property
    def items(self) -> "HotbarSlotItems":
        """
        Access the items associated with this hotbar slot.

        Returns:
            HotbarSlotItems: A dict-like wrapper for item compatibility.
        """
        return HotbarSlotItems(self.get("items", {}))
    
    @property
    def wiki_link(self) -> str:
        """Return a wiki-formatted link to this slot's display name."""
        return util.link("AttachmentsProvided", self.name, anchor=self.slot_id)
    
    @property
    def wiki_link_id(self) -> str:
        """Return a wiki-formatted link using the slot ID as both label and anchor."""
        return util.link("AttachmentsProvided", self.slot_id, anchor=self.slot_id)

class HotbarSlotItems:
    """
    Wrapper around hotbar slot item data, providing both property access
    and dict-like behaviour.
    """
    def __init__(self, data: dict[str, list[str]]):
        """
        Initialise the item wrapper.

        Args:
            data (dict): A dictionary of attachment type lists.
        """
        self._data = data

    @property
    def attachments(self) -> list[str]:
        """Items with a matching AttachmentType."""
        return self._data.get("AttachmentType", [])

    @property
    def provided(self) -> list[str]:
        """Items that provide this slot via AttachmentsProvided."""
        return self._data.get("AttachmentsProvided", [])

    @property
    def replaced(self) -> list[str]:
        """Items that replace this slot via AttachmentReplacement."""
        return self._data.get("AttachmentReplacement", [])

    def get(self, key: str, default=None):
        """
        Get a list of items by raw key.

        Args:
            key (str): The internal item key.
            default: A fallback if the key is missing.

        Returns:
            list[str]: A list of item IDs.
        """
        return self._data.get(key, default)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

    def __str__(self):
        return str(self._data)
    
class AttachmentType:
    """
    Represents an attachment point across all hotbar slots.
    Groups metadata and related items under a specific attachment ID.
    """
    _data = None
    _instances: dict[str, "AttachmentType"] = {}

    def __new__(cls, attachment_id: str):
        """
        Ensure a shared instance per attachment_id.

        Args:
            attachment_id (str): The ID of the attachment point.

        Returns:
            AttachmentType: A shared instance of the attachment type.
        """
        cls._load()
        if attachment_id not in cls._instances:
            cls._instances[attachment_id] = super().__new__(cls)
        return cls._instances[attachment_id]

    def __init__(self, attachment_id: str):
        """
        Initialise the AttachmentType instance with parsed data.

        Args:
            attachment_id (str): The ID of the attachment point.
        """
        if hasattr(self, "attachment_id"):
            return
        self.attachment_id = attachment_id
        self._attachment_data = self._data[attachment_id]

    @classmethod
    def _load(cls):
        """
        Load parsed attachment data from HotbarSlot.
        """
        if cls._data is not None:
            return

        cls._data = HotbarSlot.get_attachment_data()
    
    @classmethod
    def all(cls) -> dict[str, "AttachmentType"]:
        """
        Return all attachment types as a dictionary.

        Returns:
            dict[str, AttachmentType]: Mapping of attachment_id to instance.
        """
        cls._load()
        return {attachment_id: cls(attachment_id) for attachment_id in cls._data}

    @classmethod
    def keys(cls):
        """
        Return all attachment type IDs.

        Returns:
            KeysView[str]: The attachment IDs.
        """
        cls._load()
        return cls._data.keys()

    @classmethod
    def values(cls):
        """
        Return all AttachmentType instances.

        Returns:
            Generator[AttachmentType]: Generator of all instances.
        """
        cls._load()
        return (cls(attachment_id) for attachment_id in cls._data)
    
    @classmethod
    def count(cls) -> int:
        """
        Return the total number of attachment types.

        Returns:
            int: Count of known attachment types.
        """
        cls._load()
        return len(cls._data)

    @classmethod
    def exists(cls, attachment_id: str) -> bool:
        """
        Check if an attachment ID exists in the parsed data.

        Args:
            attachment_id (str): The attachment ID to check.

        Returns:
            bool: True if the attachment exists, False otherwise.
        """
        cls._load()
        return attachment_id in cls._data

    def __repr__(self):
        """
        Return a debug representation of the attachment.

        Returns:
            str: A string in the format <AttachmentType attachment_id>.
        """
        return f"<AttachmentType {self.attachment_id}>"
    
    @property
    def valid(self) -> bool:
        """Whether this AttachmentType instance corresponds to known data."""
        return self.attachment_id in self._data

    @property
    def name(self) -> str:
        """The display name of this attachment (from HotbarSlot)."""
        return self._attachment_data["AttachedLocation"]

    @property
    def slots(self) -> list[str]:
        """List of hotbar slot IDs that use this attachment type."""
        return self._attachment_data["AttachmentsProvided"]

    @property
    def items(self) -> list[str]:
        """List of item IDs that use this attachment via AttachmentType."""
        return self._attachment_data["Items"]
    
    @property
    def wiki_link(self) -> str:
        """Return a wiki-formatted link to this attachment type's display name."""
        return util.link("AttachmentType", self.name, anchor=self.attachment_id)
    
    @property
    def wiki_link_id(self) -> str:
        """Return a wiki-formatted link using the attachment ID as both label and anchor."""
        return util.link("AttachmentType", self.attachment_id, anchor=self.attachment_id)