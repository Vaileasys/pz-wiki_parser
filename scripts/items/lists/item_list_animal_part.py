import os
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.animal_part import AnimalPart, AnimalMeat
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "animal_part_table.json")

table_map = {}
animal_parts_list = []  # List of item ids parsed in AnimalPart class


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
        if item.type == "weapon":
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
    if item.has_tag("AnimalSkull"):
        return "animal_skull"
    elif item.has_tag("AnimalHead"):
        return "animal_head"
    elif item.has_tag("Feather"):
        return "feather"
    elif item.has_tag("AnimalBrain"):
        return "brain"
    elif item.has_tag("AnimalBone") or item.has_tag("LargeAnimalBone"):
        return "bone"
    elif (
        AnimalMeat.exists(item.item_id)
        or item.food_type in ("Poultry", "Game")
        or item.has_tag("Vermin")
    ):
        return "meat"
    elif item.item_id in animal_parts_list:
        for _, parts in AnimalPart.all().items():
            if item.item_id in parts.bone_items:
                return "bone"
            elif item == parts.leather:
                return "leather"
            elif item == parts.head:
                return "animal_head"
            elif item == parts.skull:
                return "animal_skull"
    return "other"


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
    global animal_parts_list
    items = {}
    item_count = 0

    # Collect items
    with tqdm(
        total=Item.count(),
        desc="Processing items",
        bar_format=PBAR_FORMAT,
        unit=" items",
        leave=False,
    ) as pbar:
        pbar.set_postfix_str(f"Collecting animal parts")
        animal_parts = set()
        for _, animal_part in AnimalPart.all().items():
            animal_parts.update(animal_part.all_parts)

        animal_parts_list = animal_parts.copy()  # cache so we can search it later

        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")

            if item.has_category("animal_part"):
                animal_parts.add(item_id)

            pbar.update(1)

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
