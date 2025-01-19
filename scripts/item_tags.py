"""
Gets all tags and the items with those tags.
Can be output in 3 formats:
    1: Tag images: Outputs all items as a cycling image.
    2: Tag item list: Outputs a separate table for each tag with a list of items that have it.
    3: Tag table: Outputs all tags in a single table with a list of items that have it.
"""

import os
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core import utility

pbar_format = "{l_bar}{bar:30}{r_bar}"

def generate_tags_dict():
    tags_dict = {}
    parsed_item_data = item_parser.get_item_data()

    with tqdm(total=len(parsed_item_data), desc="Generating tag data", bar_format=pbar_format, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f"Processing: {item_id[:15]}")
            if 'Tags' in item_data:
                name = item_data.get('DisplayName')
                icon = utility.get_icon(item_id)
                tags = item_data.get('Tags', [])
                if isinstance(tags, str):
                    tags = [tags]
                for tag in tags:
                    if tag not in tags_dict:
                        tags_dict[tag] = []
                    tags_dict[tag].append({'item_id': item_id, 'icon': icon, 'name': name})
            pbar.update(1)
        pbar.bar_format = f"Tag data generated."
    return tags_dict


# Write each tag's item icons for `cycle-img`
def write_tag_image(tags_dict):
    output_dir = "output/tags/cycle-img/"
    os.makedirs(output_dir, exist_ok=True)

    with tqdm(total=len(tags_dict), desc="Generating tag images", bar_format=pbar_format, unit=" tags") as pbar:
        for tag, tag_data in tags_dict.items():
            # Change the string at the end of the progress bar
            pbar.set_postfix_str(f"Processing: {tag[:15]}")
            output_file = os.path.join(output_dir, f'{tag}.txt')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write('<span class="cycle-img">')
                for item in tag_data:
                    icon = item['icon']
                    name = item['name']
                    file.write(f"[[File:{icon}|32x32px|link={tag} (tag)|{name}]]")
                file.write("</span>")
            pbar.update(1)
        pbar.bar_format = f"Tag images completed. Files can be found in '{output_dir}'"


# Write a wikitable showing all tags and corresponding items
def write_tag_table(tags_dict):
    output_dir = "output/tags/"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'tags_table.txt')

    with tqdm(total=len(tags_dict), desc="Generating tags table", bar_format=pbar_format, unit=" tags") as pbar:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('{| class="wikitable theme-blue"\n|-\n! Tag !! Items\n')
            for tag in sorted(tags_dict.keys()):
                # Change the string at the end of the progress bar
                pbar.set_postfix_str(f"Processing: {tag[:15]}")

                tag_data = sorted(tags_dict[tag], key=lambda item: item['name'])

                # Generate link for each item
                tag_items = ', '.join(
                    utility.format_link(item['name'], utility.get_page(item['item_id'], item['name']))
                    for item in tag_data
                )

                file.write(f'|-\n| <span id="tag-{tag}">[[{tag} (tag)|{tag}]]</span> || {tag_items}\n')
                pbar.update(1)
            file.write('|}')
        pbar.bar_format = f"Tags table completed. File can be found in '{output_file}'"


# Write each tag item as an item_list
def write_tag_list(tags_dict):
    output_dir = "output/tags/item_list/"
    os.makedirs(output_dir, exist_ok=True)

    with tqdm(total=len(tags_dict), desc="Generating tag item list", bar_format=pbar_format, unit=" tags") as pbar:
        for tag, tag_data in tags_dict.items():
            # Change the string at the end of the progress bar
            pbar.set_postfix_str(f"Processing: {tag[:15]}")

            output_file = os.path.join(output_dir, f'{tag}.txt')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write('{| class="wikitable theme-blue sortable" style="text-align:center;"\n! Icon !! name !! Item ID\n')
                for item in tag_data:
                    item_id = item['item_id']
                    icon = item['icon']
                    name = item['name']
                    page = utility.get_page(item_id, name)
                    link = utility.format_link(name, page)
                    file.write(f"|-\n| [[File:{icon}|32x32px]] || {link} || {item_id}\n")
                file.write('|}')
            pbar.update(1)
        pbar.bar_format = f"Tags table completed. Files can be found in '{output_dir}'"


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
    
    print("Generating tag data...")
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


if __name__ == "__main__":
    main()
