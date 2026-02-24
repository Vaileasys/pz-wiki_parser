"""
Project Zomboid Wiki Meta Recipe Parser

This script identifies and processes meta recipes from Project Zomboid's craft recipe data.
Meta recipes allow multiple recipes to be learned by just knowing one recipe name.

The script:
- Loads craft recipe data from cache
- Identifies recipes with the 'MetaRecipe' key
- Groups recipes by their meta recipe identifier
- Provides a way to expand meta recipe names to all associated recipes
- Saves the meta recipe mapping to cache for use by other scripts
"""

import os
import json
from scripts.core.version import Version
from scripts.core.constants import DATA_DIR
from scripts.core.cache import save_cache, load_cache
from scripts.utils import echo

# Cache file name
CACHE_JSON = "metarecipe_data.json"

# Global dictionary to store the parsed meta recipe data
metarecipe_data = {}

def get_metarecipe_data():
    """
    Returns the parsed meta recipe data.

    Returns:
        dict: A dictionary mapping meta recipe names to lists of recipe names.
    """
    global metarecipe_data
    if not metarecipe_data:
        main()
    return metarecipe_data


def build_metarecipe_mapping(craft_data):
    """
    Builds a mapping of meta recipes to their associated recipes.
    
    Args:
        craft_data (dict): Dictionary of craft recipes.
        
    Returns:
        dict: Dictionary mapping meta recipe names to lists of recipe names.
    """
    meta_recipes = {}
    
    for recipe_name, recipe_data in craft_data.items():
        # Check if recipe has the MetaRecipe key
        meta_recipe_name = recipe_data.get("MetaRecipe")
        if meta_recipe_name:
            # Add the recipe to the meta recipe mapping
            if meta_recipe_name not in meta_recipes:
                meta_recipes[meta_recipe_name] = []
            
            # Add this recipe to the meta recipe's list
            meta_recipes[meta_recipe_name].append(recipe_name)
    
    return meta_recipes


def expand_recipe_list(recipe_list):
    """
    Expands a list of recipe names, replacing meta recipes with their associated recipes.
    
    Args:
        recipe_list (list or str): A list of recipe names or a single recipe name.
        
    Returns:
        list: An expanded list of recipe names with meta recipes replaced by their components.
    """
    if not recipe_list:
        return []
        
    # Ensure recipe_list is a list
    if not isinstance(recipe_list, list):
        recipe_list = [recipe_list]
    
    # Expand the list by replacing meta recipes
    expanded_list = []
    for recipe_name in recipe_list:
        if recipe_name in metarecipe_data:
            # Add all recipes associated with this meta recipe
            expanded_list.extend(metarecipe_data[recipe_name])
        else:
            # Add the original recipe name
            expanded_list.append(recipe_name)
    
    return expanded_list


def main():
    """
    Initializes the meta recipe data.
    
    This function:
    1. Checks for existing cache
    2. If needed, parses craft recipe data to extract meta recipes
    3. Builds a mapping of meta recipes to their associated recipes
    4. Saves the mapping to cache
    """
    global metarecipe_data
    
    cache_file = os.path.join(DATA_DIR, CACHE_JSON)
    # Try to get cache from json file
    meta_cache, cache_version = load_cache(cache_file, "metarecipe", get_version=True)
    
    # Parse meta recipes if there is no cache, or it's outdated
    if cache_version != Version.get():
        echo.info("Building meta recipe cache")
        
        # Load craft recipe data
        CRAFT_CACHE_FILE = "parsed_craftRecipe_data.json"
        craft_cache_path = os.path.join(DATA_DIR, CRAFT_CACHE_FILE)
        
        try:
            craft_data, _ = load_cache(craft_cache_path, "Craft", get_version=True)
            
            # Build meta recipe mapping
            metarecipe_data = build_metarecipe_mapping(craft_data)
            
            # Save the mapping to cache
            save_cache(metarecipe_data, CACHE_JSON)
            
            echo.success(f"Metarecipe cache saved to {CACHE_JSON}")
            
        except Exception as e:
            echo.warning(f"Error building meta recipe mapping: {e}")
            metarecipe_data = {}
    else:
        metarecipe_data = meta_cache
        echo.info(f"Loaded meta recipes from cache")