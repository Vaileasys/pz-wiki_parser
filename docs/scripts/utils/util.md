[Previous Folder](../tools/compare_item_lists.md) | [Previous File](table_helper.md) | [Next File](utility.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# util.py

## Functions

### [`capitalize(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L6)

_Safely perform the capitalize method if a value is not a string. Lists will also be capitalized, provided their values are strings._
### [`format_positive(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L39)

_Formats a number with '+' if positive, trimming trailing zeros. Returns original value as string if invalid._
### [`link(page: str, name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L56)

_Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages._
### [`format_link(name: str, page: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L72)

_Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages._
### [`convert_percentage(value: str | int | float, start_zero, percentage)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L92)

_Converts a numeric value to a percentage string._

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
### [`convert_int(value: int | float)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L123)

_Converts a value to an integer if it has no decimal (isn't float-like)._
### [`tick(text: str, link: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L140)
### [`cross(text: str, link: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L145)
### [`enumerate_params(parameters)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L153)
### [`check_zero(value: int | float, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/util.py#L168)

_Returns 'default' if the value is zero._


[Previous Folder](../tools/compare_item_lists.md) | [Previous File](table_helper.md) | [Next File](utility.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
