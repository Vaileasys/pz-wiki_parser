"""
Generates wiki-formatted tables for Project Zomboid.

This module loads item data, builds structured tables with translations and formatting,
and writes them as individual or combined output files for use on the PZwiki.
"""
import os
from pathlib import Path
from scripts.core.language import Translate
from scripts.core.constants import ITEM_DIR, BOT_FLAG, BOT_FLAG_END
from scripts.core.cache import load_json
from scripts.utils import echo
from scripts.core.file_loading import write_file

DEF_TABLE_HEADER = '{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"'
DEF_TABLE_FOOTER = '|}'
TABLE_WRAP_BEFORE = '<div class="scroll-x">\n'
TABLE_WRAP_AFTER = '\n</div>'


def get_table_data(path:str, extra_keys:str|list=None):
    """
    Loads table data and optionally extracts extra keys from the JSON file.

    Args:
        path (str): Path to the JSON file.
        extra_keys (str | list, optional): Single key or list of keys to extract additional data.

    Returns:
        tuple: (map, headings[, extra_data]) depending on whether extra_keys is provided.
    """
    data = load_json(path)
    map = data.get("map")
    headings = data.get("headings")

    if extra_keys:
        is_list = True
        if isinstance(extra_keys, str):
            is_list = False
            extra_keys = [extra_keys]
        else:
            extra_data = {}
        for key in extra_keys:
            value = data.get(key)
            if is_list:
                extra_data[key] = value
            else:
                extra_data = value
                break
        return map, headings, extra_data

    return map, headings


def get_column_headings(table_type:str, table_map:dict, columns:dict):
    """
    Builds the list of column headings for a given table type.

    Args:
        table_type (str): Table type to look up.
        table_map (dict): Mapping of table types to their column keys.
        columns (dict): Translated heading strings by key.

    Returns:
        list[str]: Formatted wiki heading strings.
    """
    column_def = table_map.get(table_type) or table_map.get("default")

    if column_def is None:
        echo.warning(f"No mapping for table type: '{table_type}'")
        return []

    if isinstance(column_def, list):
        return [columns.get(key, f'! {key}') for key in column_def]
    elif isinstance(column_def, dict):
        return generate_column_headings(column_def, columns)
    else:
        echo.warning(f"Invalid column definition type for '{table_type}'")
        return []


def generate_column_headings(column_def: dict, headings: dict) -> list:
    """
    Generates multi-row wiki headings from a nested column definition.

    Supports attributes like 'style' and 'class' on child headings,
    as well as colspan/rowspan for structured table layouts.

    Args:
        column_def (dict): Column layout with optional attributes and nesting.
        headings (dict): Mapping of keys to translated headings.

    Returns:
        list[str]: Formatted wiki markup for table headers.
    """
    top_row = []
    sub_row = []

    for key, val in column_def.items():
        if "parent" not in val:
            heading = headings.get(key, f'! {key}')
            colspan = val.get("colspan", 1)
            rowspan = val.get("rowspan", 1)

            if "children" in val:
                top_row.append(f'! colspan={colspan} | {heading.lstrip("! ").strip()}')

                for child in val["children"]:
                    child_val = column_def.get(child, {})
                    attr_parts = []

                    for attr_key in ("class", "style"):
                        if attr_key in child_val:
                            attr_parts.append(f'{attr_key}="{child_val[attr_key]}"')

                    attr_str = " ".join(attr_parts)
                    sub_heading = headings.get(child, f'! {child}')
                    if attr_str:
                        sub_row.append(f'! {attr_str} | {sub_heading.lstrip("! ").strip()}')
                    else:
                        sub_row.append(sub_heading)

            else:
                top_row.append(f'! rowspan={rowspan} | {heading.lstrip("! ").strip()}')

    result = top_row.copy()
    if sub_row:
        result.append("|-")
        result.extend(sub_row)

    return result


def generate_table(
        table_type: str,
        data: dict,
        column_headings: list,
        table_header: str = DEF_TABLE_HEADER,
        table_footer: str = DEF_TABLE_FOOTER,
        caption_top: str = None,
        caption_bottom: str = None,
        caption: str = None,
        table_before: str = None,
        table_after: str = None,
        do_bot_flag: bool = True,
        bot_flag_type: str = "table",
        do_horizontal_scroll: bool = True
        ) -> list:
    """
    Generates a full wiki-formatted table for the given data and headings.

    Args:
        table_type (str): Used in comments and IDs.
        data (dict): List of dicts representing table rows.
        column_headings (list): Header rows for the table.
        table_header (str): Starting wiki markup for the table.
        table_footer (str): Closing wiki markup.
        caption_top (str): Optional caption shown above the table.
        caption_bottom (str): Optional caption shown below the table.
        caption (str): Optional centered caption (overrides top/bottom).
        table_before (str): Content before the table.
        table_after (str): Content after the table.
        do_bot_flag (bool): Whether to include bot flag markers.
        bot_flag_type (str): Type used in bot flag comment.
        do_horizontal_scroll (bool): Wraps table in a scrollable container.

    Returns:
        list[str]: The full table as a list of wiki lines.
    """
    
    content = []

    table_wrap_before = TABLE_WRAP_BEFORE if do_horizontal_scroll else ""
    table_after_after = TABLE_WRAP_AFTER if do_horizontal_scroll else ""

    table_before = "" if table_before is None else table_before
    table_after = "" if table_after is None else table_after

    bot_flag_start = BOT_FLAG.format(type=bot_flag_type, id=table_type.replace(" ", "_")) if do_bot_flag else ''
    bot_flag_end = BOT_FLAG_END.format(type=bot_flag_type, id=table_type.replace(" ", "_")) if do_bot_flag else ''

    content.append(bot_flag_start + table_wrap_before + table_before + table_header)

    if caption_top and not caption:
        content.append(f'|+ style="caption-side:top; font-weight:normal; | {caption_top}', '|-')
    
    if caption:
        content.append('|+ ' + caption)

    content.extend(column_headings)

    for item in data:
        item_content = []
        item_content.append("|-")
        for value in list(item.values()):
            item_content.append(f"| {value}")
        
        content.extend(item_content)

    if caption_bottom and not caption_top and not caption:
        content.extend(['|-', f'|+ style="caption-side:bottom; font-weight:normal; border: none;" | <div style="text-wrap: white-space: nowrap; overflow: auto;"><div style="white-space: normal; display: inline-block;">{caption_bottom}</div></div>'])
    
    content.append(table_footer + table_after + table_after_after + bot_flag_end)

    # Get translations
    content = [Translate.get_wiki(value) for value in content]

    return content


def process_notes(data_list):
    """
    Extracts notes from the first entry in a data list, if present.

    Args:
        data_list (list): List of data dictionaries.

    Returns:
        tuple: (caption str, remaining data list)
    """
    if data_list and isinstance(data_list[0], dict) and "notes" in data_list[0]:
        notes = data_list[0]["notes"]
        data = data_list[1:]
    else:
        notes = []
        data = data_list

    caption = "<br>".join(notes)

    return caption, data


def create_tables(
        item_type: str,
        all_data: dict,
        columns: dict,
        table_map: dict = {},
        table_header = DEF_TABLE_HEADER,
        table_footer = DEF_TABLE_FOOTER,
        caption = None,
        caption_top = None,
        caption_bottom = None,
        combine_tables: bool = True,
        root_path: str = os.path.join(ITEM_DIR, "lists"),
        do_bot_flag: bool = True,
        bot_flag_type: str = "table",
        suppress: bool = False
        ):
    """
    Creates and writes individual and/or combined item tables for each table type.

    Args:
        item_type (str): The main category name for grouping the output.
        all_data (dict[str, list]): A dictionary mapping table types to lists of item data.
        columns (dict[str, str]): A mapping of column keys to translated heading strings.
        table_map (dict[str, list[str]]): A mapping of table types to their expected column keys. Defaults to empty dictionary.
        table_header (str): Custom table header to use. Defaults to DEF_TABLE_HEADER.
        table_footer (str): Custom table footer to use. Defaults to DEF_TABLE_FOOTER.
        caption (str | None): A shared table caption (centered, overrides caption_top and caption_bottom).
        caption_top (str | None): Caption to appear above the table.
        caption_bottom (str | None): Caption to appear below the table if no top or center caption is set.
        combine_tables (bool): If True, combines all tables into one file. Defaults to True.
        root_path (str): Root path where files will be written. `{language_code}` will be formatted to the current language code.
        do_bot_flag (bool): Whether to add the bot flag comment to the output. Defaults to True.
        bot_flag_type (str): The identifier used in bot flag comments. Defaults to "table".
        suppress (bool): If True, suppresses terminal output except for final success message.

    Returns:
        None
    """

    all_tables = []
    for table_type, data in sorted(all_data.items()):

        content = []

        # Reset captions per table
        local_caption = caption
        local_caption_top = caption_top
        local_caption_bottom = caption_bottom

        caption_notes, data = process_notes(data)

        if not local_caption_top and not local_caption_bottom and not local_caption:
            local_caption_bottom = caption_notes

        # Sort by item_name then remove it before writing
        data.sort(key=lambda x: x["item_name"])
        for item in data:
            item.pop("item_name", None)

        column_headings = get_column_headings(table_type, table_map, columns)

        content.extend(generate_table(table_type, data, column_headings, table_header, table_footer, caption_bottom=local_caption_bottom, caption_top=local_caption_top, caption=local_caption, do_bot_flag=do_bot_flag, bot_flag_type=bot_flag_type))
        rel_path = os.path.join(item_type, table_type + ".txt")
        output_dir = write_file(content, rel_path=rel_path, root_path=root_path, suppress=suppress)

        if combine_tables:
            all_tables.extend([f'=={table_type.replace("_", " ").capitalize()}=='])
            all_tables.extend(content)

    if combine_tables:
        rel_path = os.path.join(item_type, "all_tables.txt")
        write_file(all_tables, rel_path=rel_path, root_path=root_path, suppress=suppress)

    tables_name = Path(rel_path).parent.name.replace("_", " ").capitalize()
    echo.success(f"{tables_name} tables written to '{output_dir}'")