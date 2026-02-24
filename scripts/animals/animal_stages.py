import os
from scripts.objects.animal import AnimalBreed
from scripts.core import constants, file_loading

STAGES_DIR = os.path.join(constants.ANIMAL_DIR, "stages")

def table_row(content: list):
    return [f"| {data}" for data in content]

def main():
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

if __name__ == "__main__":
    main()