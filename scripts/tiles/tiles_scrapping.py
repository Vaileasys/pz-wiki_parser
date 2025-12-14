import os
from scripts.objects.item import Item
from scripts.utils import echo

def generate_scrapping_tables(tiles: dict, definitions: dict, lang_code: str) -> dict:
    """
    Generate scrapping and breakage tables for tiles in the specified language.

    Args:
        tiles (dict): Dictionary containing tile definitions and properties.
        definitions (dict): Dictionary containing scrapping and material definitions.
        lang_code (str): Language code for localization.

    Returns:
        dict: Dictionary containing generated scrapping and breakage information for each tile group.

    The function creates MediaWiki-formatted tables for both scrapping and breakage mechanics,
    saving them to separate files in the output directory.
    """
    base_dir = os.path.join('output', lang_code, 'tiles', 'crafting')
    os.makedirs(base_dir, exist_ok=True)

    scrappings = {}

    for group_name, variant_dict in tiles.items():
        safe_name = group_name.replace(' ', '_')
        first_tile = next(iter(variant_dict.values()))
        generic = first_tile.get('properties', {}).get('generic', {})
        can_scrap = 'CanScrap' in generic
        can_break = 'CanBreak' in generic

        group_entry = {}

        # Disassembly
        if can_scrap:
            content = _generate_disassembly_section(generic, definitions)
            group_entry['scrapping'] = content
            if content:
                file_path = os.path.join(base_dir, f"{safe_name}_scrapping.txt")
                try:
                    with open(file_path, 'w', encoding='utf-8') as out:
                        out.write(content)
                except Exception as e:
                    echo.error(f"Failed writing scrapping table for '{group_name}': {e}")

        # Breakage
        if can_break:
            content = _generate_breakage_section(generic, definitions)
            group_entry['breakage'] = content
            if content:
                file_path = os.path.join(base_dir, f"{safe_name}_breakage.txt")
                try:
                    with open(file_path, 'w', encoding='utf-8') as out:
                        out.write(content)
                except Exception as e:
                    echo.error(f"Failed writing breakage table for '{group_name}': {e}")

        scrappings[group_name] = group_entry

    return scrappings


def _generate_disassembly_section(generic: dict, definitions: dict) -> str:
    """
    Generate a MediaWiki table for disassembly (scrapping) information.

    Args:
        generic (dict): Generic properties of the tile containing material information.
        definitions (dict): Dictionary containing scrap item definitions and rules.

    Returns:
        str: MediaWiki-formatted table showing disassembly materials, chances, and quantities.
        Returns empty string if no materials are defined.
    """
    scrap_items = definitions.get('scrap_items', [])
    scrap_defs = definitions.get('scrap_definitions', {})

    materials = [generic.get(k) for k in ('Material','Material2','Material3') if generic.get(k)]
    if not materials:
        return ""

    intro_note   = "Base chance is not a percentage, but can provide a basic idea of rarity."
    header_title = "Disassembly materials"
    col_material = "Material"
    col_tries    = "Amount of tries"
    col_chance   = "Base chance"
    col_max      = "Maximum amount"
    on_fail      = "On dismantle failure"

    lines = [
        '{| class="wikitable theme-red"',
        f'|+ {intro_note}',
        '|-',
        f'! colspan="4" | {header_title}',
        '|-',
        f'! {col_material}',
        f'! {col_tries}',
        f'! {col_chance}',
        f'! {col_max}',
    ]

    for mat in materials:
        for entry in scrap_items:
            if entry.get('material') == mat:
                item_id = entry.get('returnItem', '')
                tries  = entry.get('maxAmount', '')
                chance = entry.get('chancePerRoll', '')
                max_a  = entry.get('maxAmount', '')
                
                item = Item(item_id)
                icon = item.icon
                page_link = item.wiki_link

                lines += [
                    '|-',
                    f'| {icon} {page_link}',
                    f'| {tries}',
                    f'| {chance}',
                    f'| {max_a}',
                ]

    # failure
    unusables = []
    for mat in materials:
        sd = scrap_defs.get(mat, {})
        ui = sd.get('unusableItem')
        if ui:
            keys = ui.keys() if isinstance(ui, dict) else [ui]
            for item_id in keys:
                item = Item(item_id)
                icon = item.icon
                page_link    = item.wiki_link
                unusables.append(f"{icon} {page_link}")

    if unusables:
        lines.append('|-')
        lines.append(f'! colspan="4" | {on_fail}')
        for link in unusables:
            lines += ['|-', f'| colspan="4" | {link}']

    lines.append('|}')
    return "\n".join(lines) + "\n\n"


def _generate_breakage_section(generic: dict, definitions: dict) -> str:
    """
    Generate a MediaWiki table for breakage (destruction) information.

    Args:
        generic (dict): Generic properties of the tile containing material information.
        definitions (dict): Dictionary containing material definitions for breakage.

    Returns:
        str: MediaWiki-formatted table showing breakage materials, chances, and quantities.
        Returns empty string if no materials are defined.
    """
    material_defs = definitions.get('material_definitions', {})

    materials = [generic.get(k) for k in ('Material','Material2','Material3') if generic.get(k)]
    if not materials:
        return ""

    header_title = "Breakage materials"
    col_item     = "Item dropped"
    col_max      = "Maximum amount"
    col_chance   = "Chance per roll"

    lines = [
        '{| class="wikitable theme-red sortable"',
        '|-',
        f'! colspan="3" | {header_title}',
        '|-',
        f'! {col_item}',
        f'! {col_max}',
        f'! {col_chance}',
    ]

    for mat in materials:
        items = material_defs.get(mat, [])
        for entry in items:
            item_id = entry.get('returnItem', '')
            max_a  = entry.get('maxAmount', '')
            chance = entry.get('chancePerRoll', '')
            item = Item(item_id)
            page_link = item.wiki_link
            icon = item.icon

            lines += [
                '|-',
                f'| {icon} {page_link}',
                f'| {max_a}',
                f'| {chance}',
            ]

    lines.append('|}')
    return "\n".join(lines) + "\n"
