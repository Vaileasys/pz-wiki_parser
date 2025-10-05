import os
import math
from tqdm import tqdm

from scripts.core.constants import ANIMAL_DIR, PBAR_FORMAT
from scripts.core.language import Language
from scripts.core.version import Version
from scripts.utils import echo, util
from scripts.core.file_loading import write_file, load_file

from scripts.objects.animal import Animal, AnimalBreed
from scripts.animals import animal_infobox, animal_products, animal_stages, animal_genes, animal_food

ANIM_DIR = ANIMAL_DIR.format(language_code=Language.get())
article = "a" # A grammatical article, either "A" or "An"

def generate_header(breed: AnimalBreed):
    """
    Generates the header for the article.
    """
    header = "{{{{Header|Project Zomboid|World|AI|Animals|{category}}}}}"
    page_version = f"{{{{Page version|{Version.get()}}}}}"

    group_name = breed.animal.group_name_en
    category_plural = {
        "Sheep": "Sheep",
        "Mouse": "Mice",
        "Deer": "Deer"
    }
    category = group_name + "s" if group_name not in category_plural else category_plural[group_name]
    header = header.format(category=category)

    return [header, page_version]

def generate_intro(breed: AnimalBreed):
    """
    Generates the introduction for the article.
    """
    global article
    name = breed.name
    group = util.link(breed.animal.page, breed.animal.group_name.lower())

    article = "an" if name[0].lower() in "aeiou" else "a"

    return [f"{article.capitalize()} '''{name}''' is an {util.link("animal")} in the {group} group."]

def generate_overview(breed: AnimalBreed):
    content = []
    content.append(f"{article.capitalize()} {breed.name} is a {breed.animal.gender.lower()} {breed.animal.group_link} of the {breed.breed_name} breed.")

    return content

def generate_behaviour(breed: AnimalBreed):
    """
    Generates the behaviour section for the article.
    """
    def check_first():
        """
        Checks if this is the first section being added, and adds a newline if not.
        """
        nonlocal is_first
        nonlocal content
        if is_first:
            is_first = False
            return
        content.append("")
        return
    
    is_first = True

    animal = breed.animal

    content = []

    # === Feeding and luring ===
    feeding_content = []
    if animal.food_types and not (animal.baby and animal.eat_from_mother):
        feeding_content.append(f"This animal can be fed or lured with the following food types:")
        feeding_content.extend(load_file(rel_path=os.path.join(breed.full_breed_id + ".txt"), root_path=animal_food.ANIMAL_FOOD_DIR))
#        for food_type, value_type in animal.food_types.items():
#            if value_type == "Unknown":
#                continue
#            if value_type == "All":
#                feeding_content.append(f"* All [[food]] types")
#            else:
#                feeding_content.append(f"* {food_type} ({value_type})")
        feeding_content.append("The chance of successfully luring an animal depends on the animal's acceptance towards the player and its stress level.")

        if animal.eat_grass:
            feeding_content.append("\nIf there is no trough for it to eat from, it will try to eat from the [[grass]] instead, however it will not grow as big or produce as many resources.")
    
    if animal.baby:
        if animal.eat_from_mother and breed.milk_type and breed.milk_type.valid:
            milk = breed.milk_type
            feeding_content.append(f"As a baby, it will drink milk from its mother. If it does not have a mother, it must be fed by the player with {milk.wiki_link}.")
        elif animal.eat_from_mother is True:
            feeding_content.append(f"As a baby, it will drink milk from its mother. If it does not have a mother, it will eventually starve to death, so long as it is within a [[Animal#Livestock zone|livestock zone]].")
        else:
            feeding_content.append(f"As a baby, it can survive without its mother.")

    if feeding_content:
        check_first()
        content.append("=== Feeding and luring ===")
        content.extend(feeding_content)

#    if animal.min_enclosure_size:
#        check_first()
#        content.append("=== Livestock zones ===")
#        content.append("{{Main|Animal Care#Livestock zone}}")
#        zone_hutch = " A [[Chicken Hutch|hutch]] should also be placed in the livestock zone for it to roost in. It will lay eggs in the hutch, otherwise they will be laid on the ground." if animal.hutches else ""
#        content.append(f"This animal can be kept in a livestock zone. The minimum size of the zone must be {animal.min_enclosure_size}. Having a small enclosure size will drastically reduce the size and weight of the animal when growing up, affecting the amount of [[#Products|resources]] it will produce.{zone_hutch}")

    # === Livestock zones ===
    if animal.can_be_domesticated:
        if animal.min_enclosure_size:
            zone_hutch = (
                " A [[Chicken Hutch|hutch]] should also be placed in the livestock zone for it to roost in. "
                "It will lay eggs in the hutch, otherwise they will be laid on the ground." if animal.hutches else ""
            )
            enclosure_size = (
                f" The minimum size of the zone must be {animal.min_enclosure_size}."
                f" Having a small enclosure size will drastically reduce the size and weight of the animal when growing up, affecting the amount of [[#Products|resources]] it will produce."
                f"{zone_hutch}"
            )
        else:
            enclosure_size = ""
        if animal.wild:
            livestock_zones = f"This animal can be found in the wild, however it can still be domesticated in a [[Animal Care#Livestock zone|livestock zone]].{enclosure_size}"
        else:
            livestock_zones = f"This animal can be domesticated in a [[Animal Care#Livestock zone|livestock zone]].{enclosure_size}"
    else:
        livestock_zones = "This animal is wild, and cannot be domesticated. However, it will still appear in the [[Animal Care#Livestock zone|livestock zone]] window, allowing the player to check its info. "

    if livestock_zones:
        check_first()
        content.append("=== Livestock zones ===")
        content.append("{{Main|Animal Care#Livestock zone}}")
        content.append(livestock_zones)

    # === Stress ===
    check_first()
    content.append("=== Stress ===")
    if animal.always_flee_humans:
        zombie_beh = " and [[zombie]]s" if animal.flee_zombies else ""
        content.append(f"This animal will always flee [[survivor]]s{zombie_beh}, regardless of its stress level.")
    else:
        zombie_beh = "It will always flee [[zombie]]s." if animal.flee_zombies else "It will not flee [[zombie]]s."
        content.append(f"When stressed (>50%) it is more likely to flee the [[player]], with the acceptance level reducing the distance it flees to. {zombie_beh}")
        content.append("\nStress can be caused by various factors, including:")
        attack_back = " and will attack back" if animal.attack_back else ""
        content.extend([
            "* Starving.",
            "* Dying of thirst.",
            "* Being near [[zombie]]s.",
            "* Seeing a player running.",
            "* Seeing a player with low acceptance.",
            f"* Being attacked{attack_back}.",
            "* Being in a [[vehicle]] traveling greater than 5km/h.",
            ])
        if animal.stress_under_rain:
            content.append("* Being in the [[Weather#Rain and snow|rain]].")
        if animal.stress_above_ground:
            content.append("* Being above ground level.")
        if animal.can_be_milked and animal.udder:
            content.append("* Being [[#Milking|milked]] by a player with less than [[Animal Care|animal care]] level 5.")
            #content.append(f"* Being milked (chance if [[Animal Care|animal care]] is less than 7 and animal's stress is already greater than 40).")

    
    if animal.attack_if_stressed or animal.can_thump or animal.max_milk or breed.wool_type:
        content.append("When stressed, this animal may:")
        if animal.attack_if_stressed:
            content.append("* Attack the player.")
        if animal.can_thump:
            content.append("* Destroy [[furniture]].")
        if animal.max_milk:
            content.append("* Reduce milk production (>40).")
        if animal.can_be_milked and animal.udder:
            content.append("* Break from being [[#Milking|milked]], increasing its stress and knocking over the [[Fluid container|container]], emptying it (>40 and [[Animal Care|animal care]] <7).")
        if breed.wool_type:
            content.append("* Reduce wool production (>40).")
            content.append("* Break from being [[#Shearing|sheared]], increasing its stress (>40 and [[Animal Care|animal care]] <7).")

    # === Petting ===
    if animal.can_be_pet:
        check_first()
        content.append("=== Petting ===")
        content.append(f"This animal can be pet, reducing its [[Animal#Stress|stress]] by 3–7 plus the player's [[Animal Care|animal care]] level. This will also increase its [[Animal#Animal acceptance|acceptance]] towards the player.")

    # === Fighting ===
    fighting_content = []
    if not animal.dont_attack_other_male and animal.male:
        fighting_content.append(f"*Attacks other nearby males.")
    if animal.attack_back:
        fighting_content.append("*Attacks back when attacked.")
    if animal.attack_if_stressed:
        fighting_content.append("*Attacks players when stressed.")
    if animal.can_thump:
        fighting_content.append("*Attacks [[furniture]] blocking its path, such as when stressed.")
    if fighting_content:
        check_first()
        content.append("=== Fighting ===")
        content.append("This animal may attack in the following situations: ")
        content.extend(fighting_content)

#    content.append("\n=== Animal acceptance ===")
#    content.append("Each animal has an acceptance value towards each player. Certain activities will increase or decrease this value, and determines their overall behaviour towards that player.")

    return content

def generate_products(breed: AnimalBreed):
    full_breed_id = breed.full_breed_id
    animal = breed.animal

    content = []

    # === Butchering ===
    butchering_parts = load_file(rel_path=os.path.join("products", "butchering_parts", full_breed_id + ".txt"), root_path=ANIM_DIR)
    butchering_meat_hunger = load_file(rel_path=os.path.join("products", "butchering_meat_hunger", full_breed_id + ".txt"), root_path=ANIM_DIR)
    butchering_meat_calories = load_file(rel_path=os.path.join("products", "butchering_meat_calories", full_breed_id + ".txt"), root_path=ANIM_DIR)
    butchering_meat_carbohydrates = load_file(rel_path=os.path.join("products", "butchering_meat_carbohydrates", full_breed_id + ".txt"), root_path=ANIM_DIR)
    butchering_meat_lipids = load_file(rel_path=os.path.join("products", "butchering_meat_lipids", full_breed_id + ".txt"), root_path=ANIM_DIR)
    butchering_meat_proteins = load_file(rel_path=os.path.join("products", "butchering_meat_proteins", full_breed_id + ".txt"), root_path=ANIM_DIR)

    if butchering_parts or butchering_meat_hunger:
        content.append("\n=== Butchering ===")
        content.append("{{Main|Butchering}}")
        if animal.can_be_hooked:
            hook_desc = "This animal can be butchered, either from the ground or a [[Butcher Hook|butcher hook]], to obtain [[Animal part|parts]]."
        else:
            hook_desc = "This animal can only be butchered from the ground (not on a [[Butcher Hook|hook]]) to obtain [[Animal part|parts]]."
        if butchering_meat_hunger:
            meat_desc = "Every 2 levels of the [[butchering]] skill increases the maximum potential meat by 10%."
        else:
            meat_desc = ""
        content.append(f"{hook_desc} {meat_desc}")
        if butchering_parts:
            content.append("")
            content.append(f"This table shows the parts that can be obtained when butchering, depending on how it was killed and butchered.")
            content.extend(butchering_parts)

        if butchering_meat_hunger:
            content.append("")
            content.append("The [[butchering]] skill increases the odds of higher-quality cuts. At level 0, only poor cuts will be obtained, which will increase each level. This probability is depedant on the animal size, butchering skill and the [[#Genes|meat ratio gene]].")
            content.append("")
            content.append("This table shows the hunger and [[nutrition]] for the meat obtained from butchering, depending on how it was killed and butchered.")
            content.append('<div style="display:flex; gap:1em; flex-wrap:wrap;"><div>')
            content.extend(butchering_meat_hunger)
            content.append('</div><div>')
            content.extend(butchering_meat_calories)
            content.append('</div><div>')
            content.extend(butchering_meat_carbohydrates)
            content.append('</div><div>')
            content.extend(butchering_meat_lipids)
            content.append('</div><div>')
            content.extend(butchering_meat_proteins)
            content.append('</div></div>')

    # === Harvesting ===
    harvesting_content = []
    if animal.dung and animal.dung.valid and animal.dung_chance_per_day:
        dung_hutch = " (reduced by time spent in a hutch)" if animal.hutches else ""
        harvesting_content.append(f"* Drops {animal.dung.icon} {animal.dung.wiki_link} with a {util.convert_int((0.6 * (animal.dung_chance_per_day / 100)) * 100)}% chance per day{dung_hutch}.")
    if animal.egg_type and animal.eggs_per_day:
        egg_season = f"laying {'–'.join([str(animal.min_clutch_size), str(animal.max_clutch_size)])} per season, with the season starting in {animal.lay_egg_period_month_start}" if animal.min_clutch_size and animal.max_clutch_size and animal.lay_egg_period_month_start else "year-round"
        harvesting_content.append(f"* Lays up to {animal.eggs_per_day} {animal.egg_type.icon} {animal.egg_type.wiki_link} per day, {egg_season}. Eggs will be laid in a hutch if there is one, otherwise on the ground.")
    if breed.feather_item and breed.feather_item.valid:
        feather_hutch = " (reduced by time spent in a hutch)" if animal.hutches else ""
        harvesting_content.append(f"* 1% chance of dropping a {breed.feather_item.icon} {breed.feather_item.wiki_link} every hour{feather_hutch}.")
    
    # ==== Shearing ====
    if breed.wool_type and not animal.baby:
        harvesting_content.append("==== Shearing ====")
        wool_content = (
            f"This animal can be sheared once it has grown enough wool. "
            f"Once it's reached 200 days old, it will begin to grow {breed.wool_type.icon} {breed.wool_type.wiki_link} so long as it doesn't have a genetic disorder. "
            f"The time it takes to shear is dependant on the amount of wool, the player's [[Animal Care|animal care]] skill, and the shears being used. [[Shears - Electric|Electric shears]] are 40% quicker than regular [[shears]]."
        )
        wool_capacity = f"* Maximum wool: {str(int(breed.max_wool[0]))}–{str(int(breed.max_wool[1]))}"
        harvesting_content.extend([wool_content, wool_capacity])
        #harvesting_content.append(f"* {breed.wool_type.icon} {breed.wool_type.wiki_link}: {'–'.join(["0", str(util.convert_int(animal.max_wool))])}")
    
    # ==== Milking ====
    if animal.min_milk and animal.can_be_milked and breed.milk_type and animal.udder:
        harvesting_content.append("==== Milking ====")
        milk_content = (
            f"This animal can be milked once it has produced enough milk. "
            f"After giving birth, it will generate {breed.milk_type.rgb_link} {breed.milk_type.wiki_link} until it becomes too old (over 80% of its maximum age). "
            f"Milk production rate is influenced by the animal’s milk capacity, the [[#Genes|milk inc gene]], genetic disorders, and its [[#Stress|stress]] level. "
            f"Animals that are milked regularly can increase their capacity by up to 30%, while those left unmilked will gradually lose health."
        )
        milk_capacity_min = f"* Minimum milk capacity: {str(int(breed.actual_min_milk_min))}–{str(int(breed.actual_min_milk_max))} L"
        milk_capacity_max = f"* Maximum milk capacity: {str(int(breed.actual_max_milk_min))}–{str(int(breed.actual_max_milk_max))} L"
        harvesting_content.extend([milk_content, milk_capacity_min, milk_capacity_max])
        #harvesting_content.append(f"* {breed.milk_type.rgb_link} {breed.milk_type.wiki_link}: {'–'.join([str(animal.min_milk), str(animal.max_milk)])} L")

    if harvesting_content:
        content.append("=== Harvesting ===")
        content.append("{{Main|Animal Care}}")
        content.append(f"Some items can be obtained from this animal, either from the ground, {'[[Chicken Hutch|hutch]], ' if animal.hutches else ''}or harvested directly from the animal. They can only be obtained if the animal is in a [[#Livestock zones|livestock zone]] and not wild.")
        content.extend(harvesting_content)
    
    return content


def generate_breeding(breed: AnimalBreed):
    """
    Generates the breeding section for the article.
    """
    animal = breed.animal

    content = []

    content.append("{{Main|Breeding}}")

#    if animal.can_be_domesticated:
    if animal.baby:
        content.append("This animal is a baby, so it cannot breed until it reaches an [[#Stages|adult stage]].")
    else:
        baby_count = "a" if not animal.baby_nbr else f"{animal.baby_nbr[0]} to {animal.baby_nbr[1]}"
        baby_key = f"{animal.baby_type}{breed.breed_id}"
        if not animal.female:
            mate = Animal(animal.mate)
            baby_breed = f"{Animal(mate.baby_type).wiki_link}, which will be the breed of the mother"
        else:
            baby_breed = AnimalBreed.from_key(baby_key).wiki_link

        baby = ". " if not animal.baby_type else f", producing {baby_count} {baby_breed}. "
        mating_period = ". " if not animal.mating_period_month_start else f", and can only breed during its mating period ({animal.mating_period_month_start} to {animal.mating_period_month_end}). "
        pregnant_period = "" if not animal.pregnant_period else f"The pregnancy lasts {animal.pregnant_period} days. "
        pregnancy_break = "" if not animal.time_before_next_pregnancy else f"After giving birth, at least {animal.time_before_next_pregnancy} days must pass before it can get pregnant again. "
        egg_laying = "" if not animal.egg_type else (f"Instead of getting pregnant, it will become \"fertilized\" which lasts {animal.fertilized_time_max} hours ({animal.fertilized_time_max // 24} days). "
                                                    f"During this time, any eggs that it [[#Harvesting|lays]] will be fertilized. "
                                                    f"A fertilized egg will take {math.floor(animal.time_to_hatch * 0.7)} hours ({math.floor(animal.time_to_hatch * 0.7 // 24)} days) to hatch. ")
        hutch = "" if not animal.hutches else f"The animal must be kept in a [[#Livestock zones|livestock zone]] in order to lay fertilized eggs, ideally with a [[Chicken Hutch|hutch]]. "
        content.append(
            f"This animal can breed with other animals in the {animal.group_link} group{baby}"
            f"It must be at least {animal.min_age_for_baby} days old to breed{mating_period}"
            f"{pregnant_period}{pregnancy_break}"
            f"{egg_laying}{hutch}"
            )
#    else:
#        content.append("This animal is wild, and cannot be used to breed.{{verify}}")

    # === Genes ===
    genes_table = load_file(rel_path=os.path.join(breed.full_breed_id + ".txt"), root_path=animal_genes.GENES_DIR)
    if genes_table:
        content.append("=== Genes ===")
        content.append("This table below shows the genes that this animal breed has, along with their dominance and potential range for the first generation (when first spawned). It should be noted that these can be affected by mutations.")
        content.extend(genes_table)
    else:
        echo.warning(f"No genes table found for '{breed.full_breed_id}.txt' in '{animal_stages.STAGES_DIR}'")
    
    # === Stages ===
    stages_table = load_file(rel_path=os.path.join(breed.full_breed_id + ".txt"), root_path=animal_stages.STAGES_DIR)
    if stages_table:
        content.append("\n=== Stages ===")
        content.extend(stages_table)

    return content


def generate_location(breed: AnimalBreed):
    """
    Generates the location section for the article.
    """
    animal = breed.animal

    content = []

    zones = breed.animal.ranch_zones
    if zones and animal.wild:
        content.append(f"{article.capitalize()} {breed.name} can be found in the wild or in one of the following ranch zones:")
    elif zones and not animal.wild:
        content.append(f"{article.capitalize()} {breed.name} can only be found in one of the following ranch zones:")
    else:
        content.append(f"{article.capitalize()} {breed.name} can only be found in the wild.")

    if zones:
        content.append(f"<!-- Bot_flag|type=animal_ranch_zone|id={breed.full_breed_id} -->")
        zones = [zone.id for zone in zones]
        for zone in zones:
            content.append(f"* {zone}")
        content.append(f"<!-- Bot_flag_end|type=animal_ranch_zone|id={breed.full_breed_id} -->")

    return content

def generate_see_also(breed: AnimalBreed):
    """ 
    Generates the see also section for the article.
    """
    content = []

    content.extend([
        "*[[Tracking]]",
        "*[[Trapping]]"
    ])

    return content

def load_modules():
    animal_infobox.main(pre_choice=2)
    animal_products.main()
    animal_stages.main()
    animal_genes.main()
    animal_food.main()

def process_animal(breed: AnimalBreed):
    animal = Animal(breed.animal_id)

    header_content = generate_header(breed)
    infobox_content = load_file(rel_path=os.path.join("infoboxes", breed.full_breed_id + ".txt"), root_path=ANIM_DIR)
    intro_content = generate_intro(breed)
#    overview_content = generate_overview(breed)
    behaviour_content = generate_behaviour(breed)
    products_content = generate_products(breed)
    breeding_content = generate_breeding(breed)
    location_content = generate_location(breed)
    see_also_content = generate_see_also(breed)

    content = []

    content.extend(header_content)
    content.append("{{Autogenerated|B42 animals}}")
#    content.append("{{Underconstruction|This article was automatically generated, and is currently undergoing testing. Any changes may be overwritten.}}")
    content.extend(infobox_content)
    content.extend(intro_content)

#    if overview_content:
#        content.append("\n== Overview ==")
#        content.extend(overview_content)

    if behaviour_content:
        content.append("\n== Behaviour ==")
        content.extend(behaviour_content)

    if products_content:
        content.append("\n== Products ==")
        content.extend(products_content)

    if breeding_content:
        content.append("\n== Breeding ==")
        content.extend(breeding_content)
    
    if location_content:
        content.append("\n== Location ==")
        content.extend(location_content)

    content.append("\n== See also ==")
    content.extend(see_also_content)

    content.append("\n== Navigation ==")
    content.append("{{Navbox animals}}")

    rel_path = breed.full_breed_id + ".txt"
    write_file(content, rel_path=rel_path, root_path=output_dir, suppress=True)

def main():
    global output_dir
    output_dir = os.path.join(ANIM_DIR, "articles")
    load_modules()
    with tqdm(total=AnimalBreed.count(), desc="Generating animal articles", bar_format=PBAR_FORMAT, unit=" animals", leave=False) as pbar:
        for full_breed_id, breed in AnimalBreed.all().items():
            pbar.set_postfix_str(f"Processing: {full_breed_id[:30]}")
            process_animal(breed)
            pbar.update(1)

    echo.success(f"Article files saved to '{output_dir}'")

if __name__ == "__main__":
    main()