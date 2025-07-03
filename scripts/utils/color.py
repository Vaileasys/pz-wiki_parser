"""
ANSI terminal styling helpers for coloured and formatted text output.

Includes basic styles, colours, and helper functions like `error()`, `warning()`, and `info()`.
"""
# Text styles
RESET       = "\033[0m"
BOLD        = "\033[1m"
DIM         = "\033[2m"
ITALIC      = "\033[3m"
UNDERLINE   = "\033[4m"
BLINK       = "\033[5m"
REVERSE     = "\033[7m"
HIDDEN      = "\033[8m"
STRIKETHROUGH = "\033[9m"

# Regular colours
BLACK       = "\033[30m"
RED         = "\033[31m"
GREEN       = "\033[32m"
YELLOW      = "\033[33m"
BLUE        = "\033[34m"
MAGENTA     = "\033[35m"
CYAN        = "\033[36m"
WHITE       = "\033[37m"

# Bright colours
BRIGHT_BLACK   = "\033[90m"
BRIGHT_RED     = "\033[91m"
BRIGHT_GREEN   = "\033[92m"
BRIGHT_YELLOW  = "\033[93m"
BRIGHT_BLUE    = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN    = "\033[96m"
BRIGHT_WHITE   = "\033[97m"

# Background colours
BG_BLACK     = "\033[40m"
BG_RED       = "\033[41m"
BG_GREEN     = "\033[42m"
BG_YELLOW    = "\033[43m"
BG_BLUE      = "\033[44m"
BG_MAGENTA   = "\033[45m"
BG_CYAN      = "\033[46m"
BG_WHITE     = "\033[47m"

# Bright background colours
BG_BRIGHT_BLACK   = "\033[100m"
BG_BRIGHT_RED     = "\033[101m"
BG_BRIGHT_GREEN   = "\033[102m"
BG_BRIGHT_YELLOW  = "\033[103m"
BG_BRIGHT_BLUE    = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN    = "\033[106m"
BG_BRIGHT_WHITE   = "\033[107m"

## ------------------- Style Helpers ------------------- ##

def style(text: str, *styles: str) -> str:
    """Apply one or more styles to a string."""
    return f"{''.join(styles)}{text}{RESET}"

## ------------------- Preset Styles ------------------- ##

def error(text: str) -> str:
    return style(text, RED, BOLD)

def warning(text: str) -> str:
    return style(text, YELLOW)

def success(text: str) -> str:
    return style(text, GREEN)

def info(text: str) -> str:
    return style(text, CYAN)

def dimmed(text: str) -> str:
    return style(text, DIM)

def debug(text: str) -> str:
    return style(text, BRIGHT_MAGENTA, BOLD)
