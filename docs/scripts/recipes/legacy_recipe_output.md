[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](legacy_recipe_format.md) | [Next File](legacy_recipe_parser.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)

# legacy_recipe_output.py

Project Zomboid Wiki Legacy Recipe Output Generator

This script processes parsed recipe data and generates formatted wiki markup for
recipe pages. It handles various recipe components including ingredients, tools,
skills, and products, converting them into properly formatted wiki templates.

The script handles:
- Ingredient processing with icons and amounts
- Tool requirements with conditions and flags
- Recipe learning methods (books, traits, etc.)
- Product outputs with quantities
- XP gains and workstation requirements
- Item usage tracking and documentation
- Lua table generation for wiki templates

## Functions

### [`process_ingredients(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L30)

Process recipe ingredients and format them for wiki display.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing ingredient information._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for ingredients section.

<ins>**Handles:**</ins>
  - Tag-based ingredients with icons
  - Fluid ingredients with colors
  - Numbered list ingredients
  - Standard ingredients with amounts
  - Proper grouping of "One of" vs "Each of" items

### [`process_tools(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L169)

Process tool requirements and format them for wiki display.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing tool requirements._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for tools section.

<ins>**Handles:**</ins>
  - Individual tool requirements
  - Tool tag groups
  - Tool condition flags
  - Proper grouping of "One of" vs "Each of" tools
  - Icon integration for tools

### [`process_recipes(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L252)

Process recipe learning methods and format them for wiki display.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing learning requirements._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for recipe learning section.

<ins>**Handles:**</ins>
  - Skillbook requirements
  - Auto-learn conditions
  - Schematic requirements
  - Trait requirements
  - Proper formatting with alternatives

### [`process_skills(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L339)

Process skill requirements and format them for wiki display.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing skill requirements._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for skills section.

<ins>**Handles:**</ins>
  - Skill level requirements
  - Multiple skill combinations
  - Proper formatting with alternatives

### [`process_workstation(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L367)

Process workstation requirements and format them for wiki display.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing workstation information._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for workstation section.

<ins>**Handles:**</ins>
  - Required crafting stations
  - Special location requirements
  - Proper formatting with alternatives

### [`process_products(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L390)

Process recipe products and format them for wiki display.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing product information._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for products section.

<ins>**Handles:**</ins>
  - Standard product outputs
  - Fluid outputs
  - Product amounts and variations
  - Icon integration for products

### [`process_xp(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L537)

Process experience gains and format them for wiki display.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing XP information._

<ins>**Returns:**</ins>
  - **str:**
      - Formatted wiki markup for XP section.

<ins>**Handles:**</ins>
  - XP amounts per skill
  - Multiple skill XP gains
  - Proper formatting with amounts

### [`fluid_rgb(fluid_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L560)

Get RGB color values for a fluid type.


<ins>**Args:**</ins>
  - **fluid_id (str)**:
      - _Identifier for the fluid._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary containing:
        - name: Display name of the fluid
        - R: Red color value
        - G: Green color value
        - B: Blue color value
      - Handles proper color mapping for all fluid types.

### [`gather_item_usage(recipes_data, tags_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L618)

Gather information about how items are used in recipes.


<ins>**Args:**</ins>
  - **recipes_data (dict)**:
      - _Dictionary of all recipe data._
  - **tags_data (dict)**:
      - _Dictionary of item tag data._

<ins>**Returns:**</ins>
  - **tuple:**
      - Four dictionaries mapping items to their recipe usage:
        - Normal recipe inputs
        - Normal recipe outputs
        - Construction recipe inputs
        - Construction recipe outputs
      - Tracks both direct item usage and tag-based usage.

### [`output_item_usage(normal_item_input_map, normal_item_output_map, construction_item_input_map, construction_item_output_map)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L751)

Generate wiki markup for item usage in recipes.


<ins>**Args:**</ins>
  - **normal_item_input_map (dict)**:
      - _Items used as inputs in normal recipes._
  - **normal_item_output_map (dict)**:
      - _Items produced as outputs in normal recipes._
  - **construction_item_input_map (dict)**:
      - _Items used as inputs in construction recipes._
  - **construction_item_output_map (dict)**:
      - _Items produced as outputs in construction recipes._
      - _Creates individual files documenting how each item is used in recipes,_
      - _both as ingredients and as products._

### [`output_skill_usage(recipes_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L839)

Generate wiki markup for skill usage in recipes.


<ins>**Args:**</ins>
  - **recipes_data (dict)**:
      - _Dictionary of all recipe data._
      - _Creates files documenting which recipes require each skill_
      - _and what level of skill is needed._

### [`strip_prefix(text, prefix)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L906)

Remove a prefix from text if it exists.


<ins>**Args:**</ins>
  - **text (str)**:
      - _Text to process._
  - **prefix (str)**:
      - _Prefix to remove._

<ins>**Returns:**</ins>
  - **str:**
      - Text with prefix removed if it existed, original text otherwise.

### [`output_lua_tables(processed_recipes)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L922)

Generate Lua tables for recipe data.


<ins>**Args:**</ins>
  - **processed_recipes (dict)**:
      - _Dictionary of processed recipe data._
      - _Creates Lua table files that can be used by wiki templates_
      - _to display recipe information._

### [`main(recipes_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/legacy_recipe_output.py#L1034)

Main execution function for recipe output generation.


<ins>**Args:**</ins>
  - **recipes_data (dict, optional)**:
      - _Pre-loaded recipe data._
      - _If None, data will be loaded from cache._
      - _This function:_
      - _1. Loads or uses provided recipe data_
      - _2. Processes all recipes into wiki format_
      - _3. Generates item usage documentation_
      - _4. Creates skill usage documentation_
      - _5. Outputs Lua tables for templates_



[Previous Folder](../parser/distribution_container_parser.md) | [Previous File](legacy_recipe_format.md) | [Next File](legacy_recipe_parser.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
