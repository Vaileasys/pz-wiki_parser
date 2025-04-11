import os
import traceback
from scripts.core.constants import OUTPUT_PATH

LOG_PATH = f"{OUTPUT_PATH}\\logging"
DEF_FILE = "log.txt"
is_first_log = True


def get_log_path(file_name=DEF_FILE):
    return os.path.join(LOG_PATH, file_name)


def init_log_file(file_name="log.txt"):
    """Initialise log file erasing existing contents"""
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, 'w') as file:
        file.write("")


def write(message, print_bool=False, file_name=DEF_FILE, exception=None):
    """Used to log important info to a log file"""
    from scripts.utils.util import echo # lazy import to avoid import loop
    global is_first_log
    file_name = get_log_path(file_name)

    # If this is the first log, initialise the log file
    if is_first_log:
        init_log_file(file_name)
        is_first_log = False

    if exception is not None:
        tb = traceback.extract_tb(exception.__traceback__)
        filename, lineno, func, text = tb[-1]

        # Get the current working directory
        base_dir = os.path.abspath(os.getcwd())
        abs_path = os.path.abspath(filename)

        # Get the relative path from the working dir
        try:
            rel_path = os.path.relpath(abs_path, base_dir)
        except ValueError:
            # If relpath fails just use filename
            rel_path = os.path.basename(filename)

        post_message = f": {exception} (File {rel_path}, line {lineno}, in {func})"
    else:
        post_message = ""


    if print_bool:
        echo(f"{message}{post_message}")

    with open(file_name, 'a') as file:
        file.write(f"{message}{post_message}\n")