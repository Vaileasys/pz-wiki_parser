import re
import os
from scripts.utils import utility

RESOURCE_PATH = "resources/scripts/"
DATA_FILE = "fluid_data.json"

fluid_counter = 0
parsed_data = {}


# Get the fluid data
def get_fluid_data():
    global parsed_data
    if parsed_data == {}:
        init()
    return parsed_data


# Converts a string to a boolean
def convert_boolean(value):
    value = str(value).lower()
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else: 
        return value


# Gets key-value pairs separated by '='
def get_key_values(block_content):
    result = {}
    for line in block_content.splitlines():
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue

        # Match 'key = value'
        match = re.match(r"(\w+)\s*=\s*(.+)", line)
        if match:
            key, value = match.groups()
            value = value.rstrip(',').strip()

            # Value is a list of values separated by ':'
            if ':' in value:
                values = [v.strip() for v in value.split(':')]
                processed_values = []
                for v in values:
                    # Convert to int or float
                    try:
                        if '.' in v:
                            v_converted = float(value)
                        else:
                            value_converted = int(value)
                        processed_values.append(v_converted)
                    except ValueError:
                        processed_values.append(v.strip('"').strip("'"))
                result[key] = processed_values
            
            # Generic value
            else:
                # Convert to int or float
                try:
                    if '.' in value:
                        value_converted = float(value)
                    else:
                        value_converted = int(value)
                    result[key] = value_converted
                except ValueError:
                    result[key] = value.strip('"').strip("'")

    return result


# Find the content for a specified block
def get_block_content(content, block_name):
    # Find the index where 'block_name {' begins
    match = re.search(fr"{re.escape(block_name)}\s*\{{", content)
    if not match:
        return None

    start_idx = match.end()
    brace_count = 1
    i = start_idx

    # Step through each block until the matching closing brace is found
    while i < len(content) and brace_count > 0:
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
        i += 1
    
    return content[start_idx : i-1]


# Parse all fluid blocks
def parse_fluid_file(filepath):
    global fluid_counter
    fluids_data = {}

    with open(filepath, 'r') as file:
        content = file.read()

    fluid_pattern = re.compile(r"fluid\s+(\w+)\s*\{")
    fluid_blocks = []

    # Find all fluid blocks
    for match in fluid_pattern.finditer(content):
        fluid_id = match.group(1)
        fluid_content = get_block_content(content, f"fluid {fluid_id}")
        if fluid_content is not None:
            fluid_blocks.append((fluid_id, fluid_content))
        
    # Define each sub-block so they don't get included in the fluid (top-level) block
    sub_blocks = ['Categories', 'Properties', 'Poison', 'BlendWhiteList', 'BlendBlackList']

    # Parse each fluid block
    for fluid_id, fluid_content in fluid_blocks:
        fluid_counter += 1
        fluid_dict = {}

        # Remove sub-blocks from fluid_content
        sub_block_contents = {}
        fluid_main_content = fluid_content

        for sub_block in sub_blocks:
            sub_content = get_block_content(fluid_content, sub_block)
            if sub_content:
                sub_block_contents[sub_block] = sub_content
                sub_block_pattern = re.compile(fr"{re.escape(sub_block)}\s*\{{.*?\}}", re.DOTALL)
                fluid_main_content = sub_block_pattern.sub('', fluid_main_content, count=1)

        # Parse top-level key-value pairs
        top_level_kv = get_key_values(fluid_main_content)
        fluid_dict.update(top_level_kv)

        # Parse each sub-block
        if 'Categories' in sub_block_contents:
            categories_content = sub_block_contents['Categories']
            categories = re.findall(r"\w+", categories_content)
            fluid_dict['Categories'] = categories

        if 'Properties' in sub_block_contents:
            properties_content = sub_block_contents['Properties']
            properties = get_key_values(properties_content)
            fluid_dict['Properties'] = properties

        if 'Poison' in sub_block_contents:
            poison_content = sub_block_contents['Poison']
            poison = get_key_values(poison_content)
            fluid_dict['Poison'] = poison

        if 'BlendWhiteList' in sub_block_contents:
            blend_white_content = sub_block_contents['BlendWhiteList']
            blend_white_data = get_key_values(blend_white_content)

            # Parse 'categories' block
            blend_white_categories_content = get_block_content(blend_white_content, 'categories')
            if blend_white_categories_content:
                categories = re.findall(r"\w+", blend_white_categories_content)
                blend_white_data['categories'] = categories

            # Convert 'whitelist' to a boolean
            if 'whitelist' in blend_white_data:
                whitelist = convert_boolean(blend_white_data['whitelist'])
                blend_white_data['whitelist'] = whitelist

            fluid_dict['BlendWhiteList'] = blend_white_data

        if 'BlendBlackList' in sub_block_contents:
            blend_black_content = sub_block_contents['BlendBlackList']
            blend_black_data = get_key_values(blend_black_content)

            # Parse 'categories' block
            blend_black_categories_content = get_block_content(blend_black_content, 'categories')
            if blend_black_categories_content:
                categories = re.findall(r"\w+", blend_black_categories_content)
                blend_black_data['categories'] = categories

            # Convert 'blacklist' to a boolean
            if 'blacklist' in blend_black_data:
                blacklist = convert_boolean(blend_black_data['blacklist'])
                blend_black_data['blacklist'] = blacklist

            fluid_dict['BlendBlackList'] = blend_black_data

        fluids_data[fluid_id] = fluid_dict

    return fluids_data


# Parse all fluid files
def parse_files(directory):
    global parsed_data

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                fluids_data = parse_fluid_file(filepath)
                parsed_data.update(fluids_data)

    return parsed_data


# Initialise parser
def init():
    global fluid_counter

    fluid_data = parse_files(RESOURCE_PATH)
    utility.save_cache(fluid_data, DATA_FILE)
    print(f"Total number of fluids parsed: {fluid_counter}")

    
if __name__ == "__main__":
    init()