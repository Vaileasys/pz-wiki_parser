"""
Gets all tags and the items with those tags.
Can be output in 3 formats:
    1: Tag images: Outputs all items as a cycling image.
    2: Tag item list: Outputs a separate table for each tag with a list of items that have it.
    3: Tag table: Outputs all tags in a single table with a list of items that have it.
"""

import os
from scripts.parser import item_parser
from scripts.core import utility


def generate_tags_dict():
    tags_dict = {}
    for item_id, item_data in item_parser.get_item_data().items():
        if 'Tags' in item_data:
            name = item_data.get('DisplayName')
            icon = utility.get_icon(item_data, item_id)
            tags = item_data.get('Tags', [])
            if isinstance(tags, str):
                tags = [tags]
            for tag in tags:
                if tag not in tags_dict:
                    tags_dict[tag] = []
                tags_dict[tag].append({'item_id': item_id, 'icon': icon, 'name': name})
    return tags_dict


def main():

    print("""Choose a script to run.
0: All
1: Tag images - Outputs all items as a cycling image.
2: Tag item list - Outputs a separate table for each tag with a list of items that have it.
3: Tag table - Outputs all tags in a single table with a list of items that have it.
Q: Quit.""")

    user_input = input("> ") or "0"

    if user_input.lower() == 'q':
        return

    tags_dict = generate_tags_dict()

    script_options = {
        "1": write_tag_image,
        "2": write_tag_list,
        "3": write_tag_table,
    }

    if user_input == "0":
        print("Running all scripts...")
        for func in script_options.values():
            func(tags_dict)
    elif user_input in script_options:
        print(f"Running selected script ({user_input})...")
        script_options[user_input](tags_dict)
    else:
        print("Invalid option. Exiting.")


# Write each tag's item icons for `cycle-img`
def write_tag_image(tags_dict):
    output_dir = "output/tags/cycle-img/"
    os.makedirs(output_dir, exist_ok=True)
    for tag, tag_data in tags_dict.items():
        output_file = os.path.join(output_dir, f'{tag}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('<span class="cycle-img">')
            for item in tag_data:
                icon = item['icon']
                name = item['name']
                file.write(f"[[File:{icon}.png|32x32px|link={tag} (tag)|{name}]]")
            file.write("</span>")
    print(f"Completed Tag images script. Files can be found in '{output_dir}'")


# Write a wikitable showing all tags and corresponding items
def write_tag_table(tags_dict):
    output_dir = "output/tags/"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'tags_table.txt')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('{| class="wikitable theme-blue"\n|-\n! Tag !! Items\n')
        for tag in sorted(tags_dict.keys()):
            tag_data = tags_dict[tag]
            names = sorted(item['name'] for item in tag_data)
            tag_items = ', '.join(f'[[{name}]]' for name in names)
            file.write(f'|-\n| <span id="tag-{tag}">[[{tag} (tag)|{tag}]]</span> || {tag_items}\n')
        file.write('|}')
    print(f"Completed Tag table script. File can be found in '{output_file}'")


# Write each tag item as an item_list
def write_tag_list(tags_dict):
    output_dir = "output/tags/item_list/"
    os.makedirs(output_dir, exist_ok=True)
    for tag, tag_data in tags_dict.items():
        output_file = os.path.join(output_dir, f'{tag}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('{| class="wikitable theme-blue sortable" style="text-align:center;"\n! Icon !! name !! Item ID\n')
            for item in tag_data:
                item_id = item['item_id']
                icon = item['icon']
                name = item['name']
                file.write(f"|-\n| [[File:{icon}.png|32x32px]] || [[{name}]] || {item_id}\n")
            file.write('|}')
    print(f"Completed Tag item list script. Files can be found in '{output_dir}'")


if __name__ == "__main__":
    main()
