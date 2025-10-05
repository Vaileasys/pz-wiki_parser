import os
from scripts.objects.animal_part import AnimalPart, AnimalMeat, AnimalMeatVariant
from scripts.objects.animal import Animal, AnimalBreed
from scripts.objects.item import Item
from scripts.utils import echo, table_helper, util
from scripts.core.constants import BOT_FLAG, BOT_FLAG_END, ANIMAL_DIR
from scripts.core.file_loading import write_file

root_path = os.path.join(ANIMAL_DIR, "products")
root_path_parts = os.path.join(root_path, "butchering_parts")
root_path_meat = os.path.join(root_path, "butchering_meat_")

def generate_data(breed: AnimalBreed) -> dict[str, str]:
    carcass: AnimalPart = breed.parts

    results = {}
    meats = []

    all_one = { "ground": "1", "hook": "1", "ground_roadkill": "1", "hook_roadkill": "1" }

    if carcass.head:
        # Will always be one
        results[carcass.head] = all_one
    if carcass.skull:
        bones = all_one.copy()
        bones["is_bone"] = True
        # Will always be one
        results[carcass.skull] = bones
    if carcass.leather:
        # No leather if from ground, unless it's a baby
        if breed.animal.baby:
            products = all_one
        else:
            products = { "ground": "0", "hook": "1", "ground_roadkill": "0", "hook_roadkill": "1" }
        results[carcass.leather] = products
    if breed.feather_item:
        # Animal should also drop feathers
        item = breed.feather_item
        feather_str = "≤" + str(breed.max_feather)
        products = { "ground": feather_str, "hook": feather_str, "ground_roadkill": feather_str, "hook_roadkill": feather_str }
        results[item] = products

    for part in carcass.parts:
        item = Item(part.get("item"))
        products, meat = get_parts(part, breed)
        if meat:
            meats.append(meat)
        results[item] = products
    
    for bone in carcass.bones:
        item = Item(bone.get("item"))
        products, _ = get_parts(bone, breed)
        products["is_bone"] = True
        results[item] = products
    
    return results, meats

def get_parts(part: dict, breed: AnimalBreed):
    meat = None
    if not isinstance(part, dict):
        ground = "1"
        hook = "1"
        ground_roadkill = "1"
        hook_roadkill = "1"

    elif part.get("nb"):
        value = str(part.get("nb"))
        ground = value
        hook = value
        ground_roadkill = value
        hook_roadkill = value

    else:
        item = Item(part.get("item"))

        base_min = part.get("minNb")
        base_max = part.get("maxNb")
        
        # Ground and hook affects all items that have a minNb and maxNb value
        ground_min = base_min * 0.6
        ground_max = base_max * 0.6
        hook_min = base_min * 1.2
        hook_max = base_max * 1.2

        # Game's check for applying meatRatio is if it's a Food object
        if item.type == "Food":
            ground_min *= breed.meat_ratio[0]
            ground_max *= breed.meat_ratio[1]
            hook_min *= breed.meat_ratio[0]
            hook_max *= breed.meat_ratio[1]

            if AnimalMeat.exists(item.item_id):
                meat = AnimalMeat(item.item_id)
        
        ground = f"{round(ground_min):.0f}–{round(ground_max):.0f}"
        hook = f"{round(hook_min):.0f}–{round(hook_max):.0f}"
        ground_roadkill = f"{round(ground_min / 2):.0f}–{round(ground_max / 2):.0f}"
        hook_roadkill = f"{round(hook_min / 2):.0f}–{round(hook_max / 2):.0f}"

    products = {
        "ground": ground,
        "hook": hook,
        "ground_roadkill": ground_roadkill,
        "hook_roadkill": hook_roadkill
        }

    return products, meat

def do_meat_table(meats: list[AnimalMeat], breed: AnimalBreed, stat: str = "hunger"):
    if not meats: # skip creating table because we have nothing to add
        return

    content = []

    bot_flag_start = BOT_FLAG.format(type=f"meat_{stat}", id=breed.full_breed_id)
    bot_flag_end = BOT_FLAG_END.format(type=f"meat_{stat}", id=breed.full_breed_id)

    content.append(bot_flag_start + table_helper.TABLE_WRAP_BEFORE + table_helper.DEF_TABLE_HEADER)
    # Animals that don't have a butchers hook entry in AnimalAvatarDefintion.lua can't be hooked
    content.append(f"|+ ''{stat.capitalize()} at different cuts''")
    if breed.animal.can_be_hooked:
        content.extend([
            '! rowspan="2" | Icon',
            '! rowspan="2" | Name',
            '! colspan="2" | Ground',
            '! colspan="2" | Hook',
            '|-',
            '! Normal',
            '! Roadkill',
            '! Normal',
            '! Roadkill'
        ])
    else:
        content.extend([
            '! Icon',
            '! Name',
            '! Normal',
            '! Roadkill'
        ])
    
    for meat in meats:

        # Check if meat is valid, else we skip it
        if not meat.is_valid:
            echo.warning(f"'{meat.item_id}' doesn't exist in the item data. Skipping.")
            continue

        meat_ratio = breed.meat_ratio

        variants = get_meat_variants(meat, meat_ratio, breed)

        for variant in variants:

            content.append("|-")
            # Animals that don't have a butchers hook entry in AnimalAvatarDefintion.lua can't be hooked
            content.extend([
                "| " + variant.get("icon"), # icon
                "| " + variant.get("link"), # name
                "| " + variant.get(f"{stat}_ground"), # normal
                "| " + variant.get(f"{stat}_ground_roadkill"), # roadkill
            ])
            if breed.animal.can_be_hooked:
                content.extend([
                "| " + variant.get(f"{stat}_hook"), # normal
                "| " + variant.get(f"{stat}_hook_roadkill"), # roadkill
                ])

    content.append(table_helper.DEF_TABLE_FOOTER + table_helper.TABLE_WRAP_AFTER + bot_flag_end)

    write_file(content, rel_path=breed.full_breed_id + ".txt", root_path=root_path_meat + stat)


def get_meat_variants(meat: AnimalMeat, meat_ratio: list, breed: AnimalBreed) -> list[dict]:

    variants = []
    for variant in meat.variants:
        values = {}
        item = variant.item

        values["name"] = variant.name
        values["link"] = variant.wiki_link
        values["icon"] = item.icon

        hunger_boost = variant.hunger_boost if variant.hunger_boost else 1

        ## ------ HUNGER ------ ##
        base_hunger = item.hunger_change

        # Hook
        hunger, hunger_roadkill = calculate_meat(base_hunger, hunger_boost, meat_ratio)
        values["hunger_hook"] = f"{hunger[0]:.0f}–{hunger[1]:.0f}"
        values["hunger_hook_roadkill"] = f"{hunger_roadkill[0]:.0f}–{hunger_roadkill[1]:.0f}"

        # Ground
        hunger, hunger_roadkill = calculate_meat(base_hunger, hunger_boost, meat_ratio, ground=True)
        values["hunger_ground"] = f"{hunger[0]:.0f}–{hunger[1]:.0f}"
        values["hunger_ground_roadkill"] = f"{hunger_roadkill[0]:.0f}–{hunger_roadkill[1]:.0f}"

        ## ------ CALORIES ------ ##
        calories_base = item.calories

        # Hook
        calories, calories_roadkill = calculate_meat(calories_base, hunger_boost, meat_ratio)
        values["calories_hook"] = f"{calories[0]:.0f}–{calories[1]:.0f}"
        values["calories_hook_roadkill"] = f"{calories_roadkill[0]:.0f}–{calories_roadkill[1]:.0f}"

        # Ground
        calories, calories_roadkill = calculate_meat(calories_base, hunger_boost, meat_ratio, ground=True)
        values["calories_ground"] = f"{calories[0]:.0f}–{calories[1]:.0f}"
        values["calories_ground_roadkill"] = f"{calories_roadkill[0]:.0f}–{calories_roadkill[1]:.0f}"

        ## ------ CARBOHYDRATES ------ ##
        carbohydrates_base = item.carbohydrates

        # Hook
        carbohydrates, carbohydrates_roadkill = calculate_meat(carbohydrates_base, hunger_boost, meat_ratio)
        values["carbohydrates_hook"] = f"{carbohydrates[0]:.0f}–{carbohydrates[1]:.0f}"
        values["carbohydrates_hook_roadkill"] = f"{carbohydrates_roadkill[0]:.0f}–{carbohydrates_roadkill[1]:.0f}"

        # Ground
        carbohydrates, carbohydrates_roadkill = calculate_meat(carbohydrates_base, hunger_boost, meat_ratio, ground=True)
        values["carbohydrates_ground"] = f"{carbohydrates[0]:.0f}–{carbohydrates[1]:.0f}"
        values["carbohydrates_ground_roadkill"] = f"{carbohydrates_roadkill[0]:.0f}–{carbohydrates_roadkill[1]:.0f}"

        ## ------ PROTEINS ------ ##
        proteins_base = item.proteins

        # Hook
        proteins, proteins_roadkill = calculate_meat(proteins_base, hunger_boost, meat_ratio)
        values["proteins_hook"] = f"{proteins[0]:.0f}–{proteins[1]:.0f}"
        values["proteins_hook_roadkill"] = f"{proteins_roadkill[0]:.0f}–{proteins_roadkill[1]:.0f}"

        # Ground
        proteins, proteins_roadkill = calculate_meat(proteins_base, hunger_boost, meat_ratio, ground=True)
        values["proteins_ground"] = f"{proteins[0]:.0f}–{proteins[1]:.0f}"
        values["proteins_ground_roadkill"] = f"{proteins_roadkill[0]:.0f}–{proteins_roadkill[1]:.0f}"

        ## ------ LIPIDS ------ ##
        lipids_base = item.lipids

        # Hook
        lipids, lipids_roadkill = calculate_meat(lipids_base, hunger_boost, meat_ratio)
        values["lipids_hook"] = f"{lipids[0]:.0f}–{lipids[1]:.0f}"
        values["lipids_hook_roadkill"] = f"{lipids_roadkill[0]:.0f}–{lipids_roadkill[1]:.0f}"

        # Ground
        lipids, lipids_roadkill = calculate_meat(lipids_base, hunger_boost, meat_ratio, ground=True)
        values["lipids_ground"] = f"{lipids[0]:.0f}–{lipids[1]:.0f}"
        values["lipids_ground_roadkill"] = f"{lipids_roadkill[0]:.0f}–{lipids_roadkill[1]:.0f}"

        variants.append(values)

    return variants


def calculate_meat(
        base_value: float|int,
        hunger_boost: float|int,
        meat_ratio: list[float],
        ground: bool = False
        ) -> list[list[int]]:
    
    if ground:
        hunger_boost = hunger_boost * 0.6

    meat_ratio_roadkill = [0.2, 0.4]

    # Normal
    ratio_min = meat_ratio[0] * hunger_boost
    ratio_max = meat_ratio[1] * hunger_boost
    value_min = round(abs(base_value * ratio_min * 0.9))
    value_max = round(abs(base_value * ratio_max * 1.1))
    value = [value_min, value_max]

    # Roadkill
    ratio_roadkill_min = meat_ratio_roadkill[0] * hunger_boost
    ratio_roadkill_max = meat_ratio_roadkill[1] * hunger_boost
    value_roadkill_min = round(abs(base_value * ratio_roadkill_min * 0.9))
    value_roadkill_max = round(abs(base_value * ratio_roadkill_max * 1.1))
    value_roadkill = [value_roadkill_min, value_roadkill_max]

    return value, value_roadkill


def do_parts_table(results: dict[Item, dict[str, str]], breed: AnimalBreed) -> list[str]:
    content = []

    bot_flag_start = BOT_FLAG.format(type="butchering_parts", id=breed.full_breed_id)
    bot_flag_end = BOT_FLAG_END.format(type="butchering_parts", id=breed.full_breed_id)

    content.append(bot_flag_start + table_helper.TABLE_WRAP_BEFORE + table_helper.DEF_TABLE_HEADER)
    # Animals that don't have a butchers hook entry in AnimalAvatarDefintion.lua can't be hooked
    can_be_hooked = breed.animal.can_be_hooked
    if can_be_hooked:
        content.extend([
            '! rowspan="2" | Icon',
            '! rowspan="2" | Name',
            '! colspan="2" | Ground',
            '! colspan="2" | Hook',
            '|-',
            '! Normal',
            '! Roadkill',
            '! Normal',
            '! Roadkill'
        ])
    else:
        content.extend([
            '! Icon',
            '! Name',
            '! Normal',
            '! Roadkill'
        ])
    
    is_bone = False # Flag to indicate if there are any bones in the table
    for item, products in results.items():

        # Check if item is valid, else we skip it
        if not item.valid:
            echo.warning(f"'{item.item_id}' doesn't exist in the item data. Skipping.")
            continue
        
        bone = ""
        if products.get("is_bone"):
            bone = " {{Footnote|*|name=*}}" # Add asterisk for the bone note
            is_bone = True

        content.append("|-")
        content.extend([
            "| " + item.icon,
            "| " + item.wiki_link + bone,
            "| " + products.get("ground"),
            "| " + products.get("ground_roadkill"),
        ])
        if can_be_hooked:
            content.extend([
            "| " + products.get("hook"),
            "| " + products.get("hook_roadkill")
            ])
    footnote = "{{Footnote|*|Obtained from an animal skeleton.|name=*}}" if is_bone else ""
    content.append(
        table_helper.DEF_TABLE_FOOTER + footnote + table_helper.TABLE_WRAP_AFTER + bot_flag_end)
    
    write_file(content, rel_path=breed.full_breed_id + ".txt", root_path=root_path_parts)


def main():
    for _, breed in AnimalBreed.all().items():
        products, meats = generate_data(breed)
    
        do_parts_table(products, breed)

        do_meat_table(meats, breed, "hunger")
        do_meat_table(meats, breed, "calories")
        do_meat_table(meats, breed, "carbohydrates")
        do_meat_table(meats, breed, "proteins")
        do_meat_table(meats, breed, "lipids")


if __name__ == "__main__":
    main()