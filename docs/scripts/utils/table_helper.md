[Previous Folder](../tools/compare_item_lists.md) | [Previous File](media_helper.md) | [Next File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# table_helper.py

## Functions

### [`get_table_data(path: str, extra_keys: str | list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L15)

Get table data from a json file.

### [`get_column_headings(table_type: str, table_map: dict, columns: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L42)

Returns the list of column headings for a given table type.

:param str table_type: The type of table to retrieve headings for.
:param dict table_map: A mapping of table types to lists of column keys.
:param dict columns: A mapping of column keys to their translated heading text.
:return list: A list of translated column headings, or an empty list if the table type is not found.

### [`generate_column_headings(column_def: dict, headings: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L66)

Generates wiki-style headings with rowspan/colspan markup from a nested dict.

Supports attributes like 'style', 'class', etc., applied directly to each field.

### [`generate_table(table_type: str, data: dict, column_headings: list, table_header: str, table_footer: str, caption_top: str, caption_bottom: str, caption: str, table_before: str, table_after: str, do_bot_flag: bool, do_horizontal_scroll: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L109)

Generates a wiki-formatted table from data and headings.

:param str table_type: The category of the table, used in comments and naming.
:param dict data: A list of dictionaries representing table rows.
:param list column_headings: A list of formatted column header strings.
:param str table_header: The initial wiki table header. Defaults to DEF_TABLE_HEADER.
:param str table_footer: The closing wiki table footer. Defaults to DEF_TABLE_FOOTER.
:param str table_before: A string to be added before the table. Defaults to empty string.
:param str table_after: A string to be added after the table. Defaults to empty string.
:param bool do_bot_flag: Determines whether to add the bot flag comment. Defaults to True.
:param bool do_horizontal_scroll: Determines whether to add the horizontal scrolling wrapper. Defaults to True.
:return list: A list of strings forming the complete table content.

### [`process_notes(data_list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L178)

Extracts notes from the first element of the list if present.

Returns a tuple: (notes, data)

### [`create_tables(item_type: str, all_data: dict, columns: dict, table_map: dict, table_header, table_footer, caption, caption_top, caption_bottom, combine_tables: bool, root_path: str, do_bot_flag: bool, suppress: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L195)

Creates and writes individual and/or combined item tables for each table type.

:param str item_type: The main category name for grouping the output.
:param dict all_data: A dictionary mapping table types to lists of item data.
:param dict columns: A mapping of column keys to translated heading strings.
:param dict table_map: A mapping of table types to their expected column keys. Defaults to empty dictionary.
:param str|None table_header: Custom table header to use. Defaults to DEF_TABLE_HEADER.
:param bool combine_tables: If True, combines all tables into one file. Defaults to True.
:param str root_path: The root path where the files will be written. {language_code} will be formatted to current language code.
:param bool do_bot_flag: Determines whether to add the bot flag comment. Defaults to True.
:param bool suppress: Suppresses terminal prints when creating files. Note: will still print final folder location.
:return: None



[Previous Folder](../tools/compare_item_lists.md) | [Previous File](media_helper.md) | [Next File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
