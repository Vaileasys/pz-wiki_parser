[Previous Folder](../tools/compare_item_lists.md) | [Next File](lua_helper.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# echo.py

Console logging utilities with coloured output, warning control, and tqdm support.

## Functions

### [`_message(message: str, prefix: str, colour_code: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L11)

Print a coloured message with optional warning metadata.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The message text to display._
  - **prefix (str)**:
      - _Label prefix (e.g., "[Info]", "[Warning]")._
  - **colour_code (str)**:
      - _ANSI colour code for the prefix._
  - **emit_warning (bool, optional)**:
      - _Whether to append stack info for warnings._
  - **warnings_level (int, optional)**:
      - _Warning level threshold for display._

### [`ignore_warnings(warnings_level: int, ignore: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L51)

Enable or disable warning output filtering by level.


<ins>**Args:**</ins>
  - **warnings_level (int)**:
      - _Minimum warning level to show._
  - **ignore (bool)**:
      - _Whether to suppress warnings below the level._

### [`write(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L63)

Print a standard message safely, supporting tqdm progress bars.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The message text to print._

### [`info(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L75)

Print an informational message in cyan.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The message text to display._

### [`warning(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L84)

Print a warning message in yellow with warning context.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The warning text to display._

### [`error(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L93)

Print an error message in red with error context.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The error text to display._

### [`success(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L102)

Print a success message in green.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The success message to display._

### [`debug(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L111)

Print a debug message in magenta if debug mode is enabled.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The debug text to display._

### [`deprecated(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L124)

Print a deprecation warning in magenta with warning context.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The deprecation message to display._

### [`echo(message)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L137)

Safely prints a standard message with tqdm support.

### [`echo_info(message)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L145)
### [`echo_warning(message)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L148)
### [`echo_error(message)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L151)
### [`echo_success(message)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L154)
### [`echo_debug(message)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L157)
### [`echo_deprecated(message)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L164)


[Previous Folder](../tools/compare_item_lists.md) | [Next File](lua_helper.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
