import os
from pathlib import Path

# Root directories
PROJECT_ROOT = str(Path(__file__).parent.parent.parent.resolve())
OUTPUT_DIR = os.path.join("output")
RESOURCE_DIR = os.path.join("resources")
DATA_DIR = os.path.join("data")
DOCS_DIR = os.path.join("docs")

LUA_PATH = os.path.join(RESOURCE_DIR, "lua")
LUA_STUB_PATH = os.path.join(LUA_PATH, "stubs")

# Resource directories
TABLES_DIR = os.path.join(RESOURCE_DIR, "tables")

# Output directories
LOGGING_DIR = os.path.join(OUTPUT_DIR, "logging")
DIFF_DIR = os.path.join(OUTPUT_DIR, "diffs")

OUTPUT_LANG_DIR = os.path.join(OUTPUT_DIR, "{language_code}") # Assign a language code with 'OUTPUT_LANG_DIR.format(language_code=Language.get())'
VEHICLE_DIR = os.path.join(OUTPUT_LANG_DIR, "vehicle")
ITEM_DIR = os.path.join(OUTPUT_LANG_DIR, "item")
FLUID_DIR = os.path.join(OUTPUT_LANG_DIR, "fluid")
TAGS_DIR = os.path.join(OUTPUT_LANG_DIR, "tags")
FIXING_DIR = os.path.join(OUTPUT_LANG_DIR, "fixing")
RECIPES_DIR = os.path.join(OUTPUT_LANG_DIR, "recipes")
FORAGING_DIR = os.path.join(OUTPUT_LANG_DIR, "foraging")
ANIMAL_DIR = os.path.join(OUTPUT_LANG_DIR, "animal")

# Data directories
CACHE_DIR = os.path.join(DATA_DIR, "cache")
SNAPSHOT_DIR = os.path.join(DATA_DIR, "snapshots")

# TQDM progress bar format - 'bar_format' variable
PBAR_FORMAT = "{l_bar}{bar:30}{r_bar}"

# Other
BOT_FLAG = "<!-- Bot_flag|type={type}|id={id} -->"
BOT_FLAG_END = "<!-- Bot_flag_end|type={type}|id={id} -->"
