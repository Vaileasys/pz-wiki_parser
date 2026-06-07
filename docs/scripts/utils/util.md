[Previous Folder](../tools/batch_processor.md) | [Previous File](table_helper.md) | [Next File](utility.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# util.py

## Functions

### [`capitalize(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L4)

Safely perform the capitalize method if a value is not a string. Lists will also be capitalized, provided their values are strings.

<ins>**Args:**</ins>
  - **value**:
      - _The string or list of strings to capitalize._

<ins>**Returns:**</ins>
  - **str | list | None**:
      - _Capitalized values if a string or list, otherwise None._

### [`format_positive(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L38)

Formats a number with '+' if positive, trimming trailing zeros. Returns original value as string if invalid.

<ins>**Args:**</ins>
  - **value**:
      - _The value to format._

<ins>**Returns:**</ins>
  - **str**:
      - _Formatted string with '+' prefix if positive, or original value as a string if invalid._

### [`link(page: str, name: str = None, anchor: str = None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L56)

Returns a wiki link in the format `[[Page#Anchor|Name]]`, including a language suffix for non-English languages.

<ins>**Args:**</ins>
  - **page**:
      - _The target page_
  - **name**:
      - _The display text of the link (optional). Defaults to `page`._
  - **anchor**:
      - _The section anchor within the page (optional)._

<ins>**Returns:**</ins>
  - **str**:
      - _The formatted wiki link._

### [`convert_percentage(value: str | int | float, start_zero = True, percentage = False, default = None, decimals: int = 0) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L93)

Converts a numeric value to a percentage string.

<ins>**Args:**</ins>
  - **value (str, int, float)**:
      - _The value to be converted to a percentage. Can be a number or a string representation of a number._
  - **start_zero (bool, optional)**:
      - _If True, treats the value as a fraction (e.g., 0.5 -> 50%)._
  - **If False, assumes the value starts from 100% (e.g., 1.5 -> 150%). Defaults to True.**:
  - **percentage (bool, optional)**:
      - _If True, the value is already a percentage and will not be scaled. Defaults to False._
  - **default (str)**:
      - _The value to return for invalid input or when the percentage rounds to 0._

<ins>**Returns:**</ins>
  - **str**:
      - _The formatted percentage as a string with a '%' sign._
  - **Returns '-' for invalid inputs.**:

### [`convert_int(value: int | float) -> int | float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L126)

Converts a value to an integer if it has no decimal (isn't float-like).

### [`to_bool(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L142)

Convert a value to boolean by checking common 'true' strings.

<ins>**Args:**</ins>
  - **value**:
      - _Any value to check._

<ins>**Returns:**</ins>
  - **bool**:
      - _True if the value matches a 'true' string; False otherwise._

### [`flip_data(data: dict) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L155)

Flip a flat dictionary so that values become keys, and keys become values.
If multiple keys share the same value, they are grouped in a list.

Raises:
    TypeError: If 'data' is not a dictionary or a value is unhashable.

<ins>**Args:**</ins>
  - **data (dict)**:
      - _A flat dictionary to flip. All values must be hashable._

<ins>**Returns:**</ins>
  - **dict**:
      - _A new dictionary with values as keys and lists of original keys as values._

### [`deep_merge(base: dict, override: dict) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L180)

Recursively merge two dictionaries, preserving existing keys.

<ins>**Args:**</ins>
  - **base (dict)**:
      - _The base dictionary._
  - **override (dict)**:
      - _The dictionary with overriding values._

<ins>**Returns:**</ins>
  - **dict**:
      - _A new dictionary with combined contents._

### [`deep_getattr(obj: object, attr_path: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L202)

Access nested attributes on an object using dot‑notation.

<ins>**Args:**</ins>
  - **obj (object)**:
      - _The object to fetch attributes from._
  - **attr_path (str)**:
      - _A string of attribute names separated by '.', e.g. "fluid_container.capacity" - the path to the desired value._
  - **default (str | int | float, optional)**:
      - _A fallback value returned if any attribute in the path doesn't exist or its value is `None`._

<ins>**Returns:**</ins>
  - **The value found at the end of the attribute path, or `default` if any intermediate attribute is missing or `None`.**:

### [`calculate_drain_rate(use_delta: float, unit: str = 'hour', tick_minutes: int = 1, as_percentage: bool = False) -> str | float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L223)

Calculates how much of a drainable item is consumed over time.

<ins>**Args:**</ins>
  - **use_delta (float)**:
      - _Radio UseDelta value from item script (e.g., 0.014 for 1.4% per hour)._
  - **as_percentage (bool)**:
      - _Return as a percentage string (default False)._
  - **unit (str)**:
      - _Time unit to calculate ('minute', 'hour', 'day')._
  - **as_percentage (bool)**:
      - _Return as a percentage string (default False)._

<ins>**Returns:**</ins>
  - **str | float**:
      - _Battery drain over the given time unit._

### [`convert_unit(value: float, unit: str, start_prefix: str = '', force_prefix: str = None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L250)

Convert a value from a given SI prefix (default: base) to the most appropriate SI prefix
between milli (m) and Mega (M), or force it to a specific one.

<ins>**Args:**</ins>
  - **value (float)**:
      - _The numeric value to convert._
  - **unit (str)**:
      - _The unit to append after the converted value._
  - **start_prefix (str, optional)**:
      - _The starting SI prefix (default ""). One of: "m", "", "k", "M"._
  - **force_prefix (str, optional)**:
      - _If set, force output to this SI prefix. Skips automatic scaling._

<ins>**Returns:**</ins>
  - **str**:
      - _A human-readable string with the chosen prefix and unit._

### [`split_camel_case(text: str, sep: str = ' ', preserve_caps: bool = True) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L289)

Add separator between words in a camel case string.

<ins>**Args:**</ins>
  - **text (str)**:
      - _A camelCase or PascalCase string._
  - **sep (str)**:
      - _String used to join split parts._
  - **preserve_caps (bool)**:
      - _Keep consecutive capital letters together._

<ins>**Returns:**</ins>
  - **str**:
      - _The string with separators added between words._

### [`tick(text: str = None, link: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L311)

Return a wiki-formatted tick/check icon, optionally with text and link.

<ins>**Args:**</ins>
  - **text (str, optional)**:
      - _Display text._
  - **link (str, optional)**:
      - _Link target._

<ins>**Returns:**</ins>
  - **str**:
      - _Formatted wiki string for the tick icon._

### [`cross(text: str = None, link: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L327)

Return a wiki-formatted cross icon, optionally with text and link.

<ins>**Args:**</ins>
  - **text (str, optional)**:
      - _Display text._
  - **link (str, optional)**:
      - _Link target._

<ins>**Returns:**</ins>
  - **str**:
      - _Formatted wiki string for the cross icon._

### [`rgb(red: int | float = 0, green: int | float = 0, blue: int | float = 0)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L343)

Return an rgb template string with the given colour values.

Each colour component can be specified as either:
  - An int (0–255), representing the raw RGB value.
  - A float (0.0–1.0), representing a normalised fraction which will be scaled to 0–255.

<ins>**Args:**</ins>
  - **red (int | float)**:
      - _Red component (default: 0)._
  - **green (int | float)**:
      - _Green component (default: 0)._
  - **blue (int | float)**:
      - _Blue component (default: 0)._

<ins>**Returns:**</ins>
  - **str**:
      - _A string formatted as '{{rgb|R, G, B}}' where R, G, and B are integers._

### [`enumerate_params(parameters: dict, whitelist: list[str] = None, blacklist: list[str] = None, separator: str = '<br>') -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L373)

Expand list values in a dict into numbered keys for infobox use.

<ins>**Args:**</ins>
  - **parameters (dict)**:
      - _Dictionary of parameter names and values._
  - **whitelist (list[str], optional)**:
      - _Only keys in this list will be enumerated. If None, all keys are considered._
  - **blacklist (list[str], optional)**:
      - _Keys in this list will be excluded from enumeration._
  - **separator (str, optional)**:
      - _String to use for joining non-enumerated list values. Defaults to "<br>"._

<ins>**Returns:**</ins>
  - **dict**:
      - _New dictionary with expanded numbered keys._

### [`check_zero(value: int | float, default = None) -> int | float | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L413)

Return 'default' if the numeric value is zero, else return the value.

<ins>**Args:**</ins>
  - **value (int or float)**:
      - _Value to check._
  - **default (optional)**:
      - _Value to return if input is zero._

<ins>**Returns:**</ins>
  - **int, float, or None**:
      - _Original value or 'default' if zero._


[Previous Folder](../tools/batch_processor.md) | [Previous File](table_helper.md) | [Next File](utility.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
