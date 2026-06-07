[Previous Folder](../items/lists/item_list_animal_part.md) | [Previous File](attachment_list.md) | [Next File](body_parts_list.md) | [Next Folder](../misc/item_merger.md) | [Back to Index](../../index.md)

# body_locations_list.py

Generates a formatted wiki table listing Project Zomboid body locations, their exclusive relationships,
hidden locations, and associated wearable items.

This script uses parsed `BodyLocation` and `Item` data to build a wiki-compatible table and writes the
output to a text file.

## Functions

### [`build_table(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/body_locations_list.py#L17)

Builds a MediaWiki-formatted table from processed body location data.

<ins>**Args:**</ins>
  - **data (dict)**:
      - _Dictionary of body location metadata including exclusive and hidden locations, and items._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _Lines of the MediaWiki table content._

### [`generate_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/body_locations_list.py#L51)

Gathers all body location data and formats it for table generation.

<ins>**Returns:**</ins>
  - **dict**:
      - _Mapping of location names to their display values including exclusives, hidden locations, and item icons._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/body_locations_list.py#L96)

Entry point. Loads language data, generates body location table content, and writes it to a file.


[Previous Folder](../items/lists/item_list_animal_part.md) | [Previous File](attachment_list.md) | [Next File](body_parts_list.md) | [Next Folder](../misc/item_merger.md) | [Back to Index](../../index.md)
