import os
import shutil
import script_parser
from core import logging
from core import translate
from core import utility


def get_fixing():
    while True:
        fixing_id = input("Enter an item id\n> ")
        for module, module_data in script_parser.parsed_fixing_data.items():
            for fixing, fixing_data in module_data.items():
                fixing_id = f"{module}.{fixing}"
                fixing_id = fixing_id.replace(" ", "_")
                return module, fixing_id, fixing_data
        print(f"No item found for '{fixing_id}', please try again.")


# get fixer(s)
def get_fixer(fixing_id, index=""):
    items = []
    item_values = []
    skills = []
    skill_values = []
    module, fixing = fixing_id.split(".")
    fixing = fixing.replace("_", " ")
    
    for parsed_module, module_data in script_parser.parsed_fixing_data.items():
        if parsed_module == module:
            for parsed_fixing, fixing_data in module_data.items():
                if parsed_fixing == fixing:
                    for property, property_data in fixing_data.items():
                        if "Fixer" in property:
                            skill_data = property_data.get("skills", {})

                            for subprop, subprop_data in property_data.items():
                                if "items" in subprop:
                                    items.extend(subprop_data.keys())
                                    item_values.extend(subprop_data.values())

                                    for item_key in subprop_data.keys():
                                        item_skills = []
                                        item_skill_values = []

                                        for skill, level in skill_data.items():
                                            item_skills.append(skill)
                                            item_skill_values.append(level)

                                        skills.append(item_skills)
                                        skill_values.append(item_skill_values)
                    
    # handle indexing
    if index != "":
        if index < len(items):
            items = items[index]
            item_values = item_values[index]
            skills = skills[index]
            skill_values = skill_values[index]
        else:
            print(f"Index {index} is out of range.")
            return None, None, None, None
                 
    return items, item_values, skills, skill_values


def get_require(module, fixing_data):
    name = ""
    item_id = ""
    if 'Require' in fixing_data:
        item_fixed = fixing_data['Require']
        if isinstance(item_fixed, list):
            for item in item_fixed:
                item_id_new = f"{module}.{item}"
                translated_name = translate.get_translation(item_id_new, "DisplayName")

                if translated_name not in name:
                    if name:
                        name += "; "
                    name += translated_name
                if item_id:
                    item_id += "; "
                item_id += item_id_new
        else:
            item_id = f"{module}.{item_fixed}"
            name = translate.get_translation(item_id, "DisplayName")
    return item_id, name


# format fixers
def format_fixers(module, fixers):
    formatted_fixers = []
    for fixer in fixers:
        fixer = f"{module}.{fixer}"
        fixer = translate.get_translation(fixer, "DisplayName")
        formatted_fixer = f"{{{{ll|{fixer}}}}}"
        formatted_fixers.append(formatted_fixer)
    return formatted_fixers


# format skills
def format_skills(skills, skill_values):
    """Format skills and skill values into a string with <br> for line breaks."""
    if not skills or not skill_values:
        return ""
    if len(skills) != len(skill_values):
        return ""
    
    formatted_skills = []
    for skill, value in zip(skills, skill_values):
        translated_skill = translate.get_translation(skill, "Categories")
        if not translated_skill:
            translated_skill = skill
        if not value:
            value = "0"
        formatted_skills.append(f"{value} {{{{ll|{translated_skill}}}}}")
    
    return "<br>".join(formatted_skills)


def write_to_output(module, fixing_id, fixing_data, output_dir='output/fixing'):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{fixing_id}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("{{Fixing")

            item_id, name = get_require(module, fixing_data)
            condition_modifier = fixing_data.get('ConditionModifier', '')
            if condition_modifier != '':
                condition_modifier = condition_modifier[0]
            
            global_item_value = ''
            global_item = ''
            global_item_dict = fixing_data.get('GlobalItem1', {}).get('items', {})
            if global_item_dict:
                # expect single entry
                global_item, global_item_value = next(iter(global_item_dict.items()))

            fixers, fixer_values, skills, skill_values = get_fixer(fixing_id)
            fixers = format_fixers(module, fixers)
            
            parameters = {
                "name": name,
                "item_id": item_id,
                "global_item": global_item,
                "global_item_value": global_item_value,
                "condition_modifier": condition_modifier,
            }

            # Add fixers, fixer_values, skills, and skill_values dynamically
            for i in range(max(len(fixers), len(fixer_values), len(skills), len(skill_values))):
                if i < len(fixers):
                    parameters[f"fixer{i+1}"] = fixers[i]
                if i < len(fixer_values):
                    parameters[f"fixer{i+1}_value"] = fixer_values[i]
                if i < len(skills):
                    skill_str = format_skills(skills[i], skill_values[i])
                    parameters[f"fixer{i+1}_skill"] = skill_str

            for key, value in parameters.items():
                if value:
                    file.write(f"\n|{key}={value}")

            file.write("\n}}")
    except Exception as e:
        print(f"Error writing file {fixing_id}.txt: {e}")
        logging.log_to_file(f"Error writing file {fixing_id}.txt: {e}")
    return


def process_item(module, fixing_id, fixing_data, output_dir):
    write_to_output(module, fixing_id, fixing_data, output_dir)


def automatic_extraction():
    output_dir = 'output/fixing'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for module, module_data in script_parser.parsed_fixing_data.items():
        for fixing, fixing_data in module_data.items():
            fixing_id = f"{module}.{fixing}"
            fixing_id = fixing_id.replace(" ", "_")
            process_item(module, fixing_id, fixing_data, output_dir)


def main():
    script_parser.init()

    while True:
        choice = input("1: Automatic\n2: Manual\nQ: Quit\n> ").strip().lower()
        if choice == '1':
            automatic_extraction()
            print("Extraction complete, the files can be found in output/fixing.")
        elif choice == '2':
            module, fixing_id, fixing_data = get_fixing()
            write_to_output(module, fixing_id, fixing_data)
            print("Extraction complete, the file can be found in output/fixing.")
        elif choice == 'q':
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
