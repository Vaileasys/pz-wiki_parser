import os
import shutil
from tqdm import tqdm
from scripts.objects.fluid import Fluid
from scripts.core.version import Version
from scripts.core.language import Language, Translate
from scripts.core.constants import FLUID_DIR, PBAR_FORMAT
from scripts.core.file_loading import write_file
from scripts.utils.util import enumerate_params, check_zero
from scripts.utils.echo import echo_warning, echo_success
from scripts.core import logger

ROOT_DIR = os.path.join(FLUID_DIR.format(language_code=Language.get()), "infoboxes")


def check_fluid():
    """Check if a fluid exists"""
    while True:
        query_id = input("Enter a fluid id\n> ")
        query_id = Fluid.fix_fluid_id(query_id)
        if query_id in Fluid.keys():
            return query_id
        echo_warning(f"No fluid found for '{query_id}', please try again.")


def generate_data(fluid_id):
    """Generate a fluid's infobox parameters"""
    try:
        fluid = Fluid(fluid_id)

        parameters = {
            "name": fluid.name,
            "categories": '<br>'.join(fluid.categories),
            "blend_whitelist": fluid.blend_whitelist.categories,
            "blend_blacklist": fluid.blend_blacklist.categories,
            "unhappy_change": check_zero(fluid.unhappy_change),
            "stress_change": check_zero(fluid.stress_change),
            "fatigue_change": check_zero(fluid.fatigue_change),
            "endurance_change": check_zero(fluid.endurance_change),
            "flu_reduction": check_zero(fluid.flu_reduction),
            "pain_reduction": check_zero(fluid.pain_reduction),
            "sick_reduction": check_zero(fluid.food_sickness_reduction),
            "hunger_change": check_zero(fluid.hunger_change),
            "thirst_change": check_zero(fluid.thirst_change),
            "calories": check_zero(fluid.calories),
            "carbohydrates": check_zero(fluid.carbohydrates),
            "proteins": check_zero(fluid.proteins),
            "lipids": check_zero(fluid.lipids),
            "alcohol": check_zero(fluid.alcohol),
            "poison_max_effect": Translate.get("Fluid_Poison_" + fluid.poison.max_effect) if fluid.poison.max_effect != "None" else None,
            "poison_min_amount": check_zero(fluid.poison.min_amount),
            "poison_dilute_ratio": check_zero(fluid.poison.dilute_ratio),
            "fluid_color": ', '.join(str(c) for c in fluid.color),
            "fluid_color_ref": fluid.color_reference,
            "fluid_id": f"{fluid_id}",
            "infobox_version": Version.get()
        }

        parameters = enumerate_params(parameters)
        parameters["infobox_version"] = Version.get()

        return parameters
    except Exception as e:
        logger.write(f"Error generating data for {fluid_id}", True, exception=e, category="error")


def process_fluid(fluid_id):
    parameters = generate_data(fluid_id)
    if parameters is not None:
        fluid_id = parameters.get("fluid_id")
        rel_path = f'{fluid_id}.txt'
        content = []

        # Generate infobox template
        content.append("{{Infobox fluid")
        for key, value in parameters.items():
            content.append(f"|{key}={value}")
        content.append("}}")

        write_file(content, rel_path=rel_path, root_path=ROOT_DIR, suppress=True)


def automatic_extraction():
    # Create 'output_dir'
    if os.path.exists(ROOT_DIR):
        shutil.rmtree(ROOT_DIR)
    os.makedirs(ROOT_DIR)

    with tqdm(total=len(Fluid.keys()), desc="Processing fluids", unit=" items", bar_format=PBAR_FORMAT, unit_scale=True, leave=False) as pbar:
        for fluid_id in Fluid.keys():
            pbar.set_postfix_str(f"Processing: '{fluid_id[:30]}'")
            process_fluid(fluid_id)
            pbar.update(1)


def main(pre_choice: str = None):
    """
    :param pre_choice: str - Automatically sets a choice without querying the user.
    """
    # Call early
    Language.get()

    while True:
        options = ("1", "2", "q")
        if str(pre_choice).lower() not in options:
            choice = input("1: Automatic\n2: Manual\nQ: Quit\n> ").strip().lower()
        else:
            choice = str(pre_choice).lower()

        if choice == '1':
            automatic_extraction()
            echo_success(f"Fluid infoboxes generated and saved to '{ROOT_DIR}'.")
            return
        elif choice == '2':
            fluid_id = check_fluid()
            process_fluid(fluid_id)
            file_path = os.path.join(ROOT_DIR, fluid_id + ".txt")
            echo_success(f"Fluid infobox generated and saved to '{file_path}'.")
            return
        elif choice == 'q':
            return
        else:
            echo_warning("Invalid choice.")


if __name__ == "__main__":
    main()
