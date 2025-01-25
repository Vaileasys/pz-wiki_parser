import os
from tqdm import tqdm
from scripts.parser import item_parser, recipe_parser
from scripts.core import translate, utility

language_code = "en"
pbar_format = "{l_bar}{bar:30}{r_bar}"

# Used for getting table values
TABLE_DICT = {
    "generic": ['icon', 'name', 'weight', 'item_id'],
    "leisure": ['icon', 'name', 'weight', 'unhappy', 'stress', 'boredom', 'item_id'],
    "recipe": ['icon', 'name', 'weight', 'recipes', 'skill', 'item_id'],
    "skill": ['icon', 'name', 'weight', 'pages', 'multiplier', 'skill', 'levels', 'item_id'],
    "writable": ['icon', 'name', 'weight', 'pages', 'item_id'],
}

# Map table values with their headings
COLUMNS_DICT = {
    "icon": "! Icon",
    "name": "! Name",
    "weight": "! [[File:Status_HeavyLoad_32.png|32px|link=Heavy load|Encumbrance]]",
    "unhappy": "! [[File:Mood_Sad_32.png|32px|link=Unhappy]]",
    "stress": "! [[File:Mood_Stressed_32.png|32px|link=Stressed]]",
    "boredom": "! [[File:Mood_Bored_32.png|32px|link=Bored]]",
    "pages": "! Pages",
    "multiplier": "! Multiplier",
    "recipes": "! Recipes",
    "skill": "! Skill",
    "levels": "! Levels",
    "item_id": "! Item ID",
}

# Map the headings to their table_key (TABLE_DICT key)
TABLE_MAPPING = {
    "Map": "map",
    "Writable": "writable",
    "Recipe magazines": "recipe",
    "Schematics": "recipe",
    "Skill books": "skill",
    "Seed packets": "recipe",
    "Hollow books": "leisure",
    "Hardcover books": "leisure",
    "Leatherbound books": "leisure",
    "Paperback books": "leisure",
    "Magazines": "leisure",
    "Newspapers": "leisure",

    "Miscellaneous": "leisure",
    "Other": "generic",
}

# Map sections to the correct position
# TODO: not currently used. Intended to be used as part of a merge_txt_files function.
SECTION_DICT = {
    'Skill books': [],
    'Recipe': [
        'Recipe magazines',
        'Schematics'
    ],
    'Leisure': [
        'Hollow books',
        'Hardcover books',
        'Leatherbound books',
        'Paperback books',
        'Magazines',
        'Newspapers',
        'Miscellaneous'
    ],
    'Cartography': [
        'Maps',
        'Annotated maps'
    ],
    'Writable': [],
}

TABLE_HEADER ='{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"'

# Get the list type, for mapping the section/table
def get_list_type(item_id, item_data):
    TYPE_MAPPING = {
        "ComicBook": "Miscellaneous", # Included so it doesn't get added to 'Hardcover books'
        "PhotoBook": "Miscellaneous", # Included so it doesn't get added to 'Hardcover books'
        "PictureBook": "Miscellaneous", # Included so it doesn't get added to 'Hardcover books'
        "HollowBook": "Hollow books",
        "HollowFancyBook": "Hollow books",
        "BookFancy": "Leatherbound books",
        "Book": "Hardcover books",
        "Magazine": "Magazines",
        "HottieZ": "Magazines",
        "HunkZ": "Magazines",
        "Newspaper": "Newspapers",
        "Paperback": "Paperback books"
    }

    item_type = item_data["Type"]
    display_category = item_data.get("DisplayCategory", item_type)

    # Map/Cartography
    if item_type == "Map":
        return "Map"
    
    # Writable
    if "CanBeWrite" in item_data:
        return "Writable"
    
    # Skill Books & Recipes
    if display_category == "SkillBook":
        schematics = ["Schematic", "Recipe"]
        if "TeachedRecipes" in item_data:
            return "Recipe magazines"
        elif any(keyword in item_data.get("OnCreate", "") for keyword in schematics) or any(keyword in item_id for keyword in schematics):
            return "Schematics"
        else:
            return "Skill books"
    # Seed packets
    elif display_category == "Gardening":
        return "Seed packets"
    
    # Leisure. Map to the correct heading.
    for key, value in TYPE_MAPPING.items():
        if key in item_id:
            return value
    
    # Default
    return "Miscellaneous"
        

# Get list of recipes an item teaches.
# TODO: Partially incomplete. Waiting for construction recipes.
def get_recipes(item_data):

    # Get and format the link
    def get_link_from_id(id, recipe_name):
        product_name = translate.get_translation(id)
        product_page = utility.get_page(id, product_name)
#        product_link = utility.format_link(product_name, product_page)
        product_link = f"[[{product_page}|{recipe_name}]]"
        return product_link

    if item_data.get("OnCreate"):
        return "''Randomized''"
    else:
        recipes_raw = item_data.get('TeachedRecipes')
        if recipes_raw is None:
            return "-"
        elif isinstance(recipes_raw, str):
            recipes_raw = [recipes_raw]
        
        parsed_recipe_data = recipe_parser.get_recipe_data()

        recipes = []

        for recipe in recipes_raw:
            recipe_name = translate.get_translation(recipe, "")
            if recipe_name == recipe:
                recipe_name = translate.get_translation(recipe, "TeachedRecipes")
            # Check if recipe is in the recipe data. Some won't be in there, such as farming.
            if recipe.lower() in [rec["name"].lower() for rec in parsed_recipe_data["recipes"]]:

                for rec in parsed_recipe_data["recipes"]:
                    if rec["name"].lower() == recipe.lower():
                        # Check if it's a mapping product
                        if rec.get("outputs", [{}])[0].get("mapper"):
                            mapper = rec.get("outputs", [{}])[0].get("mapper")
                            product_link= f'<span title="Recipe mapper: {mapper}">{recipe_name}</span>'
                            #TODO: decide how to handle recipe product mapping
#                            product_id = next(iter(rec.get("itemMappers", {}).get(mapper, {}).values()), "")
#                            product_link = get_link_from_id(product_id, recipe_name)
                        else:
                            product_id = rec["outputs"][0]["items"]
                            if len(product_id) > 1:
                                print("WARNING: More than 1 product.")
                            product_link = get_link_from_id(product_id[0], recipe_name)

                        #Add the product to the list if it hasn't already
                        if product_link not in recipes:
                            recipes.append(product_link)
            else:
                recipes.append(recipe_name)

        
        recipes_output = "<br>".join(recipes)
    return recipes_output


# Get the skill for an item return a formatted link
def get_skills(item_id, item_data):
    SKILL_MAP = {
        "Armor": None,
        "BagSeed": "Farming",
        "Cooking": "Cooking",
        "Electronics": "Electricity",
        "Engineer": "Electricity",
        "Farming": "Farming",
        "Fishing": "Fishing",
        "Glassmaking": "Glassmaking",
        "Hemp": "Farming",
        "Herbalist": "Foraging",
        "Hunting": "Trapping",
        "Key": None,
        "Knitting": "Tailoring",
        "Mechanic": "Mechanics",
        "Metalwork": "MetalWelding",
        "PrimitiveTool": None,
        "Radio": "Electricity",
        "Smithing": "Smithing",
        "Trick": None,
        "Weapon": None
    }

    skill = item_data.get('SkillTrained')

    # Map the item id to a skill in SKILL_MAP
    if not skill:
        for key, value in SKILL_MAP.items():
            if key in item_id:
                skill = value

    # Translate skill and format link
    if skill is not None:
        if skill == "FirstAid":
            skill = "Doctor" # So it can be translating correctly
        skill_en = translate.get_translation(skill, "SkillTrained", "en")
        if language_code != "en":
            skill_translated = translate.get_translation(skill, "SkillTrained")
        else:
            skill_translated = skill_en
        return utility.format_link(skill_translated, skill_en)
    
    return "-"


# Process items, returning the heading and row data.
def process_item(item_id, item_data):
    heading = get_list_type(item_id, item_data)
    columns = TABLE_DICT.get(TABLE_MAPPING[heading], TABLE_DICT["generic"])
    language_code = translate.get_default_language()
    name_ref = utility.get_name(item_id, item_data)

    item = {}

    if "icon" in columns:
        item["icon"] = utility.get_icon(item_id, True, True, True)

    if "name" in columns:
        page_name = utility.get_page(item_id, name_ref)
        item_link = f"[[{page_name}]]"
        if language_code != "en":
            item_link = f"[[{page_name}/{language_code}|{name_ref}]]"
        item["name"] = item_link

    if "weight" in columns:
        item["weight"] = item_data.get('Weight', '1')
    
    if "unhappy" in columns:
        item["unhappy"] = item_data.get('UnhappyChange', '-')

    if "stress" in columns:
        item["stress"] = item_data.get('StressChange', '-')

    if "boredom" in columns:
        item["boredom"] = item_data.get('BoredomChange', '-')

    if "recipes" in columns:
        recipes = get_recipes(item_data)
        item["recipes"] = recipes

    if "pages" in columns:
        item["pages"] = item_data.get('PageToWrite', item_data.get('NumberOfPages', '-'))

    if "multiplier" in columns:
        skill_level = int(item_data.get("LvlSkillTrained", 1))
        levels_trained = int(item_data.get("NumLevelsTrained", 2))
        item["multiplier"] = str(skill_level * levels_trained)

    if "skill" in columns:
        skill = get_skills(item_id, item_data)
        item["skill"] = skill

    if "levels" in columns:
        skill_level_min = int(item_data.get("LvlSkillTrained", 1))
        levels_trained = int(item_data.get("NumLevelsTrained", 2))
        skill_level_max = skill_level_min + levels_trained - 1
        item["levels"] = f"{skill_level_min}–{skill_level_max}"

    if "item_id" in columns:
        item["item_id"] = f"{{{{ID|{item_id}}}}}"
    
    item["item_name"] = name_ref

    return heading, item


# Get necessary literature items and process them
def get_items():
    literature_dict = {}
    parsed_item_data = item_parser.get_item_data()

    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=pbar_format, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item_data.get("Type") in ("Literature", "Map") or item_data.get("DisplayCategory") == "Literature":
                heading, item = process_item(item_id, item_data)

                # Add heading to dict if it hasn't been added yet.
                if heading not in literature_dict:
                    literature_dict[heading] = []

                literature_dict[heading].append(item)

            pbar.update(1)

        pbar.bar_format = f"Items processed."

    return literature_dict


# Write to txt files. Separate file for each heading.
def write_to_output(literature_dict):
    # write to output.txt
    language_code = translate.get_language_code()
    output_dir = os.path.join('output', language_code, 'literature')

    os.makedirs(output_dir, exist_ok=True)

    for heading, items in literature_dict.items():
        columns = TABLE_DICT.get(TABLE_MAPPING[heading], TABLE_DICT["generic"])

        # Build the table heading based on values
        table_headings = []
        for col in columns:
            mapped_headings = COLUMNS_DICT.get(col, col)
            table_headings.append(mapped_headings)
        table_headings = "\n".join(table_headings)

        output_path = os.path.join(output_dir, f"{heading}.txt")
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(f"<!--BOT_FLAG-start-{heading.replace(" ", "_")}. DO NOT REMOVE-->")
            file.write(f"{TABLE_HEADER}\n")
            file.write(f"{table_headings}\n")

            items = sorted(items, key=lambda x: x['item_name'])
            for item in items:
                # Remove 'item_name' from the dict, so it doesn't get added to the table.
                item.pop("item_name", None)
                row = "\n| ".join([value for key, value in item.items()])
                file.write(f"|-\n| {row}\n")

            file.write("|}")
            file.write(f"<!--BOT_FLAG-end-{heading.replace(" ", "_")}. DO NOT REMOVE-->")

    print(f"Output saved to {output_dir}")


def main():
    global language_code
    language_code = language_code = translate.get_language_code()
    items = get_items()
    write_to_output(items)
                

if __name__ == "__main__":
    main()
