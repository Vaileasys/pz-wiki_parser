from pathlib import Path
from scripts.core import translate
from scripts.core.constants import OUTPUT_PATH
from scripts.utils.util import echo, load_json


OUTPUT_DIR = Path(OUTPUT_PATH) / translate.get_language_code() / "item_list"

DEF_TABLE_HEADER = '{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"'


def get_table_data(path:str):
    """
    Get table data from a json file.
    """
    data = load_json(path)
    map = data.get("map")
    headings = data.get("headings")
    return map, headings


def get_column_headings(table_type:str, table_map:dict, columns:dict):
    """
    Returns the list of column headings for a given table type.

    :param str table_type: The type of table to retrieve headings for.
    :param dict table_map: A mapping of table types to lists of column keys.
    :param dict columns: A mapping of column keys to their translated heading text.
    :return list: A list of translated column headings, or an empty list if the table type is not found.
    """
    column_keys = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")
    column_headings = []

    if column_keys is None:
        echo(f"Error: No mapping for table type: '{table_type}'")
        return column_headings

    for key in column_keys:
        if key in columns:
            column_headings.append(columns[key])

    return column_headings


def generate_table(table_type:str, data:dict, column_headings:list, table_header:str=DEF_TABLE_HEADER) -> list:
    """
    Generates a wiki-formatted table from data and headings.

    :param str table_type: The category of the table, used in comments and naming.
    :param dict data: A list of dictionaries representing table rows.
    :param list column_headings: A list of formatted column header strings.
    :param str table_header: The initial wiki table header. Defaults to DEF_TABLE_HEADER.
    :return list: A list of strings forming the complete table content.
    """
    if table_header is None:
        table_header = DEF_TABLE_HEADER
    
    content = []
    content.append(f'<!--BOT_FLAG-start-{table_type.replace(" ", "_")}. DO NOT REMOVE-->' + table_header)

    content.extend(column_headings)

    for item in data:
        item_content = []
        item_content.append("|-")
        for value in list(item.values()):
            item_content.append(f"| {value}")
        
        content.extend(item_content)
    
    content.append("|}" + f'<!--BOT_FLAG-end-{table_type.replace(" ", "_")}. DO NOT REMOVE-->')

    return content


def write_to_file(content:list, rel_path="list.txt"):
    """
    Writes content to a file, creating directories as needed.

    :param list content: A list of strings to write to the file.
    :param str rel_path: The relative path where the file will be saved. If no file extension is given, the path is treated as a directory.
    :return: None
    """
    _output_path = OUTPUT_DIR / rel_path
    _output_dir = _output_path.parent if _output_path.suffix else _output_path
    _output_dir.mkdir(parents=True, exist_ok=True)

    if _output_path.suffix:
        with open(_output_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(content))
    
        echo(f"File saved to '{_output_path}'")
    else:
        echo(f"Warning: No file written. '{_output_path}' appears to be a directory.")


def create_tables(item_type:str, all_data:dict, columns:dict, table_map:dict={}, table_header=None, combine_tables:bool=True, map_path:str=None):
    """
    Creates and writes individual and/or combined item tables for each table type.

    :param str item_type: The main category name for grouping the output.
    :param dict all_data: A dictionary mapping table types to lists of item data.
    :param dict columns: A mapping of column keys to translated heading strings.
    :param dict table_map: A mapping of table types to their expected column keys. Defaults to empty dictionary.
    :param str|None table_header: Custom table header to use. Defaults to DEF_TABLE_HEADER.
    :param bool combine_tables: If True, combines all tables into one file. Defaults to True.
    :param str map_path: File path to JSON file containing map path data. Defaults to None.
    :return: None
    """
    # Get table map
    if map_path is not None:
        table_map = load_json(map_path)


    all_tables = []
    for table_type, data in sorted(all_data.items()):
        content = []

        # Sort by item_name then remove it before writing
        data.sort(key=lambda x: x["item_name"])
        for item in data:
            item.pop("item_name", None)

        column_headings = get_column_headings(table_type, table_map, columns)

        content.extend(generate_table(table_type, data, column_headings, table_header))
        rel_path = f"{item_type}/{table_type}.txt"
        write_to_file(content, rel_path)

        if combine_tables:
            all_tables.extend([f"=={table_type.replace("_", " ").capitalize()}=="])
            all_tables.extend(content)
    
    if combine_tables:
        write_to_file(all_tables, f"{item_type}/all_tables.txt")