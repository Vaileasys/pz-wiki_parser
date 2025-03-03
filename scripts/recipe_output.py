import os
import json
from collections import defaultdict
from scripts import item_tags, recipe_format
from scripts.parser import fluid_parser
from scripts.core import translate, utility


def process_ingredients(data):
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
                tag_strings.append(f"{{{{Tag_{tag}}}}} [[{tag} (tag)]] <small>×{amount}</small>")
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
                link = utility.format_link(name, page)
                if item_id != "Any fluid container":
                    try:
                        icon = utility.get_icon(item_id) if item_id else "Question On.png"
                        if isinstance(icon, list):
                            icon = icon[0] if icon else "Question On.png"
                    except Exception as e:
                        print(f"Error fetching icon for raw_name '{item_id}': {e}")
                        icon = "Question On.png"
                else:
                    icon = "Question On.png"

                numbered_strings.append(
                    f"[[file:{icon}|32x32px|class=pixelart]] {link} <small>×{amount}</small>"
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
                link = utility.format_link(name, page)
                if item_id != "Any fluid container":
                    try:
                        icon = utility.get_icon(item_id) if item_id else "Question On.png"
                        if isinstance(icon, list):
                            icon = icon[0] if icon else "Question On.png"
                    except Exception as e:
                        print(f"Error fetching icon for raw_name '{item_id}': {e}")
                        icon = "Question On.png"
                else:
                    icon = "Question On.png"

                item_strings.append(f"[[file:{icon}|32x32px|class=pixelart]] {link} <small>×{amount}</small>")
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
    Process the 'tools' field from the data and format it, including icons and sorting 'each of' items to the top.

    Args:
        data (dict): The recipe data containing tool requirements.

    Returns:
        str: A formatted string representing the tools and their conditions.
    """
    tools_data = data.get("inputs", {}).get("tools", {})
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
                name = utility.get_name(item_id)
                page = utility.get_page(item_id, name)
                link = utility.format_link(name, page)
                try:
                    icon = utility.get_icon(item_id) if item_id else "Question On.png"
                    if isinstance(icon, list):
                        icon = icon[0] if icon else "Question On.png"
                except Exception as e:
                    print(f"Error fetching icon for raw_name '{item_id}': {e}")
                    icon = "Question On.png"

                tool_entry = f"[[file:{icon}|32x32px|class=pixelart]] {link}"
                each_of_parts.append(tool_entry + "<br>")
        elif key.endswith("_tags"):

            # Handle tagged groups
            tool_flags = tools_data.get(f"{key[:-5]}_flags", [])
            list_parts = []
            for tag in value:
                tag_entry = f"{{{{Tag_{tag}}}}} [[{tag} (tag)]]"
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
    Process the 'skillbooks', 'autolearn', 'schematics', and 'traits' fields from the data and format them.

    Args:
        data (dict): The recipe data containing skillbooks, autolearn, schematics, and traits information.

    Returns:
        str: A formatted string representing the recipes and their conditions.
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
            translated_key = translate.get_translation(key, "Perk")
            recipe_parts.append(f"[[{translated_key}]] {value}")

    return "".join(recipe_parts)


def process_skills(data):
    """
    Process the 'skillrequired' field from the data and format it.

    Args:
        data (dict): The recipe data containing skill requirements.

    Returns:
        str: A formatted string representing the skills and their levels.
    """
    skills_data = data.get("requirements", {}).get("skillrequired", {})
    if not skills_data:
        return "skills=''none''"

    skills_list = []
    for skill, level in skills_data.items():
        skill = translate.get_translation(skill, "Perk")
        skills_list.append(f"[[{skill}]] {level}")

    skills_str = "<br><small>and</small><br>".join(skills_list)
    return f"skills={skills_str}"


def process_workstation(data):
    if "workstation" in data and data["workstation"].strip():
        if data['workstation'] == "Any surface":
            return f"workstation=''{data['workstation']}''"
        else:
            return f"workstation=[[{data['workstation']}]]"
    return "workstation=''none''"


def process_products(data):
    """
    Processes the 'outputs' field from the data and formats it, including icons for item products and mapper objects.

    For construction recipes:
      - If an "icon" field exists, that image is used.
      - Otherwise, the code falls back to searching the (potentially nested) "spriteOutputs" structure
        for the first sprite value.
      - If the resulting icon name starts with "Item_", the prefix is removed and the icon is rendered at 64x64.
      - Otherwise, it is rendered at 96x96.

    For non-construction recipes, standard processing is applied.
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
                f"[[file:{icon}.png|{size}|class=pixelart]]<br>[[{translated_product}]] ×{products_number}"
            )

        # Standard
        elif "raw_product" in output_info and "translated_product" in output_info:
            item_id = output_info.get("raw_product")
            name = utility.get_name(item_id)
            page = utility.get_page(item_id, name)
            link = utility.format_link(name, page)

            products_number = output_info.get("products_number", 1)
            if item_id:
                try:
                    icon = utility.get_icon(item_id) if item_id else "Question On.png"
                    if isinstance(icon, list):
                        icon = icon[0] if icon else "Question On.png"
                except Exception as e:
                    print(f"Error fetching icon for ID '{item_id}': {e}")
                    icon = "Question On.png"
            else:
                try:
                    icon = output_info.get("icon", "Question On.png")
                except Exception as e:
                    print(f"Error fetching icon for product: {e}")
                    icon = "Question On.png"
            items_section.append(
                f"[[file:{icon}|64x64px|class=pixelart]]<br>{link} ×{products_number}"
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
                        link = utility.format_link(name, page)
                        try:
                            icon = utility.get_icon(raw_output) if raw_output else "Question On.png"
                            if isinstance(icon, list):
                                icon = icon[0] if icon else "Question On.png"
                        except Exception as e:
                            print(f"Error fetching icon for mapper product '{raw_output}': {e}")
                            icon = "Question On.png"

                        mapper_lines.append(
                            f"[[file:{icon}|64x64px|class=pixelart]]<br>{link} ×{amount}"
                        )
                else:
                    try:
                        icon = utility.get_icon(raw_output_group) if raw_output_group else "Question On.png"
                        if isinstance(icon, list):
                            icon = icon[0] if icon else "Question On.png"
                    except Exception as e:
                        print(f"Error fetching icon for mapper product '{raw_output_group}': {e}")
                        icon = "Question On.png"
                    mapper_lines.append(
                        f"[[file:{icon}|64x64px|class=pixelart]]<br>[[{translated_output_group}]] ×{amount}"
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
    if "xp" in data:
        if data['xp'] == "0":
            return "xp=''0''"
        else:
            return f"xp={data['xp']}"
    return ""


def fluid_rgb(fluid_id):
    """
    Retrieve the name and RGB values of a fluid based on its ID.

    Args:
        fluid_id (str): The ID of the fluid to process.

    Returns:
        dict: A dictionary containing the fluid name and RGB values as separate keys.
    """
    try:
        fluid_data = fluid_parser.get_fluid_data().get(fluid_id)
        if not fluid_data:
            raise ValueError(f"No fluid found for ID: {fluid_id}")

        with open("resources/color_reference.json", "r") as f:
            color_reference = json.load(f)

        name = utility.get_fluid_name(fluid_data)

        if fluid_id == "TaintedWater":
            tainted_water = translate.get_translation("ItemNameTaintedWater", 'IGUI')
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
    For each item (by its raw name), collect the set of recipe names in which
    it appears as an input and the set of recipe names in which it appears as an output.
    Tag-based ingredients and tools are processed separately for regular and construction recipes.
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
    Outputs combined files and individual recipe files for item usage, separated by type.

    - Non-construction combined files are saved in output/recipes/crafting_combined/.
    - Non-construction individual recipe files are saved in output/recipes/crafting/.
    - Construction combined files are saved in output/recipes/construction_crafting_combined/.
    - Construction individual recipe files are saved in output/recipes/construction_crafting/.
    """
    # Process non-construction items
    combined_output_dir_normal = 'output/recipes/crafting_combined/'
    individual_dir_normal = 'output/recipes/crafting/'
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
    combined_output_dir_construction = 'output/recipes/construction_crafting_combined/'
    individual_dir_construction = 'output/recipes/construction_crafting/'
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


def output(processed_recipes):
    """
    Outputs the processed recipes to individual files and two combined files in the specified format,
    ensuring all files are encoded in UTF-8.
    """
    # Output individual recipe files separated by type
    for raw_name, recipe_data in processed_recipes.items():
        if recipe_data.get("construction", False):
            output_dir = 'output/recipes/construction_recipes_seperate/'
        else:
            output_dir = 'output/recipes/recipes_seperate/'
        os.makedirs(output_dir, exist_ok=True)

        ingredients = recipe_data["ingredients"]
        tools = recipe_data["tools"]
        recipes = recipe_data["recipes"]
        skills = recipe_data["skills"]
        workstation = recipe_data["workstation"]
        products = recipe_data["products"]
        xp = recipe_data["xp"]

        output_file = os.path.join(output_dir, f'{raw_name}.txt')
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(f"|{raw_name.lower()}= \n")
            out_file.write("    {{Recipe/sandbox\n")
            out_file.write(f"        |{ingredients}\n")
            out_file.write(f"        |{tools}\n")
            out_file.write(f"        |{recipes}\n")
            out_file.write(f"        |{skills}\n")
            out_file.write(f"        |{workstation}\n")
            out_file.write(f"        |{xp}\n")
            out_file.write(f"        |{products}\n")
            out_file.write("    }}")

    # Separate recipes based on construction flag for combined templates
    crafting_recipes = {}
    construction_recipes = {}
    for raw_name, recipe_data in processed_recipes.items():
        if recipe_data.get("construction", False):
            construction_recipes[raw_name] = recipe_data
        else:
            crafting_recipes[raw_name] = recipe_data

    # Crafting Template for non-construction recipes
    recipe_names_crafting = [raw_name.lower() for raw_name in crafting_recipes.keys()]
    limited_recipe_names_crafting = recipe_names_crafting[:150]
    recipe_list_crafting = "\n".join([f"|{name}" for name in limited_recipe_names_crafting])
    combined_header_crafting = (
        "<noinclude>[[Category:Crafting templates]]\n{{wip}}\n"
        "{{Documentation|doc=\n"
        "{{Crafting/sandbox\n"
        f"{recipe_list_crafting}\n"
        "}}\n"
        "}}\n"
        "</noinclude><includeonly><!--\n\n"
        "#############################################\n"
        "###           START OF RECIPES            ###\n"
        "#############################################\n\n"
        "-->\n"
        "{{#switch: {{{1|}}}\n"
        "|#default=\n"
        "  {{!}}-\n"
        "  {{!}} N/A\n"
        "  {{!}}{{!}} This index number contains no data\n"
    )
    combined_content_crafting = [combined_header_crafting]

    for raw_name, recipe_data in crafting_recipes.items():
        ingredients = recipe_data["ingredients"]
        tools = recipe_data["tools"]
        recipes = recipe_data["recipes"]
        skills = recipe_data["skills"]
        workstation = recipe_data["workstation"]
        products = recipe_data["products"]
        xp = recipe_data["xp"]

        combined_content_crafting.append(
            f"    |{raw_name.lower()}=\n"
            f"        {{{{Recipe/sandbox\n"
            f"            |{ingredients}\n"
            f"            |{tools}\n"
            f"            |{recipes}\n"
            f"            |{skills}\n"
            f"            |{workstation}\n"
            f"            |{xp}\n"
            f"            |{products}\n"
            f"        }}}}"
        )

    combined_footer = "}}</includeonly>"
    combined_content_crafting.append(combined_footer)

    combined_output_file_crafting = 'output/recipes/recipe list.txt'
    with open(combined_output_file_crafting, 'w', encoding='utf-8') as combined_file:
        combined_file.write("\n".join(combined_content_crafting))

    # Construction Template for construction recipes
    recipe_names_construction = [raw_name.lower() for raw_name in construction_recipes.keys()]
    limited_recipe_names_construction = recipe_names_construction[:150]
    recipe_list_construction = "\n".join([f"|{name}" for name in limited_recipe_names_construction])
    combined_header_construction = (
        "<noinclude>[[Category:Construction templates]]\n{{wip}}\n"
        "{{Documentation|doc=\n"
        "{{Building\n"
        f"{recipe_list_construction}\n"
        "}}\n"
        "}}\n"
        "</noinclude><includeonly><!--\n\n"
        "#############################################\n"
        "###           START OF RECIPES            ###\n"
        "#############################################\n\n"
        "-->\n"
        "{{#switch: {{{1|}}}\n"
        "|#default=\n"
        "  {{!}}-\n"
        "  {{!}} N/A\n"
        "  {{!}}{{!}} This index number contains no data\n"
    )
    combined_content_construction = [combined_header_construction]

    for raw_name, recipe_data in construction_recipes.items():
        ingredients = recipe_data["ingredients"]
        tools = recipe_data["tools"]
        recipes = recipe_data["recipes"]
        skills = recipe_data["skills"]
        workstation = recipe_data["workstation"]
        products = recipe_data["products"]
        xp = recipe_data["xp"]

        combined_content_construction.append(
            f"    |{raw_name.lower()}=\n"
            f"        {{{{Recipe/sandbox\n"
            f"            |{ingredients}\n"
            f"            |{tools}\n"
            f"            |{recipes}\n"
            f"            |{skills}\n"
            f"            |{workstation}\n"
            f"            |{xp}\n"
            f"            |{products}\n"
            f"        }}}}"
        )

    combined_content_construction.append(combined_footer)

    combined_output_file_construction = 'output/recipes/building_list.txt'
    with open(combined_output_file_construction, 'w', encoding='utf-8') as combined_file:
        combined_file.write("\n".join(combined_content_construction))


def main(recipes_data=None):
    print("Processing recipe output...")

    # Load the recipe data
    if not recipes_data:  # Avoid circular imports if running from recipe_format.py
        recipes_data = recipe_format.get_processed_recipes()

    # Load the tags data
    tags_data = item_tags.get_tag_data()

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
            "construction": construction_flag
        }

    output(processed_recipes)

    normal_item_input_map, normal_item_output_map, construction_item_input_map, construction_item_output_map = gather_item_usage(recipes_data, tags_data)

    output_item_usage(normal_item_input_map, normal_item_output_map, construction_item_input_map, construction_item_output_map)


if __name__ == "__main__":
    main()
