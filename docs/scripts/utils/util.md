[Previous Folder](../tools/update_icons.md) | [Previous File](table_helper.md) | [Next File](utility.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# util.py

## Functions

### [`capitalize(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L4)

Safely perform the capitalize method if a value is not a string. Lists will also be capitalized, provided their values are strings.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - str | list | None: Capitalized values if a string or list, otherwise None.

### [`format_positive(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L38)

Formats a number with '+' if positive, trimming trailing zeros. Returns original value as string if invalid.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **str:**
      - Formatted string with '+' prefix if positive, or original value as a string if invalid.

### [`link(page: str, name: str, anchor: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L56)

Returns a wiki link in the format [[Page#Anchor|Name]], including a language suffix for non-English languages.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **str:**
      - The formatted wiki link.

### [`convert_percentage(value: str | int | float, start_zero, percentage, default, decimals: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L81)

Converts a numeric value to a percentage string.


<ins>**Args:**</ins>
  - **value (str, int, float)**:
      - _The value to be converted to a percentage. Can be a number or a string representation of a number._
  - **start_zero (bool, optional)**:
      - _If True, treats the value as a fraction (e.g., 0.5 -> 50%)._
      - _If False, assumes the value starts from 100% (e.g., 1.5 -> 150%). Defaults to True._
  - **percentage (bool, optional)**:
      - _If True, the value is already a percentage and will not be scaled. Defaults to False._
  - **default (str)**:
      - _The value to return for invalid input or when the percentage rounds to 0._

<ins>**Returns:**</ins>
  - **str:**
      - The formatted percentage as a string with a '%' sign.
      - Returns '-' for invalid inputs.

### [`convert_int(value: int | float)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L114)

Converts a value to an integer if it has no decimal (isn't float-like).

### [`to_bool(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L130)

Convert a value to boolean by checking common 'true' strings.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **bool:**
      - True if the value matches a 'true' string; False otherwise.

### [`flip_data(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L143)

Flip a flat dictionary so that values become keys, and keys become values.

If multiple keys share the same value, they are grouped in a list.

<ins>**Args:**</ins>
  - **data (dict)**:
      - _A flat dictionary to flip. All values must be hashable._

<ins>**Returns:**</ins>
  - **dict:**
      - A new dictionary with values as keys and lists of original keys as values.

<ins>**Raises:**</ins>
  - **TypeError:**
      - If 'data' is not a dictionary or a value is unhashable.

### [`deep_merge(base: dict, override: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L168)

Recursively merge two dictionaries, preserving existing keys.


<ins>**Args:**</ins>
  - **base (dict)**:
      - _The base dictionary._
  - **override (dict)**:
      - _The dictionary with overriding values._

<ins>**Returns:**</ins>
  - **dict:**
      - A new dictionary with combined contents.

### [`deep_getattr(obj: object, attr_path: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L190)

Access nested attributes on an object using dot‑notation.


<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - The value found at the end of the attribute path, or `default` if any intermediate attribute is missing or `None`.

### [`calculate_drain_rate(use_delta: float, unit: str, tick_minutes: int, as_percentage: bool)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L211)

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
  - str | float: Battery drain over the given time unit.

### [`convert_unit(value: float, unit: str, start_prefix: str, force_prefix: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L238)

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
  - **str:**
      - A human-readable string with the chosen prefix and unit.

### [`split_camel_case(text: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L277)

Add spaces between words in a camel case string.


<ins>**Args:**</ins>
  - **text (str)**:
      - _A camelCase or PascalCase string._

<ins>**Returns:**</ins>
  - **str:**
      - The string with spaces added between words.

### [`tick(text: str, link: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L290)

Return a wiki-formatted tick/check icon, optionally with text and link.


<ins>**Args:**</ins>
  - **text (str, optional)**:
      - _Display text._
  - **link (str, optional)**:
      - _Link target._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki string for the tick icon.

### [`cross(text: str, link: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L306)

Return a wiki-formatted cross icon, optionally with text and link.


<ins>**Args:**</ins>
  - **text (str, optional)**:
      - _Display text._
  - **link (str, optional)**:
      - _Link target._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki string for the cross icon.

### [`rgb(red: int | float, green: int | float, blue: int | float)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L322)

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
  - **str:**
      - A string formatted as '{{rgb|R, G, B}}' where R, G, and B are integers.

### [`enumerate_params(parameters)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L352)

Expand list values in a dict into numbered keys for infobox use.


<ins>**Args:**</ins>
  - **parameters (dict)**:
      - _Dictionary of parameter names and values._
      - _List values will be split into numbered keys._

<ins>**Returns:**</ins>
  - **dict:**
      - New dictionary with expanded numbered keys.

### [`check_zero(value: int | float, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L377)

Return 'default' if the numeric value is zero, else return the value.


<ins>**Args:**</ins>
  - **value (int or float)**:
      - _Value to check._
  - **default (optional)**:
      - _Value to return if input is zero._

<ins>**Returns:**</ins>
  - **int, float, or None:**
      - Original value or 'default' if zero.



[Previous Folder](../tools/update_icons.md) | [Previous File](table_helper.md) | [Next File](utility.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
