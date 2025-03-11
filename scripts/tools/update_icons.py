# Tool used to update/create the 'sprite_list.json' file

import shutil
from pathlib import Path
from scripts.core import utility
from scripts.core.constants import RESOURCE_PATH

RESOURCES_DIR = Path(RESOURCE_PATH)
ICON_DIR = RESOURCES_DIR / "icons"
NEW_ICON_DIR = ICON_DIR / "new_textures"
ICON_FILE = "sprite_list.json"
SPRITE_LIST_FILE = RESOURCES_DIR / ICON_FILE


def load_existing_textures():
    if SPRITE_LIST_FILE.exists():
        return utility.load_cache(SPRITE_LIST_FILE)
    return {}

def update_textures_list():
    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    
    existing_textures = load_existing_textures()
    
    png_dict = {}
    new_textures = {}
    
    for file in ICON_DIR.glob('*.png'):
        filename = file.name
        
        if "_" in filename:
            prefix, name = filename.split("_", 1)
        else:
            prefix, name = "Other", filename
        
        if prefix not in png_dict:
            png_dict[prefix] = []
        
        if name not in png_dict[prefix]:
            png_dict[prefix].append(name)
        
        # Check if the icon is new
        if prefix not in existing_textures or name not in existing_textures.get(prefix, []):
            if prefix not in new_textures:
                new_textures[prefix] = []
            new_textures[prefix].append(name)
        
            # Copy new icon to new_textures folder
            prefix_dir = NEW_ICON_DIR / prefix
            prefix_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(file, prefix_dir / name)
    
    for prefix, files in png_dict.items():
        print(f"{prefix}: {len(files)} files")
    
    utility.save_cache(png_dict, ICON_FILE, RESOURCES_DIR)
    
    if new_textures:
        utility.save_cache(new_textures, "new_textures.json")
        for prefix, files in new_textures.items():
            print(f"{prefix}: {len(files)} new textures found")

if __name__ == "__main__":
    update_textures_list()
