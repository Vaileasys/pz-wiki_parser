import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from core import utility


def extract_code_snippet(line_number, lines):
    item_code = ""
    for i in range(line_number, len(lines)):
        item_code += lines[i]
        if '}' in lines[i]:
            break
    return item_code, line_number + 1


def write_snippet(name, cleaned_code, line, source, version, output_dir):
    formatted_code = f"""{{{{CodeSnip
  | lang = java
  | line = true
  | start = {line}
  | source = {source}
  | retrieved = true
  | version = {version}
  | code =
{cleaned_code}
}}}}"""

    formatted_code_cleaned = "\n".join([line.rstrip() for line in formatted_code.splitlines()])
    with open(os.path.join(output_dir, f'{name}.txt'), 'w') as f:
        f.write(formatted_code_cleaned)


def save_snippet(item_name, item_code, line, source, version, output_dir):
    # Remove trailing whitespace
    cleaned_code = "\n".join([line.rstrip() for line in item_code.splitlines()])
    write_snippet(item_name, cleaned_code, line, source, version, output_dir)

    if item_name.endswith("TEXTURE_TINT") or item_name.endswith("DECAL_TINT"):
        base_name = item_name.replace("TEXTURE_TINT", "").replace("DECAL_TINT", "")
        write_snippet(base_name, cleaned_code, line, source, version, output_dir)


def process_file(file_path, version, output_dir):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith('item'):
                item_code, line_num = extract_code_snippet(i, lines)
                item_name = line.split()[1]
                save_snippet(item_name, item_code, line_num, os.path.basename(file_path), version, output_dir)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def main():
    version = utility.version
    output_dir = 'output/codesnips'
    resources_dir = 'resources/scripts'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = [os.path.join(root, file) for root, _, files in os.walk(resources_dir) for file in files]

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(process_file, file_path, version, output_dir) for file_path in files]
        for future in as_completed(futures):
            pass


if __name__ == "__main__":
    main()
