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
literature_refs = {}


def get_literature_data():
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


# Parses special cases as a dictionary (BookDetails, ComicBookDetails, MagazineDetails)
def parse_special_details(content):
    # For Both: "key = { ... }" and "["..."] = { ... }"
    pattern = re.compile(r'(?:\["(.*?)"\]|(\w+))\s*=\s*{([^}]*)}')
    results = {}

    for match in pattern.finditer(content):
        key = match.group(1) if match.group(1) else match.group(2) # Extract key
        details_content = match.group(3)  # Extract { ... }

        # Extract properties from the content (e.g., issues, cover, firstYear)
        details = {}
        for detail_match in re.finditer(r'(\w+)\s*=\s*(.+?)(?:,|$)', details_content):
            detail_key = detail_match.group(1)
            detail_value = detail_match.group(2).strip()
            
            # Handle types for detail values
            if detail_value.isdigit():  # Convert numeric values
                details[detail_key] = int(detail_value)
            elif detail_value.lower() in ['true', 'false']:  # Convert boolean values
                details[detail_key] = detail_value.lower() == 'true'
            else:  # Treat as string
                details[detail_key] = detail_value.strip('"')
        
        # Add to results
        results[key] = details

    return results


# Extracts content nested in { ... }
def extract_nested_content(content, start_index):
    stack = []
    nested_content = []
    for i in range(start_index, len(content)):
        char = content[i]
        if char == '{':
            stack.append(char)
        elif char == '}':
            stack.pop()
            # We've closed the top-level brace
            if not stack:
                return ''.join(nested_content)
        nested_content.append(char)
    raise ValueError("Unmatched braces in the Lua file.")


# Helper to parse dictionary-like structures in Lua
def parse_lua_dict(content):
    # key = { cover = "value", ... }
    pattern = re.compile(r'(\w+|".*?")\s*=\s*{([^}]*)}')
    results = {}

    for match in pattern.finditer(content):
        key = match.group(1).strip('"')  # Extract key
        details_content = match.group(2)   # Extract inner dictionary content
        
        # Extract the 'cover' value within the dictionary content
        cover_match = re.search(r'\bcover\s*=\s*"(.*?)"', details_content)
        if cover_match:
            cover_type = cover_match.group(1)
            if cover_type not in results:
                results[cover_type] = []  # Initialize list for this cover type
            results[cover_type].append(key)  # Add the book title to the cover type list
    
    return results


# Parses a lua file extracting lists starting with 'SpecialLootSpawns'
def parse_lua_file(file_path):
    data = {}
    special_cases = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # SpecialLootSpawns.<key1>.<key2> = { ... }
    pattern = re.compile(r"SpecialLootSpawns\.([\w\.]+)\s*=\s*{")
    matches = list(pattern.finditer(content))

    # Extracts keys and content
    for match in matches:
        nested_keys = match.group(1).split('.')
        start_index = match.end() - 1
        nested_content = extract_nested_content(content, start_index)

        # Handle special cases
        if nested_keys[-1] in ['BookDetails', 'ComicBookDetails', 'MagazineDetails']:
            special_cases[nested_keys[-1]] = parse_special_details(nested_content)
        else:
            # General case for lists
            items = re.findall(r'"(.*?)"', nested_content)
            add_to_nested_dict(data, nested_keys, items)

    return data, special_cases


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


# Combines general parsed lists and the special case dictionaries
def combine_parsed_data(data_list, special_cases_list):
    combined_data = {}

    # Merge list data
    for data in data_list:
        for key, value in data.items():
            if key not in combined_data:
                combined_data[key] = value
            else:
                # Merge lists
                if isinstance(combined_data[key], list):
                    combined_data[key].extend(item for item in value if item not in combined_data[key])
                # Merge dictionaries
                elif isinstance(combined_data[key], dict):
                    combined_data[key].update(value)

    # Merge special cases
    for special_cases in special_cases_list:
        for key, value in special_cases.items():
            if key not in combined_data:
                combined_data[key] = value
            else:
                # Merge dictionaries
                if isinstance(combined_data[key], dict):
                    combined_data[key].update(value)
                else:
                    raise TypeError(f"Conflict at {key}: Cannot merge non-dictionary with dictionary.")

    return combined_data


# Saves parsed data to a json file, for debugging
def save_to_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"Parsed data saved to '{output_file}'")


def init():
    global parsed_data

    file_paths = [os.path.join(LUA_DIRECTORY, file_name) for file_name in FILES_LIST]

    # Parse all files
    data_list = []
    special_cases_list = []
    for file_path in file_paths:
        file_data, special_cases = parse_lua_file(file_path)
        data_list.append(file_data)
        special_cases_list.append(special_cases)

    # Combine the results
    parsed_data = combine_parsed_data(data_list, special_cases_list)

    save_to_json(parsed_data, JSON_FILE_PATH)


if __name__ == "__main__":
    init()