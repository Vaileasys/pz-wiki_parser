import json
import os
import platform
import re
import subprocess
from tqdm import tqdm
import scripts.parser.outfit_parser as outfit_parser
from scripts.core import page_manager, cache, config_manager
from scripts.core.version import Version
from scripts.core.constants import OUTPUT_DIR, BOT_FLAG, BOT_FLAG_END, CACHE_DIR
from scripts.core.file_loading import get_lua_dir
from scripts.utils import echo
from scripts.utils.lua_helper import parse_lua_tables, save_cache
from scripts.objects.item import Item

# Cache for clothing name to game item ID mapping
_clothing_name_cache = None

# Global cache for story outfits data
_story_outfits_data = None

# Global cache for zone definitions data
_zone_definitions_data = None


def _build_clothing_name_mapping():
    """
    Build a reverse mapping from clothing item names to game item IDs.
    This uses cached item data (not reparsing) and caches the mapping itself.

    For example: "Belt" -> "Base.Belt2", "Bag_HikingBag" -> "Base.Bag_HikingBag"

    Returns:
        dict: Mapping of clothing item name to game item ID
    """
    global _clothing_name_cache

    clothing_mapping = {}

    # Load all items (uses cache if available - not reparsing!)
    if Item._items is None:
        Item._load_items()

    # Build reverse lookup for items with ClothingItem property
    for item_id, item_data in Item._items.items():
        clothing_name = item_data.get("clothingitem")  # Keys are lowercase
        if clothing_name:
            # Use the first item found for each clothing name (usually the base version)
            if clothing_name not in clothing_mapping:
                clothing_mapping[clothing_name] = item_id

    # Cache the mapping
    _clothing_name_cache = clothing_mapping
    return clothing_mapping


def parse_story_outfits(outfit_data, force_regenerate=False):
    """
    Parse randomized story Java files to find which outfits appear in which stories.
    Similar to parse_stories in distribution_parser.py but specifically for outfits.

    Args:
        outfit_data (dict): The outfit data dictionary containing MaleOutfits and FemaleOutfits
        force_regenerate (bool): If True, regenerate cache even if it exists

    Returns:
        dict: Mapping of story types and IDs to the outfit IDs they contain
    """
    cache_file = os.path.join(CACHE_DIR, "story_outfits.json")

    # Check if cache exists and return it if not forcing regeneration
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

    # Get all unique outfit IDs from both male and female sections
    all_outfit_ids = set()
    all_outfit_ids.update(outfit_data.get("MaleOutfits", {}).keys())
    all_outfit_ids.update(outfit_data.get("FemaleOutfits", {}).keys())

    echo.info(f"Searching for {len(all_outfit_ids)} outfit IDs in story files...")

    def get_story_files():
        """
        Scans the decompiled Java directory and categorizes story files by prefix.
        Returns:
            dict: Dictionary mapping story types to lists of file paths
        """
        base_path = os.path.join(
            OUTPUT_DIR, "ZomboidDecompiler", "source", "zombie", "randomizedWorld"
        )

        if not os.path.exists(base_path):
            echo.warning(f"Decompiler output directory not found at {base_path}")
            return {}

        # Define file categorization based on prefixes
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

        # Scan all subdirectories for Java files
        for root, dirs, files in os.walk(base_path):
            for filename in files:
                if not filename.endswith(".java"):
                    continue

                # Skip base classes
                if filename.endswith("Base.java"):
                    continue

                # Check prefixes in order (most specific first)
                for prefix, story_type in prefix_mapping.items():
                    if filename.startswith(prefix):
                        file_path = os.path.join(root, filename)
                        story_files[story_type].append(file_path)
                        break

        # Print summary
        total_files = sum(len(files) for files in story_files.values())
        echo.info(f"Found {total_files} story files to search")

        return story_files

    def search_file_for_outfits(file_path, outfit_ids):
        """
        Search a Java file for outfit ID references.

        Args:
            file_path (str): Path to the Java file
            outfit_ids (set): Set of outfit IDs to search for

        Returns:
            list: List of outfit IDs found in the file
        """
        filename = os.path.basename(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        except Exception as e:
            echo.error(f"Error reading {filename}: {e}")
            return []

        found_outfits = []

        # Search for each outfit ID in the file content
        for outfit_id in outfit_ids:
            # Look for the outfit ID as a complete word (not part of another word)
            # Common patterns: "OutfitID" or 'OutfitID' or OutfitID in various contexts
            pattern = rf"\b{re.escape(outfit_id)}\b"
            if re.search(pattern, file_content):
                found_outfits.append(outfit_id)

        return found_outfits

    # Get all story files
    story_files = get_story_files()

    if not story_files or sum(len(files) for files in story_files.values()) == 0:
        echo.warning("No story files found to search")
        return {}

    # Build mapping of stories to outfits
    story_outfits_data = {"story_types": {}, "outfit_to_stories": {}}

    # Initialize outfit_to_stories mapping for all outfit IDs
    for outfit_id in all_outfit_ids:
        story_outfits_data["outfit_to_stories"][outfit_id] = []

    # Track statistics
    total_matches = 0
    files_with_matches = 0

    # Process each story type
    for story_type, file_paths in story_files.items():
        if not file_paths:
            continue

        echo.info(f"Searching {story_type} stories ({len(file_paths)} files)...")

        story_type_data = {}

        # Process each file with progress bar
        with tqdm(total=len(file_paths), desc=f"  {story_type}", unit="files") as pbar:
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                story_id = os.path.splitext(filename)[0]

                # Search for outfit IDs in this file
                found_outfits = search_file_for_outfits(file_path, all_outfit_ids)

                if found_outfits:
                    # Store in story_types mapping
                    story_type_data[story_id] = {
                        "file": filename,
                        "outfits": sorted(found_outfits),
                    }

                    # Store in outfit_to_stories reverse mapping
                    for outfit_id in found_outfits:
                        story_outfits_data["outfit_to_stories"][outfit_id].append(
                            {"type": story_type, "id": story_id, "file": filename}
                        )

                    total_matches += len(found_outfits)
                    files_with_matches += 1

                pbar.update(1)

        if story_type_data:
            story_outfits_data["story_types"][story_type] = story_type_data

    # Clean up outfit_to_stories - remove entries with no stories
    story_outfits_data["outfit_to_stories"] = {
        outfit_id: stories
        for outfit_id, stories in story_outfits_data["outfit_to_stories"].items()
        if stories
    }

    # Print summary
    echo.success(
        f"Found {total_matches} outfit references across {files_with_matches} story files"
    )
    echo.info(
        f"{len(story_outfits_data['outfit_to_stories'])} outfits appear in at least one story"
    )

    # Save to cache
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(story_outfits_data, f, indent=2)
        echo.success(f"Saved story outfits data to cache: {cache_file}")
    except Exception as e:
        echo.error(f"Failed to save cache: {e}")

    # Store in global cache for use by overview functions
    global _story_outfits_data
    _story_outfits_data = story_outfits_data

    return story_outfits_data


def load_zone_definitions(force_regenerate=False):
    """
    Load and cache zone definitions from ZombiesZoneDefinition.lua file.

    Args:
        force_regenerate (bool): If True, regenerate cache even if it exists

    Returns:
        dict: Zone definitions data
    """
    global _zone_definitions_data

    cache_file = os.path.join(CACHE_DIR, "zone_definitions.json")

    # Check if cache exists and return it if not forcing regeneration
    if not force_regenerate and os.path.exists(cache_file):
        echo.info("Loading zone definitions from cache...")
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
            echo.success("Loaded cached zone definitions data")
            _zone_definitions_data = cached_data
            return cached_data
        except Exception as e:
            echo.warning(f"Failed to load cache, regenerating: {e}")

    echo.info("Loading ZombiesZoneDefinition.lua file...")

    # Build the path to the ZombiesZoneDefinition.lua file
    lua_dir = get_lua_dir()
    zone_file_path = os.path.join(
        lua_dir, "shared", "npcs", "ZombiesZoneDefinition.lua"
    )

    if not os.path.exists(zone_file_path):
        echo.error(f"ZombiesZoneDefinition.lua not found at {zone_file_path}")
        return {}

    try:
        # Load the Lua file directly since it's not in the game file map
        from scripts.core.file_loading import read_file
        from lupa import LuaRuntime, LuaError

        # Create Lua runtime with proper package paths
        lua_runtime = LuaRuntime(unpack_returned_tuples=True)
        lua_path = os.path.normpath(get_lua_dir()).replace(os.sep, "/")
        extra_paths = [
            f"{lua_path}/?.lua",
            f"{lua_path}/shared/?.lua",
            f"{lua_path}/client/?.lua",
            f"{lua_path}/server/?.lua",
        ]
        lua_runtime.execute(
            "package.path = package.path .. ';" + ";".join(extra_paths) + "'"
        )

        # Execute the Lua file content directly
        lua_content = read_file(zone_file_path)
        try:
            lua_runtime.execute(lua_content)
        except LuaError as e:
            echo.error(f"Failed to execute Lua file {zone_file_path}: {e}")
            return {}

        # Parse the ZombiesZoneDefinition table specifically
        try:
            parsed_data = parse_lua_tables(
                lua_runtime, tables=["ZombiesZoneDefinition"]
            )
        except LuaError as e:
            echo.warning(f"Failed to parse ZombiesZoneDefinition table: {e}")
            parsed_data = {}

        # Also try to get all tables to see what's available for debugging
        try:
            all_tables = parse_lua_tables(lua_runtime)
        except LuaError as e:
            echo.warning(f"Failed to parse all tables: {e}")
            all_tables = {}

        if "ZombiesZoneDefinition" not in parsed_data and all_tables:
            echo.warning(
                "ZombiesZoneDefinition not found in globals, available tables: "
                + ", ".join(all_tables.keys())
            )
            parsed_data = all_tables

        echo.success(f"Parsed {len(parsed_data)} zone definition tables")

        # Save to cache
        try:
            save_cache(parsed_data, "zone_definitions.json")
            echo.success(f"Saved zone definitions data to cache: {cache_file}")
        except Exception as e:
            echo.error(f"Failed to save cache: {e}")

        # Store in global cache
        _zone_definitions_data = parsed_data
        return parsed_data

    except Exception as e:
        echo.error(f"Error loading zone definitions: {e}")
        return {}


def get_outfit_display_name(outfit_id, page_dict):
    """
    Get the display name for an outfit from the page dictionary

    Args:
        outfit_id (str): The outfit ID
        page_dict (dict): Page dictionary

    Returns:
        str: Display name for the outfit
    """
    # Find all pages that have this outfit_id
    for page_name, page_data in page_dict.items():
        if "outfit_id" in page_data:
            outfit_ids = page_data.get("outfit_id", [])
            if isinstance(outfit_ids, str):
                outfit_ids = [outfit_ids]
            if outfit_id in outfit_ids:
                return page_name

    # Return fallback to outfit_id if not found
    return outfit_id


def create_articles(outfit_data, page_dict, output_dir, story_outfits_data=None):
    """
    Create outfit articles using nested functions to build each section

    Args:
        outfit_data (dict): Parsed outfit data from cache
        page_dict (dict): Page dictionary with items and outfits sections
        output_dir (str): Output directory path
        story_outfits_data (dict): Story outfits data for spawn location processing
    """
    echo.info("Creating outfit articles...")

    # Build reverse mapping: clothing item name -> game item ID
    echo.info("Building clothing item name to game item ID mapping...")
    clothing_to_item_mapping = _build_clothing_name_mapping()
    echo.success(f"Mapped {len(clothing_to_item_mapping)} clothing items to game items")

    def build_article(outfit_id, outfit_data, sex_type="Both", story_data=None):
        """
        Build a complete article for a specific outfit

        Args:
            outfit_id (str): The outfit ID (e.g., "1RJTest")
            outfit_data (dict): The complete outfit data dictionary
            sex_type (str): "Male", "Female", or "Both"
            story_data (dict): Story outfits data for spawn location processing

        Returns:
            dict: Dictionary containing all sections and the complete article
        """
        # Get outfit name for file naming
        outfit_name = get_outfit_display_name(outfit_id, page_dict)

        # Build each section
        header_section = create_header()
        infobox_section = create_infobox(outfit_id, outfit_data, sex_type)
        intro_section = create_intro(outfit_id, outfit_data)
        overview_section = create_overview(
            outfit_id, outfit_data, sex_type, story_outfits_data
        )
        items_data = create_items(outfit_id, outfit_data, sex_type)
        code_section = create_code(outfit_id, outfit_data)
        navigation_section = create_navigation(sex_type)

        # Combine all sections into complete article with proper formatting
        complete_article = (
            header_section
            + infobox_section
            + intro_section
            + "\n\n== Overview ==\n"
            + overview_section["content"]
        )

        # Only add Items section if there is item data
        if items_data["content"].strip():
            complete_article += "\n\n== Items ==\n" + items_data["content"]

        complete_article += (
            "\n\n== Code ==\n"
            + code_section
            + "\n\n== Navigation ==\n"
            + navigation_section
        )

        # Return all sections and complete article
        return {
            "article_name": outfit_name,
            "complete_article": complete_article,
            "infobox": infobox_section,
            "overview_content": overview_section["content"],
            "items_content": items_data["content"],
            "items_tables": items_data["tables_data"],
            "code": code_section,
        }

    def create_header():
        """Create the header section of the article"""
        version = config_manager.get_version()
        return f"""{{{{Header|Project Zomboid|World|Lore|Outfits}}}}
{{{{Page version|{version}}}}}
"""

    def create_infobox(outfit_id, outfit_data, sex_type):
        """
        Create the infobox section for a specific outfit

        Args:
            outfit_id (str): The outfit ID (e.g., "1RJTest")
            outfit_data (dict): The outfit data dictionary
            sex_type (str): "Male", "Female", or "Both"

        Returns:
            str: Complete infobox template
        """
        # Get outfit name from page dictionary or use outfit_id as fallback
        outfit_name = get_outfit_display_name(outfit_id, page_dict)
        sex_exclusivity = "Male and Female"  # Default fallback

        # Determine sex exclusivity based on outfit data
        male_exists = outfit_id in outfit_data.get("MaleOutfits", {})
        female_exists = outfit_id in outfit_data.get("FemaleOutfits", {})

        if male_exists and female_exists:
            sex_exclusivity = "Male and Female"
        elif male_exists:
            sex_exclusivity = "Male exclusive"
        elif female_exists:
            sex_exclusivity = "Female exclusive"

        # Get GUIDs for this outfit
        guids = []
        if male_exists:
            male_outfit = outfit_data["MaleOutfits"][outfit_id]
            if "GUID" in male_outfit:
                guids.append(male_outfit["GUID"])
        if female_exists:
            female_outfit = outfit_data["FemaleOutfits"][outfit_id]
            if "GUID" in female_outfit:
                guids.append(female_outfit["GUID"])

        # Build infobox
        infobox_lines = [
            "{{Infobox outfit",
            f"|name={outfit_name}",
        ]

        # Handle image parameters based on sex availability
        if male_exists and female_exists:
            # Both sexes - need image and image2
            infobox_lines.append(f"|image=outfit_{outfit_id}_Male.png")
            infobox_lines.append(f"|image2=outfit_{outfit_id}_Female.png")
        else:
            # Single sex - use appropriate image
            if male_exists:
                infobox_lines.append(f"|image=outfit_{outfit_id}_Male.png")
            else:
                infobox_lines.append(f"|image=outfit_{outfit_id}_Female.png")

        infobox_lines.extend(
            [
                f"|sex={sex_exclusivity}",
                f"|outfit_id={outfit_id}",
            ]
        )

        # Add GUID parameters
        for i, guid in enumerate(guids):
            if i == 0:
                infobox_lines.append(f"|guid={guid}")
            else:
                infobox_lines.append(f"|guid{i + 1}={guid}")

        infobox_lines.append("}}")
        return "\n".join(infobox_lines).rstrip("\n")

    def create_overview(outfit_id, outfit_data, sex_type, story_data=None):
        """
        Create the overview section of the article

        Args:
            outfit_id (str): The outfit ID
            outfit_data (dict): The complete outfit data dictionary
            sex_type (str): "Male", "Female", or "Both"
            story_data (dict): Story outfits data for spawn location processing

        Returns:
            dict: Contains 'content' (for article) and 'bot_flagged' (for individual files)
        """

        def process_stories(outfit_id, story_data=None):
            """
            Process story-related spawn locations for the outfit

            Args:
                outfit_id (str): The outfit ID
                story_data (dict): Story outfits data for spawn location processing

            Returns:
                str: Story-related spawn information
            """
            global _story_outfits_data

            # Use provided story data, or fallback to global cache, or load from file
            if story_data is not None:
                pass  # Use the provided story_data
            else:
                # Try to load from cache file
                cache_file = os.path.join(CACHE_DIR, "story_outfits.json")
                if os.path.exists(cache_file):
                    try:
                        with open(cache_file, "r", encoding="utf-8") as f:
                            story_data = json.load(f)
                        # Update global cache
                        _story_outfits_data = story_data
                    except Exception as e:
                        echo.warning(f"Failed to load story outfits cache: {e}")
                        return "Story data not available"
                else:
                    return "Story data not available"

            # Get stories that contain this outfit
            outfit_stories = story_data.get("outfit_to_stories", {}).get(outfit_id, [])

            if not outfit_stories:
                return ""

            # Group stories by type and collect unique story IDs
            stories_by_type = {}
            for story in outfit_stories:
                story_type = story.get("type", "unknown")
                story_id = story.get("id", "unknown")

                if story_type not in stories_by_type:
                    stories_by_type[story_type] = []
                stories_by_type[story_type].append(story_id)

            # Build the story list text
            story_lines = []

            # Collect all unique story IDs across all types
            all_story_ids = set()
            story_type_map = {}  # Map story_id to its type for link formatting

            for story in outfit_stories:
                story_type = story.get("type", "unknown")
                story_id = story.get("id", "unknown")
                all_story_ids.add(story_id)
                story_type_map[story_id] = story_type

            # Sort all story IDs
            for story_id in sorted(all_story_ids):
                # Get the story type for this ID
                story_type = story_type_map.get(story_id, "unknown")
                # Format link based on story type
                story_link = format_story_link(story_type, story_id)
                story_lines.append(f"*{story_link}")

            return "\n".join(story_lines)

        def format_display_name(story_id):
            """
            Format a story ID for display by removing prefix and converting camel case to spaced words

            Args:
                story_id (str): The story ID (e.g., "RBBurntFireman")

            Returns:
                str: Formatted display name (e.g., "Burnt Fireman")
            """
            # Remove common prefixes
            prefixes = ["RB", "RDS", "RVS", "RZS", "RBTS"]
            display_name = story_id

            for prefix in prefixes:
                if story_id.startswith(prefix):
                    display_name = story_id[len(prefix) :]
                    break

            # Convert camel case to spaced words
            # Insert space before capital letters (except at start)
            display_name = re.sub(r"(?<!^)([A-Z])", r" \1", display_name)

            return display_name

        def format_story_link(story_type, story_id):
            """
            Format a story link based on the story type

            Args:
                story_type (str): The type of story (e.g., "random_building", "random_vehicle")
                story_id (str): The story ID (e.g., "RBBurntFireman")

            Returns:
                str: Formatted wiki link
            """
            display_name = format_display_name(story_id)

            if story_type == "random_building":
                # Building stories: [[Building stories#{anchor_name}|{display_name}]]
                # Remove RB prefix and apply camel case splitting to anchor as well
                temp_name = story_id[2:] if story_id.startswith("RB") else story_id
                anchor_name = re.sub(r"(?<!^)([A-Z])", r" \1", temp_name)
                return f"[[Building stories#{anchor_name}|{display_name}]]"
            else:
                # All other story types: link directly to the display name
                return f"[[{display_name}]]"

        def process_zones(outfit_id, outfit_data, sex_type):
            """
            Process zone-related spawn locations for the outfit

            Args:
                outfit_id (str): The outfit ID
                outfit_data (dict): The complete outfit data dictionary
                sex_type (str): "Male", "Female", or "Both"

            Returns:
                str: Zone-related spawn information
            """
            global _zone_definitions_data

            # Ensure zone definitions are loaded
            if _zone_definitions_data is None:
                _zone_definitions_data = load_zone_definitions()

            if not _zone_definitions_data:
                # Fallback if no zone data available - return empty
                return ""

            # Search for outfit_id in zone definitions
            found_zones = []

            for table_name, table_data in _zone_definitions_data.items():
                if not isinstance(table_data, dict):
                    continue

                # Look for outfit references in the zone data
                for zone_name, zone_info in table_data.items():
                    if not isinstance(zone_info, dict):
                        continue

                    # Check each outfit entry in this zone
                    for outfit_key, outfit_data in zone_info.items():
                        if not isinstance(outfit_data, dict):
                            continue

                        # Check if this outfit entry contains our outfit_id
                        outfit_name = outfit_data.get("name", "")
                        if outfit_name == outfit_id:
                            found_zones.append(
                                {
                                    "zone_name": zone_name,
                                    "outfit_key": outfit_key,
                                    "outfit_info": outfit_data,
                                    "table_name": table_name,
                                }
                            )

            # Deduplicate zones - if same zone appears multiple times, keep only one entry
            # This handles cases like Chef and ChefM both having name="Chef"
            seen_zones = set()
            unique_zones = []
            for zone_data in found_zones:
                zone_name = zone_data["zone_name"]
                if zone_name not in seen_zones:
                    seen_zones.add(zone_name)
                    unique_zones.append(zone_data)

            # If no zones found, return empty (don't show section)
            if not unique_zones:
                return ""

            # Build table with found zones
            table_lines = []
            table_lines.append('{| class="wikitable theme-red sortable"')
            table_lines.append("! Spawn Zone")
            table_lines.append("! Chance")

            for zone_data in unique_zones:
                zone_name = zone_data["zone_name"]
                outfit_info = zone_data["outfit_info"]

                # Format spawn zone as a link
                spawn_zone_link = (
                    f"[https://b42map.com/?zombie={zone_name} {zone_name}]"
                )

                # Format chance information
                chance = "Unknown"
                if "chance" in outfit_info:
                    chance_value = outfit_info["chance"]
                    if isinstance(chance_value, (int, float)):
                        chance = f"{chance_value}%"
                elif outfit_info.get("mandatory") == "true":
                    to_spawn = outfit_info.get("toSpawn", 1)
                    if isinstance(to_spawn, (int, float)):
                        chance = f"{int(to_spawn)} mandatory"
                    else:
                        chance = "1 mandatory"

                table_lines.append("|-")
                table_lines.append(f"| {spawn_zone_link}")
                table_lines.append(f"| {chance}")

            table_lines.append("|}")
            return "\n".join(table_lines)

        # Process spawn locations using the nested functions
        stories_info = process_stories(outfit_id, outfit_data)
        zones_info = process_zones(outfit_id, outfit_data, sex_type)

        # Determine what sections to include based on available data
        has_stories = bool(stories_info.strip())
        has_zones = bool(zones_info.strip())

        if not has_stories and not has_zones:
            # Default case: no stories, no zones
            overview_content = (
                "It does not spawn in any [[randomized stories]] or zombie zones."
            )
        elif has_stories and not has_zones:
            # Stories only case
            overview_content = f"""It spawns in the following [[randomized stories]]:
{stories_info}"""
        elif not has_stories and has_zones:
            # Zones only case
            overview_content = f"""It spawns in the following zombie zones:
{zones_info}"""
        else:
            # Both stories and zones case
            overview_content = f"""It spawns in the following [[randomized stories]]:
{stories_info}

It spawns in the following zombie zones:
{zones_info}"""

        return {"content": overview_content}

    def create_intro(outfit_id, outfit_data):
        """
        Create the introduction section of the article

        Args:
            outfit_id (str): The outfit ID
            outfit_data (dict): The complete outfit data dictionary
            sex_type (str): "Male", "Female", or "Both"

        Returns:
            str: Complete introduction section
        """
        # Get outfit display name for the intro
        outfit_name = get_outfit_display_name(outfit_id, page_dict)

        # Determine sex availability for intro
        male_exists = outfit_id in outfit_data.get("MaleOutfits", {})
        female_exists = outfit_id in outfit_data.get("FemaleOutfits", {})

        if male_exists and female_exists:
            sex_text = "male and female"
        elif male_exists:
            sex_text = "male"
        else:
            sex_text = "female"

        return f"\n'''{outfit_name}''' is a [[clothing]] [[outfit]] available for {sex_text} characters."

    def create_items(outfit_id, outfit_data, sex_type):
        """
        Create the items section of the article

        Args:
            outfit_id (str): The outfit ID
            outfit_data (dict): The complete outfit data dictionary
            sex_type (str): "Male", "Female", or "Both"

        Returns:
            str: Complete items section with tables for each sex
        """

        items_sections = []

        # Helper function to create a single items table
        def create_items_table(items_dict, guid, sex_label):
            """
            Create a wikitable for items with sub-items support

            Returns:
                dict: Contains 'table_only' (just the bot-flagged table) and
                      'full_section' (header + table for article)
            """
            if not items_dict:
                return None

            # Build the wikitable itself
            table_lines = []
            table_lines.append('{| class="wikitable theme-red sortable"')
            table_lines.append("! Item")
            table_lines.append("! Spawn Chance")
            table_lines.append("! Alternatives")

            # Track missing items for summary warning
            missing_items = []

            # Add items in the order they appear (maintaining GUID order)
            for item_name, item_data in items_dict.items():
                # Skip makeup items and ZedDmg items
                if item_name.startswith("MakeUp_") or item_name.startswith("ZedDmg_"):
                    continue

                probability = item_data.get("probability", 100)
                sub_items = item_data.get("subItems", {})

                # Try to map clothing item name to game item ID first
                game_item_id = clothing_to_item_mapping.get(item_name)
                if not game_item_id:
                    # Fallback to fix_item_id if not in clothing mapping
                    game_item_id = Item.fix_item_id(item_name)

                item = Item(game_item_id)

                if item.valid:
                    main_item_link = item.wiki_link
                else:
                    # Fallback to plain item name if not found
                    main_item_link = f"[[{item_name}]]"
                    missing_items.append(item_name)

                # Main item row
                table_lines.append("|-")
                table_lines.append(f"| {main_item_link}")
                table_lines.append(f"| {probability}%")

                # Alternatives column
                if sub_items:
                    # Filter out makeup items and ZedDmg items from sub_items
                    filtered_sub_items = {
                        k: v
                        for k, v in sub_items.items()
                        if not (k.startswith("MakeUp_") or k.startswith("ZedDmg_"))
                    }

                    if filtered_sub_items:
                        # Count total alternatives (primary + filtered sub-items)
                        total_count = 1 + len(filtered_sub_items)
                        alternatives_list = []

                        # Add primary item first
                        alternatives_list.append(f"{main_item_link} (1/{total_count})")

                        # Add all filtered sub-items
                        for sub_item_name in filtered_sub_items.keys():
                            # Try to map clothing item name to game item ID first
                            sub_game_item_id = clothing_to_item_mapping.get(
                                sub_item_name
                            )
                            if not sub_game_item_id:
                                # Fallback to fix_item_id if not in clothing mapping
                                sub_game_item_id = Item.fix_item_id(sub_item_name)

                            sub_item = Item(sub_game_item_id)

                            if sub_item.valid:
                                sub_item_link = sub_item.wiki_link
                            else:
                                # Fallback to plain item name if not found
                                sub_item_link = f"[[{sub_item_name}]]"
                                missing_items.append(sub_item_name)

                            alternatives_list.append(
                                f"{sub_item_link} (1/{total_count})"
                            )

                        # Join with line breaks
                        table_lines.append("| " + "<br>".join(alternatives_list))
                    else:
                        # All sub-items were makeup items (filtered out)
                        table_lines.append("| —")
                else:
                    # No alternatives
                    table_lines.append("| —")

            # Report missing items once at the end if any were found
            if missing_items:
                unique_missing = list(set(missing_items))
                echo.warning(
                    f"Outfit GUID {guid}: {len(unique_missing)} clothing items not found in parsed item data: {', '.join(unique_missing[:5])}{'...' if len(unique_missing) > 5 else ''}"
                )

            # Close table
            table_lines.append("|}")

            # Create the bot-flagged table (for individual files)
            table_only = (
                BOT_FLAG.format(type="items", id=f"items-{guid}")
                + "\n"
                + "\n".join(table_lines)
                + "\n"
                + BOT_FLAG_END.format(type="items", id=f"items-{guid}")
            )

            # Create the full section for the article (header + bot-flagged table)
            full_section_lines = []

            # Add sex-specific header if both sexes present
            if sex_type == "Both":
                full_section_lines.append(f"=== {sex_label} ===")

            # Add the bot-flagged table
            full_section_lines.append(table_only)

            return {
                "table_only": table_only,
                "full_section": "\n".join(full_section_lines),
            }

        # Check which sex variants exist
        male_exists = outfit_id in outfit_data.get("MaleOutfits", {})
        female_exists = outfit_id in outfit_data.get("FemaleOutfits", {})

        # Store table data for both article creation and individual file writing
        tables_data = {}

        # Create table for female outfit if it exists
        if female_exists:
            female_outfit = outfit_data["FemaleOutfits"][outfit_id]
            female_guid = female_outfit.get("GUID", "unknown")
            female_items = female_outfit.get("Items", {})
            female_table_data = create_items_table(female_items, female_guid, "Female")
            if female_table_data:
                items_sections.append(female_table_data["full_section"])
                tables_data["female"] = {
                    "guid": female_guid,
                    "table_only": female_table_data["table_only"],
                }

        # Create table for male outfit if it exists
        if male_exists:
            male_outfit = outfit_data["MaleOutfits"][outfit_id]
            male_guid = male_outfit.get("GUID", "unknown")
            male_items = male_outfit.get("Items", {})
            male_table_data = create_items_table(male_items, male_guid, "Male")
            if male_table_data:
                items_sections.append(male_table_data["full_section"])
                tables_data["male"] = {
                    "guid": male_guid,
                    "table_only": male_table_data["table_only"],
                }

        # Join all sections for the article
        if items_sections:
            # Add the explanation text once at the beginning
            explanation_text = (
                "The following table lists the items that can spawn as part of this outfit. "
                "When an item has alternatives listed, the game randomly selects one option from "
                "the primary item and all its alternatives with equal probability."
            )
            items_content = explanation_text + "\n\n" + "\n\n".join(items_sections)
        else:
            items_content = ""

        # Return both the article content and the individual table data
        return {"content": items_content, "tables_data": tables_data}

    def create_code(outfit_id, outfit_data):
        """
        Create the code section with outfit data

        Args:
            outfit_id (str): The outfit ID
            outfit_data (dict): The complete outfit data dictionary

        Returns:
            str: Complete code section
        """
        version = config_manager.get_version()
        code_sections = []

        # Check if male outfit exists
        if outfit_id in outfit_data.get("MaleOutfits", {}):
            male_outfit = outfit_data["MaleOutfits"][outfit_id]
            male_json = json.dumps({outfit_id: male_outfit}, indent=2)

            code_sections.append(f"""{{{{CodeSnip
  | lang = json
  | line = false
  | path = [[https://github.com/Vaileasys/pz-wiki_parser/]]
  | source = outfit_parser
  | retrieved = true
  | version = {version}
  | code =
{male_json}
}}}}""")

        # Check if female outfit exists
        if outfit_id in outfit_data.get("FemaleOutfits", {}):
            female_outfit = outfit_data["FemaleOutfits"][outfit_id]
            female_json = json.dumps({outfit_id: female_outfit}, indent=2)

            code_sections.append(f"""{{{{CodeSnip
  | lang = json
  | line = false
  | path = [[https://github.com/Vaileasys/pz-wiki_parser/]]
  | source = outfit_parser
  | retrieved = true
  | version = {version}
  | code =
{female_json}
}}}}""")

        # Combine all code sections in a CodeBox
        if code_sections:
            code_content = "\n".join(code_sections)
            return f"{{{{CodeBox|\n{code_content}\n}}}}"
        else:
            return "<!-- No outfit data available -->\n\n"

    def create_navigation(sex_type):
        """Create the navigation section of the article"""
        # Determine category based on sex type
        if sex_type == "Both":
            category = "Unisex outfits"
        elif sex_type == "Male":
            category = "Male outfits"
        elif sex_type == "Female":
            category = "Female outfits"
        else:
            category = "Outfits"  # fallback

        return f"""{{{{Navbox/sandbox|outfits}}}}

{{{{ll|Category:Outfits}}}}
{{{{ll|Category:{category}}}}}
"""

    # Get all unique outfit IDs from both male and female sections
    male_outfit_ids = set(outfit_data.get("MaleOutfits", {}).keys())
    female_outfit_ids = set(outfit_data.get("FemaleOutfits", {}).keys())
    all_outfit_ids = male_outfit_ids | female_outfit_ids

    echo.info(f"Processing {len(all_outfit_ids)} unique outfit IDs...")

    # Create output directories
    articles_dir = os.path.join(output_dir, "articles")
    infobox_dir = os.path.join(output_dir, "infobox")
    items_dir = os.path.join(output_dir, "items")
    code_dir = os.path.join(output_dir, "code")

    os.makedirs(articles_dir, exist_ok=True)
    os.makedirs(infobox_dir, exist_ok=True)
    os.makedirs(items_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)

    # Process each outfit ID with progress bar
    processed_count = 0

    # Create progress bar for outfit processing
    with tqdm(
        total=len(all_outfit_ids), desc="Processing outfits", unit="outfits"
    ) as pbar:
        for outfit_id in all_outfit_ids:
            # Check if outfit exists in both male and female sections
            male_exists = outfit_id in male_outfit_ids
            female_exists = outfit_id in female_outfit_ids

            if male_exists and female_exists:
                # Process as combined male/female outfit
                article_data = build_article(
                    outfit_id, outfit_data, "Both", story_outfits_data
                )
                sex_type = "Both"
            elif male_exists:
                # Process as male-only outfit
                article_data = build_article(
                    outfit_id, outfit_data, "Male", story_outfits_data
                )
                sex_type = "Male"
            elif female_exists:
                # Process as female-only outfit
                article_data = build_article(
                    outfit_id, outfit_data, "Female", story_outfits_data
                )
                sex_type = "Female"
            else:
                echo.warning(
                    f"Outfit ID '{outfit_id}' not found in either section - skipping"
                )
                pbar.update(1)  # Still update progress bar even for skipped outfits
                continue

            # Write complete article
            article_filename = f"{article_data['article_name']}.txt"
            article_path = os.path.join(articles_dir, article_filename)
            with open(article_path, "w", encoding="utf-8") as f:
                f.write(article_data["complete_article"])

            # Write individual sections
            infobox_path = os.path.join(
                infobox_dir, f"{article_data['article_name']}_infobox.txt"
            )
            with open(infobox_path, "w", encoding="utf-8") as f:
                f.write(article_data["infobox"])

            # Write items tables separately by GUID
            # Each sex variant gets its own file named by GUID (containing only bot-flagged table)
            items_tables = article_data.get("items_tables", {})

            # Write female items table if available
            if "female" in items_tables:
                female_guid = items_tables["female"]["guid"]
                female_table_only = items_tables["female"]["table_only"]
                female_items_path = os.path.join(items_dir, f"items_{female_guid}.txt")
                with open(female_items_path, "w", encoding="utf-8") as f:
                    f.write(female_table_only)

            # Write male items table if available
            if "male" in items_tables:
                male_guid = items_tables["male"]["guid"]
                male_table_only = items_tables["male"]["table_only"]
                male_items_path = os.path.join(items_dir, f"items_{male_guid}.txt")
                with open(male_items_path, "w", encoding="utf-8") as f:
                    f.write(male_table_only)

            code_path = os.path.join(
                code_dir, f"{article_data['article_name']}_code.txt"
            )
            with open(code_path, "w", encoding="utf-8") as f:
                f.write(article_data["code"])

            processed_count += 1
            pbar.set_postfix_str(f"Last: {article_data['article_name']} ({sex_type})")
            pbar.update(1)

    echo.success(f"Successfully processed {processed_count} outfits into articles")


def create_list(outfit_data, page_dict, output_dir):
    """
    Create an outfit list table with male/female images, links, and GUIDs

    Args:
        outfit_data (dict): Parsed outfit data from cache
        page_dict (dict): Page dictionary with items and outfits sections
        output_dir (str): Output directory path
    """
    echo.info("Creating outfit list...")

    # Get all pages that contain outfit data
    outfit_pages = {}

    # Check each page to see if it has outfit_id field (indicating it's an outfit page)
    for page_name, page_data in page_dict.items():
        if "outfit_id" in page_data:
            outfit_pages[page_name] = page_data

    if not outfit_pages:
        echo.warning("No outfit pages found in page dictionary")
        echo.info(f"Available keys in page_dict: {list(page_dict.keys())}")
        return

    # Build the table rows
    table_rows = []

    for page_name, page_data in outfit_pages.items():
        # Handle both single outfit_id and list of outfit_ids
        outfit_ids = page_data.get("outfit_id", [])
        if isinstance(outfit_ids, str):
            outfit_ids = [outfit_ids]

        # Process each outfit ID for this page
        for outfit_id in outfit_ids:
            # Get outfit display name
            display_name = get_outfit_display_name(outfit_id, page_dict)

            # Get GUIDs for male and female variants
            male_guid = None
            female_guid = None

            # Check male outfit
            if outfit_id in outfit_data.get("MaleOutfits", {}):
                male_outfit = outfit_data["MaleOutfits"][outfit_id]
                male_guid = male_outfit.get("GUID")

            # Check female outfit
            if outfit_id in outfit_data.get("FemaleOutfits", {}):
                female_outfit = outfit_data["FemaleOutfits"][outfit_id]
                female_guid = female_outfit.get("GUID")

            # Format male image
            male_image = (
                f"[[File:outfit_{outfit_id}_Male.png|100px]]<br>{outfit_id}"
                if male_guid
                else ""
            )

            # Format female image
            female_image = (
                f"[[File:outfit_{outfit_id}_Female.png|100px]]<br>{outfit_id}"
                if female_guid
                else ""
            )

            # Format link
            link = f"[[{display_name}]]"

            # Format GUIDs with labels if multiple
            guids = []
            if male_guid:
                guids.append(f"{male_guid} (male)")
            if female_guid:
                guids.append(f"{female_guid} (female)")

            guids_text = "<br>".join(guids) if guids else ""

            # Add table row
            table_rows.append(
                f"| {male_image} || {female_image} || {link} || {guids_text}"
            )

    if not table_rows:
        echo.warning("No outfit data found to create list")
        return

    # Build complete table
    table_content = (
        """<div style="overflow: auto; white-space: nowrap;">
{| class="wikitable theme-red sortable" style="text-align: center;"
|-
! Male image
! Female image
! Link
! GUIDs
|-
"""
        + "\n|-\n".join(table_rows)
        + "\n|}"
        + "\n</div>"
    )

    # Write to file
    list_file_path = os.path.join(output_dir, "outfits_list.txt")
    try:
        with open(list_file_path, "w", encoding="utf-8") as f:
            f.write(table_content)
        echo.success(f"Created outfit list: {list_file_path}")
    except Exception as e:
        echo.error(f"Failed to write outfit list: {e}")


def run_decompiler():
    """
    Ensure the ZomboidDecompiler has been run.
    If not, run it now.

    Returns:
        bool: True if decompiler output exists or was successfully created, False otherwise
    """
    decompiler_output = os.path.join(OUTPUT_DIR, "ZomboidDecompiler")
    if os.path.exists(decompiler_output) and os.path.isdir(decompiler_output):
        echo.success("ZomboidDecompiler output found. Skipping decompilation.")
        return True

    echo.info("ZomboidDecompiler output not found. Running decompiler...")

    # Check if Java is installed
    try:
        # Check for Java installation
        if platform.system() == "Windows":
            result = subprocess.run(
                ["java", "-version"],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            result = subprocess.run(
                ["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

        if result.returncode != 0:
            echo.error(
                "Error: Java is not installed or not in PATH. Cannot run decompiler."
            )
            return False
    except Exception as e:
        echo.error(f"Error checking Java installation: {e}")
        return False

    # Run the decompiler
    from scripts.core import runner

    result = runner.run_zomboid_decompiler()

    if result:
        echo.warning("Warning: Decompiler may not have completed successfully.")
        return False
    else:
        echo.success("Decompiler completed successfully.")
        return True


def main():
    echo.info("Starting outfits processing...")

    # Ensure decompiler has been run before proceeding
    if not run_decompiler():
        echo.error("Cannot continue without decompiler output.")
        echo.error("Please ensure Java is installed and the decompiler can run.")
        return False

    # Load cache
    cached_data, cache_version = cache.load_cache("outfits.json", get_version=True)

    if cache_version == Version.get():
        echo.info("Outfit cache is up to date")
        outfit_data = cached_data
    else:
        echo.info("Regenerating outfit cache...")
        outfit_parser.main()
        outfit_data, _ = cache.load_cache("outfits.json", get_version=True)

    echo.success(
        f"Loaded {len(outfit_data.get('FemaleOutfits', {}))} female outfits, {len(outfit_data.get('MaleOutfits', {}))} male outfits"
    )

    # Parse story files
    echo.info("Parsing story files for outfit references...")
    story_outfits_data = parse_story_outfits(outfit_data, force_regenerate=True)

    # Load page dictionary
    page_manager.init()
    page_dict = page_manager.get_flattened_page_dict()

    # Set output path
    output_dir = os.path.join("output", "en", "outfits")
    os.makedirs(output_dir, exist_ok=True)

    # Start processing
    create_articles(outfit_data, page_dict, output_dir, story_outfits_data)
    create_list(outfit_data, page_dict, output_dir)

    echo.success("Outfits processing completed")
