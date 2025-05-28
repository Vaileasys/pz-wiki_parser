# Manages accessing and processing the data in the page dictionary.

import os
from scripts.core.cache import load_json, save_cache
from scripts.core.constants import RESOURCE_DIR
from scripts.utils.echo import echo_warning

PAGE_DICT_FILE = "page_dictionary.json"
FILE_PATH = os.path.join(RESOURCE_DIR, PAGE_DICT_FILE)
CACHE_FILE = "page_data_by_id.json"

_raw_data = None
_flat_page_data = {}
_id_data = {}


def get_ids(page, id_type: str = "item_id") -> list[str]:
    """
    Returns a list of ids for a given page and id_type.

    Args:
        page (str): Page name.
        id_type (str): The id type key (default: 'item_id').

    Returns:
        list[str] or None: List of ids if found.
    """
    return get_flattened_page_dict().get(page, {}).get(id_type)


def get_pages(query_id: str, id_type: str = None) -> list[str]:
    """
    Returns a list of pages for a given id.

    Args:
        query_id (str): The id to search for.
        id_type (str, optional): Restrict search to this id type. Defaults to searching all.

    Returns:
        list[str] or None: List of pages if found, else None.
    """
    id_data = get_id_data()
    if id_type is None:
        for key, value in id_data.items():
            if query_id in value:
                return value[query_id]
        echo_warning(f"Unable to find page for '{query_id}'.")
        return None

    if id_type in id_data:
        return id_data[id_type].get(query_id)
    else:
        echo_warning(f"Unable to find page for '{query_id}' in '{id_type}'.")
        return None


def get_categories(page):
    """
    Returns the list of categories for the given page.

    Args:
        page (str): Wiki page name.

    Returns:
        list: Category names if found, else an empty list.
    """
    return get_flattened_page_dict().get(page, {}).get("categories", [])


def get_id_categories(script_id, id_type="item_id"):
    """
    Returns the list of categories for the given script_id.

    Args:
        script_id (str): Full ID like 'Base.Axe'.
        id_type (str): Key name to look up IDs (default: 'item_id').

    Returns:
        list: Category names if found, else an empty list.
    """
    pages = get_pages(script_id, id_type=id_type)
    if pages:
        page = pages[0]
        return get_categories(page)
    echo_warning(f"Unable to find categories for '{script_id}'.")
    return []


def get_id_data():
    """Returns the page dictionary organised with the id as the key."""
    global _id_data
    if not _id_data:
        _restructure_id_data()
    return _id_data


def get_flattened_page_dict():
    """Returns the flattened page dictionary, removing first-level keys (item, tile, vehicle)."""
    global _flat_page_data
    if not _flat_page_data:
        _flatten_page_dict()
    return _flat_page_data


def get_raw_page_dict():
    """Returns the raw page dictionary data."""
    load()
    return _raw_data


def _flatten_page_dict():
    """Flattens the page dictionary into a single-level dict."""
    global _flat_page_data
    _flat_page_data = {}
    for group in get_raw_page_dict().values():
        if isinstance(group, dict):
            _flat_page_data.update(group)


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


def load(filepath=FILE_PATH):
    """Load the page dictionary data from file if not already loaded."""
    global _raw_data
    if _raw_data is None:
        _raw_data = load_json(filepath)


def init() -> None:
    """Initialise all data, storing in cache."""
    load()
    get_flattened_page_dict()
    get_id_data()