[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](evolvedrecipe.md) | [Next File](teached_recipes.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)

# researchrecipes.py

Project Zomboid Wiki Research Recipes Generator

This script processes items in Project Zomboid that can be researched to learn new
recipes. It generates wiki markup showing which recipes can be learned by researching
each item, using the Crafting/sandbox template for proper formatting.

The script handles:
- Parsing item data for researchable recipes
- Generating formatted wiki markup with recipe lists
- Creating output in both research and crafting directories
- Proper template formatting for wiki integration
- Expanding meta recipes into their component recipes

## Functions

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/researchrecipes.py#L23)

Main execution function for research recipes generation.

This function:
1. Loads parsed item data
2. Identifies items with researchable recipes
3. Generates wiki markup using Crafting/sandbox template
4. Creates output files in both research and crafting directories
5. Handles proper formatting for wiki integration
6. Expands meta recipes into their component recipes
The output is saved in two locations:
- output/recipes/researchrecipes/
- output/recipes/crafting/
Each containing one file per researchable item.



[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](evolvedrecipe.md) | [Next File](teached_recipes.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
