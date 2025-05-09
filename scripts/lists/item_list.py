from tqdm import tqdm
import os
from scripts.objects.item import Item
from scripts.core import logger
from scripts.core.language import Language, Translate
from scripts.core.constants import (PBAR_FORMAT, OUTPUT_DIR)
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
    output_dir = f'{OUTPUT_DIR}/{language_code}/item_list/'
    output_file = f'item_list.txt'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    content = []

    lc_subpage = ""
    if language_code != "en":
        lc_subpage = f"/{language_code}"
    
    content.append('{| class="wikitable theme-blue"')
    translated_header = Translate.get_wiki(HEADER)

    for display_category in sorted(items_data.keys()):
        content.append("|-")
        content.append(f'! colspan="3"| <h3 style="margin-top:0;">{display_category}</h3>')
        content.append("|-")
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
                item_id += "*"

            content.append(f"| {icons_image}")
            content.append(f"| {item_link}")
            content.append(f"| {item_id}")

    content.append("|}\n")

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(content))

    echo_success(f"Output saved to {output_path}")


def generate_item_list():
    items_data = {}
    items = Item.all()

    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in items.items():
            pbar.set_postfix_str(f"Processing: {item.get('Type', 'Unknown')} ({item_id[:30]})")
            display_category = item.get('DisplayCategory', 'Other')
            display_category = translate_category(display_category)
            id_type = item.get_id_type()

            icon = item.get_icon(format=False, all_icons=True)

            translated_item_name = item.get_name("en")
            page_name = item.get_page()

            if Language.get() != 'en':
                translated_item_name = item.get_name()

            skip_item = False
            for filter_key, conditions in filters.items():
                enabled = conditions[0]
                if not enabled:
                    continue
                if id_type.startswith(filter_key):
                    skip_item = True
                    continue
                if len(conditions) > 1:
                    property_name, property_value = conditions[1:]
                    property_filter = item.get(property_name)
                    if property_filter and property_filter.lower() == property_value.lower():
                        skip_item = True
                        break
            if skip_item:
                continue

            if display_category not in items_data:
                items_data[display_category] = []

            processed_item = {
                "page_name": page_name,
                "item_name": translated_item_name,
                "icon": icon,
                "item_id": item_id,
                "id_rec": item.page_exists()
            }

            items_data[display_category].append(processed_item)
            pbar.update(1)

    for display_category in items_data:
        items_data[display_category] = sorted(items_data[display_category], key=lambda x: x["item_name"])

    write_to_output(items_data)


def main():
    Language.get()
    generate_item_list()

if __name__ == "__main__":
    main()
