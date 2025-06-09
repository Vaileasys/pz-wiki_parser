[Previous Folder](../tools/compare_item_lists.md) | [Previous File](table_helper.md) | [Next File](utility.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# util.py

## Functions

### [`capitalize(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L4)

Safely perform the capitalize method if a value is not a string. Lists will also be capitalized, provided their values are strings.

:param value: The string or list of strings to capitalize.
:type value: str
:return: Capitalized values if a string or list, otherwise None.
:rtype: str | list | None

### [`format_positive(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L37)

Formats a number with '+' if positive, trimming trailing zeros. Returns original value as string if invalid.

:param value: The value to format.
:type value: float | int | str | any
:return: Formatted string with '+' prefix if positive, or original value as a string if invalid.
:rtype: str

### [`link(page: str, name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L54)

Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages.

:param page: The target page
:param name: The display text of the link (optional). Defaults to `page`.
:return: The formatted wiki link.

### [`format_link(name: str, page: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L72)

Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages.

:param name: The display text of the link.
:param page: The target page (optional). Defaults to `name`.
:return: The formatted wiki link.

### [`convert_percentage(value: str | int | float, start_zero, percentage)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L94)

Converts a numeric value to a percentage string.


<ins>**Args:**</ins>
  - **value (str, int, float)**:
      - _The value to be converted to a percentage. Can be a number or a string representation of a number._
  - **start_zero (bool, optional)**:
      - _If True, treats the value as a fraction (e.g., 0.5 -> 50%)._
      - _If False, assumes the value starts from 100% (e.g., 1.5 -> 150%). Defaults to True._
  - **percentage (bool, optional)**:
      - _If True, the value is already a percentage and will not be scaled. Defaults to False._

<ins>**Returns:**</ins>
  - **str:**
      - The formatted percentage as a string with a '%' sign.
      - Returns '-' for invalid inputs.

### [`convert_int(value: int | float)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L125)

Converts a value to an integer if it has no decimal (isn't float-like).

### [`to_bool(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L141)

Convert a value to boolean by checking common 'true' strings.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **bool:**
      - True if the value matches a 'true' string; False otherwise.

### [`tick(text: str, link: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L154)

Return a wiki-formatted tick/check icon, optionally with text and link.


<ins>**Args:**</ins>
  - **text (str, optional)**:
      - _Display text._
  - **link (str, optional)**:
      - _Link target._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki string for the tick icon.

### [`cross(text: str, link: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L169)

Return a wiki-formatted cross icon, optionally with text and link.


<ins>**Args:**</ins>
  - **text (str, optional)**:
      - _Display text._
  - **link (str, optional)**:
      - _Link target._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki string for the cross icon.

### [`enumerate_params(parameters)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L187)

Expand list values in a dict into numbered keys for infobox use.


<ins>**Args:**</ins>
  - **parameters (dict)**:
      - _Dictionary of parameter names and values._
      - _List values will be split into numbered keys._

<ins>**Returns:**</ins>
  - **dict:**
      - New dictionary with expanded numbered keys.

### [`check_zero(value: int | float, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L212)

Return 'default' if the numeric value is zero, else return the value.


<ins>**Args:**</ins>
  - **value (int or float)**:
      - _Value to check._
  - **default (optional)**:
      - _Value to return if input is zero._

<ins>**Returns:**</ins>
  - **int, float, or None:**
      - Original value or 'default' if zero.



[Previous Folder](../tools/compare_item_lists.md) | [Previous File](table_helper.md) | [Next File](utility.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
