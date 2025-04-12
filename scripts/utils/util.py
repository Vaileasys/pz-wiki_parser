from scripts.core.language import Language


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


def format_link(name:str, page:str=None) -> str:
    """
    Returns a wiki link in the format [[Page|Name]], including a language suffix for non-English languages.

    :param name: The display text of the link.
    :param page: The target page (optional). Defaults to `name`.
    :return: The formatted wiki link.
    """
    language_code = Language.get()
    
    if language_code != "en":
        return f"[[{page or name}/{language_code}|{name}]]"
    
    if page is None or page == name:
        return f"[[{name}]]"
    else:
        return f"[[{page}|{name}]]"