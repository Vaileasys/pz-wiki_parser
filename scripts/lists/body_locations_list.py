"""
Generates a formatted wiki table listing Project Zomboid body locations, their exclusive relationships,
hidden locations, and associated wearable items.

This script uses parsed `BodyLocation` and `Item` data to build a wiki-compatible table and writes the
output to a text file.
"""

from scripts.core.language import Language
from scripts.objects.body_location import BodyLocation
from scripts.objects.item import Item
from scripts.utils.util import link
from scripts.core.file_loading import write_file

OUTPUT_FILE = "bodylocations_exclusives.txt"

def build_table(data: dict):
    """
    Builds a MediaWiki-formatted table from processed body location data.

    Args:
        data (dict): Dictionary of body location metadata including exclusive and hidden locations, and items.

    Returns:
        list[str]: Lines of the MediaWiki table content.
    """
    content = [
        '{| class="wikitable theme-blue"',
        '! Location',
        '! Exclusive locations',
        '! Hidden locations',
        '! Items'
    ]

    for k, v in data.items():
        content.extend((
            f'|- id="{v.get("location")}"',
            f'| {v.get("location")}',
            f'| {v.get("exclusive")}',
            f'| {v.get("hidden")}',
            f'| {v.get("items")}'
        ))
    
    content.append('|}')

    return content


def generate_data():
    """
    Gathers all body location data and formats it for table generation.

    Returns:
        dict: Mapping of location names to their display values including exclusives, hidden locations, and item icons.
    """
    location_data = {}

    for loc_id in BodyLocation.all():
        loc = BodyLocation(loc_id)

        location = loc.name

        exclusive = []
        excl_locs = loc.exclusive
        for excl_loc in excl_locs:
            exclusive.append(link(f"#{excl_loc.name}", excl_loc.name))
        exclusive = " &bull; ".join(exclusive) if exclusive else "-"
        
        hidden = []
        hidden_locs = loc.hide_model
        for hidden_loc in hidden_locs:
            hidden.append(link(f"#{hidden_loc.name}", hidden_loc.name))
        hidden = " &bull; ".join(hidden) if hidden else "-"

        items = []
        item_ids = loc.items
        for item_id in item_ids:
            item = Item(item_id)
            if item.icon not in items:
                items.append(item.icon)
        items = "".join(items) if items else "-"
        
        location_data[location] = {
            "location": location,
            "exclusive": exclusive,
            "hidden": hidden,
            "items": items,
        }

    return dict(sorted(location_data.items()))


def main():
    """
    Entry point. Loads language data, generates body location table content, and writes it to a file.
    """
    Language.get()
    location_data = generate_data()
    content = build_table(location_data)
    write_file(content, rel_path=OUTPUT_FILE)


if __name__ == "__main__":
    main()