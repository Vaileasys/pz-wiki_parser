import script_parser
from core import translate


def write_to_output(items):
    # write to output.txt
    output_file = 'output/nutrition.txt'
    language_code = translate.language_code
    with open(output_file, 'w', encoding='utf-8') as file:

        lc_subpage = ""
        if language_code != "en":
            lc_subpage = f"/{language_code}"

        file.write("{| class=\"wikitable theme-red sortable\" style=\"text-align:center;\"")
        file.write("\n! Icon !! Name !! [[File:Moodle_Icon_HeavyLoad.png|link=Heavy load|Encumbrance]] !! [[File:Moodle_Icon_Hungry.png|link=Hungry|Hunger]] !! [[File:Fire_01_1.png|32px|link=Nutrition#Calories|Calories]] !! [[File:Wheat.png|32px|link=Nutrition#Carbohydrates|Carbohydrates]] !! [[File:Steak.png|32px|link=Nutrition#Proteins|Proteins]] !! [[File:Butter.png|32px|link=Nutrition#Fat|Fat]] !! Item ID\n")
        
        for item in items:
            item_id = item['item_id']
            item_name = item['item_name']
            translated_item_name = item['translated_item_name']
            icons = item['icons']
            weight = item['weight']
            hunger = item['hunger']
            calories = item['calories']
            carbohydrates = item['carbohydrates']
            lipids = item['lipids']
            proteins = item['proteins']

            icons_image = ' '.join([f"[[File:{icon}.png|32px]]" for icon in icons])
            item_link = f"[[{item_name}]]"

            if language_code != "en":
                item_link = f"[[{item_name}{lc_subpage}|{translated_item_name}]]"
            file.write(f"|-\n| {icons_image} || {item_link} || {weight} || {hunger} || {calories} || {carbohydrates} || {proteins} || {lipids} || {item_id}\n")
            
        file.write("|}")

    print(f"Output saved to {output_file}")


def get_items():
    items = []
    
    for module, module_data in script_parser.parsed_item_data.items():
        for item_key, item_value in module_data.items():
            if "Calories" in item_value:
                item_id = f"{module}.{item_key}"
                item_name = item_value.get('DisplayName')
                translated_item_name = translate.get_translation(item_id, "DisplayName")

                items.append({
                    'item_id': item_id,
                    'item_name': item_name,
                    'translated_item_name': translated_item_name,
                    'icons': [item_value.get('Icon')],
                    'weight': item_value.get('Weight', '1'),
                    'hunger': item_value.get('HungerChange', '0'),
                    'calories': item_value.get('Calories', '0'),
                    'carbohydrates': item_value.get('Carbohydrates', '0'),
                    'lipids': item_value.get('Lipids', '0'),
                    'proteins': item_value.get('Proteins', '0')
                })
    
    return items


def main():
    script_parser.init()
    items = get_items()
    write_to_output(items)
                

if __name__ == "__main__":
    main()