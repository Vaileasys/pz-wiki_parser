import os
import traceback
from tqdm import tqdm

_ignore_warnings = False # True=Ignore warnings
_warnings_level = 3 # 0=All, 1=Error, 2=Warnings, 3=Deprecated

def ignore_warnings(ignore: bool = True, warnings_level: int = 0):
    global _ignore_warnings, _warnings_level
    _ignore_warnings = ignore
    _warnings_level = warnings_level


def _echo_colour(message, prefix, colour_code, *, emit_warning: bool = False, warnings_level: int = 3):
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

    colour_prefix = f"\033[{colour_code}m{prefix}\033[0m "
    output = f"{colour_prefix}{message}"

    if tqdm._instances:
        tqdm.write(output)
    else:
        print(output)


def echo(message):
    """Safely prints a standard message with tqdm support."""
    if tqdm._instances:
        tqdm.write(f"{message}")
    else:
        print(f"{message}")


def echo_info(message):
    _echo_colour(message, "[Info]", "96")

def echo_warning(message):
    _echo_colour(message, "[Warning]", "93", emit_warning=True, warnings_level=2)

def echo_error(message):
    _echo_colour(message, "[Error]", "91", emit_warning=True, warnings_level=1)

def echo_success(message):
    _echo_colour(message, "[Success]", "92")

def echo_debug(message):
    _echo_colour(message, "[Debug]", "95")

def echo_deprecated(message):
    _echo_colour(message, "[Deprecated]", "95", emit_warning=True, warnings_level=3)
