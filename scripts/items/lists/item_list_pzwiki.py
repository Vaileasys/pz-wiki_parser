import os
from tqdm import tqdm
from scripts.objects.item import Item
from scripts.core.language import Language, Translate
from scripts.core.constants import PBAR_FORMAT, ITEM_DIR
from scripts.core.file_loading import write_file
from scripts.utils import util

ROOT_PATH = os.path.join(ITEM_DIR.format(language_code=Language.get()), "lists")
OUTPUT_FILE = 'item_list.txt'

HEADER = "! <<icon>> !! <<name>> !! <<page>> !! <<item_id>>"


def generate_table(items_data: dict):
    content = []
    
    content.append('{| class="wikitable theme-blue"')
    header = Translate.get_wiki(HEADER)

    for category in sorted(items_data.keys()):
        content.extend((
            '|-',
            f'! colspan="4"| <h3 style="margin-top:0;">{category}</h3>',
            '|-',
            f'{header}'
        ))

        for item in items_data[category]:
            page_name = item["page_name"]
            item_name = item["item_name"]
            icons = item["icon"]
            item_id = item["item_id"]
            id_rec = item["id_rec"]

            icons_image = ' '.join([f"[[File:{icon}|32x32px]]" for icon in icons])

            item_link = util.link(page_name, item_name)
            page_link = util.link(page_name)

            if id_rec:
                content.append('|-')
            else:
                content.append('|- title="ID missing in infobox" style="background-color: var(--background-color-warning-subtle); color: red;"')
                item_id += "*"

            content.extend((
                f'| {icons_image}',
                f'| {item_link}',
                f'| {page_link}',
                f'| {item_id}'
            ))

    content.append("|}\n")

    write_file(content, rel_path=OUTPUT_FILE, root_path=ROOT_PATH)


def generate_item_list():
    items_data = {}

    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id in Item.keys():
            item = Item(item_id)

            pbar.set_postfix_str(f"Processing: {item.type} ({item_id[:30]})")

            category = item.display_category_name

            if category not in items_data:
                items_data[category] = []

            page_name = item.page
            if item.media_category:
                if "VHS" in item.media_category:
                    page_name = "VHS"
                elif "CD" in item.media_category:
                    page_name = "CD"

            processed_item = {
                "page_name": page_name,
                "item_name": item.name,
                "icon": item.get_icon(format=False, all_icons=True),
                "item_id": item_id,
                "id_rec": item.has_page
            }

            items_data[category].append(processed_item)
            pbar.update(1)

    for category in items_data:
        items_data[category] = sorted(items_data[category], key=lambda x: x["item_name"])

    generate_table(items_data)


def main():
    Language.get()
    generate_item_list()

if __name__ == "__main__":
    main()
