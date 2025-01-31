from scripts.parser import item_parser


def sort_by_property(property):
    sorted_data = {}

    # Iterate through the parsed data and sort it based on the specified property
    for item_id, item_data in item_parser.get_item_data().items():
        if property in item_data:
            property_value = item_data.get(property)
            if isinstance(property_value, list):
                for value in property_value:
                    if value not in sorted_data:
                        print(value)
                        sorted_data[value] = []
                        sorted_data[value].append((item_id))
            else:
                if property_value not in sorted_data:
                    print(property_value)
                    sorted_data[property_value] = []
                sorted_data[property_value].append((item_id))

    # Write to output.txt
    output_file = 'output/output.txt'
    with open(output_file, 'w') as file:
        for property_value in sorted(sorted_data.keys()):
            file.write(f"<!-- ## {property_value} ## -->\n")
            for item_id in sorted_data[property_value]:
                file.write(f"{item_id}\n")
            file.write("\n")

    print(f"Output saved to {output_file}")


def main():
    # sorts by a user-defined property
    while True:
        property_name = input("Enter a property or Q to quit:\n> ")
        if property_name.lower() == 'q':
            print("Exiting...")
            break
        sort_by_property(property_name)


if __name__ == "__main__":
    main()
