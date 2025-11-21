import os
import re
from typing import Dict, List, Tuple
from scripts.core.cache import load_cache
from scripts.core.constants import CACHE_DIR
from scripts.core.version import Version
from scripts.core.language import Translate
from scripts.utils import echo

_SKILL_TO_WIKI = {
    'Woodwork': '{{ll|Carpentry}}',
    'Electricity': '{{ll|Electrical}}',
    'Farming': '{{ll|Farming}}',
    'MetalWelding': '{{ll|Welding}}',
    'Strength': '{{ll|Strength}}',
}

_TOOL_TYPE_MAP = {
    "Hammer": "tag", "Shovel": "tag",
    "Wrench": "tool", "Electrician": "tool",
    "Crowbar": "tool", "Cutter": "tag",
}

_TOOL_VALUE_MAP = {
    "Hammer": "Hammer", "Shovel": "DigPlow",
    "Wrench": "Wrench", "Electrician": "Screwdriver",
    "Crowbar": "Crowbar", "Cutter": "Cutter",
}

_TOOL_SKILL_MAP = {
    "Hammer": "{{ll|Carpentry}}", "Shovel": "{{ll|Farming}}",
    "Wrench": "None", "Electrician": "{{ll|Electrical}}",
    "Crowbar": "{{ll|Carpentry}}", "Cutter": "{{ll|Carpentry}}",
}


def _build_composite_sprite_name(sprite_ids: List[str]) -> str:
    """
    Generate a composite name from multiple sprite IDs.

    Args:
        sprite_ids (List[str]): List of sprite identifiers.

    Returns:
        str: Combined name where sprites are joined with '+'.
    """
    if not sprite_ids:
        return ""
    if len(sprite_ids) == 1:
        return sprite_ids[0]
    
    # Join all sprite IDs with +
    return "+".join(sprite_ids)


def build_entity_icon_params(sprite_outputs: Dict[str, List[str]]) -> Tuple[List[str], List[str]]:
    """
    Generate icon and sprite_id parameters from spriteOutputs.

    Args:
        sprite_outputs (Dict[str, List[str]]): Dictionary mapping facing directions to sprite lists.

    Returns:
        Tuple[List[str], List[str]]: Tuple containing (icon_lines, sprite_id_lines).
    """
    facing_map = {"S": "South", "W": "West", "N": "North", "E": "East", "SINGLE": "East"}
    facing_order = ["S", "E", "N", "W", "SINGLE"]
    
    icon_lines: List[str] = []
    sprite_id_lines: List[str] = []
    
    icon_idx = 1
    sprite_idx = 1
    for facing in facing_order:
        if facing not in sprite_outputs:
            continue
        
        sprites = sprite_outputs[facing]
        if not sprites:
            continue
        
        # Create composite name from all sprites in this direction for the icon
        composite_name = _build_composite_sprite_name(sprites)
        
        suffix = "" if icon_idx == 1 else str(icon_idx)
        icon_lines.append(f"|icon{suffix}={composite_name}.png\n")
        
        direction = facing_map.get(facing)
        if direction:
            icon_lines.append(f"|icon_name{suffix}={direction} sprite\n")
        
        # Add each sprite as a separate sprite_id parameter
        for sprite in sprites:
            sprite_suffix = "" if sprite_idx == 1 else str(sprite_idx)
            sprite_id_lines.append(f"|sprite_id{sprite_suffix}={sprite}\n")
            sprite_idx += 1
        
        icon_idx += 1
    
    return icon_lines, sprite_id_lines


def build_entity_infobox(
    entity_name: str,
    entity_def: dict,
    lang_code: str,
    game_version: str
) -> str:
    """
    Build a complete infobox template for an entity.

    Args:
        entity_name (str): Name identifier of the entity.
        entity_def (dict): Entity definition dictionary.
        lang_code (str): Language code for translations.
        game_version (str): Current game version.

    Returns:
        str: Complete MediaWiki infobox template markup.
    """
    
    # Get display name from outputs
    outputs = entity_def.get("outputs", [])
    if outputs and len(outputs) > 0:
        display_name_key = outputs[0].get("displayName", "")
        # Try to translate the display name
        translated = Translate.get(display_name_key, "DisplayName")
        if translated and translated != display_name_key:
            display_name = translated
        else:
            display_name = display_name_key
    else:
        display_name = entity_name
    
    # Get sprite outputs for icons
    sprite_outputs = entity_def.get("spriteOutputs", {})
    icon_lines, sprite_id_lines = build_entity_icon_params(sprite_outputs)
    
    # Get category
    category = entity_def.get("category", "Construction")
    category_line = f"|category={category}\n"
    
    # Get skill requirements
    skill_lines: List[str] = []
    skill_required = entity_def.get("SkillRequired", [])
    if skill_required and len(skill_required) > 0:
        # SkillRequired is a list of dicts like [{"Woodwork": 4}]
        skill_dict = skill_required[0]
        for skill_name, skill_level in skill_dict.items():
            wiki_skill = _SKILL_TO_WIKI.get(skill_name, f"{{{{ll|{skill_name}}}}}")
            skill_lines.append(f"|build_skill={wiki_skill}\n")
            skill_lines.append(f"|build_level={skill_level}\n")
            break
    
    # Get build tool from timedAction
    timed_action = entity_def.get("timedAction", "")
    if timed_action:
        # Extract tool from timedAction (e.g., "BuildWallHammer" -> "Hammer")
        for tool_key in _TOOL_TYPE_MAP.keys():
            if tool_key in timed_action:
                tt = _TOOL_TYPE_MAP.get(tool_key)
                if tt == "tool":
                    skill_lines.append(f"|build_tool={{{{ll|{_TOOL_VALUE_MAP[tool_key]}}}}}\n")
                else:
                    tag_value = "tag"
                    if _TOOL_VALUE_MAP[tool_key] == "Cutter":
                        tag_links = []
                        for cutter_item in ("SharpKnife", "Scissors"):
                            link = (f"Item tag/{lang_code}#tag-{cutter_item}"
                                    if lang_code.lower() != "en"
                                    else f"Item tag#tag-{cutter_item}")
                            tag_links.append(f"[[{link}|{cutter_item} ({tag_value})]]")
                        extras = ["{{ll|Kitchen Knife}}", "{{ll|Scissors}}", "{{ll|Hunting Knife}}", "{{ll|Chipped Stone}}"]
                        skill_lines.append("|build_tool=" + "<br>".join(tag_links + extras) + "\n")
                    else:
                        link = (f"Item tag/{lang_code}#tag-{_TOOL_VALUE_MAP[tool_key]}"
                                if lang_code.lower() != "en"
                                else f"Item tag#tag-{_TOOL_VALUE_MAP[tool_key]}")
                        skill_lines.append(f"|build_tool=[[{link}|{_TOOL_VALUE_MAP[tool_key]} ({tag_value})]]\n")
                break
    
    # Assemble the infobox
    lines = [
        "{{Infobox tile\n",
        f"|name={display_name}\n",
        *icon_lines,
        category_line,
        *skill_lines,
        *sprite_id_lines,
        f"|infobox_version={game_version}\n",
        "}}"
    ]
    
    infobox_text = "".join(lines)
    return infobox_text


def generate_entity_infoboxes(
    entity_data: Dict[str, dict],
    lang_code: str,
    game_version: str
) -> Dict[str, str]:
    """
    Generate infobox templates for all entities.

    Args:
        entity_data (Dict[str, dict]): Dictionary of entity definitions.
        lang_code (str): Language code for translations.
        game_version (str): Current game version.

    Returns:
        Dict[str, str]: Dictionary mapping entity names to their infobox markup.
    """
    
    output_directory = os.path.join("output", lang_code, "tiles", "entity_infoboxes")
    os.makedirs(output_directory, exist_ok=True)
    
    infoboxes: Dict[str, str] = {}
    
    for idx, (entity_name, entity_def) in enumerate(entity_data.items(), 1):
        
        if not isinstance(entity_def, dict):
            echo.error(f"Skipping entity '{entity_name}': expected a dict, got {type(entity_def)}")
            continue
        
        try:
            infobox_text = build_entity_infobox(
                entity_name,
                entity_def,
                lang_code,
                game_version
            )
            infoboxes[entity_name] = infobox_text
            
            # Write to file
            filename = entity_name.replace(" ", "_") + ".txt"
            output_path = os.path.join(output_directory, filename)
            with open(output_path, "w", encoding="utf-8") as fh:
                fh.write(infobox_text)
        except Exception as exc:
            echo.error(f"Failed to generate infobox for entity '{entity_name}': {exc}")

    return infoboxes


def build_merged_entity_infobox(
    base_name: str,
    entity_variants: List[tuple],
    lang_code: str,
    game_version: str
) -> str:
    """
    Build a merged infobox for all level variants of an entity.

    Args:
        base_name (str): Base name without level suffix.
        entity_variants (List[tuple]): List of (entity_name, entity_def) tuples.
        lang_code (str): Language code for translations.
        game_version (str): Current game version.

    Returns:
        str: Complete MediaWiki infobox template markup with merged level variants.
    """
    # Use the first variant for display name (without level descriptor)
    first_entity_name, first_entity_def = entity_variants[0]
    
    # Get display name from outputs
    outputs = first_entity_def.get("outputs", [])
    if outputs and len(outputs) > 0:
        display_name_key = outputs[0].get("displayName", "")
        translated = Translate.get(display_name_key, "DisplayName")
        if translated and translated != display_name_key:
            display_name = translated
        else:
            display_name = display_name_key
    else:
        display_name = base_name
    
    # Remove level descriptors like "(Shoddy)", "(Sturdy)", "(Solid)"
    display_name = re.sub(r'\s*\([^)]+\)\s*$', '', display_name)
    
    # Get category from first variant
    category = first_entity_def.get("category", "Construction")
    category_line = f"|category={category}\n"
    
    # Collect skill requirements from all level variants
    skill_lines: List[str] = []
    skill_name_for_all = None
    build_levels: List[str] = []
    
    for entity_name, entity_def in entity_variants:
        skill_required = entity_def.get("SkillRequired", [])
        if skill_required and len(skill_required) > 0:
            skill_dict = skill_required[0]
            for skill_name, skill_level in skill_dict.items():
                if skill_name_for_all is None:
                    skill_name_for_all = skill_name
                build_levels.append(str(skill_level))
                break
    
    if skill_name_for_all and build_levels:
        wiki_skill = _SKILL_TO_WIKI.get(skill_name_for_all, f"{{{{ll|{skill_name_for_all}}}}}")
        skill_lines.append(f"|build_skill={wiki_skill}\n")
        skill_lines.append(f"|build_level={', '.join(build_levels)}\n")
    
    # Get build tool from first variant's timedAction
    timed_action = first_entity_def.get("timedAction", "")
    if timed_action:
        # Extract tool from timedAction (e.g., "BuildWallHammer" -> "Hammer")
        for tool_key in _TOOL_TYPE_MAP.keys():
            if tool_key in timed_action:
                tt = _TOOL_TYPE_MAP.get(tool_key)
                if tt == "tool":
                    skill_lines.append(f"|build_tool={{{{ll|{_TOOL_VALUE_MAP[tool_key]}}}}}\n")
                else:
                    tag_value = "tag"
                    if _TOOL_VALUE_MAP[tool_key] == "Cutter":
                        tag_links = []
                        for cutter_item in ("SharpKnife", "Scissors"):
                            link = (f"Item tag/{lang_code}#tag-{cutter_item}"
                                    if lang_code.lower() != "en"
                                    else f"Item tag#tag-{cutter_item}")
                            tag_links.append(f"[[{link}|{cutter_item} ({tag_value})]]")
                        extras = ["{{ll|Kitchen Knife}}", "{{ll|Scissors}}", "{{ll|Hunting Knife}}", "{{ll|Chipped Stone}}"]
                        skill_lines.append("|build_tool=" + "<br>".join(tag_links + extras) + "\n")
                    else:
                        link = (f"Item tag/{lang_code}#tag-{_TOOL_VALUE_MAP[tool_key]}"
                                if lang_code.lower() != "en"
                                else f"Item tag#tag-{_TOOL_VALUE_MAP[tool_key]}")
                        skill_lines.append(f"|build_tool=[[{link}|{_TOOL_VALUE_MAP[tool_key]} ({tag_value})]]\n")
                break
    
    # Build icons and sprite IDs for all level variants
    icon_lines: List[str] = []
    sprite_id_lines: List[str] = []
    
    facing_map = {"S": "South", "W": "West", "N": "North", "E": "East", "SINGLE": "East"}
    facing_order = ["S", "E", "N", "W", "SINGLE"]
    
    icon_idx = 1
    sprite_idx = 1
    for lvl_idx, (entity_name, entity_def) in enumerate(entity_variants, 1):
        sprite_outputs = entity_def.get("spriteOutputs", {})
        
        # Extract level number from entity name
        level_match = re.search(r'_Lvl_?(\d+)$', entity_name, re.IGNORECASE)
        level_num = level_match.group(1) if level_match else str(lvl_idx)
        
        for facing in facing_order:
            if facing not in sprite_outputs:
                continue
            
            sprites = sprite_outputs[facing]
            if not sprites:
                continue
            
            # Create composite name from all sprites in this direction for the icon
            composite_name = _build_composite_sprite_name(sprites)
            
            suffix = "" if icon_idx == 1 else str(icon_idx)
            icon_lines.append(f"|icon{suffix}={composite_name}.png\n")
            
            direction = facing_map.get(facing)
            if direction:
                icon_lines.append(f"|icon_name{suffix}=Level {level_num} {direction} sprite\n")
            
            # Add each sprite as a separate sprite_id parameter
            for sprite in sprites:
                sprite_suffix = "" if sprite_idx == 1 else str(sprite_idx)
                sprite_id_lines.append(f"|sprite_id{sprite_suffix}={sprite}\n")
                sprite_idx += 1
            
            icon_idx += 1
    
    # Assemble the infobox
    lines = [
        "{{Infobox tile\n",
        f"|name={display_name}\n",
        *icon_lines,
        category_line,
        *skill_lines,
        *sprite_id_lines,
        f"|infobox_version={game_version}\n",
        "}}"
    ]
    
    infobox_text = "".join(lines)
    return infobox_text


def generate_merged_entity_infoboxes(
    grouped_entities: Dict[str, List[tuple]],
    lang_code: str,
    game_version: str
) -> Dict[str, str]:
    """
    Generate merged infobox templates for all base entities.

    Args:
        grouped_entities (Dict[str, List[tuple]]): Dictionary mapping base names to list of (entity_name, entity_def) tuples.
        lang_code (str): Language code for translations.
        game_version (str): Current game version.

    Returns:
        Dict[str, str]: Dictionary mapping base entity names to their merged infobox markup.
    """

    output_directory = os.path.join("output", lang_code, "tiles", "entity_infoboxes")
    os.makedirs(output_directory, exist_ok=True)
    
    infoboxes: Dict[str, str] = {}
    
    for base_name, entity_variants in grouped_entities.items():
        try:
            infobox_text = build_merged_entity_infobox(
                base_name,
                entity_variants,
                lang_code,
                game_version
            )
            infoboxes[base_name] = infobox_text
            
            # Write to file
            filename = base_name.replace(" ", "_") + ".txt"
            output_path = os.path.join(output_directory, filename)
            with open(output_path, "w", encoding="utf-8") as fh:
                fh.write(infobox_text)
        except Exception as exc:
            echo.error(f"Failed to generate merged infobox for base '{base_name}': {exc}")

    return infoboxes


def main(lang_code: str):
    """
    Main execution function for entity infobox generation.

    Args:
        lang_code (str): Language code to process

    This function:
    1. Loads the parsed entity data cache
    2. Generates entity infoboxes
    3. Outputs files to output/{lang_code}/tiles/entity_infoboxes/
    """
    
    ENTITY_CACHE_FILE = "parsed_entity_data.json"
    game_version = Version.get()
    
    entity_path = os.path.join(CACHE_DIR, ENTITY_CACHE_FILE)
    
    try:
        entity_data = load_cache(entity_path, "Entity")
    except Exception as exc:
        echo.error(f"Failed to load entity cache: {exc}")
        echo.error("Make sure the entity cache exists by running the script parser first")
        return
    
    if not entity_data:
        echo.error("Entity data is empty, skipping generation")
        return
    
    echo.info("Generating entity infoboxes")
    entity_infoboxes = generate_entity_infoboxes(
        entity_data, lang_code, game_version
    )

