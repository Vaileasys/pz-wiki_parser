from scripts.utils import echo


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


def link(page:str, name:str=None, anchor:str=None) -> str:
    """
    Returns a wiki link in the format [[Page#Anchor|Name]], including a language suffix for non-English languages.

    :param page: The target page
    :param name: The display text of the link (optional). Defaults to `page`.
    :param anchor: The section anchor within the page (optional).
    :return: The formatted wiki link.
    """
    from scripts.core.language import Language

    page_anchor = f"{page}#{anchor}" if anchor else page
    full_page = f"{page_anchor}{Language.get_subpage()}"

    if name is None:
        return f"[[{full_page}]]"
    elif page == name and Language.get() == "en" and not anchor:
        return f"[[{page}]]"
    else:
        return f"[[{full_page}|{name}]]"

# @Deprecated
def format_link(name:str, page:str=None) -> str:
    """
    Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages.

    :param name: The display text of the link.
    :param page: The target page (optional). Defaults to `name`.
    :return: The formatted wiki link.
    """
    from scripts.core.language import Language

    echo.deprecated("'format_link()' is deprecated, use link() instead.")
    language_code = Language.get()
    
    if language_code != "en":
        return f"[[{page or name}/{language_code}|{name}]]"
    
    if page is None or page == name:
        return f"[[{name}]]"
    else:
        return f"[[{page}|{name}]]"


def convert_percentage(value: str | int | float, start_zero=True, percentage=False, default=None) -> str:
    """Converts a numeric value to a percentage string.

    Args:
        value (str, int, float): The value to be converted to a percentage. Can be a number or a string representation of a number.
        start_zero (bool, optional): If True, treats the value as a fraction (e.g., 0.5 -> 50%).
                                     If False, assumes the value starts from 100% (e.g., 1.5 -> 150%). Defaults to True.
        percentage (bool, optional): If True, the value is already a percentage and will not be scaled. Defaults to False.
        default (str): The value to return for invalid input or when the percentage rounds to 0.

    Returns:
        str: The formatted percentage as a string with a '%' sign.
             Returns '-' for invalid inputs.
    """
    if not value or value == '-':
        return default if default is not None else '-'
    
    try:
        value = float(value)
    except (ValueError, TypeError):
        return default if default is not None else '-'
    
    if not percentage:
        if not start_zero:
            value -= 1
        value *= 100

    value = int(round(value))

    if value == 0:
        return default if default is not None else '0%'
    
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

def to_bool(value):
    """
    Convert a value to boolean by checking common 'true' strings.

    Args:
        value: Any value to check.

    Returns:
        bool: True if the value matches a 'true' string; False otherwise.
    """
    return str(value).lower() in ('true', 't', '1', 'yes', 'y', 'on')


def tick(text: str = None, link: str = None):
    """
    Return a wiki-formatted tick/check icon, optionally with text and link.

    Args:
        text (str, optional): Display text.
        link (str, optional): Link target.

    Returns:
        str: Formatted wiki string for the tick icon.
    """
    link = f"|link=" + link if link else ""
    text = "|" + text if text else ""
    return f"[[File:UI_Tick.png|32px{link}{text}]]"

def cross(text: str = None, link: str = None):
    """
    Return a wiki-formatted cross icon, optionally with text and link.

    Args:
        text (str, optional): Display text.
        link (str, optional): Link target.

    Returns:
        str: Formatted wiki string for the cross icon.
    """
    link = f"|link=" + link if link else ""
    text = "|" + text if text else ""
    return f"[[File:UI_Cross.png|32px{link}{text}]]"


## ------------------------- Infobox helpers ------------------------- ##

def enumerate_params(parameters):
    """
    Expand list values in a dict into numbered keys for infobox use.

    Args:
        parameters (dict): Dictionary of parameter names and values.
            List values will be split into numbered keys.

    Returns:
        dict: New dictionary with expanded numbered keys.
    """
    new_parameters = {}
    for key, value in parameters.items():
        # Remove key-value pairs if they have no value
        if not value:
            continue
        if isinstance(value, list):
            new_parameters[key] = value[0]
            for i, v in enumerate(value[1:], start=2):
                new_parameters[f"{key}{i}"] = v
        else:
            new_parameters[key] = value
    return new_parameters


def check_zero(value: int|float, default = None) -> int|float|None:
    """
    Return 'default' if the numeric value is zero, else return the value.

    Args:
        value (int or float): Value to check.
        default (optional): Value to return if input is zero.

    Returns:
        int, float, or None: Original value or 'default' if zero.
    """
    return default if float(value) == 0.0 else value