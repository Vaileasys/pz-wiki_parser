"""
Generates a wiki-formatted table of all BloodLocation values for the modding article.

This script outputs a MediaWiki table showing each BloodLocation name, the associated body parts,
and an image reference. The data is sourced directly from the BloodLocation and BodyPart classes,
and is intended for use in the PZWiki modding documentation.
"""

from scripts.objects.body_location import BloodLocation
from scripts.core.file_loading import write_file
from scripts.utils.util import link

OUTPUT_FILE = "blood_location_list.txt"

display_name_data = {}
blood_location_data = {}

TABLE_HEADER = [
    '{| class="wikitable theme-blue"',
    '! BloodLocation',
    '! Body part(s)',
    '! Visual'
    ]

IMAGE_MAP = {
    "ShirtNoSleeves": "Torso",
    "JumperNoSleeves": "Torso",
    "ShirtLongSleeves": "Jumper",
    "FullHelmet": "Head",
    "Bag": "None",
    "UpperBody": "Torso_Upper",
    "LowerBody": "Torso_Lower",
}

PART_MAP = {
    "UpperBody": "Torso_Upper",
    "LowerBody": "Torso_Lower",
    "Bag": "Back"
}

def build_links(location: BloodLocation) -> str:
    """
    Builds a single string of internal anchor links for all body parts in a BloodLocation.

    Args:
        location (BloodLocation): The location to extract links from.

    Returns:
        str: A string of wiki-formatted anchor links joined with <br> tags.
    """
    return "<br>".join(
        link(f"#{bp.body_part_id}", bp.name)
        for bp in location.body_parts
    )


def get_image(blood_location: str) -> str:
    """
    Returns the appropriate image tag for a given BloodLocation.

    Args:
        blood_location (str): The name of the BloodLocation.

    Returns:
        str: A wiki-formatted image link.
    """
    ref = IMAGE_MAP.get(blood_location, blood_location)
    return f"[[File:BodyPart_{ref}.png|62px|{blood_location}]]"


def generate_content() -> list[str]:
    """
    Builds the full wiki table content for all BloodLocations.

    Returns:
        list[str]: A list of strings representing lines of the wiki table.
    """
    content = TABLE_HEADER

    for loc in BloodLocation.all():
        content.append(f'|- id="{PART_MAP.get(loc.blood_location, loc.blood_location)}"')
        content.append(f'| <code>{loc.blood_location}</code>')
        content.append("| " + build_links(loc))
        content.append(f'| style="text-align: center;" | {get_image(loc.blood_location)}')

    content.append('|}')
    return content


def main():
    """
    Entry point for the script. Generates the table and writes it to the output file.
    """
    content = generate_content()
    write_file(content, rel_path=OUTPUT_FILE)


if __name__ == "__main__":
    main()
