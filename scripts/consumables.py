import os
import shutil
from scripts.parser import item_parser
from scripts.core import logging, translate


def get_item():
    while True:
        query_item_id = input("Enter an item id\n> ")
        for item_id, item_data in item_parser.get_item_data().items():
            if item_id == query_item_id:
                return item_data, query_item_id
        print(f"No item found for '{query_item_id}', please try again.")


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
    else:
        value = ''
    return value


def write_to_output(item_data, item_id, output_dir):
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
            logging.log_to_file(f"Error writing file {item_id}.txt: {e}", True)


def process_item(item_data, item_id, output_dir):
    write_to_output(item_data, item_id, output_dir)


def automatic_extraction(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for item_id, item_data in item_parser.get_item_data().items():
        process_item(item_data, item_id, output_dir)


def main():
    language_code = translate.get_language_code()
    output_dir = f'output/{language_code}/consumables'

    while True:
        choice = input("1: Automatic\n2: Manual\nQ: Quit\n> ").strip().lower()
        if choice == '1':
            automatic_extraction(output_dir)
            print(f"Extraction complete, the files can be found in {output_dir}.")
            return
        elif choice == '2':
            item_data, item_id = get_item()
            write_to_output(item_data, item_id, output_dir)
            print(f"Extraction complete, the file can be found in {output_dir}.")
            return
        elif choice.lower() == 'q':
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
