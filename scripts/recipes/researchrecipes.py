import os
from tqdm import tqdm
from scripts.parser import item_parser


def main():
    parsed_item_data = item_parser.get_item_data()

    research_dir = os.path.join("output", "recipes", "researchrecipes")
    crafting_dir = os.path.join("output", "recipes", "crafting")
    os.makedirs(research_dir, exist_ok=True)
    os.makedirs(crafting_dir, exist_ok=True)

    for item_id, item_data in tqdm(parsed_item_data.items(), desc="Processing Items"):
        researchable_recipes = item_data.get("ResearchableRecipes")
        if not researchable_recipes:
            continue

        # Ensure researchable_recipes is always a list.
        if not isinstance(researchable_recipes, list):
            researchable_recipes = [researchable_recipes]

        lines = [
            "===Researchable recipes===",
            "The following recipes can be learned by researching this item:",
            "",
            f"{{{{Crafting/sandbox|id={item_id}_research"
        ]
        for recipe in researchable_recipes:
            lines.append(f"|{recipe}")
        lines.append("}}")

        output_content = "\n".join(lines)

        research_file_path = os.path.join(research_dir, f"{item_id}_research.txt")
        crafting_file_path = os.path.join(crafting_dir, f"{item_id}_research.txt")

        try:
            with open(research_file_path, "w") as f:
                f.write(output_content)
            with open(crafting_file_path, "w") as f:
                f.write(output_content)
        except Exception as e:
            tqdm.write(f"Error writing file for {item_id}: {e}")


if __name__ == '__main__':
    main()
