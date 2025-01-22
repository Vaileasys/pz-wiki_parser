import os
import json
import random
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core import utility, translate, version

is_run_locally = False

pbar_format = "{l_bar}{bar:30}{r_bar}"
language_code = translate.get_language_code()
tags_dir = os.path.join("output", language_code, "tags")

tag_data = {}


## -------------------- ARTICLE CONTENT -------------------- ##

def write_tag_image():
    """Write each tag's item icons for `cycle-img`."""
    tags_dict = get_tag_data()
    output_dir = os.path.join(tags_dir, "cycle-img")
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


def write_tag_table():
    """Write a wikitable showing all tags and corresponding items."""
    tags_dict = get_tag_data()
    output_dir = tags_dir
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
                    utility.format_link(item['name'], item['page'])
                    for item in tag_data
                )

                file.write(f'|-\n| <span id="tag-{tag}">[[{tag} (tag)|{tag}]]</span> || {tag_items}\n')
                pbar.update(1)
            file.write('|}')
        pbar.bar_format = f"Tags table completed. File can be found in '{output_file}'"


def write_tag_list():
    """Write each tag item as an item_list."""
    tags_dict = get_tag_data()
    output_dir = os.path.join(tags_dir, "item_list")
    os.makedirs(output_dir, exist_ok=True)

    with tqdm(total=len(tags_dict), desc="Generating tag item list", bar_format=pbar_format, unit=" tags") as pbar:
        for tag, tag_data in tags_dict.items():
            # Change the string at the end of the progress bar
            pbar.set_postfix_str(f"Processing: {tag[:15]}")

            output_file = os.path.join(output_dir, f'{tag}.txt')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(
                    '{| class="wikitable theme-blue sortable" style="text-align:center;"\n! Icon !! name !! Item ID\n')
                for item in tag_data:
                    item_id = item['item_id']
                    icon = item['icon']
                    name = item['name']
                    page = item['page']
                    link = utility.format_link(name, page)
                    file.write(f"|-\n| [[File:{icon}|32x32px]] || {link} || {item_id}\n")
                file.write('|}')
            pbar.update(1)
        pbar.bar_format = f"Tags list completed. Files can be found in '{output_dir}'"


# Write a json with each tag, and a list of its items
def write_json_list():
    tags_dict = generate_tags_dict()
    output_dir = "output/tags/"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'tags.json')
    json_data = {}
    for tag, tag_data in tags_dict.items():
        json_data[tag] = [
            {"item_id": item["item_id"], "name": item["name"], "icon": item["icon"]}
            for item in tag_data
        ]
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)
    print(f"Completed JSON export. File can be found in '{output_file}'")


## -------------------- ARTICLES -------------------- ##

# get 3 random filenames and include in 'see also'
def get_see_also(all_filenames):
    if len(all_filenames) < 3:
        print("Not enough files to select 3 random filenames.")
        return []

    random_filenames = random.sample(all_filenames, 3)

    see_also = sorted(os.path.splitext(filename)[0] for filename in random_filenames)

    return see_also


def write_article(tag, item_content, see_also, dest_dir):
    write_type = os.path.basename(os.path.normpath(dest_dir))
    file_name = tag + ".txt"
    file_path = os.path.join(dest_dir, file_name)

    os.makedirs(dest_dir, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as file:

        if write_type == "templates":

            file.write(
                f"<noinclude>\n{{{{Documentation|doc=\nThis template is used to add an image that cycles through all the icons for the '{tag}' tag.\n\n")

            file.write(
                f"==Usage==\nPaste the following to the article.\n\n{{{{tlx|Tag {tag}}}}} → {{{{Tag {tag}}}}}\n\n")

            file.write("==See also==\n")
            file.write('\n'.join(f"*{{{{ll|Template:Tag {t}}}}}" for t in see_also))

            file.write("\n}}\n")

            file.write("{{ll|Category:Tag templates}}\n")

            file.write(f"</noinclude><includeonly>{item_content}</includeonly>")

        elif write_type == "modding":
            file.write(
                f"{{{{Header|Modding|Item tags}}}}\n{{{{Page version|{version.get_version()}}}}}\n{{{{Autogenerated|tags}}}}\n")

            file.write(f"'''{tag}''' is an [[item tag]].\n\n")

            file.write("==Usage==\n[enter a list of where and how this tag is used]\n\n")

            file.write(f"==List of items==\n{item_content}\n\n")

            file.write("==See also==\n")
            file.write('\n'.join(f"*[[{t} (tag)]]" for t in see_also))
            file.write("\n")


def get_item_list(source_dir):
    if not os.path.exists(source_dir):
        print(f"The source directory {source_dir} does not exist. Make sure to run 'item_tags.py (Tag images)' first")
        return []

    item_list = []

    for filename in os.listdir(source_dir):
        tag, _ = os.path.splitext(filename)
        source_file_path = os.path.join(source_dir, filename)

        if os.path.isfile(source_file_path):
            with open(source_file_path, 'r') as src_file:
                content = src_file.read()

            item_list.append((content, tag))

    return item_list


## -------------------- TAG ARTICLE (MODDING) -------------------- ##

def generate_article_modding():
    source_dir = os.path.join(tags_dir, "item_list")
    if not os.path.exists(source_dir):
        print(f"'source_dir' doesn't exist, running 'Tag item list'")
        write_tag_list()
    dest_dir = os.path.join(tags_dir, "articles", "modding")
    item_list = get_item_list(source_dir)
    if item_list:
        all_tags = [tag for _, tag in item_list]

        for content, tag in item_list:
            see_also = get_see_also(all_tags)
            write_article(tag, content, see_also, dest_dir)

        print(f"Modding articles completed. Files can be found in '{dest_dir}'")


## -------------------- TEMPLATE ARTICLE -------------------- ##

def generate_article_templates():
    source_dir = os.path.join(tags_dir, "cycle-img")
    if not os.path.exists(source_dir):
        print(f"'source_dir' doesn't exist, running 'Tag item list'")
        write_tag_image()
    dest_dir = os.path.join(tags_dir, "articles", "templates")
    item_list = get_item_list(source_dir)
    if item_list:
        all_tags = [tag for _, tag in item_list]

        for content, tag in item_list:
            see_also = get_see_also(all_tags)
            write_article(tag, content, see_also, dest_dir)

        print(f"Template articles completed. Files can be found in '{dest_dir}'")


## -------------------- TAG DATA -------------------- ##

def get_tag_data():
    """Retrieve tag data, generating it if not already.

    Returns:
        dict: Dictionary with keys as tag names, and values that are lists of items.
            Each item is a dictionary with the following data:
              - 'item_id': item's unique ID, including the module (Base).
              - 'icon': item's icon.
              - 'name': item's display name as it appears in-game.
              - 'page': item's page name as it is on the wiki.
    """
    global tag_data
    if not tag_data:
        tag_data = generate_tags_dict()
    return tag_data


def generate_tags_dict():
    """Generate a tags dictionary, mapping them to their associated items."""
    tags_dict = {}
    parsed_item_data = item_parser.get_item_data()

    with tqdm(total=len(parsed_item_data), desc="Generating tag data", bar_format=pbar_format, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f"Processing: {item_id[:15]}")
            if 'Tags' in item_data:
                name = utility.get_name(item_id, item_data)
                page = utility.get_page(item_id, name)
                icon = utility.get_icon(item_id)
                tags = item_data.get('Tags', [])
                if isinstance(tags, str):
                    tags = [tags]
                for tag in tags:
                    if tag not in tags_dict:
                        tags_dict[tag] = []
                    tags_dict[tag].append({'item_id': item_id, 'icon': icon, 'name': name, 'page': page})
            pbar.update(1)
        pbar.bar_format = f"Tag data generated."
    return tags_dict


## -------------------- MAIN/MENU -------------------- ##

MENU_STRUCTURE_ROOT = {
    "0": {"name": "All", "description": "", "function": "all_functions"},
    "1": {"name": "Article content", "description": "Generate tag content to be used on articles.",
          "function": "article_content"},
    "2": {"name": "Template articles", "description": "Generate tag template articles",
          "function": "generate_article_templates"},
    "3": {"name": "Modding articles", "description": "Generate tag modding articles",
          "function": "generate_article_modding"}
}

MENU_STRUCTURE_CONTENT = {
    "0": {"name": "All", "description": "", "function": "all_content_functions"},
    "1": {"name": "Tag images", "description": "Outputs all items as a cycling image.", "function": "write_tag_image"},
    "2": {"name": "Tag item list",
          "description": "Outputs a separate table for each tag with a list of items that have it.",
          "function": "write_tag_list"},
    "3": {"name": "Tag table", "description": "Outputs all tags in a single table with a list of items that have it.",
          "function": "write_tag_table"}
}


def run_function(option: dict):
    name = option["name"]
    func = option["function"]

    # Change to article content menu
    if func == "article_content":
        nav_menu(MENU_STRUCTURE_CONTENT)

    # Run all functions
    elif func == "all_functions":
        print(f"Running all scripts...")
        write_tag_image()
        write_tag_list()
        write_tag_table()
        generate_article_templates()
        generate_article_modding()
        (f"Completed running all scripts.")

    # Run all content functions
    elif func == "all_content_functions":
        print(f"Running all article content scripts...")
        write_tag_image()
        write_tag_list()
        write_tag_table()
        (f"Completed running all article content scripts.")

    # Run function
    else:
        print(f"Running selected script ({name})...")
        globals()[func]()

    print("\nReturning to the menu...\n")


def display_menu(menu, is_root=False):
    for key, value in menu.items():
        if value['description'] == "":
            print(f"{key}: {value['name']}")
        else:
            print(f"{key}: {value['name']} - {value['description']}")

    if not is_root:
        print("B: Back")
    if is_root:
        print("Q: Quit")


def nav_menu(menu, is_root=False):
    while True:
        display_menu(menu, is_root)
        user_input = input("> ").strip().upper()

        if is_root and user_input == "Q" or not is_root and user_input == "B":
            break

        if user_input in menu:
            user_choice = menu[user_input]
            run_function(user_choice)
        else:
            print("Invalid input. Please try again.")


def main():
    nav_menu(MENU_STRUCTURE_ROOT, is_run_locally)


if __name__ == "__main__":
    is_run_locally = True
    main()