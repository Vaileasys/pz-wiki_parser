import os
import script_parser
from core import utility

def main(user_input):
    tags_dict = {}
    for module, module_data in script_parser.parsed_item_data.items():
        for item_type, item_data in module_data.items():
            if 'Tags' in item_data:
                item_id = f"{module}.{item_type}"
                name = item_data.get('DisplayName')
                icon = utility.get_icon(item_data, item_id)
                tags = item_data.get('Tags', [])
                if isinstance(tags, str):
                    tags = [tags]
                for tag in tags:
                    if tag not in tags_dict:
                        tags_dict[tag] = []
                    tags_dict[tag].append({'item_id': item_id, 'icon': icon, 'name': name})
                    
    if user_input == "1":
        print("Running Tag images script...")
        write_tag_image(tags_dict)
    elif user_input == "2":
        print("Running Tag table script...")
        write_tag_table(tags_dict)
    elif user_input == "3":
        print("Running Tag item list script...")
        write_tag_list(tags_dict)
    else:
        print("Running both scripts...")
        write_tag_image(tags_dict)
        write_tag_table(tags_dict)


# write each tag's item icons for `cycle-img`
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


# write a wikitable showing all tags and corresponding items
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


# write each tag item as an item_list
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


if __name__ == "__main__":
    script_parser.init()
    while True:
        print("""Choose a script to run.
    0: Both
    1: Tag images
    2: Tag table
    3: Tag item list""")

        user_input = input("> ")

        if user_input == "":
            user_input = "0"

        if user_input in {"0", "1", "2", "3"}:
            main(user_input)
            break