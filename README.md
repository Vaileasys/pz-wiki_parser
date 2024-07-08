# PZ Script Parser
Parses Project Zomboid 'scripts' files and outputs in the desired format for PZwiki.

# Requires:
* Python 3
* Chardet

# Instructions
## Setting up the resources folder
1. Create a folder called "resources" in the same folder as `main.py`. 
2. Add the game's scripts files to a folder called "scripts".
3. Add the game's icons to a folder called "icons" (ensure 'Item_' prefix is removed). This is only relevant for some modules.
4. Add the desired translations to a "Translate" folder. E.g. `ItemName_EN.txt` can go in 'resources\Translate\ItemName'. This will output the correct in-game name rather than the DisplayName value.

## Using a module
This programme is bundled with a range of modules that can be run independently or in the terminal by first running `main.py`.
1. Run `main.py`
2. Select a module/script you want to run.
3. Follow the prompts for that module.
4. The script will run, parsing the data, and then output. Some modules will output to a file such as `output.txt` while others will just output to the terminal.

_Some scripts will prompt the user for a language code (default 'en') which is used to translate to the desired language. The translations must have been added to the "Translate" folder._

## Creating a module

### Using parsed data
The parser stores data in a nested dictionary, where the top-level keys are module names, the second-level keys are item types within each module, and the third-level keys are properties of each item type.
Example: DisplayCategory for Base.Axe
* module: Base
* type: Axe
* property: DisplayCategory

_After running the script parser, the parsed data can be visualised as indentations in `parsed_data.txt`._
1. Import `script_parser`
2. Call a value using the `get()` method. E.g. `display_category = script_parser.main().get('DisplayCategory')`.

### Adding module to available commands
Modules can be run via `main.py` using `importlib`. 
1. Go to `main.py` and add your module along with its description to `help_info`.
	E.g. `'user_input': "my_script: my script description",`
2. Add your module to `scripts`.
	E.g. `user_input': 'my_script',`
