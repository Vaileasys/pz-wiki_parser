import os

# Root directories
OUTPUT_DIR = os.path.join("output")
RESOURCE_DIR = os.path.join("resources")
DATA_DIR = os.path.join("data")

LUA_PATH = os.path.join(RESOURCE_DIR, "lua")

# Output directories
LOGGING_DIR = os.path.join(OUTPUT_DIR, "logging")

OUTPUT_LANG_DIR = os.path.join(OUTPUT_DIR, "{language_code}") # Assign a language code with 'OUTPUT_LANG_DIR.format(language_code=Language.get())'
VEHICLE_DIR = os.path.join(OUTPUT_LANG_DIR, "vehicle")
ITEM_DIR = os.path.join(OUTPUT_LANG_DIR, "item")
FLUID_DIR = os.path.join(OUTPUT_LANG_DIR, "fluid")
TAGS_DIR = os.path.join(OUTPUT_LANG_DIR, "tags")
FIXING_DIR = os.path.join(OUTPUT_LANG_DIR, "fixing")
RECIPES_DIR = os.path.join(OUTPUT_LANG_DIR, "recipes")

# TQDM progress bar format - 'bar_format' variable
PBAR_FORMAT = "{l_bar}{bar:30}{r_bar}"