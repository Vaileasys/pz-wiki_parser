"""This script is used to compare 2 txt files for unique item IDs.
The txt files should be in the format of the 'PZwiki:Item_list' article (item_list.py).
"""

import os
import re

INPUT1_PATH = "resources/PZwiki_Item_list_1.txt"
INPUT2_PATH = "resources/PZwiki_Item_list_2.txt"
OUTPUT_DIR = "output/compared_items"
OUTPUT_COMMON_FILE = "common_items.txt"
OUTPUT1_FILE = "unique_b41.txt"
OUTPUT2_FILE = "unique_b42.txt"


def extract_item_ids(file_path):
    """Extracts item IDs from the given file based on the format Base.<item_name>."""
    items = {}
    
    # Regex to match item name and ID
    pattern = re.compile(r"\|\|\s*(.*?)\s*\|\|.*?(?:Base|radio|farming|camping)\.\S+")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                name = match.group(1).strip()
                item_id = re.search(r"(?:Base|radio|farming|camping)\.\S+", line).group(0)
                items[item_id] = name
    
    return items


def compare_item_ids(file1, file2):
    """Compares item IDs from two files and returns common and unique item IDs."""
    items_file1 = extract_item_ids(file1)
    items_file2 = extract_item_ids(file2)

    common_ids = set(items_file1.keys()).intersection(items_file2.keys())
    unique_to_file1 = set(items_file1.keys()) - set(items_file2.keys())
    unique_to_file2 = set(items_file2.keys()) - set(items_file1.keys())

    common = {item_id: items_file1[item_id] for item_id in common_ids}
    unique1 = {item_id: items_file1[item_id] for item_id in unique_to_file1}
    unique2 = {item_id: items_file2[item_id] for item_id in unique_to_file2}

    return common, unique1, unique2


def write_results(common, unique1, unique2):
    """Writes the comparison results to separate text files."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    common_output_path = os.path.join(OUTPUT_DIR, OUTPUT_COMMON_FILE)
    output1_path = os.path.join(OUTPUT_DIR, OUTPUT1_FILE)
    output2_path = os.path.join(OUTPUT_DIR, OUTPUT2_FILE)

    with open(common_output_path, "w", encoding="utf-8") as common_file:
        common_file.write('<div class="list-columns">\n')
        for item_id, name in common.items():
            common_file.write(f"*{name}\n")
        common_file.write('</div>')

    with open(output1_path, "w", encoding="utf-8") as unique1_file:
        unique1_file.write('<div class="list-columns">\n')
        for item_id, name in unique1.items():
            unique1_file.write(f"*{name}\n")
        unique1_file.write('</div>')

    with open(output2_path, "w", encoding="utf-8") as unique2_file:
        unique2_file.write('<div class="list-columns">\n')
        for item_id, name in unique2.items():
            unique2_file.write(f"*{name}\n")
        unique2_file.write('</div>')

    return common_output_path, output1_path, output2_path


def main():
    print(f"Comparing: '{INPUT1_PATH}' and '{INPUT2_PATH}'")
    input1 = os.path.exists(INPUT1_PATH)
    input2 = os.path.exists(INPUT2_PATH)

    if input1 and input2:

        # Compare item IDs from the files
        common, unique1, unique2 = compare_item_ids(INPUT1_PATH, INPUT2_PATH)

        write_results(common, unique1, unique2)

        print(f"Results written to '{OUTPUT_DIR}'")
    else:
        failed_source = []
        if not input1:
            failed_source.append(f"'{INPUT1_PATH}'")
        if not input2:
            failed_source.append(f"'{INPUT2_PATH}'")
        print(f"Error: Unable to locate the following source file(s): {', '.join(failed_source)}")
        

if __name__ == "__main__":
    main()