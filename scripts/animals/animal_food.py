import os

from scripts.core.language import Translate, Language
from scripts.core import constants
from scripts.core import file_loading
from scripts.utils import echo, util
from scripts.objects.animal import AnimalBreed
from scripts.objects.item import Item

BOT_FLAG_TYPE = "animal_food_types"
ANIMAL_FOOD_DIR = os.path.join(constants.ANIMAL_DIR, BOT_FLAG_TYPE)

animal_food_cache: dict[list[Item]] = {}

def generate_data(breed: AnimalBreed) -> dict[str, list[str]] | str:
    animal = breed.animal

    foods = {}

    for food_type, value_type in animal.food_types.items():
        foods[food_type] = []
        if value_type == "Unknown":
            continue
        
        # No icon, just a link if it's 'All'
        if value_type == "All":
            all_link = util.link("Food", "Food")
            foods[food_type].append(f"Any {all_link}")

            return foods
        
        food_type_icon = {
            "Vegetables": Item("Base.Carrots"),
            "Fruits": Item("Base.Apple"),
            "Nut": Item("Base.Peanuts"),
            "Insect": Item("Base.Worm")
        }
        # Get FoodType icon and link
        if value_type == "FoodType":

            icon_item = food_type_icon.get(food_type)
            if not icon_item:
                echo.warning(f"No food type icon found for '{food_type}' when generating food list for '{breed.full_breed_id}'.")
                continue

            icon_raw = icon_item.get_icon(False, False, False)
            food_name = Translate.get(f"ContextMenu_FoodType_{food_type}")

            icon = f"[[File:{icon_raw}|32x32px|link=Food{Language.get_subpage()}#{food_name}|{food_name}]]"
            name = util.link("Food", food_name, f"{food_name}s") # Add 's' to anchor link

            foods[food_type].append(f"{icon} Any {name}")

        # Get items for AnimalFeedType icons and links
        elif value_type == "AnimalFeedType":
            foods[food_type] = []
            for item in animal_food_cache.get(food_type, []):
                item: Item
                
                if not item:
                    echo.warning(f"No item found for AnimalFoodType '{food_type}'when generating food list for '{breed.full_breed_id}'.")
                    continue
                
                icon = item.get_icon(True, False, False)
                name = item.wiki_link

                foods[food_type].append(f"{icon} {name}")
        
    return foods


def do_list(foods: dict[list[str]]|str, breed: AnimalBreed):
    if not foods:
        return

    content = []

    bot_flag_start = constants.BOT_FLAG.format(type=BOT_FLAG_TYPE, id=breed.full_breed_id)
    bot_flag_end = constants.BOT_FLAG_END.format(type=BOT_FLAG_TYPE, id=breed.full_breed_id)

    content.append(f'{bot_flag_start}<div class="list-columns">')
    for food_type, food_list in foods.items():
        for entry in food_list:
            content.append(f"*{entry}")
    content.append(f'</div>{bot_flag_end}')

    file_loading.write_file(content, rel_path=breed.full_breed_id + ".txt", root_path=ANIMAL_FOOD_DIR)


def cache_animal_food_types():
    echo.info("Generating cache for AnimalFoodTypes...")
    global animal_food_cache

    animal_food_cache = {}
    for item_id, item in Item.items():
        if item.animal_feed_type:
            if item.animal_feed_type not in animal_food_cache:
                animal_food_cache[item.animal_feed_type] = []
            animal_food_cache[item.animal_feed_type].append(item)

    return animal_food_cache


def main():
    cache = cache_animal_food_types()
#    file_loading.save_json("temp.json", cache)

    for _, breed in AnimalBreed.all().items():
        foods = generate_data(breed)
    
        do_list(foods, breed)



if __name__ == "__main__":
    main()