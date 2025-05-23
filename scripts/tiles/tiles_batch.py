import os

from scripts.core.cache import load_cache
from scripts.core.constants import DATA_DIR
from scripts.core.version import Version
from scripts.core.language import Language
from scripts.utils.echo import echo_info, echo_error, echo_success

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

"""
This script handles the cache generation an the in order running of tiles scripts
"""


def generate_cache(cache_path: str, cache_label: str, parser_func, game_version: str):
    try:
        data, cache_version = load_cache(cache_path, cache_label, get_version=True)
        if cache_version != game_version:
            echo_info(f"Generating {cache_label.lower()} cache")
            parser_func()
            data, cache_version = load_cache(cache_path, cache_label, get_version=True)
        echo_info(f"{cache_label} cache loaded")
        return data, cache_version
    except Exception as exc:
        echo_error(f"Error loading {cache_label.lower()} cache: {exc}")
        return None, None

def main():
    """Ensure caches are fresh, generate all components, and assemble articles."""
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
        echo_error("One or more caches failed to load.")
        return

    echo_success("All caches loaded")

    echo_info("Generating infoboxes")
    infoboxes = generate_infoboxes(named_tiles_data, movable_defs_data, lang_code, game_version)
    echo_success("Infoboxes generated")

    echo_info("Generating CodeSnips")
    codesnips = generate_codesnips(named_tiles_data, lang_code, game_version)
    echo_success("CodeSnips generated")

    echo_info("Generating Scrapping tables")
    scrapping = generate_scrapping_tables(
        tiles=      named_tiles_data,
        definitions=movable_defs_data,
        lang_code=  lang_code
    )
    echo_success("Scrapping tables generated")

    echo_info("Assembling tile articles")
    generate_tile_articles(named_tiles_data, infoboxes, codesnips, scrapping)
    echo_success("Tile articles assembled")

    echo_info("Generating furniture lists")
    generate_furniture_lists(named_tiles_data)
    echo_success("Furniture lists generated")

    echo_info("Generating crafting surfaces list")
    generate_surface_list(named_tiles_data)
    echo_success("Crafting surfaces list generated")

if __name__ == "__main__":
    main()