import csv
from scripts.parser import item_parser


def main():
    output_file_path = 'output/evolved_recipe_values.csv'
    parsed_item_data = item_parser.get_item_data()
    # Store only unique 'EvolvedRecipe' values
    evolved_recipes = set()

    try:
        # Iterate through each item getting all unique 'EvolvedRecipe' values
        for item_id, item_data in parsed_item_data.items():
            property_data = item_data.get("EvolvedRecipe")
            if property_data:
                evolved_recipes.update(property_data.keys())
    
        # Sort alphabetically then add 'Name' and 'FoodType' columns
        evolved_recipes = sorted(evolved_recipes)
        evolved_recipes = ['Name'] + ['FoodType'] + evolved_recipes
        
    except Exception as e:
        print(f"An error occurred when getting the heading: {e}")

    try:
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(list(evolved_recipes))

            # Iterate through each item getting the 'EvolvedRecipe' and 'FoodType'
            for item_id, item_data in parsed_item_data.items():
                evolved_recipe = item_data.get('EvolvedRecipe', None)
                food_type = item_data.get('FoodType', 'NoExplicit')
                
                # Don't include item if it doesn't have an evolved_recipe
                if evolved_recipe is None:
                    continue
                
                # Get item_name from the item_id [compatibility]
                item_name = item_id.split('.')[1]
                row = [item_name] + [food_type]

                # Append the item's evolved_recipes to the row in the correct column
                for key in evolved_recipes[2:]:
                    value = evolved_recipe.get(key, None)
                    # Convert attributes (e.g. 'Cooked') back to scripts format [compatibility]
                    if isinstance(value, list):
                        value = '|'.join(value)
                    row.append(value if value is not None else '')
                
                writer.writerow(row)
                print("\nSuccessfully extracted evolved recipe values and food types.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()