import os
from tqdm import tqdm
from scripts.core.cache import save_cache
from scripts.core.language import Language
from scripts.core.constants import TABLES_DIR, PBAR_FORMAT
from scripts.objects.item import Item
from scripts.objects.craft_recipe import CraftRecipe
from scripts.utils import table_helper, echo, util

TABLE_PATH = os.path.join(TABLES_DIR, "tool_table.json")

table_map = {}


def generate_data(item: Item):
    table_type = find_table_type(item)
    columns = (
        table_map.get(table_type)
        if table_map.get(table_type) is not None
        else table_map.get("default")
    )

    item_dict = {}

    item_dict["icon"] = item.icon if "icon" in columns else None
    item_dict["name"] = item.wiki_link if "name" in columns else None
    item_dict["weight"] = util.convert_int(item.weight) if "weight" in columns else None
    if "weapon" in columns:
        if item.type == "weapon":
            item_dict["weapon"] = util.tick(
                text="Can be used as a weapon", link="Weapon"
            )
        else:
            item_dict["weapon"] = util.cross(
                text="Cannot be used as a weapon", link="Weapon"
            )
    item_dict["types"] = find_types(item) if "types" in columns else None
    item_dict["category"] = item.display_category if "category" in columns else None

    item_dict["item_id"] = item.item_id if "item_id" in columns else None

    # Remove any values that are None
    item_dict = {k: v for k, v in item_dict.items() if v is not None}

    # Ensure column order is correct
    item_dict = {key: item_dict[key] for key in columns if key in item_dict}

    if item.name is None:
        print(f"Missing name for item_id: {item.item_id}")

    # Add item_name for sorting
    item_dict["item_name"] = item.name

    return item_dict


def find_types(item: Item):
    types = []
    if item.has_tag("Screwdriver"):
        types.append("Screwdriver")
    if item.has_tag("BoltCutters"):
        types.append("Bolt Cutters")
    if item.has_tag("DrillWoodPoor", "DrillWood", "DrillMetal"):
        types.append("Drill")
    if item.has_tag("Awl"):
        types.append("Awl")
    if item.has_tag("ChopTree"):
        types.append("Axe")
    if item.has_tag(
        "Hammer",
        "BallPeenHammer",
        "SmithingHammer",
        "ClubHammer",
        "HammerStone",
        "Mallet",
    ):
        types.append("Hammer")
    if item.has_tag("SewingNeedle"):
        types.append("Needle")
    if item.has_tag("CarpentryChisel", "MasonsChisel", "MetalworkingChisel"):
        types.append("Chisel")
    if item.has_tag("ClayTool"):
        types.append("Scupting Tool")
    if item.has_tag("Crowbar"):
        types.append("Crowbar")
    if item.has_tag("File", "SmallFiles"):
        types.append("File")
    if item.has_tag("FleshingTool"):
        types.append("Fleshing Tool")
    if item.has_tag("Saw", "SmallSaw", "CrudeSaw", "MetalSaw"):
        types.append("Saw")
    if item.has_tag("DigPlow"):
        types.append("Plow")
    if item.has_tag("BottleOpener"):
        types.append("Bottle Opener")
    if item.has_tag("SharpKnife"):
        types.append("Knife")
    if item.has_tag("CanOpener"):
        types.append("Can Opener")
    if item.has_tag("Corkscrew"):
        types.append("Corkscrew")
    if item.has_tag("HeadingTool"):
        types.append("Heading Tool")
    if item.has_tag("Whetstone"):
        types.append("Whetstone")
    if item.has_tag("KnappingTool"):
        types.append("Knapping Tool")
    if item.has_tag("KnittingNeedles"):
        types.append("Knitting Needles")
    if item.has_tag("Magnifier"):
        types.append("Magnifier")
    if item.has_tag("MasonsTrowel"):
        types.append("Masons Trowel")
    if item.has_tag("Pliers", "MetalworkingPliers"):
        types.append("Pliers")
    if item.has_tag("MetalworkingPunch", "SmallPunch"):
        types.append("Punch")
    if item.has_tag("RemoveBullet", "RemoveGlass"):
        types.append("Tweezers")
    if item.has_tag("Scissors"):
        types.append("Scissors")
    if item.has_tag("Paintbrush"):
        types.append("Paintbrush")
    if item.has_tag("PickAxe"):
        types.append("Pickaxe")
    if item.has_tag("Wrench", "PipeWrench"):
        types.append("Wrench")
    if item.has_tag("PlasterTrowel"):
        types.append("Plaster Trowel")
    if item.has_tag("RailroadSpikePuller"):
        types.append("Railroad Spike Puller")
    if item.has_tag("SiphonGas"):
        types.append("Siphon Gas")
    if item.has_tag("Shear"):
        types.append("Shear")
    if item.has_tag("SheetMetalSnips", "LightMetalSnips"):
        types.append("Metal Snips")
    if item.has_tag("CrudeTongs", "Tongs"):
        types.append("Tongs")
    if item.has_tag("Sledgehammer"):
        types.append("Sledgehammer")
    if item.has_tag("ClearAshes", "TakeDung"):
        types.append("Scoop")
    if item.has_tag("Thimble"):
        types.append("Thimble")
    if item.has_tag("ViseGrips"):
        types.append("ViseGrips")
    if item.has_tag("WeldingMask"):
        types.append("Welding Mask")
    if item.has_tag("BlowTorch"):
        types.append("BlowTorch")
    if item.has_tag("MixingUtensil"):
        types.append("Mixing Utensil")
    if item.has_tag("FishingRod"):
        types.append("Fishing Rod")
    if item.has_tag("MortarPestle"):
        types.append("Mortar and Pestle")
    if item.has_tag("Scythe"):
        types.append("Scythe")

    if not types:
        return "-"
    return "<br>".join(sorted(types))


def find_crafting_categories(item: Item):
    categories = set()
    for recipe_id, recipe in CraftRecipe.all().items():
        if item.item_id in recipe.input_items:
            categories.add(recipe.category)

    if item.has_category("fishing"):
        categories.add("Fishing")
    if item.has_category("cooking"):
        categories.add("Cooking")
    if item.has_category("gardening"):
        categories.add("Farming")
    if item.has_category("medical"):
        categories.add("Medical")

    categories = list(categories)

    if not categories:
        categories = ["other"]

    return sorted(categories)


def find_table_type(item: Item):
    if not find_crafting_categories(item):
        return "other"
    return "tool"


def process_items() -> dict:
    items = {}
    item_count = 0
    item_count_sub = 0

    # Get items
    with tqdm(
        total=Item.count(),
        desc="Processing items",
        bar_format=PBAR_FORMAT,
        unit=" items",
        leave=False,
    ) as pbar:
        for item_id, item in Item.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item.has_category("tool"):
                item_dict = generate_data(item)

                crafting_categories = find_crafting_categories(item)
                for table_type in crafting_categories:
                    # Add table_type to dict if it hasn't been added yet.
                    if table_type not in items:
                        items[table_type] = []

                    items[table_type].append(item_dict.copy())

                    item_count_sub += 1

                item_count += 1

            pbar.update(1)

    echo.info(
        f"Finished processing {item_count_sub} ({item_count} unique) items for {len(items)} tables."
    )

    return items


def main():
    Language.get()
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)

    items = process_items()

    save_cache(items, "temp_data.json")

    table_helper.create_tables(
        "tool_item_list",
        items,
        table_map=table_map,
        columns=column_headings,
        suppress=True,
        bot_flag_type="tool_item_list",
        combine_tables=False,
    )


if __name__ == "__main__":
    main()
