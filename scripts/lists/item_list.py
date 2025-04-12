from tqdm import tqdm
import os
from scripts.parser import item_parser
from scripts.core import logger
from scripts.core.language import Language, Translate
from scripts.core.constants import (PBAR_FORMAT, OUTPUT_PATH)
from scripts.utils import utility
from scripts.utils.echo import echo_success, echo_warning

filters = {
#    'ExampleItemPrefix': (True,),
#    'ExampleProperty': (False, 'PropertyName', 'PropertyValue')
}

# store category translations in a dict to improve efficiency
categories = {}

HEADER = "! <<icon>> !! <<name>> !! <<item_id>>"

# checks if a category exists in the dict before trying to translate
def translate_category(category, property="DisplayCategory"):
    if category not in categories:
        try:
            cat_translated = Translate.get(category, property)
            categories[category] = cat_translated
        except Exception as e:
            logger.write(f"Error translating category '{category}': {e}")
            cat_translated = category
    else:
        cat_translated = categories[category]
    return cat_translated


def write_to_output(items_data):
    language_code = Language.get()
    output_dir = f'{OUTPUT_PATH}/{language_code}/item_list/'
    output_file = f'item_list.txt'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    content = []

    lc_subpage = ""
    if language_code != "en":
        lc_subpage = f"/{language_code}"

    for display_category in sorted(items_data.keys()):
        translated_header = Translate.get_wiki(HEADER)
        content.append(f"=={display_category}==")
        content.append('{| class="wikitable theme-blue"')
        content.append(f"{translated_header}")

        for item in items_data[display_category]:
            page_name = item["page_name"]
            item_name = item["item_name"]
            icons = item["icon"]
            item_id = item["item_id"]
            id_rec = item["id_rec"]

            icons_image = ' '.join([f"[[File:{icon}|32x32px]]" for icon in icons])
            item_link = f"[[{page_name}]]"

            if language_code != "en" or page_name != item_name:
                item_link = f"[[{page_name}{lc_subpage}|{item_name}]]"

            if id_rec:
                content.append('|-')
            else:
                content.append('|- title="ID missing in infobox" style="background-color: var(--background-color-warning-subtle); color:red;"')
                item_id = item_id + "*"

            content.append(f"| {icons_image} || {item_link} || {item_id}")
        content.append("|}\n")

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(content))

    echo_success(f"Output saved to {output_path}")


def generate_item_list():
    items_data = {}
    parsed_item_data = item_parser.get_item_data()

    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            id_rec = False
            pbar.set_postfix_str(f"Processing: {item_data.get('Type', 'Unknown')} ({item_id[:30]})")
            # Check if 'DisplayCategory' property exists for the item
            if 'DisplayCategory' in item_data:
                display_category = item_data.get('DisplayCategory', 'Other')
                display_category = translate_category(display_category)
                module, item_name = item_id.split('.', 1)

                icon = utility.find_icon(item_id, True)
                
                # Get the item name and use it as the page name if there isn't one defined.
                translated_item_name = utility.get_name(item_id, item_data, "en")
                page_name = utility.get_page(item_id)
                if page_name == 'Unknown':
                    page_name = translated_item_name
                else:
                    id_rec = True

                if Language.get() != 'en':
                    translated_item_name = utility.get_name(item_id, item_data)
                
                skip_item = False

                for filter_key, conditions in filters.items():
                    enabled = conditions[0]
                    if not enabled:
                        continue
                    
                    if item_name.startswith(filter_key):
                        skip_item = True
                        continue

                    if len(conditions) > 1:
                        property_name, property_value = conditions[1:]
                        property_filter = item_data.get(property_name)
                        if property_filter is not None and property_filter.lower() == property_value.lower():
                            skip_item = True
                            break
                    
                if skip_item:
                    continue

                # Add item to the sorted dictionary
                if display_category is None:
                    display_category = 'Unknown'

                if display_category not in items_data:
                    items_data[display_category] = []

                processed_item = {
                    "page_name": page_name,
                    "item_name": translated_item_name,
                    "icon": icon,
                    "item_id": item_id,
                    "id_rec": id_rec
                    }

                items_data[display_category].append(processed_item)

#                items_data[display_category].append((page_name, translated_item_name, icon, item_id, id_rec))
            pbar.update(1)
        pbar.bar_format = f"Items processed."

    for display_category in items_data:
        items_data[display_category] = sorted(items_data[display_category], key=lambda x: x["item_name"])

    write_to_output(items_data)


def filters_tree():
    while True:
        print("Current filters:")
        # Print a list of filters
        for filter_name, enabled in filters.items():
            print(f"{filter_name}: {'Enabled' if enabled else 'Disabled'}")
        filter_input = input("Enter filter name to toggle, 'add' to create a new filter or 'done' to exit:\n> ")

        if filter_input in filters:
            filters[filter_input] = not filters[filter_input]

        # User can add a new filter
        elif filter_input == "add":
            filter_name = input("Enter a name for the filter:\n> ")
            property_name = input("Enter the property name for the filter (e.g., 'Type'):\n> ")
            property_value = input("Enter the property value for the filter (e.g., 'Weapon'):\n> ")
            filter_name = filter_name or property_value  # change filter_name to property_value if empty
            filters[filter_name] = (True, property_name, property_value)
            print(f"Filter added: {filter_name} ({property_name} = {property_value})")
        elif filter_input == "done":
            return
        else:
            echo_warning("Invalid filter name. Please try again.")


def main():
#    while True:
#        user_input = input("1: Run script\n2: Set up a filter\nQ: Quit\n> ").lower()
#        if user_input == "1":
#            generate_item_list()
#            return
#        elif user_input == "2":
#            filters_tree()
#        elif user_input == "q":
#            return
    generate_item_list()

if __name__ == "__main__":
    main()
