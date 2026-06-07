[Previous Folder](../objects/animal.md) | [Next File](distribution_container_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# creation_method_parser.py

Parser for MainCreationMethods.lua file to extract traits and occupations data with translation support.

## Functions

### [`determine_trait_type(cost: int) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L14)

Determine if a trait is positive or negative based on cost.

### [`determine_occupation_points_type(cost: int) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L24)

Determine if an occupation cost is positive or negative.

### [`generate_trait_infobox(trait_data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L34)

Generate a trait infobox in the specified format.

### [`generate_occupation_infobox(occupation_data: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L81)

Generate an occupation infobox in the specified format.

### [`output_trait_files(traits_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L148)

Output trait infobox files to the output directory.

### [`output_occupation_files(occupations_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L171)

Output occupation infobox files to the output directory.

### [`output_recipe_files(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L194)

Output recipe files for traits and occupations to the output directory.

### [`remove_comments(lua_content: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L246)

Remove both single-line and multi-line comments from Lua code.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Raw Lua file content_

<ins>**Returns:**</ins>
  - **str**:
      - _Lua content with comments removed_

### [`parse_trait_factory_calls(lua_content: str) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L270)

Parse TraitFactory.addTrait calls to extract trait data.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Lua content with comments removed_

<ins>**Returns:**</ins>
  - **dict**:
      - _Structured traits data_

### [`parse_trait_xp_boosts(lua_content: str, traits: dict) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L325)

Parse XP boost assignments for traits.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Lua content with comments removed_
  - **traits (dict)**:
      - _Traits dictionary to update_

### [`parse_trait_free_recipes(lua_content: str, traits: dict) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L358)

Parse free recipe assignments for traits.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Lua content with comments removed_
  - **traits (dict)**:
      - _Traits dictionary to update_

### [`parse_mutual_exclusions(lua_content: str, traits: dict) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L389)

Parse mutual exclusion rules for traits.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Lua content with comments removed_
  - **traits (dict)**:
      - _Traits dictionary to update_

### [`parse_profession_factory_calls(lua_content: str) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L417)

Parse ProfessionFactory.addProfession calls to extract profession data.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Lua content with comments removed_

<ins>**Returns:**</ins>
  - **dict**:
      - _Structured professions data_

### [`parse_profession_xp_boosts(lua_content: str, professions: dict) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L459)

Parse XP boost assignments for professions.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Lua content with comments removed_
  - **professions (dict)**:
      - _Professions dictionary to update_

### [`parse_profession_free_traits(lua_content: str, professions: dict) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L490)

Parse free trait assignments for professions.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Lua content with comments removed_
  - **professions (dict)**:
      - _Professions dictionary to update_

### [`parse_profession_free_recipes(lua_content: str, professions: dict) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L522)

Parse free recipe assignments for professions.

<ins>**Args:**</ins>
  - **lua_content (str)**:
      - _Lua content with comments removed_
  - **professions (dict)**:
      - _Professions dictionary to update_

### [`parse_lua_file() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L553)

Main function to parse the Lua file and extract traits and occupations data.

<ins>**Returns:**</ins>
  - **dict**:
      - _Complete parsed data with traits and occupations_

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/creation_method_parser.py#L603)

Main function to run the parser and save the cache.


[Previous Folder](../objects/animal.md) | [Next File](distribution_container_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
