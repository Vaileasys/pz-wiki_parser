import os
from core import translate

parsed_item_data = ""
parsed_fixing_data = ""


# parse fixing data
def get_fixing_properties(line, data, current_module, current_fixing):   
    if ':' in line and current_module and current_fixing:
        role, value = line.split(':', 1)
        role = role.strip()
        value = value.rstrip(',').strip()

        if role == 'Fixer':
            fixer_entries = value.split(';')
            if 'Fixer' not in data[current_module][current_fixing]:
                data[current_module][current_fixing]['Fixer'] = []
            
            fixer_item = {}
            for entry in fixer_entries:
                entry = entry.strip()
                if '=' in entry:
                    key, val = entry.split('=')
                    key = key.strip()
                    val = int(val.strip())
                else:
                    key = entry.strip()
                    val = 1
                
                fixer_item[key] = {'amount': val}

            data[current_module][current_fixing]['Fixer'].append(fixer_item)
        elif role == 'Require':
            data[current_module][current_fixing]['Require'] = value

    return


# parse item data
def get_item_properties(line, data, current_module, current_item):
    # get properties
    if '=' in line and current_module and current_item:
        prop, value = line.split('=', 1)
        prop = prop.strip()
        value = value.rstrip(',').strip()

        if prop == 'DisplayName':
            item_id = f"{current_module}.{current_item}"
            item_name = translate.get_translation(item_id, 'DisplayName', 'en')
            if item_name is not None:
                data[current_module][current_item][prop] = item_name
            else:
                data[current_module][current_item][prop] = value
        else:
            # check for ';' for fourth level
            if ';' in value:
                data[current_module][current_item][prop] = value.split(';')
            else:
                data[current_module][current_item][prop] = value
    return


# parse each line and add to a "data" dictionary
def parse_file(file_path, data, block_type="item"):
    current_module = None
    current_type = None
    block = None
    indent_level = 0
    is_comment = False
    is_imports_block = False
    type_counter = 0
#    block_type = "fixing" # TODO: give user option to define the block type (e.g. item, recipe, fixing, etc.)

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
            if line.startswith(block_type) and indent_level == 1:
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
                    print(f"Type '{current_type}' already exists when parsing '{block_type}'")
                    current_type = None
                    continue
            # close item block
            elif line.startswith('}') and indent_level == 2:
                indent_level -= 1
                block = None
                
            
            # get item properties
            elif block == "item" and indent_level == 2:
                get_item_properties(line, data, current_module, current_type)
            elif block == "fixing" and indent_level == 2:
                get_fixing_properties(line, data, current_module, current_type)
                
    return data, type_counter


# defines the files to be parsed - will parse every txt file in the "folder_path"
def parse_files_in_folder(folder_path):
    parsed_item_data = {}
    parsed_fixing_data = {}
    total_item_counter = 0
    total_fixing_counter = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
#            print("Processing", filename)
            file_path = os.path.join(folder_path, filename)
            parsed_item_data, item_counter = parse_file(file_path, parsed_item_data)
            parsed_fixing_data, fixing_counter = parse_file(file_path, parsed_fixing_data, "fixing")
            total_item_counter += item_counter
            total_fixing_counter += fixing_counter
            
    return parsed_item_data, parsed_fixing_data, total_item_counter, total_fixing_counter


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
                    # fixing
                    if prop == 'Fixer':
                        file.write(f"        {prop}:\n")
                        for fixer_dict in values:
                            fixer_line = '; '.join(f"{key} = {val['amount']}" for key, val in fixer_dict.items())
                            file.write(f"            {fixer_line}\n")
                    # item
                    else:
                        file.write(f"        {prop} = {values}\n")
                file.write('\n')


# initialise parser
def init():
    global parsed_item_data
    global parsed_fixing_data
    parsed_item_data, parsed_fixing_data, total_item_counter, total_fixing_counter = parse_files_in_folder('resources/scripts')
    output_parsed_data_to_txt(parsed_item_data, 'logging/parsed_data.txt')
    output_parsed_data_to_txt(parsed_fixing_data, 'logging/parsed_fixing_data.txt')
    print("Total items parsed:", total_item_counter)
    print("Total fixings parsed:", total_fixing_counter)

    
if __name__ == "__main__":
    init()