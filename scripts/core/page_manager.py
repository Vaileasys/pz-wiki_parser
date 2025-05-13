# Manages accessing and processing the data in the page dictionary.

import os
from scripts.core.cache import load_json, save_cache
from scripts.core.constants import RESOURCE_DIR
from scripts.utils.echo import echo_warning

PAGE_DICT_FILE = "page_dictionary.json"
FILE_PATH = os.path.join(RESOURCE_DIR, PAGE_DICT_FILE)
CACHE_FILE = "page_data_by_id.json"

_raw_data = {}
_flat_page_data = {}
_id_data = {}


def get_ids_from_page(page, id_type: str = "item_id") -> list[str]:
    """Returns a list of ids for a given page and id_type."""
    return get_flattened_page_dict().get(page).get(id_type)


def get_page_from_id(query_id: str, id_type: str = None) -> str:
    """Returns a page for a given id. Option to provide the 'id_type' to search only in that id type."""
    if id_type is None:
        for key, value in get_id_data().items():
            if query_id in value:
                return value[query_id][0]
        echo_warning(f"Unable to find page for '{query_id}'.")
        return None
    
    if id_type in get_id_data():
        return get_id_data()[id_type][query_id]
    else:
        echo_warning(f"Unable to find page for '{query_id}' in '{id_type}'.")
        return None


def get_id_data() -> dict[list]:
    """Returns the page dictionary organised with the id as the key."""
    if not _id_data:
        _restructure_id_data()
    return _id_data


def _restructure_id_data() -> None:
    """Restructures the flattened page dict so the key is the id, and page is the value."""
    global _id_data
    _id_data = {}

    for page, data in get_flattened_page_dict().items():
        for key, values in data.items():
            # Skip values that aren't lists
            if not isinstance(values, list):
                continue

            if key not in _id_data:
                _id_data[key] = {}

            for value in values:
                _id_data[key].setdefault(value, []).append(page)

    save_cache(_id_data, CACHE_FILE, suppress=True)


def get_flattened_page_dict() -> dict:
    """Returns the flattened page dictionary data."""
    if not _flat_page_data:
        _flatten_page_dict()
    return _flat_page_data


def _flatten_page_dict() -> None:
    """Flattens the page dictionary, removing the first level keys (item, tile, vehicle)"""
    global _flat_page_data
    _flat_page_data = {}
    for group in get_raw_page_dict().values():
        if isinstance(group, dict):
            _flat_page_data.update(group)


def get_raw_page_dict() -> dict:
    """Returns the raw page dictionary data."""
    if not _raw_data:
        _update_page_dict()
    return _raw_data


def _update_page_dict() -> None:
    """Updates the raw page dictionary date."""
    global _raw_data
    _raw_data = load_json(FILE_PATH)


def init() -> None:
    """Initialise all data, storing in cache."""
    get_raw_page_dict()
    get_flattened_page_dict()
    get_id_data()