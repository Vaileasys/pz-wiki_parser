import script_parser

def sort_by_property(parsed_data, property):
    sorted_data = {}

    # iterate through the parsed data and sort it based on the specified property
    for module, module_data in parsed_data.items():
        for item_type, type_data in module_data.items():
            if property in type_data:
                property_value = type_data.get(property)
                key = f'{property_value}_{module}_{item_type}'
                if property_value not in sorted_data:
                    sorted_data[property_value] = []
                sorted_data[property_value].append((module, item_type))

    # write to output.txt
    output_file = 'output.txt'
    with open(output_file, 'w') as file:
        for property_value in sorted(sorted_data.keys()):
            file.write(f"<!-- ## {property_value} ## -->\n")
            for module, item_type in sorted_data[property_value]:
                file.write(f"{module}.{item_type}\n")
            file.write("\n")
    
    print(f"Output saved to {output_file}")

def main():
    # sorts by a user-defined property
    sort_by_property(script_parser.main(), input("Enter a property:\n> "))

if __name__ == "__main__":
    main()