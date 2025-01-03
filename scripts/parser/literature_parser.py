# Parses literature lua files

import os
import re
import json

LUA_DIRECTORY = "resources/lua/"
JSON_FILE_PATH = "output/logging/parsed_literature_data.json"

FILES_LIST = [
    'SpecialItemData_Books.lua',
    'SpecialItemData_Comics.lua',
    'SpecialItemData_Magazines.lua',
    'SpecialItemData_Misc.lua',
    'SpecialItemData_Photos.lua'
]

parsed_data = {}


def get_item_data():
    global parsed_data
    if parsed_data == {}:
        init()
    return parsed_data


# Handles nested dictionaries, creating new ones, or converting list values to a dict.
def add_to_nested_dict(data, keys, values):
    """Adds values to a nested dictionary structure based on a list of keys.

    Args:
        data (dict): The dictionary where the values will be added.
        keys (list or str): List of keys representing the hierarchical path. E.g. ['Level1', 'Level2', 'Level3']
        values (list or str): List of values to be added to the nested dictionary.
    """
    current = data
    # Traverse all keys except the last, as this is where we will store the list of values
    for key in keys[:-1]:

        # Create the dictionary
        if key not in current:
            current[key] = {}
        
        # Convert list to dictionary if deeper nesting is needed
        elif isinstance(current[key], list):
            current[key] = {f"default_{i}": item for i, item in enumerate(current[key])}
        
        elif not isinstance(current[key], dict):
            raise TypeError(f"Expected a dictionary or list at {key}, but found {type(current[key]).__name__}")
        
        current = current[key]
    
    # Add the last key to the dictionary, if it doesn't already exist
    if keys[-1] not in current:
        current[keys[-1]] = list(set(values))

    # Append unique values if it's a list
    elif isinstance(current[keys[-1]], list):
        current[keys[-1]].extend(value for value in values if value not in current[keys[-1]])

    elif isinstance(current[keys[-1]], dict):
        raise TypeError(f"Cannot add list values to an existing dictionary at {keys[-1]}")
    else:
        raise TypeError(f"Unexpected type at {keys[-1]}: {type(current[keys[-1]]).__name__}")


# Parses a lua file extracting lists starting with 'SpecialLootSpawns'
def parse_lua_file(file_path):
    data = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        # Match nested structures like SpecialLootSpawns.<key1>.<key2>.<key3> = { "value1", "value2", ... }
        pattern = re.compile(r"SpecialLootSpawns\.([\w\.]+)\s*=\s*{([^}]*)}")
        
        for match in pattern.finditer(content):
            nested_keys = match.group(1).split('.') # Get the nested keys by splitting
            list_content = match.group(2)
            
            # Extract strings within quotes and ignore comments
            items = re.findall(r'"(.*?)"', list_content)
            add_to_nested_dict(data, nested_keys, items)
    
    return data


# Parses all files and combines them into a single dictionary
def parse_files(file_list):
    combined_results = {}
    
    for file_path in file_list:
        file_results = parse_lua_file(file_path)
        
        # Merge results into a combined dictionary
        for key, value in file_results.items():
            if key not in combined_results:
                combined_results[key] = value
            else:
                # Combine lists if key already exists
                combined_results[key].update(value)
    
    return combined_results


# Saves parsed data to a json file, for debugging
def save_to_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"Parsed data saved to '{output_file}'")


def init():
    global parsed_data

    file_paths = [os.path.join(LUA_DIRECTORY, file_name) for file_name in FILES_LIST]

    parsed_data = parse_files(file_paths)

    total_values = sum(
        len(values) if isinstance(values, list) else sum(len(v) for v in values.values()) for values in parsed_data.values()
    )
    print(f"Total number of values found: {total_values}")

    save_to_json(parsed_data, JSON_FILE_PATH)


if __name__ == "__main__":
    init()