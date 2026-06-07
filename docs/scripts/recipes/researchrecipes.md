[Previous Folder](../parser/creation_method_parser.md) | [Previous File](evolved_recipes.md) | [Next File](teached_recipes.md) | [Next Folder](../tiles/entity_article.md) | [Back to Index](../../index.md)

# researchrecipes.py

Project Zomboid Wiki Research Recipes Generator

This script processes items in Project Zomboid that can be researched to learn new
recipes. It generates wiki markup showing which recipes can be learned by researching
each item, using the Crafting/sandbox template for proper formatting.

The script handles:
- Parsing item data for researchable recipes (from item's ResearchableRecipes property)
- Finding recipes where the item is a product (product-based research)
- Combining all researchable recipes into a single unified list
- Generating formatted wiki markup with recipe lists
- Creating output in both research and crafting directories
- Proper template formatting for wiki integration
- Expanding meta recipes into their component recipes

## Functions

### [`find_recipes_producing_item(item_id: str) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/researchrecipes.py#L29)

Find all recipes that produce the given item as an output.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _The item ID to search for_

<ins>**Returns:**</ins>
  - **list[str]**:
      - _List of recipe IDs that produce this item_

### [`main(batch: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/researchrecipes.py#L56)

Main execution function for research recipes generation.

<ins>**Args:**</ins>
  - **batch (bool)**:
      - _If True, skip language initialization_
  - **This function**:
  - **1. Loads parsed item data**:
  - **2. Identifies items with researchable recipes (traditional and product-based)**:
  - **3. Combines all researchable recipes into a single unified list per item**:
  - **4. Generates wiki markup using Crafting/sandbox template**:
  - **5. Creates output files organized by individual IDs and by wiki pages**:
  - **6. Handles proper formatting for wiki integration**:
  - **7. Expands meta recipes into their component recipes**:
  - **The output is saved in multiple locations**:
  - **- output/recipes/researchrecipes/id/ (individual item files)**:
  - **- output/recipes/researchrecipes/page/ (page-combined files)**:
  - **- output/recipes/crafting/id/ (individual item files)**:
  - **- output/recipes/crafting/page/ (page-combined files)**:


[Previous Folder](../parser/creation_method_parser.md) | [Previous File](evolved_recipes.md) | [Next File](teached_recipes.md) | [Next Folder](../tiles/entity_article.md) | [Back to Index](../../index.md)
