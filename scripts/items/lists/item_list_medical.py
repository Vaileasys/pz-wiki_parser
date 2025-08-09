import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.fluid import Fluid
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "medical_table.json")

table_map = {}

def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    item_dict["hunger"] = util.convert_int(item.hunger_change or "-") if "hunger" in columns else None
    item_dict["fresh"] = item.days_fresh or "-" if "fresh" in  columns else None
    item_dict["rotten"] = item.days_totally_rotten or "-" if "rotten" in  columns else None
    item_dict["effect"] = find_effect(item) if "effect" in columns else None
    if "alcohol_power" in columns:
        alcohol_power = item.alcohol_power
        if item.fluid_container:
            for fluid in item.fluid_container.fluids:
                fluid: Fluid
                if fluid.alcohol:
                    alcohol_power = fluid.alcohol
        item_dict["alcohol_power"] = util.convert_int(alcohol_power)
    item_dict["bandage_power"] = util.convert_int(item.bandage_power) if "bandage_power" in columns else None
    item_dict["capacity"] = (item.capacity or "-") if "capacity" in columns else None

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def find_effect(item: Item):
    effects = {
        "pain": util.link("Pain", "pain"),
        "broken bones": util.link("Health", "broken bones", anchor="Fracture"),
        "cold and flu": util.link("Has a cold", "cold and flu"),
        "endurance": util.link("Endurance", "endurance"),
        "deep wound": util.link("Health", "deep wound", anchor="Deep Wound"),
        "wounds": util.link("Health", "wounds", anchor="Types of injuries"),
        "infection": util.link("Health", "infection", anchor="Wound infection"),
        "Engineer": util.link("Engineer"),
        "sneezes and coughs": util.link("Has a cold", "sneezes and coughs"),
        "unhappiness": util.link("Unhappy", "unhappiness"),
        "panic": util.link("Panic", "panic"),
        "fatigue": util.link("Tired", "fatigue"),
        "Suture Needle": util.link("Suture Needle"),
        "broken glass": util.link("Health", "broken glass", anchor="Lodged Glass Shard"),
        "bullets": util.link("Health", "bullets", anchor="Lodged Bullet"),
        "zombification": util.link("Knox Infection", "zombification"),
        "sleep": util.link("Sleep", "sleep"),
        "anxious": util.link("Stressed", "anxious"),
        "poultice": util.link("Poultice", "poultice"),
        "bandage": util.link("Bandage", "bandage"),
        "Bandages": util.link("Bandage", "Bandages")
    }
    if item.tooltip and item.get("ToolTip") != "Tooltip_UseOnHealthPanel":
        effect = item.tooltip
        for key, link in effects.items():
            if key in effect:
                effect = effect.replace(key, link)

    elif item.type == "Clothing":
        effect = util.link("Clothing")
    elif item.type == "Weapon":
        effect = util.link("Weapon")
    else:
        effect = "-"
    
    return effect


def find_table_type(item: Item):
    if item.can_bandage:
        return "bandage"
    if item.alcohol_power:
        return "disinfectant"
    if item.fluid_container:
        if item.fluid_container.has_fluid("Alcohol"):
            return "disinfectant"
    if (item.food_type == "Herb"
        or item.has_tag("Comfrey")
        or item.has_tag("HerbalTea")
        or item.has_tag("Plantain")
        or item.has_tag("WildGarlic")
        ):
        return "herb"
    if any(x in item.id_type for x in ("Cataplasm", "Poultice")):
        return "poultice"
    if item.has_tag("Pills") or item.type == "Food":
        return "pharmaceutical"
    if item.type == "Container" or "Box" in item.id_type:
        return "package"
    if (item.has_tag("RemoveBullet")
        or item.has_tag("RemoveGlass")
        or item.has_tag("Scissors")
        or item.has_tag("Sharpenable")
        or item.has_tag("MortarPestle")
        or "Needle" in item.id_type
        ):
        return "tools"
    return "other"    

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("medical"):
                table_type, item_dict = generate_data(item)

                # Add table_type to dict if it hasn't been added yet.
                if table_type not in items:
                    items[table_type] = []

                items[table_type].append(item_dict)

                item_count += 1
        
            pbar.update(1)

    echo.info(f"Finished processing {item_count} items for {len(items)} tables.")
    
    return items

def main():
    Language.get()
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)

    items = process_items()

    table_helper.create_tables("medical_item_list", items, table_map=table_map, columns=column_headings, suppress=True, bot_flag_type="medical_item_list", combine_tables=False)

if __name__ == "__main__":
    main()