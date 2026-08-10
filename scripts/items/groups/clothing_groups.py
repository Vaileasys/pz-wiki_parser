"""Body-location groups shared by clothing lists and wearable navboxes.

The public grouping classes are intentionally separate:

* :class:`ClothingGroups` owns garments, armour, footwear, tails, and Other.
* :class:`AccessoryGroups` owns the accessory sections used by the wiki.

Both classes read the same ``clothing_table.json`` resource so the combined
clothing item list and the two navboxes use one body-location mapping.
"""

from __future__ import annotations

import os
import re
import typing

from scripts.core import file_loading
from scripts.core.constants import TABLES_DIR
from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


TABLE_PATH = os.path.join(TABLES_DIR, "clothing_table.json")

ACCESSORY_SECTION_ORDER = (
    "Headwear",
    "Eyewear",
    "Masks",
    "Neck",
    "Necklace",
    "Long necklace",
    "Nose",
    "Ears",
    "Gloves",
    "Wrists",
    "Fingers",
    "Belly",
    "Belts",
    "Back",
)

_ACCESSORY_GROUP_NAMES = frozenset(ACCESSORY_SECTION_ORDER)
_EXCLUDED_ID_PREFIXES = (
    "MakeUp_",
    "ZedDmg_",
    "Wound_",
    "Bandage_",
    "F_Hair_",
    "M_Hair_",
    "M_Beard_",
)


def is_wearable_item(item: "Item") -> bool:
    """Return whether an item belongs in clothing/accessory outputs."""
    id_type = item.id_type or ""

    return bool(
        item.valid
        and item.has_category("clothing")
        and not item.obsolete
        and not id_type.startswith(_EXCLUDED_ID_PREFIXES)
        and not id_type.endswith("_Reverse")
    )


def get_wearable_location_id(item: "Item") -> str | None:
    """Return the effective BodyLocation or CanBeEquipped location ID."""
    body_location = item.body_location or item.can_be_equipped
    return getattr(body_location, "location_id", None)


class _BodyLocationGroups(ItemGroups):
    """Private resource-backed implementation shared by the two classifiers."""

    GROUPS: dict[str, GroupInfo] = {}
    INCLUDED_GROUP_NAMES: frozenset[str] | None = None
    EXCLUDED_GROUP_NAMES: frozenset[str] = frozenset()
    DEFAULT_GROUP_ID: str | None = None
    GROUP_CATEGORY = "wearable"
    SECTION_ORDER: tuple[str, ...] | None = None

    _loaded = False
    _body_location_lookup: dict[str, str] = {}
    _all_body_locations: frozenset[str] = frozenset()

    def __init_subclass__(cls, **kwargs) -> None:
        """Give each public classifier independent lazy-loaded state."""
        super().__init_subclass__(**kwargs)
        cls.GROUPS = {}
        cls._loaded = False
        cls._body_location_lookup = {}
        cls._all_body_locations = frozenset()

    @staticmethod
    def _normalise_type_id(display_name: str) -> str:
        """Convert a section heading into a stable snake-case group ID."""
        type_id = re.sub(r"[^a-z0-9]+", "_", display_name.casefold()).strip("_")
        return type_id or "other"

    @classmethod
    def _includes_group(cls, display_name: str) -> bool:
        """Return whether the concrete classifier owns a resource section."""
        if (
            cls.INCLUDED_GROUP_NAMES is not None
            and display_name not in cls.INCLUDED_GROUP_NAMES
        ):
            return False
        return display_name not in cls.EXCLUDED_GROUP_NAMES

    @classmethod
    def _ensure_groups_loaded(cls) -> None:
        """Load this classifier's groups from the clothing-table resource."""
        if cls._loaded:
            return

        data = file_loading.load_json(TABLE_PATH) or {}
        body_locations = data.get("body_locations") or {}

        groups: dict[str, GroupInfo] = {}
        location_lookup: dict[str, str] = {}
        all_locations: set[str] = set()

        for display_order, (display_name, group_data) in enumerate(
            body_locations.items(),
            start=1,
        ):
            locations = tuple(group_data.get("body_location") or ())
            all_locations.update(location.casefold() for location in locations)

            if not cls._includes_group(display_name):
                continue

            type_id = cls._normalise_type_id(display_name)
            groups[type_id] = GroupInfo(
                type_id=type_id,
                display_name=display_name,
                category=cls.GROUP_CATEGORY,
                display_order=display_order,
                metadata={
                    "body_locations": locations,
                    "table": group_data.get("table") or "generic",
                },
            )

            # Preserve the resource's first-match behaviour when a location is
            # listed in more than one section.
            for location_id in locations:
                location_lookup.setdefault(location_id.casefold(), type_id)

        if cls.DEFAULT_GROUP_ID and cls.DEFAULT_GROUP_ID not in groups:
            groups[cls.DEFAULT_GROUP_ID] = GroupInfo(
                type_id=cls.DEFAULT_GROUP_ID,
                display_name="Other",
                category=cls.GROUP_CATEGORY,
                display_order=len(body_locations) + 1,
                metadata={
                    "body_locations": ("Unknown",),
                    "table": "normal",
                },
            )

        cls.GROUPS = groups
        cls._body_location_lookup = location_lookup
        cls._all_body_locations = frozenset(all_locations)
        cls._loaded = True

    @classmethod
    def reset(cls) -> None:
        """Clear resource-derived state so it reloads on next access."""
        cls.GROUPS = {}
        cls._body_location_lookup = {}
        cls._all_body_locations = frozenset()
        cls._loaded = False

    @classmethod
    def classify_location(cls, location_id: str | None) -> str | None:
        """Classify a body location owned by this grouping class.

        Locations owned by the other classifier return ``None``. A genuinely
        unknown location falls back to ``DEFAULT_GROUP_ID`` when configured.
        """
        cls._ensure_groups_loaded()

        if not location_id:
            return None

        normalised = location_id.casefold()
        mapped_group = cls._body_location_lookup.get(normalised)
        if mapped_group:
            return mapped_group

        if normalised in cls._all_body_locations:
            return None

        return cls.DEFAULT_GROUP_ID

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str | None:
        """Classify an item using BodyLocation or CanBeEquipped."""
        location_id = kwargs.get("location_id") or get_wearable_location_id(item)
        return cls.classify_location(location_id)

    @classmethod
    def is_known_body_location(cls, location_id: str | None) -> bool:
        """Return whether clothing_table.json maps a body location anywhere."""
        cls._ensure_groups_loaded()
        return bool(
            location_id
            and location_id.casefold() in cls._all_body_locations
        )

    @classmethod
    def get_table_type(cls, type_id: str) -> str:
        """Return the clothing-table layout configured for a group."""
        group = cls.get_group_info(type_id)
        if group:
            return group.metadata.get("table", "generic")
        return "generic"

    @classmethod
    def get_section_order(cls, include_unordered: bool = False) -> list[str]:
        """Return explicit wiki order or the clothing resource order."""
        cls._ensure_groups_loaded()

        if cls.SECTION_ORDER is None:
            return super().get_section_order(include_unordered=include_unordered)

        available_names = {group.display_name for group in cls.GROUPS.values()}
        return [
            display_name
            for display_name in cls.SECTION_ORDER
            if display_name in available_names
        ]


class ClothingGroups(_BodyLocationGroups):
    """Classify garments, armour, footwear, tails, and unknown locations."""

    EXCLUDED_GROUP_NAMES = _ACCESSORY_GROUP_NAMES
    DEFAULT_GROUP_ID = "other"
    GROUP_CATEGORY = "clothing"


class AccessoryGroups(_BodyLocationGroups):
    """Classify the accessory sections used by the wiki."""

    INCLUDED_GROUP_NAMES = _ACCESSORY_GROUP_NAMES
    SECTION_ORDER = ACCESSORY_SECTION_ORDER
    GROUP_CATEGORY = "accessory"
