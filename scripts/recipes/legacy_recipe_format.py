#!/usr/bin/env python3
"""
Project Zomboid Wiki Legacy Recipe Formatter

This script processes raw recipe data into a structured format suitable for wiki
documentation. It handles the complex task of formatting various recipe components,
including inputs, outputs, requirements, and special cases like construction recipes.

The script handles:
- Recipe name translation and formatting
- Input processing (tools, ingredients, energy)
- Output processing with mappers
- Requirement formatting (skills, books, traits)
- Construction recipe special cases
- XP and workstation information
"""

import os
import re
import json
from tqdm import tqdm
from scripts.parser import literature_parser, item_parser
from scripts.recipes import legacy_recipe_parser
from scripts.core.version import Version
from scripts.core.language import Language, Translate
from scripts.core.constants import (PBAR_FORMAT, DATA_DIR)
from scripts.recipes import legacy_recipe_output
from scripts.utils import utility
from scripts.core.cache import save_cache, load_cache

processed_recipes = {}

def get_processed_recipes():
    """
    Get the processed recipe data, initializing if empty.

    Returns:
        dict: Dictionary of processed recipe data.

    This function serves as the main interface to access processed recipe data,
    ensuring the data is loaded before being accessed.
    """
    print("getting processed recipes")
    if not processed_recipes:
        main()
    return processed_recipes


def process_recipe(recipe, parsed_item_data):
    """
    Process a recipe into a structured format.

    Args:
        recipe (dict): Raw recipe data.
        parsed_item_data (dict): Parsed item data for reference.

    Returns:
        dict: Processed recipe data including:
            - name: Recipe name and translation
            - inputs: Tools and ingredients
            - outputs: Products and results
            - requirements: Skills, books, and traits
            - workstation: Required crafting location
            - xp: Experience gains
            - construction: Construction recipe flag
            - category: Recipe category

    Handles validation and proper formatting of all recipe components.
    """
    if not isinstance(recipe, dict):
        print("Invalid recipe format: Expected a dictionary.")
        return None

    processed_data = {}

    processed_data["name"] = process_name(recipe)
    processed_data["inputs"] = process_inputs(recipe)
    processed_data["outputs"] = process_outputs(recipe)
    processed_data["requirements"] = process_requirements(recipe, parsed_item_data)
    processed_data["workstation"] = process_workstation(recipe)
    processed_data["xp"] = process_xp(recipe)
    processed_data["construction"] = recipe.get("construction", False)

    if "category" in recipe:
        processed_data["category"] = recipe["category"]
    else:
        processed_data["category"] = "Other"

    return processed_data

def process_name(recipe):
    """
    Process recipe name and get its translation.

    Args:
        recipe (dict): Recipe data containing name field.

    Returns:
        tuple: (raw_name, translated_name) where:
            - raw_name: Original recipe name
            - translated_name: Translated version of the name
        Returns (None, None) if name is invalid.
    """
    if "name" not in recipe or not isinstance(recipe["name"], str):
        print("No 'name' field found or 'name' is not a valid string.")
        return None, None

    raw_name = recipe["name"]
    translated_name = Translate.get(raw_name, property_key="TeachedRecipes")

    return raw_name, translated_name


def process_inputs(recipe):
    """
    Process recipe inputs into structured format.

    Args:
        recipe (dict): Recipe data containing inputs field.

    Returns:
        dict: Processed inputs containing:
            - tools: Required tools with properties
            - ingredients: Required ingredients with amounts
            - energy: Energy requirements if any

    Handles:
    - Tool requirements and flags
    - Ingredient amounts and types
    - Fluid ingredients
    - Energy inputs
    - Numbered list inputs
    """
    inputs_key = "inputs"
    if inputs_key not in recipe or not isinstance(recipe[inputs_key], list):
        print("No 'inputs' field found or 'inputs' is not a valid list.")
        return {}

    processed_inputs = {"tools": {}, "ingredients": {}}
    tool_count = 0
    ingredient_count = 0

    # Always skip these items
    EXCLUDED_ITEMS = {"Base.bobOmb"}

    def safe_get_name(item):
        if item == "Any fluid container":
            return item
        try:
            return utility.get_name(item)
        except Exception:
            return item

    def process_tool(tool):
        """
        Processes a tool input and categorizes it as either tags or items.

        Args:
            tool (dict): A dictionary representing a tool input.

        Returns:
            dict: A dictionary representing the processed tool.
        """
        nonlocal tool_count

        # Skip if "mapper" is found in the tool
        if any("mapper" in str(value).lower() for value in tool.values()):
            return {}

        tool_count += 1
        tool_key = f"tool{tool_count}"

        if "tags" in tool:
            return {
                f"{tool_key}_tags": tool["tags"],
                f"{tool_key}_flags": tool.get("flags", []),
            }
        elif "items" in tool:
            # Filter out excluded items from the tools
            filtered_items = [item for item in tool["items"] if item not in EXCLUDED_ITEMS]
            if not filtered_items:
                return {}

            return {
                tool_key: [
                    {
                        "raw_name": item,
                        "translated_name": safe_get_name(item),
                    }
                    for item in filtered_items
                ]
            }

    for input_item in recipe[inputs_key]:
        # Skip the entire input item if "mapper" is found
        if any("mapper" in str(value).lower() for value in input_item.values()):
            continue

        if "items" in input_item and isinstance(input_item["items"], list):
            input_item["items"] = [
                i for i in input_item["items"] if i not in EXCLUDED_ITEMS
            ]

        if input_item.get("mode") == "Keep":
            if "fluidModifier" in input_item and isinstance(input_item["fluidModifier"], dict):
                ingredient_count += 1
                ingredient_key = f"ingredient{ingredient_count}"
                fluid_modifier = input_item["fluidModifier"]
                processed_inputs["ingredients"][ingredient_key] = {
                    "fluid": True,
                    "amount": fluid_modifier.get("amount", 1),
                    "fluidType": fluid_modifier.get("fluidType", []),
                    "items": [
                        {
                            "raw_name": item,
                            "translated_name": safe_get_name(item),
                        }
                        for item in input_item.get("items", [])
                    ],
                    "flags": input_item.get("flags", []),
                }
            else:
                tool_data = process_tool(input_item)
                if tool_data:
                    processed_inputs["tools"].update(tool_data)
        else:
            ingredient_count += 1
            ingredient_key = f"ingredient{ingredient_count}"

            # Handle energy inputs
            if input_item.get("energy", False):
                processed_inputs["ingredients"][ingredient_key] = {
                    "energy": True,
                    "amount": input_item.get("amount", 0),
                    "type": input_item.get("type", "Unknown"),
                    "modifiers": input_item.get("modifiers", ""),
                }

            elif input_item.get("fluidModifier") and isinstance(input_item["fluidModifier"], dict):
                fluid_modifier = input_item["fluidModifier"]
                processed_inputs["ingredients"][ingredient_key] = {
                    "fluid": True,
                    "amount": fluid_modifier.get("amount", 1),
                    "fluidType": fluid_modifier.get("fluidType", []),
                    "items": [
                        {
                            "raw_name": item,
                            "translated_name": safe_get_name(item),
                        }
                        for item in input_item.get("items", [])
                    ],
                    "flags": input_item.get("flags", []),
                }

            # Handle numbered list inputs
            elif "items" in input_item and isinstance(input_item["items"], list):
                numbered_list = False
                parsed_items = []

                for item in input_item["items"]:
                    if ":" in item:
                        numbered_list = True
                        prefix_removed = item.replace("Base.", "", 1)
                        amount, raw_name = prefix_removed.split(":", 1)
                        parsed_items.append({
                            "raw_name": raw_name.strip(),
                            "amount": int(amount.strip()),
                            "translated_name": safe_get_name(raw_name.strip()),
                        })

                if numbered_list:
                    processed_inputs["ingredients"][ingredient_key] = {
                        "numbered_list": True,
                        "items": parsed_items,
                        "flags": input_item.get("flags", []),
                        "index": input_item.get("index", 1),
                    }
                else:
                    processed_inputs["ingredients"][ingredient_key] = {
                        "items": [
                            {
                                "raw_name": item,
                                "translated_name": safe_get_name(item),
                            }
                            for item in input_item["items"]
                        ],
                        "flags": input_item.get("flags", []),
                        "index": input_item.get("index", 1),
                    }

            # Handle other fluid inputs
            elif input_item.get("fluid", False):
                processed_inputs["ingredients"][ingredient_key] = {
                    "fluid": True,
                    "amount": input_item["amount"],
                    "items": [
                        {
                            "raw_name": item,
                            "translated_name": safe_get_name(item),
                        }
                        for item in input_item.get("items", [])
                    ],
                    "flags": input_item.get("flags", []),
                }

            # Handle tagged inputs
            elif "tags" in input_item:
                processed_inputs["ingredients"][ingredient_key] = {
                    "tags": input_item["tags"],
                    "flags": input_item.get("flags", []),
                    "amount": input_item.get("index", 1),
                }

            # Handle item lists
            elif "items" in input_item:
                processed_inputs["ingredients"][ingredient_key] = {
                    "items": [
                        {
                            "raw_name": item,
                            "translated_name": safe_get_name(item),
                        }
                        for item in input_item["items"]
                    ],
                    "flags": input_item.get("flags", []),
                    "amount": input_item.get("index", 1),
                }

    return processed_inputs


def construction_output(outputs, recipe):
    """
    Process construction recipe outputs.

    Args:
        outputs (list): List of output items.
        recipe (dict): Full recipe data.

    Returns:
        list: Processed construction outputs with:
            - Sprite information
            - Icon details
            - Item properties
    """
    processed_outputs = {}
    output_index = 1

    # Helper function to recursively search for the first valid value.
    def find_first_value(obj):
        if isinstance(obj, (str, int, float)):
            return obj
        elif isinstance(obj, dict):
            for value in obj.values():
                result = find_first_value(value)
                if result is not None:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = find_first_value(item)
                if result is not None:
                    return result
        return None

    # Determine candidate sprite icon from spriteOutputs if available.
    sprite_icon = None
    if "spriteOutputs" in recipe:
        sprite_icon = find_first_value(recipe["spriteOutputs"])

    if outputs:
        for output in outputs:
            new_output = {}
            if "displayName" in output:
                translated = Translate.get(output["displayName"])
                new_output["translated_product"] = translated
            if "icon" in output:
                new_output["icon"] = output["icon"]
            elif sprite_icon is not None:
                new_output["icon"] = sprite_icon

            if not new_output:
                new_output = output
            processed_outputs[f"output{output_index}"] = new_output
            output_index += 1
    else:
        if "name" in recipe:
            translated_name = Translate.get(recipe["name"], property_key="TeachedRecipes")
        else:
            translated_name = ""
        new_output = {"translated_product": translated_name}
        if sprite_icon is not None:
            new_output["icon"] = sprite_icon
        processed_outputs[f"output{output_index}"] = new_output

    return {"outputs": processed_outputs}


def process_outputs(recipe):
    """
    Process recipe outputs into structured format.

    Args:
        recipe (dict): Recipe data containing outputs.

    Returns:
        dict: Processed outputs containing:
            - Standard outputs with amounts
            - Construction outputs if applicable
            - Mapper-based outputs
            - Fluid outputs
    """
    outputs_key = "outputs"
    if outputs_key not in recipe or not isinstance(recipe[outputs_key], list):
        print("No 'outputs' field found or 'outputs' is not a valid list.")
        return {}

    if recipe.get("construction", False):
        return construction_output(recipe[outputs_key], recipe)

    processed_outputs = {}
    output_index = 1

    for output in recipe[outputs_key]:
        # Handle energy outputs
        if output.get("energy", False):
            processed_outputs[f"output{output_index}"] = {
                "energy": True,
                "amount": output.get("amount", 0),
                "type": output.get("type", "Unknown"),
                "modifiers": output.get("modifiers", ""),
            }
            output_index += 1
            continue

        # Handle outputs with mapper
        if "mapper" in output:
            mapper_string = output["mapper"]
            processed_outputs[f"output{output_index}"] = process_output_mapper(recipe, mapper_string)
            output_index += 1
            continue

        # Handle outputs with a fluidModifier
        fluid_modifier = output.get("fluidModifier")
        if fluid_modifier and isinstance(fluid_modifier, dict):
            processed_outputs[f"output{output_index}"] = {
                "fluid": True,
                "amount": fluid_modifier.get("amount", 1),
                "fluidType": fluid_modifier.get("fluidType", []),
                "tags": output.get("tags", []),
                "flags": output.get("flags", []),
            }
            output_index += 1
            continue

        # Handle item outputs
        if "items" in output and isinstance(output["items"], list):
            for raw_product in output["items"]:
                translated_product = utility.get_name(raw_product)
                product_number = output.get("index", None)  # Retrieve the 'index' field if present

                # Create a dictionary for this output
                processed_outputs[f"output{output_index}"] = {
                    "raw_product": raw_product,
                    "translated_product": translated_product,
                    "products_number": product_number,
                }
                output_index += 1
        else:
            print(f"Unexpected format for output: {output}")

    return {"outputs": processed_outputs}


def process_output_mapper(recipe, mapper_string):
    """
    Process output mapper strings into structured format.

    Args:
        recipe (dict): Recipe data.
        mapper_string (str): Mapper string to process.

    Returns:
        dict: Processed mapper data with:
            - Mapped items
            - Item properties
            - Amounts
    """
    # Check if 'itemMappers' exists in the recipe
    if "itemMappers" not in recipe or not isinstance(recipe["itemMappers"], dict):
        print(f"'itemMappers' not found or invalid in recipe: {mapper_string}")
        return {"mapper": False}

    item_mappers = recipe["itemMappers"]

    # Check if the specified mapper exists in 'itemMappers'
    if mapper_string not in item_mappers:
        print(f"Mapper '{mapper_string}' not found in 'itemMappers'.")
        return {"mapper": False}

    mapper_data = item_mappers[mapper_string]

    if not isinstance(mapper_data, dict):
        print(f"Invalid format for mapper '{mapper_string}' in 'itemMappers'.")
        return {"mapper": False}

    # Build the output dictionary, including both raw and translated outputs
    output_mapper = {
        "mapper": True,
        "Amount": recipe.get("index", 1),
        "RawOutputs": [],
        "TranslatedOutputs": [],
    }

    # Iterate over mapper keys and process them, excluding 'default'
    for key, target_raw_names in mapper_data.items():
        if key.lower() == "default":
            continue

        raw_items = [key]
        translated_items = [utility.get_name(key.strip())]
        output_mapper["RawOutputs"].append(raw_items)
        output_mapper["TranslatedOutputs"].append(translated_items)

    return output_mapper


def process_requirements(recipe, parsed_item_data):
    """
    Process recipe requirements into structured format.

    Args:
        recipe (dict): Recipe data.
        parsed_item_data (dict): Reference item data.

    Returns:
        dict: Processed requirements including:
            - Required skills and levels
            - Required books or literature
            - Required traits
            - Auto-learn conditions
            - Schematic requirements
    """
    requirements = {
        "skillrequired": {},
        "skillbooks": [],
        "autolearn": {},
        "schematics": [],
        "traits": [],
    }

    # Check for 'NeedToBeLearn'
    if recipe.get("NeedToBeLearn") == "True":
        requirements["NeedToBeLearn"] = True

    # Process 'SkillRequired'
    if "SkillRequired" in recipe:
        skill_required = recipe["SkillRequired"]

        if isinstance(skill_required, str):
            skill, level = skill_required.split(":")
            requirements["skillrequired"][skill.strip()] = int(level.strip())

        elif isinstance(skill_required, list):
            for skill_entry in skill_required:
                skill, level = skill_entry.split(":")
                requirements["skillrequired"][skill.strip()] = int(level.strip())

    # Check for "name" to process books, schematics, and traits
    if "name" in recipe:
        raw_name = recipe["name"]
        translated_name = Translate.get(raw_name, property_key="TeachedRecipes")

        # Add to skillbooks based on teached recipes
        for item_name, item_details in parsed_item_data.items():
            if "TeachedRecipes" in item_details and raw_name in item_details["TeachedRecipes"]:
                translated_item_name = utility.get_name(item_name)
                requirements["skillbooks"].append(translated_item_name)

        # Add schematics based on parsed literature data
        
        try:
            literature_data = literature_parser.get_literature_data()

            # Access the nested SpecialLootSpawns structure
            special_loot_spawns = literature_data.get("SpecialLootSpawns", {})
            for schematic_category, schematic_list in special_loot_spawns.items():
                if raw_name in schematic_list:
                    if "schematics" not in requirements:
                        requirements["schematics"] = []
                    requirements["schematics"].append(schematic_category)
        except Exception as e:
            print(f"Error adding schematics from parsed literature data: {e}")

        # Add to traits based on MainCreationMethods.lua
        try:
            with open(os.path.join("resources", "lua", "MainCreationMethods.lua"), "r", encoding="utf-8") as file:
                lua_lines = file.readlines()

            for line in lua_lines:
                line = line.strip()
                if line.startswith("--"):
                    continue
                # Match recipe name as a whole string within quotes
                if re.search(rf'"{re.escape(raw_name)}"', line) or re.search(rf'"{re.escape(translated_name)}"', line):
                    if ":" in line:
                        trait = line.split(":")[0].strip()
                        trait_add_pattern = rf"local\s+{re.escape(trait)}\s*=\s*TraitFactory\.addTrait\("
                        for add_trait_line in lua_lines:
                            if re.search(trait_add_pattern, add_trait_line):
                                match = re.search(r'getText\("([^"]+)"\)', add_trait_line)
                                if match:
                                    text_key = match.group(1)
                                    if text_key.startswith("UI_trait_"):
                                        translation_key = text_key.replace("UI_trait_", "")
                                        translated_trait = Translate.get(
                                            translation_key, property_key="Trait"
                                        )
                                        if translated_trait not in requirements["traits"]:  # Avoid duplicates
                                            requirements["traits"].append(translated_trait)
                                break

        except FileNotFoundError:
            print("File not found:", os.path.join("resources", "lua", "MainCreationMethods.lua"))
        except Exception as e:
            print(f"Error processing MainCreationMethods.lua: {e}")

    # Process 'AutoLearn'
    if "AutoLearnAll" in recipe:
        auto_learn = recipe["AutoLearnAll"]

        if isinstance(auto_learn, str):
            skill, level = auto_learn.split(":")
            requirements["autolearn"][skill.strip()] = int(level.strip())

        elif isinstance(auto_learn, list):
            for auto_entry in auto_learn:
                skill, level = auto_entry.split(":")
                requirements["autolearn"][skill.strip()] = int(level.strip())

    return requirements


def process_workstation(recipe):
    """
    Process workstation requirements.

    Args:
        recipe (dict): Recipe data.

    Returns:
        str: Formatted workstation requirement,
             or empty string if no workstation needed.
    """
    tags_key = next((key for key in recipe if key.lower() == "tags" and not isinstance(recipe[key], (dict, list))), None)

    if not tags_key:
        return ""

    # Extract tags and ensure it's a list
    tags = recipe[tags_key]
    if isinstance(tags, str):
        tags = [tags]
    elif not isinstance(tags, list):
        print(f"Unexpected format for 'Tags': {tags}")
        return ""

    workstation_mapping = {
        "anysurfacecraft": "Any surface",
        "choppingblock": "Chopping block",
        "grindstone": "Grindstone",
        "grinding_slab": "Grinding Slab",
        "weaving": "Loom",
        "stone_mill": "Stone Mill",
        "stone_quern": "Stone Quern",
        "churnbucket": "Butter Churn",
        "dryleatherlarge": "Large Drying Rack",
        "dryleathermedium": "Medium Drying Rack",
        "dryleathersmall": "Small Drying Rack",
        "tanleather": "Tanning Barrel",
        "advancedforge": "Advanced Forge",
        "dryingrackgrain": "Drying Rack (Grain)",
        "dryingrackherb": "DryingRack (Herb)",
        "forge": "Forge",
        "furnace": "Furnace",
        "metalbandsaw": "Metal Bandsaw",
        "potterywheel": "Pottery Wheel",
        "potterybench": "Pottery Bench",
        "primitiveforge": "Primitive Forge",
        "primitivefurnace": "Primitive Furnace",
        "removeflesh": "Softening Beam",
        "removefur": "Softening Beam",
        "spinningwheel": "Spinning Wheel",
        "standingdrillpress": "Standing Drill Press",
        "whetstone": "Whetstone",
        "toaster": "Toaster"
    }

    for tag in tags:
        normalized_tag = tag.lower()
        if normalized_tag in workstation_mapping:
            workstation_string = workstation_mapping[normalized_tag]
            return workstation_string

    return ""


def process_xp(recipe):
    """
    Process experience gain information.

    Args:
        recipe (dict): Recipe data.

    Returns:
        str: Formatted XP gain information,
             or "0" if no XP is gained.
    """
    if "xpAward" not in recipe:
        return "0"

    xp_award = recipe["xpAward"]

    if isinstance(xp_award, str) and ":" in xp_award:
        string_part, value = xp_award.split(":", 1)
        if string_part == "WoodWork":
            string_part = string_part.capitalize()
        translated_string = Translate.get(string_part.strip(), "Perk")
        return f"[[{translated_string}]] {value.strip()}"

    elif isinstance(xp_award, list):
        formatted_xp = []
        for entry in xp_award:
            if ":" in entry:
                string_part, value = entry.split(":", 1)
                translated_string = Translate.get(string_part.strip(), "Perk")
                formatted_xp.append(f"[[{translated_string}]] {value.strip()}")
        return "<br>".join(formatted_xp)

    return "0"


def main():
    """
    Main execution function for recipe formatting.

    This function:
    1. Loads necessary data from parsers
    2. Processes all recipes into structured format
    3. Handles construction recipes
    4. Saves processed data to cache
    5. Returns processed recipe data
    """
    global processed_recipes
    language_code = Language.get()
    game_version = Version.get()

    #pre-load data
    try:
        parser_name = "item"
        parsed_item_data = item_parser.get_item_data()
        parser_name = "literature"
        literature_parser.get_literature_data()
    except Exception as e:
        print(f"Error getting {parser_name} data: {e}")
        return

    print("Parsers complete, please wait...")

    CACHE_FILE = "recipes_processed_data.json"
    cache_file = os.path.join(DATA_DIR, CACHE_FILE)

    # Try to load data from cache
    processed_recipes, cache_version = load_cache(cache_file, "processed recipe", get_version=True)

    # If cache version is old, we generate new data
    if cache_version != game_version:
        data = legacy_recipe_parser.get_recipe_data()

        if "recipes" not in data or not isinstance(data["recipes"], list):
            print("Unexpected JSON structure: 'recipes' key not found or not a list.")
            return

        with tqdm(total=len(data["recipes"]), desc="Processing recipes", bar_format=PBAR_FORMAT, unit=" recipes") as pbar:
            for recipe in data["recipes"]:
                pbar.set_postfix_str(f'Processing: {recipe["name"][:30]}')
                recipe_str = json.dumps(recipe)
                recipe_str = recipe_str.replace("Electricity", "Electrical")
                recipe = json.loads(recipe_str)

                processed = process_recipe(recipe, parsed_item_data)
                if processed and processed["name"][0]:
                    recipe_name = processed["name"][0]
                    processed_recipes[recipe_name] = processed
                pbar.update(1)
            
            pbar.bar_format = f"Recipes processed."

        save_cache(processed_recipes, CACHE_FILE)

    legacy_recipe_output.main(processed_recipes)


if __name__ == "__main__":
    main()
