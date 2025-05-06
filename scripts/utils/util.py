from scripts.core.language import Language
from scripts.utils.echo import echo_deprecated


def capitalize(value):
    """
    Safely perform the capitalize method if a value is not a string. Lists will also be capitalized, provided their values are strings.

    :param value: The string or list of strings to capitalize.
    :type value: str
    :return: Capitalized values if a string or list, otherwise None.
    :rtype: str | list | None
    """
    if isinstance(value, str):
        value = [value]
        is_string = True
    elif isinstance(value, list):
        is_string = False
    else:
        return None

    rvalue = []
    
    for v in value:
        if isinstance(v, str):
            v = v.capitalize()
        else:
            v = None

        rvalue.append(v)

    if is_string:
        return rvalue[0]
    
    return rvalue


def format_positive(value):
    """
    Formats a number with '+' if positive, trimming trailing zeros. Returns original value as string if invalid.
    
    :param value: The value to format.
    :type value: float | int | str | any
    :return: Formatted string with '+' prefix if positive, or original value as a string if invalid.
    :rtype: str
    """
    try:
        value = float(value)
        text = f"{value:.10f}".rstrip("0").rstrip(".")
        return f"+{text}" if value > 0 else text
    except (ValueError, TypeError):
        return str(value)


def link(page:str, name:str=None) -> str:
    """
    Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages.

    :param page: The target page
    :param name: The display text of the link (optional). Defaults to `page`.
    :return: The formatted wiki link.
    """
    if name is None:
        return f"[[{page}{Language.get_subpage()}]]"
    elif page == name and Language.get() == "en":
        return f"[[{page}]]"
    else:
        return f"[[{page}{Language.get_subpage()}|{name}]]"

# @Deprecated
def format_link(name:str, page:str=None) -> str:
    """
    Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages.

    :param name: The display text of the link.
    :param page: The target page (optional). Defaults to `name`.
    :return: The formatted wiki link.
    """
    echo_deprecated("'format_link()' is deprecated, use link() instead.")
    language_code = Language.get()
    
    if language_code != "en":
        return f"[[{page or name}/{language_code}|{name}]]"
    
    if page is None or page == name:
        return f"[[{name}]]"
    else:
        return f"[[{page}|{name}]]"


def convert_percentage(value: str | int | float, start_zero=True, percentage=False) -> str:
    """Converts a numeric value to a percentage string.

    Args:
        value (str, int, float): The value to be converted to a percentage. Can be a number or a string representation of a number.
        start_zero (bool, optional): If True, treats the value as a fraction (e.g., 0.5 -> 50%).
                                     If False, assumes the value starts from 100% (e.g., 1.5 -> 150%). Defaults to True.
        percentage (bool, optional): If True, the value is already a percentage and will not be scaled. Defaults to False.

    Returns:
        str: The formatted percentage as a string with a '%' sign.
             Returns '-' for invalid inputs.
    """
    if not value or value == '-':
        return '-'
    
    try:
        value = float(value)
    except ValueError:
        return '-'
    
    if not percentage:
        if not start_zero:
            value -= 1
        value *= 100

    value = int(round(value))
    
    return f"{value}%"


def convert_int(value: int | float) -> int | float:
    """Converts a value to an integer if it has no decimal (isn't float-like)."""

    # Try to convert string to a float.
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return str(value)

    # Convert to an int if it's not float-like.
    if isinstance(value, (int, float)) and value == int(value):
        return str(int(value))

    return str(value)