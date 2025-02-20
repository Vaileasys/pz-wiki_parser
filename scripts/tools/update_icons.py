# Tool used to update/create the 'sprite_list.json' file

from pathlib import Path
from scripts.core import utility

RESOURCES_DIR = Path("resources")
ICON_DIR = Path("resources/icons")

def update_sprite_list():
    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    
    png_dict = {}
    
    for file in ICON_DIR.glob('*.png'):
        filename = file.name
        
        if "_" in filename:
            prefix, name = filename.split("_", 1)
        else:
            prefix, name = "Other", filename
        
        if prefix not in png_dict:
            png_dict[prefix] = []
        png_dict[prefix].append(name)
    
    for prefix, files in png_dict.items():
        print(f"{prefix}: {len(files)} files")
    
    utility.save_cache(png_dict, "sprite_list.json", RESOURCES_DIR)

if __name__ == "__main__":
    update_sprite_list()
