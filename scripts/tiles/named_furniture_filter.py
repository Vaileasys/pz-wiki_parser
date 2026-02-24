"""
Project Zomboid Wiki Named Furniture Filter

This script processes and organizes tile data for named furniture in Project Zomboid.
It handles both manually defined furniture groups and automatically detected furniture
based on game properties. The script is responsible for grouping related furniture
sprites and organizing them into logical sets for wiki documentation.

The script handles:
- Manual furniture group definitions
- Automatic furniture detection and grouping
- Multi-sprite furniture composition
- Variant handling for similar furniture types
- Directional (facing) furniture organization
"""

import os
from os import path
from scripts.core.constants import DATA_DIR
from scripts.core.cache import load_cache, save_cache
from scripts.utils import echo

MANUAL_GROUPS = {
    'Air conditioner': [
        "industry_01_4",
        "industry_01_5",
    ],
    'Air conditioner_2': [
        "rooftop_furniture_2",
        "rooftop_furniture_3",
    ],
    'Air conditioner_3': [
        "rooftop_furniture_5",
        "rooftop_furniture_4",
    ],
    'Air conditioner_4': [
        "rooftop_furniture_6",
        "rooftop_furniture_7",
    ],
    'Air conditioner_5': [
        "rooftop_furniture_8",
        "rooftop_furniture_9",
    ],
    'Air conditioner_6': [
        "rooftop_furniture_10",
        "rooftop_furniture_11",
    ],
    'Air conditioner_7': [
        "rooftop_furniture_13",
        "rooftop_furniture_12",
    ],
    'Air conditioner_8': [
        "rooftop_furniture_18",
        "rooftop_furniture_17",
    ],
    'Air conditioner_9': [
        "rooftop_furniture_20",
        "rooftop_furniture_19",
    ],
    'Hospital Bed': [
        "furniture_bedding_01_64",
        "furniture_bedding_01_65",
        "furniture_bedding_01_66",
        "furniture_bedding_01_67",
    ],
    'Wooden Bench': [
        "furniture_seating_indoor_03_66",
        "furniture_seating_indoor_03_67",
    ],
    'Wooden Bench_2': [
        "furniture_seating_indoor_03_64",
        "furniture_seating_indoor_03_65",
    ],
    'Park Bench': [
        "furniture_seating_outdoor_01_0",
        "furniture_seating_outdoor_01_1",
        "furniture_seating_outdoor_01_2",
        "furniture_seating_outdoor_01_3",
        "furniture_seating_outdoor_01_6",
        "furniture_seating_outdoor_01_7",
        "furniture_seating_outdoor_01_4",
        "furniture_seating_outdoor_01_5",
    ],
    'Office Desk': [
        "location_business_office_generic_01_5",
        "location_business_office_generic_01_6",
    ],
    'Office Desk_2': [
        "location_business_office_generic_01_42",
        "location_business_office_generic_01_43",
    ],
    'Office Desk_3': [
        "location_business_office_generic_01_1",
        "location_business_office_generic_01_0",
    ],
    'Crude Tall Locker': [
        "crafted_05_16",
        "crafted_05_17",
        "crafted_05_19",
    ],
    'Crude Tall Locker_2': [ # Bug doubled up S sprite
        "crafted_05_18",
    ],
    'Garbage Bin': [
        "location_restaurant_pizzawhirled_01_17",
        "location_restaurant_pizzawhirled_01_18",
    ],
    'Garbage Bin_2': [
        "location_restaurant_seahorse_01_38",
        "location_restaurant_seahorse_01_39",
    ],
    'Medical Desk': [
        "location_community_medical_01_106",
    ],
    'Large Metal Trough': [
        "location_farm_accesories_01_24",
        "location_farm_accesories_01_25",
        "location_farm_accesories_01_26",
    ],
    'Large Metal Trough_1': [
        "location_farm_accesories_01_24",
        "location_farm_accesories_01_25",
        "location_farm_accesories_01_26",
    ],
    'Small Metal Trough': [
        "location_farm_accesories_01_32",
        "location_farm_accesories_01_33",
    ],
    'Window': ["fixtures_windows_01_0"],
    'Window_2': ["fixtures_windows_01_2"],
    'Window_3': ["fixtures_windows_01_4"],
    'Window_4': ["fixtures_windows_01_6"],
    'Window_5': ["fixtures_windows_01_8"],
    'Window_6': ["fixtures_windows_01_10"],
    'Window_7': ["fixtures_windows_01_12"],
    'Window_8': ["fixtures_windows_01_14"],
    'Window_9': ["fixtures_windows_01_16"],
    'Window_10': ["fixtures_windows_01_18"],
    'Window_11': ["fixtures_windows_01_20"],
    'Window_12': ["fixtures_windows_01_22"],
    'Window_13': ["fixtures_windows_01_24"],
    'Window_14': ["fixtures_windows_01_26"],
    'Window_15': ["fixtures_windows_01_28"],
    'Window_16': ["fixtures_windows_01_30"],
    'Window_17': ["fixtures_windows_01_32"],
    'Window_18': ["fixtures_windows_01_34"],
    'Window_19': ["fixtures_windows_01_36"],
    'Window_20': ["fixtures_windows_01_38"],
    'Window_21': ["fixtures_windows_01_56"],
    'Window_22': ["fixtures_windows_01_58"],
    'Window_23': ["fixtures_windows_01_60"],
    'Window_24': ["fixtures_windows_01_62"],
}

def process_tiles(tiles_data: dict) -> dict:
    """
    Process and organize tile data into furniture groups.

    Args:
        tiles_data (dict): Raw tile data from the game files.

    Returns:
        dict: Processed and organized furniture groups.

    The processing follows these steps:
    1. Process manually defined groups from MANUAL_GROUPS
    2. Group remaining tiles by their GroupName and CustomName properties
    3. Within each group:
        - Split by sprite prefix if multiple exist
        - Handle facing directions for multi-sprite objects
        - Group by signature for variant handling
    """
    processed = {}

    # manual definitions
    manual_keys = set()
    for sprite_list in MANUAL_GROUPS.values():
        manual_keys.update(sprite_list)

    for display_name, sprite_list in MANUAL_GROUPS.items():
        group_obj = {}
        for key in sprite_list:
            info = tiles_data.get(key)
            if not info:
                continue
            entry = {'sprite': key}
            entry.update(info)
            group_obj[key] = entry
        if group_obj:
            processed[display_name] = group_obj

    remaining_tiles = {
        name: info
        for name, info in tiles_data.items()
        if name not in manual_keys
    }

    # Sort by display name
    buckets = {}
    for tile_name, tile_info in remaining_tiles.items():
        generic = tile_info.get('properties', {}).get('generic', {})
        if 'IsMoveAble' not in generic or not any(k in generic for k in ('GroupName', 'CustomName')):
            continue
        group_name = generic.get('GroupName', '').strip()
        custom_name = generic.get('CustomName', '').strip()
        display_key = f"{group_name} {custom_name}".strip()
        buckets.setdefault(display_key, []).append((tile_name, tile_info))

    FACING_ORDER = {'E': 0, 'S': 1, 'W': 2, 'N': 3}

    def _process_group(entries, base_name):
        """
        Process a group of related tile entries into a furniture group.

        Args:
            entries (list): List of tuples containing (tile_name, tile_info).
            base_name (str): Base name for the group, may include variant suffixes.

        The function handles:
        - Multi-sprite furniture with facing directions
        - Signature-based grouping for variants
        - Name deduplication for multiple variants
        """
        # Multi-sprite grouping
        if any('Facing' in info.get('properties', {}).get('generic', {}) for _, info in entries):
            entries.sort(
                key=lambda pair: FACING_ORDER.get(
                    pair[1]['properties']['generic'].get('Facing', ''),
                    pair[1].get('id', 0)
                )
            )
            group = {}
            for name, info in entries:
                entry = {'sprite': name}
                entry.update(info)
                group[name] = entry
            processed[base_name] = group
            return

        # No Facing
        signature_buckets = {}
        for name, info in entries:
            gp = info.get('properties', {}).get('generic', {})
            signature = (
                info.get('tileSheetIndex'),
                gp.get('PickUpWeight'),
                gp.get('IsoType'),
                gp.get('Material'),
                gp.get('Material2'),
                gp.get('Material3'),
            )
            signature_buckets.setdefault(signature, []).append((name, info))

        groups = list(signature_buckets.values())
        if len(groups) == 1:
            group = {}
            for name, info in groups[0]:
                entry = {'sprite': name}
                entry.update(info)
                group[name] = entry
            processed[base_name] = group
        else:
            # handle duplicate names
            for idx, sig_entries in enumerate(groups, start=1):
                variant_name = base_name if idx == 1 else f"{base_name}_{idx}"
                group = {}
                for name, info in sig_entries:
                    entry = {'sprite': name}
                    entry.update(info)
                    group[name] = entry
                processed[variant_name] = group

    for display_key, entries in buckets.items():
        prefix_map = {}
        for name, info in entries:
            prefix = name.split('_', 1)[0]
            prefix_map.setdefault(prefix, []).append((name, info))

        if len(prefix_map) > 1:
            for idx, variant_entries in enumerate(prefix_map.values(), start=1):
                variant_name = display_key if idx == 1 else f"{display_key}_{idx}"
                _process_group(variant_entries, variant_name)
        else:
            _process_group(entries, display_key)

    return processed

def main():
    """
    Main execution function for the named furniture filter.

    This function:
    1. Loads the tile data cache
    2. Processes tiles into furniture groups
    3. Saves the processed data back to cache
    4. Provides progress feedback through echo messages
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    tiles_cache_filename = 'tiles_data.json'
    tiles_cache_path = path.join(DATA_DIR, tiles_cache_filename)
    echo.info(f'Loading tiles cache from {tiles_cache_path}')
    try:
        tiles_data = load_cache(tiles_cache_path, 'Tiles')
    except Exception as err:
        echo.error(f'Error loading tiles cache: {err}')
        return

    processed_data = process_tiles(tiles_data)

    output_filename = 'named_furniture.json'
    output_path = path.join(DATA_DIR, output_filename)
    echo.info(f'Saving processed tiles to {output_path}')
    try:
        save_cache(processed_data, output_filename, DATA_DIR)
        echo.success(f'Successfully saved {len(processed_data)} groups to {output_filename}')
    except Exception as err:
        echo.error(f'Error saving processed tiles: {err}')

if __name__ == '__main__':
    main()