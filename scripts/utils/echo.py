from tqdm import tqdm

_ignore_warnings = False


def ignore_warnings(ignore: bool = True):
    global _ignore_warnings
    _ignore_warnings = ignore


def _echo_colour(message, prefix, colour_code, emit_warning=False):
    if _ignore_warnings and emit_warning:
        return

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
    _echo_colour(message, "[Warning]", "93", emit_warning=True)

def echo_error(message):
    _echo_colour(message, "[Error]", "91", emit_warning=True)

def echo_success(message):
    _echo_colour(message, "[Success]", "92")