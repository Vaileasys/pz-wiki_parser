"""
Weapon item grouping and classification.

Classifies weapons by melee skill, firearm type, explosives, and weapon parts,
then exposes their display names, categories, and ordering for generated
navboxes, lists, and item data.
"""
import typing

from scripts.utils import echo
from scripts.items.item_groups import ItemGroups, GroupInfo

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item



class WeaponGroups(ItemGroups):
    """
    Item grouping rules for weapons and weapon-related items.

    Defines the recognised weapon groups, their display labels, parent
    categories, and display order. Classification is based on weapon skill
    categories, firearm properties, display category, or item type.
    """
    
    GROUPS: dict[str, GroupInfo] = {
        # Melee weapons
        "axe": GroupInfo("axe", "Axes", "melee", 1),
        "blunt": GroupInfo("blunt", "Long blunt", "melee", 2),
        "smallblunt": GroupInfo("smallblunt", "Short blunt", "melee", 3),
        "longblade": GroupInfo("longblade", "Long blades", "melee", 4),
        "smallblade": GroupInfo("smallblade", "Short blades", "melee", 5),
        "spear": GroupInfo("spear", "Spears", "melee", 6),
        "improvised": GroupInfo("improvised", "Improvised", "melee", 7),
        "unarmed": GroupInfo("unarmed", "Unarmed", "melee", 8),
        
        # Firearms
        "handgun": GroupInfo("handgun", "Handguns", "firearm", 9),
        "rifle": GroupInfo("rifle", "Rifles", "firearm", 10),
        "shotgun": GroupInfo("shotgun", "Shotguns", "firearm", 11),
        
        # Other weapon-related
        "explosive": GroupInfo("explosive", "Explosives", "explosive", 12),
        "weapon_part": GroupInfo("weapon_part", "Weapon parts", "weapon_part", 13),
    }
    
    # Category groupings
    CATEGORY_GROUPS: dict[str, list[str]] = {
        "melee": ["axe", "blunt", "smallblunt", "longblade", "smallblade", 
                  "spear", "improvised", "unarmed"],
        "firearm": ["handgun", "shotgun", "rifle"],
        "explosive": ["explosive"],
        "weapon_part": ["weapon_part"],
    }
    
    @classmethod
    def classify(cls, item: Item, **kwargs) -> str | None:
        """
        Classify an item as a weapon group type.

        Weapons with skill categories are grouped by their primary skill, with
        "Improvised" ignored when another skill is present. Firearms are grouped
        as handguns, rifles, or shotguns based on equipment and projectile data.
        Explosives and weapon parts are handled by display category or item type.

        Args:
            item: Item object to classify.
            **kwargs: Additional context accepted for API compatibility.

        Returns:
            Weapon group type ID, or None if the item is not weapon-related.
        """
        
        table_type = None

        # Weapons
        if item.item_type == "weapon":
            skill = item.categories
            if skill:
                # Melee weapons - classified by skill category
                # Remove "Improvised" if there are other categories
                if "Improvised" in skill and len(skill) > 1:
                    skill = [cat for cat in skill if cat != "Improvised"]
                    if len(skill) > 1:
                        echo.warning(f"More than 1 skill ({','.join(skill)})")
                table_type = skill[0]
            elif item.subcategory == "Firearm":
                # Firearms - classified by equipment requirements
                table_type = "handgun"
                if item.requires_equipped_both_hands:
                    table_type = "rifle"
                    if int(item.projectile_count) > 1:
                        table_type = "shotgun"
            elif item.raw_display_category == "Explosives":
                table_type = "explosive"
        
        # Weapon parts
        elif item.item_type == "weaponpart":
            table_type = "weapon_part"

        return table_type
