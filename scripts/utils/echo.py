"""
Console logging utilities with coloured output, warning control, and tqdm support.
"""
import os
import traceback
from tqdm import tqdm
from scripts.utils import color

_ignore_warnings = False # True=Ignore warnings
_warnings_level = 3 # 0=All, 1=Error, 2=Warnings, 3=Deprecated

def _message(message: str, prefix: str, style_func, *, emit_warning: bool = False, warnings_level: int = 3):
    """
    Print a coloured message with optional warning metadata.

    Args:
        message (str): The message text to display.
        prefix (str): Label prefix (e.g., "[Info]", "[Warning]").
        style_func (callable): A function that applies styling (e.g., color.info).
        emit_warning (bool, optional): Whether to append stack info for warnings.
        warnings_level (int, optional): Warning level threshold for display.
    """
    if emit_warning:
        if _ignore_warnings and warnings_level > _warnings_level:
            return
    
    if emit_warning:
        stack = traceback.extract_stack()
        tb = stack[-4] if len(stack) >= 4 else stack[-3]
        filename, lineno, func, _ = tb
        
        if func == "<module>":
            func = os.path.splitext(os.path.basename(filename))[0]

        base_dir = os.path.abspath(os.getcwd())
        abs_path = os.path.abspath(filename)
        try:
            rel_path = os.path.relpath(abs_path, base_dir)
        except ValueError:
            rel_path = os.path.basename(filename)

        message += f" (File {rel_path}, line {lineno}, in {func})"

    output = f"{style_func(prefix)} {message}"

    if tqdm._instances:
        tqdm.write(output)
    else:
        print(output)

def ignore_warnings(warnings_level: int = 0, ignore: bool = True):
    """
    Enable or disable warning output filtering by level.

    Args:
        warnings_level (int): Minimum warning level to show.
        ignore (bool): Whether to suppress warnings below the level.
    """
    global _ignore_warnings, _warnings_level
    _ignore_warnings = ignore
    _warnings_level = warnings_level

def write(message: str, style_func=None):
    """
    Print a standard message safely, supporting tqdm progress bars.

    Args:
        message (str): The message text to print.
        style_func (callable, optional): A colour/style function (e.g. color.info).
    """
    output = style_func(message) if style_func else message

    if tqdm._instances:
        tqdm.write(f"{output}")
    else:
        print(f"{output}")

def info(message: str):
    """
    Print an informational message in cyan.

    Args:
        message (str): The message text to display.
    """
    _message(message, "[Info]", color.info)

def warning(message: str):
    """
    Print a warning message in yellow with warning context.

    Args:
        message (str): The warning text to display.
    """
    _message(message, "[Warning]", color.warning, emit_warning=True, warnings_level=2)

def error(message: str):
    """
    Print an error message in red with error context.

    Args:
        message (str): The error text to display.
    """
    _message(message, "[Error]", color.error, emit_warning=True, warnings_level=1)

def success(message: str):
    """
    Print a success message in green.

    Args:
        message (str): The success message to display.
    """
    _message(message, "[Success]", color.success)

def debug(message: str):
    """
    Print a debug message in magenta if debug mode is enabled.

    Args:
        message (str): The debug text to display.
    """
    from scripts.core import config_manager as config
    debug_mode = config.get_debug_mode()

    if debug_mode:
        _message(message, "[Debug]", "95")

def deprecated(message: str):
    """
    Print a deprecation warning in magenta with warning context.

    Args:
        message (str): The deprecation message to display.
    """
    _message(message, "[Deprecated]", color.debug, emit_warning=True, warnings_level=3)