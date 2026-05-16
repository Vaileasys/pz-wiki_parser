from scripts.core.file_loading import write_file
from scripts.objects.outfit import Outfit
from scripts.utils import echo

OUTPUT_FILE = "outfits_list.txt"

TABLE_HEADER = [
    '<div style="overflow: auto; white-space: nowrap;">',
    '{| class="wikitable theme-red sortable" style="text-align: center;"',
    '|-',
    '! Male image',
    '! Female image',
    '! Link',
    '! GUIDs',
]

def get_image(outfit: Outfit, sex: str) -> str:
    guid = outfit.male_guid if sex == "Male" else outfit.female_guid

    if not guid:
        return ""

    return f"[[File:outfit_{outfit.outfit_id}_{sex}.png|100px]]<br>{outfit.outfit_id}"


def get_guids(outfit: Outfit) -> str:
    guids = []

    if outfit.male_guid:
        guids.append(f"{outfit.male_guid} (male)")

    if outfit.female_guid:
        guids.append(f"{outfit.female_guid} (female)")

    return "<br>".join(guids)

def generate_content() -> list[str]:
    content = TABLE_HEADER.copy()

    for outfit in Outfit.values():
        content.append("|-")
        content.append(
            " || ".join(
                [
                    f"| {get_image(outfit, 'Male')}",
                    get_image(outfit, "Female"),
                    f"[[{outfit.page}]]",
                    get_guids(outfit),
                ]
            )
        )

    content.append("|}")
    content.append("</div>")

    return content


def generate():
    content = generate_content()

    if not content:
        echo.warning("No outfit data found to create list")
        return

    write_file(content, rel_path=OUTPUT_FILE)

if __name__ == "__main__":
    generate()