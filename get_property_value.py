import script_parser

# gets the value of a property for a specific item
def get_property_value(data, item_type, property_name=None):
    for module, module_data in data.items():
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
    # user defines an item and property then runs the get_property_value function
    while True:
        item_type = input("Enter the type: \n> ")
        if any(item_type in module_data for module_data in script_parser.main().values()):
            break
        print(f"No type found for {item_type}")
    property_name = input("Enter the property: \n> ")
    get_property_value(script_parser.main(), item_type, property_name)


if __name__ == "__main__":
    main()