import os
import shutil
from scripts.parser import item_parser
from scripts.core import logger
from scripts.core.language import Language, Translate
from scripts.utils import utility


def get_item():
    while True:
        query_item_id = input("Enter an item id\n> ")
        for item_id, item_data in item_parser.get_item_data().items():
            if item_id == query_item_id:
                return item_data, query_item_id
        print(f"No item found for '{query_item_id}', please try again.")


def get_icon_variant(item_id, variant=None):
    """Gets an icon for a specific variant. Returns the base icon if there is no variant defined or it doesn't exist.

    Args:
        item_id (str): The Item ID to get the icon for.
        variant (str, optional): The variant type to find and output if it exists. Defaults to None.

    Returns:
        str: The icon for the defined variant. Will return the base icon if the variant isn't defined or doesn't exist.
    """
    icons = utility.find_icon(item_id, True)
    if variant is not None:
        variant = variant.lower()
        icon_variants = {
            "rotten": ['Rotten', 'Spoiled'],
            "cooked": ['Cooked'],
            "burnt": ['Burnt', 'Overdone']
        }
        if variant in icon_variants:
            for variant_suffix in icon_variants[variant]:
                # Build icon to compare against, removing '.png' from the original icon
                variant_icon = f"{icons[0].replace('.png', '')}{variant_suffix}.png"
                for icon in icons:

                    if icon == variant_icon:
                        return icon
            return icons[0]
        else:
            print(f"Unknown variant: {variant}, using default icon.")
            return icons[0]
    else:
        return icons[0]


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
                    "name": Translate.get(item_id, "DisplayName"),
                    "image": get_icon_variant(item_id),
                    "cooked_image": get_icon_variant(item_id, "cooked"),
                    "rotten_image": get_icon_variant(item_id, "rotten"),
                    "burned_image": get_icon_variant(item_id, "burnt"),
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
            logger.write(f"Error writing file {item_id}.txt: {e}", True)


def process_item(item_data, item_id, output_dir):
    write_to_output(item_data, item_id, output_dir)


def automatic_extraction(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for item_id, item_data in item_parser.get_item_data().items():
        process_item(item_data, item_id, output_dir)


def main():
    language_code = Language.get()
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
