import os
from tqdm import tqdm
from scripts.core.language import Language, Translate
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT, FORAGING_DIR
from scripts.objects.forage import ForagingItem
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "foraging_table.json")

table_map = {}

def generate_data(foraging: ForagingItem, table_type: str):
    item = foraging.item
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    if "count" in columns:
        min = foraging.min_count * item.count_
        max = foraging.max_count * item.count_
        if min == max:
            item_dict["count"] = min
        else:
            item_dict["count"] = f"{min}–{max}"
    item_dict["level"] = foraging.skill if "level" in columns else None
    item_dict["zones"] = (
        'style="text-align:left;" | ' +
        "<br>".join(
            f"{util.link(Translate.get('IGUI_SearchMode_Zone_Names_' + k))}: {v}"
            for k, v in foraging.zones.items()
            )
        ) if "zones" in columns else None
    item_dict["snow_chance"] = (
        f"{foraging.snow_chance}%" if foraging.snow_chance else "-"
        ) if "snow_chance" in columns else None
    item_dict["rain_chance"] = (
        f"{foraging.rain_chance}%" if foraging.rain_chance else "-"
        ) if "rain_chance" in columns else None
    item_dict["day_chance"] = (
        f"{foraging.day_chance}%" if foraging.day_chance else "-"
        ) if "day_chance" in columns else None
    item_dict["night_chance"] = (
        f"{foraging.night_chance}%" if foraging.night_chance else "-"
        ) if "night_chance" in columns else None
    if "available_months" in columns:
        if len(foraging.months) == 12:
            item_dict["available_months"] = "All"
        else:
            item_dict["available_months"] = "<br>".join(foraging.months) or "-"
    item_dict["bonus_months"] = ("<br>".join(foraging.bonus_months) or "-") if "bonus_months" in columns else None
    item_dict["malus_months"] = ("<br>".join(foraging.malus_months) or "-") if "malus_months" in columns else None
    item_dict["poison_chance"] = (
        f"{foraging.poison_chance}%" if foraging.poison_chance else "-"
        ) if "poison_chance" in columns else None
    if "poison_power" in columns:
        if foraging.poison_power_max > 0:
            item_dict["poison_power"] = f"{foraging.poison_power_min}–{foraging.poison_power_max}"
        else:
            item_dict["poison_power"] = "-"
    item_dict["detection_level"] = (foraging.poison_detection_level or "-") if "detection_level" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.page
    
    return item_dict  


def process_items() -> dict:
    items = {}
    item_count = 0
    item_count_sub = 0

    # Get items
    with tqdm(total=ForagingItem.count(), desc="Processing foraging items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for foraging_id, foraging in ForagingItem.items():
            foraging: ForagingItem
            pbar.set_postfix_str(f"Processing: {foraging_id[:30]}")

            categories = foraging.categories
            for table_type in categories:
                item_dict = generate_data(foraging, table_type)

                # Add table_type to dict if it hasn't been added yet.
                if table_type not in items:
                    items[table_type] = []

                items[table_type].append(item_dict.copy())

                item_count_sub += 1

            item_count += 1
        
            pbar.update(1)

    echo.info(f"Finished processing {item_count_sub} ({item_count} unique) items for {len(items)} tables.")
    
    return items

def main():
    Language.get()
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)

    items = process_items()

    table_helper.create_tables("foraging_item_list", items, table_map=table_map, columns=column_headings, root_path=FORAGING_DIR, suppress=True, bot_flag_type="foraging_item_list", combine_tables=False)

if __name__ == "__main__":
    main()