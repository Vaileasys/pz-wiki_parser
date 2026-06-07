[Previous Folder](../objects/animal.md) | [Previous File](movable_definitions_parser.md) | [Next File](outfit_story_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# outfit_parser.py

## Functions

### [`guid_item_mapping(guid_table)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L8)

Parse the GUID XML table and create a mapping of GUIDs to item names.

### [`parse_outfits(xml_file, guid_mapping)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L24)

Parse the outfits XML file and return a structured JSON based on GUID mapping.

### [`get_outfits()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L113)

Get the parsed outfits data from cache, or parse XML files if cache doesn't exist.

<ins>**Returns:**</ins>
  - **dict**:
      - _Parsed outfits data with MaleOutfits and FemaleOutfits_

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L131)


[Previous Folder](../objects/animal.md) | [Previous File](movable_definitions_parser.md) | [Next File](outfit_story_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
