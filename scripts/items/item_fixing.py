"""
Processes and generates [Fixing](https://pzwiki.net/wiki/Template:Fixing) templates for items.

This script extracts fixing data, formats it into wiki templates, and saves individual
.txt files for each item-fixing combination under the `items/fixing/` directory.

The output is in the following MediaWiki format:

Example:
    {{Fixing
    |name=JS-2000 Shotgun
    |item_id=Base.Shotgun
    |fixer1=[[JS-2000 Shotgun]]
    |fixer1_value=1
    |fixer1_skill=2 [[Aiming]]
    |fixer2=[[Sawed-off JS-2000 Shotgun]]
    |fixer2_value=1
    |fixer2_skill=2 [[Aiming]]
    }}

    {{Fixing
    |name=Hood (Standard Vehicle)
    |item_id=Base.EngineDoor1
    |global_item=[[Welding Torch]]
    |global_item_value=2
    |fixer1=[[Steel Sheet]]
    |fixer1_value=1
    |fixer1_skill=1 [[Welding]]<br>2 [[Mechanics]]
    |fixer2=[[Steel Sheet - Small]]
    |fixer2_value=2
    |fixer2_skill=1 [[Welding]]<br>2 [[Mechanics]]
    |condition_modifier=120%
    }}
"""

import os
from tqdm import tqdm
from scripts.core.constants import PBAR_FORMAT, ITEM_DIR
from scripts.core.file_loading import write_file
from scripts.objects.item import Item
from scripts.objects.fixing import Fixing, Fixer
from scripts.core.language import Language
from scripts.utils import echo

FIXING_DIR = os.path.join(ITEM_DIR.format(language_code=Language.get()), "fixing")

def process_fixers(fixers: list[Fixer]) -> dict:
    """
    Process a list of Fixer objects into a dictionary of wiki template values.

    Args:
        fixers (list[Fixer]): List of fixer items used for a single fixing entry.

    Returns:
        dict: A dictionary with fixer names, quantities, and skill requirements, formatted for wiki template usage.
    """
    result = {}

    for i, fixer in enumerate(fixers, start=1):
        key = f"fixer{i}"
        result[key] = fixer.item.wiki_link
        result[f"{key}_value"] = fixer.amount

        if fixer.skills:
            skill_lines = [
                f"{fixer.get_skill_level(skill)} {skill.wiki_link}"
                for skill in fixer.skills
            ]
            result[f"{key}_skill"] = "<br>".join(skill_lines)

    return result


def generate_data(item: Item, fixing: Fixing):
    """
    Generate the base data dictionary for a fixing wiki template.

    Args:
        item (Item): The item this fixing applies to.
        fixing (Fixing): The corresponding fixing object.

    Returns:
        dict: A dictionary of all relevant wiki template keys and values.
    """
    template = {}
    template["name"] = item.name
    template["item_id"] = item.item_id

    if fixing.global_items:
        global_item = fixing.global_items[0]
        template["global_item"] = global_item.item.wiki_link
        template["global_item_value"] = global_item.amount

    if fixing.fixers:
        template.update(process_fixers(fixing.fixers))
    
    if fixing.condition_modifier != 1.0:
        template["condition_modifier"] = f"{round(fixing.condition_modifier * 100)}%"

    return template


def generate_template(data: dict):
    """
    Convert a fixing data dictionary into a list of lines representing a wiki template.

    Args:
        data (dict): The fixing data to embed in the template.

    Returns:
        list[str]: Lines forming the complete {{Fixing}} wiki template.
    """
    content = []

    content.append("{{Fixing")

    for key, value in data.items():
        content.append(f"|{key}={value}")
    
    content.append("}}")

    return content


def main(batch=False):
    """
    Generate and save {{Fixing}} templates for all items with fixings.

    Args:
        batch (bool): If True, skip language loading (for batch processing).
    """
    if not batch:
        Language.get() #Ensure language is loaded

    file_count = 0

    fixings = Fixing.all()
    with tqdm(total=Fixing.count(), desc="Processing fixing recipes", unit=" recipes", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        for fixing_id in fixings:
            fixing = Fixing(fixing_id)

            for item in fixing.requires:
                data = generate_data(item, fixing)
                content = generate_template(data)
                filename = f"{item.item_id}_{fixing.fixing_id}.txt"

                file_count += 1

                write_file(content, rel_path=filename, root_path=FIXING_DIR, suppress=True)

            pbar.update(1)
    
    echo.success(f"Saved {file_count} files to '{FIXING_DIR}'")


if __name__ == "__main__":
    main()