from pathlib import Path
from scripts.core.language import Language
from scripts.objects.forage import ForageSkill, ForageCategory
from scripts.objects.profession import Occupation, Trait
from scripts.core.constants import FORAGING_DIR, BOT_FLAG, BOT_FLAG_END
from scripts.core.file_loading import write_file, clear_dir
from scripts.utils import echo, util

root_dir = Path(FORAGING_DIR.format(language_code=Language.get()))


def generate_data(profession: Occupation | Trait, category: ForageCategory) -> dict:
    parameters = {
        "sort_key": profession.page,
        "icon": profession.icon,
        "name": profession.wiki_link,
        "cost": profession.cost,
        "factor": "-",
        "vision_bonus": "-",
        "darkness_effect": "-",
        "weather_effect": "-"
    }
    if ForageSkill.exists(profession.id):
        forage_skill = ForageSkill(profession.id)
        parameters["factor"] = util.convert_percentage(forage_skill.specialisations.get(category), False, True) or "-"
        parameters["vision_bonus"] = util.format_positive(forage_skill.vision_bonus) if forage_skill.vision_bonus else "-"
        parameters["darkness_effect"] = f"-{forage_skill.darkness_effect}%" if forage_skill.darkness_effect else "-"
        parameters["weather_effect"] = f"-{forage_skill.weather_effect}%" if forage_skill.weather_effect else "-"

    return parameters


def build_table(data_list: list, category: str, prof_type: str, root_path: str):
    if not data_list:
        echo.debug(f"Skipping {prof_type} table for '{category}' as no data was found.")
        return

    content = [
        BOT_FLAG.format(type=f"foraging_{prof_type}", id=category),
        "{| class=\"wikitable theme-red sortable\" style=\"text-align: center;\"",
        "! Icon",
        "! Name",
        "! Cost",
        "! Detection bonus", #specialisations
        "! Vision bonus (tiles)", #visonBonus
        "! Darkness effect", #darknessEffect
        "! Weather effect" #weatherEffect
    ]

    for row in data_list:
        content.append("|-")
        for key, value in row.items():
            content.append(f"| {value}")
    
    content.append("|}")
    content.append(BOT_FLAG_END.format(type=f"{prof_type}_table", id=category))

    rel_path = category + ".txt"

    write_file(content, rel_path=rel_path, root_path=str(root_path), suppress=True)


def main():
    occupation_name = "occupation"
    trait_name = "trait"
    occupation_path = str(root_dir / (occupation_name + "_table"))
    trait_path = str(root_dir / (trait_name + "_table"))

    clear_dir(occupation_path)
    clear_dir(trait_path)

    for category_id, category in ForageCategory.all().items():
        # Occupations
        occupation_rows = [generate_data(o, category) for o in category.occupations]
        occupation_rows.sort(key=lambda r: (r.get("sort_key") or "").casefold())
        occupation_rows = [{k: v for k, v in r.items() if k != "sort_key"} for r in occupation_rows]
        build_table(occupation_rows, category_id, occupation_name, occupation_path)

        # Traits
        trait_rows = [generate_data(t, category) for t in category.traits]
        trait_rows.sort(key=lambda r: (r.get("sort_key") or "").casefold())
        trait_rows = [{k: v for k, v in r.items() if k != "sort_key"} for r in trait_rows]
        build_table(trait_rows, category_id, trait_name, trait_path)
    
    echo.success(f"Occupation files saved to '{occupation_path}'.")
    echo.success(f"Trait files saved to '{trait_path}'.")


if __name__ == "__main__":
    main()