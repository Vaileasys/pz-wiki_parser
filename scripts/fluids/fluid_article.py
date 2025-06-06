import os
from tqdm import tqdm
from scripts.core.constants import FLUID_DIR, PBAR_FORMAT
from scripts.objects.fluid import Fluid
from scripts.core.version import Version
from scripts.core.language import Language
from scripts.fluids import fluid_infobox
from scripts.core.file_loading import write_file, load_file
from scripts.utils import echo
from scripts.utils.util import link

OUTPUT_DIR = os.path.join(FLUID_DIR.format(language_code=Language.get()))
INFOBOX_DIR = os.path.join(OUTPUT_DIR, "infoboxes")
ARTICLE_DIR = os.path.join(OUTPUT_DIR, "articles")

HEADER = (
    '{{Header|Project Zomboid|Fluids}}',
    f'{{{{Page version|{Version.get()}}}}}',
    '{{Autogenerated|fluids|source=https://github.com/Vaileasys/pz-wiki_parser}}'
)


def check_name(fluid_id, name, method):
    """Check if a name is or contains a proper noun for capitalisation"""
    PROPER_NOUN_FILTER = {
        'SecretFlavoring': {
            'lower': 'substance RTMS-M1A1',
            'capitalize': 'Substance RTMS-M1A1'
        },
        'SpiffoJuice': {
            'lower': "Spiffo's juice",
            'capitalize': "Spiffo's juice"
        },
        'Test': {
            'lower': "FLUID_TEST",
            'capitalize': "FLUID_TEST"
        },
        'FilterTestA': {
            'lower': "Fluid_Filter_A",
            'capitalize': "Fluid_Filter_A"
        },
        'FilterTestB': {
            'lower': "Fluid_Filter_B",
            'capitalize': "Fluid_Filter_B"
        },
        'FilterTestC': {
            'lower': "Fluid_Filter_C",
            'capitalize': "Fluid_Filter_C"
        }
    }
        
    try:
        if fluid_id in PROPER_NOUN_FILTER:
            return PROPER_NOUN_FILTER[fluid_id][method]
        elif method == 'lower':
            return name.lower()
        elif method == 'capitalize':
            return name.capitalize()
    except Exception:
        echo.error(f"'{method}' is an unknown method")
        return name


def calculate_similar_fluids(fluid_id):
    """Gets similar fluids based on a calculated score.

    Args:
        fluid_id (str): Fluid identifier.

    Returns:
        list[str]: List of wiki links to the top 3 similar fluids.
    """
    # General comparison weights
    weights = {
        "categories": 3,
        "poison": 3,
        "fatigue_change": 1,
        "hunger_change": 1,
        "stress_change": 1,
        "thirst_change": 1,
        "unhappy_change": 1,
        "calories": 0.5,
        "carbohydrates": 0.5,
        "lipids": 0.5,
        "proteins": 0.5,
        "alcohol": 3,
        "flu_reduction": 2,
        "pain_reduction": 2,
        "endurance_change": 1,
        "food_sickness_reduction": 2
    }

    # Poison weights
    poison_effect = {
        'None': 0,
        'Mild': 1,
        'Medium': 2,
        'Severe': 3,
        'Extreme': 4,
        'Deadly': 5
    }

    target_fluid = Fluid(fluid_id)
    similar_fluids = []

    # Compare target against all fluids
    for compared_id in Fluid.keys():
        if compared_id == fluid_id:
            continue

        compared_fluid = Fluid(compared_id)
        score = 0

        # Loop over all weighted properties
        for prop, weight in weights.items():
            if prop == "categories":
                # Compare categories
                shared_categories = set(target_fluid.categories) & set(compared_fluid.categories)
                score += len(shared_categories) * weight
            elif prop == "poison":
                # Compare poison
                target_poison = poison_effect.get(getattr(target_fluid.poison, "max_effect", 'None'), 0)
                other_poison = poison_effect.get(getattr(compared_fluid.poison, "max_effect", 'None'), 0)
                score += weight * min(target_poison, other_poison)
            else:
                # Compare properties
                target_value = getattr(target_fluid, prop)
                compared_value = getattr(compared_fluid, prop)
                if target_value == compared_value:
                    score += weight

        similar_fluids.append({'id': compared_id, 'name': compared_fluid.name, 'score': score})

    # Sort fluids by score
    similar_fluids.sort(key=lambda x: x['score'], reverse=True)
    processed_links = [Fluid(entry['id']).wiki_link for entry in similar_fluids[:3]]

    return processed_links


def generate_infobox(fluid_id: str):
    DEFAULT = (
        '{{Infobox fluid',
        '|name=',
        '|categories=',
        '|fluid_color=0, 0, 0',
        f'|fluid_id=Base.{fluid_id}',
        f'|infobox_version={Version.get()}',
        '}}'
        )
    
    file_name = fluid_id + ".txt"
    file_path = os.path.join(INFOBOX_DIR, file_name)

    try:
        if os.path.exists(file_path):
            infobox_content = load_file(rel_path=file_name, root_path=INFOBOX_DIR)
        else:
            echo.warning(f"File not found for '{fluid_id}'. Try generating infoboxes again.")
            infobox_content = DEFAULT
        
    except Exception as e:
        echo.error(f"Failed reading infobox file '{file_path}': {e}")
        infobox_content = DEFAULT
    
    return infobox_content


def generate_intro(fluid: Fluid):
    fluid_id = fluid.fluid_id

    alcoholic = True if fluid.alcohol else False
    beverage = True if "Beverage" in fluid.categories else False
    poison = True if fluid.poison.max_effect.lower() != "none" else False
    debug_fluid = True if "test" in fluid_id.lower() or "debug" in fluid_id.lower() or "test" in fluid.name.lower() or "debug" in fluid.name.lower() else False

    INTRO_DICT = {
        'default': f"'''{check_name(fluid_id, fluid.name, 'capitalize')}''' is a type of [[fluid]].",
        'alcohol': f"'''{check_name(fluid_id, fluid.name, 'capitalize')}''' is a type of [[fluid]] containing alcohol.",
        'alcohol_beverage': f"'''{check_name(fluid_id, fluid.name, 'capitalize')}''' is a type of [[fluid]] containing alcohol, that can also be used in beverages.",
        'poison': f"'''{check_name(fluid_id, fluid.name, 'capitalize')}''' is a type of [[fluid]] that acts as a {fluid.poison.max_effect.lower()} poison.",
        'poison_alcohol': f"'''{check_name(fluid_id, fluid.name, 'capitalize')}''' is a type of [[fluid]] containing alcohol and acts as a {fluid.poison.max_effect.lower()} poison.",
        'beverage': f"'''{check_name(fluid_id, fluid.name, 'capitalize')}''' is a type of [[fluid]] that can be used in beverages.",
        'debug': f"'''{check_name(fluid_id, fluid.name, 'capitalize')}''' is a type of [[fluid]] used in debugging."
    }
    intro = INTRO_DICT['default']
    if debug_fluid:
        intro = intro = INTRO_DICT['debug']
    elif alcoholic and beverage:
        intro = INTRO_DICT['alcohol_beverage']
    elif alcoholic and poison:
        intro = INTRO_DICT['poison_alcohol']
    elif alcoholic:
        intro = INTRO_DICT['alcohol']
    elif poison:
        intro = INTRO_DICT['poison']
    elif beverage:
        intro = intro = INTRO_DICT['beverage']
    
    return intro


def generate_usage(fluid: Fluid):
    fluid_id = fluid.fluid_id

    content = []
    content.append(f"Like other {link('fluid')}s, {check_name(fluid_id, fluid.name, 'lower')} can be stored in a {link('fluid container')}, which may be an {link('item')} or {link('tile')}.")
    # Add mixing info if it has a whitelist
    if fluid.blend_whitelist.whitelist:
        content.append("===Mixing===")
        #FIXME: this is wrong. Fluids can be mixed with fluids that have a fluid's category whitelisted OR if another fluid has one of its categories whitelisted.
        if not fluid.blend_whitelist.categories:
            content.append(f"{check_name(fluid_id, fluid.name, 'capitalize')} cannot be mixed with other fluids.")
        elif len(fluid.blend_whitelist.categories) == 1:
            content.append(f"{check_name(fluid_id, fluid.name, 'capitalize')} can be mixed with other fluids that have the '{fluid.blend_whitelist.categories[0]}' category.")
        else:
            content.append(f"{check_name(fluid_id, fluid.name, 'capitalize')} can be mixed with other fluids that have the following categories:")
            content.append("*" + "\n*".join(fluid.blend_whitelist.categories))

    return content


def generate_history(fluid_id):
    history_table = (
        '{{HistoryTable|',
        f'{{{{HistoryLine|Build {Version.get().split(".")[0]}|Build {Version.get()}|Released on this version.}}}}',
        f'|fluid_id=Base.{fluid_id}',
        '}}'
    )
    return history_table


def process_fluid(fluid_id):
    fluid = Fluid(fluid_id)

    content = []

    infobox_content = generate_infobox(fluid_id)
    intro_content = generate_intro(fluid)
    usage_content = generate_usage(fluid)
    history_content = generate_history(fluid_id)

    try:
        # Header
        content.extend(HEADER)
        # Infobox
        content.extend(infobox_content)
        # Intro
        content.append(intro_content)
        # Usage
        content.append("\n==Usage==")
        content.extend(usage_content)
        # History
        content.append(f"\n==History==")
        content.extend(history_content)
        # See also
        content.append(f"\n==See also==")
        content.append("*" + "\n*".join(calculate_similar_fluids(fluid_id)))

    except Exception as e:
        echo.error(f"Failed processing article for '{fluid_id}': {e}")
        return [f"{{{{Note|type=error|Error generating article for fluid: {fluid_id}.}}}}"]
    
    write_file(content, root_path=ARTICLE_DIR, rel_path=fluid_id + ".txt", suppress=True)


def main():
    if not os.path.exists(INFOBOX_DIR):
        fluid_infobox.main(pre_choice="1")
    
    if not os.path.exists(ARTICLE_DIR):
        os.makedirs(ARTICLE_DIR)

    with tqdm(total=Fluid.count(), desc="Generating fluid articles", bar_format=PBAR_FORMAT, unit=" fluids", leave=False) as pbar:
        for fluid_id in Fluid.keys():
            pbar.set_postfix_str(f"Processing: {fluid_id[:45]}")
            process_fluid(fluid_id)
            pbar.update(1)

    echo.success(f"Fluid articles saved to '{ARTICLE_DIR}'")


if __name__ == "__main__":
    main()