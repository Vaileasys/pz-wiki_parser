[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](researchrecipes.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)

# teached_recipes.py

Project Zomboid Wiki Taught Recipes Generator

This script processes items in Project Zomboid that teach recipes (like recipe books
or VHS tapes) and generates wiki markup showing which recipes each item teaches.
It creates individual files for each item that contains recipe teaching information.

The script handles:
- Parsing item data for recipe teaching properties
- Generating formatted wiki markup with recipe links
- Creating individual files for each teaching item
- Proper bot flag markup for wiki integration
- Expanding meta recipes into their component recipes

## Functions

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/teached_recipes.py#L26)

Main execution function for taught recipes generation.

This function:
1. Loads parsed item data
2. Identifies items that teach recipes
3. Generates wiki markup for each teaching item
4. Creates individual files with recipe lists
5. Includes proper bot flags for wiki integration
6. Expands meta recipes into their component recipes
The output is saved in the 'output/recipes/teachedrecipes' directory,
with one file per teaching item.



[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](researchrecipes.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
