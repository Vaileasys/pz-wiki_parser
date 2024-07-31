import os
import shutil
import script_parser
from core import logging
from core import translate
from core import utility


def get_item():
    while True:
        item_id = input("Enter an item id\n> ")
        for module, module_data in script_parser.parsed_fixing_data.items():
            for fixing, fixing_data in module_data.items():
                if 'Require' in fixing_data:
                    item_fixed = fixing_data['Require']
                    item_data = item_data = fixing_data['Fixer']
                    if f"{module}.{item_fixed}" == item_id:
                        return module, item_data, item_id
        print(f"No item found for '{item_id}', please try again.")


def write_to_output(module, item_data, item_id, output_dir='output/fixing'):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{item_id}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("{{Fixing")

            # Up to 10 fixers
            fixers = list(item_data)[:10]
            parameters = {
                "name": translate.get_translation(item_id, "DisplayName")
            }

            for i, fixer_dict in enumerate(fixers):
                fixer_key = f"fixer{i+1}"
                fixer_value_key = f"{fixer_key}_value"
                fixer_skill_key = f"{fixer_key}_skill"
                fixer_skill_value_key = f"{fixer_skill_key}_value"

                fixer_items = list(fixer_dict.items())
                lc = ""
                if translate.language_code != "en":
                    lc = f"/{translate.language_code}"
                if len(fixer_items) > 0:
                    fixer_item_key, fixer_item_value = fixer_items[0]
                    fixer_id = f"{module}.{fixer_item_key}"
                    fixer_name = translate.get_translation(fixer_id, "DisplayName", "en")
                    
                    fixer_name_translated = fixer_name
                    if translate.language_code != "en":
                        fixer_name_translated = translate.get_translation(fixer_id)
                    fixer_icon = f"[[File:{utility.get_icon_from_id(fixer_id)}.png|link={fixer_name}{lc}|{fixer_name_translated}]]"
                    parameters[fixer_key] = f"{fixer_icon} [[{fixer_name}{lc}]]"
                    parameters[fixer_value_key] = fixer_item_value['amount']
                else:
                    parameters[fixer_key] = ''
                    parameters[fixer_value_key] = ''
                
                if len(fixer_items) > 1:
                    skill_name, skill_value = fixer_items[1]
                    if skill_name:
                        skill_name = translate.get_translation(skill_name, "Categories", "en")
                    
                    parameters[fixer_skill_key] = f"[[{skill_name}{lc}]]"
                    parameters[fixer_skill_value_key] = skill_value['amount']
                else:
                    parameters[fixer_skill_key] = ''
                    parameters[fixer_skill_value_key] = ''

            for key, value in parameters.items():
                if value:
                    file.write(f"\n|{key}={value}")

            file.write("\n}}")
    except Exception as e:
        print(f"Error writing file {item_id}.txt: {e}")
        logging.log_to_file(f"Error writing file {item_id}.txt: {e}")
    return


def process_item(module, item_data, item_id, output_dir):
    write_to_output(module, item_data, item_id, output_dir)


def automatic_extraction():
    output_dir = 'output/fixing'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for module, module_data in script_parser.parsed_fixing_data.items():
        for fixing, fixing_data in module_data.items():
            if 'Require' in fixing_data:
                item_id = f"{module}.{fixing_data['Require']}"
                item_data = item_data = fixing_data['Fixer']
                process_item(module, item_data, item_id, output_dir)


def main():
    script_parser.init()

    choice = input("Select extraction mode (1: automatic, 2: manual):\n> ")
    if choice == '1':
        automatic_extraction()
        print("Extraction complete, the files can be found in output/fixing.")
    elif choice == '2':
        module, item_data, item_id = get_item()
        write_to_output(module, item_data, item_id)
        print("Extraction complete, the file can be found in output/fixing.")
    else:
        print("Invalid choice. Please restart the script and choose 1 or 2.")


if __name__ == "__main__":
    main()