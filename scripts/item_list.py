import os
import script_parser
from core import translate, utility

filters = {
    'MakeUp_': (True,),
    'obsolete': (True, 'OBSOLETE', 'true')
#    'ExampleFilter': (False, 'PropertyName', 'PropertyValue')
}

# store category translations in a dict to improve efficiency
categories = {}


# checks if a category exists in the dict before trying to translate
def translate_category(category, property="DisplayCategory"):
    if category not in categories:
        try:
            cat_translated = translate.get_translation(category, property)
            categories[category] = cat_translated
        except Exception as e:
            print(f"Error translating category '{category}': {e}")
            cat_translated = category
    else:
        cat_translated = categories[category]
    return cat_translated


def write_to_output(sorted_items):
    language_code = translate.get_language_code()
    output_dir = f'output/{language_code}/item_list/'
    output_file = f'item_list_{language_code.upper()}.txt'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    with open(output_path, 'w', encoding='utf-8') as file:

        lc_subpage = ""
        if language_code != "en":
            lc_subpage = f"/{language_code}"

        for display_category in sorted(sorted_items.keys()):
            file.write(f"=={display_category}==\n")
            file.write("{| class=\"wikitable theme-blue\"\n! Icon !! Name !! Item ID\n")
            for page_name, translated_item_name, icons, item_id in sorted_items[display_category]:
                icons_image = ' '.join([f"[[File:{icon}.png|32x32px]]" for icon in icons])
                item_link = f"[[{page_name}]]"

                if language_code != "en" or page_name != translated_item_name:
                    item_link = f"[[{page_name}{lc_subpage}|{translated_item_name}]]"
                file.write(f"|-\n| {icons_image} || {item_link} || {item_id}\n")
            file.write("|}\n\n")

        file.write(f"==See also==\n*{{{{ll|PZwiki:Tile list}}}}")
    print(f"Output saved to {output_path}")


def item_list():
    sorted_items = {}
    icon_dir = 'resources/icons/'

    for module, module_data in script_parser.parsed_item_data.items():
        for item_type, item_data in module_data.items():
            # Check if 'DisplayCategory' property exists for the item
            if 'DisplayCategory' in item_data:
                display_category = item_data.get('DisplayCategory', 'Other')
                display_category = translate_category(display_category)
                
                item_id = f"{module}.{item_type}"
                
                icons = []
                
                # check if 'IconsForTexture' property exists and use it for icon
                icons_for_texture = []
                if 'IconsForTexture' in item_data:
                    icon = "Question_On"
                    icons_for_texture = item_data.get('IconsForTexture', [''])
                    if isinstance(icons_for_texture, str):
                        icons_for_texture = [icons_for_texture]
                    icons = [icon.strip() for icon in icons_for_texture]
                else:
                    # get 'Icon' property
                    icon = utility.get_icon(item_data, item_id)
                    if icon != "default":
                        icons.append(icon)

                if icon == "Question_On":
                    if icons_for_texture:
                        icons = [icon.strip() for icon in icons_for_texture]
                
                # check if icon has variants
                icon_variants = ['Rotten', 'Spoiled', 'Cooked', '_Cooked', 'Burnt', 'Overdone']
                for variant in icon_variants:
                    variant_icon = f"{icon}{variant}.png"
                    if os.path.exists(os.path.join(icon_dir, variant_icon)):
                        icons.append(icon + variant)

                # check if 'WorldObjectSprite' property exists and use it for icon
                if icon == "default":
                    icon = item_data.get('WorldObjectSprite', ['Flatpack'])
                    icons.append(icon)
                
                # we don't need to translate again if language code is 'en'
                translated_item_name = item_data.get('DisplayName', [''])
                page_name = utility.get_page(item_id)
                if page_name == 'Unknown':
                    page_name = translated_item_name
                if translate.get_language_code() != 'en':
                    translated_item_name = translate.get_translation(item_id, "DisplayName")
                
                skip_item = False

                for filter_key, conditions in filters.items():
                    enabled = conditions[0]
                    if not enabled:
                        continue

                    if item_type.startswith(filter_key):
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

                # add item to the sorted dictionary
                if display_category not in sorted_items:
                    sorted_items[display_category] = []
                sorted_items[display_category].append((page_name, translated_item_name, icons, item_id))
    write_to_output(sorted_items)


def filters_tree():
    while True:
        print("Current filters:")
        # print a list of filters
        for filter_name, enabled in filters.items():
            print(f"{filter_name}: {'Enabled' if enabled else 'Disabled'}")
        filter_input = input("Enter filter name to toggle, 'add' to create a new filter or 'done' to exit:\n> ")

        if filter_input in filters:
            filters[filter_input] = not filters[filter_input]

        # user can add a new filter
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
            print("Invalid filter name. Please try again.")


def main():
    script_parser.init()
    while True:
        user_input = input("1: Run script\n2: Set up a filter\nQ: Quit\n> ").lower()
        if user_input == "1":
            item_list()
            return
        elif user_input == "2":
            filters_tree()
        elif user_input == "q":
            return


if __name__ == "__main__":
    main()
