Welcome to the **PZwiki Parser** wiki! This project is designed to streamline the processing of game data from Project Zomboid into a structured output format that can be easily integrated into the [PZwiki](https://pzwiki.net). This documentation will guide you through setup, usage, and development.

---
# **Overview**
The aim of this project is to simplify and unify the processing of game data into various outputs for usage on PZwiki. By automating these tasks, the parser reduces manual effort and ensures consistent, accurate data across PZwiki pages.

# Installation
This guide will help you install the parser on your local machine.

## 1: Clone the Repository

To begin, clone the repository to your desired location using the following command:

```bash
git clone https://github.com/Vaileasys/pz-wiki_parser
```

## 2: Install Requirements
- **Python 3** *(built for 3.12)*

Additionally, several Python modules are required for some of the scripts to function. You can install them using the following methods:

1. **Using the provided script (windows)**:  
   Run the `install_requirements.bat` file for a quick installation of all dependencies.

2. **Using pip (automated)**:  
   * ```bash
      pip install -r requirements.txt

3. **Using pip (manual)**:
   * `pip install chardet`
   * `pip install tqdm`
   * `pip install lupa`
   * `pip install slpp`

---

# First Time Setup
After successfully installing the required dependencies, follow the instructions below to perform the initial setup.

## Setup

Once the requirements are installed, you can start the parser by either:

- Running the provided batch file:
  
    ```bash
  run.bat
    ```

- Or, manually running the script through your terminal:
  ```bash
  python main.py
  ```


### First Time Setup
When running the program for the first time, you will be prompted to perform the First Time Setup. This process will automatically populate the necessary files in the resources folder. Follow the on-screen prompts to complete this setup.

If the first time setup fails, you will have to add the resources manually by following [these](#Resources) steps

---

# Resources
These steps are only required if any of the first time set up failed.

### Scripts
1. Find your `scripts` folder in the media folder of your Project Zomboid install location.
2. Copy the entire `scripts` folder into the `resources` folder of this project.

### Lua
Add the following Lua files to `resources`, all are found within `ProjectZomboid\projectzomboid\media\lua\`:

1. `shared\Distributions.lua`
2. `shared\ProceduralDistributions.lua`
3. `shared\Foraging\forageDefinitions.lua`
4. `server\Vehicles\VehicleDistributions.lua`
5. `shared\Definitions\AttachedWeaponDefinitions.lua`

### Translations
You can get the translation files from [Project Zomboid Translations](https://github.com/TheIndieStone/ProjectZomboidTranslations/).

Download the entire folder and place it into the `resources` folder, naming it "Translate." Each language should be in its respective subfolder within the "Translate" folder.

Add the game's icons to a folder called "icons" (ensure 'Item_' prefix is removed). Icons can be extracted with TileZed. This is only relevant for some modules.

_`icons.csv` and `item_id_dictionary.csv` are included with the package. The latest version of `item_id_dictionary.csv` can be found [here](https://drive.google.com/file/d/1Gjl7WJMm7qYaJ5S_J2FtM1iTlyfLI-z8/view)._

---

# Configuration
The parser allows you to adjust various settings using the `config.ini` file, or through the program's [main menu](./Main Menu). Below are the details on how to configure and customize the parser.

The config file is managed by `config_manager.py`.


### Config File: `config.ini`

The main configuration file, `config.ini`, is located in the root directory of the project. This file contains various settings that control how the parser behaves. You can modify these settings directly in the file, or via the in-program menu.


### Modifying `config.ini`

To make changes to the `config.ini` file, open the file and adjust the values you need to change.

#### Settings
* `first_time_run`: This is an automatic flag that designates whether to show the first time setup.
* `default_language`: The default language the parser should use, you can still specify other languages when running modules.
* `version`: The version of your project zomboid installation, or resource files.
* `game_directory`: The root directory where the game is installed. This path should point to the folder containing the game executable.


# Usage

This program is bundled with a range of modules for various outputs. Most modules will **not** work if you try to run them directly.

## Instructions
1. Run `run.bat` (windows) or `main.py`.
2. Complete the first-time setup to get resources (scripts and translations).
3. Follow the menus to run the desired script.
4. Follow the prompts for that module.
5. The script will run, parsing the data, and then output. Most scripts will output to a file such as `output.txt` while others will just output to the terminal.

_Most scripts will prompt the user for a language code (default 'en') which is used to translate to the desired language. The translations must have been added to the "Translate" folder._


# **File Structure**
The parser follows a simple file structure. In the root folder is just `main.py`. The rest of the modules are in the `scripts` folder. The scripts folder contains most modules that can be run by the user.

```
pz-wiki_parser/
├── main.py
├── scripts/
│   ├── core/
│   └── parser/
├── output/
│   ├── distributions/
│   ├── codesnips/
│   ├── recorded_media/
│   ├── radio/
│   ├── logging/
│   └── language_code/
│       ├── consumables/
│       ├── fixing/
│       ├── infoboxes/
│       └── articles/
├── resources/
    ├── Translate/
    ├── icons/
    ├── lua/
    ├── radio/
    ├── scripts/
    ├── item_id_dictionary.csv
    └── icons.csv
```

---

## `Scripts/`
The scripts folder contains the main modules that can be executed or utilized by the parser. It is split into two subdirectories: core and parser.

`core/`: This directory contains the essential modules that form the backbone of the parser. These modules are not standalone and are used internally by other components to perform key operations such as configuration management, logging, and version control.

Modules in core:
* Handle configuration settings (config_manager).
* Provide utility functions and logging support.
* Ensure proper language translation through the `translate` module.

* `parser/`: This folder contains parser file parsers, which are used to create data files, and limited output.

---

## `Output/`
The `output` folder is where all the data generated by the parser is stored. The folder is organized into subdirectories, each representing a different type of output. This separation ensures that generated files are neatly categorized based on their purpose.

`distributions/`: Contains the output for the location (distribution) tables. 

`codesnips/`: Contains the codesnips for each parsed item.

`recorded_media/`: WIP.

`radio/`: Stores the output of the radio parser.

`logging/`: Stores log files created by the parser and its modules.

`language_code/`: Stores the subfolders for outputs in that language:

* `consumables/`: Contains generated tables for consumable items.
* `fixing/`: Contains fixing template outputs.
* `infoboxes/`: Stores generated infoboxes for wiki pages.
* `articles`/`: Contains complete wiki articles generated by the parser.

---

## `Resources/`
The resources folder contains essential data and files needed for the parser to function correctly. It includes translations, icons, Lua scripts, and radio transcripts, all of which are necessary for proper data generation and wiki integration. Instructions for setting up the resources folder can be found [here](./Getting-Started).

`Translate/`: This folder contains the translation files needed to localize the parser’s outputs. It allows the parser generate content in multiple languages, and lookup item names. This should be included in the setup.

`icons/`:  Stores the `.png` icons used by files.

`lua/`: Contains Lua scripts, from the game installation. This should be included in the setup.

`radio/`: Stores the radio data. This should be included in the setup.

`scripts/`: Contains the scripts parsed by the parser. This should be included in the setup.

`item_id_dictionary.csv`: A CSV file containing a list of items and their corresponding IDs currently on the wiki. This should be included in your repo. Otherwise, can be found [here](https://drive.google.com/file/d/1Gjl7WJMm7qYaJ5S_J2FtM1iTlyfLI-z8/view)

`icons.csv`: PLACEHOLDER
