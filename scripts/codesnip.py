import os
from concurrent.futures import ThreadPoolExecutor
from scripts.core import version


def extract_code_snippet(line_number, lines):
    item_code = ""
    first_line = lines[line_number].strip()
    item_code += first_line + "\n"

    # Process the rest of the lines normally
    for i in range(line_number + 1, len(lines)):
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
    game_version = version.get_version()
    output_dir = 'output/codesnips'
    resources_dir = 'resources/scripts'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Exclude files that don't parse well
    EXCLUDED_PREFIXES = ("recipes", "entity_", "xs_", "craftrecipe", "template_", "vehicle_", "dbg_")

    files = [
        os.path.join(root, file)
        for root, _, files in os.walk(resources_dir)
        for file in files
        if not file.startswith(EXCLUDED_PREFIXES)
    ]

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(process_file, files, [game_version] * len(files), [output_dir] * len(files))


if __name__ == "__main__":
    main()
