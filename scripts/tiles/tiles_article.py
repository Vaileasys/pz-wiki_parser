"""
Project Zomboid Wiki Article Generator

This script generates complete wiki articles for Project Zomboid tiles. It combines
various components including infoboxes, usage information, code snippets, and navigation
elements to create comprehensive wiki pages for each tile type.

The script handles:
- Article structure and formatting
- Usage descriptions based on tile properties
- Dismantling and breakage information
- Code snippet integration
- Navigation elements
"""

import os
from scripts.core.language import Language
from scripts.core.version import Version

def process_usage(tile_name, tile_data, scrappings):
    """
    Build the 'Usage' section for a tile article.

    Args:
        tile_name (str): Name of the tile group.
        tile_data (dict): Dictionary containing tile properties and variants.
        scrappings (dict): Dictionary containing dismantling and breakage information.

    Returns:
        str: Formatted wiki markup for the Usage section, including property-based
             descriptions and dismantling/breakage information.
    """
    usage_intro = "==Usage==\n"

    # Property‐based usage
    first_info = next(iter(tile_data.values()), {})
    generic = first_info.get('properties', {}).get('generic', {})
    container = generic.get('container', '').lower()
    capacity = generic.get('ContainerCapacity', '')
    freezer_capacity = generic.get('FreezerCapacity', '')
    bed_type = generic.get('BedType', '')
    custom_item = generic.get('CustomItem', '')

    bed_quality_map = {
        "badBed": "Bad",
        "averageBed": "Average",
        "goodBed": "Good",
    }
    bed_quality = bed_quality_map.get(bed_type, "")

    sentences = []

    if container in ("stove", "microwave"):
        sentences.append(
            f"This tile can be used as a [[heat source]] to cook [[food]] or use [[electricity|power]] to operate. "
            f"It has a capacity of {capacity}."
        )
    elif container in ("woodstove", "barbecue"):
        sentences.append(
            f"This tile can be used as a [[heat source]] to cook [[food]]. "
            f"It requires [[fuel]] to work. It has a capacity of {capacity}."
        )
    elif container == "clothingwasher":
        sentences.append(
            f"This tile can be used to wash [[clothing]]. It has a capacity of {capacity}."
        )
    elif container == "clothingdryerbasic":
        sentences.append(
            f"This tile can be used to dry wet [[clothing]]. It has a capacity of {capacity}."
        )
    elif container in (
        "crate", "medicine", "counter", "shelves", "metal_shelves", "wardrobe",
        "sidetable", "dresser", "desk", "filingcabinet", "displaycasebakery",
        "bin", "cashregister", "vendingsnack", "vendingpop", "clothingrack",
        "displaycasebutcher", "grocerstand", "displaycase", "smallcrate",
        "smallbox", "overhead", "postbox", "corn", "locker", "dishescabinet",
        "restaurantdisplay", "toolcabinet", "militarycrate", "militarylocker"
    ):
        if capacity and capacity not in ("0", "-", "unknown"):
            sentences.append(
                f"This tile can be used to store [[item]]s. It has a capacity of {capacity}."
            )
    elif container == "fridge":
        sentences.append(
            f"This fridge can slow down the process of [[food]] rotting. "
            f"It has a storage capacity of {capacity} and a freezer capacity of {freezer_capacity}."
        )

    if bed_type:
        sentences.append(
            f"This tile can be used as a bed to [[sleep]] on. It has a quality of {bed_quality.lower()}."
        )

    if custom_item and custom_item not in ("-", ""):
        # use original custom_item name directly
        item_id = custom_item[5:] if custom_item.startswith("Base.") else custom_item
        sentences.append(
            f"This tile uses the custom item {{{{ll|{item_id}}}}} when picked up."
        )
    else:
        sentences.append(
            "This tile uses the generic movable item when picked up."
        )

    # Dismantling and breakage
    entry = scrappings.get(tile_name, {})
    dismantle = entry.get('scrapping', '').strip()
    breakage = entry.get('breakage', '').strip()

    # Assemble Usage
    usage = usage_intro
    if sentences:
        usage += "\n".join(sentences) + "\n"
    if dismantle:
        usage += "\n===Dismantling===\n" + dismantle + "\n"
    if breakage:
        usage += "\n===Breakage===\n" + breakage + "\n"

    return usage

def process_codesnip(tile_data, codesnips):
    """
    Create a CodeBox section containing all CodeSnip templates for a tile group.

    Args:
        tile_data (dict): Dictionary of sprite names and their data.
        codesnips (dict): Dictionary mapping sprite names to their CodeSnip markup.

    Returns:
        str: Formatted wiki markup for the Code section containing all relevant
             CodeSnip templates wrapped in a CodeBox.
    """
    snippets = []
    for sprite_name in tile_data.keys():
        snip = codesnips.get(sprite_name, "").rstrip("\n")
        if snip:
            snippets.append(snip)
    if not snippets:
        return ""
    box = "{{CodeBox|\n" + "\n".join(snippets) + "\n}}"
    return "==Code==\n" + box

def assemble_article(header, infobox, intro, usage, codesnip, navigation):
    """
    Combine all article sections into a complete wiki article.

    Args:
        header (str): Article header with metadata templates.
        infobox (str): Infobox template markup.
        intro (str): Article introduction paragraph.
        usage (str): Usage section markup.
        codesnip (str): Code section markup.
        navigation (str): Navigation template markup.

    Returns:
        str: Complete wiki article text with all sections properly formatted.
    """
    sections = [
        header,
        infobox,
        intro,
        usage,
        codesnip,
        navigation
    ]

    sections = [s for s in sections if s.strip()]
    return "\n".join(sections)

def sanitize_filename(name):
    """
    Convert a string into a safe filesystem filename.

    Args:
        name (str): Original string to convert.

    Returns:
        str: Sanitized string safe for use as a filename, with special characters
             replaced by underscores and spaces converted to underscores.
    """
    safe = []
    for ch in name:
        if ch.isalnum() or ch in (" ", "_", "-"):
            safe.append(ch)
        else:
            safe.append("_")
    fn = "".join(safe).strip().replace(" ", "_")
    return fn.lower()

def generate_tile_articles(tiles_data, infoboxes, codesnips, scrappings):
    """
    Generate and save wiki articles for all tile groups.

    Args:
        tiles_data (dict): Dictionary containing all tile group data.
        infoboxes (dict): Dictionary mapping tile names to their infobox markup.
        codesnips (dict): Dictionary mapping sprite names to their CodeSnip markup.
        scrappings (dict): Dictionary containing dismantling and breakage information.

    The function generates complete wiki articles by combining various components
    and saves them to individual files in the output directory structure.
    Each article includes metadata, infobox, introduction, usage information,
    code snippets, and navigation elements.
    """
    articles = {}
    version = Version.get()
    for tile_name, tile_data in tiles_data.items():
        header = f"{{{{Header|Tiles}}}}\n{{{{Page version|{version}}}}}\n{{{{Autogenerated|B42 tiles}}}}"
        infobox = infoboxes.get(tile_name, "")

        # Intro logic
        if tile_name.lower().endswith('s'):
            # plural
            display_name = tile_name.capitalize()
            intro = f"'''{display_name}''' are a [[tile]] in [[Project Zomboid]].\n"
        else:
            # singular
            first_char = tile_name[0] if tile_name else ''
            article_word = 'An' if first_char.lower() in 'aeiou' else 'A'
            intro = f"{article_word} '''{tile_name.lower()}''' is a [[tile]] in [[Project Zomboid]].\n"

        usage = process_usage(tile_name, tile_data, scrappings)
        codesnip = process_codesnip(tile_data, codesnips)
        navigation = "\n==Navigation==\n{{Navbox tiles}}"

        article = assemble_article(
            header,
            infobox,
            intro,
            usage,
            codesnip,
            navigation
        )
        articles[tile_name] = article

    lang_code = Language.get()
    out_dir   = os.path.join("output", lang_code, "tiles", "articles")
    os.makedirs(out_dir, exist_ok=True)

    for tile_name, content in articles.items():
        safe = sanitize_filename(tile_name)
        path = os.path.join(out_dir, f"{safe}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
