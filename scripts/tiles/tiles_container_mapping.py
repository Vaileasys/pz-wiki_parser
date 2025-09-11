"""
Project Zomboid Wiki Container Mapping Generator

This script processes the tiles cache to create a mapping of container types to their
associated tile textures. It identifies tiles that have a non-empty "container" property
in their generic properties and groups them by container type.

The output is a JSON file that maps container types to lists of tile textures that
belong to that container type, useful for wiki organization and cross-referencing.
"""

import os
import json
from typing import Dict, List
from scripts.core.constants import DATA_DIR, OUTPUT_LANG_DIR
from scripts.core.language import Language
from scripts.core.cache import load_cache
from scripts.utils import echo


def generate_container_mapping(
    tiles_data: Dict, lang_code: str
) -> Dict[str, Dict[str, List[str]]]:
    """
    Generate container mapping from tiles data.

    Args:
        tiles_data (Dict): The loaded tiles cache data
        lang_code (str): Language code for output directory

    Returns:
        Dict[str, Dict[str, List[str]]]: Mapping of container types to objects with textures lists
    """
    container_mapping = {}

    for tile_name, tile_data in tiles_data.items():
        # Check if tile has properties and generic properties
        if not tile_data.get("properties") or not tile_data["properties"].get(
            "generic"
        ):
            continue

        generic_props = tile_data["properties"]["generic"]
        container_type = generic_props.get("container")

        # Only process tiles with non-empty container property
        if container_type and container_type.strip():
            if container_type not in container_mapping:
                container_mapping[container_type] = {"textures": []}

            # Add the tile name to the container's texture list
            container_mapping[container_type]["textures"].append(tile_name)

    # Sort the texture lists for consistent output
    for container_type in container_mapping:
        container_mapping[container_type]["textures"].sort()

    return container_mapping


def save_container_mapping(
    container_mapping: Dict[str, Dict[str, List[str]]], lang_code: str
) -> None:
    """
    Save each container type to a separate JSON file in the container_mapping directory
    and generate a batch file for processing.

    Args:
        container_mapping (Dict[str, Dict[str, List[str]]]): The container mapping data
        lang_code (str): Language code for output directory
    """
    # Create the output directory structure
    output_dir = OUTPUT_LANG_DIR.format(language_code=lang_code)
    container_mapping_dir = os.path.join(output_dir, "tiles", "container_mapping")
    os.makedirs(container_mapping_dir, exist_ok=True)

    # Save each container type to a separate file
    for container_type, container_data in container_mapping.items():
        # Create a safe filename by replacing invalid characters
        safe_filename = (
            container_type.replace("/", "_").replace("\\", "_").replace(":", "_")
        )
        output_file = os.path.join(container_mapping_dir, f"{safe_filename}.json")

        # Create the properly nested structure with container type as the key
        nested_data = {container_type: container_data}

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(nested_data, f, indent=2, ensure_ascii=False)

        echo.info(f"Container '{container_type}' saved to {output_file}")

    # Generate the batch file in the main tiles output directory
    tiles_output_dir = os.path.join(output_dir, "tiles")
    batch_file_path = os.path.join(tiles_output_dir, "locate_containers.bat")

    with open(batch_file_path, "w", encoding="utf-8") as f:
        f.write("@echo off\n\n")
        f.write("if not exist processed_containers mkdir processed_containers\n\n")

        for container_type in container_mapping.keys():
            # Create a safe filename for the batch command
            safe_filename = (
                container_type.replace("/", "_").replace("\\", "_").replace(":", "_")
            )
            # Use relative paths: input from container_mapping, output to processed_containers
            f.write(
                f"python locate_texture.py --disable-adjacency-filter -c S:\\PZmap\\conf\\conf.yaml -p 16 -o processed_containers\\{safe_filename}_processed_containers.json -z 128 -i container_mapping\\{safe_filename}.json\n"
            )

        f.write("\npause\n")

    echo.info(f"Batch file 'locate_containers.bat' created at {batch_file_path}")
    echo.info(f"All container mappings saved to {container_mapping_dir}")


def main(tiles_data: Dict = None, lang_code: str = None) -> None:
    """
    Main function to generate container mapping from tiles data.

    Args:
        tiles_data (Dict, optional): Pre-loaded tiles data. If None, loads from cache.
        lang_code (str, optional): Language code. If None, gets from Language.get().
    """
    if tiles_data is None:
        # Load tiles data from cache
        tiles_cache_path = os.path.join(DATA_DIR, "cache", "tiles_data.json")
        tiles_data = load_cache(tiles_cache_path, "Tiles")

    if lang_code is None:
        lang_code = Language.get()

    echo.info("Generating container mapping")

    # Generate the container mapping
    container_mapping = generate_container_mapping(tiles_data, lang_code)

    # Save the mapping
    save_container_mapping(container_mapping, lang_code)

    # Report statistics
    total_containers = len(container_mapping)
    total_tiles = sum(
        len(container_data["textures"]) for container_data in container_mapping.values()
    )

    echo.success(
        f"Container mapping generated: {total_containers} container types, {total_tiles} total tiles"
    )


if __name__ == "__main__":
    main()
