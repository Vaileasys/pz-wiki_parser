[Previous Folder](../parser/distribution_container_parser.md) | [Next File](evolvedrecipe.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)

# craft_recipes.py

> Project Zomboid Wiki Crafting Recipe Processor

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

### [`fluid_rgb(fluid_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L36)

_Get RGB color values for a fluid type._

<ins>**Args:**</ins>
  - **fluid_id (str)**:
      - _Fluid identifier, can be in form 'categories[Water]'._

<ins>**Returns:**</ins>
  - **dict:**
      - Dictionary containing:
      - - name: Display name of the fluid
      - - R: Red color value (0-255)
      - - G: Green color value (0-255)
      - - B: Blue color value (0-255)
      - Raises:
  - **RuntimeError:**
      - If there's an error processing the fluid.
      - Handles:
      - - Category-based fluid IDs
      - - Color reference lookups
      - - Tainted water special case
      - - RGB value normalization
### [`process_ingredients(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L106)

_Process recipe ingredients into wiki markup._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing ingredients._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for ingredients section.
      - Handles:
      - - Energy inputs
      - - Fluid ingredients with colors
      - - Numbered list ingredients
      - - Tag-based ingredients
      - - Simple item ingredients
      - - Proper grouping of "One of" vs "Each of" items
      - - Icon integration
### [`process_tools(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L301)

_Process tool requirements into wiki markup._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing tool requirements._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for tools section.
      - Handles:
      - - Individual tool requirements
      - - Tool tag groups
      - - Tool condition flags
      - - Icon integration
      - - Proper grouping of requirements
### [`process_workstation(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L385)

_Process workstation requirements into wiki markup._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing workstation info._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for workstation section.
      - Handles:
      - - Required crafting stations
      - - Special location requirements
      - - Building-specific workstations
### [`process_output_mapper(recipe: dict, mapper_key: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L450)

_Process output mapper strings into item lists._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing mappers._
  - **mapper_key (str)**:
      - _Key for the mapper to process._

<ins>**Returns:**</ins>
  - **list[str]:**
      - List of mapped item IDs.
      - Handles:
      - - Mapper resolution
      - - Item ID normalization
      - - Multiple mapper types
### [`process_products(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L499)

_Process recipe products into wiki markup._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing products._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for products section.
      - Handles:
      - - Standard product outputs
      - - Building recipe outputs
      - - Fluid outputs with colors
      - - Icon integration
      - - Amount formatting
### [`process_xp(recipe: dict, build_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L672)

_Process experience gains into wiki markup._

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing XP info._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for XP section.
      - Handles:
      - - XP amounts per skill
      - - Multiple skill XP gains
      - - Building-specific XP
### [`process_recipes(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L710)

_Process recipe learning methods into wiki markup._

<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing learning methods._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for recipe learning section.
      - Handles:
      - - Skillbook requirements
      - - Auto-learn conditions
      - - Schematic requirements
      - - Trait requirements
### [`process_skills(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L785)

_Process skill requirements into wiki markup._

<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing skill requirements._

<ins>**Returns:**</ins>
  - **str:**
      - Wiki markup for skills section.
      - Handles:
      - - Required skill levels
      - - Multiple skill requirements
      - - Skill alternatives
### [`process_requirements(recipe: dict, parsed_item_metadata: dict, literature_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L811)

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
      - Handles:
      - - Skill requirements
      - - Literature requirements
      - - Trait requirements
      - - Auto-learn conditions
### [`build_tag_to_items_map(parsed_item_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L896)

_Build mapping of tags to items._

<ins>**Args:**</ins>
  - **parsed_item_data (dict)**:
      - _Parsed item data._

<ins>**Returns:**</ins>
  - **dict[str, list[dict[str, str]]]:**
      - Mapping of tags to item lists.
      - Creates a lookup table for items by their tags.
### [`output_item_article_lists(crafting_recipe_map: dict[str, dict], building_recipe_map: dict[str, dict], tag_to_items_map: dict[str, list[dict[str, str]]])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L917)

_Generate wiki article lists for items._

<ins>**Args:**</ins>
### [`output_skill_usage(recipe_data_map: dict[str, dict])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1049)

_Generate wiki markup for skill usage._

<ins>**Args:**</ins>
### [`output_lua_tables(recipe_data_map: dict[str, dict])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1097)

_Generate Lua tables for recipe data._

<ins>**Args:**</ins>
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1205)

_Main execution function for recipe processing._


[Previous Folder](../parser/distribution_container_parser.md) | [Next File](evolvedrecipe.md) | [Next Folder](../tiles/named_furniture_filter.md) | [Back to Index](../../index.md)
