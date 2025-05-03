import os

# Root directories
OUTPUT_DIR = os.path.join("output")
RESOURCE_DIR = os.path.join("resources")
DATA_DIR = os.path.join("data")
LUA_PATH = os.path.join(RESOURCE_DIR, "lua")

# TQDM progress bar format - 'bar_format' variable
PBAR_FORMAT = "{l_bar}{bar:30}{r_bar}"