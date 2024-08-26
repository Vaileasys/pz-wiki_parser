import csv
import script_parser
import re
import os

def main():
    script_parser.init()

    input_file_path = 'output/logging/parsed_item_data.txt'
    output_file_path = 'output/evolved_recipe_values.csv'

    # Check if the input file exists
    if not os.path.exists(input_file_path):
        print(f"Error: The file {input_file_path} does not exist.")
        return

    try:
        # Remove comments from the file content
        with open(input_file_path, 'r') as file:
            content = file.read()
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'//.*', '', content)

        lines = content.splitlines()
        items_dict = {}
        current_item_name = None
        current_food_type = None

        # Process each line
        for line in lines:
            line = line.strip()

            # Check if the line defines a new item
            if line.startswith('item'):
                current_item_name = line.split()[1]
                items_dict[current_item_name] = {'FoodType': None}

            # Check if the line contains a FoodType and not EvolvedRecipeName
            if line.startswith('FoodType =') and current_item_name:
                current_food_type = extract_food_type(line)
                items_dict[current_item_name]['FoodType'] = current_food_type

            # Check if the line contains an EvolvedRecipe and not EvolvedRecipeName
            if line.startswith('EvolvedRecipe =') and current_item_name:
                evolved_recipe_values = extract_evolved_recipe_values(line)

                # Populate the dictionary only if evolved recipes exist
                if evolved_recipe_values:
                    items_dict[current_item_name].update(evolved_recipe_values)

        # Filter out items without any evolved recipes
        items_dict = {k: v for k, v in items_dict.items() if len(v) > 1}

        # Extract all unique recipe names and sort them alphabetically
        all_recipe_names = sorted({recipe for values in items_dict.values() for recipe in values.keys() if recipe != 'FoodType'})

        # Write the results to the CSV file
        with open(output_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            header_row = ['Name', 'FoodType'] + all_recipe_names
            csvwriter.writerow(header_row)

            for item_name, recipes in items_dict.items():
                row = [item_name, recipes.get('FoodType', '')] + [recipes.get(recipe, '') for recipe in all_recipe_names]
                csvwriter.writerow(row)

        print("\nSuccessfully extracted evolved recipe values and food types.")

    except Exception as e:
        print(f"An error occurred: {e}")

def extract_food_type(line):
    return line.split('=', 1)[1].strip()

def extract_evolved_recipe_values(line):
    evolved_recipes = line.split('=', 1)[1].strip()
    recipe_values = {}
    matches = re.findall(r"'([^']+):([^']+)'", evolved_recipes)

    for recipe, value in matches:
        recipe_values[recipe.strip()] = value.strip()

    return recipe_values

if __name__ == '__main__':
    main()
