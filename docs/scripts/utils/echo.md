[Previous Folder](../tools/update_icons.md) | [Previous File](color.md) | [Next File](lua_helper.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# echo.py

Console logging utilities with coloured output, warning control, and tqdm support.

## Functions

### [`_message(message: str, prefix: str, style_func)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L12)

Print a coloured message with optional warning metadata.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The message text to display._
  - **prefix (str)**:
      - _Label prefix (e.g., "[Info]", "[Warning]")._
  - **style_func (callable)**:
      - _A function that applies styling (e.g., color.info)._
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

### [`write(message: str, style_func)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L63)

Print a standard message safely, supporting tqdm progress bars.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The message text to print._
  - **style_func (callable, optional)**:
      - _A colour/style function (e.g. color.info)._

### [`info(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L78)

Print an informational message in cyan.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The message text to display._

### [`warning(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L87)

Print a warning message in yellow with warning context.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The warning text to display._

### [`error(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L96)

Print an error message in red with error context.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The error text to display._

### [`success(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L105)

Print a success message in green.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The success message to display._

### [`debug(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L114)

Print a debug message in magenta if debug mode is enabled.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The debug text to display._

### [`deprecated(message: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/echo.py#L127)

Print a deprecation warning in magenta with warning context.


<ins>**Args:**</ins>
  - **message (str)**:
      - _The deprecation message to display._



[Previous Folder](../tools/update_icons.md) | [Previous File](color.md) | [Next File](lua_helper.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
