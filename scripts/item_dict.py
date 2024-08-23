import os
import shutil
import csv
import script_parser
from core import utility

"""
This script gets all the items present in a 'scripts' folder and outputs the item id and name to a csv file.
The generated file can then be compared with an existing file. This is used to compare which items have been added/removed between versions. 
New items will be added to a new 'Compared' CSV file and 'new items' wikitable.
"""

directory = "output/items_version"

def generate_csv(data, file):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file)
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
    script_parser.init()
    data = []
    for module, module_data in script_parser.parsed_item_data.items():
        for item_type, item_data in module_data.items():
            item_id = f"{module}.{item_type}"
            name = item_data.get('DisplayName', 'Unknown')
            data.append([item_id, name])

    version = utility.version
    output_file = f'items_{version}.csv'
    generate_csv(data, output_file)
    output_file = os.path.join(directory, output_file)
    
    compare_option = input("Want to compare the generated file with another CSV file? (y/n):\n> ").strip().lower()
    if compare_option == 'y':
        compare_version = input("Enter the version to compare with:\n> ").strip()
        compare_path = os.path.join(directory, f"items_{compare_version}.csv")
        print(compare_path)
        if os.path.exists(compare_path):
            compare_csv(output_file, compare_path, f'{directory}/Compared {compare_version} and {version}.csv', f'{directory}/{version} new items.txt')
        else:
            print(f"Comparison file 'items_{compare_version}.csv' not found in the output folder.")
    else:
        print("Comparison skipped.")

if __name__ == "__main__":
    main()