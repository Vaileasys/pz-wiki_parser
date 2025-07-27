import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "communication_table.json")

table_map = {}

def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    item_dict["mic_range"] = (item.mic_range or "-") if "mic_range" in columns else None
    item_dict["volume_range"] = util.convert_int(item.base_volume_range) if "volume_range" in columns else None
    item_dict["frequency_min"] = util.convert_unit(item.min_channel, "Hz", "k", "M") if "frequency_min" in columns else None
    item_dict["frequency_max"] = util.convert_unit(item.max_channel, "Hz", "k", "M") if "frequency_max" in columns else None
    item_dict["transmit_range"] = (item.transmit_range or "-") if "transmit_range" in columns else None
    item_dict["battery_drain"] = util.calculate_drain_rate(item.use_delta, as_percentage=True) if "battery_drain" in columns else None
    #TODO: confirm values are accurate

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict


def find_table_type(item: Item):
    if item.is_television:
        return "television"
    if item.two_way:
        return "two_way"
    return "radio"
    

def process_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("communication"):
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

    table_helper.create_tables("communication", items, table_map=table_map, columns=column_headings, suppress=True, bot_flag_type="communication_item_list", combine_tables=False)

if __name__ == "__main__":
    main()