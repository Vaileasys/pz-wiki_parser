# PZ Script Parser
Parses Project Zomboid 'scripts' files and outputs in the desired format for PZwiki.

# Requires:
* Python 3 (Written for 3.12)
* Chardet

# Instructions
## Setting up the resources folder
1. Create a folder called "resources" in the same folder as `main.py`. 
2. Add the game's scripts files to a folder called "scripts".
3. Add the game's icons to a folder called "icons" (ensure 'Item_' prefix is removed). This is only relevant for some modules.
4. Add the desired translations to a "Translate" folder. E.g. `ItemName_EN.txt` can go in 'resources\Translate\ItemName'. This will output the correct in-game name rather than the DisplayName value.
5. Add `item_id_dictionary.csv` from  [here](https://drive.google.com/file/d/1Gjl7WJMm7qYaJ5S_J2FtM1iTlyfLI-z8/view).
6. Add `icons.csv` (Currently not public/implemented).

## Using a module
This programme is bundled with a range of modules that can be used by first running `main.py`. Most modules will **not** work if you try to run them directly.
1. Run `main.py`.
2. Follow the menus to run the desired script.
3. Follow the prompts for that module.
4. The script will run, parsing the data, and then output. Some modules will output to a file such as `output.txt` while others will just output to the terminal.

_Some scripts will prompt the user for a language code (default 'en') which is used to translate to the desired language. The translations must have been added to the "Translate" folder._

## Generating articles
Article generation requires the use of multiple modules and scripts in order to return good output.
1. Copy the output from [here](https://github.com/CalvyPZ/pz-distribution-to-wikitable) into `resources`, and rename the folder `distribution`.
2. (Not public/implemented) Add the output of the code scraper to the `resources` folder named `code`.
3. Run each module in the `Data generation` tree to generate usable data.

## Creating a module

### Using parsed data
The parser stores data in a nested dictionary, where the top-level keys are module names, the second-level keys are item types within each module, and the third-level keys are properties of each item type.
Example: DisplayCategory for Base.Axe
* module: Base
* type: Axe
* property: DisplayCategory

_After running the script parser, the parsed data can be visualised as indentations in `parsed_data.txt`._
1. Import `script_parser`
2. Call a value using the `get()` method. E.g. `data[module_name][item_type].get(property_name)`

### Adding module to available commands
Modules can be run via `main.py` using `importlib`. 
1. Add your module to `/scripts/`
2. Add a new line to the menu tree in `main.py` with your module, name, and description.
	E.g. `'1': {'module': 'infobox', 'name': 'Infobox', 'description': 'Generates infoboxes.'},`
