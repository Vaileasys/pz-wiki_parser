import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.craft_recipe import CraftRecipe
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "electronic_table.json")

table_map = {}

def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    if "dismantle" in columns: #FIXME: currently returns 1 product. Needs to return correct mapped product. May need work on CraftRecipe
        if item.item_id in CraftRecipe("DismantleMiscElectronics").input_items:
            dismantle_products = CraftRecipe("DismantleMiscElectronics").output_items
        elif item.item_id in CraftRecipe("DismantleElectronics").input_items:
            dismantle_products = CraftRecipe("DismantleElectronics").output_items
        elif item.item_id in CraftRecipe("DismantlePowerBar").input_items:
            dismantle_products = CraftRecipe("DismantlePowerBar").output_items
        for i, product_id in enumerate(dismantle_products):
            product = Item(product_id)
            products = product.icon if product.valid else product_id

        item_dict["dismantle"] = "".join(products)
    item_dict["degradation"] = util.convert_percentage(1 / item.condition_lower_chance_one_in, decimals=1) if "degradation" in columns else None
    item_dict["sound_radius"] = item.sound_radius if "sound_radius" in columns else None
    
    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def find_table_type(item: Item):
    if item.has_tag("Generator"):
        return "generator"
    if "Battery" in item.id_type:
        return "battery"
    if "LightBulb" in item.id_type:
        return "light_bulb"
    if (item.has_tag("MiscElectronic") 
        or item.type == "Radio"
        or item.has_tag("TVRemote")
        or item.item_id in CraftRecipe("DismantleMiscElectronics").input_items
        or item.item_id in CraftRecipe("DismantleElectronics").input_items
        or item.item_id in CraftRecipe("DismantlePowerBar").input_items
        ):
        return "appliance"
    if (item.item_id in CraftRecipe("DismantleMiscElectronics").output_items
        or item.item_id in CraftRecipe("DismantleElectronics").output_items
        or item.item_id in CraftRecipe("DismantlePowerBar").output_items
        or item.item_id in ("Base.RadioReceiver", "Base.RadioTransmitter", "Base.ScannerModule")
        ):
        return "component"
    if (item.item_id in CraftRecipe("MakeRemoteTrigger").output_items
        or item.item_id in CraftRecipe("MakeRemoteControllerV1").output_items
        or item.item_id in CraftRecipe("MakeRemoteControllerV2").output_items
        or item.item_id in CraftRecipe("MakeRemoteControllerV3").output_items
        or item.item_id in CraftRecipe("MakeTimer").output_items
        ):
        return "upgrade"
    return "other"
    

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("electronics"):
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

    table_helper.create_tables("electronic_item_list", items, table_map=table_map, columns=column_headings, suppress=True, bot_flag_type="electronic_item_list", combine_tables=False)

if __name__ == "__main__":
    main()