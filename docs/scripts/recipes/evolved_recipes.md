[Previous Folder](../parser/creation_method_parser.md) | [Previous File](craft_recipes.md) | [Next File](researchrecipes.md) | [Next Folder](../tiles/entity_article.md) | [Back to Index](../../index.md)

# evolved_recipes.py

## Functions

### [`format_recipe_info(recipe)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/evolved_recipes.py#L14)

Format evolved recipe information in wiki article format.

<ins>**Args:**</ins>
  - **recipe (EvolvedRecipe)**:
      - _The evolved recipe object to format_

<ins>**Returns:**</ins>
  - **list**:
      - _Formatted lines for the wiki article_

### [`format_recipe_template(item, evolved_recipe)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/evolved_recipes.py#L154)

Format evolved recipe template information for an item.

<ins>**Args:**</ins>
  - **item (Item)**:
      - _The item object to format_
  - **evolved_recipe (dict)**:
      - _The evolved recipe data for the item_

<ins>**Returns:**</ins>
  - **list**:
      - _Formatted lines for the wiki template_

### [`main(batch: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/evolved_recipes.py#L179)

Main execution function for evolved recipes article generation.

<ins>**Args:**</ins>
  - **batch (bool)**:
      - _If True, skip language initialization_
  - **This function**:
  - **1. Loads all evolved recipes**:
  - **2. For each recipe with a result item**:
  - **- Formats the recipe information in wiki article format**:
  - **- Creates a file named after the result item's ID**:
  - **- Writes the formatted content to the output directory**:
  - **3. For each item with evolved recipe properties**:
  - **- Formats the recipe template information**:
  - **- Creates a file named after the item's ID**:
  - **- Writes the formatted content to the template directory**:


[Previous Folder](../parser/creation_method_parser.md) | [Previous File](craft_recipes.md) | [Next File](researchrecipes.md) | [Next Folder](../tiles/entity_article.md) | [Back to Index](../../index.md)
