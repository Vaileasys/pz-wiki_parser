[Previous Folder](../objects/components.md) | [Previous File](distribution_container_parser.md) | [Next File](evolvedrecipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# distribution_parser.py

## Functions

### [`parse_container_files(distributions_lua_path, procedural_distributions_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L15)

_Parses Lua container files to extract distribution data and convert it to JSON format._

### [`parse_foraging(forage_definitions_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L237)

_Parses foraging-related Lua files and combines their data into a single JSON output._

<ins>**Args:**</ins>
  - **forage_definitions_path (str)**:
      - _Path to the primary forageDefinitions.lua file._
  - **output_path (str)**:
      - _Directory where the final foraging JSON will be saved._

### [`parse_vehicles(vehicle_distributions_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L349)

_Parse the Lua vehicle distribution file and convert it into JSON format._

### [`parse_attachedweapons(attached_weapon_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L428)

_Parses a Lua file containing attached weapon definitions and converts it into a JSON format._

<ins>**Args:**</ins>
  - **attached_weapon_path (str)**:
      - _The file path to the Lua file containing attached weapon definitions._
  - **output_path (str)**:
      - _The directory where the output JSON file ('attached_weapons.json') will be saved._

<ins>**Raises:**</ins>
  - **Exception:**
      - If there is an error executing Lua code or processing the Lua tables.

### [`parse_clothing(clothing_file_path, guid_table_path, output_file)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L501)

_Parse the clothing XML file and generate a JSON file containing outfit data with item probabilities._

### [`parse_stories(class_files_directory, output_file)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L573)

_Processes all .class files in the given directory and collects their relevant string constants._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L683)
### [`init()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L708)


[Previous Folder](../objects/components.md) | [Previous File](distribution_container_parser.md) | [Next File](evolvedrecipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
