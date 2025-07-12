[Previous Folder](../tools/update_icons.md) | [Previous File](media_helper.md) | [Next File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# table_helper.py

Generates wiki-formatted tables for Project Zomboid.

This module loads item data, builds structured tables with translations and formatting,
and writes them as individual or combined output files for use on the PZwiki.

## Functions

### [`get_table_data(path: str, extra_keys: str | list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L21)

Loads table data and optionally extracts extra keys from the JSON file.


<ins>**Args:**</ins>
  - **path (str)**:
      - _Path to the JSON file._
  - **extra_keys (str | list, optional)**:
      - _Single key or list of keys to extract additional data._

<ins>**Returns:**</ins>
  - **tuple:**
      - (map, headings[, extra_data]) depending on whether extra_keys is provided.

### [`get_column_headings(table_type: str, table_map: dict, columns: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L55)

Builds the list of column headings for a given table type.


<ins>**Args:**</ins>
  - **table_type (str)**:
      - _Table type to look up._
  - **table_map (dict)**:
      - _Mapping of table types to their column keys._
  - **columns (dict)**:
      - _Translated heading strings by key._

<ins>**Returns:**</ins>
  - **list[str]:**
      - Formatted wiki heading strings.

### [`generate_column_headings(column_def: dict, headings: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L82)

Generates multi-row wiki headings from a nested column definition.

Supports attributes like 'style' and 'class' on child headings,
as well as colspan/rowspan for structured table layouts.

<ins>**Args:**</ins>
  - **column_def (dict)**:
      - _Column layout with optional attributes and nesting._
  - **headings (dict)**:
      - _Mapping of keys to translated headings._

<ins>**Returns:**</ins>
  - **list[str]:**
      - Formatted wiki markup for table headers.

### [`generate_table(table_type: str, data: dict, column_headings: list, table_header: str, table_footer: str, caption_top: str, caption_bottom: str, caption: str, table_before: str, table_after: str, do_bot_flag: bool, bot_flag_type: str, do_horizontal_scroll: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L134)

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
  - **list[str]:**
      - The full table as a list of wiki lines.

### [`process_notes(data_list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L211)

Extracts notes from the first entry in a data list, if present.


<ins>**Args:**</ins>
  - **data_list (list)**:
      - _List of data dictionaries._

<ins>**Returns:**</ins>
  - **tuple:**
      - (caption str, remaining data list)

### [`create_tables(item_type: str, all_data: dict, columns: dict, table_map: dict, table_header, table_footer, caption, caption_top, caption_bottom, combine_tables: bool, root_path: str, do_bot_flag: bool, bot_flag_type: str, suppress: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/table_helper.py#L233)

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

<ins>**Returns:**</ins>
  - None



[Previous Folder](../tools/update_icons.md) | [Previous File](media_helper.md) | [Next File](util.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
