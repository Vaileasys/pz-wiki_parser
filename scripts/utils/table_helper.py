from pathlib import Path
from scripts.core import translate
from scripts.core.constants import OUTPUT_PATH
from scripts.utils.util import echo, load_json
from scripts.utils.utility import save_cache


OUTPUT_DIR = Path(OUTPUT_PATH) / translate.get_language_code() / "item_list"

DEF_TABLE_HEADER = '{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"'
DEF_TABLE_FOOTER = '|}'


def get_table_data(path:str, extra_keys:str|list=None):
    """
    Get table data from a json file.
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


#def map_heading_rows():



def get_column_headings(table_type:str, table_map:dict, columns:dict):
    """
    Returns the list of column headings for a given table type.

    :param str table_type: The type of table to retrieve headings for.
    :param dict table_map: A mapping of table types to lists of column keys.
    :param dict columns: A mapping of column keys to their translated heading text.
    :return list: A list of translated column headings, or an empty list if the table type is not found.
    """
    column_def = table_map.get(table_type) or table_map.get("default")

    if column_def is None:
        print(f"Error: No mapping for table type: '{table_type}'")
        return []

    if isinstance(column_def, list):
        return [columns.get(key, f'! {key}') for key in column_def]
    elif isinstance(column_def, dict):
        return generate_column_headings(column_def, columns)
    else:
        print(f"Error: Invalid column definition type for '{table_type}'")
        return []


def generate_column_headings(column_def: dict, headings: dict) -> list:
    """
    Generates wiki-style headings with rowspan/colspan markup from a nested dict.
    Supports attributes like 'style', 'class', etc., applied directly to each field.
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


def generate_table(table_type:str, data:dict, column_headings:list, table_header:str=DEF_TABLE_HEADER, table_footer:str=DEF_TABLE_FOOTER, caption_top:str=None, caption_bottom:str=None, table_before:str=None, table_after:str=None) -> list:
    """
    Generates a wiki-formatted table from data and headings.

    :param str table_type: The category of the table, used in comments and naming.
    :param dict data: A list of dictionaries representing table rows.
    :param list column_headings: A list of formatted column header strings.
    :param str table_header: The initial wiki table header. Defaults to DEF_TABLE_HEADER.
    :param str table_footer: The closing wiki table footer. Defaults to DEF_TABLE_FOOTER.
    :param str table_before: A string to be added before the table. Defaults to empty string.
    :param str table_after: A string to be added after the table. Defaults to empty string.
    :return list: A list of strings forming the complete table content.
    """
    
    content = []

    table_before = "" if table_before is None else table_before
    table_after = "" if table_after is None else table_after

    content.append(f'<!--BOT_FLAG-start-{table_type.replace(" ", "_")}. DO NOT REMOVE-->' + table_before + table_header)

    if caption_top:
        content.append(f'|+ style="caption-side:top; font-weight:normal; | {caption_top}', '|-')

    content.extend(column_headings)

    for item in data:
        item_content = []
        item_content.append("|-")
        for value in list(item.values()):
            item_content.append(f"| {value}")
        
        content.extend(item_content)

    if caption_bottom and not caption_top:
        content.extend(['|-', f'|+ style="caption-side:bottom; font-weight:normal; border: none;" | {caption_bottom}'])
    
    content.append(table_footer + table_after + f'<!--BOT_FLAG-end-{table_type.replace(" ", "_")}. DO NOT REMOVE-->')

    # Get translations
    content = [translate.get_wiki_translation(value) for value in content]

    return content


def write_to_file(content:list, rel_path="list.txt", suppress=False):
    """
    Writes content to a file, creating directories as needed.

    :param list content: A list of strings to write to the file.
    :param str rel_path: The relative path where the file will be saved. If no file extension is given, the path is treated as a directory.
    :return: The directory the file is saved to.
    """
    _output_path = OUTPUT_DIR / rel_path
    _output_dir = _output_path.parent if _output_path.suffix else _output_path
    _output_dir.mkdir(parents=True, exist_ok=True)

    if _output_path.suffix:
        with open(_output_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(content))

        if not suppress:
            echo(f"File saved to '{_output_path}'")
        
    else:
        echo(f"Warning: No file written. '{_output_path}' appears to be a directory.")
    
    return _output_dir


def process_notes(data_list):
    """
    Extracts notes from the first element of the list if present.
    Returns a tuple: (notes, data)
    """
    if data_list and isinstance(data_list[0], dict) and "notes" in data_list[0]:
        notes = data_list[0]["notes"]
        data = data_list[1:]
    else:
        notes = []
        data = data_list

    caption = "<br>".join(notes)

    return caption, data


def create_tables(item_type:str, all_data:dict, columns:dict, table_map:dict={}, table_header=DEF_TABLE_HEADER, table_footer=DEF_TABLE_FOOTER, combine_tables:bool=True, suppress:bool=False):
    """
    Creates and writes individual and/or combined item tables for each table type.

    :param str item_type: The main category name for grouping the output.
    :param dict all_data: A dictionary mapping table types to lists of item data.
    :param dict columns: A mapping of column keys to translated heading strings.
    :param dict table_map: A mapping of table types to their expected column keys. Defaults to empty dictionary.
    :param str|None table_header: Custom table header to use. Defaults to DEF_TABLE_HEADER.
    :param bool combine_tables: If True, combines all tables into one file. Defaults to True.
    :param bool suppress: Suppresses terminal prints when creating files. Note: will still print final folder location.
    :return: None
    """

    all_tables = []
    for table_type, data in sorted(all_data.items()):

        content = []

        caption, data = process_notes(data)

        # Sort by item_name then remove it before writing
        data.sort(key=lambda x: x["item_name"])
        for item in data:
            item.pop("item_name", None)

        column_headings = get_column_headings(table_type, table_map, columns)

        content.extend(generate_table(table_type, data, column_headings, table_header, table_footer, caption_bottom=caption))
        rel_path = f"{item_type}/{table_type}.txt"
        output_dir = write_to_file(content, rel_path, suppress=suppress)

        if combine_tables:
            all_tables.extend([f"=={table_type.replace("_", " ").capitalize()}=="])
            all_tables.extend(content)

    if combine_tables:
        write_to_file(all_tables, f"{item_type}/all_tables.txt", suppress=suppress)

    echo(f"Tables written to {output_dir}")