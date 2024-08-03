import os
import script_parser
from core import utility

def main(user_input):
    tags_dict = {}
    for module, module_data in script_parser.parsed_item_data.items():
        for item_type, item_data in module_data.items():
            if 'Tags' in item_data:
                name = item_data.get('DisplayName')
                icon = utility.get_icon(item_data)
                tags = item_data.get('Tags', [])
                if isinstance(tags, str):
                    tags = [tags]
                for tag in tags:
                    if tag not in tags_dict:
                        tags_dict[tag] = []
                    tags_dict[tag].append({'icon': icon, 'name': name})
                    
    if user_input == "1":
        print("Running Tag images script...")
        write_tag_image(tags_dict)
    elif user_input == "2":
        print("Running Tag table script...")
        write_tag_table(tags_dict)
    else:
        print("Running both scripts...")
        write_tag_image(tags_dict)
        write_tag_table(tags_dict)


def write_tag_image(tags_dict):
    output_dir = "output/tags/"
    os.makedirs(output_dir, exist_ok=True)
    for tag, tag_data in tags_dict.items():
        output_file = os.path.join(output_dir, f'{tag}.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('<span class="cycle-img">')
            for item in tag_data:
                icon = item['icon']
                name = item['name']
                file.write(f"[[File:{icon}.png|32x32px|link=Item tags#tag-{tag}|{name}]]")
            file.write("</span>")
    print(f"Completed Tag images script. Files can be found in '{output_dir}'")


def write_tag_table(tags_dict):
    output_dir = "output/"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'tags_table.txt')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('{| class="wikitable theme-blue"\n|-\n! Tag !! Items\n')
        for tag in sorted(tags_dict.keys()):
            tag_data = tags_dict[tag]
            names = sorted(item['name'] for item in tag_data)
            tags = ', '.join(f'[[{name}]]' for name in names)
            file.write(f'|-\n| <span id="tag-{tag}">[[#{tag}|{tag}]]</span> || {tags}\n')
        file.write('|}')
    print(f"Completed Tag table script. File can be found in '{output_file}'")
        


if __name__ == "__main__":
    script_parser.init()
    while True:
        print("""Choose a script to run.
    0: Both
    1: Tag images
    2: Tag table""")

        user_input = input("> ")

        if user_input == "":
            user_input = "0"

        if user_input in {"0", "1", "2"}:
            main(user_input)
            break