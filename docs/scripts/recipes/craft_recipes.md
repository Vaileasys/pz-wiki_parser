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

### [`fluid_rgb(fluid_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L35)

_Get RGB color values for a fluid type._

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
  - Color reference lookups
  - Tainted water special case
  - RGB value normalization

### [`process_ingredients(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L105)

_Process recipe ingredients into wiki markup._

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

### [`process_tools(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L300)

_Process tool requirements into wiki markup._

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

### [`process_workstation(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L384)

_Process workstation requirements into wiki markup._

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

### [`process_output_mapper(recipe: dict, mapper_key: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L449)

_Process output mapper strings into item lists._

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

### [`process_products(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L498)

_Process recipe products into wiki markup._

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

### [`process_xp(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L671)

_Process experience gains into wiki markup._

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

### [`process_recipes(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L709)

_Process recipe learning methods into wiki markup._

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

### [`process_skills(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L784)

_Process skill requirements into wiki markup._

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

### [`process_requirements(recipe: dict, parsed_item_metadata: dict, literature_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L810)

_Process recipe requirements into wiki markup._

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

### [`build_tag_to_items_map(parsed_item_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L895)

_Build mapping of tags to items._

<ins>**Args:**</ins>
  - **parsed_item_data (dict)**:
      - _Parsed item data._

<ins>**Returns:**</ins>
  - **dict[str, list[dict[str, str]]]:**
      - Mapping of tags to item lists.
      - Creates a lookup table for items by their tags.

### [`output_item_article_lists(crafting_recipe_map: dict[str, dict], building_recipe_map: dict[str, dict], tag_to_items_map: dict[str, list[dict[str, str]]])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L916)

_Generate wiki article lists for items._

<ins>**Args:**</ins>
  - **crafting_recipe_map (dict[str, dict])**:
      - _Crafting recipe data._
  - **building_recipe_map (dict[str, dict])**:
      - _Building recipe data._
  - **tag_to_items_map (dict[str, list[dict[str, str]]])**:
      - _Tag to items mapping._
      - _Creates files documenting how items are used in recipes,_
      - _both as ingredients and as products._

### [`output_skill_usage(recipe_data_map: dict[str, dict])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1048)

_Generate wiki markup for skill usage._

<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
      - _Creates files documenting which recipes require each skill_
      - _and what level of skill is needed._

### [`output_lua_tables(recipe_data_map: dict[str, dict])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1096)

_Generate Lua tables for recipe data._

<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
      - _Creates Lua table files that can be used by wiki templates_
      - _to display recipe information._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1204)

_Main execution function for recipe processing._



[Previous Folder](../parser/distribution_container_parser.md) | [Next File](evolvedrecipe.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
