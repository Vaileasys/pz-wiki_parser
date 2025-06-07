import re, os
from scripts.core.constants import DATA_DIR
from scripts.core.cache import save_cache
from scripts.utils import echo

def split_arguments(arguments_string):
    argument_list = []
    current_argument = ''
    nesting_level = 0
    current_index = 0

    while current_index < len(arguments_string):
        current_character = arguments_string[current_index]
        if current_character == '{':
            nesting_level += 1
            current_argument += current_character
        elif current_character == '}':
            nesting_level -= 1
            current_argument += current_character
        elif current_character == ',' and nesting_level == 0:
            argument_list.append(current_argument.strip())
            current_argument = ''
        else:
            current_argument += current_character
        current_index += 1

    if current_argument.strip():
        argument_list.append(current_argument.strip())

    return argument_list

def parse_argument(argument_string):
    stripped_argument = argument_string.strip()

    # String literal
    if stripped_argument.startswith('"') and stripped_argument.endswith('"'):
        return stripped_argument[1:-1]

    # Nested table
    if stripped_argument.startswith('{') and stripped_argument.endswith('}'):
        inner_content = stripped_argument[1:-1].strip()
        sub_argument_strings = split_arguments(inner_content)
        return [parse_argument(sub_argument) for sub_argument in sub_argument_strings]

    if stripped_argument == 'true':
        return True
    if stripped_argument == 'false':
        return False

    # Fallback
    try:
        if '.' in stripped_argument:
            return float(stripped_argument)
        return int(stripped_argument)
    except ValueError:
        return stripped_argument

def main():
    lua_file_path = os.path.join('resources', 'lua', 'ISMoveableDefinitions.lua')

    filtered_lines = []
    with open(lua_file_path, 'r', encoding='utf-8') as file_handle:
        for raw_line in file_handle:
            stripped_line = raw_line.strip()
            if not stripped_line or stripped_line.startswith('--'):
                continue
            filtered_lines.append(stripped_line)

    function_names = [
        'addToolDefinition',
        'addMaterialDefinition',
        'addScrapDefinition',
        'addScrapItem'
    ]
    patterns_by_function = {
        function_name: re.compile(rf'moveableDefinitions\.{function_name}\s*\(')
        for function_name in function_names
    }

    tool_definitions = {}
    material_definitions = {}
    scrap_definitions = {}
    scrap_items_list = []

    parameter_name_map = {
        'addToolDefinition': [
            'name', '_items', 'perk',
            'baseActionTime', 'sound', 'isWav'
        ],
        'addMaterialDefinition': [
            'material', 'returnItem',
            'maxAmount', 'chancePerRoll'
        ],
        'addScrapDefinition': [
            'material', 'tools', 'tools2', 'perk',
            'baseActionTime', 'sound', 'isWav',
            'baseChance', 'unusableItem'
        ],
        'addScrapItem': [
            'material', 'returnItem',
            'maxAmount', 'chancePerRoll', 'isStaticSize'
        ]
    }

    line_index = 0
    while line_index < len(filtered_lines):
        current_line = filtered_lines[line_index]
        match_found = False

        for function_name, regex_pattern in patterns_by_function.items():
            if regex_pattern.search(current_line):
                block_lines = [current_line]
                parenthesis_balance = current_line.count('(') - current_line.count(')')
                line_index += 1

                while parenthesis_balance > 0 and line_index < len(filtered_lines):
                    next_line = filtered_lines[line_index]
                    block_lines.append(next_line)
                    parenthesis_balance += next_line.count('(') - next_line.count(')')
                    line_index += 1

                full_call_string = ' '.join(block_lines)
                arguments_text = re.sub(rf'.*{function_name}\s*\(', '', full_call_string).rsplit(')', 1)[0]
                raw_argument_list = split_arguments(arguments_text)
                parsed_arguments = [parse_argument(argument_string) for argument_string in raw_argument_list]
                parameter_names = parameter_name_map[function_name]
                argument_dictionary = dict(zip(parameter_names, parsed_arguments))

                if function_name == 'addToolDefinition':
                    tool_definitions[argument_dictionary['name']] = argument_dictionary

                elif function_name == 'addMaterialDefinition':
                    material_name = argument_dictionary['material']
                    material_definitions.setdefault(material_name, []).append({
                        'returnItem':    argument_dictionary['returnItem'],
                        'maxAmount':     argument_dictionary['maxAmount'],
                        'chancePerRoll': argument_dictionary['chancePerRoll']
                    })

                elif function_name == 'addScrapDefinition':
                    scrap_definitions[argument_dictionary['material']] = argument_dictionary

                elif function_name == 'addScrapItem':
                    scrap_items_list.append(argument_dictionary)

                match_found = True
                break

        if not match_found:
            line_index += 1

    consolidated_definitions = {
        'tool_definitions':     tool_definitions,
        'material_definitions': material_definitions,
        'scrap_definitions':    scrap_definitions,
        'scrap_items':          scrap_items_list
    }

    save_cache(consolidated_definitions, 'movable_definitions.json', DATA_DIR)
    echo.success("Movable definitions parsed and cached successfully.")

if __name__ == '__main__':
    main()
