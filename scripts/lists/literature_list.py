from tqdm import tqdm
from scripts.parser import item_parser, stash_parser
from scripts.recipes import legacy_recipe_parser
from scripts.core.language import Language, Translate
from scripts.core.constants import RESOURCE_PATH, PBAR_FORMAT
from scripts.utils import utility, util, table_helper

TABLE_PATH = f"{RESOURCE_PATH}/tables/literature_table.json"

table_map = None
table_type_map = None

# Get the list type, for mapping the section/table
def get_list_type(item_id, item_data, special_data):
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

    # Annotated maps
    if "map_id" in special_data:
        return "Annotated maps"

    item_type = item_data["Type"]
    display_category = item_data.get("DisplayCategory", item_type)

    # Map/Cartography
    if item_type == "Map":
        return "Maps"
    
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
def get_recipes(item_data):

    if item_data.get("OnCreate"):
        return "''Randomized''"
    else:
        recipes_raw = item_data.get('TeachedRecipes')
        if recipes_raw is None:
            return "-"
        elif isinstance(recipes_raw, str):
            recipes_raw = [recipes_raw]

        recipes = []

        for recipe in recipes_raw:
            recipes.append(utility.get_recipe(recipe))
        
        recipes_output = "<br>".join(recipes)
    return recipes_output


# Get the skill for an item return a formatted link
def get_skills(item_id, item_data):
    SKILL_MAP = {
        "Armor": None,
        "BagSeed": "Agriculture",
        "Cooking": "Cooking",
        "Electronics": "Electricity",
        "Engineer": "Electricity",
        "Farming": "Agriculture",
        "Fishing": "Fishing",
        "Glassmaking": "Glassmaking",
        "Hemp": "Agriculture",
        "Herbalist": "Foraging",
        "Hunting": "Trapping",
        "Key": None,
        "Knitting": "Tailoring",
        "Mechanic": "Mechanics",
        "Metalwork": "Welding",
        "PrimitiveTool": None,
        "Radio": "Electricity",
        "Smithing": "Metalworking",
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
        skill_en = Translate.get(skill, "SkillTrained", "en")
        if Language.get() != "en":
            skill_translated = Translate.get(skill, "SkillTrained")
        else:
            skill_translated = skill_en
        return util.format_link(skill_translated, skill_en)
    
    return "-"


def get_region(region_key):
    REGION_MAPPING = {
        "BBurg": "Brandenburg",
        "Ekron": "Ekron",
        "Irvington": "Irvington",
        "Louisville": "Louisville",
        "MarchRidge": "March Ridge",
        "Mul": "Muldraugh",
        "Riverside": "Riverside",
        "Rosewood": "Rosewood",
        "World": "World",
        "Map": "World",
        "Wp": "West Point",
        "Westpoint": "West Point"
    }

    for key, value in REGION_MAPPING.items():
        if region_key.startswith(key):
            return value
    
    return "World"


# Process items, returning the heading and row data.
def process_item(item_id, item_data, special_data={}):
    heading = get_list_type(item_id, item_data, special_data)
    columns = table_map.get(table_type_map[heading], table_map["generic"])
    language_code = Language.get()
    map_data = {}
    map_id = special_data.get("map_id", "")
    custom_Name = None
    if special_data.get("map_data"):
        map_data = special_data["map_data"]
        custom_Name = map_data.get("customName", "Stash_AnnotedMap")
        region = get_region(map_id)

        item_name = Translate.get(custom_Name, "") # set item name
        name_ref = map_id # set name ref (used for sorting)
        page_name =  f"{item_name} ({region})" # set page name
    else:
        item_name = utility.get_name(item_id, item_data) # set item name
        name_ref = item_name # set item ref (used for sorting)
        page_name = utility.get_page(item_id, item_name) # set page name
        
    containers_data = map_data.get("containers", [])

    item = {}

    if "icon" in columns:
        if map_data:
            icon = utility.get_icon(item_id)
            if language_code != "en":
                icon = f"[[File:{icon}|32x32px|link={page_name}/{language_code}|{item_name}]]"
            else:
                icon = f"[[File:{icon}|32x32px|link={page_name}|{item_name}]]"
        else:
            icon = utility.get_icon(item_id, True, True, True)
        item["icon"] = icon

    if "name" in columns:
        item_link = f"[[{page_name}]]"
        if language_code != "en":
            item_link = f"[[{page_name}/{language_code}|{item_name}]]"
        item["name"] = item_link
    
    if "map_id" in columns:
        item["map_id"] = special_data.get("map_id", "-")

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

    if "region" in columns:
        if map_id:
            region = get_region(map_id)
        else:
            region = get_region(item_id.split(".")[1])
        if region == "World":
            region = "Knox Country"

        if region is None:
            item["region"] = "Unknown"

        else:
            if language_code != "en":
                region = f"[[{region}/{language_code}]]"
            else:
                region = f"[[{region}]]"
            item["region"] = region

    if "coords" in columns:
        xcoord = map_data.get("buildingX", 0)
        ycoord = map_data.get("buildingY", 0)
        if None not in (xcoord, ycoord) and 0 not in (xcoord, ycoord):
            item["coords"] = f"{{{{Coordinates|{xcoord}x{ycoord}}}}}"
        else:
            item["coords"] = "Unknown"

    if "container" in columns:
        containers_list = []
        for container in containers_data:
            if container["containerSprite"]:
                # Tile
                container_sprite = container["containerSprite"]
                if container["containerSprite"].startswith("floors"):
                    container_sprite_str = "Floor"
                else:
                    container_sprite_str = f'[[File:{container_sprite}.png|32x32px]]'

                containers_list.append(container_sprite_str)
            else:
                # Item
                container_icon = utility.get_icon(container["containerItem"], True, True, True)
                containers_list.append(container_icon)
        containers = "".join(containers_list)
        if not containers:
            containers = "-"
        item["container"] = containers

    if "container_coords" in columns:
        coordinates_list = []
        for container in containers_data:
            container_x = container.get("x")
            container_y = container.get("y")
            container_z = container.get("z") #Currently unused
            coords = "Randomized"
            if None not in (container_x, container_y, container_z):
                coords = f"{{{{Coordinates|{container_x}x{container_y}}}}}"                
            
            # Don't add duplicate entries of the same coordinates
            if coords not in coordinates_list:
                coordinates_list.append(coords)
            
        container_coords = "".join(coordinates_list)
        if not container_coords:
            container_coords = "-"
        item["container_coords"] = container_coords

    if "loot_table" in columns:
        loot_table = map_data.get("spawnTable", "-")
        if not loot_table:
            loot_table = "-"
        item["loot_table"] = loot_table
    
    if "spawn_on_zed" in columns:
        item["spawn_on_zed"]

    if "item_id" in columns:
        item["item_id"] = f"{{{{ID|{item_id}}}}}"
    
    # Remove any values that are None
    item = {k: v for k, v in item.items() if v is not None}

    # Ensure column order is correct
    item = {key: item[key] for key in columns if key in item}

    # Add item_name for sorting
    item["item_name"] = name_ref

    return heading, item


def process_map(map_region, map_id, map_data):
    special_data = {
        "map_region": map_region,
        "map_id": map_id,
        "map_data": map_data,
    }
    item_id = map_data["item"]
    item_data = utility.get_item_data_from_id(item_id)
    heading, item = process_item(item_id, item_data, special_data)

    return heading, item


# Get necessary literature items and process them
def get_items():
    literature_dict = {}
    parsed_item_data = item_parser.get_item_data()
    legacy_recipe_parser.get_recipe_data() # Call early so print doesn't interrupt progress bars
    parsed_stash_data = stash_parser.get_stash_data()

    # Get items
    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f'Processing: {item_data.get("Type", "Unknown")} ({item_id[:30]})')
            if item_data.get("Type") in ("Literature", "Map") or item_data.get("DisplayCategory") == "Literature":
                heading, item = process_item(item_id, item_data)

                # Add heading to dict if it hasn't been added yet.
                if heading not in literature_dict:
                    literature_dict[heading] = []

                literature_dict[heading].append(item)

            pbar.update(1)

        pbar.bar_format = f"Items processed."
    
    # Get annotated maps
    with tqdm(total=len(parsed_item_data), desc="Processing annotated maps", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for map_region, region_data in parsed_stash_data.items():
            for map_id, map_data in region_data.items():
                pbar.set_postfix_str(f"Processing: Map ({map_id[:30]})")
                heading, annotated_map = process_map(map_region, map_id, map_data)

                # All annotated maps should be "Annotated map", but we'll be consistent.
                if heading not in literature_dict:
                    literature_dict[heading] = []

                literature_dict[heading].append(annotated_map)

            pbar.update(1)
        
        pbar.bar_format = f"Annotated maps processed."

            
    return literature_dict


def main():
    global table_map
    global table_type_map
    table_map, column_headings, table_type_map = table_helper.get_table_data(TABLE_PATH, "type_map")

    items = get_items()

    mapped_table = {
        item_type: table_map[table_type]
        for item_type, table_type in table_type_map.items()
    }

    table_helper.create_tables("literature", items, columns=column_headings, table_map=mapped_table)
                

if __name__ == "__main__":
    main()
