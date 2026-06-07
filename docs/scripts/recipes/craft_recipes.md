[Previous Folder](../parser/creation_method_parser.md) | [Next File](evolved_recipes.md) | [Next Folder](../tiles/entity_article.md) | [Back to Index](../../index.md)

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

### [`get_unit_tool_ids() -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L41)

Get list of item IDs that should be treated as unit tools.
Finds all items with Type "Drainable" from the item data cache.

<ins>**Returns:**</ins>
  - **list[str]**:
      - _List of item IDs that are unit tools (drainable items)_

### [`get_use_delta(item_id: str) -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L64)

Get the UseDelta value for a unit tool item.

<ins>**Args:**</ins>
  - **item_id (str)**:
      - _The item ID to look up_

<ins>**Returns:**</ins>
  - **float**:
      - _The UseDelta value as a float, or 0.1 as default if not found_

### [`format_count(count_data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L82)

Format count as 'min-max' string or int for display.

<ins>**Args:**</ins>
  - **count_data**:
      - _Either an int for fixed counts or a dict with min/max/variable keys_

<ins>**Returns:**</ins>
  - **str | int**:
      - _Formatted count as "min-max" string for variable counts, or int for fixed counts_

### [`fluid_rgb(fluid_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L97)

Get RGB color values for a fluid type.

Raises:
    RuntimeError: If there's an error processing the fluid.

Handles:
- Category-based fluid IDs
- RGB value normalization

<ins>**Args:**</ins>
  - **fluid_id (str)**:
      - _Fluid identifier, can be in form 'categories[Water]'._

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary containing:_
  - **- name**:
      - _Display name of the fluid_
  - **- R**:
      - _Red color value (0-255)_
  - **- G**:
      - _Green color value (0-255)_
  - **- B**:
      - _Blue color value (0-255)_

### [`process_ingredients(recipe: dict, build_data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L136)

Process recipe ingredients into wiki markup.

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing ingredients._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str**:
      - _Wiki markup for ingredients section._
  - **Handles**:
  - **- Energy inputs**:
  - **- Fluid ingredients with colors**:
  - **- Numbered list ingredients**:
  - **- Tag-based ingredients**:
  - **- Simple item ingredients**:
  - **- Proper grouping of "One of" vs "Each of" items**:
  - **- Icon integration**:
  - **- Unit items with Unit bar template**:

### [`process_tools(recipe: dict, build_data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L385)

Process tool requirements into wiki markup.

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing tool requirements._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str**:
      - _Wiki markup for tools section._
  - **Handles**:
  - **- Individual tool requirements**:
  - **- Tool tag groups**:
  - **- Tool condition flags**:
  - **- Icon integration**:
  - **- Proper grouping of requirements**:
  - **- Unit items with Unit bar template**:

### [`process_workstation(recipe: dict, build_data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L492)

Process workstation requirements into wiki markup.

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing workstation info._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str**:
      - _Wiki markup for workstation section._
  - **Handles**:
  - **- Required crafting stations**:
  - **- Special location requirements**:
  - **- Building-specific workstations**:

### [`process_output_mapper(recipe: dict, mapper_key: str) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L570)

Process output mapper strings into item lists.

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing mappers._
  - **mapper_key (str)**:
      - _Key for the mapper to process._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _List of mapped item IDs._
  - **Handles**:
  - **- Mapper resolution**:
  - **- Item ID normalization**:
  - **- Multiple mapper types**:

### [`process_products(recipe: dict, build_data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L616)

Process recipe products into wiki markup.

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing products._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str**:
      - _Wiki markup for products section._
  - **Handles**:
  - **- Standard product outputs**:
  - **- Building recipe outputs**:
  - **- Fluid outputs with colors**:
  - **- Icon integration**:
  - **- Amount formatting**:

### [`process_xp(recipe: dict, build_data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L802)

Process experience gains into wiki markup.

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data containing XP info._
  - **build_data (dict)**:
      - _Additional building recipe data._

<ins>**Returns:**</ins>
  - **str**:
      - _Wiki markup for XP section._
  - **Handles**:
  - **- XP amounts per skill**:
  - **- Multiple skill XP gains**:
  - **- Building-specific XP**:

### [`process_recipes(data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L840)

Process recipe learning methods into wiki markup.

<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing learning methods._

<ins>**Returns:**</ins>
  - **str**:
      - _Wiki markup for recipe learning section._
  - **Handles**:
  - **- Skillbook requirements**:
  - **- Auto-learn conditions**:
  - **- Schematic requirements**:
  - **- Trait requirements**:

### [`process_skills(data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L933)

Process skill requirements into wiki markup.

<ins>**Args:**</ins>
  - **data (dict)**:
      - _Recipe data containing skill requirements._

<ins>**Returns:**</ins>
  - **str**:
      - _Wiki markup for skills section._
  - **Handles**:
  - **- Required skill levels**:
  - **- Multiple skill requirements**:
  - **- Skill alternatives**:

### [`process_requirements(recipe: dict, literature_data: dict) -> tuple[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L961)

Process recipe requirements into wiki markup.

<ins>**Args:**</ins>
  - **recipe (dict)**:
      - _Recipe data._
  - **parsed_item_metadata (dict)**:
      - _Item metadata for reference._
  - **literature_data (dict)**:
      - _Literature data for books/magazines._

<ins>**Returns:**</ins>
  - **tuple[str, str]**:
      - _(recipes_markup, skills_markup) for wiki sections._
  - **Handles**:
  - **- Skill requirements**:
  - **- Literature requirements**:
  - **- Trait requirements**:
  - **- Auto-learn conditions**:

### [`build_research_items_map(craft_data: dict, build_data: dict) -> dict[str, list[str]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1069)

Build a reverse mapping of recipe_id -> list of item IDs that can research that recipe.

This is the reverse of researchrecipes.py: instead of listing which recipes an item
can teach, this lists which items can be used to research/unlock a given recipe.

Two sources are combined:
- Items whose ResearchableRecipes property lists this recipe (after meta expansion).
- Items that are outputs of this recipe when the recipe requires skill or auto-learn.

<ins>**Args:**</ins>
  - **craft_data (dict)**:
      - _Raw crafting recipe data keyed by recipe_id._
  - **build_data (dict)**:
      - _Raw building/entity recipe data keyed by recipe_id._

<ins>**Returns:**</ins>
  - **dict[str, list[str]]**:
      - _recipe_id -> sorted list of item IDs._

### [`process_research_items(recipe_id: str, research_items_map: dict[str, list[str]]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1120)

Generate a collapsible wiki list of items that can be researched to learn this recipe.

<ins>**Args:**</ins>
  - **recipe_id (str)**:
      - _The recipe identifier._
  - **research_items_map (dict[str, list[str]])**:
      - _Mapping from recipe_id to item IDs._

<ins>**Returns:**</ins>
  - **str**:
      - _Wiki markup for a collapsible list, or empty string if none._

### [`build_tag_to_items_map() -> dict[str, list[dict[str, str]]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1158)

Build mapping of tags to items.

<ins>**Args:**</ins>
  - **parsed_item_data (dict)**:
      - _Parsed item data._

<ins>**Returns:**</ins>
  - **dict[str, list[dict[str, str]]]**:
      - _Mapping of tags to item lists._
  - **Creates a lookup table for items by their tags.**:

### [`output_item_article_lists(crafting_recipe_map: dict[str, dict], building_recipe_map: dict[str, dict], tag_to_items_map: dict[str, list[dict[str, str]]]) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1179)

Generate wiki article lists for items with id and page subfolders.

<ins>**Args:**</ins>
  - **crafting_recipe_map (dict[str, dict])**:
      - _Crafting recipe data._
  - **building_recipe_map (dict[str, dict])**:
      - _Building recipe data._
  - **tag_to_items_map (dict[str, list[dict[str, str]]])**:
      - _Tag to items mapping._
  - **Creates files documenting how items are used in recipes,**:
  - **both as ingredients and as products. Organizes outputs into**:
  - **id and page subfolders for better wiki organization.**:

### [`output_skill_usage(recipe_data_map: dict[str, dict]) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1475)

Generate wiki markup for skill usage.

<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
  - **Creates files documenting which recipes require each skill**:
  - **and what level of skill is needed.**:

### [`output_category_usage(recipe_data_map: dict[str, dict]) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1549)

Generate wiki markup for category usage.

<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
  - **Creates files documenting which recipes belong to each category**:
  - **and outputs them in template format.**:

### [`output_workstation_usage(recipe_data_map: dict[str, dict]) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1608)

Generate wiki markup for workstation usage.

<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
  - **Creates files documenting which recipes require each workstation,**:
  - **organized by crafting vs building recipes.**:

### [`output_tag_usage(crafting_recipe_map: dict[str, dict], building_recipe_map: dict[str, dict]) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1723)

Generate wiki markup for tag usage.

<ins>**Args:**</ins>
  - **crafting_recipe_map (dict[str, dict])**:
      - _Crafting recipe data._
  - **building_recipe_map (dict[str, dict])**:
      - _Building recipe data._
  - **Creates files documenting which recipes use each tag,**:
  - **organized by crafting vs building recipes.**:

### [`output_lua_tables(recipe_data_map: dict[str, dict]) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1827)

Generate Lua tables for recipe data.

<ins>**Args:**</ins>
  - **recipe_data_map (dict[str, dict])**:
      - _Recipe data._
  - **Creates Lua table files that can be used by wiki templates**:
  - **to display recipe information.**:

### [`main(batch: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/recipes/craft_recipes.py#L1935)

Main execution function for recipe processing.

<ins>**Args:**</ins>
  - **batch (bool)**:
      - _If True, skip language initialization_
  - **This function**:
  - **1. Loads necessary data from parsers**:
  - **2. Processes all recipes into wiki format**:
  - **3. Generates item usage documentation**:
  - **4. Creates skill usage documentation**:
  - **5. Outputs Lua tables for templates**:


[Previous Folder](../parser/creation_method_parser.md) | [Next File](evolved_recipes.md) | [Next Folder](../tiles/entity_article.md) | [Back to Index](../../index.md)
