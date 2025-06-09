#!/usr/bin/env python3
"""
Project Zomboid Wiki CodeSnip Generator

This script generates MediaWiki CodeSnip templates for Project Zomboid tile definitions.
It processes tile data and creates formatted code snippets that can be embedded in wiki
pages, showing the exact tile definitions from the game's source files.

Each tile's definition is formatted as a JSON code block within a CodeSnip template,
which provides syntax highlighting and source attribution on the wiki. The script
generates individual files for each tile definition and maintains a mapping of
all generated snippets.
"""

import os, json
from typing import Dict
from scripts.utils import echo

def generate_codesnips(
    named_tiles_data: Dict[str, Dict[str, dict]],
    lang_code: str,
    game_version: str
) -> Dict[str, str]:
    """
    Generate a CodeSnip wikitext snippet for each tile in every named group,
    write each snippet to its own file, and return a mapping of
    sprite_name -> codesnip wikitext.

    Args:
        named_tiles_data (dict): Tiles organized by group name.
        lang_code (str): Language code (used as folder name).
        game_version (str): Current game version.

    Returns:
        dict: Mapping from sprite_name to its CodeSnip wikitext.
    """
    output_directory = os.path.join("output", lang_code, "tiles", "codesnips")
    os.makedirs(output_directory, exist_ok=True)

    codesnips: Dict[str, str] = {}

    for group_name, tiles in named_tiles_data.items():
        if not isinstance(tiles, dict):
            echo.error(f"Skipping group '{group_name}': expected a dict of tiles")
            continue

        for sprite_name, tile_info in tiles.items():
            if not isinstance(tile_info, dict):
                continue

            lines = [
                "{{CodeSnip",
                "  | lang = json",
                "  | line = false",
                "  | source = NewTileDefinitions.Tiles",
                "  | path = ProjectZomboid\\media",
                "  | retrieved = true",
                f"  | version = {game_version}",
                "  | code =",
            ]

            tile_json = json.dumps({sprite_name: tile_info}, indent=4)
            for json_line in tile_json.splitlines():
                lines.append(f"  {json_line}")
            lines.append("}}")
            codesnip_markup = "\n".join(lines) + "\n"

            codesnips[sprite_name] = codesnip_markup

            filename = f"{sprite_name}.txt"
            filepath = os.path.join(output_directory, filename)
            try:
                with open(filepath, "w", encoding="utf-8") as out:
                    out.write(codesnip_markup)
            except Exception as err:
                echo.error(f"Failed to write CodeSnip for '{sprite_name}' to '{filepath}': {err}")

    return codesnips
