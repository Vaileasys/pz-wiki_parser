[Previous Folder](../objects/animal.md) | [Previous File](literature_parser.md) | [Next File](movable_definitions_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# metarecipe_parser.py

Project Zomboid Wiki Meta Recipe Parser

This script identifies and processes meta recipes from Project Zomboid's craft recipe data.
Meta recipes allow multiple recipes to be learned by just knowing one recipe name.

The script:
- Loads craft recipe data from cache
- Identifies recipes with the 'MetaRecipe' key
- Groups recipes by their meta recipe identifier
- Provides a way to expand meta recipe names to all associated recipes
- Saves the meta recipe mapping to cache for use by other scripts

## Functions

### [`get_metarecipe_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/metarecipe_parser.py#L28)

Returns the parsed meta recipe data.

<ins>**Returns:**</ins>
  - **dict**:
      - _A dictionary mapping meta recipe names to lists of recipe names._

### [`build_metarecipe_mapping(craft_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/metarecipe_parser.py#L41)

Builds a mapping of meta recipes to their associated recipes.

<ins>**Args:**</ins>
  - **craft_data (dict)**:
      - _Dictionary of craft recipes._

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary mapping meta recipe names to lists of recipe names._

### [`expand_recipe_list(recipe_list)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/metarecipe_parser.py#L67)

Expands a list of recipe names, replacing meta recipes with their associated recipes.

<ins>**Args:**</ins>
  - **recipe_list (list or str)**:
      - _A list of recipe names or a single recipe name._

<ins>**Returns:**</ins>
  - **list**:
      - _An expanded list of recipe names with meta recipes replaced by their components._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/metarecipe_parser.py#L97)

Initializes the meta recipe data.

This function:
1. Checks for existing cache
2. If needed, parses craft recipe data to extract meta recipes
3. Builds a mapping of meta recipes to their associated recipes
4. Saves the mapping to cache


[Previous Folder](../objects/animal.md) | [Previous File](literature_parser.md) | [Next File](movable_definitions_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
