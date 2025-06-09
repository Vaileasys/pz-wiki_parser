#!/usr/bin/env python3
"""
Project Zomboid Wiki Tile Processing Orchestrator

This script orchestrates the complete tile processing pipeline for the Project Zomboid Wiki.
It manages cache generation, data parsing, and the generation of various wiki components
including infoboxes, code snippets, scrapping tables, and complete articles.

The script handles:
- Cache management and validation
- Data parsing from game files
- Generation of wiki components
- Article assembly and organization
- List generation for furniture and crafting surfaces
"""

import os

from scripts.core.cache import load_cache
from scripts.core.constants import DATA_DIR
from scripts.core.version import Version
from scripts.core.language import Language
from scripts.utils import echo

# parsers
from scripts.parser.tiles_parser import main as parse_tiles
from scripts.parser.movable_definitions_parser import main as parse_movable_definitions
from scripts.tiles.named_furniture_filter import main as parse_named_furniture

# generators
from scripts.tiles.tiles_infobox import generate_infoboxes
from scripts.tiles.tiles_codesnip import generate_codesnips
from scripts.tiles.tiles_scrapping import generate_scrapping_tables
from scripts.tiles.tiles_article import generate_tile_articles
from scripts.lists.furniture_list import generate_furniture_lists
from scripts.lists.furniture_surfaces_list import generate_surface_list

TILE_CACHE_FILE = "tiles_data.json"
NAMED_FURNITURE_CACHE_FILE = "named_furniture.json"
MOVABLE_DEFINITIONS_CACHE_FILE = "movable_definitions.json"


def generate_cache(cache_path: str, cache_label: str, parser_func, game_version: str):
    """
    Generate or load a cache file for tile data.

    Args:
        cache_path (str): Path to the cache file.
        cache_label (str): Human-readable label for the cache type.
        parser_func (callable): Function to parse data if cache needs regeneration.
        game_version (str): Current game version for cache validation.

    Returns:
        tuple: (cache_data, cache_version) where:
            - cache_data: The loaded data or None if loading failed
            - cache_version: Version string of the cache or None if loading failed
    """
    try:
        data, cache_version = load_cache(cache_path, cache_label, get_version=True)
        if cache_version != game_version:
            echo.info(f"Generating {cache_label.lower()} cache")
            parser_func()
            data, cache_version = load_cache(cache_path, cache_label, get_version=True)
        echo.info(f"{cache_label} cache loaded")
        return data, cache_version
    except Exception as exc:
        echo.error(f"Error loading {cache_label.lower()} cache: {exc}")
        return None, None


def main():
    """
    Main execution function for the tile processing pipeline.

    This function:
    1. Ensures all necessary caches are present and up-to-date
    2. Loads or generates required data from game files
    3. Generates various wiki components:
       - Infoboxes for tile properties
       - CodeSnips showing tile definitions
       - Scrapping tables for dismantling info
       - Complete wiki articles
       - Furniture and crafting surface lists
    4. Provides progress feedback through echo messages
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    game_version = Version.get()
    lang_code    = Language.get()

    tile_path   = os.path.join(DATA_DIR, TILE_CACHE_FILE)
    named_path  = os.path.join(DATA_DIR, NAMED_FURNITURE_CACHE_FILE)
    defs_path   = os.path.join(DATA_DIR, MOVABLE_DEFINITIONS_CACHE_FILE)

    tiles_data, _        = generate_cache(tile_path,   "Tiles",               parse_tiles,               game_version)
    named_tiles_data, _  = generate_cache(named_path,  "Named Tiles",         parse_named_furniture,     game_version)
    movable_defs_data, _ = generate_cache(defs_path,   "Movable Definitions", parse_movable_definitions, game_version)

    if tiles_data is None or named_tiles_data is None or movable_defs_data is None:
        echo.error("One or more caches failed to load.")
        return

    echo.success("All caches loaded")

    echo.info("Generating infoboxes")
    infoboxes = generate_infoboxes(named_tiles_data, movable_defs_data, lang_code, game_version)
    echo.success("Infoboxes generated")

    echo.info("Generating CodeSnips")
    codesnips = generate_codesnips(named_tiles_data, lang_code, game_version)
    echo.success("CodeSnips generated")

    echo.info("Generating Scrapping tables")
    scrapping = generate_scrapping_tables(
        tiles=      named_tiles_data,
        definitions=movable_defs_data,
        lang_code=  lang_code
    )
    echo.success("Scrapping tables generated")

    echo.info("Assembling tile articles")
    generate_tile_articles(named_tiles_data, infoboxes, codesnips, scrapping)
    echo.success("Tile articles assembled")

    echo.info("Generating furniture lists")
    generate_furniture_lists(named_tiles_data)
    echo.success("Furniture lists generated")

    echo.info("Generating crafting surfaces list")
    generate_surface_list(named_tiles_data)
    echo.success("Crafting surfaces list generated")

if __name__ == "__main__":
    main()