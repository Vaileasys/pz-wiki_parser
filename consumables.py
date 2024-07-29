import os
import shutil
import script_parser
from core import logging
from core import translate


def get_item(parsed_data):
    while True:
        item_id = input("Enter an item id\n> ")
        for module, module_data in parsed_data.items():
            for item_type, item_data in module_data.items():
                if f"{module}.{item_type}" == item_id:
                    return item_data, item_id
        print(f"No item found for '{item_id}', please try again.")


def get_icon(item_data, variant=""):
    icon_dir = 'resources/icons/'
    icon_variants = {
        "rotten": ['Rotten'],
        "cooked": ['Cooked', '_Cooked'],
        "burnt": ['Burnt', 'Overdone']
    }

    icon = item_data.get("Icon", '')
    if variant:
        variant = variant.lower()

        if variant in icon_variants:
            variant_exists = False
            
            for suffix in icon_variants[variant]:
                variant_icon = f"{icon}{suffix}"
                if os.path.exists(os.path.join(icon_dir, variant_icon + ".png")):
                    icon = variant_icon
                    variant_exists = True
                    break
            
            if not variant_exists:
                return ''
        
        else:
            raise ValueError(f"Variant '{variant}' could not be found in icon_variants dictionary")

    icon = icon + ".png"

    return icon


def is_egg(tags):
    if isinstance(tags, str):
        tags = [tags]
    if "Egg" in tags:
        value = 'true'
    else: value = ''
    return value


def write_to_output(parsed_data, item_data, item_id, output_dir='output/consumables'):
    if item_data.get('Type') == "Food" and ('IsCookable' in item_data or 'DaysTotallyRotten' in item_data):
        try:
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'{item_id}.txt')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write("{{Consumables")

                perishable = item_data.get("DaysTotallyRotten", '')
                if perishable:
                    perishable = "true"

                parameters = {
                    "name": translate.get_translation(item_id, "DisplayName"),
                    "image": get_icon(item_data),
                    "cooked_image": get_icon(item_data, "cooked"),
                    "rotten_image": get_icon(item_data, "rotten"),
                    "burned_image": get_icon(item_data, "burnt"),
                    "hunger": item_data.get("HungerChange", ''),
                    "boredom": item_data.get("BoredomChange", ''),
                    "unhappiness": item_data.get("UnhappyChange", ''),
                    "dangerous_uncooked": item_data.get("DangerousUncooked", '').lower(),
                    "egg": is_egg(item_data.get("Tags", '')),
                    "cookable": item_data.get("IsCookable", '').lower(),
                    "perishable": perishable,
                    "RemoveNegativeEffectOnCooked": item_data.get("RemoveNegativeEffectOnCooked", '').lower()
                }

                for key, value in parameters.items():
                    if value:
                        file.write(f"\n|{key}={value}")

                file.write("\n}}")

        except Exception as e:
            print(f"Error writing file {item_id}.txt: {e}")
            logging.log_to_file(f"Error writing file {item_id}.txt: {e}")


def process_item(parsed_data, item_data, item_id, output_dir):
    write_to_output(parsed_data, item_data, item_id, output_dir)


def automatic_extraction(parsed_data):
    output_dir = 'output/consumables'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for module, module_data in parsed_data.items():
        for item_type, item_data in module_data.items():
            item_id = f"{module}.{item_type}"
            process_item(parsed_data, item_data, item_id, output_dir)


def main():
    parsed_data = script_parser.main()

    choice = input("Select extraction mode (1: automatic, 2: manual):\n> ")
    if choice == '1':
        automatic_extraction(parsed_data)
        print("Extraction complete, the files can be found in output/infoboxes.")
    elif choice == '2':
        item_data, item_id = get_item(parsed_data)
        write_to_output(parsed_data, item_data, item_id)
        print("Extraction complete, the file can be found in output/infoboxes.")
    else:
        print("Invalid choice. Please restart the script and choose 1 or 2.")


if __name__ == "__main__":
    main()