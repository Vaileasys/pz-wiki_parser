import os
from scripts.core.language import Language, Translate
from scripts.objects.fluid import Fluid
from scripts.utils.util import check_zero
from scripts.utils.table_helper import get_table_data, create_tables
from scripts.utils.echo import echo_success
from scripts.core.constants import FLUID_DIR, RESOURCE_DIR

TABLE_PATH = os.path.join(RESOURCE_DIR, "tables", "fluid_table.json")
ROOT_PATH = os.path.join(FLUID_DIR, "lists")


def process_fluid(fluid_id):
    """Get fluid data for table"""
    table_type = "default"
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    fluid = Fluid(fluid_id)

    fluid_content = {
        "name": fluid.wiki_link,
        "color": fluid.rgb,
        "hunger_change": check_zero(fluid.hunger_change, default='-'),
        "thirst_change": check_zero(fluid.thirst_change, default='-'),
        "calories": check_zero(fluid.calories, default='-'),
        "carbohydrates": check_zero(fluid.carbohydrates, default='-'),
        "lipids": check_zero(fluid.lipids, default='-'),
        "proteins": check_zero(fluid.proteins, default='-'),
        "poison": Translate.get("Fluid_Poison_" + fluid.poison.max_effect) if fluid.poison.max_effect != "None" else "-",
        "alcohol": check_zero(fluid.alcohol),
        "fatigue_change": check_zero(fluid.fatigue_change),
        "stress_change": check_zero(fluid.stress_change),
        "unhappy_change": check_zero(fluid.unhappy_change),
        # No fluids with the following data yet
        #"flu_reduction": check_zero(fluid.flu_reduction),
        #"pain_reduction": check_zero(fluid.pain_reduction),
        #"endurance_change": check_zero(fluid.endurance_change),
        #"food_sickness_reduction": check_zero(fluid.food_sickness_reduction),
        "fluid_id": fluid_id
    }

    # Remove any values that are None
    fluid_content = {k: v for k, v in fluid_content.items() if v is not None}

    # Ensure column order is correct
    fluid_content = {key: fluid_content[key] for key in columns if key in fluid_content}

    # Add item_name for sorting
    fluid_content["item_name"] = fluid.name

    return fluid_content


def main():
    Language.get()
    global table_map
    table_map, column_headings = get_table_data(TABLE_PATH)
    fluid_data = {"fluid": []}

    for fluid_id in Fluid.keys():
        fluid_data["fluid"].append(process_fluid(fluid_id))

    create_tables("fluid", fluid_data, table_map=table_map, columns=column_headings, root_path=ROOT_PATH, combine_tables=False)


if __name__ == "__main__":
    main()