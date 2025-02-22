import os
import re
from scripts.core import logger, utility, version
from scripts.core.constants import DATA_PATH

CACHE_JSON = 'fixing_data.json'
SCRIPTS_DIR = "resources/scripts"

parsed_fixing_data = {}

def get_fixing_data(suppress=False):
    if not parsed_fixing_data:
        init(suppress)
    return parsed_fixing_data


# parse fixing properties
def get_fixing_properties(line, data, current_module, current_fixing):
    if current_module is None or current_fixing is None:
        logger.write(f"Skipping line due to unset module or type: {line}")
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
#TODO: remove item parsing
def parse_file(file_path, data, block_type="fixing"):
    current_module = None
    current_type = None
    block = None
    indent_level = 0
    is_comment = False
    is_skippable_block = False

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
                if current_type in data[current_module]:
                    # type already exists, skip it
                    logger.write(f"Type '{current_type}' already exists when parsing '{block_type}'")
                    current_type = None
                    continue
            # close item block
            elif line.startswith('}') and indent_level == 2:
                indent_level -= 1
                block = None
                

            elif block == "fixing" and indent_level == 2:
                get_fixing_properties(line, data, current_module, current_type)
                
    return data


# defines the files to be parsed - will parse every txt file in the "SCRIPTS_DIR"
def parse_files_in_folder():
    parsed_fixing_data = {}
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                parsed_fixing_data = parse_file(file_path, parsed_fixing_data, "fixing")
            
    return parsed_fixing_data


# initialise parser
def init(suppress=False):
    global parsed_fixing_data

    cache_file = os.path.join(DATA_PATH, CACHE_JSON)
    # Try to get cache from json file
    parsed_fixing_data, cache_version = utility.load_cache(cache_file, get_version=True, suppress=suppress)

    # Parse items if there is no cache, or it's outdated.
    if cache_version != version.get_version():
        parsed_fixing_data = parse_files_in_folder()
        utility.save_cache(parsed_fixing_data, CACHE_JSON)

    if not suppress:
        fixing_counter = 0
        for module, fixing_data in parsed_fixing_data.items():
            fixing_counter += len(fixing_data)
    
        print("Number of fixings found:", fixing_counter)

    
if __name__ == "__main__":
    init()
