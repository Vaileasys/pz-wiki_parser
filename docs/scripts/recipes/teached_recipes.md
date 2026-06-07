[Previous Folder](../parser/creation_method_parser.md) | [Previous File](researchrecipes.md) | [Next Folder](../tiles/entity_article.md) | [Back to Index](../../index.md)

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

### [`main(batch: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/teached_recipes.py#L29)

Main execution function for taught recipes generation.

<ins>**Args:**</ins>
  - **batch (bool)**:
      - _If True, skip language initialization_
  - **This function**:
  - **1. Loads parsed item data**:
  - **2. Identifies items that teach recipes**:
  - **3. Generates wiki markup for each teaching item**:
  - **4. Creates files organized by individual IDs and by wiki pages**:
  - **5. Includes proper bot flags for wiki integration**:
  - **6. Expands meta recipes into their component recipes**:
  - **The output is saved in multiple locations**:
  - **- output/recipes/teachedrecipes/id/ (individual item files)**:
  - **- output/recipes/teachedrecipes/page/ (page-combined files)**:


[Previous Folder](../parser/creation_method_parser.md) | [Previous File](researchrecipes.md) | [Next Folder](../tiles/entity_article.md) | [Back to Index](../../index.md)
