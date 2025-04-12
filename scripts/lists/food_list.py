import os
from tqdm import tqdm
from scripts.parser import item_parser, evolvedrecipe_parser, recipe_parser
from scripts.core.language import Language
from scripts.core.constants import RESOURCE_PATH, PBAR_FORMAT
from scripts.utils import utility, lua_helper, table_helper, util
from scripts.core.cache import save_cache

TABLE_PATH = f"{RESOURCE_PATH}/tables/food_table.json"

evolvedrecipe_products = []
recipe_products = []
forage_categories = {}
table_map = {}


def generate_data(item_id, item_data):
    table_type = item_data.get("TableType")
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item = {}

    item_name = utility.get_name(item_id, item_data)

    item["icon"] = utility.get_icon(item_id, True, True, True) if "icon" in columns else None
    item["name"] = util.format_link(item_name, utility.get_page(item_id, item_name)) if "name" in columns else None
    item["weight"] = item_data.get("Weight", "1") if "weight" in columns else None
    item["hunger"] = item_data.get("HungerChange", "-") if "hunger" in columns else None
    item["thirst"] = item_data.get("ThirstChange", "-") if "thirst" in columns else None
    item["calories"] = item_data.get("Calories", "-") if "calories" in columns else None
    item["carbohydrates"] = item_data.get("Carbohydrates", "-") if "carbohydrates" in columns else None
    item["lipids"] = item_data.get("Lipids", "-") if "lipids" in columns else None
    item["proteins"] = item_data.get("Proteins", "-") if "proteins" in columns else None
    if "unhappiness" in columns:
        unhappiness = item_data.get("UnhappyChange")
        if unhappiness is not None and item_data.get("RemoveUnhappinessWhenCooked", "").lower() == "true":
            item["unhappiness"] = f"{unhappiness}*"
        elif unhappiness is not None:
            item["unhappiness"] = unhappiness
        else:
            item["unhappiness"] = "-"
    item["boredom"] = item_data.get("BoredomChange", "-") if "boredom" in columns else None
    item["stress"] = item_data.get("StressChange", "-") if "stress" in columns else None
    item["fatigue"] = item_data.get("FatigueChange", "-") if "fatigue" in columns else None
    item["alcohol"] = item_data.get("Alcoholic", "-") if "alcohol" in columns else None
    if "sickness" in columns: #TODO: look at raw food
        if item_data.get("ReduceFoodSickness"):
            item["sickness"] = item_data.get("ReduceFoodSickness")
        elif item_data.get("DangerousUncooked"):
            item["sickness"] = "?"
        else:
            item["sickness"] = "-"
    item["poison"] = item_data.get("PoisonPower", "-") if "poison" in columns else None
    item["fresh"] = item_data.get("DaysFresh", "-") if "fresh" in columns else None
    item["rotten"] = item_data.get("DaysTotallyRotten", "-") if "rotten" in columns else None
    item["cooked"] = item_data.get("MinutesToCook", "-") if "cooked" in columns else None
    item["burned"] = item_data.get("MinutesToBurn", "-") if "burned" in columns else None
    if "spice" in columns:
        if item_data.get("Spice", "").lower() == "true":
            item["spice"] = '[[File:UI Tick.png|link=|Used as spice in cooking]]'
        else:
            item["spice"] = '[[File:UI Cross.png|link=|Used as ingredient in cooking]]'
    item["item_id"] = item_id if "item_id" in columns else None

    # Remove any values that are None
    item = {k: v for k, v in item.items() if v is not None}

    # Ensure column order is correct
    item = {key: item[key] for key in columns if key in item}

    # Add item_name for sorting
    item["item_name"] = item_name

    return item


def find_table_type(item_id, item_data):
    type_name = item_id.split(".")[1]
    display_name = item_data.get("DisplayName", "")
    table_type = None
    if type_name in evolvedrecipe_products or item_id in evolvedrecipe_products:
        table_type = "Evolved_recipes"
    elif "Canned" in display_name or "Can of Food" in display_name:
        table_type = "Canned"
    else:
        food_type = item_data.get("FoodType", "").lower()
        if food_type == "egg":
            table_type = "Egg"
        elif item_id in forage_categories["WildPlants"]:
            table_type = "Wild_plants"
        elif food_type == "herb" or item_id in forage_categories["WildHerbs"]:
            table_type = "Herb"
        elif item_id in forage_categories["MedicinalPlants"] or item_id in forage_categories["Medical"]:
            table_type = "Medicinal"
        elif food_type in ("vegetable", "vegetables", "mushroom", "greens", "hotpepper") or item_id in forage_categories["Vegetables"] or item_id in forage_categories["Mushrooms"]:
            table_type = "Vegetables"
        elif food_type in ("fruits", "citrus", "berry") or item_id in forage_categories["Berries"] or item_id in forage_categories["Fruits"]:
            table_type = "Fruits"
        elif food_type in ("meat", "poultry", "bacon", "beef", "sausage", "venison"):
            table_type = "Meat"
        elif food_type in ("seafood", "fish", "roe") or "Fish" in item_data.get("Icon", item_data.get("IconsForTexture", "")):
            table_type = "Seafood"
        elif food_type == "Insect" or item_id in forage_categories["Insects"] or item_id in forage_categories["FishBait"]:
            table_type = "Insect"
        elif food_type == "game" or "Dead" in display_name:
            table_type = "Game"
        elif any(x in display_name for x in ("Head", "Animal")) and "Sunflower" not in display_name:
            table_type = "Animal_parts"
        elif item_id in recipe_products:
            table_type = "Prepared"
        elif food_type in ("bread", "pasta", "rice"):
            table_type = "Grains"
        elif any(x in display_name for x in ("Dung", "Droppings")):
            table_type = "Droppings"
        elif item_data.get("Spice", "").lower() == "true":
            table_type = "Spice"
        elif food_type in ("cheese", "chocolate", "cocoa", "coffee", "oil", "nut", "seed", "stock", "sugar", "tea", "thickener", "catfood", "dogfood"):
            table_type = "Miscellaneous"
        elif food_type == "" or food_type == "noexplicit":
            table_type = "Other"
        else:
            table_type = food_type

    item_data["TableType"] = table_type

    return table_type, item_data


def parse_foraging():
    LUA_EVENTS = ("""
        package = package or {}
        package.preload = package.preload or {}

        -- Stub Foraging modules
        package.preload["Foraging/forageSystem"] = function() return {} end
        package.preload["Foraging/forageDefinitions"] = function() return {} end

        -- Stub global engine function
        function getTexture(name)
            return {
                getName = function() return name end
            }
        end

        -- Generic fallback for missing globals
        local function fallback()
            return setmetatable({}, {
                __index = function(_, key)
                    return function() return tostring(key) end
                end
            })
        end

        Events = Events or {}

        setmetatable(Events, {
            __index = function(_, key)
                return fallback()
            end
        })

        setmetatable(_G, {
            __index = function(_, key)
                return fallback()
            end
        })
    """)

    lua_files = [
        "forageDefinitions.lua",
        "forageSystem.lua",
        "Ammo.lua",
        "Animals.lua",
        "Artifacts.lua",
        "Berries.lua",
        "Bones.lua",
        "Clothing.lua",
        "CraftingMaterials.lua",
        "DeadAnimals.lua",
        "ForestGoods.lua",
        "ForestRarities.lua",
        "Fruits.lua",
        "Herbs.lua",
        "Insects.lua",
        "Junk.lua",
        "JunkFood.lua",
        "JunkWeapons.lua",
        "Medical.lua",
        "MedicinalPlants.lua",
        "Mushrooms.lua",
        "Stones.lua",
        "Trash.lua",
        "Vegetables.lua",
        "WildPlants.lua",
    ]
    # Inject lua: Foraging - initialises and stubs Events table
    lua_runtime = lua_helper.load_lua_file(lua_files, inject_lua=LUA_EVENTS)
    parsed_data = lua_helper.parse_lua_tables(lua_runtime)
    all_forage_data = parsed_data["forageDefs"]
    save_cache(all_forage_data, "foraging_2.json")

    global forage_categories
    forage_items = {}
    for forage_name, forage_data in all_forage_data.items():
        item_id = forage_data.get("type")
        categories = forage_data.get("categories", [])
        if item_id is not None:
            forage_items[item_id] = categories

        for category in categories:
            if category not in forage_categories:
                forage_categories[category] = []
            forage_categories[category].append(item_id)
    
    save_cache(forage_items, "forage_items.json")
    save_cache(forage_categories, "forage_categories.json")


def find_items():
    all_item_data = item_parser.get_item_data()
    food_items = {}
    nutrition_items = {}

    for item_id, item_data in all_item_data.items():
        item_type = item_data.get("Type", "")
        if item_type.lower() == "food":
            food_items[item_id] = item_data

            if item_data.get("Calories"):
                nutrition_items[item_id] = item_data
    
    return food_items, nutrition_items


def main():
    global language_code
    global evolvedrecipe_products
    global recipe_products
    global table_map
    language_code = Language.get()
    evolvedrecipe_data = evolvedrecipe_parser.get_evolvedrecipe_data()
    recipes_data = recipe_parser.get_recipe_data()["recipes"]
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)
    parse_foraging()

    cooking_recipe_data = {}
    i = 0
    for recipe in recipes_data:
        is_mapper = False
        if recipe.get("category") == "Cooking" and recipe.get("xpAward"):
            cooking_recipe_data[recipe.get("name", i)] = recipe
            outputs = recipe.get("outputs", [])
            for p in outputs:
                products = p.get("items")
                if products:
                    recipe_products.extend(products)
                if "mapper" in p:
                    is_mapper = True
            if is_mapper:
                item_mappers = recipe.get("itemMappers", {})
                for key, value in item_mappers.items():
                    recipe_products.extend(list(value.keys()))

        i += 1
    
    save_cache(cooking_recipe_data, "cooking_recipe_data.json")
    save_cache({"recipes": recipe_products}, "recipe_products_data.json")


    # Store all evolvedrecipe products in a list for determining section
    for recipe, recipe_data in evolvedrecipe_data.items():
        evolvedrecipe_products.append(recipe_data.get("ResultItem"))

    with tqdm(total=0, desc="Preparing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        food_items, nutrition_items = find_items()

        # Update the total once we know how many items
        pbar.total = len(food_items) + len(nutrition_items)
        pbar.refresh()

        all_food_data = {"nutrition": []}

        # Process food items
        for item_id, item_data in food_items.items():
            pbar.set_postfix_str(f'Generating: Food ({item_id[:30]})')
            table_type, item_data = find_table_type(item_id, item_data)
            food_data = generate_data(item_id, item_data)

            if table_type not in all_food_data:
                all_food_data[table_type] = []
            
            all_food_data[table_type].append(food_data)

            pbar.update(1)

        # Process nutrition items
        for item_id, item_data in nutrition_items.items():
            pbar.set_postfix_str(f'Generating: Nutrition ({item_id[:30]})')
            item_data["TableType"] = "nutrition"
            nutrition_data = generate_data(item_id, item_data)
            all_food_data["nutrition"].append(nutrition_data)

            pbar.update(1)

        pbar.set_postfix_str("Creating tables...")
        table_helper.create_tables("food", all_food_data, table_map=table_map, columns=column_headings)


if __name__ == "__main__":
    main()