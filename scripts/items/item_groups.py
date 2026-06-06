"""
Shared item grouping framework.

Defines a small metadata model and base class for assigning items to named
groups, such as weapon types, ammo types, food categories, or clothing sections.
Group subclasses provide the actual classification logic while this module
handles display names, category lookups, ordering, and validation.
"""

from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class GroupInfo:
    """
    Metadata for a single item group.

    Attributes:
        type_id: Internal group identifier used for lookups.
        display_name: Display label used in generated output. Defaults to type_id.
        category: Optional parent category for grouping related types.
        display_order: Sort order used when generating ordered sections.
        metadata: Extra group-specific values for specialised use cases.
    """
    type_id: str
    display_name: str = None
    category: str = None
    display_order: int = 999
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """
        Fill missing display values after initialisation.

        Sets display_name to type_id when no explicit display name was provided.
        """
        if self.display_name is None:
            self.display_name = self.type_id


class ItemGroups(ABC):
    """
    Base class for item grouping systems.

    Subclasses define available groups with GROUPS and implement classify()
    to assign items to one of those group IDs. Shared helper methods provide
    consistent access to labels, categories, ordering, and validation.
    """
    
    # Must be defined by subclasses
    GROUPS: dict[str, GroupInfo] = {}
    
    # Optional: Define explicit category groupings
    CATEGORY_GROUPS: dict[str, list[str]] = {}
    
    @classmethod
    @abstractmethod
    def classify(cls, item, **kwargs) -> str:
        """
        Classify an item into a group type.

        Args:
            item: Item object to classify.
            **kwargs: Optional context required by subclass logic.

        Returns:
            The matching group type ID, or None if the item does not belong to any group.
        """
        pass
    
    @classmethod
    def find_type(cls, item, **kwargs) -> str:
        """
        Classify an item using the subclass rules.

        Args:
            item: Item object to classify.
            **kwargs: Optional context passed through to classify().

        Returns:
            The matching group type ID, or None if no group applies.
        """
        return cls.classify(item, **kwargs)
    
    @classmethod
    def get_group_info(cls, type_id: str) -> GroupInfo:
        """
        Get metadata for a group type.

        Args:
            type_id: Group type ID to look up.

        Returns:
            The matching GroupInfo object, or None if the type ID is not defined.
        """
        return cls.GROUPS.get(type_id)
    
    @classmethod
    def get_display_name(cls, type_id: str) -> str:
        """
        Get the display label for a group type.

        Args:
            type_id: Group type ID to look up.

        Returns:
            The group's display name, or type_id if the group is not defined.
        """
        group = cls.GROUPS.get(type_id)
        return group.display_name if group else type_id
    
    @classmethod
    def get_type_to_display_map(cls) -> dict[str, str]:
        """
        Get all group type IDs mapped to their display labels.

        Returns:
            Dictionary mapping each type ID to its display name.
        """
        return {type_id: group.display_name for type_id, group in cls.GROUPS.items()}
    
    @classmethod
    def get_section_order(cls, include_unordered: bool = False) -> list[str]:
        """
        Get group display labels sorted by display order.

        Args:
            include_unordered: Whether to include groups using the default
                unordered display value.

        Returns:
            Ordered list of group display names.
        """
        if include_unordered:
            sorted_groups = sorted(cls.GROUPS.values(), key=lambda x: x.display_order)
        else:
            # Only include groups with explicit ordering (not default 999)
            sorted_groups = sorted(
                [g for g in cls.GROUPS.values() if g.display_order != 999],
                key=lambda x: x.display_order
            )
        return [g.display_name for g in sorted_groups]
    
    @classmethod
    def get_types_by_category(cls, category: str) -> list[str]:
        """
        Get all group type IDs in a category.

        Args:
            category: Category name to look up.

        Returns:
            List of type IDs in the category. Returns an empty list if the
            category is not found.
        """
        # First check explicit CATEGORY_GROUPS mapping
        if cls.CATEGORY_GROUPS and category in cls.CATEGORY_GROUPS:
            return cls.CATEGORY_GROUPS[category]
        
        # Fallback to search GROUPS for matching category
        return [
            type_id for type_id, group in cls.GROUPS.items()
            if group.category == category
        ]
    
    @classmethod
    def get_all_type_ids(cls) -> list[str]:
        """
        Get every group type ID defined by the class.

        Returns:
            List of all type IDs in GROUPS.
        """
        return list(cls.GROUPS.keys())
    
    @classmethod
    def get_all_categories(cls) -> list[str]:
        """
        Get every category used by the grouping class.

        Returns:
            Sorted list of category names.
        """
        if cls.CATEGORY_GROUPS:
            return sorted(cls.CATEGORY_GROUPS.keys())
        
        # Extract unique categories from GROUPS
        categories = {g.category for g in cls.GROUPS.values() if g.category}
        return sorted(categories)
    
    @classmethod
    def validate_type_id(cls, type_id: str) -> bool:
        """
        Check whether a group type ID is defined.

        Args:
            type_id: Group type ID to check.

        Returns:
            True if the type ID exists in GROUPS, otherwise False.
        """
        return type_id in cls.GROUPS
    
    @classmethod
    def get_groups_by_order(cls) -> list[tuple[str, GroupInfo]]:
        """
        Get all groups sorted by display order.

        Returns:
            List of (type_id, GroupInfo) tuples sorted by display_order.
        """
        sorted_items = sorted(
            cls.GROUPS.items(),
            key=lambda x: x[1].display_order
        )
        return sorted_items
