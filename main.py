import importlib

print("Which script do you want to run?")

# list of available commands
help_info = {
    '1': "item_list: return all items in a list organised by DisplayCategory",
    '2': "weapon_list: return all weapons in a list with stats organised by their skill",
    '3': "property_list: return all values of a specific property",
    '4': "get_property_value: returns the value of a property for a specific item",
    '5': "sort_by_property: sort all parsed data and organise for a user defined property",
}

while True:
    # print a list of available commands
    for command, description in help_info.items():
        print(f"'{command}' - {description}")

    user_input = input("> ")

    if user_input == "exit":
        break

    scripts = {
        '1': 'item_list',
        '2': 'weapon_list',
        '3': 'property_list',
        '4': 'get_property_value',
        '5': 'sort_by_property',
    }

    module_name = scripts.get(user_input)

    if module_name:
        try:
            module = importlib.import_module(module_name)
            module.main()
        except ImportError as e:
            print(f"Error importing module {module_name}: {e}")
        break
    else:
        print("Invalid input. Please type a valid command.")
