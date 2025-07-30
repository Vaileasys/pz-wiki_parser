# Helper for media types

import re
from scripts.utils import util

# From ISRadioInteractions.lua
CODES = {
    # Moodles
    "ANG": {"id": "anger", "title": "IGUI_HaloNote_Anger", "icon": "File:Mood_Angry_32.png", "type": "moodle", "scale": 5},
    "BOR": {"id": "boredom", "title": "IGUI_HaloNote_Boredom", "icon": "File:Mood_Bored_32.png", "type": "moodle", "scale": 5},
    "END": {"id": "endurance", "title": "IGUI_HaloNote_Endurance", "icon": "File:Status_DifficultyBreathing_32.png", "type": "moodle", "scale": 5},
    "FAT": {"id": "fatigue", "title": "IGUI_HaloNote_Fatigue", "icon": "File:Mood_Sleepy_32.png", "type": "moodle", "scale": 5},
    "FIT": {"id": "fitness", "title": "IGUI_HaloNote_Fitness", "type": "moodle", "scale": 5},
    "HUN": {"id": "hunger", "title": "IGUI_HaloNote_Hunger", "icon": "File:Status_Hunger_32.png", "type": "moodle", "scale": 5},
    "MOR": {"id": "morale", "title": "IGUI_HaloNote_Morale", "type": "moodle", "scale": 5},
    "STS": {"id": "stress", "title": "IGUI_HaloNote_Stress", "icon": "File:Mood_Stressed_32.png", "type": "moodle", "scale": 0.05},
    "FEA": {"id": "fear", "title": "IGUI_HaloNote_Fear", "icon": "File:Mood_Scared_32.png", "type": "moodle", "scale": 0.05},
    "PAN": {"id": "panic", "title": "IGUI_HaloNote_Panic", "icon": "File:Mood_Panicked_32.png", "type": "moodle", "scale": 5},
    "SAN": {"id": "sanity", "title": "IGUI_HaloNote_Sanity", "type": "moodle", "scale": 5},
    "SIC": {"id": "sickness", "title": "IGUI_HaloNote_Sickness", "icon": "File:Mood_Nauseous_32.png", "type": "moodle", "scale": 5},
    "PAI": {"id": "pain", "title": "IGUI_HaloNote_Pain", "icon": "File:Mood_Pained_32.png", "type": "moodle", "scale": 5},
    "DRU": {"id": "drunkenness", "title": "IGUI_HaloNote_Drunkenness", "icon": "File:Mood_Drunk_32.png", "type": "moodle", "scale": 5},
    "THI": {"id": "thirst", "title": "IGUI_HaloNote_Thirst", "icon": "File:Status_Thirst_32.png", "type": "moodle", "scale": 5},
    "UHP": {"id": "unhappiness", "title": "IGUI_HaloNote_Unhappiness", "icon": "File:Mood_Sad_32.png", "type": "moodle", "scale": 5},

    # Skills
    # TODO: connect skills with Skill class
    # TODO: fix scale. Seems to be 12.5 for RecMedia, but 50 for RadioData
    "SPR": {"id": "sprinting", "title": "IGUI_perks_Sprinting", "icon": "File:ShoesRunningBlue.png", "type": "skill", "scale": 12.5},
    "LFT": {"id": "lightfooted", "title": "IGUI_perks_Lightfooted", "icon": "File:Trait_clumsy.png", "type": "skill", "scale": 12.5},
    "NIM": {"id": "nimble", "title": "IGUI_perks_Nimble", "icon": "File:Trait_graceful.png", "type": "skill", "scale": 12.5},
    "SNE": {"id": "sneaking", "title": "IGUI_perks_Sneaking", "icon": "File:Trait_inconspicuous.png", "type": "skill", "scale": 12.5},
    "BAA": {"id": "axe", "title": "IGUI_perks_Axe", "icon": "File:Axe.png", "type": "skill", "scale": 12.5},
    "BUA": {"id": "long_blunt", "title": "IGUI_perks_Blunt", "icon": "File:BaseballBat.png", "type": "skill", "scale": 12.5},
    "CRP": {"id": "carpentry", "title": "IGUI_perks_Carpentry", "icon": "File:Hammer.png", "type": "skill", "scale": 12.5},
    "COO": {"id": "cooking", "title": "IGUI_perks_Cooking", "icon": "File:PanFull.png", "type": "skill", "scale": 12.5},
    "FRM": {"id": "farming", "title": "IGUI_perks_Farming", "icon": "File:TZ_IndieStoneNPK.png", "type": "skill", "scale": 12.5},
    "DOC": {"id": "first_aid", "title": "IGUI_perks_Doctor", "icon": "File:Bandage.png", "type": "skill", "scale": 12.5},
    "ELC": {"id": "electricity", "title": "IGUI_perks_Electricity", "icon": "File:ElectronicsScrap.png", "type": "skill", "scale": 12.5},
    "MTL": {"id": "metalworking", "title": "IGUI_perks_MetalWelding", "icon": "File:BlowTorch.png", "type": "skill", "scale": 12.5},
    "FKN": {"id": "flint_knapping", "title": "IGUI_perks_FlintKnapping", "icon": "File:FlintAngular.png", "type": "skill", "scale": 12.5},
    "CRV": {"id": "carving", "title": "IGUI_perks_Carving", "icon": "File:KnifeFlint.png", "type": "skill", "scale": 12.5},
    "MAS": {"id": "masonry", "title": "IGUI_perks_Masonry", "icon": "File:MasonTrowel.png", "type": "skill", "scale": 12.5},
    "POT": {"id": "pottery", "title": "IGUI_perks_Pottery", "icon": "File:ClayJar_Glazed_Unfired.png", "type": "skill", "scale": 12.5},
    "AIM": {"id": "aiming", "title": "IGUI_perks_Aiming", "icon": "File:Trait_hunter.png", "type": "skill", "scale": 12.5},
    "REL": {"id": "reloading", "title": "IGUI_perks_Reloading", "icon": "File:BerettaClip.png", "type": "skill", "scale": 12.5},
    "FIS": {"id": "fishing", "title": "IGUI_perks_Fishing", "icon": "File:FishingTackle.png", "type": "skill", "scale": 12.5},
    "TRA": {"id": "trapping", "title": "IGUI_perks_Trapping", "icon": "File:TrapBox.png", "type": "skill", "scale": 12.5},
    "FOD": {"id": "foraging2", "title": "IGUI_perks_Foraging", "icon": "File:Trait_outdoorsman.png", "type": "skill", "scale": 12.5},
    "FOR": {"id": "foraging", "title": "IGUI_perks_Foraging", "icon": "File:Trait_outdoorsman.png", "type": "skill", "scale": 12.5},
    "TAI": {"id": "tailoring", "title": "IGUI_perks_Tailoring", "icon": "File:Thread.png", "type": "skill", "scale": 12.5},
    "MEC": {"id": "mechancis", "title": "IGUI_perks_Mechanics", "icon": "File:LugWrench.png", "type": "skill", "scale": 12.5},
    "CMB": {"id": "combat", "title": "IGUI_perks_Combat", "icon": "File:AssaultRifle.png", "type": "skill", "scale": 12.5},
    "SPE": {"id": "spear", "title": "IGUI_perks_Spear", "icon": "File:SpearStick.png", "type": "skill", "scale": 12.5},
    "SBU": {"id": "short_blunt", "title": "IGUI_perks_SmallBlunt", "icon": "File:ClubHammer.png", "type": "skill", "scale": 12.5},
    "LBA": {"id": "long_blade", "title": "IGUI_perks_LongBlade", "icon": "File:Katana.png", "type": "skill", "scale": 12.5},
    "SBA": {"id": "short_blade", "title": "IGUI_perks_SmallBlade", "icon": "File:KnifeChopping.png", "type": "skill", "scale": 12.5},

    # Recipes
    "RCP": {"id": "recipe", "title": "IGUI_HaloNote_LearnedRecipe", "type": "recipe"}
}


def parse_code_effects(full_code: str) -> dict[str, str | int | float]:
    parts = re.split(r',+', full_code)
    result = {}

    for part in parts:
        # Handle RCP
        if '=' in part:
            code, value = part.split('=', 1)
            if CODES.get(code, {}).get("type") == "recipe":
                result[code] = value.strip()
            continue

        # Handle numeric codes
        match = re.match(r'([A-Z]+)([+-]\d*\.?\d+)', part)
        if match:
            code, raw_value = match.groups()
            try:
                value = float(raw_value)
            except ValueError:
                continue

            scale = CODES.get(code, {}).get("scale", 1)
            value *= scale

            value = util.convert_int(result.get(code, 0) + value)

            result[code] = value

    return result

def get_code_name(code: str) -> str:
    """
    Returns the translated name of a code based on its title ID.
    
    Args:
        code (str): The short effect code, e.g., "BOR", "CRP", "RCP"
    
    Returns:
        str: Translated name if available, or the raw code if not found.
    """
    code_info = CODES.get(code)
    if not code_info:
        return code

    title_id = code_info.get("title")
    if not title_id:
        return code

    from scripts.core.language import Translate
    return Translate.get(title_id)

def get_icon(code: str, value: int | float = None, size: str = "32px") -> str | None:
    """
    Returns a wiki image for the code's icon, or None if there isn't one.
    If it's a recipe (i.e. RCP), this returns None so text can be displayed instead.
    """
    if code.startswith("RCP"):
        return None

    code_info = CODES.get(code)
    if not code_info:
        return None

    icon_file = code_info.get("icon")
    if not icon_file:
        return None
    
    name = get_code_name(code)

    if value is not None:
        from scripts.utils import util
        effect = util.format_positive(value)
        label = f"{effect} {name}"
    else:
        label = name

    return f"[[{icon_file}|{size}|link={name}|{label}]]"