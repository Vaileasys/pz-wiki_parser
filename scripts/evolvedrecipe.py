import os
from tqdm import tqdm
from scripts.parser import item_parser


def main():
    parsed_item_data = item_parser.get_item_data()
    output_dir = 'output/evolved_recipes'
    os.makedirs(output_dir, exist_ok=True)

    for item_id, item_data in tqdm(parsed_item_data.items(), desc="Processing Items"):
        evolved_recipe = item_data.get("EvolvedRecipe", {})
        if not evolved_recipe:
            continue
        lines = ["{{EvolvedRecipesForItem", f"|id={item_id}"]

        if item_data.get("Spice") == "TRUE":
            lines.append("|spice=true")

        for key, value in evolved_recipe.items():
            if isinstance(value, list):
                value = '|'.join(value)
            if isinstance(value, str) and value.endswith('|Cooked'):
                value = value[:-len('|Cooked')]
            lines.append(f"|{key.lower()}={value}")

        lines.append("}}")
        output_content = "\n".join(lines)

        output_file_path = os.path.join(output_dir, f"{item_id}.txt")
        try:
            with open(output_file_path, "w") as f:
                f.write(output_content)
        except Exception as e:
            tqdm.write(f"Error writing file for {item_id}: {e}")


if __name__ == '__main__':
    main()
