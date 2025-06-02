[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](craft_recipes.md) | [Next File](legacy_recipe_format.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)

# evolvedrecipe.py

Project Zomboid Wiki Evolved Recipes Generator

This script processes items in Project Zomboid that are part of evolved recipes
(recipes that can change or improve over time, like food combinations). It generates
wiki markup using the EvolvedRecipesForItem template to document these recipes.

The script handles:
- Parsing item data for evolved recipe properties
- Processing spice attributes for recipes
- Formatting recipe combinations and variations
- Generating MediaWiki template markup
- Special handling for cooked food variants

## Functions

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/evolvedrecipe.py#L22)

Main execution function for evolved recipes generation.

This function:
1. Loads parsed item data
2. Identifies items with evolved recipe properties
3. Processes special attributes like spices
4. Formats recipe data for wiki template
5. Creates output files with proper template markup
The output is saved in the 'output/evolved_recipes' directory,
with one file per item that has evolved recipe properties.
Special handling is included for:
- Spice attributes
- List-type recipe values
- Cooked food variants



[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](craft_recipes.md) | [Next File](legacy_recipe_format.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
