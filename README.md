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
   * `pip install tqdm`
   * `pip install lupa`
   * `pip install pillow`

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
The resources directory contains resources used by various scripts, such as custom translations, wiki page dictionary, and more.

Useful resources not specific to this project include:
* `texture_names.json`: A dictionary of the game's texture names, including item icons and build icons. _Updated with the **Update textures** tool script._
* `page_dictionary.json`: A dictionary of each wiki page with the IDs and categories on them.
* `item_keys.json`: A list of each item's `ItemKey` declaration from `ItemKey.class`. _Updated with the **Item key parser** tool script._

---

# Configuration
The parser allows you to adjust various settings using the `config.ini` file, or through the program's [main menu](./Main Menu). Below are the details on how to configure and customize the parser.

The config file is managed by `config.py`.


### Config File: `config.ini`

The main configuration file, `config.ini`, is located in the root directory of the project. This file contains various settings that control how the parser behaves. You can modify these settings directly in the file, or via the in-program menu.


### Modifying `config.ini`

To make changes to the `config.ini` file, open the file and adjust the values you need to change.

#### Settings
* `first_time_run`: This is an automatic flag that designates whether to show the first time setup.
* `default_language`: The default language the parser should use, you can still specify other languages when running modules.
* `version`: The version of your project zomboid installation, or resource files.
* `game_directory`: The root directory where the game is installed. This path should point to the folder containing the game executable.
* `debug_mode`: Whether to show debug messages in the terminal.


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
│   ├── codesnips/
│   ├── distributions/
│   ├── recorded_media/
│   ├── logging/
│   └── language_code/
│       ├── fluid/
│       ├── item/
│       ├── tiles/
│       └── vehicle/
└── resources/
    ├── icons/
    ├── tables/
    ├── lua/
    ├── radio/
    ├── Translate/
    ├── color_reference.json
    └── icons.csv
    ├── page_dictionary.json
    └── texture_names.json
```

---

## `Scripts/`
The scripts folder contains the main modules that can be executed or utilized by the parser. There are three main subdirectories: core, parser, utils and objects.

`core/`: This directory contains the essential modules that form the backbone of the parser. These modules are not standalone and are used internally by other components to perform key operations such as configuration management, logging, and version control.

Modules in core:
* Handle configuration settings (config).
* Provide logging support.
* Ensure proper language translation through the `translate` module.

* `parser/`: This folder contains parser file parsers, which are used to create data files, and limited output.

* `utils/`: Contains general-purpose helper functions and utilities used to support common tasks.

* `objects/`: Defines structured classes that represent parsed game data, providing clean access to item properties, recipes, and other in-game concepts.

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

`icons/`:  Stores the `.png` icons used by the icon update tool.

`lua/`: Contains Lua scripts, from the game installation. This should be included in the setup.

`radio/`: Stores the radio data. This should be included in the setup.

`scripts/`: Contains the txt scripts parsed by the parser. This should be included in the setup.

`tables/`: Contains the table maps for the various list scripts. This should be included in your repo.

`color_reference`: A JSON file containing RGB color references, taken from Colors.class in the game's files. This should be included in your repo.

`icons.csv`: A CSV file containing custom icon maps. These icons use RGB tints in-game.

`page_dictionary.json`: A JSON file containing a list of items and their corresponding IDs currently on the wiki. This should be included in your repo.

`texture_names.json`: A map of textures from the game's files. Used as a reference for various scripts and checking for new textures upon each game release. This should be included in your repo.
