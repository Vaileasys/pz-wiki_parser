from objects.item import Item

def is_weapon(item: Item) -> bool:
    return item.type == "Weapon"

def is_weapon_part(item: Item) -> bool:
    return item.type == "WeaponPart"

def is_ammo(item: Item) -> bool:
    return (
        item.get("DisplayCategory") == "Ammo"
        or item.has_tag("Ammo", "PistolMagazine", "RifleMagazine")
    )

def is_clothing(item: Item) -> bool:
    return item.type == "Clothing"

def is_container(item: Item) -> bool:
    return item.type == "Container"

def is_fluid_container(item: Item) -> bool:
    return item.fluid_container

def is_food(item: Item) -> bool:
    return (
        item.type == "Food" 
        or item.get("DisplayCategory") == "Food"
        )

def is_fuel(item: Item) -> bool:
    return item.burn_time

def is_animal_part(item: Item) -> bool:
    return item.get("DisplayCategory") in ("AnimalPart", "AnimalPartWeapon")

def is_appearance(item: Item) -> bool:
    return (
        item.get("DisplayCategory") == "Appearance"
        or item.make_up_type
        or item.id_type in ("Razor", "Scissors", "Hairgel", "Hairspray2")
        or item.has_tag("Razor", "Scissors", "DoHairdo", "SlickHair")
    )

def is_camping(item: Item) -> bool:
    return item.get("DisplayCategory") in ("Camping")

def is_communication(item: Item) -> bool:
    return item.get("DisplayCategory") in ("Communications")

def is_cooking(item: Item) -> bool:
    return item.get("DisplayCategory") in ("Cooking", "CookingWeapon")

def is_corpse(item: Item) -> bool:
    return item.get("DisplayCategory") in ("Corpse")

def is_electronics(item: Item) -> bool:
    return item.get("DisplayCategory") in ("Electronics")

def is_fire_source(item: Item) -> bool:
    return (
        item.get("DisplayCategory") in ("FireSource")
        or item.has_tag("StartFire")
        or item.id_type == "PercedWood"
        )

def is_medical(item: Item) -> bool:
    return (
        item.get("DisplayCategory") in ("FirstAid", "FirstAidWeapon")
        or item.can_bandage
        or item.medical
        )

def is_vehicle_maintenance(item: Item) -> bool:
    return item.get("DisplayCategory") in ("VehicleMaintenance", "VehicleMaintenanceWeapon")

def is_literature(item: Item) -> bool:
    return (
        item.type in ("Literature", "Map")
        or item.get("DisplayCategory") in ("Literature")
        )

ITEM_CHECKS = [
    (is_weapon, "weapon"),
    (is_weapon_part, "weapon_part"),
    (is_ammo, "ammo"),
    (is_clothing, "clothing"),
    (is_container, "container"),
    (is_fluid_container, "fluid_container"),
    (is_food, "food"),
    (is_fuel, "fuel"),
    (is_animal_part, "animal_part"),
    (is_appearance, "appearance"),
    (is_camping, "camping"),
    (is_communication, "communication"),
    (is_cooking, "cooking"),
    (is_corpse, "corpse"),
    (is_electronics, "electronics"),
    (is_fire_source, "fire_source"),
    (is_medical, "medical"),
    (is_vehicle_maintenance, "vehicle_maintenance"),
    (is_literature, "literature"),
]

def find_categories(obj: object, *, do_all: bool = False, checks: list[tuple] = ITEM_CHECKS) -> list[str]:
    """
    Determine categories for an object using a list of check functions. Option to return only one (default) or all.

    Args:
        obj (object): The object to evaluate (typically an Item).
        do_all (bool, optional): If True, return all matching categories. If False (default), return only the first match.
        checks (list[tuple], optional): A list of (function, category_name) pairs to check against. 
                                        Each function should return a bool when passed `obj`.

    Returns:
        list[str]: A list of category names. Returns a single-element list if do_all is False,
                   or multiple category names if do_all is True. Returns an empty list if no match is found.
    """
    if do_all:
        return [name for check, name in checks if check(obj)]
    else:
        for check, name in checks:
            if check(obj):
                return [name]
        return []

def find_all_categories(obj: object, *, checks: list[tuple] = ITEM_CHECKS) -> list[str]:
    """
    Return all category names that match the given object.
    This is a shorthand for calling `find_categories` with `do_all=True`.

    Args:
        obj (object): The object to evaluate (typically an Item).
        checks (list[tuple], optional): A list of (function, category_name) pairs to check against.

    Returns:
        list[str]: A list of all category names that match.
    """
    return find_categories(obj, do_all=True, checks=checks)