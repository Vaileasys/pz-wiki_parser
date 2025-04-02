# Helper for media types

import re

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
    "SPR": {"id": "sprinting", "title": "IGUI_perks_Sprinting", "type": "skill", "scale": 50},
    "LFT": {"id": "lightfooted", "title": "IGUI_perks_Lightfooted", "type": "skill", "scale": 50},
    "NIM": {"id": "nimble", "title": "IGUI_perks_Nimble", "type": "skill", "scale": 50},
    "SNE": {"id": "sneaking", "title": "IGUI_perks_Sneaking", "type": "skill", "scale": 50},
    "BAA": {"id": "axe", "title": "IGUI_perks_Axe", "type": "skill", "scale": 50},
    "BUA": {"id": "long_blunt", "title": "IGUI_perks_Blunt", "type": "skill", "scale": 50},
    "CRP": {"id": "carpentry", "title": "IGUI_perks_Carpentry", "type": "skill", "scale": 50},
    "COO": {"id": "cooking", "title": "IGUI_perks_Cooking", "type": "skill", "scale": 50},
    "FRM": {"id": "farming", "title": "IGUI_perks_Farming", "type": "skill", "scale": 50},
    "DOC": {"id": "first_aid", "title": "IGUI_perks_Doctor", "type": "skill", "scale": 50},
    "ELC": {"id": "electricity", "title": "IGUI_perks_Electricity", "type": "skill", "scale": 50},
    "MTL": {"id": "metalworking", "title": "IGUI_perks_Metalworking", "type": "skill", "scale": 50},
    "FKN": {"id": "flint_knapping", "title": "IGUI_perks_FlintKnapping", "type": "skill", "scale": 50},
    "CRV": {"id": "carving", "title": "IGUI_perks_Carving", "type": "skill", "scale": 50},
    "MAS": {"id": "masonry", "title": "IGUI_perks_Masonry", "type": "skill", "scale": 50},
    "POT": {"id": "pottery", "title": "IGUI_perks_Pottery", "type": "skill", "scale": 50},
    "AIM": {"id": "aiming", "title": "IGUI_perks_Aiming", "type": "skill", "scale": 50},
    "REL": {"id": "reloading", "title": "IGUI_perks_Reloading", "type": "skill", "scale": 50},
    "FIS": {"id": "fishing", "title": "IGUI_perks_Fishing", "type": "skill", "scale": 50},
    "TRA": {"id": "trapping", "title": "IGUI_perks_Trapping", "type": "skill", "scale": 50},
    "FOD": {"id": "foraging2", "title": "IGUI_perks_Foraging", "type": "skill", "scale": 50},
    "FOR": {"id": "foraging", "title": "IGUI_perks_Foraging", "type": "skill", "scale": 50},
    "TAI": {"id": "tailoring", "title": "IGUI_perks_Tailoring", "type": "skill", "scale": 50},
    "MEC": {"id": "mechancis", "title": "IGUI_perks_Mechanics", "type": "skill", "scale": 50},
    "CMB": {"id": "combat", "title": "IGUI_perks_Combat", "type": "skill", "scale": 50},
    "SPE": {"id": "spear", "title": "IGUI_perks_Spear", "type": "skill", "scale": 50},
    "SBU": {"id": "short_blunt", "title": "IGUI_perks_SmallBlunt", "type": "skill", "scale": 50},
    "LBA": {"id": "long_blade", "title": "IGUI_perks_LongBlade", "type": "skill", "scale": 50},
    "SBA": {"id": "short_blade", "title": "IGUI_perks_SmallBlade", "type": "skill", "scale": 50},

    # Recipes
    "RCP": {"id": "recipe", "title": "IGUI_HaloNote_LearnedRecipe", "type": "recipe"}
}


def parse_code_effects(full_code: str):
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

            result[code] = result.get(code, 0) + value

    return result