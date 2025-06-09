[Previous Folder](../objects/body_location.md) | [Previous File](distribution_container_parser.md) | [Next File](evolvedrecipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# distribution_parser.py

## Functions

### [`parse_container_files(distributions_lua_path, procedural_distributions_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L15)

Parses Lua container files to extract distribution data and convert it to JSON format.

Includes debug statements at each step for troubleshooting.

### [`parse_foraging(forage_definitions_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L237)

Parses foraging-related Lua files and combines their data into a single JSON output.

This function reads the main forageDefinitions.lua and other foraging-related Lua files, extracts
relevant data, and augments the extracted data with additional information like item chances. The
results are then saved into a JSON file.

<ins>**Args:**</ins>
  - **forage_definitions_path (str)**:
      - _Path to the primary forageDefinitions.lua file._
  - **output_path (str)**:
      - _Directory where the final foraging JSON will be saved._

### [`parse_vehicles(vehicle_distributions_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L349)

Parse the Lua vehicle distribution file and convert it into JSON format.

Parameters:
vehicle_distributions_path (str): Path to the Lua file to parse.
output_path (str): Path where the output JSON file will be written.

### [`parse_attachedweapons(attached_weapon_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L428)

Parses a Lua file containing attached weapon definitions and converts it into a JSON format.

This function reads a Lua file specified by the `attached_weapon_path`, executes the Lua code
within a Lua runtime to retrieve the 'AttachedWeaponDefinitions' table, and converts this table
into a Python dictionary. It specifically extracts entries that contain a 'chance' field,
which are considered weapon definitions. The resulting dictionary is then written to a JSON
file at the specified `output_path`.

<ins>**Args:**</ins>
  - **attached_weapon_path (str)**:
      - _The file path to the Lua file containing attached weapon definitions._
  - **output_path (str)**:
      - _The directory where the output JSON file ('attached_weapons.json') will be saved._

<ins>**Raises:**</ins>
  - **Exception:**
      - If there is an error executing Lua code or processing the Lua tables.

### [`parse_clothing(clothing_file_path, guid_table_path, output_file)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L501)

Parse the clothing XML file and generate a JSON file containing outfit data with item probabilities.

:param clothing_file_path: The path to the clothing XML file
:param guid_table_path: The path to the GUID table XML file
:param output_file_path: The path to the output JSON file
:return: None

### [`parse_stories(class_files_directory, output_file)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L573)

Processes all .class files in the given directory and collects their relevant string constants.

This function takes two parameters: the path to the directory containing the .class files
and the path to the output JSON file.
It first processes each .class file in the given directory and collects their relevant string
constants. It then saves the collected constants to a JSON file at the specified output path.
:param class_files_directory: The path to the directory containing the .class files
:param output_path: The path to the output JSON file
:return: None

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L683)
### [`init()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L708)


[Previous Folder](../objects/body_location.md) | [Previous File](distribution_container_parser.md) | [Next File](evolvedrecipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
