import re
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


def convert_percentage(value: str | int | float, start_zero=True, percentage=False, default=None, decimals: int = 0) -> str:
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

    if round(value, decimals) == 0:
        return default if default is not None else '0%'

    return f"{value:.{decimals}f}%"


def convert_int(value: int | float) -> int | float:
    """Converts a value to an integer if it has no decimal (isn't float-like)."""

    if isinstance(value, (int, float)):
        return int(value) if value == int(value) else float(value)

    if isinstance(value, str):
        try:
            num = float(value)
            return int(num) if num == int(num) else num
        except ValueError:
            pass

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


def flip_data(data: dict) -> dict:
    """
    Flip a flat dictionary so that values become keys, and keys become values.
    If multiple keys share the same value, they are grouped in a list.

    Args:
        data (dict): A flat dictionary to flip. All values must be hashable.

    Returns:
        dict: A new dictionary with values as keys and lists of original keys as values.

    Raises:
        TypeError: If 'data' is not a dictionary or a value is unhashable.
    """
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary.")
    
    flipped = {}
    for key, value in data.items():
        if value not in flipped:
            flipped[value] = []
        flipped[value].append(key)
    return flipped


def deep_getattr(obj: object, attr_path: str, default=None):
    """
    Access nested attributes on an object using dot‑notation.

    Args:
        obj: The object to fetch attributes from.
        attr_path: A string of attribute names separated by '.', e.g. "fluid_container.capacity" - the path to the desired value.
        default: A fallback value returned if any attribute in the path doesn't exist or its value is `None`.

    Returns:
        The value found at the end of the attribute path, or `default` if any intermediate attribute is missing or `None`.
    """
    for attr in attr_path.split('.'):
        if obj is None:
            return default
        obj = getattr(obj, attr, default)
        if obj is default:
            return default
    return obj


def calculate_drain_rate(use_delta: float, unit: str = "hour", tick_minutes: int = 1, as_percentage: bool = False) -> str | float:
    """
    Calculates how much of a drainable item is consumed over time.

    Args:
        use_delta (float): Radio UseDelta value from item script (e.g., 0.014 for 1.4% per hour).
        as_percentage (bool): Return as a percentage string (default False).
        unit (str): Time unit to calculate ('minute', 'hour', 'day').
        as_percentage (bool): Return as a percentage string (default False).

    Returns:
        str | float: Battery drain over the given time unit.
    """
    unit_minutes = {"minute": 1, "hour": 60, "day": 1440}
    if unit not in unit_minutes:
        raise ValueError(f"Invalid unit '{unit}'.")

    # Adjust per-minute drain to reflect tick duration
    per_tick = use_delta * (tick_minutes / 60)
    drain_fraction = per_tick * (unit_minutes[unit] / tick_minutes)

    if as_percentage:
        return convert_percentage(drain_fraction, start_zero=True, decimals=1)

    return round(drain_fraction, 3)


def convert_unit(value: float, unit: str, start_prefix: str = "", force_prefix: str = None) -> str:
    """
    Convert a value from a given SI prefix (default: base) to the most appropriate SI prefix
    between milli (m) and Mega (M), or force it to a specific one.

    Args:
        value (float): The numeric value to convert.
        unit (str): The unit to append after the converted value.
        start_prefix (str, optional): The starting SI prefix (default ""). One of: "m", "", "k", "M".
        force_prefix (str, optional): If set, force output to this SI prefix. Skips automatic scaling.

    Returns:
        str: A human-readable string with the chosen prefix and unit.
    """
    prefixes = ["m", "", "k", "M"]
    factors = {"m": 0.001, "": 1, "k": 1_000, "M": 1_000_000}

    if start_prefix not in prefixes:
        raise ValueError(f"Invalid start prefix '{start_prefix}'. Use one of: {', '.join(prefixes)}")
    if force_prefix and force_prefix not in prefixes:
        raise ValueError(f"Invalid force prefix '{force_prefix}'. Use one of: {', '.join(prefixes)}")

    base_value = value * factors[start_prefix]

    if force_prefix:
        scaled = base_value / factors[force_prefix]
        return f"{convert_int(scaled)} {force_prefix}{unit}"

    start_index = prefixes.index(start_prefix)

    for prefix in reversed(prefixes[:start_index + 3]):
        factor = factors[prefix]
        if abs(base_value) >= factor or prefix == "m":
            scaled = base_value / factor
            return f"{convert_int(scaled)} {prefix}{unit}"

    return f"{base_value} {prefixes[start_index]}{unit}"


def split_camel_case(text: str) -> str:
    """
    Add spaces between words in a camel case string.

    Args:
        text (str): A camelCase or PascalCase string.

    Returns:
        str: The string with spaces added between words.
    """
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)


def tick(text: str = None, link: str = None):
    """
    Return a wiki-formatted tick/check icon, optionally with text and link.

    Args:
        text (str, optional): Display text.
        link (str, optional): Link target.

    Returns:
        str: Formatted wiki string for the tick icon.
    """
    from scripts.core.language import Language
    link = f"|link={link}{Language.get_subpage()}" if link else ""
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
    from scripts.core.language import Language
    link = f"|link={link}{Language.get_subpage()}" if link else ""
    text = "|" + text if text else ""
    return f"[[File:UI_Cross.png|32px{link}{text}]]"

def rgb(red: int | float = 0, green: int | float = 0, blue: int | float = 0):
    """
    Return an rgb template string with the given colour values.

    Each colour component can be specified as either:
      - An int (0–255), representing the raw RGB value.
      - A float (0.0–1.0), representing a normalised fraction which will be scaled to 0–255.

    Args:
        red (int | float): Red component (default: 0).
        green (int | float): Green component (default: 0).
        blue (int | float): Blue component (default: 0).

    Returns:
        str: A string formatted as '{{rgb|R, G, B}}' where R, G, and B are integers.
    """
    def convert(value):
        if isinstance(value, float):
            return round(value * 255)
        return int(value)
    
    r = convert(red)
    g = convert(green)
    b = convert(blue)
    return f"{{{{rgb|{r}, {g}, {b}}}}}"
    


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