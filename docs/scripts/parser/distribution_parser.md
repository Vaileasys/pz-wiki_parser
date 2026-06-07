[Previous Folder](../objects/animal.md) | [Previous File](distribution_container_parser.md) | [Next File](evolvedrecipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# distribution_parser.py

## Functions

### [`parse_container_files(distributions_lua_path, procedural_distributions_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L20)

Parses Lua container files to extract distribution data and convert it to JSON format.
Includes debug statements at each step for troubleshooting.

### [`parse_foraging(output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L277)

Parses foraging-related Lua files and combines their data into a single JSON output.

This function reads the main forageDefinitions.lua and other foraging-related Lua files, extracts
relevant data, and augments the extracted data with additional information like item chances. The
results are then saved into a JSON file.

<ins>**Args:**</ins>
  - **output_path (str)**:
      - _Directory where the final foraging JSON will be saved._

### [`parse_vehicles(vehicle_distributions_path, output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L398)

Parse the Lua vehicle distribution file and convert it into JSON format.

<ins>**Args:**</ins>
  - **vehicle_distributions_path (str)**:
      - _Path to the Lua file to parse._
  - **output_path (str)**:
      - _Path where the output JSON file will be written._

### [`parse_clothing(clothing_file_path, guid_table_path, output_file)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L481)

Parse the clothing XML file and generate a JSON file containing outfit data with item probabilities.

:param clothing_file_path: The path to the clothing XML file
:param guid_table_path: The path to the GUID table XML file
:return: None

### [`check_decompiler_output()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L571)

Check if the ZomboidDecompiler output directory exists.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if decompiler output exists, False otherwise_

### [`ensure_decompiler_run()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L582)

Ensure the ZomboidDecompiler has been run.
If not, run it now.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if decompiler output exists or was successfully created, False otherwise_

### [`parse_stories(output_file)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L636)

Parses story-related files from the game directory and decompiled Java files.

This function orchestrates parsing of:
- Story clutter definitions from Lua files
- Various story types from decompiled Java files (building, table, survivor, vehicle, zone)

The parsing process:
1. Extracts all strings containing "Base." from Java files and removes the prefix
2. Checks if story clutter category names appear in each Java file
3. If found, includes all items from that clutter category in the story's item list

<ins>**Args:**</ins>
  - **output_file (str)**:
      - _Name of the output JSON file (will be saved in cache/distributions/)_

### [`parse_container_contents(output_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L921)

Parse container contents using distribution_container_parser and save to cache.
This generates the same data as item_container_contents.py but saves it to cache.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L1063)

Main function to process all distribution data.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if processing was successful, False if decompiler check failed_

### [`init(*file_paths)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_parser.py#L1113)


[Previous Folder](../objects/animal.md) | [Previous File](distribution_container_parser.md) | [Next File](evolvedrecipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
