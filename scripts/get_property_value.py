import script_parser


# gets the value of a property for a specific item
def get_property_value(item_type, property_name=None):
    for module, module_data in script_parser.parsed_item_data.items():
        if item_type in module_data:
            block = module_data[item_type]
            if property_name and property_name in block:
                property_value = block.get(property_name)
                print(f"'{property_name}' value found for '{module}.{item_type}':", property_value)
                return property_value
            else:
                print("Property not found")
                return None
    return None


def main():
    script_parser.init()
    # user defines an item and property then runs the get_property_value function
    while True:
        item_type = input("Enter the type or Q to quit: \n> ")
        if item_type.lower() == 'q':
            return
        if any(item_type in module_data for module_data in script_parser.parsed_item_data.values()):
            break
        print(f"No type found for {item_type}")

    while True:
        property_name = input("Enter the property or Q to quit: \n> ")
        if property_name.lower() == 'q':
            return
        get_property_value(item_type, property_name)


if __name__ == "__main__":
    main()
