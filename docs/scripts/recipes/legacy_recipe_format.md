[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](evolvedrecipe.md) | [Next File](legacy_recipe_output.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)

# legacy_recipe_format.py

Project Zomboid Wiki Legacy Recipe Formatter

This script processes raw recipe data into a structured format suitable for wiki
documentation. It handles the complex task of formatting various recipe components,
including inputs, outputs, requirements, and special cases like construction recipes.

The script handles:
- Recipe name translation and formatting
- Input processing (tools, ingredients, energy)
- Output processing with mappers
- Requirement formatting (skills, books, traits)
- Construction recipe special cases
- XP and workstation information

## Functions

### [`get_processed_recipes()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L33)

_Get the processed recipe data, initializing if empty._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary of processed recipe data.
      - This function serves as the main interface to access processed recipe data,
      - ensuring the data is loaded before being accessed.

### [`process_recipe(recipe, parsed_item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L49)

_Process a recipe into a structured format._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Raw recipe data._
  - **parsed_item_data (dict)**:
      - _Parsed item data for reference._

<ins>**Returns:**</ins>
  - **dict:**
      - Processed recipe data including:
        - name: Recipe name and translation
        - inputs: Tools and ingredients
        - outputs: Products and results
        - requirements: Skills, books, and traits
        - workstation: Required crafting location
        - xp: Experience gains
        - construction: Construction recipe flag
        - category: Recipe category
      - Handles validation and proper formatting of all recipe components.

### [`process_name(recipe)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L91)

_Process recipe name and get its translation._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing name field._

<ins>**Returns:**</ins>
  - **tuple:**
      - (raw_name, translated_name) where:
        - raw_name: Original recipe name
        - translated_name: Translated version of the name
      - Returns (None, None) if name is invalid.

### [`process_inputs(recipe)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L114)

_Process recipe inputs into structured format._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing inputs field._

<ins>**Returns:**</ins>
  - **dict:**
      - Processed inputs containing:
        - tools: Required tools with properties
        - ingredients: Required ingredients with amounts
        - energy: Energy requirements if any

<ins>**Handles:**</ins>
  - Tool requirements and flags
  - Ingredient amounts and types
  - Fluid ingredients
  - Energy inputs
  - Numbered list inputs

### [`construction_output(outputs, recipe)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L331)

_Process construction recipe outputs._

<ins>**Args:**</ins>
  - **outputs (list)**:
      - _List of output items._
  - **recipe (dict)**:
      - _Full recipe data._

<ins>**Returns:**</ins>
  - **list:**
      - Processed construction outputs with:
        - Sprite information
        - Icon details
        - Item properties

### [`process_outputs(recipe)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L397)

_Process recipe outputs into structured format._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing outputs._

<ins>**Returns:**</ins>
  - **dict:**
      - Processed outputs containing:
        - Standard outputs with amounts
        - Construction outputs if applicable
        - Mapper-based outputs
        - Fluid outputs

### [`process_output_mapper(recipe, mapper_string)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L473)

_Process output mapper strings into structured format._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data._
  - **mapper_string (str)**:
      - _Mapper string to process._

<ins>**Returns:**</ins>
  - **dict:**
      - Processed mapper data with:
        - Mapped items
        - Item properties
        - Amounts

### [`process_requirements(recipe, parsed_item_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L526)

_Process recipe requirements into structured format._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data._
  - **parsed_item_data (dict)**:
      - _Reference item data._

<ins>**Returns:**</ins>
  - **dict:**
      - Processed requirements including:
        - Required skills and levels
        - Required books or literature
        - Required traits
        - Auto-learn conditions
        - Schematic requirements

### [`process_workstation(recipe)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L642)

_Process workstation requirements._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted workstation requirement,
      - or empty string if no workstation needed.

### [`process_xp(recipe)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L706)

_Process experience gain information._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted XP gain information,
      - or "0" if no XP is gained.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_format.py#L741)

_Main execution function for recipe formatting._



[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](evolvedrecipe.md) | [Next File](legacy_recipe_output.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
