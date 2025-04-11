"""
This script gets all the items present in a 'scripts' folder and outputs the item id and name to a csv file.
The generated file can then be compared with an existing file. This is used to compare which items have been added/removed between versions. 
New items will be added to a new 'Compared' CSV file and 'new items' wikitable.
"""

import os
import csv
from scripts.parser import item_parser
from scripts.core.version import Version
from scripts.core.language import Language

def generate_csv(data, file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, file)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        file_path = file_path.replace('\\', '/')
        print(f"CSV file generated, which can be found in '{file_path}'.")

def compare_csv(file1, file2, output_file, wiki_output_file):
    with open(file1, mode='r') as f1, open(file2, mode='r') as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)

        items1 = {rows[0]: rows[1] for rows in reader1}
        items2 = {rows[0]: rows[1] for rows in reader2}

        unique_items = []
        table = ['{| class="wikitable theme-blue"\n! # !! Name !! Item ID']
        count = 1
        for item_id, name in items1.items():
            if item_id not in items2:
                count += 1
                unique_items.append([item_id, name])
                table.append(f"|-\n| {count} || [[{name}]] || {item_id}")
        table.append("|}")

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(unique_items)
    print(f"Unique items have been written to {output_file}")

    with open(wiki_output_file, mode='w', encoding='utf-8') as file:
        file.write("\n".join(table))
    print(f"Wiki list has been written to {wiki_output_file}")

def main():
    language_code = Language.get()
    output_dir = f'output/{language_code}/items_version'

    data = []
    for item_id, item_data in item_parser.get_item_data().items():
        name = item_data.get('DisplayName', 'Unknown')
        data.append([item_id, name])

    game_version = Version.get()
    output_file = f'items_{game_version}.csv'
    generate_csv(data, output_file, output_dir)
    output_file = os.path.join(output_dir, output_file)

    compare_option = input("Want to compare the generated file with another CSV file? (y/n):\n> ").strip().lower()
    if compare_option == 'y':
        compare_version = input("Enter the version to compare with:\n> ").strip()
        compare_path = os.path.join(output_dir, f"items_{compare_version}.csv")
        print(compare_path)
        if os.path.exists(compare_path):
            compare_csv(output_file, compare_path, f'{output_dir}/Compared {compare_version} and {game_version}.csv', f'{output_dir}/{game_version} new items.txt')
        else:
            print(f"Comparison file 'items_{compare_version}.csv' not found in the output folder.")
    else:
        print("Comparison skipped.")

if __name__ == "__main__":
    main()