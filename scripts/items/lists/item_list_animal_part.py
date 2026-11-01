import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.animal_part import AnimalPart, AnimalMeat
from scripts.items.groups.animal_part_groups import AnimalPartGroups
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "animal_part_table.json")

table_map = {}


def process_item(item: Item, cut: str = None):
    notes = None

    table_type = find_table_type(item)
    columns = (
        table_map.get(table_type)
        if table_map.get(table_type) is not None
        else table_map.get("default")
    )

    item_dict = {}
    breeds = AnimalPart.get_breeds(item.item_id)

    item_dict["icon"] = item.icon if "icon" in columns else None
    if not cut:
        item_dict["name"] = item.wiki_link if "name" in columns else None
        item_dict["weight"] = (
            util.convert_int(item.weight) if "weight" in columns else None
        )
        item_dict["hunger"] = item.hunger_change if "hunger" in columns else None
    if cut:
        meat = AnimalMeat(item.item_id)
        item_dict["name"] = meat.get_link(cut) if "name" in columns else None
        item_dict["weight"] = (
            util.convert_int(item.weight) if "weight" in columns else None
        )
        item_dict["hunger"] = meat.get_hunger(cut) if "hunger" in columns else None
        notes = "Note: these hunger values are at the upper limit of the potential hunger. There are several factors affecting the hunger value, such as the animal breed, its genes, whether it was roadkill, butchered on the ground or on a hook."
    item_dict["animal"] = (
        ("<br>".join([breed.wiki_link for breed in breeds]) if breeds else "-")
        if "animal" in columns
        else None
    )
    if "weapon" in columns:
        if item.item_type == "weapon":
            weapon = util.tick(text="Can be used as a weapon", link="Weapon")
        else:
            weapon = util.cross(text="Cannot be used as a weapon", link="Weapon")
        item_dict["weapon"] = weapon

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    # Add item_name for sorting
    item_dict["item_name"] = item.name
    item_dict["notes"] = notes if notes else None

    return table_type, item_dict


def find_table_type(item: Item):
    """Return the table key from the shared animal-part classifier."""
    return AnimalPartGroups.find_type(item)


def generate_item(item: Item, items: dict, cut: str = None):
    table_type, item_dict = process_item(item, cut)

    note = item_dict.pop("notes", None)

    # Add table_type to dict if it hasn't been added yet.
    if table_type not in items:
        items[table_type] = [{"notes": [note]}] if note else [{"notes": []}]
    else:
        if note:
            if note not in items[table_type][0]["notes"]:
                items[table_type][0]["notes"].append(note)

    items[table_type].append(item_dict)


def find_items() -> dict:
    items = {}
    item_count = 0

    animal_parts = AnimalPartGroups.get_item_ids()

    # Process items
    with tqdm(
        total=len(animal_parts),
        desc="Processing items",
        bar_format=PBAR_FORMAT,
        unit=" items",
        leave=False,
    ) as pbar:
        for item_id in animal_parts:
            item = Item(item_id)

            if AnimalMeat.exists(item_id):
                for cut in AnimalMeat(item_id).variants:
                    generate_item(item, items, cut)
            else:
                generate_item(item, items)

            item_count += 1
            pbar.update(1)

    echo.info(f"Finished processing {item_count} items for {len(items)} tables.")

    return items


def main():
    Language.get()
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)

    items = find_items()

    table_helper.create_tables(
        "animal_part_item_list",
        items,
        table_map=table_map,
        columns=column_headings,
        suppress=True,
        bot_flag_type="animal_part_item_list",
        combine_tables=False,
    )


if __name__ == "__main__":
    main()
