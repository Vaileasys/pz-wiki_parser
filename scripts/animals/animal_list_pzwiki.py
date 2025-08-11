"""Generates a list of animals and their breeds for PZwiki:Animal_list."""
from collections import defaultdict
from scripts.objects.animal import AnimalBreed
from scripts.core import constants, file_loading
from scripts.utils import echo

ROOT_PATH = constants.ANIMAL_DIR

TABLE_HEADERS = [
    "! Icon",
    "! Name",
    "! Stage",
    "! Animal ID",
    "! Breed ID",
]

def table_header(content: list[str]) -> None:
    content.append('{| class="wikitable theme-red sortable" style="text-align: center;"')
    content.extend(TABLE_HEADERS)

def table_row(content: list[str], row: list[str]) -> None:
    content.append("|-")
    content.extend([f"| {cell}" for cell in row])

def main():
    groups: dict[str, list[AnimalBreed]] = defaultdict(list)
    for _, breed in AnimalBreed.all().items():
        g = (breed.animal.group_link or "").strip() or "Other"
        groups[g].append(breed)

    group_names = sorted(groups.keys())
    content: list[str] = []

    for i, group_name in enumerate(group_names):
        content.append(f"=={group_name}==")

        table_header(content)

        for breed in sorted(
            groups[group_name],
            key=lambda b: (b.animal.gender.lower(), b.breed_id.lower()),
        ):
            animal = breed.animal
            row = [
                breed.icon,
                breed.wiki_link,
                animal.gender,
                animal.animal_id,
                breed.breed_id,
            ]
            table_row(content, row)

        content.append("|}")

        if i != len(group_names) - 1:
            content.append("")

    rel_path = "animal_list.txt"
    file_path = file_loading.write_file(content, rel_path=rel_path, root_path=ROOT_PATH, suppress=True)

    echo.success(f"Animal list generated to {file_path / rel_path}.")

if __name__ == "__main__":
    main()
