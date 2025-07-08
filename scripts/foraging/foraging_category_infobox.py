import os
from tqdm import tqdm
from scripts.core import logger
from scripts.objects.forage import ForageCategory
from scripts.objects.skill import Skill
from scripts.utils import echo, util
from scripts.core.version import Version
from scripts.core.constants import FORAGING_DIR, PBAR_FORMAT
from scripts.core.language import Language
from scripts.core.file_loading import write_file, clear_dir

ROOT_PATH = os.path.join(FORAGING_DIR.format(language_code=Language.get()), "infoboxes")

def generate_data(category: ForageCategory) -> str:
    """
    Generates an infobox for a foraging category.

    :param category: The ForageCategory object to generate the infobox for.
    :return: A string containing the formatted infobox.
    """
    try:
        if not category:
            echo.error("No category provided for infobox generation.")
            return {}
        
        parameters = {
            "name": category.name,
            "image": f"{category.icon_raw}.png",
            "type_category": category.type_category,
            "hidden": category.is_hidden,
            "identify": f"{Skill(category.identify_perk).wiki_link} {category.identify_level}",
            "focus_chance": f"{util.convert_int(category.focus_chance_min)}–{util.convert_int(category.focus_chance_max)}" if category.focus_chance_min else None,
            "valid_floors": '<br>'.join(floor.capitalize() for floor in category.valid_floors),
            "sprite_affinity": util.split_camel_case(category.sprite_affinity).capitalize() if category.sprite_affinity else None,
            "chance_to_create_icon": f"{util.convert_int(category.chance_to_create_icon)}%" if category.chance_to_create_icon else None,
            "chance_to_move_icon": f"{util.convert_int(category.chance_to_move_icon)}%" if category.chance_to_move_icon else None,
            "has_rained_chance": f"{category.has_rained_chance}%" if category.has_rained_chance else None,
            "rain_chance": f"{category.rain_chance}%" if category.rain_chance else None,
            "snow_chance": f"{category.snow_chance}%" if category.snow_chance else None,
            "night_chance": f"{category.night_chance}%" if category.night_chance else None,
            "foraging_nav": category.zones.get("ForagingNav", 0),
            "trailer_park": category.zones.get("TrailerPark", 0),
            "birch_forest": category.zones.get("BirchForest", 0),
            "ph_forest": category.zones.get("PHForest", 0),
            "forest": category.zones.get("Forest", 0),
            "vegitation": category.zones.get("Vegitation", 0),
            "organic_forest": category.zones.get("OrganicForest", 0),
            "deep_forest": category.zones.get("DeepForest", 0),
            "pr_forest": category.zones.get("PRForest", 0),
            "town_zone": category.zones.get("TownZone", 0),
            "farm_land": category.zones.get("FarmLand", 0),
            "category_id": category.id,
            "infobox_version": Version.get()
        }

        parameters = util.enumerate_params(parameters)

        return parameters
    except Exception as e:
        logger.write(f"Error generating data for {category.id}", True, exception=e, category="error")


def build_infobox(infobox_data: dict) -> list[str]:
    """
    Builds an infobox template from the provided parameters.

    Args:
        infobox_data (dict): Dictionary of key-value infobox fields.

    Returns:
        list[str]: A list of lines forming the infobox template.
    """
    content = []
    content.append("{{Infobox foraging category")
    for key, value in infobox_data.items():
        content.append(f"|{key}={value}")
    content.append("}}")
    return content


def process_categories() -> None:
    """
    Generates infoboxes for a list of specific category IDs and writes output files.
    """ 
    clear_dir(directory=ROOT_PATH)
    for category_id, category in ForageCategory.all().items():
        infobox_data = generate_data(category)
        if not infobox_data:
            continue
        content = build_infobox(infobox_data)
        output_dir = write_file(content, category_id + ".txt", root_path=ROOT_PATH, suppress=True)
    echo.success(f"Files saved to '{output_dir}'.")


def main():
    process_categories()

if __name__ == "__main__":
    main()