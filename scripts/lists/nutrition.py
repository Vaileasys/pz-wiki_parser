import os
from tqdm import tqdm
from scripts.parser import item_parser
from scripts.core import translate, utility
from scripts.core.constants import PBAR_FORMAT

def write_to_output(items):
    items = sorted(items, key=lambda x: x['item_name'].lower())

    # write to output.txt
    language_code = translate.get_language_code()
    output_dir = os.path.join("output", language_code, 'item_list')
    output_file = os.path.join(output_dir, 'nutrition.txt')
    os.makedirs(output_dir, exist_ok=True)

    with tqdm(total=len(items), desc="Writing nutrition table", bar_format=PBAR_FORMAT, unit=" items") as pbar:
    
        with open(output_file, 'w', encoding='utf-8') as file:

            file.write("{| class=\"wikitable theme-red sortable\" style=\"text-align:center;\"")
            file.write("\n! Icon !! Name !! [[File:Status_HeavyLoad_32.png|32px|link=Heavy load|Encumbrance]] !! [[File:Status_Hunger_32.png|32px|link=Hungry|Hunger]] !! [[File:Fire_01_1.png|32px|link=Nutrition#Calories|Calories]] !! [[File:Wheat.png|32px|link=Nutrition#Carbohydrates|Carbohydrates]] !! [[File:Steak.png|32px|link=Nutrition#Proteins|Proteins]] !! [[File:Butter.png|32px|link=Nutrition#Fat|Fat]] !! Item ID\n")
        
            for item in items:
                item_id = item['item_id']

                pbar.set_postfix_str(f"Writing: {item_id}")

                item_link = item['item_link']
                icons = item['icons']
                weight = item['weight']
                hunger = item['hunger']
                calories = item['calories']
                carbohydrates = item['carbohydrates']
                lipids = item['lipids']
                proteins = item['proteins']

                file.write(f"|-\n| {icons} || {item_link} || {weight} || {hunger} || {calories} || {carbohydrates} || {proteins} || {lipids} || {item_id}\n")

                pbar.update(1)

            file.write("|}")
        pbar.clear()
        pbar.bar_format = f"Nutrition table completed. File can be found in '{output_file}'\n"


def get_items():
    items = []
    parsed_items = item_parser.get_item_data().items()
    language_code = translate.get_language_code()
    
    with tqdm(total=len(parsed_items), desc="Getting food items", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item_data in parsed_items:
            # Change the string at the end of the progress bar
            pbar.set_postfix_str(f"Processing: {item_data.get("Type", "Unknown")} ({item_id[:30]})")

            if "Calories" in item_data:
                if language_code != "en":
                    item_name = translate.get_translation(item_id, "DisplayName")
                else:
                    item_name = item_data.get('DisplayName')
                page_name = utility.get_page(item_id, item_name)
                item_link = utility.format_link(item_name, page_name)


                items.append({
                    'item_id': item_id,
                    'item_name': item_name,
                    'item_link': item_link,
                    'icons': utility.get_icon(item_id, True, True, True),
                    'weight': item_data.get('Weight', '1'),
                    'hunger': item_data.get('HungerChange', '0'),
                    'calories': item_data.get('Calories', '0'),
                    'carbohydrates': item_data.get('Carbohydrates', '0'),
                    'lipids': item_data.get('Lipids', '0'),
                    'proteins': item_data.get('Proteins', '0')
                })
            pbar.update(1)
        pbar.clear()
        pbar.bar_format = f"Finished getting items."
    
    return items


def main():
    items = get_items()
    write_to_output(items)
                

if __name__ == "__main__":
    main()
