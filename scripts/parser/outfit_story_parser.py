"""
Parses outfit usage from decompiled randomized story Java files.

Scans randomizedWorld story classes for outfit ID references and caches both
story-to-outfit and outfit-to-story lookup data.
"""
import json
import os
import re
from tqdm import tqdm

from scripts.core.constants import OUTPUT_DIR, CACHE_DIR
from scripts.utils import echo


def parse_outfit_stories(outfit_data: dict, force_regenerate: bool = False) -> dict:
    """
    Parse randomized story files for outfit references.

    Args:
        outfit_data: Parsed outfit data.
        force_regenerate: Reparse files instead of using cache.
    """
    cache_file = os.path.join(CACHE_DIR, "story_outfits.json")

    if not force_regenerate and os.path.exists(cache_file):
        echo.info("Loading story outfits from cache...")

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_data = json.load(f)

            echo.success("Loaded cached story outfits data")
            return cached_data
        except Exception as e:
            echo.warning(f"Failed to load cache, regenerating: {e}")

    echo.info("Parsing story files for outfit references...")

    outfit_ids = get_outfit_ids(outfit_data)
    echo.info(f"Searching for {len(outfit_ids)} outfit IDs in story files...")

    story_files = get_story_files()

    if not story_files or sum(len(files) for files in story_files.values()) == 0:
        echo.warning("No story files found to search")
        return {}

    story_outfits_data = {
        "story_types": {},
        "outfit_to_stories": {
            outfit_id: []
            for outfit_id in outfit_ids
        },
    }

    total_matches = 0
    files_with_matches = 0

    for story_type, file_paths in story_files.items():
        if not file_paths:
            continue

        echo.info(f"Searching {story_type} stories ({len(file_paths)} files)...")
        story_type_data = {}

        with tqdm(total=len(file_paths), desc=f"  {story_type}", unit="files") as pbar:
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                story_id = os.path.splitext(filename)[0]

                found_outfits = search_file_for_outfits(file_path, outfit_ids)

                if found_outfits:
                    story_type_data[story_id] = {
                        "file": filename,
                        "outfits": sorted(found_outfits),
                    }

                    for outfit_id in found_outfits:
                        story_outfits_data["outfit_to_stories"][outfit_id].append(
                            {
                                "type": story_type,
                                "id": story_id,
                                "file": filename,
                            }
                        )

                    total_matches += len(found_outfits)
                    files_with_matches += 1

                pbar.update(1)

        if story_type_data:
            story_outfits_data["story_types"][story_type] = story_type_data

    story_outfits_data["outfit_to_stories"] = {
        outfit_id: stories
        for outfit_id, stories in story_outfits_data["outfit_to_stories"].items()
        if stories
    }

    echo.success(
        f"Found {total_matches} outfit references across {files_with_matches} story files"
    )
    echo.info(
        f"{len(story_outfits_data['outfit_to_stories'])} outfits appear in at least one story"
    )

    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(story_outfits_data, f, indent=2)

        echo.success(f"Saved story outfits data to cache: {cache_file}")
    except Exception as e:
        echo.error(f"Failed to save cache: {e}")

    return story_outfits_data


def get_outfit_ids(outfit_data: dict) -> set[str]:
    """
    Return all outfit IDs from male and female outfit data.

    Args:
        outfit_data: Parsed outfit data.
    """
    outfit_ids = set()
    outfit_ids.update(outfit_data.get("MaleOutfits", {}).keys())
    outfit_ids.update(outfit_data.get("FemaleOutfits", {}).keys())
    return outfit_ids


def get_story_files() -> dict[str, list[str]]:
    """Return randomized story Java files grouped by story type."""
    base_path = os.path.join(
        OUTPUT_DIR,
        "ZomboidDecompiler",
        "source",
        "zombie",
        "randomizedWorld",
    )

    if not os.path.exists(base_path):
        echo.warning(f"Decompiler output directory not found at {base_path}")
        return {}

    prefix_mapping = {
        "RBTS": "random_table",
        "RB": "random_building",
        "RDS": "random_survivor",
        "RVS": "random_vehicle",
        "RZS": "random_zone",
    }

    story_files = {
        "random_building": [],
        "random_table": [],
        "random_survivor": [],
        "random_vehicle": [],
        "random_zone": [],
    }

    for root, dirs, files in os.walk(base_path):
        for filename in files:
            if not filename.endswith(".java"):
                continue

            if filename.endswith("Base.java"):
                continue

            for prefix, story_type in prefix_mapping.items():
                if filename.startswith(prefix):
                    file_path = os.path.join(root, filename)
                    story_files[story_type].append(file_path)
                    break

    total_files = sum(len(files) for files in story_files.values())
    echo.info(f"Found {total_files} story files to search")

    return story_files


def search_file_for_outfits(file_path: str, outfit_ids: set[str]) -> list[str]:
    """
    Search a Java file for outfit ID references.

    Args:
        file_path: Java file path.
        outfit_ids: Outfit IDs to search for.
    """
    filename = os.path.basename(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception as e:
        echo.error(f"Error reading {filename}: {e}")
        return []

    found_outfits = []

    for outfit_id in outfit_ids:
        pattern = rf"\b{re.escape(outfit_id)}\b"

        if re.search(pattern, file_content):
            found_outfits.append(outfit_id)

    return found_outfits