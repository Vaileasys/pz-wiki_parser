[Previous Folder](../tools/compare_item_lists.md) | [Previous File](media_helper.md) | [Next File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# table_helper.py

## Functions

### [`get_table_data(path: str, extra_keys: str | list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L15)

_Get table data from a json file._

### [`get_column_headings(table_type: str, table_map: dict, columns: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L42)

_Returns the list of column headings for a given table type._

### [`generate_column_headings(column_def: dict, headings: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L66)

_Generates wiki-style headings with rowspan/colspan markup from a nested dict._

### [`generate_table(table_type: str, data: dict, column_headings: list, table_header: str, table_footer: str, caption_top: str, caption_bottom: str, caption: str, table_before: str, table_after: str, do_bot_flag: bool, do_horizontal_scroll: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L109)

_Generates a wiki-formatted table from data and headings._

### [`process_notes(data_list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L178)

_Extracts notes from the first element of the list if present._

### [`create_tables(item_type: str, all_data: dict, columns: dict, table_map: dict, table_header, table_footer, caption, caption_top, caption_bottom, combine_tables: bool, root_path: str, do_bot_flag: bool, suppress: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L195)

_Creates and writes individual and/or combined item tables for each table type._



[Previous Folder](../tools/compare_item_lists.md) | [Previous File](media_helper.md) | [Next File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
