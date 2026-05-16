"""
Generates wiki-formatted outfit article output.

Builds outfit pages from Outfit data, including infoboxes, overviews, item tables, 
code sections, and navigation. Story and zone spawn data are pulled from
OutfitStory and OutfitZone, while list output is handled separately.
"""

import json
import os
import platform
import re
import subprocess
from tqdm import tqdm

from scripts.core.version import Version
from scripts.core.constants import OUTPUT_DIR, BOT_FLAG, BOT_FLAG_END
from scripts.core.file_loading import write_file
from scripts.utils import echo
from scripts.objects.item import Item
from scripts.objects.outfit import Outfit
from scripts.objects.outfit_story import OutfitStory
from scripts.objects.outfit_zone import OutfitZone
from scripts.lists import outfit_list

ARTICLE_DIR = os.path.join("outfits", "articles")
INFOBOX_DIR = os.path.join("outfits", "infobox")
ITEMS_DIR = os.path.join("outfits", "items")
CODE_DIR = os.path.join("outfits", "code")

# Cache for clothing name to game item ID mapping
_clothing_name_cache = None

# =============================================================================
# Data helpers
# =============================================================================

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

# =============================================================================
# Formatting helpers
# =============================================================================

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

# =============================================================================
# Spawn lookup
# =============================================================================

def process_stories(outfit_id: str) -> list[str]:
    """
    Process story-related spawn locations for the outfit

    Args:
        outfit_id (str): The outfit ID

    Returns:
        str: Story-related spawn information
    """
    outfit_stories = OutfitStory.get(outfit_id)

    if not outfit_stories:
        return []

    story_lines = []
    all_story_ids = set()
    story_type_map = {}

    # Group stories by type and collect unique story IDs
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

    return story_lines

def process_zones(outfit_id: str) -> list[str]:
    """
    Process zone-related spawn locations for the outfit

    Args:
        outfit_id (str): The outfit ID

    Returns:
        list[str]: Zone-related spawn information
    """
    zones = OutfitZone.get(outfit_id)

    if not zones:
        return []

    lines = [
        '{| class="wikitable theme-red sortable"',
        "! Spawn Zone",
        "! Chance",
    ]
    
    for zone_data in zones:
        zone_name = zone_data["zone_name"]
        outfit_info = zone_data["outfit_info"]

        # Format spawn zone as a link
        spawn_zone_link = f"[https://b42map.com/?zombie={zone_name} {zone_name}]"

        chance = "Unknown"

        # Format chance information
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

        # Build table with found zones
        lines.append("|-")
        lines.append(f"| {spawn_zone_link}")
        lines.append(f"| {chance}")

    lines.append("|}")
    return lines

# =============================================================================
# Article section builders
# =============================================================================

def create_header():
    """Create the header section of the article"""
    version = Version.get()
    return [
        "{{LangSwitch}}",
        "{{Navbar lore}}",
        f"{{{{Page version|{version}}}}}"
        ]

def create_infobox(outfit: Outfit):
    """
    Create the infobox section for a specific outfit

    Args:
        outfit (Outfit): The outfit object

    Returns:
        str: Complete infobox template
    """
    outfit_name = outfit.outfit_id

    # Determine sex exclusivity based on outfit data
    if outfit.sex == "Both":
        sex_exclusivity = "Male and Female"
    elif outfit.sex == "Male":
        sex_exclusivity = "Male exclusive"
    elif outfit.sex == "Female":
        sex_exclusivity = "Female exclusive"
    else:
        sex_exclusivity = ""

    # Build infobox
    lines = [
        "{{Infobox outfit",
        f"|name={outfit_name}",
    ]

    # Handle image parameters based on sex availability
    if outfit.has_male and outfit.has_female:
        # Both sexes - need image and image2
        lines.append(f"|image=outfit_{outfit.outfit_id}_Male.png")
        lines.append(f"|image2=outfit_{outfit.outfit_id}_Female.png")
    else:
        # Single sex - use appropriate image
        if outfit.has_male:
            lines.append(f"|image=outfit_{outfit.outfit_id}_Male.png")
        elif outfit.has_female:
            lines.append(f"|image=outfit_{outfit.outfit_id}_Female.png")

    lines.extend(
        [
            f"|sex={sex_exclusivity}",
            f"|outfit_id={outfit.outfit_id}",
        ]
    )

    # Add GUID parameters
    for i, guid in enumerate(outfit.guids):
        if i == 0:
            lines.append(f"|guid={guid}")
        else:
            lines.append(f"|guid{i + 1}={guid}")

    lines.append("}}")
    return lines

def create_intro(outfit: Outfit):
    """
    Create the introduction section of the article

    Args:
        outfit (Outfit): The outfit object

    Returns:
        str: Complete introduction section
    """
    # Get outfit sex for the intro
    if outfit.sex == "Both":
        sex_text = "male and female"
    elif outfit.sex == "Male":
        sex_text = "male"
    else:
        sex_text = "female"

    return [f"'''{outfit.outfit_id}''' is a [[clothing]] [[outfit]] available for {sex_text} characters."]

def create_overview(outfit: Outfit) -> list[str]:
    """
    Create the overview section of the article

    Args:
        outfit (Outfit): The outfit object

    Returns:
        dict: Contains 'content' (for article) and 'bot_flagged' (for individual files)
    """

    # Process spawn locations using the nested functions
    stories_info = process_stories(outfit.outfit_id)
    zones_info = process_zones(outfit.outfit_id)

    # Determine what sections to include based on available data
    has_stories = bool(stories_info)
    has_zones = bool(zones_info)

    # Default case: no stories, no zones
    if not has_stories and not has_zones:
        return ["It does not spawn in any [[randomized stories]] or zombie zones."]
    
    # Stories only case
    if has_stories and not has_zones:
        return ["It spawns in the following [[randomized stories]]:", *stories_info]
    
    # Zones only case
    if not has_stories and has_zones:
        return ["It spawns in the following zombie zones:", *zones_info]
    
    # Both stories and zones case
    return [
        "It spawns in the following [[randomized stories]]:",
        *stories_info,
        "",
        "It spawns in the following zombie zones:",
        *zones_info,
    ]

def create_items(outfit: Outfit, clothing_to_item_mapping: dict) -> dict:
    """
    Create the items section of the article

    Args:
        outfit (Outfit): The outfit object
        clothing_to_item_mapping (dict): Mapping of clothing item names to game item IDs
    Returns:
        dict: Contains 'content' (complete items section) and 'tables_data' (individual table data)
    """

    items_sections = []

    # Store table data for both article creation and individual file writing
    tables_data = {}

    # Create table for female outfit if it exists
    if outfit.has_female:
        female_guid = outfit.female_guid or "unknown"
        
        female_table_data = create_items_table(
            outfit,
            outfit.female_items,
            female_guid,
            "Female",
            clothing_to_item_mapping,
        )

        if female_table_data:
            items_sections.extend(female_table_data["full_section"])
            tables_data["female"] = {
                "guid": female_guid,
                "table_only": female_table_data["table_only"],
            }

    # Create table for male outfit if it exists
    if outfit.has_male:
        male_guid = outfit.male_guid or "unknown"
        
        male_table_data = create_items_table(
            outfit,
            outfit.male_items,
            male_guid,
            "Male",
            clothing_to_item_mapping,
        )

        if male_table_data:
            if items_sections:
                items_sections.append("")

            items_sections.extend(male_table_data["full_section"])
            tables_data["male"] = {
                "guid": male_guid,
                "table_only": male_table_data["table_only"],
            }

    # Join all sections for the article
    if items_sections:
        # Add the explanation text once at the beginning
        content = [
            "The following table lists the items that can spawn as part of this outfit. "
            "When an item has alternatives listed, the game randomly selects one option from "
            "the primary item and all its alternatives with equal probability.",
            "",
            *items_sections,
        ]
    else:
        content = []

    # Return both the article content and the individual table data
    return {"content": content, "tables_data": tables_data}

def create_items_table(
    outfit: Outfit,
    items_dict: dict,
    guid: str,
    sex_label: str,
    clothing_to_item_mapping: dict,
) -> dict[str, list[str]] | None:
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
    table_only = [
        BOT_FLAG.format(type="items", id=f"items-{guid}"),
        *table_lines,
        BOT_FLAG_END.format(type="items", id=f"items-{guid}"),
    ]

    # Create the full section for the article (header + bot-flagged table)
    full_section_lines = []

    # Add sex-specific header if both sexes present
    if outfit.sex == "Both":
        full_section_lines.append(f"=== {sex_label} ===")

    # Add the bot-flagged table
    full_section_lines.extend(table_only)

    return {
        "table_only": table_only,
        "full_section": full_section_lines,
    }

def create_code(outfit: Outfit):
    """
    Create the code section with outfit data

    Args:
        outfit (Outfit): The outfit object

    Returns:
        str: Complete code section
    """
    version = Version.get()
    code_sections = []

    # Check if male outfit exists
    if outfit.has_male:
        male_json = json.dumps({outfit.outfit_id: outfit.male_data}, indent=2)

        code_sections.extend([
            "{{CodeSnip",
            "  | lang = json",
            "  | line = false",
            "  | path = [[https://github.com/Vaileasys/pz-wiki_parser/]]",
            "  | source = outfit_parser",
            "  | retrieved = true",
            f"  | version = {version}",
            "  | code =",
            *male_json.splitlines(),
            "}}",
        ])
        

    # Check if female outfit exists
    if outfit.has_female:
        female_json = json.dumps({outfit.outfit_id: outfit.female_data}, indent=2)

        code_sections.extend([
            "{{CodeSnip",
            "  | lang = json",
            "  | line = false",
            "  | path = [[https://github.com/Vaileasys/pz-wiki_parser/]]",
            "  | source = outfit_parser",
            "  | retrieved = true",
            f"  | version = {version}",
            "  | code =",
            *female_json.splitlines(),
            "}}",
        ])

    
    if not code_sections:
        return ["<!-- No outfit data available -->"]

    # Combine all code sections in a CodeBox
    return [
        "{{CodeBox|",
        *code_sections,
        "}}",
    ]

def create_navigation(sex_type: str) -> list[str]:
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

    return [
        "{{Navbox/sandbox|outfits}}",
        "",
        "{{ll|Category:Outfits}}",
        f"{{{{ll|Category:{category}}}}}",
    ]

# =============================================================================
# Article assembly
# =============================================================================

def build_article(outfit: Outfit, clothing_to_item_mapping: dict) -> dict:
    """
    Build a complete article for a specific outfit

    Args:
        outfit (Outfit): The outfit object
        clothing_to_item_mapping (dict): Mapping of clothing item names to game item IDs

    Returns:
        dict: Dictionary containing all sections and the complete article
    """
    # Get outfit name for file naming
    outfit_name = outfit.page

    # Build each section
    header_section = create_header()
    infobox_section = create_infobox(outfit)
    intro_section = create_intro(outfit)
    overview_section = create_overview(outfit)
    items_data = create_items(outfit, clothing_to_item_mapping)
    code_section = create_code(outfit)
    navigation_section = create_navigation(outfit.sex)

    # Combine all sections into complete article with proper formatting
    complete_article = [
        *header_section,
        *infobox_section,
        *intro_section,
        "",
        "== Overview ==",
        *overview_section,
    ]

    # Only add Items section if there is item data
    if items_data["content"]:
        complete_article.extend([
            "",
            "== Items ==",
            *items_data["content"],
        ])

    complete_article.extend([
        "",
        "== Code ==",
        *code_section,
        "",
        "== Navigation ==",
        *navigation_section,
    ])

    # Return all sections and complete article
    return {
        "article_name": outfit_name,
        "complete_article": complete_article,
        "infobox": infobox_section,
        "overview_content": overview_section,
        "items_content": items_data["content"],
        "items_tables": items_data["tables_data"],
        "code": code_section,
    }

# =============================================================================
# Output
# =============================================================================

def write_article_files(article_data: dict):
    article_name = article_data["article_name"]

    write_file(
        article_data["complete_article"],
        rel_path=os.path.join(ARTICLE_DIR, f"{article_name}.txt"),
    )

    write_file(
        article_data["infobox"],
        rel_path=os.path.join(INFOBOX_DIR, f"{article_name}_infobox.txt"),
    )

    items_tables = article_data.get("items_tables", {})

    if "female" in items_tables:
        female_guid = items_tables["female"]["guid"]

        write_file(
            items_tables["female"]["table_only"],
            rel_path=os.path.join(ITEMS_DIR, f"items_{female_guid}.txt"),
        )

    if "male" in items_tables:
        male_guid = items_tables["male"]["guid"]

        write_file(
            items_tables["male"]["table_only"],
            rel_path=os.path.join(ITEMS_DIR, f"items_{male_guid}.txt"),
        )

    write_file(
        article_data["code"],
        rel_path=os.path.join(CODE_DIR, f"{article_name}_code.txt"),
    )

def create_articles():
    """
    Create outfit articles using nested functions to build each section
    """
    echo.info("Creating outfit articles...")

    # Build reverse mapping: clothing item name -> game item ID
    echo.info("Building clothing item name to game item ID mapping...")
    clothing_to_item_mapping = _build_clothing_name_mapping()
    echo.success(f"Mapped {len(clothing_to_item_mapping)} clothing items to game items")

    # Get all unique outfit IDs from both male and female sections
    outfits = list(Outfit.values())

    echo.info(f"Processing {len(outfits)} unique outfit IDs...")

    # Process each outfit ID with progress bar
    processed_count = 0

    # Create progress bar for outfit processing
    with tqdm(total=len(outfits), desc="Processing outfits", unit="outfits") as pbar:
        for outfit in outfits:
            if not outfit.valid:
                echo.warning(f"Outfit ID '{outfit.outfit_id}' not found in either section - skipping")
                pbar.update(1)
                continue

            article_data = build_article(outfit, clothing_to_item_mapping)
            write_article_files(article_data)

            processed_count += 1
            pbar.set_postfix_str(f"Last: {article_data['article_name']} ({outfit.sex})")
            pbar.update(1)

    echo.success(f"Successfully processed {processed_count} outfits into articles")

# =============================================================================
# Processing entry point
# =============================================================================

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
    
    Outfit.load()

    # Parse story files
    echo.info("Parsing story files for outfit references...")
    OutfitStory.load(force=True)

    # Start processing
    create_articles()
    outfit_list.generate()

    echo.success("Outfits processing completed")

if __name__ == "__main__":
    main()