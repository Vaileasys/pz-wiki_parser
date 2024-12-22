import os
import re
from scripts.core import logging_file

parsed_fixing_data = ""
scripts_dir = "resources/scripts"

def get_fixing_data():
    if not parsed_fixing_data:
        init()
    return parsed_fixing_data

# parse fixing properties
def get_fixing_properties(line, data, current_module, current_fixing):
    if current_module is None or current_fixing is None:
        logging_file.log_to_file(f"Skipping line due to unset module or type: {line}")
        return

    if current_module not in data:
        data[current_module] = {}
    if current_fixing not in data[current_module]:
        data[current_module][current_fixing] = {}

    if ':' in line:
        property, value = line.split(':', 1)
        property = property.strip()
        value = value.rstrip(',').strip()

        # 'Fixer' and 'GlobalItem' should be treated differently (GlobalItem included for future-proofing)
        if property == "Fixer" or property == "GlobalItem":
            base_property = property
            count = 1

            while f"{base_property}{count}" in data[current_module][current_fixing]:
                count += 1
            property = f"{base_property}{count}"
            data[current_module][current_fixing][property] = {'items': {}, 'skills': {}}
            value_parts = value.split(';')

            for i, fixer_data in enumerate(value_parts):
                fixer_data = fixer_data.strip()
                if '=' in fixer_data:
                    k, v = fixer_data.split('=')
                    k = k.strip()
                    v = v.strip()
                else:
                    k = fixer_data
                    v = '1'

                if i == 0:
                    data[current_module][current_fixing][property]['items'][k] = v
                else:
                    data[current_module][current_fixing][property]['skills'][k] = v

        else:
            if property not in data[current_module][current_fixing]:
                data[current_module][current_fixing][property] = []

            value_parts = value.split(';')
            for item in value_parts:
                item = item.strip()
                if item:
                    data[current_module][current_fixing][property].append(item)

    return


# parse each line and add to a "data" dictionary
def parse_file(file_path, data, block_type="fixing"):
    current_module = None
    current_type = None
    block = None
    indent_level = 0
    is_comment = False
    is_skippable_block = False
    type_counter = 0
    deprecated_message = False

    skippable_blocks = ("imports", "template")

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
            
            # skip blocks
            if any(re.match(rf'^{skippable_block}(\s|$)', line) for skippable_block in skippable_blocks):
                indent_level += 1
                is_skippable_block = True
            elif is_skippable_block:
                if line.startswith('}'):
                    indent_level -= 1
                    is_skippable_block = False
                continue
                        
            # open module
            if re.match(r'^module(\s|$)', line):
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
            if re.match(rf'^{block_type}(\s|$)', line) and indent_level == 1:
                indent_level += 1
                block = block_type
                current_type = line[len(block_type):].strip()
                if current_module not in data:
                    data[current_module] = {}
                if current_type not in data[current_module]:
                    data[current_module][current_type] = {'block': block}
                    type_counter += 1
                else:
                    # type already exists, skip it
                    logging_file.log_to_file(f"Type '{current_type}' already exists when parsing '{block_type}'")
                    current_type = None
                    continue
            # close item block
            elif line.startswith('}') and indent_level == 2:
                indent_level -= 1
                block = None
                

            elif block == "fixing" and indent_level == 2:
                get_fixing_properties(line, data, current_module, current_type)
                
    return data, type_counter


# defines the files to be parsed - will parse every txt file in the "scripts_dir"
def parse_files_in_folder():
    parsed_fixing_data = {}
    total_fixing_counter = 0
    for root, dirs, files in os.walk(scripts_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                parsed_fixing_data, fixing_counter = parse_file(file_path, parsed_fixing_data, "fixing")
                total_fixing_counter += fixing_counter
            
    return parsed_fixing_data, total_fixing_counter


# for debugging - outputs all the parsed data into a txt file
def output_parsed_data_to_txt(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
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

                for property, property_data in type_data.items():
                    # fixing
                    if 'fixing' in block_value:
                        if len(property_data) == 1:
                            property_data = str(property_data[0])
                            file.write(f"        {property}: {property_data}\n")

                        else:
                            if isinstance(property_data, list):
                                items = ', '.join(property_data)
                                file.write(f"        {property}: {items}\n")
                            else:
                                file.write(f"        {property}:\n")
                                for fixer, fixer_data in property_data.items():
                                    if fixer_data:
                                        file.write(f"            {fixer}:\n")

                                        for pair, pair_data in fixer_data.items():
                                            file.write(f"                {pair} = {pair_data}\n")
                    # item
                    else:
                        file.write(f"        {property} = {property_data}\n")
                file.write('\n')


# initialise parser
def init():
    global parsed_fixing_data
    parsed_fixing_data, total_fixing_counter = parse_files_in_folder()
    output_parsed_data_to_txt(parsed_fixing_data, 'output/logging/parsed_fixing_data.txt')
    print("Total fixings parsed:", total_fixing_counter)

    
if __name__ == "__main__":
    init()
