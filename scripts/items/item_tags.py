import os
from difflib import SequenceMatcher
from tqdm import tqdm
from scripts.objects.item import Item
from scripts.core.version import Version
from scripts.core.language import Language
from scripts.core.constants import OUTPUT_DIR, PBAR_FORMAT, DATA_DIR
from scripts.utils import util, echo
from scripts.core.cache import save_cache, load_cache

CACHE_JSON = "tags_data.json"
is_run_locally = False

language_code = Language.get()
output_tags_dir = os.path.join(OUTPUT_DIR, language_code, "tags")

tag_data = {}


## -------------------- ARTICLE CONTENT -------------------- ##

def write_tag_image():
    """Write each tag's item icons for `cycle-img`."""
    tags_dict = get_tag_data()
    output_dir = os.path.join(output_tags_dir, "cycle-img")
    os.makedirs(output_dir, exist_ok=True)

    with tqdm(total=len(tags_dict), desc="Generating tag images", bar_format=PBAR_FORMAT, unit=" tags", leave=False) as pbar:
        for tag, tag_data in tags_dict.items():
            # Change the string at the end of the progress bar
            pbar.set_postfix_str(f"Processing: {tag[:30]}")
            output_file = os.path.join(output_dir, f'{tag}.txt')
            output_list = []
            for item in tag_data:
                icon = item['icon']
                name = item['name']
                entry = f"[[File:{icon}|32x32px|link={tag} (tag)|{name}]]"
                if entry not in output_list:
                    output_list.append(entry)

            with open(output_file, 'w', encoding='utf-8') as file:
                tag_string = "".join(output_list)
                file.write(f'<span class="cycle-img">{tag_string}</span>')
            pbar.update(1)
    echo.success(f"Tag images completed. Files can be found in '{output_dir}'")


def write_tag_table():
    """Write a wikitable showing all tags and corresponding items."""
    tags_dict = get_tag_data()
    output_dir = output_tags_dir
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'tags_table.txt')

    with tqdm(total=len(tags_dict), desc="Generating tags table", bar_format=PBAR_FORMAT, unit=" tags", leave=False) as pbar:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('{| class="wikitable theme-blue"\n|-\n! Tag !! Items\n')
            for tag in sorted(tags_dict.keys()):
                # Change the string at the end of the progress bar
                pbar.set_postfix_str(f"Processing: {tag[:30]}")

                tag_data = sorted(tags_dict[tag], key=lambda item: item['name'])

                # Generate link for each item
                tag_items = ', '.join(
                    util.link(item['page'], item['name'])
                    for item in tag_data
                )

                file.write(f'|- id="tag-{tag}"\n| [[{tag} (tag)|{tag}]] || {tag_items}\n')
                pbar.update(1)
            file.write('|}')
    echo.success(f"Tags table completed. File can be found in '{output_file}'")


def write_tag_list():
    """Write each tag item as an item_list."""
    tags_dict = get_tag_data()
    output_dir = os.path.join(output_tags_dir, "item_list")
    os.makedirs(output_dir, exist_ok=True)

    with tqdm(total=len(tags_dict), desc="Generating tag item list", bar_format=PBAR_FORMAT, unit=" tags", leave=False) as pbar:
        for tag, tag_data in tags_dict.items():
            # Change the string at the end of the progress bar
            pbar.set_postfix_str(f"Processing: {tag[:30]}")

            output_file = os.path.join(output_dir, f'{tag}.txt')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(
                    '{| class="wikitable theme-blue sortable" style="text-align: center;"\n! Icon !! Name !! Item ID\n')
                for item in tag_data:
                    item_id = item['item_id']
                    icon = item['icon']
                    name = item['name']
                    page = item['page']
                    link = util.link(page, name)
                    file.write(f"|-\n| [[File:{icon}|32x32px]] || {link} || {item_id}\n")
                file.write('|}')
            pbar.update(1)
    echo.success(f"Tags list completed. Files can be found in '{output_dir}'")


## -------------------- ARTICLES -------------------- ##


def get_see_also(all_filenames, reference_filename):
    """Get 3 similarly named filenames and include in 'see also'"""

    if len(all_filenames) < 3:
        echo.warning("Not enough files to select 3 similar filenames.")
        return []

    reference_name = os.path.splitext(reference_filename)[0]

    # Calculate similarity scores for each filename
    similarity_scores = []
    for filename in all_filenames:
        name = os.path.splitext(filename)[0]
        score = SequenceMatcher(None, reference_name, name).ratio()
        similarity_scores.append((name, score))

    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    see_also = [name for name, _ in similarity_scores if name != reference_name][:3]

    return sorted(see_also)


def write_article(tag, item_content, see_also_list, dest_dir):
    write_type = os.path.basename(os.path.normpath(dest_dir))
    file_name = tag + ".txt"
    file_path = os.path.join(dest_dir, file_name)

    os.makedirs(dest_dir, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as file:

        if write_type == "templates":
            page_content = (
                f"<noinclude>\n{{{{Documentation|doc=\n"
                f"{{{{Autogenerated|reason=Any changes to this page will be overwritten automatically ''(Last updated: {Version.get()})''.|source=[https://github.com/Vaileasys/pz-wiki_parser pz-wiki_parser (GitHub)]|hidecat=true}}}}\n"
                f"This template is used to add an image that cycles through all the icons for the [[{tag} (tag)|'{tag}' tag]].\n\n"
                f"==Usage==\n"
                f"Paste the following to the article.\n\n{{{{tlx|Tag {tag}}}}} → {{{{Tag {tag}}}}}\n\n"
                "==See also==\n"
                + "\n".join(f"*{{{{ll|Template:Tag {t}}}}}" for t in see_also_list)
                + "\n}}\n"
                "{{ll|Category:Tag templates}}\n</noinclude>"
                f"<includeonly>{item_content}</includeonly>"
            )

        elif write_type == "modding":
            page_content = (
                f"{{{{Header|Modding|Item tags}}}}\n"
                f"{{{{Page version|{Version.get()}}}}}\n{{{{Autogenerated|tags}}}}\n"
                f"'''{tag}''' is an [[item tag]].\n\n"
                "==Usage==\n"
                "[enter a list of where and how this tag is used]\n\n"
                "==List of items=="
                f"\n{item_content}\n\n"
                "==See also==\n"
                + "\n".join(f"*[[{t} (tag)]]" for t in see_also_list)
                + "\n"
            )

        if page_content is not None:
            file.write(page_content)


def get_item_list(source_dir):
    if not os.path.exists(source_dir):
        echo.error(f"The source directory {source_dir} does not exist. Make sure to run 'item_tags.py (Tag images)' first")
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
    source_dir = os.path.join(output_tags_dir, "item_list")
    if not os.path.exists(source_dir):
        echo.warning(f"'source_dir' doesn't exist, running 'Tag item list'")
        write_tag_list()
    dest_dir = os.path.join(output_tags_dir, "articles", "modding")
    item_list = get_item_list(source_dir)
    if item_list:
        all_tags = [tag for _, tag in item_list]

        with tqdm(total=len(item_list), desc="Generating modding articles", bar_format=PBAR_FORMAT, unit=" tags", leave=False) as pbar:
            for content, tag in item_list:
                # Change the string at the end of the progress bar
                pbar.set_postfix_str(f"Processing: {tag[:30]}")

                see_also = get_see_also(all_tags, tag)
                write_article(tag, content, see_also, dest_dir)

                pbar.update(1)

        echo.success(f"Modding articles completed. Files can be found in '{dest_dir}'")


## -------------------- TEMPLATE ARTICLE -------------------- ##

def generate_article_templates():
    source_dir = os.path.join(output_tags_dir, "cycle-img")
    if not os.path.exists(source_dir):
        echo.warning(f"'source_dir' doesn't exist, running 'Tag item list'")
        write_tag_image()
    dest_dir = os.path.join(output_tags_dir, "articles", "templates")
    item_list = get_item_list(source_dir)
    if item_list:
        all_tags = [tag for _, tag in item_list]

        with tqdm(total=len(item_list), desc="Generating template articles", bar_format=PBAR_FORMAT, unit=" tags", leave=False) as pbar:
            for content, tag in item_list:
                # Change the string at the end of the progress bar
                pbar.set_postfix_str(f"Processing: {tag[:30]}")

                see_also = get_see_also(all_tags, tag)
                write_article(tag, content, see_also, dest_dir)

                pbar.update(1)

        echo.success(f"Template articles completed. Files can be found in '{dest_dir}'")


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

    cache_file = os.path.join(DATA_DIR, CACHE_JSON)
    tags_dict, cache_version = load_cache(cache_file, "tags", get_version=True)
    game_version = Version.get()

    # If cache version is old, we generate new data
    if cache_version != game_version:

        with tqdm(total=Item.count(), desc="Generating tag data", bar_format=PBAR_FORMAT, unit=" items") as pbar:
            for item_id in Item.all():
                item = Item(item_id)
                pbar.set_postfix_str(f'Processing: {item.type} ({item_id[:30]})')
                if item.tags:
                    name = item.name
                    page = item.page
                    icon = item.get_icon(format=False, all_icons=False)
                    tags = item.tags
                    for tag in tags:
                        if tag not in tags_dict:
                            tags_dict[tag] = []
                        tags_dict[tag].append({'item_id': item_id, 'icon': icon, 'name': name, 'page': page})
                pbar.update(1)
            pbar.bar_format = f"Tag data generated."
            
        save_cache(tags_dict, CACHE_JSON)
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
        print(f"\nCompleted running all scripts.")

    # Run all content functions
    elif func == "all_content_functions":
        print(f"Running all article content scripts...")
        write_tag_image()
        write_tag_list()
        write_tag_table()
        print(f"\nCompleted running all article content scripts.")

    # Run function
    else:
        print(f"Running selected script ({name})...")
        globals()[func]()

    print("Returning to the menu...\n")


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
