"""Container item grouping shared by container lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_container_item(item: "Item") -> bool:
    """Return whether an item belongs in container outputs."""
    return bool(item.valid and item.has_category("container"))


class ContainerGroups(ItemGroups):
    """Classify containers by worn location or restricted contents."""

    GROUPS: dict[str, GroupInfo] = {
        "back": GroupInfo("back", "Back", "wearable", 1),
        "torso": GroupInfo("torso", "Torso", "wearable", 2),
        "key_ring": GroupInfo("key_ring", "Key ring", "restricted", 3),
        "wallet": GroupInfo("wallet", "Wallet", "restricted", 4),
        "containers": GroupInfo("containers", "Containers", "general", 5),
    }

    CATEGORY_GROUPS: dict[str, list[str]] = {
        "wearable": ["back", "torso"],
        "restricted": ["key_ring", "wallet"],
        "general": ["containers"],
    }

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        """Return the container group ID for an item."""
        equipped_location = item.can_be_equipped
        if equipped_location and hasattr(equipped_location, "location_id"):
            location_id = equipped_location.location_id
            return "back" if location_id.casefold() == "back" else "torso"

        accept_function = (item.accept_item_function or "").removeprefix(
            "AcceptItemFunction."
        )
        accept_group = {
            "keyring": "key_ring",
            "wallet": "wallet",
        }.get(accept_function.casefold())

        return accept_group or "containers"
