[Previous Folder](../tools/batch_processor.md) | [Previous File](media_helper.md) | [Next File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# table_helper.py

Generates wiki-formatted tables for Project Zomboid.

This module loads item data, builds structured tables with translations and formatting,
and writes them as individual or combined output files for use on the PZwiki.

## Functions

### [`get_table_data(path: str, extra_keys: str | list = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L23)

Loads table data and optionally extracts extra keys from the JSON file.

<ins>**Args:**</ins>
  - **path (str)**:
      - _Path to the JSON file._
  - **extra_keys (str | list, optional)**:
      - _Single key or list of keys to extract additional data._

<ins>**Returns:**</ins>
  - **tuple**:
      - _(map, headings[, extra_data]) depending on whether extra_keys is provided._

### [`get_column_headings(table_type: str, table_map: dict, columns: dict, drop_keys: set[str] = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L57)

Builds the list of column headings for a given table type.

<ins>**Args:**</ins>
  - **table_type (str)**:
      - _Table type to look up._
  - **table_map (dict)**:
      - _Mapping of table types to their column keys._
  - **columns (dict)**:
      - _Translated heading strings by key._
  - **drop_keys (set[str])**:
      - _optional set of keys to exclude._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _Formatted wiki heading strings._

### [`generate_column_headings(column_def: dict, headings: dict) -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L92)

Generates multi-row wiki headings from a nested column definition.

Supports attributes like 'style' and 'class' on child headings,
as well as colspan/rowspan for structured table layouts.

<ins>**Args:**</ins>
  - **column_def (dict)**:
      - _Column layout with optional attributes and nesting._
  - **headings (dict)**:
      - _Mapping of keys to translated headings._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _Formatted wiki markup for table headers._

### [`generate_table(table_type: str, data: dict, column_headings: list, table_header: str = DEF_TABLE_HEADER, table_footer: str = DEF_TABLE_FOOTER, caption_top: str = None, caption_bottom: str = None, caption: str = None, table_before: str = None, table_after: str = None, do_bot_flag: bool = True, bot_flag_type: str = 'table', do_horizontal_scroll: bool = True) -> list`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L146)

Generates a full wiki-formatted table for the given data and headings.

<ins>**Args:**</ins>
  - **table_type (str)**:
      - _Used in comments and IDs._
  - **data (dict)**:
      - _List of dicts representing table rows._
  - **column_headings (list)**:
      - _Header rows for the table._
  - **table_header (str)**:
      - _Starting wiki markup for the table._
  - **table_footer (str)**:
      - _Closing wiki markup._
  - **caption_top (str)**:
      - _Optional caption shown above the table._
  - **caption_bottom (str)**:
      - _Optional caption shown below the table._
  - **caption (str)**:
      - _Optional centered caption (overrides top/bottom)._
  - **table_before (str)**:
      - _Content before the table._
  - **table_after (str)**:
      - _Content after the table._
  - **do_bot_flag (bool)**:
      - _Whether to include bot flag markers._
  - **bot_flag_type (str)**:
      - _Type used in bot flag comment._
  - **do_horizontal_scroll (bool)**:
      - _Wraps table in a scrollable container._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _The full table as a list of wiki lines._

### [`process_notes(data_list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L238)

Extracts notes from the first entry in a data list, if present.

<ins>**Args:**</ins>
  - **data_list (list)**:
      - _List of data dictionaries._

<ins>**Returns:**</ins>
  - **tuple**:
      - _(caption str, remaining data list)_

### [`remove_empty_columns(all_food_data: dict[str, list[dict]]) -> dict[str, set]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L260)

Remove columns from each table where all values are '-'.
Returns a dict mapping table_type -> removed column keys.

### [`create_tables(item_type: str, all_data: dict, columns: dict, table_map: dict = {}, table_header = DEF_TABLE_HEADER, table_footer = DEF_TABLE_FOOTER, caption = None, caption_top = None, caption_bottom = None, combine_tables: bool = True, root_path: str = os.path.join(ITEM_DIR, 'lists'), do_bot_flag: bool = True, bot_flag_type: str = 'table', suppress: bool = False, drop_empty_columns: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L285)

Creates and writes individual and/or combined item tables for each table type.

<ins>**Args:**</ins>
  - **item_type (str)**:
      - _The main category name for grouping the output._
  - **all_data (dict[str, list])**:
      - _A dictionary mapping table types to lists of item data._
  - **columns (dict[str, str])**:
      - _A mapping of column keys to translated heading strings._
  - **table_map (dict[str, list[str]])**:
      - _A mapping of table types to their expected column keys. Defaults to empty dictionary._
  - **table_header (str)**:
      - _Custom table header to use. Defaults to DEF_TABLE_HEADER._
  - **table_footer (str)**:
      - _Custom table footer to use. Defaults to DEF_TABLE_FOOTER._
  - **caption (str | None)**:
      - _A shared table caption (centered, overrides caption_top and caption_bottom)._
  - **caption_top (str | None)**:
      - _Caption to appear above the table._
  - **caption_bottom (str | None)**:
      - _Caption to appear below the table if no top or center caption is set._
  - **combine_tables (bool)**:
      - _If True, combines all tables into one file. Defaults to True._
  - **root_path (str)**:
      - _Root path where files will be written. `{language_code}` will be formatted to the current language code._
  - **do_bot_flag (bool)**:
      - _Whether to add the bot flag comment to the output. Defaults to True._
  - **bot_flag_type (str)**:
      - _The identifier used in bot flag comments. Defaults to "table"._
  - **suppress (bool)**:
      - _If True, suppresses terminal output except for final success message._
  - **drop_empty_columns (bool)**:
      - _If True, removes columns that are empty in all rows for each table type. Defaults to False._

<ins>**Returns:**</ins>
  - **None**:


[Previous Folder](../tools/batch_processor.md) | [Previous File](media_helper.md) | [Next File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
