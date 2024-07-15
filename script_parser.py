import os
import sys
import chardet

language_code = ""
language_codes = {
    'ar': "Cp1252", 
    'ca': "ISO-8859-15", 
    'ch': "UTF-8", 
    'cn': "UTF-8", 
    'cs': "Cp1250", 
    'da': "Cp1252", 
    'de': "Cp1252", 
    'en': "UTF-8", 
    'es': "Cp1252", 
    'fi': "Cp1252", 
    'fr': "Cp1252", 
    'hu': "Cp1250", 
    'id': "UTF-8", 
    'it': "Cp1252", 
    'jp': "UTF-8", 
    'ko': "UTF-16", 
    'nl': "Cp1252", 
    'no': "Cp1252", 
    'ph': "UTF-8", 
    'pl': "Cp1250", 
    'pt': "Cp1252", 
    'ptbr': "Cp1252", 
    'ro': "UTF-8", 
    'ru': "Cp1251", 
    'th': "UTF-8", 
    'tr': "Cp1254", 
    'ua': "Cp1251"
}

def get_language():
    global language_code
    language_code = input("Enter language code (default 'en')\n> ").strip().lower()
    if language_code in language_codes:
        print(f"Language code '{language_code}' selected.")
    else:
        language_code = "en"
        print("Unrecognised language code, setting to 'en'")

    translate_names = {}
    if language_code != "en":
        translate_names = parse_item_names(f'resources/Translate/ItemName/ItemName_{language_code.upper()}.txt', language_code)
    
    return translate_names, language_code

# detect encoding and return best-fit
def detect_file_encoding(file_path):
    print(f"Detecting encoding for '{file_path}'")
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"File encoded with '{encoding}'")
    return encoding

def read_file_with_encoding(file_path, encoding):
    item_names = {}
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            for line in file:
                line = line.strip()
                if line.startswith("ItemName_"):
                    item_id, item_name = line.split(" = ")
                    item_id = item_id[len("ItemName_"):].strip()
                    item_name = item_name.strip('"').rstrip('",')
                    item_names[item_id] = item_name
    except UnicodeDecodeError:
        print(f"Warning: There was an issue decoding the file '{file_path}' with encoding '{encoding}'.")
    return item_names


# parse the item names from translate file
def parse_item_names(file_path, lang_code):
    if not os.path.exists(file_path):
        print(f"No file found for '{file_path}'. Ensure the file is in the correct path, or try a different language code.")
        sys.exit()
    language_code = lang_code
    encoding = language_codes.get(language_code, "")
    if not encoding:
        encoding = "UTF-8"
        print(f"No encoding found for language code '{language_code}', defaulting to UTF-8")
    else:
        print(f"Encoding for language code '{language_code}' set to {encoding}")
    item_names = read_file_with_encoding(file_path, encoding)
    if item_names is None:
        print(f"Warning: There was an issue decoding the file '{file_path}' with encoding '{encoding}'. Trying to detect encoding.")
        encoding = detect_file_encoding(file_path)
        item_names = read_file_with_encoding(file_path, encoding)
        if item_names is None:
            print(f"Error: There was an issue decoding the file '{file_path}' with detected encoding '{encoding}'.")
            exit(1)
    return item_names

# parse each line and add to a "data" dictionary
# 'item_names' retrieved from the parse_item_names function
def parse_file(file_path, data, item_names):
    current_module = None
    current_type = None
    block = None
    indent_level = 0
    is_comment = False
    is_imports_block = False
    type_counter = 0
    block_type = None # TODO: give user option to define the block type (e.g. item, recipe, fixing, etc.)

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            
            # skip if comments encountered
            if line.startswith('/*'):
                is_comment = True
                if '*/' in line:
                    is_comment = False
                continue
            if is_comment:
                if '*/' in line:
                    is_comment = False
                continue
            
            # skip imports block
            if line.startswith('imports'):
                indent_level += 1
                is_imports_block = True
            elif is_imports_block:
                if line.startswith('}'):
                    indent_level -= 1
                    is_imports_block = False
                continue
                        
            # open module
            if line.startswith('module'):
                block = 'module'
                indent_level += 1
                current_module = line.split()[1]
                if current_module not in data:
                    data[current_module] = {}
                # module already exists, update block value
                if 'block' not in data[current_module]:
                    data[current_module]['block'] = block
            # close module block
            elif line.startswith('}') and indent_level == 1:
                indent_level -= 1
                current_module = None
                block = None

            # open item block
            if block_type == None:
                block_type = 'item'
            elif line.startswith(block_type) and indent_level == 1:
                indent_level += 1
                block = block_type
                current_type = line.split()[1]
                if current_module not in data:
                    data[current_module] = {}
                if current_type not in data[current_module]:
                    data[current_module][current_type] = {'block': block}
                    type_counter += 1
                else:
                    # type already exists, update block value
                    block = data[current_module][current_type]['block']
            # close item block
            elif line.startswith('}') and indent_level == 2:
                indent_level -= 1
                block = None
            
            # get properties
            elif '=' in line and current_module and current_type:
                prop, value = line.split('=', 1)
                prop = prop.strip()
                value = value.rstrip(',').strip()

                if prop == 'DisplayName':
                    item_id = f"{current_module}.{current_type}"
                    item_name = item_names.get(item_id, None)
                    if item_name is not None:
                        data[current_module][current_type][prop] = item_name
                    else:
                        data[current_module][current_type][prop] = value
                else:
                    data[current_module][current_type][prop] = value
                
#    print("Parsed Data:\n", data)
    return data, type_counter


# defines the files to be parsed - will parse every txt file in the "folder_path"
def parse_files_in_folder(folder_path, item_names):
    parsed_data = {}
    total_type_counter = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
#            print("Processing", filename)
            file_path = os.path.join(folder_path, filename)
            parsed_data, type_counter = parse_file(file_path, parsed_data, item_names)
            total_type_counter += type_counter
#    print("Script files parsed successfully")
    return parsed_data, total_type_counter


# for debugging - outputs all the parsed data into a txt file called "parsed_data.txt"
def output_parsed_data_to_txt(data, output_file):
    with open(output_file, 'w') as file:
        for module, module_data in data.items():
            if 'block' in module_data:
                block_value = module_data.pop('block')
                file.write(f"{block_value} {module}\n")
            for item_type, type_data in module_data.items():
                if 'block' in type_data: 
                    block_value = type_data.pop('block')
                    file.write(f"    {block_value} {item_type}\n")
                else:
                    file.write(f"    {item_type}\n")
                for prop, values in type_data.items():
                    file.write(f"        {prop} = {values}\n")
                file.write('\n')



def main():
    language_code = "en"
    item_names = parse_item_names('resources/Translate/ItemName/ItemName_EN.txt', language_code)
    parsed_data, total_type_counter = parse_files_in_folder('resources/scripts', item_names)
    output_parsed_data_to_txt(parsed_data, 'parsed_data.txt')
    print("Total items parsed:", total_type_counter)
    return parsed_data
    
if __name__ == "__main__":
    main()