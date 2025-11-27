import os
import re
from typing import Dict, List
from scripts.core.cache import load_cache
from scripts.core.constants import CACHE_DIR
from scripts.core.language import Translate
from scripts.utils import echo


# Mapping for descriptor replacements in merged templates
DESCRIPTOR_MAP = {
    "Shoddy": "Basic",
    "Poor": "Advanced",
    "Good": "Craftsman",
}


def extract_base_name(entity_name: str) -> str:
    """
    Extract the base name from an entity name by removing level suffix.

    Args:
        entity_name (str): Full entity name (e.g., "Wood_BarElementCorner_Lvl1")

    Returns:
        str: Base name without level suffix (e.g., "Wood_BarElementCorner")
    """
    # Remove _LvlX, _Lvl_X, LvlX, or Lvl_X patterns (underscore before Lvl is optional)
    base_name = re.sub(r"_?Lvl_?\d+$", "", entity_name, flags=re.IGNORECASE)
    return base_name


def group_entities_by_base(entity_data: Dict[str, dict]) -> Dict[str, List[tuple]]:
    """
    Group entities by their base name, sorting level variants together.

    Args:
        entity_data (Dict[str, dict]): Dictionary of all entity definitions

    Returns:
        Dict[str, List[tuple]]: Dictionary mapping base names to list of (entity_name, entity_def) tuples
    """
    grouped: Dict[str, List[tuple]] = {}

    for entity_name, entity_def in entity_data.items():
        # Skip entities starting with ES_
        if entity_name.startswith("ES_"):
            continue

        base_name = extract_base_name(entity_name)

        if base_name not in grouped:
            grouped[base_name] = []

        grouped[base_name].append((entity_name, entity_def))

    # Sort each group by level number
    for base_name in grouped:
        grouped[base_name].sort(key=lambda x: x[0])  # Sort by entity name

    return grouped


def get_translated_name(entity_def: dict) -> str:
    """
    Get the translated display name for an entity.

    Args:
        entity_def (dict): Entity definition dictionary.

    Returns:
        str: Translated display name.
    """
    outputs = entity_def.get("outputs", [])
    if outputs and len(outputs) > 0:
        display_name_key = outputs[0].get("displayName", "")
        translated = Translate.get(display_name_key, "DisplayName")
        if translated and translated != display_name_key:
            return translated
        return display_name_key
    return ""


def extract_descriptor(display_name: str) -> str:
    """
    Extract the descriptor (text in parentheses) from a display name.

    Args:
        display_name (str): Full display name like "Wooden Wall (Shoddy)"

    Returns:
        str: The descriptor text like "Shoddy", or empty string if none found.
    """
    match = re.search(r"\(([^)]+)\)\s*$", display_name)
    if match:
        return match.group(1)
    return ""


def map_descriptor(descriptor: str) -> str:
    """
    Map a descriptor to its replacement value.

    Args:
        descriptor (str): Original descriptor (e.g., "Shoddy")

    Returns:
        str: Mapped descriptor (e.g., "Basic") or original if no mapping exists.
    """
    return DESCRIPTOR_MAP.get(descriptor, descriptor)


def get_min_level(entity_def: dict) -> str:
    """
    Extract the minimum skill level required to build an entity.

    Args:
        entity_def (dict): Entity definition dictionary.

    Returns:
        str: Minimum skill level as string, or empty string if none.
    """
    skill_required = entity_def.get("SkillRequired", [])
    if skill_required and len(skill_required) > 0:
        skill_dict = skill_required[0]
        for _, skill_level in skill_dict.items():
            return str(skill_level)
    return ""


def build_health_template_single(
    entity_name: str,
    entity_def: dict,
) -> str:
    """
    Build a health template for a single entity (not merged).

    Args:
        entity_name (str): Name identifier of the entity.
        entity_def (dict): Entity definition dictionary.

    Returns:
        str: MediaWiki health template markup.
    """
    # Get display name
    display_name = get_translated_name(entity_def)
    if not display_name:
        display_name = entity_name

    # Get health values
    health = entity_def.get("health", "")
    skill_bonus = entity_def.get("skillBaseHealth", "")
    min_level = get_min_level(entity_def)

    lines = [
        "{{Construction hp/sandbox\n",
        f"|name={display_name}\n",
        f"|health={health}\n",
        f"|skill_bonus={skill_bonus}\n",
        f"|min_level={min_level}\n",
        "}}",
    ]

    return "".join(lines)


def build_health_template_merged(
    base_name: str,
    entity_variants: List[tuple],
) -> str:
    """
    Build a merged health template for all level variants of an entity.

    Args:
        base_name (str): Base name without level suffix.
        entity_variants (List[tuple]): List of (entity_name, entity_def) tuples.

    Returns:
        str: MediaWiki health template markup with merged level variants.
    """
    lines = ["{{Construction hp/sandbox\n"]

    for idx, (entity_name, entity_def) in enumerate(entity_variants, 1):
        # Get display name and extract descriptor for merged items
        display_name = get_translated_name(entity_def)
        if not display_name:
            display_name = entity_name

        # For merged items, use the descriptor (text in parentheses) as the name
        descriptor = extract_descriptor(display_name)
        # Map the descriptor to its replacement value
        name_value = map_descriptor(descriptor) if descriptor else display_name

        # Get health values
        health = entity_def.get("health", "")
        skill_bonus = entity_def.get("skillBaseHealth", "")
        min_level = get_min_level(entity_def)

        # Build parameter suffix (empty for first, "2", "3", etc. for rest)
        suffix = "" if idx == 1 else str(idx)

        lines.append(f"|name{suffix}={name_value}\n")
        lines.append(f"|health{suffix}={health}\n")
        lines.append(f"|skill_bonus{suffix}={skill_bonus}\n")
        lines.append(f"|min_level{suffix}={min_level}\n")

    lines.append("}}")

    return "".join(lines)


def has_health_values(entity_def: dict) -> bool:
    """
    Check if an entity has both health and skillBaseHealth values.

    Args:
        entity_def (dict): Entity definition dictionary.

    Returns:
        bool: True if entity has both health and skillBaseHealth values.
    """
    health = entity_def.get("health")
    skill_base_health = entity_def.get("skillBaseHealth")
    return health is not None and skill_base_health is not None


def generate_health_templates(
    grouped_entities: Dict[str, List[tuple]],
    lang_code: str,
) -> Dict[str, str]:
    """
    Generate health templates for all entities.

    Args:
        grouped_entities (Dict[str, List[tuple]]): Dictionary mapping base names to entity variants.
        lang_code (str): Language code for output directory.

    Returns:
        Dict[str, str]: Dictionary mapping base names to their health template markup.
    """
    output_directory = os.path.join("output", lang_code, "tiles", "entity_hp")
    os.makedirs(output_directory, exist_ok=True)

    templates: Dict[str, str] = {}

    for base_name, entity_variants in grouped_entities.items():
        # Skip entities starting with ES_
        if base_name.startswith("ES_"):
            continue

        # Filter variants to only include those with health and skillBaseHealth values
        valid_variants = [
            (name, defn) for name, defn in entity_variants if has_health_values(defn)
        ]

        # Skip if no valid variants remain
        if not valid_variants:
            continue

        try:
            # Determine if this is a merged entity or single entity
            if len(valid_variants) > 1:
                # Multiple level variants - use merged template
                template_text = build_health_template_merged(base_name, valid_variants)
            else:
                # Single entity - use single template
                entity_name, entity_def = valid_variants[0]
                template_text = build_health_template_single(entity_name, entity_def)

            templates[base_name] = template_text

            # Write to file
            filename = base_name.replace(" ", "_") + ".txt"
            output_path = os.path.join(output_directory, filename)
            with open(output_path, "w", encoding="utf-8") as fh:
                fh.write(template_text)

        except Exception as exc:
            echo.error(f"Failed to generate health template for '{base_name}': {exc}")

    return templates


def main(lang_code: str, entity_data: Dict[str, dict] = None) -> Dict[str, str]:
    """
    Main execution function for entity health template generation.

    Args:
        lang_code (str): Language code to process
        entity_data (Dict[str, dict], optional): Pre-loaded entity data. If None, loads from cache.

    Returns:
        Dict[str, str]: Dictionary mapping base names to their health template markup.

    This function:
    1. Loads the parsed entity data cache (if not provided)
    2. Groups entities by base name (merging level variants)
    3. Generates health templates
    4. Outputs files to output/{lang_code}/tiles/entity_hp/
    """

    # Load entity data if not provided
    if entity_data is None:
        ENTITY_CACHE_FILE = "parsed_entity_data.json"
        entity_path = os.path.join(CACHE_DIR, ENTITY_CACHE_FILE)

        try:
            entity_data = load_cache(entity_path, "Entity")
        except Exception as exc:
            echo.error(f"Failed to load entity cache: {exc}")
            echo.error(
                "Make sure the entity cache exists by running the script parser first"
            )
            return {}

    if not entity_data:
        echo.error("Entity data is empty, skipping generation")
        return {}

    # Group entities by base name (merge level variants)
    grouped_entities = group_entities_by_base(entity_data)

    # Generate health templates
    templates = generate_health_templates(grouped_entities, lang_code)

    return templates
