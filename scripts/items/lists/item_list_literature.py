import os
from tqdm import tqdm
from scripts.parser import stash_parser
from scripts.core.language import Language, Translate
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.utils import table_helper
from scripts.objects.item import Item
from scripts.objects.skill import Skill

TABLE_PATH = os.path.join(TABLES_DIR, "literature_table.json")


table_map = None
table_type_map = None

# Get the list type, for mapping the section/table
def get_list_type(item: Item, special_data):
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

    display_category = item.raw_display_category or item.type

    # Map/Cartography
    if item.type == "Map":
        return "Maps"
    
    # Writable
    if item.can_be_write:
        return "Writable"
    
    # Skill Books & Recipes
    if display_category == "SkillBook":
        schematics = ["Schematic", "Recipe"]
        if item.teached_recipes:
            return "Recipe magazines"
        elif any(keyword in (item.on_create or "") for keyword in schematics) or any(keyword in item.item_id for keyword in schematics):
            return "Schematics"
        else:
            return "Skill books"
    # Seed packets
    elif display_category == "Gardening":
        return "Seed packets"
    
    # Leisure. Map to the correct heading.
    for key, value in TYPE_MAPPING.items():
        if key in item.item_id:
            return value
    
    # Default
    return "Miscellaneous"


# Get list of recipes an item teaches.
def get_recipes(item: Item):
    if item.on_create:
        return "''Randomized''"
    else:
        recipes = item.get_recipes()
        if not recipes:
            return "-"
        
    return "<br>".join(recipes)


# Get the skill for an item return a formatted link
def get_skills(item: Item):
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
        "Herbalist": "PlantScavenging",
        "Hunting": "Trapping",
        "Key": None,
        "Knitting": "Tailoring",
        "Mechanic": "Mechanics",
        "Metalwork": "MetalWelding",
        "PrimitiveTool": None,
        "Radio": "Electricity",
        "Smithing": "MetalWelding",
        "Trick": None,
        "Weapon": None
    }

    if item.skill_trained:
        return item.skill_trained.wiki_link
    
    skill = None

    # Map the item id to a skill in SKILL_MAP
    for key, value in SKILL_MAP.items():
        if key in item.item_id:
            skill = value
            break

    if skill:
        return Skill(skill).wiki_link
    
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
def process_item(item: Item, special_data={}):
    heading = get_list_type(item, special_data)
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
        item_name = item.name # set item name
        name_ref = item_name # set item ref (used for sorting)
        page_name = item.page # set page name
        
    containers_data = map_data.get("containers", [])

    item_dict = {}

    if "icon" in columns:
        if map_data:
            raw_icon = item.get_icon(False, False, False)
            if language_code != "en":
                icon = f"[[File:{raw_icon}|32x32px|link={page_name}/{language_code}|{item_name}]]"
            else:
                icon = f"[[File:{raw_icon}|32x32px|link={page_name}|{item_name}]]"
        else:
            icon = item.icon
        item_dict["icon"] = icon

    if "name" in columns:
        item_link = f"[[{page_name}]]"
        if language_code != "en":
            item_link = f"[[{page_name}/{language_code}|{item_name}]]"
        item_dict["name"] = item_link
    
    if "map_id" in columns:
        item_dict["map_id"] = special_data.get("map_id", "-")

    if "weight" in columns:
        item_dict["weight"] = item.weight
    
    if "unhappy" in columns:
        item_dict["unhappy"] = item.unhappy_change or '-'

    if "stress" in columns:
        item_dict["stress"] = item.stress_change or '-'

    if "boredom" in columns:
        item_dict["boredom"] = item.boredom_change or '-'

    if "recipes" in columns:
        recipes = get_recipes(item)
        item_dict["recipes"] = recipes

    if "pages" in columns:
        item_dict["pages"] = item.page_to_write or item.number_of_pages or '-'

    if "multiplier" in columns:
        item_dict["multiplier"] = item.skill_multiplier or '-'

    if "skill" in columns:
        skill = get_skills(item)
        item_dict["skill"] = skill

    if "levels" in columns:
        skill_level_min = int(item.lvl_skill_trained or 1)
        levels_trained = int(item.num_levels_trained)
        skill_level_max = skill_level_min + levels_trained - 1
        item_dict["levels"] = f"{skill_level_min}–{skill_level_max}"

    if "region" in columns:
        if map_id:
            region = get_region(map_id)
        else:
            region = get_region(item.id_type)
        if region == "World":
            region = "Knox Country"

        if region is None:
            item_dict["region"] = "Unknown"

        else:
            if language_code != "en":
                region = f"[[{region}/{language_code}]]"
            else:
                region = f"[[{region}]]"
            item_dict["region"] = region

    if "coords" in columns:
        xcoord = map_data.get("buildingX", 0)
        ycoord = map_data.get("buildingY", 0)
        if None not in (xcoord, ycoord) and 0 not in (xcoord, ycoord):
            item_dict["coords"] = f"{{{{Coordinates|{xcoord}x{ycoord}}}}}"
        else:
            item_dict["coords"] = "Unknown"

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
                container_item = Item(container["containerItem"])
                container_icon = container_item.icon
                containers_list.append(container_icon)
        containers = "".join(containers_list)
        if not containers:
            containers = "-"
        item_dict["container"] = containers

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
        item_dict["container_coords"] = container_coords

    if "loot_table" in columns:
        loot_table = map_data.get("spawnTable", "-")
        if not loot_table:
            loot_table = "-"
        item_dict["loot_table"] = loot_table
    
    if "spawn_on_zed" in columns:
        item_dict["spawn_on_zed"]

    if "item_id" in columns:
        item_dict["item_id"] = item.item_id
    
    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = name_ref

    return heading, item_dict


def process_map(map_region, map_id, map_data):
    special_data = {
        "map_region": map_region,
        "map_id": map_id,
        "map_data": map_data,
    }
    item_id = map_data["item"]
    item = Item(item_id)
    heading, item_dict = process_item(item, special_data)

    return heading, item_dict


# Get necessary literature items and process them
def get_items():
    literature_dict = {}
    parsed_stash_data = stash_parser.get_stash_data()

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f'Processing: {item.type} ({item_id[:30]})')
            if item.type in ("Literature", "Map") or item.raw_display_category == "Literature":
                heading, item_dict = process_item(item)

                # Add heading to dict if it hasn't been added yet.
                if heading not in literature_dict:
                    literature_dict[heading] = []

                literature_dict[heading].append(item_dict)

            pbar.update(1)

        pbar.bar_format = f"Items processed."
    
    # Get annotated maps
    with tqdm(total=Item.count(), desc="Processing annotated maps", bar_format=PBAR_FORMAT, unit=" items") as pbar:
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

    table_helper.create_tables("literature", items, columns=column_headings, table_map=mapped_table, suppress=True, bot_flag_type="literature_item_list", combine_tables=False)
                

if __name__ == "__main__":
    main()
