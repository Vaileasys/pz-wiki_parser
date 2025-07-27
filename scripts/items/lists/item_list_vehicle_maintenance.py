import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "vehicle_maintenance_table.json")

table_map = {}

def process_item(item: Item):
    table_type = find_table_type(item)
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    item_dict["vehicle_type"] = item.vehicle_type_name if "vehicle_type" in columns else None
    item_dict["capacity"] = util.convert_int((item.fluid_container.capacity if item.fluid_container else item.max_capacity)) if "capacity" in columns else None
    item_dict["dampening"] = util.convert_int(item.suspension_damping) if "dampening" in columns else None
    item_dict["compression"] = util.convert_int(item.suspension_compression) if "compression" in columns else None
    item_dict["wheel_friction"] = util.convert_int(item.wheel_friction) if "wheel_friction" in columns else None
    item_dict["brake_force"] = util.convert_int(item.brake_force) if "brake_force" in columns else None
    item_dict["engine_loudness"] = util.convert_int(item.engine_loudness) if "engine_loudness" in columns else None
    item_dict["degradation_standard"] = util.convert_int(item.condition_lower_standard) if "degradation_standard" in columns else None
    item_dict["degradation_offroad"] = util.convert_int(item.condition_lower_offroad) if "degradation_offroad" in columns else None

    item_dict["tools"] = "TBA" if "tools" in columns else None #TODO
    item_dict["skill"] = "TBA" if "skill" in columns else None #TODO
    item_dict["recipe"] = "TBA" if "recipe" in columns else None #TODO

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    
    return table_type, item_dict

def find_table_type(item: Item):
    name = item.item_id.lower()
    if "brake" in name:
        return "brake"
    elif "carbattery" in name and "charger" not in name:
        return "battery"
    elif "carseat" in name:
        return "seat"
    elif "cardoor" in name:
        return "door"
    elif "window" in name or "windshield" in name:
        return "window"
    elif "gastank" in name:
        return "gas_tank"
    elif "glovebox" in name:
        return "glove_box"
    elif "enginedoor" in name:
        return "hood"
    elif "carmuffler" in name:
        return "muffler"
    elif "suspension" in name:
        return "suspension"
    elif "oldtire" in name or "moderntire" in name or "normaltire" in name:
        return "tire"
    elif "trunkdoor" in name:
        return "trunk_lid"
    elif "trunk" in name:
        return "trunk"
    elif "lightbar" in name:
        return "lightbar"
    elif "hoodornament" in name:
        return "hood_ornament"
    return "other"

def find_items() -> dict:
    items = {}
    item_count = 0

    # Get items
    with tqdm(total=Item.count(), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items", leave=False) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("vehicle_maintenance"):
                table_type, item_dict = process_item(item)

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

    items = find_items()

    table_helper.create_tables("vehicle_maintenance", items, table_map=table_map, columns=column_headings, suppress=True, bot_flag_type="vehicle_maintenance_item_list", combine_tables=False)

if __name__ == "__main__":
    main()