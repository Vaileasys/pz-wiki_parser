import os
from scripts.objects.animal import AnimalBreed, Animal
from scripts.core import constants, file_loading, cache

STAGES_DIR = os.path.join(constants.ANIMAL_DIR, "stages")
GROUP_BREEDS_DIR = os.path.join(constants.ANIMAL_DIR, "group_breeds")

def table_row(content: list):
    return [f"| {data}" for data in content]


def generate_breed():
    """Generate animal stages wiki tables per breed."""
    for full_breed_id, breed in AnimalBreed.all().items():
        stages = breed.animal.stages

        content = []

        bot_flag_start = constants.BOT_FLAG.format(type=f"stages", id=breed.full_breed_id)
        bot_flag_end = constants.BOT_FLAG_END.format(type=f"stages", id=breed.full_breed_id)

        content.append(bot_flag_start)
        content.append('{| class="wikitable theme-red"')
        content.extend([
            "! Icon",
            "! Name",
            "! Stage",
            "! Min. age",
            "! Max. age",
            "! Full breed ID"
        ])

        content_dict = {}

        for stage_id in stages:

            stage_key = stage_id + breed.breed_id

            stage = AnimalBreed.from_key(stage_key)

            animal = stage.animal

            row = [
                stage.icon,
                stage.wiki_link,
                animal.gender,
                animal.min_age,
                animal.max_age,
                stage.full_breed_id
            ]

            gender = "baby" if animal.baby else "male" if animal.male else "female" if animal.female else None

            content_dict[gender] = table_row(row)
        
        content.append("|-")
        content.extend(content_dict["baby"])
        content.append("|-")
        content.extend(content_dict["female"])
        content.append("|-")
        content.extend(content_dict["male"])
        
        content.append("|}")
        content.append(bot_flag_end)
        
        file_loading.write_file(content, rel_path=f"{full_breed_id}.txt", root_path=STAGES_DIR)
    
    return


def generate_group():
    """Generate animal stages wiki tables per group."""
    # group -> {breed_id: breed}
    groups: dict[str, dict[str, AnimalBreed]] = {}
    
    for animal in Animal.all().values():
        group_breeds = groups.setdefault(animal.group, {})

        for breed in animal.breeds:
            # Deduplicate breeds per group by breed_id
            group_breeds[breed.breed_id] = breed

    for group, breeds_map in groups.items():
        breeds = list(breeds_map.values())
        content = []

        bot_flag_start = constants.BOT_FLAG.format(type="group_breeds", id=group)
        bot_flag_end = constants.BOT_FLAG_END.format(type="group_breeds", id=group)

        content.append(bot_flag_start)
        content.append('{| class="wikitable theme-red"')
        content.extend([
            "! Icon",
            "! Name",
            "! Breed",
            "! Stage",
            "! Min. age",
            "! Max. age",
            "! Full breed ID",
        ])

        gender_rows = {"baby": [], "female": [], "male": [], "other": []}
        seen = set()

        for breed in sorted(breeds, key=lambda x: (x.name or "", x.breed_id or "")):
            for stage_id in breed.animal.stages:
                stage = AnimalBreed.from_key(stage_id + breed.breed_id)
                animal = stage.animal

                unique_key = stage.full_breed_id
                if unique_key in seen:
                    continue
                seen.add(unique_key)

                row = [
                    stage.icon,
                    stage.wiki_link,
                    breed.breed_name,
                    animal.gender,
                    animal.min_age,
                    animal.max_age,
                    stage.full_breed_id,
                ]

                if animal.baby:
                    gender = "baby"
                elif animal.female:
                    gender = "female"
                elif animal.male:
                    gender = "male"
                else:
                    gender = "other"

                gender_rows[gender].append(table_row(row))

        for gender in ("baby", "female", "male", "other"):
            for row_lines in gender_rows[gender]:
                content.append("|-")
                content.extend(row_lines)

        content.append("|}")
        content.append(bot_flag_end)
        
        file_loading.write_file(content, rel_path=f"{group}.txt", root_path=GROUP_BREEDS_DIR)
    
    


def main():
    generate_breed()
    generate_group()

if __name__ == "__main__":
    main()