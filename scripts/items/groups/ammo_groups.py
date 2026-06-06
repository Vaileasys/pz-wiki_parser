"""
Ammunition item grouping and relationship discovery.

Classifies ammo-related items into rounds, boxes, cartons, and magazines,
then derives their containment hierarchy from crafting recipes. Also links
ammo types to compatible weapons and magazines for generated item data.
"""

from scripts.items.item_groups import ItemGroups, GroupInfo
from scripts.objects.item import Item
from scripts.objects.craft_recipe import CraftRecipe


class AmmoGroups(ItemGroups):
    """
    Item grouping rules for ammunition and magazines.

    Defines recognised ammo groups, their display labels, parent categories,
    and display order. Classification uses recipe-derived containment data
    for boxes and cartons, and item tags for loose rounds and magazines.
    """
    
    GROUPS: dict[str, GroupInfo] = {
        "round": GroupInfo("round", "Ammo rounds", "ammo", 1),
        "box": GroupInfo("box", "Ammo boxes", "ammo", 2),
        "carton": GroupInfo("carton", "Ammo cartons", "ammo", 3),
        "magazine": GroupInfo("magazine", "Magazines", "magazine", 4),
    }
    
    # Category groupings
    CATEGORY_GROUPS: dict[str, list[str]] = {
        "ammo": ["round", "box", "carton"],
        "magazine": ["magazine"],
    }
    
    _box_types_cache: dict[str, dict] = None
    
    @staticmethod
    def build_box_types() -> dict[str, dict]:
        """
        Build ammo container relationships from crafting recipes.

        Reads known unpacking recipes to map boxes and cartons to the item they
        contain, along with the produced quantity. Supports direct recipe outputs
        and item mapper based recipes.

        Returns:
            Dictionary mapping ammo container item IDs to containment data.
        """
        
        box_types = {}
        
        AMMO_RECIPES = {
            "OpenBoxOfShotgunShells": "box",
            "OpenBoxOfBullets50": "box",
            "OpenBoxOfBullets20": "box",
            "OpenCarton12": "carton",
        }

        for recipe_id in AMMO_RECIPES:
            recipe = CraftRecipe(recipe_id)
            output = recipe.outputs[0]

            mapper = output.mapper
            count = output.count
            items = output.items

            if mapper == "ammoTypes":
                # Recipe maps ammo types: ammo_id -> box_id
                item_mappers = recipe.item_mappers.get(mapper, {})
                for key, value in item_mappers.items():
                    box_types[value] = {
                        "type": AMMO_RECIPES.get(recipe_id),
                        "contents": key,
                        "quantity": count,
                    }

            elif mapper == "boxType":
                # OpenCarton12: input 1 carton -> output 12 boxes
                # itemMappers.boxType is box_id -> carton_id
                item_mappers = recipe.item_mappers.get(mapper, {})
                for box_id, carton_id in item_mappers.items():
                    box_types[carton_id] = {
                        "type": AMMO_RECIPES.get(recipe_id),
                        "contents": box_id,
                        "quantity": count,
                    }

            elif items:
                # Direct recipe: specific input -> specific output
                box_types[recipe.inputs[0].items[0]] = {
                    "type": AMMO_RECIPES.get(recipe_id),
                    "contents": items[0],
                    "quantity": count,
                }
        
        return box_types
    
    @classmethod
    def get_box_types(cls) -> dict[str, dict]:
        """
        Get cached ammo container relationship data.

        Builds the mapping on first use, then reuses it for later classification
        and relationship lookups.

        Returns:
            Dictionary mapping ammo container item IDs to containment data.
        """
        if cls._box_types_cache is None:
            cls._box_types_cache = cls.build_box_types()
        
        
        
        return cls._box_types_cache
    
    @classmethod
    def classify(cls, item: Item, **kwargs) -> str:
        """
        Classify an item as an ammunition group type.

        Boxes and cartons are identified from recipe-derived container data.
        Loose rounds are identified by the Ammo tag, while magazines are identified
        by pistol or rifle magazine tags.

        Args:
            item: Item object to classify.
            **kwargs: Additional context accepted for API compatibility.

        Returns:
            Ammo group type ID, or None if the item is not ammo-related.
        """
        ammo_type = None
        
        # Ammunition boxes/cartons (requires box_types)
        box_types = AmmoGroups.get_box_types()
        if box_types and item.item_id in box_types:
            entry = box_types.get(item.item_id, {})
            entry_type = entry.get("type")
            if entry_type == "carton":
                # Verify it's actually a carton (contains a box)
                box_id = entry.get("contents")
                if box_id in box_types and box_types[box_id].get("type") == "box":
                    ammo_type = "carton"
            else:
                ammo_type = entry_type
        
        # Tags-based classification
        elif item.tags:
            tags = item.tags
            # Ammunition rounds
            if any(tag.lower() == "ammo" for tag in tags):
                ammo_type = "round"
            # Magazines
            elif any(tag.lower() in {"pistolmagazine", "riflemagazine"} for tag in tags):
                ammo_type = "magazine"

        return ammo_type
    
    @staticmethod
    def build_ammo_data(
        item_id: str,
        ammo_type: str,
        all_item_data: dict[str, dict]
    ) -> dict:
        """
        Build relationship data for an ammunition item.

        Traces the ammo hierarchy between rounds, boxes, and cartons, then finds
        compatible firearms and magazines by matching each item's ammo type.

        Args:
            item_id: Full item ID to analyse.
            ammo_type: Ammo group type returned by classify().
            all_item_data: Item data dictionary to read from and update.

        Returns:
            The item's data dictionary with related ammo, weapon, and magazine
            fields added where available.
        """
        box_types = AmmoGroups.get_box_types()
        box_data = box_types.get(item_id, {})
        round_id = None
        box_id = None
        carton_id = None
        magazine = None
        weapons = []

        # Trace the containment hierarchy based on item type
        if ammo_type == "carton":
            # Get carton
            carton_id = item_id
            carton_q = 1
            # Get box
            box_id = box_data.get("contents")
            box_q = box_data.get("quantity") or 1
            # Get round
            box_entry = box_types.get(box_id, {})
            if box_entry:
                round_id = box_entry.get("contents")
                qty = box_entry.get("quantity")
                round_q = (qty * box_q) if qty is not None else box_q
            else:
                round_id = None
                round_q = None
                
        elif ammo_type == "box":
            # Get box
            box_id = item_id
            box_q = 1
            # Get round
            round_id = box_data.get("contents")
            round_q = box_data.get("quantity")
            # Get carton (search backwards)
            for key, value in box_types.items():
                if value.get("contents") == box_id:
                    carton_id = key
                    qty = value.get("quantity")
                    carton_q = (qty * box_q) if qty is not None else box_q
                    break
                    
        elif ammo_type == "round":
            # Get round
            round_id = item_id
            round_q = 1
            # Get box (search backwards)
            for key, value in box_types.items():
                if value.get("contents") == item_id:
                    box_id = key
                    box_q = value.get("quantity")
                    break
            # Get carton (search backwards)
            for key, value in box_types.items():
                if value.get("contents") == box_id:
                    carton_id = key
                    qty = value.get("quantity")
                    carton_q = (qty * box_q) if (qty is not None and box_q is not None) else None
                    break

        # Prepare round ID for matching (with and without namespace)
        round_id_short = round_id.split(".", 1)[-1] if (round_id and "." in round_id) else round_id

        def _ammo_matches(ammo_type_val):
            """
            Check whether an ammo type value matches the current round.

            Args:
                ammo_type_val: Ammo type value from a weapon or magazine item.

            Returns:
                True if the value matches the full or short round ID, otherwise False.
            """
            if ammo_type_val is None:
                return False
            return ammo_type_val == round_id or ammo_type_val == round_id_short

        # Find weapons and magazines that use this ammo
        from scripts.items.groups.weapon_groups import WeaponGroups
        
        firearm_types = WeaponGroups.get_types_by_category("firearm")
        for item in Item.values():
            item_type = all_item_data.get(item.item_id, {}).get("TableType")
            
            # Get firearms that use this ammo
            if item_type in firearm_types and _ammo_matches(item.ammo_type):
                weapons.append(item.item_id)
                continue

            # Get magazine that uses this ammo
            if item_type == "magazine" and _ammo_matches(item.ammo_type):
                magazine = item.item_id

        item_data = all_item_data.get(item_id, {})

        # Add data to dict
        if carton_id and carton_id != item_id:
            item_data["AmmoCarton"] = carton_id
            item_data["AmmoCartonQuantity"] = carton_q
        if box_id and box_id != item_id:
            item_data["AmmoBox"] = box_id
            item_data["AmmoBoxQuantity"] = box_q
        if round_id and round_id != item_id:
            item_data["AmmoType"] = round_id
            item_data["AmmoTypeQuantity"] = round_q
        if weapons:
            item_data["Weapons"] = weapons
        if magazine:
            item_data["Magazine"] = magazine

        return item_data
