import os
import script_parser
from core import translate

filters = {
    'MakeUp_': (True,),
    'obsolete': (True, 'OBSOLETE', 'true')
#    'ExampleFilter': (False, 'PropertyName', 'PropertyValue')
}


def write_to_output(sorted_items):
    language_code = translate.language_code
    # write to output.txt
    output_file = 'output/output.txt'
    with open(output_file, 'w', encoding='utf-8') as file:

        lc_subpage = ""
        if language_code != "en":
            lc_subpage = f"/{language_code}"

        for display_category in sorted(sorted_items.keys()):
            file.write(f"=={display_category}==\n")
            file.write("{| class=\"wikitable theme-blue\"\n! Icon !! Name !! Item ID\n")
            for item_name, translated_item_name, icons, item_id in sorted_items[display_category]:
                icons_image = ' '.join([f"[[File:{icon}.png|32x32px]]" for icon in icons])
                item_link = f"[[{item_name}]]"

                if language_code != "en":
                    item_link = f"[[{item_name}{lc_subpage}|{translated_item_name}]]"
                file.write(f"|-\n| {icons_image} || {item_link} || {item_id}\n")
            file.write("|}\n\n")

        file.write(f"==See also==\n*[[PZwiki:Tile list{lc_subpage}]]")
    print(f"Output saved to {output_file}")


def item_list(parsed_data):
    sorted_items = {}
    icon_dir = 'resources/icons/'

    for module, module_data in parsed_data.items():
        for item_type, item_data in module_data.items():
            # Check if 'DisplayCategory' property exists for the item
            if 'DisplayCategory' in item_data:
                display_category = item_data.get('DisplayCategory', 'Other')
                
                icons = []
                
                # check if 'IconsForTexture' property exists and use it for icon
                if 'IconsForTexture' in item_data:
                    icons_for_texture = item_data.get('IconsForTexture', [''])
                    icons = [icon.strip() for icon in icons_for_texture]
                else:
                    # get 'Icon' property
                    icon = item_data.get('Icon', ['Question'])
                    if icon != "default":
                        icons.append(icon)

                if icon == "Question":
                    icons_for_texture = item_data.get('IconsForTexture', [''])
                    if icons_for_texture:
                        icons = [icon.strip() for icon in icons_for_texture]
                
                # check if icon has variants
                icon_variants = ['Rotten', 'Cooked', '_Cooked', 'Burnt', 'Overdone']
                for variant in icon_variants:
                    variant_icon = f"{icon}{variant}.png"
                    if os.path.exists(os.path.join(icon_dir, variant_icon)):
                        icons.append(icon + variant)

                # check if 'WorldObjectSprite' property exists and use it for icon
                if icon == "default":
                    icon = item_data.get('WorldObjectSprite', ['Flatpack'])
                    icons.append(icon)
                
                item_name = item_data.get('DisplayName', [''])
                item_id = f"{module}.{item_type}"

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
                sorted_items[display_category].append((item_name, translated_item_name, icons, item_id))
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
            filter_name = filter_name or property_value # change filter_name to property_value if empty
            filters[filter_name] = (True, property_name, property_value)
            print(f"Filter added: {filter_name} ({property_name} = {property_value})")
        elif filter_input == "done":
            return
        else:
            print("Invalid filter name. Please try again.")


def init():
    while True:
        user_input = input("Run script ('y') or set up a filter ('filter')?\n> ")
        if user_input == "y":
            item_list(script_parser.main())
            return
        
        # filters
        elif user_input == "filter":
            filters_tree()
            continue
        
        # cancel
        elif user_input == "n":
            print("Script cancelled")
            return
        
        # repeat
        else:
            continue


if __name__ == "__main__":
    init()
