#!/usr/bin/env python3
"""
Project Zomboid Wiki Legacy Recipe Output Generator

This script processes parsed recipe data and generates formatted wiki markup for
recipe pages. It handles various recipe components including ingredients, tools,
skills, and products, converting them into properly formatted wiki templates.

The script handles:
- Ingredient processing with icons and amounts
- Tool requirements with conditions and flags
- Recipe learning methods (books, traits, etc.)
- Product outputs with quantities
- XP gains and workstation requirements
- Item usage tracking and documentation
- Lua table generation for wiki templates
"""

import os
import re
import json
from collections import defaultdict
from scripts.items import item_tags
from scripts.recipes import legacy_recipe_format
from scripts.parser import fluid_parser
from scripts.core.language import Translate
from scripts.utils import utility, util


def process_ingredients(data):
    """
    Process recipe ingredients and format them for wiki display.

    Args:
        data (dict): Recipe data containing ingredient information.

    Returns:
        str: Formatted wiki markup for ingredients section.

    Handles:
    - Tag-based ingredients with icons
    - Fluid ingredients with colors
    - Numbered list ingredients
    - Standard ingredients with amounts
    - Proper grouping of "One of" vs "Each of" items
    """
    if (
        "inputs" not in data or
        "ingredients" not in data["inputs"] or
        not data["inputs"]["ingredients"]
    ):
        return "ingredients=''none''"

    ingredients_data = data["inputs"]["ingredients"]
    parsed_ingredients = []

    for key, ingredient_info in ingredients_data.items():
        # Tag-based ingredients
        if "tags" in ingredient_info and ingredient_info["tags"]:
            tag_list = ingredient_info["tags"]
            amount = ingredient_info.get("amount", 1)
            tag_strings = []
            for tag in tag_list:
                tag_file = os.path.join("output", "en", "tags", "cycle-img", f"{tag}.txt")
                with open (tag_file, "r") as file:
                    tag_span = file.read()
                tag_strings.append(f"{tag_span} [[{tag} (tag)]] <small>×{amount}</small>")
            final_tag_str = "<br>".join(tag_strings)
            parsed_ingredients.append(("tag", final_tag_str, "Each of"))

        # Fluid-based ingredients
        elif "fluid" in ingredient_info and ingredient_info["fluid"] is True:
            fluid_types = ingredient_info.get("fluidType", [])
            amount = ingredient_info.get("amount", 1)
            items = ingredient_info.get("items", [])
            translated_name = items[0].get("translated_name", "Any fluid container") if items else "Any fluid container"

            fluid_strings = []
            for fluid_id in fluid_types:
                fluid_info = fluid_rgb(fluid_id)
                display_name = fluid_info["name"]
                R, G, B = fluid_info["R"], fluid_info["G"], fluid_info["B"]

                fluid_strings.append(
                    f"{{{{rgb|{R}, {G}, {B}}}}} [[{display_name} (fluid)|{display_name}]] <small>×{int(amount*1000)}mL</small>"
                )
            final_fluid_str = "<br>".join(fluid_strings)
            descriptor = "One of" if len(fluid_types) > 1 else "Each of"
            parsed_ingredients.append(("fluid", final_fluid_str, descriptor))

        # Numbered list ingredients
        elif ingredient_info.get("numbered_list", False):
            numbered_items = ingredient_info["items"]
            numbered_strings = []
            for item in numbered_items:
                amount = item.get("amount", 1)
                item_id = item.get("raw_name", "Unknown Item")
                name = utility.get_name(item_id)
                page = utility.get_page(item_id, name)
                link = util.link(page, name)
                if item_id != "Any fluid container":
                    try:
                        icon = utility.get_icon(item_id) if item_id else "Question_On.png"
                        if isinstance(icon, list):
                            icon = icon[0] if icon else "Question_On.png"
                    except Exception as e:
                        print(f"Error fetching icon for raw_name '{item_id}': {e}")
                        icon = "Question_On.png"
                else:
                    icon = "Question_On.png"

                numbered_strings.append(
                    f"[[File:{icon}|32x32px|class=pixelart]] {link} <small>×{amount}</small>"
                )
            final_numbered_str = "<br>".join(numbered_strings)
            parsed_ingredients.append(("item", final_numbered_str, "One of"))

        # Standard ingredients
        elif "items" in ingredient_info and ingredient_info["items"]:
            item_list = ingredient_info["items"]
            amount = ingredient_info.get("index", 1)
            item_strings = []

            for item in item_list:
                item_id = item.get("raw_name", "Unknown Item")
                name = utility.get_name(item_id)
                page = utility.get_page(item_id, name)
                link = util.link(page, name)
                if item_id != "Any fluid container":
                    try:
                        icon = utility.get_icon(item_id) if item_id else "Question_On.png"
                        if isinstance(icon, list):
                            icon = icon[0] if icon else "Question_On.png"
                    except Exception as e:
                        print(f"Error fetching icon for raw_name '{item_id}': {e}")
                        icon = "Question_On.png"
                else:
                    icon = "Question_On.png"

                item_strings.append(f"[[File:{icon}|32x32px|class=pixelart]] {link} <small>×{amount}</small>")
            final_item_str = "<br>".join(item_strings)
            descriptor = "One of" if len(item_list) > 1 else "Each of"
            parsed_ingredients.append(("item", final_item_str, descriptor))

        else:
            parsed_ingredients.append(("item", "Unknown Ingredient", "One of"))

    final_ingredients_str = "ingredients="
    added_something = False
    last_descriptor = None

    for ingredient_type, ingredient_str, descriptor in parsed_ingredients:
        # Add the descriptor only if it hasn't already been added
        if descriptor != last_descriptor or not (ingredient_type == "fluid" and descriptor == "Each of"):
            if added_something:
                final_ingredients_str += "<br>"
            final_ingredients_str += f"<small>{descriptor}:</small><br>"
            last_descriptor = descriptor
            added_something = False
        if added_something:
            final_ingredients_str += "<br>"

        final_ingredients_str += ingredient_str
        added_something = True

    return final_ingredients_str


def process_tools(data):
    """
    Process tool requirements and format them for wiki display.

    Args:
        data (dict): Recipe data containing tool requirements.

    Returns:
        str: Formatted wiki markup for tools section.

    Handles:
    - Individual tool requirements
    - Tool tag groups
    - Tool condition flags
    - Proper grouping of "One of" vs "Each of" tools
    - Icon integration for tools
    """
    tools_data = data.get("inputs", {}).get("../tools", {})
    if not tools_data:
        return "tools=''none''"

    each_of_parts = []
    one_of_parts = []

    flag_mapping = {
        'IsDamaged': "damaged",
        'IsNotDull': "not dull",
        'MayDegrade': "may degrade",
        'MayDegradeHeavy': "may degrade",
        'MayDegradeLight': "may degrade",
        'NoBrokenItems': "not broken"
    }

    # Process tools
    for key, value in tools_data.items():
        if key.startswith("tool") and not key.endswith("_tags") and not key.endswith("_flags"):
            # Handle individual tools
            for tool in value:
                item_id = tool.get("raw_name", "Unknown Item")

                if item_id.startswith("Base.*"):
                    name = "Any fluid container"
                else:
                    name = utility.get_name(item_id)

                page = utility.get_page(item_id, name)
                link = util.link(page, name)
                try:
                    icon = utility.get_icon(item_id) if item_id else "Question_On.png"
                    if isinstance(icon, list):
                        icon = icon[0] if icon else "Question_On.png"
                except Exception as e:
                    print(f"Error fetching icon for raw_name '{item_id}': {e}")
                    icon = "Question_On.png"

                tool_entry = f"[[File:{icon}|32x32px|class=pixelart]] {link}"
                each_of_parts.append(tool_entry + "<br>")
        elif key.endswith("_tags"):
            # Handle tagged groups
            tool_flags = tools_data.get(f"{key[:-5]}_flags", [])
            list_parts = []
            for tag in value:
                tag_file = os.path.join("output", "en", "tags", "cycle-img", f"{tag}.txt")
                with open(tag_file, "r") as file:
                    tag_span = file.read()
                tag_entry = f"{tag_span} [[{tag} (tag)]]"
                if tool_flags:
                    flag_desc = [flag_mapping.get(flag, flag) for flag in tool_flags if flag in flag_mapping]
                    if flag_desc:
                        flags_html = f"<span style='color:var(--color-pz-subtle)'>({', '.join(flag_desc)})</span>"
                        tag_entry += f"<br>{flags_html}"
                list_parts.append(tag_entry + "<br>")
            one_of_parts.append("<small>One of:</small><br>" + "".join(list_parts))

    result = "tools="
    if each_of_parts:
        result += "<small>Each of:</small><br>" + "".join(each_of_parts)
    if one_of_parts:
        result += "".join(one_of_parts)

    return result


def process_recipes(data):
    """
    Process recipe learning methods and format them for wiki display.

    Args:
        data (dict): Recipe data containing learning requirements.

    Returns:
        str: Formatted wiki markup for recipe learning section.

    Handles:
    - Skillbook requirements
    - Auto-learn conditions
    - Schematic requirements
    - Trait requirements
    - Proper formatting with alternatives
    """
    SCHEMATIC = {
        "ExplosiveSchematics": ["Schematic (explosive)"],
        "MeleeWeaponSchematics": ["Schematic (melee weapon)"],
        "BSToolsSchematics": ["Tools Schematic"],
        "ArmorSchematics": ["Schematic (armor)"],
        "CookwareSchematic": ["Cookware Schematic"],
        "FoodRecipes": ["Recipe"]
    }

    skillbooks = data.get("requirements", {}).get("skillbooks", [])
    autolearn = data.get("requirements", {}).get("autolearn", {})
    schematics = data.get("requirements", {}).get("schematics", [])
    traits = data.get("requirements", {}).get("traits", [])

    if not (skillbooks or autolearn or schematics or traits):
        return "recipes=''none''"

    recipe_parts = ["recipes="]

    # Process skillbooks
    if skillbooks:
        for i, book in enumerate(skillbooks):
            if i == 0:
                recipe_parts.append(f"[[{book}]]")
            else:
                recipe_parts.append("<br><small>or</small><br>")
                recipe_parts.append(f"[[{book}]]")

    # Process schematics
    if schematics:
        if skillbooks:
            recipe_parts.append("<br><small>Schematics:</small><br>")
        else:
            recipe_parts.append("<small>Schematics:</small><br>")

        for i, schematic in enumerate(schematics):
            translated = SCHEMATIC.get(schematic, [schematic])
            for value in translated:
                if i > 0:
                    recipe_parts.append("<br><small>or</small><br>")
                recipe_parts.append(f"[[{value}]]")

    # Process traits
    if traits:
        if skillbooks or schematics:
            recipe_parts.append("<br><small>Traits:</small><br>")
        else:
            recipe_parts.append("<small>Traits:</small><br>")

        for i, trait in enumerate(traits):
            if i > 0:
                recipe_parts.append("<br>")
            recipe_parts.append(f"[[{trait}]]")

    # Process autolearn
    if autolearn:
        if skillbooks or schematics or traits:
            recipe_parts.append("<br><small>Auto-learnt at:</small><br>")
        else:
            recipe_parts.append("<small>Auto-learnt at:</small><br>")

        for i, (key, value) in enumerate(autolearn.items()):
            if i > 0:
                recipe_parts.append("<br><small>and</small><br>")
            translated_key = Translate.get(key, "Perk")
            recipe_parts.append(f"[[{translated_key}]] {value}")

    return "".join(recipe_parts)


def process_skills(data):
    """
    Process skill requirements and format them for wiki display.

    Args:
        data (dict): Recipe data containing skill requirements.

    Returns:
        str: Formatted wiki markup for skills section.

    Handles:
    - Skill level requirements
    - Multiple skill combinations
    - Proper formatting with alternatives
    """
    skills_data = data.get("requirements", {}).get("skillrequired", {})
    if not skills_data:
        return "skills=''none''"

    skills_list = []
    for skill, level in skills_data.items():
        skill = Translate.get(skill, "Perk")
        skills_list.append(f"[[{skill}]] {level}")

    skills_str = "<br><small>and</small><br>".join(skills_list)
    return f"skills={skills_str}"


def process_workstation(data):
    """
    Process workstation requirements and format them for wiki display.

    Args:
        data (dict): Recipe data containing workstation information.

    Returns:
        str: Formatted wiki markup for workstation section.

    Handles:
    - Required crafting stations
    - Special location requirements
    - Proper formatting with alternatives
    """
    if "workstation" in data and data["workstation"].strip():
        if data['workstation'] == "Any surface":
            return f"workstation=''{data['workstation']}''"
        else:
            return f"workstation=[[{data['workstation']}]]"
    return "workstation=''none''"


def process_products(data):
    """
    Process recipe products and format them for wiki display.

    Args:
        data (dict): Recipe data containing product information.

    Returns:
        str: Formatted wiki markup for products section.

    Handles:
    - Standard product outputs
    - Fluid outputs
    - Product amounts and variations
    - Icon integration for products
    """
    construction = data.get("construction", False)
    names = data.get("name", [])
    translated_name = names[1] if len(names) > 1 else "Unknown Recipe"
    products_str = f"products=<small>''{translated_name}''</small><br>"

    outputs_data = data.get("outputs", {}).get("outputs", {})
    if not outputs_data:
        return products_str + "''none''"

    items_section = []
    mappers_section = []
    energy_section = []

    # Construction
    for key, output_info in outputs_data.items():
        if construction:
            icon = output_info.get("icon")

            translated_product = output_info.get("translated_product", translated_name)
            products_number = output_info.get("products_number", 1)

            if icon.startswith("Item_",):
                icon = icon[len("Item_"):]
                size = "64x64px"
            elif icon.startswith("Build_",):
                size = "96x96px"
            else:
                size = "64x128px"

            items_section.append(
                f"[[File:{icon}.png|{size}|class=pixelart]]<br>[[{translated_product}]] ×{products_number}"
            )

        # Standard
        elif "raw_product" in output_info and "translated_product" in output_info:
            item_id = output_info.get("raw_product")
            name = utility.get_name(item_id)
            page = utility.get_page(item_id, name)
            link = util.link(page, name)

            products_number = output_info.get("products_number", 1)
            if item_id:
                try:
                    icon = utility.get_icon(item_id) if item_id else "Question_On.png"
                    if isinstance(icon, list):
                        icon = icon[0] if icon else "Question_On.png"
                except Exception as e:
                    print(f"Error fetching icon for ID '{item_id}': {e}")
                    icon = "Question_On.png"
            else:
                try:
                    icon = output_info.get("icon", "Question_On.png")
                except Exception as e:
                    print(f"Error fetching icon for product: {e}")
                    icon = "Question_On.png"
            items_section.append(
                f"[[File:{icon}|64x64px|class=pixelart]]<br>{link} ×{products_number}"
            )

        elif output_info.get("mapper"):
            raw_outputs = output_info.get("RawOutputs", [])
            translated_outputs = output_info.get("TranslatedOutputs", [])
            amount = output_info.get("Amount", 1)
            mapper_lines = []

            for raw_output_group, translated_output_group in zip(raw_outputs, translated_outputs):
                if isinstance(raw_output_group, list):
                    # Nested list format
                    for raw_output, translated_output in zip(raw_output_group, translated_output_group):
                        item_id = raw_output
                        name = utility.get_name(item_id)
                        page = utility.get_page(item_id, name)
                        link = util.link(page, name)
                        try:
                            icon = utility.get_icon(raw_output) if raw_output else "Question_On.png"
                            if isinstance(icon, list):
                                icon = icon[0] if icon else "Question_On.png"
                        except Exception as e:
                            print(f"Error fetching icon for mapper product '{raw_output}': {e}")
                            icon = "Question_On.png"

                        mapper_lines.append(
                            f"[[File:{icon}|64x64px|class=pixelart]]<br>{link} ×{amount}"
                        )
                else:
                    try:
                        icon = utility.get_icon(raw_output_group) if raw_output_group else "Question_On.png"
                        if isinstance(icon, list):
                            icon = icon[0] if icon else "Question_On.png"
                    except Exception as e:
                        print(f"Error fetching icon for mapper product '{raw_output_group}': {e}")
                        icon = "Question_On.png"
                    mapper_lines.append(
                        f"[[File:{icon}|64x64px|class=pixelart]]<br>[[{translated_output_group}]] ×{amount}"
                    )

            mapper_str = "<br>".join(mapper_lines)

            if key == "output1":
                mappers_section.append(
                    f"<small>(Products are dependent on inputs)<br>One of:</small><br>{mapper_str}"
                )
            else:
                mappers_section.append(
                    f"<br><small>(Products are dependent on inputs)<br>Each of:</small><br>{mapper_str}"
                )

        elif output_info.get("energy"):
            energy_type = output_info.get("type", "Unknown")
            amount = output_info.get("amount", 0)
            energy_section.append(f"[[{energy_type} energy]] ×{amount}")

    if items_section:
        if len(items_section) == 1:
            products_str += items_section[0]
        else:
            products_str += "<small>Each of:</small><br>" + "<br>".join(items_section)

    if mappers_section:
        if items_section:
            products_str += "<br>"
        products_str += "".join(mappers_section)

    if energy_section:
        if items_section or mappers_section:
            products_str += "<br>"
        products_str += "<br>".join(energy_section)

    return products_str if products_str else "products=<small>''none''</small><br>"


def process_xp(data):
    """
    Process experience gains and format them for wiki display.

    Args:
        data (dict): Recipe data containing XP information.

    Returns:
        str: Formatted wiki markup for XP section.

    Handles:
    - XP amounts per skill
    - Multiple skill XP gains
    - Proper formatting with amounts
    """
    if "xp" in data:
        if data['xp'] == "0":
            return "xp=''0''"
        else:
            return f"xp={data['xp']}"
    return ""


def fluid_rgb(fluid_id):
    """
    Get RGB color values for a fluid type.

    Args:
        fluid_id (str): Identifier for the fluid.

    Returns:
        dict: Dictionary containing:
            - name: Display name of the fluid
            - R: Red color value
            - G: Green color value
            - B: Blue color value

    Handles proper color mapping for all fluid types.
    """
    try:
        fluid_data = fluid_parser.get_fluid_data().get(fluid_id)
        if not fluid_data:
            raise ValueError(f"No fluid found for ID: {fluid_id}")

        with open(os.path.join("resources", "color_reference.json"), "r") as f:
            color_reference = json.load(f)

        name = utility.get_fluid_name(fluid_data)

        if fluid_id == "TaintedWater":
            tainted_water = Translate.get("ItemNameTaintedWater", 'IGUI')
            name = tainted_water.replace("%1", name)

        color_ref = fluid_data.get('ColorReference')
        numeric_color = fluid_data.get('Color', [0.0, 0.0, 0.0])

        if color_ref:
            if isinstance(color_ref, str):
                rgb_values = color_reference["colors"].get(color_ref, [0.0, 0.0, 0.0])
            elif isinstance(color_ref, list) and len(color_ref) == 1 and isinstance(color_ref[0], str):
                rgb_values = color_reference["colors"].get(color_ref[0], [0.0, 0.0, 0.0])
            else:
                rgb_values = numeric_color
        else:
            rgb_values = numeric_color

        R = int(float(rgb_values[0]) * 255)
        G = int(float(rgb_values[1]) * 255)
        B = int(float(rgb_values[2]) * 255)

        return {
            "name": name,
            "R": R,
            "G": G,
            "B": B
        }

    except Exception as e:
        raise RuntimeError(f"Error processing fluid '{fluid_id}': {e}")


def gather_item_usage(recipes_data, tags_data):
    """
    Gather information about how items are used in recipes.

    Args:
        recipes_data (dict): Dictionary of all recipe data.
        tags_data (dict): Dictionary of item tag data.

    Returns:
        tuple: Four dictionaries mapping items to their recipe usage:
            - Normal recipe inputs
            - Normal recipe outputs
            - Construction recipe inputs
            - Construction recipe outputs

    Tracks both direct item usage and tag-based usage.
    """
    normal_item_input_map = defaultdict(set)
    normal_item_output_map = defaultdict(set)
    construction_item_input_map = defaultdict(set)
    construction_item_output_map = defaultdict(set)

    for recipe_name, recipe in recipes_data.items():
        is_construction = recipe.get("construction", False)
        inputs = recipe.get("inputs", {})

        # Process Ingredients
        ingredients = inputs.get("ingredients", {})
        for _, ingredient_info in ingredients.items():
            if "items" in ingredient_info:
                for item_dict in ingredient_info["items"]:
                    raw = item_dict.get("raw_name")
                    if raw and raw != "Any fluid container":
                        if is_construction:
                            construction_item_input_map[raw].add(recipe_name)
                        else:
                            normal_item_input_map[raw].add(recipe_name)
            elif "tags" in ingredient_info and ingredient_info["tags"]:
                # Tag-based ingredients
                for tag in ingredient_info["tags"]:
                    if tag in tags_data:
                        for item in tags_data[tag]:
                            raw = item.get("item_id")
                            if raw:
                                if is_construction:
                                    construction_item_input_map[raw].add(recipe_name)
                                else:
                                    normal_item_input_map[raw].add(recipe_name)
            elif "numbered_list" in ingredient_info and ingredient_info["numbered_list"]:
                numbered_items = ingredient_info.get("items", [])
                for item_dict in numbered_items:
                    raw = item_dict.get("raw_name")
                    if raw and raw != "Any fluid container":
                        if is_construction:
                            construction_item_input_map[raw].add(recipe_name)
                        else:
                            normal_item_input_map[raw].add(recipe_name)

        # Process Tools
        tools = inputs.get("tools", {})
        for key, tool_info in tools.items():
            if key.endswith("_tags") and isinstance(tool_info, list):
                # Handle tag-based tools
                for tag in tool_info:
                    if tag in tags_data:
                        for item in tags_data[tag]:
                            raw = item.get("item_id")
                            if raw:
                                if is_construction:
                                    construction_item_input_map[raw].add(recipe_name)
                                else:
                                    normal_item_input_map[raw].add(recipe_name)
            elif key.endswith("_flags"):
                pass
            elif isinstance(tool_info, dict):
                if "items" in tool_info:
                    for item_dict in tool_info["items"]:
                        raw = item_dict.get("raw_name")
                        if raw:
                            if is_construction:
                                construction_item_input_map[raw].add(recipe_name)
                            else:
                                normal_item_input_map[raw].add(recipe_name)
                elif "tags" in tool_info and tool_info["tags"]:
                    for tag in tool_info["tags"]:
                        if tag in tags_data:
                            for item in tags_data[tag]:
                                raw = item.get("item_id")
                                if raw:
                                    if is_construction:
                                        construction_item_input_map[raw].add(recipe_name)
                                    else:
                                        normal_item_input_map[raw].add(recipe_name)
                elif "numbered_list" in tool_info and tool_info["numbered_list"]:
                    numbered_items = tool_info.get("items", [])
                    for item_dict in numbered_items:
                        raw = item_dict.get("raw_name")
                        if raw:
                            if is_construction:
                                construction_item_input_map[raw].add(recipe_name)
                            else:
                                normal_item_input_map[raw].add(recipe_name)

        # Process Outputs
        outputs = recipe.get("outputs", {}).get("outputs", {})
        for _, output_info in outputs.items():
            if "raw_product" in output_info:
                raw_output = output_info["raw_product"]
                if raw_output:
                    if is_construction:
                        construction_item_output_map[raw_output].add(recipe_name)
                    else:
                        normal_item_output_map[raw_output].add(recipe_name)
            elif output_info.get("mapper"):
                raw_outputs = output_info.get("RawOutputs", [])
                for entry in raw_outputs:
                    if isinstance(entry, list):
                        for raw in entry:
                            if raw:
                                if is_construction:
                                    construction_item_output_map[raw].add(recipe_name)
                                else:
                                    normal_item_output_map[raw].add(recipe_name)
                    else:
                        if entry:
                            if is_construction:
                                construction_item_output_map[entry].add(recipe_name)
                            else:
                                normal_item_output_map[entry].add(recipe_name)

    return normal_item_input_map, normal_item_output_map, construction_item_input_map, construction_item_output_map


def output_item_usage(normal_item_input_map, normal_item_output_map, construction_item_input_map, construction_item_output_map):
    """
    Generate wiki markup for item usage in recipes.

    Args:
        normal_item_input_map (dict): Items used as inputs in normal recipes.
        normal_item_output_map (dict): Items produced as outputs in normal recipes.
        construction_item_input_map (dict): Items used as inputs in construction recipes.
        construction_item_output_map (dict): Items produced as outputs in construction recipes.

    Creates individual files documenting how each item is used in recipes,
    both as ingredients and as products.
    """
    # Process non-construction items
    combined_output_dir_normal = os.path.join("output", "recipes", "crafting_combined")
    individual_dir_normal = os.path.join("output", "recipes", "crafting")
    os.makedirs(combined_output_dir_normal, exist_ok=True)
    os.makedirs(individual_dir_normal, exist_ok=True)

    all_normal_items = sorted(set(normal_item_input_map.keys()) | set(normal_item_output_map.keys()))
    for raw_name in all_normal_items:
        output_recipes = sorted(normal_item_output_map[raw_name])
        input_recipes = sorted(normal_item_input_map[raw_name])
        if output_recipes:
            crafting_id = f"{raw_name}_howtocraft"
            crafting_template = ["{{Crafting/sandbox|item=" + crafting_id]
            for recipe in output_recipes:
                crafting_template.append(f"|{recipe}")
            crafting_template.append("}}")
            combined_file = os.path.join(combined_output_dir_normal, f"{raw_name}.txt")
            with open(combined_file, 'w', encoding='utf-8') as f:
                f.write("===How it's made===\n")
                f.write("\n".join(crafting_template) + "\n\n")
            individual_file = os.path.join(individual_dir_normal, f"{crafting_id}.txt")
            with open(individual_file, 'w', encoding='utf-8') as craft_file:
                craft_file.write("\n".join(crafting_template))
        if input_recipes:
            crafting_id = f"{raw_name}_whatitcrafts"
            crafting_template = ["{{Crafting/sandbox|item=" + crafting_id]
            for recipe in input_recipes:
                crafting_template.append(f"|{recipe}")
            crafting_template.append("}}")
            combined_file = os.path.join(combined_output_dir_normal, f"{raw_name}.txt")
            with open(combined_file, 'a', encoding='utf-8') as f:
                f.write("===What it makes===\n")
                f.write("\n".join(crafting_template) + "\n")
            individual_file = os.path.join(individual_dir_normal, f"{crafting_id}.txt")
            with open(individual_file, 'w', encoding='utf-8') as craft_file:
                craft_file.write("\n".join(crafting_template))

    # Process construction items
    combined_output_dir_construction = os.path.join("output", "recipes", "construction_crafting_combined")
    individual_dir_construction = os.path.join("output", "recipes", "construction_crafting")
    os.makedirs(combined_output_dir_construction, exist_ok=True)
    os.makedirs(individual_dir_construction, exist_ok=True)

    all_construction_items = sorted(set(construction_item_input_map.keys()) | set(construction_item_output_map.keys()))
    for raw_name in all_construction_items:
        output_recipes = sorted(construction_item_output_map[raw_name])
        input_recipes = sorted(construction_item_input_map[raw_name])
        if output_recipes:
            crafting_id = f"{raw_name}_constructionhowtomake"
            crafting_template = ["{{Building|item=" + crafting_id]
            for recipe in output_recipes:
                crafting_template.append(f"|{recipe}")
            crafting_template.append("}}")
            combined_file = os.path.join(combined_output_dir_construction, f"{raw_name}.txt")
            with open(combined_file, 'w', encoding='utf-8') as f:
                f.write("===How it's made===\n")
                f.write("\n".join(crafting_template) + "\n\n")
            individual_file = os.path.join(individual_dir_construction, f"{crafting_id}.txt")
            with open(individual_file, 'w', encoding='utf-8') as craft_file:
                craft_file.write("\n".join(crafting_template))
        if input_recipes:
            crafting_id = f"{raw_name}_constructionwhatitcrafts"
            crafting_template = ["{{Building|item=" + crafting_id]
            for recipe in input_recipes:
                crafting_template.append(f"|{recipe}")
            crafting_template.append("}}")
            combined_file = os.path.join(combined_output_dir_construction, f"{raw_name}.txt")
            with open(combined_file, 'a', encoding='utf-8') as f:
                f.write("===What it makes===\n")
                f.write("\n".join(crafting_template) + "\n")
            individual_file = os.path.join(individual_dir_construction, f"{crafting_id}.txt")
            with open(individual_file, 'w', encoding='utf-8') as craft_file:
                craft_file.write("\n".join(crafting_template))


def output_skill_usage(recipes_data):
    """
    Generate wiki markup for skill usage in recipes.

    Args:
        recipes_data (dict): Dictionary of all recipe data.

    Creates files documenting which recipes require each skill
    and what level of skill is needed.
    """
    skills_output_dir = os.path.join("output", "recipes", "skills")
    os.makedirs(skills_output_dir, exist_ok=True)

    # Mapping for specific skills
    skill_mapping = {
        "Woodwork": "Carpentry",
        "MetalWelding": "Welding",
        "FlintKnapping": "Knapping",
        "Blacksmith": "Metalworking",
    }

    crafting_skill_map = defaultdict(set)
    building_skill_map = defaultdict(set)

    for recipe_name, recipe in recipes_data.items():
        is_building = recipe.get("construction", False)

        xp_val = recipe.get("xp", "0")
        if xp_val != "0" and xp_val:
            # Extract skills inside double square brackets
            skills_in_xp = re.findall(r'\[\[(.*?)\]\]', xp_val)
            for skill in skills_in_xp:
                final_skill = skill_mapping.get(skill, skill)
                if is_building:
                    building_skill_map[final_skill].add(recipe_name)
                else:
                    crafting_skill_map[final_skill].add(recipe_name)

        skill_required = recipe.get("requirements", {}).get("skillrequired", {})
        for skill in skill_required.keys():
            final_skill = skill_mapping.get(skill, skill)
            if is_building:
                building_skill_map[final_skill].add(recipe_name)
            else:
                crafting_skill_map[final_skill].add(recipe_name)

    # Output files for crafting recipes using the {{Crafting/sandbox template
    for skill, recipes in crafting_skill_map.items():
        filename = os.path.join(skills_output_dir, f"{skill}_crafting.txt")
        template_lines = [f"{{{{Crafting/sandbox|ID={skill}_crafting"]
        for recipe in sorted(recipes):
            template_lines.append(f"|{recipe}")
        template_lines.append("}}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(template_lines))

    # Output files for building recipes using the {{Building template
    for skill, recipes in building_skill_map.items():
        filename = os.path.join(skills_output_dir, f"{skill}_building.txt")
        template_lines = [f"{{{{Building|ID={skill}_building"]
        for recipe in sorted(recipes):
            template_lines.append(f"|{recipe}")
        template_lines.append("}}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(template_lines))


def strip_prefix(text, prefix):
    """
    Remove a prefix from text if it exists.

    Args:
        text (str): Text to process.
        prefix (str): Prefix to remove.

    Returns:
        str: Text with prefix removed if it existed, original text otherwise.
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def output_lua_tables(processed_recipes):
    """
    Generate Lua tables for recipe data.

    Args:
        processed_recipes (dict): Dictionary of processed recipe data.

    Creates Lua table files that can be used by wiki templates
    to display recipe information.
    """
    output_dir = os.path.join("output", "recipes")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join("output", "recipes", "data_files"), exist_ok=True)

    # Separate recipes into crafting and building recipes.
    crafting_recipes = {}
    building_recipes = {}
    for raw_name, recipe_data in processed_recipes.items():
        if recipe_data.get("construction", False):
            building_recipes[raw_name] = recipe_data
        else:
            crafting_recipes[raw_name] = recipe_data

    # Group crafting recipes by their category (from JSON)
    crafting_by_category = {}
    for raw_name, recipe_data in crafting_recipes.items():
        json_category = recipe_data.get("category")
        if not json_category:
            json_category = "Other"
        category_key = json_category.lower()
        if category_key not in crafting_by_category:
            crafting_by_category[category_key] = {}
        crafting_by_category[category_key][raw_name] = recipe_data

    # Write each category's crafting recipes to its own file.
    for category_key, recipes in crafting_by_category.items():
        file_name = f"{output_dir}/data_files/{category_key}_data.lua"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"-- Module:Crafting/{category_key}_data\n\n")
            f.write(f"local {category_key} = {{\n")
            for raw_name, recipe_data in recipes.items():
                key = raw_name.lower()
                ingredients = strip_prefix(recipe_data["ingredients"], "ingredients=")
                tools = strip_prefix(recipe_data["tools"], "tools=")
                recipes_str = strip_prefix(recipe_data["recipes"], "recipes=")
                skills = strip_prefix(recipe_data["skills"], "skills=")
                workstation = strip_prefix(recipe_data["workstation"], "workstation=")
                xp = strip_prefix(recipe_data["xp"], "xp=")
                product = strip_prefix(recipe_data["products"], "products=")

                recipe_block = (
                    f"  {key} = {{\n"
                    f"    ingredients = [=[{ingredients}]=],\n"
                    f"    tools       = [=[{tools}]=],\n"
                    f"    recipes     = [=[{recipes_str}]=],\n"
                    f"    skills      = [=[{skills}]=],\n"
                    f"    workstation = [=[{workstation}]=],\n"
                    f"    xp          = [=[{xp}]=],\n"
                    f"    product     = [=[{product}]=]\n"
                    f"  }},\n"
                )
                f.write(recipe_block)
            f.write("}\n\n")
            f.write(f"return {category_key}\n")

    # Write the building recipes to a single file.
    building_output_file = f"{output_dir}/data_files/building_data.lua"
    with open(building_output_file, 'w', encoding='utf-8') as f:
        f.write("-- Module:Crafting/building_data\n\n")
        f.write("local buildingList = {\n")
        for raw_name, recipe_data in building_recipes.items():
            key = raw_name.lower()
            ingredients = strip_prefix(recipe_data["ingredients"], "ingredients=")
            tools = strip_prefix(recipe_data["tools"], "tools=")
            recipes_str = strip_prefix(recipe_data["recipes"], "recipes=")
            skills = strip_prefix(recipe_data["skills"], "skills=")
            workstation = strip_prefix(recipe_data["workstation"], "workstation=")
            xp = strip_prefix(recipe_data["xp"], "xp=")
            product = strip_prefix(recipe_data["products"], "products=")

            recipe_block = (
                f"  {key} = {{\n"
                f"    ingredients = [=[{ingredients}]=],\n"
                f"    tools       = [=[{tools}]=],\n"
                f"    recipes     = [=[{recipes_str}]=],\n"
                f"    skills      = [=[{skills}]=],\n"
                f"    workstation = [=[{workstation}]=],\n"
                f"    xp          = [=[{xp}]=],\n"
                f"    product     = [=[{product}]=]\n"
                f"  }},\n"
            )
            f.write(recipe_block)
        f.write("}\n\n")
        f.write("return buildingList\n")

    # Build the index table mapping table names to the recipes they contain.
    index_table = {}
    for category_key, recipes in crafting_by_category.items():
        index_table[category_key] = sorted(recipes.keys())
    index_table["building"] = sorted(building_recipes.keys())

    # Write the index table to a Lua file.
    index_file = f"{output_dir}/index.lua"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("local index = {\n")
        for table_name, recipe_list in index_table.items():
            recipes_str = ", ".join(f'"{r}"' for r in recipe_list)
            f.write(f"  {table_name} = {{ {recipes_str} }},\n")
        f.write("}\n\n")
        f.write("return index\n")


def main(recipes_data=None):
    """
    Main execution function for recipe output generation.

    Args:
        recipes_data (dict, optional): Pre-loaded recipe data.
            If None, data will be loaded from cache.

    This function:
    1. Loads or uses provided recipe data
    2. Processes all recipes into wiki format
    3. Generates item usage documentation
    4. Creates skill usage documentation
    5. Outputs Lua tables for templates
    """
    print("Processing recipe output...")
    if not recipes_data:
        recipes_data = legacy_recipe_format.get_processed_recipes()
    tags_data = item_tags.get_tag_data()
    item_tags.write_tag_image()

    processed_recipes = {}
    for raw_name, recipe in recipes_data.items():
        ingredients = process_ingredients(recipe)
        tools = process_tools(recipe)
        recipes = process_recipes(recipe)
        skills = process_skills(recipe)
        workstation = process_workstation(recipe)
        products = process_products(recipe)
        xp = process_xp(recipe)
        construction_flag = recipe.get("construction", False)

        processed_recipes[raw_name] = {
            "ingredients": ingredients,
            "tools": tools,
            "recipes": recipes,
            "skills": skills,
            "workstation": workstation,
            "products": products,
            "xp": xp,
            "construction": construction_flag,
            "category": recipe.get("category", "Other")
        }

    normal_item_input_map, normal_item_output_map, construction_item_input_map, construction_item_output_map = gather_item_usage(
        recipes_data, tags_data)
    output_item_usage(normal_item_input_map, normal_item_output_map, construction_item_input_map,
                      construction_item_output_map)
    output_skill_usage(recipes_data)
    output_lua_tables(processed_recipes)


if __name__ == "__main__":
    main()
