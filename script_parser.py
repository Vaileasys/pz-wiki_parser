import os
from core import translate

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

# find a module for an item and return item_id (used for property values that don't define the module)
def get_module_from_item(parsed_data, item_data, property_name):
    item_types = item_data.get(property_name, [])
    modules = {}
    
    for item_type in item_types:
        item_type = item_type.strip()
        for module, items in parsed_data.items():
            if item_type in items:
                modules[item_type] = f"{module}.{item_type}"
                break

    return modules

# parse each line and add to a "data" dictionary
def parse_file(file_path, data):
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
                    item_name = translate.get_translation(item_id, 'DisplayName', 'en')
                    if item_name is not None:
                        data[current_module][current_type][prop] = item_name
                    else:
                        data[current_module][current_type][prop] = value
                else:
                    # check for ';' for fourth level
                    if ';' in value:
                        data[current_module][current_type][prop] = value.split(';')
                    else:
                        data[current_module][current_type][prop] = value
                
#    print("Parsed Data:\n", data)
    return data, type_counter


# defines the files to be parsed - will parse every txt file in the "folder_path"
def parse_files_in_folder(folder_path):
    parsed_data = {}
    total_type_counter = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
#            print("Processing", filename)
            file_path = os.path.join(folder_path, filename)
            parsed_data, type_counter = parse_file(file_path, parsed_data)
            total_type_counter += type_counter
            
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
    parsed_data, total_type_counter = parse_files_in_folder('resources/scripts')
    output_parsed_data_to_txt(parsed_data, 'logging/parsed_data.txt')
    print("Total items parsed:", total_type_counter)
    return parsed_data
    
if __name__ == "__main__":
    main()