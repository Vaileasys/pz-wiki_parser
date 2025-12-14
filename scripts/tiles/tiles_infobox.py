"""
Project Zomboid Wiki Infobox Generator

This script generates MediaWiki infobox templates for Project Zomboid tiles. It processes
tile definitions and properties to create structured information boxes that appear at
the top of wiki articles, containing key information about each tile type.

The script handles:
- Display names and translations
- Tile properties and statistics
- Tool requirements and skill levels
- Container capacities and special features
- Multi-tile object composition
- Image and sprite references
"""

import os
from typing import Dict, List, Tuple
from scripts.core.language import Translate
from scripts.utils import echo

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

_PERK_TO_SKILL = {
    'Perks.Woodwork': '{{ll|Carpentry}}',
    'Perks.Electricity': '{{ll|Electrical}}',
    'Perks.Farming': '{{ll|Farming}}',
    'Perks.MetalWelding': '{{ll|Welding}}',
    'Perks.Strength': '{{ll|Strength}}',
    'Perks.MAX': 'Unknown',
}

_BED_QUALITY_MAP = {
    "badBed": "Bad",
    "averageBed": "Average",
    "goodBed": "Good",
}


def _parse_grid(pos: str) -> Tuple[int, int]:
    """
    Parse a grid position string into column and row coordinates.

    Args:
        pos (str): Position string in format "row,column"

    Returns:
        tuple[int, int]: A tuple of (column, row) coordinates.
        Returns (0, 0) if parsing fails.
    """
    try:
        row, col = map(int, pos.split(","))
        return col, row
    except Exception:
        return 0, 0


def _build_output_name(sprite_ids: List[str]) -> str:
    """
    Generate a composite name from multiple sprite IDs.

    Args:
        sprite_ids (List[str]): List of sprite identifiers.

    Returns:
        str: Combined name where the first ID is the base and subsequent
             ones are appended as suffixes, joined with '+'.
    """
    first = sprite_ids[0]
    extras = [sid.rsplit("_", 1)[-1] for sid in sprite_ids[1:]]
    return "+".join([first, *extras])


def _get_composite_names(tile_list: List[dict]) -> List[Tuple[str, str]]:
    """
    Generate composite names for multi-tile objects based on facing direction.

    Args:
        tile_list (List[dict]): List of tile entries with sprite and facing information.

    Returns:
        List[Tuple[str, str]]: List of tuples containing (facing_direction, composite_name).
    """
    composite: List[Tuple[str, str]] = []
    for facing in ["S", "E", "N", "W"]:
        entries = [t for t in tile_list if t["facing"] == facing]
        if len(entries) < 2:
            continue
        entries.sort(key=lambda e: (e["grid"][1], e["grid"][0]))
        sprite_ids = [e["sprite_id"] for e in entries]
        name = _build_output_name(sprite_ids)
        composite.append((facing, name))
    return composite


def extract_tile_stats(
    tiles: Dict[str, dict],
    definitions: Dict[str, dict],
    lang_code: str
) -> Tuple[float, int, str, str, str, str]:
    """
    Extract key statistics and requirements for a tile group.

    Args:
        tiles (Dict[str, dict]): Dictionary of tile definitions.
        definitions (Dict[str, dict]): Dictionary of game definitions.
        lang_code (str): Language code for translations.

    Returns:
        Tuple[float, int, str, str, str, str]: Tuple containing:
            - encumbrance: Weight/encumbrance value
            - max_size: Maximum size of the tile group
            - pickup_skill: Required skill for pickup
            - pickup_tool: Required tool for pickup
            - dis_skill: Required skill for disassembly
            - dis_tool: Required tool for disassembly
    """
    tile_list, facing_counts = prepare_tile_list(tiles)
    max_size = max(facing_counts.values(), default=1) or 1

    raw_weight = tile_list[0].get("weight") if tile_list else None
    encumbrance = (int(raw_weight) / 10) if raw_weight is not None else "N/A"

    misc_lines = build_misc_params(tile_list, definitions, lang_code)

    pickup_skill = next(
        (l.split("=",1)[1].strip() for l in misc_lines if l.startswith("|pickup_skill=")),
        "[[File:UI Cross.png|link=|No skill required]]"
    )
    pickup_tool = next(
        (l.split("=",1)[1].strip() for l in misc_lines if l.startswith("|pickup_tool=")),
        "[[File:UI Cross.png|link=|No tool required]]"
    )
    if pickup_tool == "None":
        pickup_tool = "[[File:UI Cross.png|link=|No tool required]]"

    dis_skill = next(
        (l.split("=",1)[1].strip() for l in misc_lines if l.startswith("|disassemble_skill=")),
        "[[File:UI Cross.png|link=|No skill required]]"
    )
    dis_tool = next(
        (l.split("=",1)[1].strip() for l in misc_lines if l.startswith("|disassemble_tool=")),
        "[[File:UI Cross.png|link=|No tool required]]"
    )

    return encumbrance, max_size, pickup_skill, pickup_tool, dis_skill, dis_tool


def generate_infoboxes(
    named_tiles_data: Dict[str, Dict],
    definitions: Dict[str, Dict],
    lang_code: str,
    game_version: str
) -> Dict[str, str]:
    """
    Generate infobox templates for all tile groups.

    Args:
        named_tiles_data (Dict[str, Dict]): Dictionary of tile groups and their definitions.
        definitions (Dict[str, Dict]): Dictionary of game definitions.
        lang_code (str): Language code for translations.
        game_version (str): Current game version.

    Returns:
        Dict[str, str]: Dictionary mapping tile group names to their infobox markup.
    """
    output_directory = os.path.join("output", lang_code, "tiles", "infoboxes")
    os.makedirs(output_directory, exist_ok=True)

    infoboxes: Dict[str, str] = {}
    for group_name, tile_entries in named_tiles_data.items():
        if not isinstance(tile_entries, dict):
            echo.error(f"Skipping group '{group_name}': expected a dict of tiles")
            continue

        first_tile_info = next(iter(tile_entries.values()))
        generic = first_tile_info.get("properties", {}).get("generic", {})
        custom_name = generic.get("CustomName", "")
        group_key = generic.get("GroupName", "")

        candidate_keys = [
            f"{custom_name}{group_key}".replace(" ", ""),
            f"{group_key}{custom_name}".replace(" ", ""),
        ]
        for cand in candidate_keys:
            lookup = f"Base.Mov_{cand}"
            trans = Translate.get(lookup, "DisplayName")
            if trans != lookup:
                display_name = trans.strip()
                break
        else:
            display_name = f"{group_key} {custom_name}".strip()

        infobox_text = build_infobox(
            display_name,
            tile_entries,
            definitions,
            lang_code,
            game_version
        )
        infoboxes[group_name] = infobox_text

        filename = group_name.replace(" ", "_") + ".txt"
        output_path = os.path.join(output_directory, filename)
        try:
            with open(output_path, "w", encoding="utf-8") as fh:
                fh.write(infobox_text)
        except Exception as exc:
            echo.error(f"Failed to write infobox for '{group_name}' to '{output_path}': {exc}")

    return infoboxes


def build_infobox(
    display_name: str,
    tiles: Dict[str, dict],
    definitions: Dict[str, dict],
    lang_code: str,
    game_version: str
) -> str:
    """
    Build a complete infobox template for a tile group.

    Args:
        display_name (str): Display name of the tile group.
        tiles (Dict[str, dict]): Dictionary of tile definitions.
        definitions (Dict[str, dict]): Dictionary of game definitions.
        lang_code (str): Language code for translations.
        game_version (str): Current game version.

    Returns:
        str: Complete MediaWiki infobox template markup.
    """
    tile_list, facing_counts = prepare_tile_list(tiles)
    max_size = max(facing_counts.values(), default=1) or 1

    icon_lines = build_icon_params(tile_list, max_size)
    sprite_id_lines, tile_id_lines = build_sprite_tile_params(tile_list)
    misc_lines = build_misc_params(tile_list, definitions, lang_code)

    weight_line = misc_lines[0]
    remaining_misc = misc_lines[1:]

    lines = [
        "{{Infobox tile\n",
        f"|name={display_name}\n",
        *icon_lines,
        "|category=Furniture\n",
        weight_line,
        f"|size={max_size}\n",
        *remaining_misc,
        *tile_id_lines,
        *sprite_id_lines,
        f"|infobox_version={game_version}\n",
        "}}"
    ]
    return "".join(lines)


def prepare_tile_list(tiles: Dict[str, dict]) -> Tuple[List[dict], Dict[str, int]]:
    """
    Process tile definitions into a structured list and count facings.

    Args:
        tiles (Dict[str, dict]): Dictionary of tile definitions.

    Returns:
        Tuple[List[dict], Dict[str, int]]: Tuple containing:
            - List of processed tile entries with extracted properties
            - Dictionary counting tiles for each facing direction
    """
    tile_list: List[dict] = []
    facing_counts = {"E": 0, "S": 0, "W": 0, "N": 0}

    for tile_info in tiles.values():
        generic = tile_info.get("properties", {}).get("generic", {})
        entry = {
            "icon_value":        tile_info.get("sprite", ""),
            "sprite_id":         tile_info.get("sprite", ""),
            "tile_id":           tile_info.get("id", ""),
            "facing":            generic.get("Facing", ""),
            "weight":            generic.get("PickUpWeight"),
            "pickup_tool":       generic.get("PickUpTool"),
            "place_tool":        generic.get("PlaceTool"),
            "bed_type":          generic.get("BedType"),
            "pickup_level":      generic.get("PickUpLevel"),
            "is_table_top":      "IsTableTop" in generic,
            "is_low":            "IsLow" in generic,
            "capacity":          generic.get("ContainerCapacity"),
            "liquid_capacity":   generic.get("waterMaxAmount"),
            "freezer_capacity":  generic.get("FreezerCapacity"),
            "custom_item":       generic.get("CustomItem"),
            "material":          generic.get("Material"),
            "iso_type":          generic.get("IsoType"),
            "container":         generic.get("container"),
            "can_scrap":         "CanScrap" in generic,
            "crafting_surface":  generic.get("GenericCraftingSurface"),
            "move_type":         generic.get("MoveType"),
            "min_car_speed":     generic.get("MinimumCarSpeedDmg"),
            "can_break":         "CanBreak" in generic,
            "is_trash_can":      "IsTrashCan" in generic,
            "is_water_collector":"IsWaterCollector" in generic,
            "is_stackable":      "IsStackable" in generic,
            "stop_car":          "StopCar" in generic,
            "is_tv":             "TV" in generic,
            "light_r":           generic.get("lightR"),
            "light_g":           generic.get("lightG"),
            "light_b":           generic.get("lightB"),
            "grid":              _parse_grid(generic.get("SpriteGridPos", "0,0")),
        }
        tile_list.append(entry)
        facing_counts[entry["facing"]] = facing_counts.get(entry["facing"], 0) + 1

    return tile_list, facing_counts


def build_icon_params(tile_list: List[dict], max_size: int) -> List[str]:
    """
    Generate icon parameters for the infobox template.

    Args:
        tile_list (List[dict]): List of processed tile entries.
        max_size (int): Maximum size of the tile group.

    Returns:
        List[str]: List of icon parameter lines for the infobox template.
    """
    facing_map = {"S": "South", "W": "West", "N": "North", "E": "East"}
    sprite_label = "sprite"
    icon_lines: List[str] = []

    if max_size > 1:
        composite = _get_composite_names(tile_list)
        for idx, (facing, name) in enumerate(composite, start=1):
            suffix = "" if idx == 1 else str(idx)
            icon_lines.append(f"|icon{suffix}={name}.png\n")
            dir_label = facing_map.get(facing)
            if dir_label:
                icon_lines.append(f"|icon_name{suffix}={dir_label} {sprite_label}\n")
        return icon_lines

    for index, tile_entry in enumerate(tile_list, start=1):
        suffix = "" if index == 1 else str(index)
        icon_lines.append(f"|icon{suffix}={tile_entry['icon_value']}.png\n")
        direction = facing_map.get(tile_entry["facing"])
        if direction:
            icon_lines.append(f"|icon_name{suffix}={direction} {sprite_label}\n")

    return icon_lines


def build_sprite_tile_params(tile_list: List[dict]) -> Tuple[List[str], List[str]]:
    sprite_id_lines: List[str] = []
    tile_id_lines: List[str] = []

    for idx, tile_entry in enumerate(tile_list, start=1):
        suffix = "" if idx == 1 else str(idx)
        tile_id_lines.append(f"|tile_id{suffix}={tile_entry['tile_id']}\n")

    composite = _get_composite_names(tile_list)
    if composite:
        for idx, (_, name) in enumerate(composite, start=1):
            suffix = "" if idx == 1 else str(idx)
            sprite_id_lines.append(f"|sprite_id{suffix}={name}\n")
    else:
        for idx, tile_entry in enumerate(tile_list, start=1):
            suffix = "" if idx == 1 else str(idx)
            sprite_id_lines.append(f"|sprite_id{suffix}={tile_entry['sprite_id']}\n")

    return sprite_id_lines, tile_id_lines


def build_misc_params(tile_list: List[dict], definitions: Dict[str, dict], lang_code: str) -> List[str]:
    weight_values: List[float] = []
    bed_type_values: List[str] = []
    is_low_flags: List[str] = []
    iso_line = container_line = table_line = ""
    capacity_line = freezer_line = liquid_line = ""
    crafting_surface_line = move_type_line = min_car_speed_line = ""
    canbreak_line = trash_can_line = water_collector_line = ""
    stackable_line = stop_car_line = tv_line = ""
    light_color_line = ""
    pickup_tool_line = ""
    place_tool_line = ""
    pickup_level_line = ""
    pickup_skill_line = ""
    disassemble_skill_line = ""
    disassemble_tool_lines: List[str] = []

    added_flags = {
        "iso": False, "container": False,
        "capacity": False, "freezer": False,
        "pickup": False, "place": False,
        "crafting_surface": False,
        "move_type": False,
        "min_car_speed": False,
        "canbreak": False,
        "trash_can": False,
        "water_collector": False,
        "stackable": False,
        "stop_car": False,
        "tv": False,
        "light_color": False,
        "table": False,
    }

    true_value = "True"
    tag_value = "tag"

    for tile_entry in tile_list:
        raw_weight = tile_entry["weight"]
        weight_values.append(int(raw_weight) / 10 if raw_weight is not None else "-")

        bed_key = tile_entry["bed_type"]
        if bed_key is not None:
            quality = _BED_QUALITY_MAP.get(bed_key, bed_key)
            bed_type_values.append(quality)

        if tile_entry["is_low"]:
            is_low_flags.append(true_value)

        if not added_flags["iso"] and tile_entry.get("iso_type"):
            iso_line = f"|type={tile_entry['iso_type']}\n"
            added_flags["iso"] = True

        if not added_flags["container"] and tile_entry.get("container"):
            container_line = f"|container={tile_entry['container']}\n"
            added_flags["container"] = True

        cap = tile_entry["capacity"]
        if cap and not added_flags["capacity"]:
            capacity_line = f"|capacity={cap}\n"
            added_flags["capacity"] = True
        fr = tile_entry["freezer_capacity"]
        if fr and not added_flags["freezer"]:
            freezer_line = f"|freezer_capacity={fr}\n"
            added_flags["freezer"] = True
        liq = tile_entry["liquid_capacity"]
        if liq:
            liquid_line = f"|liquid_capacity={liq}\n"

        cs = tile_entry["crafting_surface"]
        if cs is not None and not added_flags["crafting_surface"]:
            crafting_surface_line = f"|is_crafting_surface={cs}\n"
            added_flags["crafting_surface"] = True

        mt = tile_entry["move_type"]
        if mt and not added_flags["move_type"]:
            move_type_line = f"|move_type={mt}\n"
            added_flags["move_type"] = True

        mcs = tile_entry["min_car_speed"]
        if mcs is not None and not added_flags["min_car_speed"]:
            min_car_speed_line = f"|min_car_speed={mcs}\n"
            added_flags["min_car_speed"] = True

        if tile_entry["can_break"] and not added_flags["canbreak"]:
            canbreak_line = "|canbreak=True\n"
            added_flags["canbreak"] = True
        if tile_entry["is_trash_can"] and not added_flags["trash_can"]:
            trash_can_line = "|trash_can=True\n"
            added_flags["trash_can"] = True
        if tile_entry["is_water_collector"] and not added_flags["water_collector"]:
            water_collector_line = "|is_water_collector=True\n"
            added_flags["water_collector"] = True
        if tile_entry["is_stackable"] and not added_flags["stackable"]:
            stackable_line = "|is_stackable=True\n"
            added_flags["stackable"] = True
        if tile_entry["stop_car"] and not added_flags["stop_car"]:
            stop_car_line = "|stop_car=True\n"
            added_flags["stop_car"] = True
        if tile_entry["is_tv"] and not added_flags["tv"]:
            tv_line = "|is_tv=True\n"
            added_flags["tv"] = True

        lr = tile_entry["light_r"]
        lg = tile_entry["light_g"]
        lb = tile_entry["light_b"]
        if not added_flags["light_color"] and lr is not None and lg is not None and lb is not None:
            light_color_line = f"|light_color={{{{Rgb|{lr}, {lg}, {lb}}}}}\n"
            added_flags["light_color"] = True

        if tile_entry["is_table_top"] and not added_flags["table"]:
            table_line = "|is_table_top=True\n"
            added_flags["table"] = True

        pt = tile_entry["pickup_tool"]
        if pt and not added_flags["pickup"]:
            tt = _TOOL_TYPE_MAP.get(pt)
            if tt == "tool":
                pickup_tool_line = f"|pickup_tool={{{{ll|{_TOOL_VALUE_MAP[pt]}}}}}\n"
            else:
                if _TOOL_VALUE_MAP[pt] == "Cutter":
                    tag_links = []
                    for cutter_item in ("SharpKnife", "Scissors"):
                        link = (f"Item tag/{lang_code}#tag-{cutter_item}"
                                if lang_code.lower() != "en"
                                else f"Item tag#tag-{cutter_item}")
                        tag_links.append(f"[[{link}|{cutter_item} ({tag_value})]]")
                    extras = ["{{ll|Kitchen Knife}}", "{{ll|Scissors}}", "{{ll|Hunting Knife}}", "{{ll|Chipped Stone}}"]
                    pickup_tool_line = "|pickup_tool=" + "<br>".join(tag_links + extras) + "\n"
                else:
                    link = (f"Item tag/{lang_code}#tag-{_TOOL_VALUE_MAP[pt]}"
                            if lang_code.lower() != "en"
                            else f"Item tag#tag-{_TOOL_VALUE_MAP[pt]}")
                    pickup_tool_line = f"|pickup_tool=[[{link}|{_TOOL_VALUE_MAP[pt]} ({tag_value})]]\n"
            added_flags["pickup"] = True
            skill_val = _TOOL_SKILL_MAP.get(pt, "None")
            if skill_val != "None":
                pickup_skill_line = f"|pickup_skill={skill_val}\n"

        lvl = tile_entry["pickup_level"]
        if lvl and not pickup_level_line:
            pickup_level_line = f"|pickup_level={lvl}\n"

        pl = tile_entry["place_tool"]
        if pl and not added_flags["place"]:
            tt = _TOOL_TYPE_MAP.get(pl)
            if tt == "tool":
                place_tool_line = f"|place_tool={{{{ll|{_TOOL_VALUE_MAP[pl]}}}}}\n"
            else:
                if _TOOL_VALUE_MAP[pl] == "Cutter":
                    tag_links = []
                    for cutter_item in ("SharpKnife", "Scissors"):
                        link = (f"Item tag/{lang_code}#tag-{cutter_item}"
                                if lang_code.lower() != "en"
                                else f"Item tag#tag-{cutter_item}")
                        tag_links.append(f"[[{link}|{cutter_item} ({tag_value})]]")
                    place_tool_line = "|place_tool=" + "<br>".join(tag_links) + "\n"
                else:
                    link = (f"Item tag/{lang_code}#tag-{_TOOL_VALUE_MAP[pl]}"
                            if lang_code.lower() != "en"
                            else f"Item tag#tag-{_TOOL_VALUE_MAP[pl]}")
                    place_tool_line = f"|place_tool=[[{link}|{_TOOL_VALUE_MAP[pl]} ({tag_value})]]\n"
            added_flags["place"] = True

    if not pickup_tool_line and any(w != "-" for w in weight_values):
        pickup_tool_line = "|pickup_tool=None\n"
        pickup_level_line = ""

    first_tile = tile_list[0]
    material_value = first_tile.get("material")
    if first_tile.get("can_scrap") and material_value:
        scrap_def = definitions.get("scrap_definitions", {}).get(material_value, {})
        perk_key = scrap_def.get("perk")
        if perk_key:
            skill_name = _PERK_TO_SKILL.get(perk_key, "Unknown")
            disassemble_skill_line = f"|disassemble_skill={skill_name}\n"
        scrap_tools = scrap_def.get("tools", []) + scrap_def.get("tools2", [])
        idx = 1
        for scrap_tool in scrap_tools:
            if scrap_tool.startswith("Base."):
                item_class = scrap_tool
                display_name = f"{{{{ll|{Translate.get(item_class, 'DisplayName')}}}}}"
            elif scrap_tool.startswith("Tag."):
                tag_name = scrap_tool[4:]
                link = (f"Item tag/{lang_code}#tag-{tag_name}"
                        if lang_code.lower() != "en"
                        else f"Item tag#tag-{tag_name}")
                display_name = f"[[{link}|{tag_name} ({tag_value})]]"
            else:
                display_name = f"{{{{ll|{Translate.get(scrap_tool, 'DisplayName')}}}}}"
            suffix = "" if idx == 1 else str(idx)
            disassemble_tool_lines.append(f"|disassemble_tool{suffix}={display_name}\n")
            idx += 1

    custom_item = first_tile.get("custom_item")
    if custom_item:
        item_id_line = f"|item_id={custom_item}\n"
    else:
        item_id_line = "|item_id=Moveables.{sprite_id}\n"

    valid_w = [w for w in weight_values if w != "-"]
    if len(set(valid_w)) == 1 and valid_w:
        weight_line = f"|weight={valid_w[0]:.1f}\n"
    else:
        weight_line = "|weight=-\n"

    if len(set(bed_type_values)) == 1 and bed_type_values:
        bed_line = f"|bed_type={bed_type_values[0]}\n"
    else:
        bed_line = ""

    if len(set(is_low_flags)) == 1 and is_low_flags:
        low_line = f"|is_low={true_value}\n"
    else:
        low_line = ""

    return [
        weight_line,
        bed_line,
        low_line,
        iso_line,
        container_line,
        capacity_line,
        freezer_line,
        liquid_line,
        crafting_surface_line,
        move_type_line,
        min_car_speed_line,
        canbreak_line,
        trash_can_line,
        water_collector_line,
        stackable_line,
        stop_car_line,
        tv_line,
        light_color_line,
        table_line,
        pickup_skill_line,
        pickup_level_line,
        pickup_tool_line,
        place_tool_line,
        disassemble_skill_line,
        *disassemble_tool_lines,
        item_id_line,
    ]
