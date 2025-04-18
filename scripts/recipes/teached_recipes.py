import os
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.utils.utility import get_recipe

def main():
    parsed_item_data = item_parser.get_item_data()

    teached_dir = 'output/recipes/teachedrecipes'
    os.makedirs(teached_dir, exist_ok=True)

    for item_id, item_data in tqdm(parsed_item_data.items(), desc="Processing Items"):
        teached_recipes = item_data.get("TeachedRecipes")
        if not teached_recipes:
            continue

        # Ensure teached_recipes is always a list.
        if not isinstance(teached_recipes, list):
            teached_recipes = [teached_recipes]

        lines = [
            "===Learned recipes===",
            "Reading this item will teach the following crafting recipes:"
        ]

        for recipe in teached_recipes:
            recipe_link = get_recipe(recipe)
            lines.append(f"*{recipe_link}")

        output_content = "\n".join(lines)
        teached_file_path = os.path.join(teached_dir, f"{item_id}_Teached.txt")

        try:
            with open(teached_file_path, "w") as f:
                f.write(output_content)
        except Exception as e:
            tqdm.write(f"Error writing file for {item_id}: {e}")

if __name__ == '__main__':
    main()
