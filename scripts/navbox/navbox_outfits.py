from pathlib import Path

from scripts.navbox.navbox import Navbox
from scripts.objects.outfit import Outfit
from scripts.utils import echo


    
OUTPUT_FILENAME = "outfits.json"

def build_outfit_navbox(section_order: list[str] | None = None) -> Navbox:
    navbox = Navbox("Outfits")

    for outfit in Outfit.values():
        if not outfit.valid:
            echo.warning(f"Skipping invalid outfit: {outfit.outfit_id}")
            continue

        navbox.add_item(outfit.navbox_section, outfit.page)

    navbox.sort(items=True, sections=False)

    if section_order:
        navbox.sort_sections_by_order(section_order)

    return navbox

def generate_outfit_navbox(output_dir: str | Path | None = None, section_order: list[str] | None = None) -> Path:
    
    SECTION_ORDER = [
        "Unisex outfits",
        "Male outfits",
        "Female outfits",
    ]
    
    navbox = build_outfit_navbox(section_order=section_order or SECTION_ORDER)
    path = navbox.save(OUTPUT_FILENAME, output_dir=output_dir)

    echo.success(f"Saved outfit navbox: {path}")
    return path


def main():
    generate_outfit_navbox()


if __name__ == "__main__":
    main()