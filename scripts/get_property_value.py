from scripts.parser import item_parser


# Gets the value of a property for a specific item
def get_property_value(query_item_id, property_name):
    for item_id, item_data in item_parser.get_item_data().items():
        if query_item_id == item_id:
            if property_name in item_data:
                property_value = item_data.get(property_name)
                print(f"{query_item_id} {property_name} is: {property_value}")
                return property_value
            else:
                print(f"Property '{property_name}' not found")
                return None
    return None


# Takes user input 
def main():
    found = False

    # Enter item id and compares with parsed data
    while not found:
        parsed_item_data = item_parser.get_item_data()
        user_input = input("Enter the item ID (Q to quit): \n> ")
        if user_input.lower() == 'q':
            return
        query_item = user_input.split('.')
        # Item ID
        if len(query_item) == 2:
            item_id = user_input
            if user_input in parsed_item_data:
                found = True
        # Item name only, not the module
        elif len(query_item) == 1:
            item_name = query_item[0]
            for key in parsed_item_data:
                if key.split('.')[1] == item_name:
                    item_id = key
                    found = True
                    break
        if found is False:
            print(f"\nNo type found for '{user_input}'")
    
    # Enter property name
    while True:
        property_name = input("Enter the property (Q to quit): \n> ")
        if property_name.lower() == 'q':
            return
        get_property_value(item_id, property_name)


if __name__ == "__main__":
    main()
