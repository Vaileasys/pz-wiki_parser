import os, re, json
from scripts.parser import recipe_parser, literature_parser
from scripts.core import version, translate
import recipe_output, item_tags


def process_recipe(recipe, parsed_item_data):
    """
    Processes a recipe and returns a dictionary of its details.

    Args:
        recipe (dict): A dictionary containing the recipe details.
        parsed_item_data (dict): Parsed item data to aid in processing requirements.

    Returns:
        dict: A dictionary with the recipe's processed details.
    """
    if not isinstance(recipe, dict):
        print("Invalid recipe format: Expected a dictionary.")
        return None

    processed_data = {}

    # Process and store each field
    processed_data["name"] = process_name(recipe)
    processed_data["inputs"] = process_inputs(recipe)
    processed_data["outputs"] = process_outputs(recipe)
    processed_data["requirements"] = process_requirements(recipe, parsed_item_data)
    processed_data["workstation"] = process_workstation(recipe)
    processed_data["xp"] = process_xp(recipe)

    # Return the processed data
    return processed_data


def process_name(recipe):
    """
    Processes the 'name' field of the recipe to find the raw name and its translation.

    Args:
        recipe (dict): A dictionary containing the recipe details.

    Returns:
        tuple: A tuple containing the raw name and translated name, or (None, None) if the name field is not found.
    """
    # Check if 'name' exists in the recipe
    if "name" not in recipe or not isinstance(recipe["name"], str):
        print("No 'name' field found or 'name' is not a valid string.")
        return None, None

    raw_name = recipe["name"]
    translated_name = translate.get_translation(raw_name, property_key="TeachedRecipes")

    return raw_name, translated_name


def process_inputs(recipe):
    """
    Processes the 'inputs' field of the recipe into tools, ingredients, and energy.

    Args:
        recipe (dict): A dictionary containing the recipe details.

    Returns:
        dict: A dictionary with tools and ingredients processed from the inputs field.
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
                return {}  # If all items were excluded, return an empty dict

            return {
                tool_key: [
                    {
                        "raw_name": item,
                        "translated_name": translate.get_translation(item),
                    }
                    for item in filtered_items
                ]
            }

    for input_item in recipe[inputs_key]:
        # Skip the entire input item if "mapper" is found
        if any("mapper" in str(value).lower() for value in input_item.values()):
            continue

        # Before processing, remove excluded items from "items" if they exist
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
                            "translated_name": translate.get_translation(item),
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
                            "translated_name": translate.get_translation(item),
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
                        prefix_removed = item.replace("Base.", "", 1)  # Remove the first "Base."
                        amount, raw_name = prefix_removed.split(":", 1)
                        parsed_items.append({
                            "raw_name": raw_name.strip(),
                            "amount": int(amount.strip()),
                            "translated_name": translate.get_translation(raw_name.strip()),
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
                                "translated_name": translate.get_translation(item),
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
                            "translated_name": translate.get_translation(item),
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
                            "translated_name": translate.get_translation(item),
                        }
                        for item in input_item["items"]
                    ],
                    "flags": input_item.get("flags", []),
                    "amount": input_item.get("index", 1),
                }

    return processed_inputs


def process_outputs(recipe):
    """
    Processes the 'outputs' field of the recipe and returns a dictionary of outputs.

    Args:
        recipe (dict): A dictionary containing the recipe details.

    Returns:
        dict: A dictionary of processed outputs, with each output labeled as 'outputX',
              where X starts at 1. Each 'outputX' is itself a dictionary containing details
              about the product, including raw names, translated names, product numbers, or fluid data.
    """
    outputs_key = "outputs"
    if outputs_key not in recipe or not isinstance(recipe[outputs_key], list):
        print("No 'outputs' field found or 'outputs' is not a valid list.")
        return {}

    processed_outputs = {}
    output_index = 1  # Start numbering outputs from 1

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

        # Handle outputs with a 'mapper'
        if "mapper" in output:
            mapper_string = output["mapper"]
            processed_outputs[f"output{output_index}"] = process_output_mapper(recipe, mapper_string)
            output_index += 1
            continue

        # Handle outputs with a 'fluidModifier'
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

        # Handle normal outputs (non-fluid and non-mapper)
        if "items" in output and isinstance(output["items"], list):
            for raw_product in output["items"]:
                translated_product = translate.get_translation(raw_product)
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
    Processes the 'mapper' field in the 'outputs' field of the recipe.

    Args:
        recipe (dict): A dictionary containing the recipe details.
        mapper_string (str): The value of the 'mapper' field in the output.

    Returns:
        dict: A dictionary containing the processed output mapper details,
              including both raw and translated outputs, in the same order.
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
        "Amount": recipe.get("index", 1),  # Default index to 1 if not provided
        "RawOutputs": [],
        "TranslatedOutputs": [],
    }

    # Iterate over mapper keys and process them, excluding 'default'
    for key, target_raw_names in mapper_data.items():
        if key.lower() == "default":  # Skip the 'default' key
            continue

        # Use the key as the raw_item
        raw_items = [key]

        # Translate the key
        translated_items = [translate.get_translation(key.strip())]

        # Append the raw and translated names to the output lists
        output_mapper["RawOutputs"].append(raw_items)
        output_mapper["TranslatedOutputs"].append(translated_items)

    return output_mapper


def process_requirements(recipe, parsed_item_data):
    """
    Processes the 'requirements' field of the recipe, extracting required skills, books, schematics, and traits.

    Args:
        recipe (dict): A dictionary containing the recipe details.
        parsed_item_data (dict): The parsed item data from 'parsed_item_data.json'.

    Returns:
        dict: A dictionary containing processed requirements, including skills, books, schematics, and traits.
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
        translated_name = translate.get_translation(raw_name, property_key="TeachedRecipes")

        # Add to skillbooks based on teached recipes
        for item_name, item_details in parsed_item_data.items():
            if "TeachedRecipes" in item_details and raw_name in item_details["TeachedRecipes"]:
                translated_item_name = translate.get_translation(item_name)
                requirements["skillbooks"].append(translated_item_name)

        # Add to schematics based on parsed literature data
        try:
            with open("output/logging/parsed_literature_data.json", "r", encoding="utf-8") as file:
                literature_data = json.load(file)

            for schematic_list, recipe_names in literature_data.items():
                if raw_name in recipe_names:
                    requirements["schematics"].append(schematic_list)

        except FileNotFoundError:
            print("File not found: output/logging/parsed_literature_data.json")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in literature data: {e}")

        # Add to traits based on MainCreationMethods.lua
        try:
            with open("resources/lua/MainCreationMethods.lua", "r", encoding="utf-8") as file:
                lua_lines = file.readlines()

            for line in lua_lines:
                line = line.strip()
                if line.startswith("--"):  # Skip comments
                    continue
                # Match recipe name (raw or translated) as a whole string within quotes
                if re.search(rf'"{re.escape(raw_name)}"', line) or re.search(rf'"{re.escape(translated_name)}"', line):
                    if ":" in line:
                        # Extract trait name (string before the first ':')
                        trait = line.split(":")[0].strip()

                        # Check for TraitFactory.addTrait
                        trait_add_pattern = rf"local\s+{re.escape(trait)}\s*=\s*TraitFactory\.addTrait\("
                        for add_trait_line in lua_lines:
                            if re.search(trait_add_pattern, add_trait_line):
                                # Parse the getText string for translation
                                match = re.search(r'getText\("([^"]+)"\)', add_trait_line)
                                if match:
                                    text_key = match.group(1)
                                    if text_key.startswith("UI_trait_"):
                                        translation_key = text_key.replace("UI_trait_", "")
                                        translated_trait = translate.get_translation(
                                            translation_key, property_key="Trait"
                                        )
                                        if translated_trait not in requirements["traits"]:  # Avoid duplicates
                                            requirements["traits"].append(translated_trait)
                                break

        except FileNotFoundError:
            print("File not found: resources/lua/MainCreationMethods.lua")
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
    Processes the top-level 'Tags' field of the recipe to determine the workstation.

    Args:
        recipe (dict): A dictionary containing the recipe details.

    Returns:
        str: A string representing the workstation based on the tags, or an empty string if no relevant tags are found.
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
    Processes the 'xpAward' field of the recipe, separates strings and numbers,
    translates strings, and formats the output.

    Args:
        recipe (dict): A dictionary containing the recipe details.

    Returns:
        str: A formatted XP string if the 'xpAward' field is present, or "0" if absent or invalid.
    """
    if "xpAward" not in recipe:
        return "0"

    xp_award = recipe["xpAward"]

    if isinstance(xp_award, str) and ":" in xp_award:
        # Handle single string format
        string_part, value = xp_award.split(":", 1)
        translated_string = translate.get_translation(string_part.strip(), "Perks")
        return f"[[{translated_string}]] {value.strip()}"

    elif isinstance(xp_award, list):
        # Handle list format
        formatted_xp = []
        for entry in xp_award:
            if ":" in entry:
                string_part, value = entry.split(":", 1)
                translated_string = translate.get_translation(string_part.strip(), "Perks")
                formatted_xp.append(f"[[{translated_string}]] {value.strip()}")
        return "<br>".join(formatted_xp)

    return "0"


def main():
    language_code = translate.get_language_code()
    game_version = version.get_version()

    recipe_parser.main()
    literature_parser.init()
    item_tags.write_json_list()

    print("Parsers complete, please wait...")

    input_file = "output/recipes/recipes.json"
    parsed_item_file = "output/logging/parsed_item_data.json"
    output_file = "output/recipes/recipes_processed.json"

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    if "recipes" not in data or not isinstance(data["recipes"], list):
        print("Unexpected JSON structure: 'recipes' key not found or not a list.")
        return

    try:
        with open(parsed_item_file, "r", encoding="utf-8") as file:
            parsed_item_data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {parsed_item_file}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in parsed item data: {e}")
        return

    processed_recipes = {}

    for recipe in data["recipes"]:
        recipe_str = json.dumps(recipe)
        recipe_str = recipe_str.replace("Electricity", "Electrical")
        recipe = json.loads(recipe_str)

        processed = process_recipe(recipe, parsed_item_data)
        if processed and processed["name"][0]:
            recipe_name = processed["name"][0]
            processed_recipes[recipe_name] = processed

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(processed_recipes, f, ensure_ascii=False, indent=4)

    print(f"Processed recipes written to {output_file}")

    recipe_output.main()


if __name__ == "__main__":
    main()
