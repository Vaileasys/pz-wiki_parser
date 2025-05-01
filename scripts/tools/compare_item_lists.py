"""This script is used to compare 2 txt files for unique item IDs.
The txt files should be in the format of the 'PZwiki:Item_list' article (item_list.py).
"""

import os
import re

INPUT1_PATH = os.path.join("resources", "PZwiki_Item_list_1.txt")
INPUT2_PATH = os.path.join("resources", "PZwiki_Item_list_2.txt")
OUTPUT_DIR = os.path.join("output", "compared_items")


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

def get_version(file_path):
    """Extracts the version number from the Page version template."""
    version_pattern = re.compile(r"{{Page version\|(\d+\.\d+\.\d+)\|")
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = version_pattern.search(line)
            if match:
                return match.group(1)
    return "unknown"

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

def write_results(common, unique1, unique2, version1, version2, include_ids):
    """Writes the comparison results to separate text files with versioned filenames."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    common_output_path = os.path.join(OUTPUT_DIR, f"common_items_{version1}_to_{version2}.txt")
    output1_path = os.path.join(OUTPUT_DIR, f"unique_{version1}.txt")
    output2_path = os.path.join(OUTPUT_DIR, f"unique_{version2}.txt")

    def format_item(name, item_id):
        return f"*{name} ({item_id})" if include_ids else f"*{name}"

    def write_sorted(file_path, items):
        sorted_items = sorted(items.items(), key=lambda x: x[1])
        with open(file_path, "w", encoding="utf-8") as file:
            file.write('<div class="list-columns">\n')
            for item_id, name in sorted_items:
                file.write(f"{format_item(name, item_id)}\n")
            file.write('</div>')

    write_sorted(common_output_path, common)
    write_sorted(output1_path, unique1)
    write_sorted(output2_path, unique2)

    return common_output_path, output1_path, output2_path

def main():
    print(f"Comparing: '{INPUT1_PATH}' and '{INPUT2_PATH}'")
    include_ids = input("1: Include item IDs\n2: Exclude item IDs\n> ") == "1"
    if os.path.exists(INPUT1_PATH) and os.path.exists(INPUT2_PATH):
        version1 = get_version(INPUT1_PATH)
        version2 = get_version(INPUT2_PATH)

        common, unique1, unique2 = compare_item_ids(INPUT1_PATH, INPUT2_PATH)
        write_results(common, unique1, unique2, version1, version2, include_ids)

        print(f"Results written to '{OUTPUT_DIR}'")
    else:
        failed_source = []
        if not os.path.exists(INPUT1_PATH):
            failed_source.append(f"'{INPUT1_PATH}'")
        if not os.path.exists(INPUT2_PATH):
            failed_source.append(f"'{INPUT2_PATH}'")
        print(f"Error: Unable to locate the following source file(s): {', '.join(failed_source)}")

if __name__ == "__main__":
    main()