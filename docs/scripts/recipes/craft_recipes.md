[Previous Folder](../parser/distribution_container_parser.md) | [Next File](evolvedrecipe.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)

# craft_recipes.py

Project Zomboid Wiki Crafting Recipe Processor

This script processes crafting recipes from Project Zomboid, converting them into
wiki-ready format. It handles both standard crafting recipes and building recipes,
with support for various recipe components and special cases.

The script handles:
- Fluid processing with RGB color values
- Ingredient processing with quantities
- Tool requirements and workstations
- Product outputs and mappers
- Experience gains and skill requirements
- Recipe learning methods
- Item and skill usage documentation
- Lua table generation for templates

## Functions

### [`get_unit_tool_ids()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L37)

Get list of item IDs that should be treated as unit tools.

Finds all items with Type "Drainable" from the item data cache.

<ins>**Returns:**</ins>
  - **list[str]:**
      - List of item IDs that are unit tools (drainable items)

### [`get_use_delta(item_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L59)

Get the UseDelta value for a unit tool item.


<ins>**Args:**</ins>
  - **item_id (str)**:
      - _The item ID to look up_

<ins>**Returns:**</ins>
  - **float:**
      - The UseDelta value as a float, or 0.1 as default if not found

### [`fluid_rgb(fluid_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L77)

Get RGB color values for a fluid type.


<ins>**Args:**</ins>
  - **fluid_id (str)**:
      - _Fluid identifier, can be in form 'categories[Water]'._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary containing:
        - name: Display name of the fluid
        - R: Red color value (0-255)
        - G: Green color value (0-255)
        - B: Blue color value (0-255)

<ins>**Raises:**</ins>
  - **RuntimeError:**
      - If there's an error processing the fluid.

<ins>**Handles:**</ins>
  - Category-based fluid IDs
  - RGB value normalization

### [`process_ingredients(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L121)

Process recipe ingredients into wiki markup.


<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing ingredients._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for ingredients section.

<ins>**Handles:**</ins>
  - Energy inputs
  - Fluid ingredients with colors
  - Numbered list ingredients
  - Tag-based ingredients
  - Simple item ingredients
  - Proper grouping of "One of" vs "Each of" items
  - Icon integration
  - Unit items with Unit bar template

### [`process_tools(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L353)

Process tool requirements into wiki markup.


<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing tool requirements._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for tools section.

<ins>**Handles:**</ins>
  - Individual tool requirements
  - Tool tag groups
  - Tool condition flags
  - Icon integration
  - Proper grouping of requirements
  - Unit items with Unit bar template

### [`process_workstation(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L452)

Process workstation requirements into wiki markup.


<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing workstation info._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for workstation section.

<ins>**Handles:**</ins>
  - Required crafting stations
  - Special location requirements
  - Building-specific workstations

### [`process_output_mapper(recipe: dict, mapper_key: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L520)

Process output mapper strings into item lists.


<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing mappers._
  - **mapper_key (str)**:
      - _Key for the mapper to process._

<ins>**Returns:**</ins>
  - **list[str]:**
      - List of mapped item IDs.

<ins>**Handles:**</ins>
  - Mapper resolution
  - Item ID normalization
  - Multiple mapper types

### [`process_products(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L565)

Process recipe products into wiki markup.


<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing products._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for products section.

<ins>**Handles:**</ins>
  - Standard product outputs
  - Building recipe outputs
  - Fluid outputs with colors
  - Icon integration
  - Amount formatting

### [`process_xp(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L735)

Process experience gains into wiki markup.


<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing XP info._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for XP section.

<ins>**Handles:**</ins>
  - XP amounts per skill
  - Multiple skill XP gains
  - Building-specific XP

### [`process_recipes(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L773)

Process recipe learning methods into wiki markup.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing learning methods._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for recipe learning section.

<ins>**Handles:**</ins>
  - Skillbook requirements
  - Auto-learn conditions
  - Schematic requirements
  - Trait requirements

### [`process_skills(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L858)

Process skill requirements into wiki markup.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing skill requirements._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for skills section.

<ins>**Handles:**</ins>
  - Required skill levels
  - Multiple skill requirements
  - Skill alternatives

### [`process_requirements(recipe: dict, literature_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L884)

Process recipe requirements into wiki markup.


<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data._
  - **parsed_item_metadata (dict)**:
      - _Item metadata for reference._
  - **literature_data (dict)**:
      - _Literature data for books/magazines._

<ins>**Returns:**</ins>
  - **tuple[str, str]:**
      - (recipes_markup, skills_markup) for wiki sections.

<ins>**Handles:**</ins>
  - Skill requirements
  - Literature requirements
  - Trait requirements
  - Auto-learn conditions

### [`build_tag_to_items_map()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L977)

Build mapping of tags to items.


<ins>**Args:**</ins>
  - **parsed_item_data (dict)**:
      - _Parsed item data._

<ins>**Returns:**</ins>
  - **dict[str, list[dict[str, str]]]:**
      - Mapping of tags to item lists.
      - Creates a lookup table for items by their tags.

### [`output_item_article_lists(crafting_recipe_map: dict[str, dict], building_recipe_map: dict[str, dict], tag_to_items_map: dict[str, list[dict[str, str]]])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L998)

Generate wiki article lists for items.


<ins>**Args:**</ins>
  - **crafting_recipe_map (dict[str, dict])**:
      - _Crafting recipe data._
  - **building_recipe_map (dict[str, dict])**:
      - _Building recipe data._
  - **tag_to_items_map (dict[str, list[dict[str, str]]])**:
      - _Tag to items mapping._
      - _Creates files documenting how items are used in recipes,_
      - _both as ingredients and as products._

### [`output_skill_usage(recipe_data_map: dict[str, dict])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1134)

Generate wiki markup for skill usage.


<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
      - _Creates files documenting which recipes require each skill_
      - _and what level of skill is needed._

### [`output_category_usage(recipe_data_map: dict[str, dict])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1182)

Generate wiki markup for category usage.


<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
      - _Creates files documenting which recipes belong to each category_
      - _and outputs them in template format._

### [`output_lua_tables(recipe_data_map: dict[str, dict])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1215)

Generate Lua tables for recipe data.


<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
      - _Creates Lua table files that can be used by wiki templates_
      - _to display recipe information._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1323)

Main execution function for recipe processing.

This function:
1. Loads necessary data from parsers
2. Processes all recipes into wiki format
3. Generates item usage documentation
4. Creates skill usage documentation
5. Outputs Lua tables for templates



[Previous Folder](../parser/distribution_container_parser.md) | [Next File](evolvedrecipe.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
