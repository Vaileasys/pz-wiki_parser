from scripts.parser import item_parser


def property_list(property_name):
    sorted_properties = {}

    parsed_items = item_parser.get_item_data()
    for item_id, item_data in parsed_items.items():
        if property_name in item_data:
            property_value = item_data[property_name]
            display_category = item_data.get('DisplayCategory', 'Other')
            if display_category not in sorted_properties:
                sorted_properties[display_category] = []
            if isinstance(property_value, list):
                for value in property_value:
                    sorted_properties[display_category].append(value)
            else:
                sorted_properties[display_category].append(property_value)

    return sorted_properties


def save_property_list_to_file(sorted_properties, output_file):
    with open(output_file, 'w') as file:
        for display_category, values in sorted(sorted_properties.items()):
            file.write(f"=== {display_category} ===\n")
            for value in values:
                file.write(f"{value}\n")
            file.write("\n")


def main():
    while True:
        property_name = input("Enter a property or Q to quit:\n> ").strip()

        if property_name.lower() == 'q':
            return

        sorted_properties = property_list(property_name)
        if sorted_properties:
            break
        print(f"No property found for '{property_name}'")

    output_file = 'output/property_list.txt'
    save_property_list_to_file(sorted_properties, output_file)
    print(f"Property values for '{property_name}' organized by 'DisplayCategory' saved to {output_file}")


if __name__ == "__main__":
    main()
