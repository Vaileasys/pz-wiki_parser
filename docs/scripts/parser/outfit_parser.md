[Previous Folder](../objects/attachment.md) | [Previous File](movable_definitions_parser.md) | [Next File](radio_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# outfit_parser.py

## Functions

### [`get_outfits()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L11)

Returns the generated outfit data.

### [`translate_outfit_name(outfit_label)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L17)
### [`generate_translated_names(outfits_json)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L26)

Generate a dictionary of translated names based on outfit labels.

### [`guid_item_mapping(guid_table)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L32)

Parse the GUID XML table and create a mapping of GUIDs to item names.

### [`parse_outfits(xml_file, guid_mapping)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L48)

Parse the outfits XML file and return a structured JSON based on GUID mapping.

### [`generate_articles(outfits_json, output_dir, translated_names)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L95)
### [`generate_name_guid_table(translated_names, outfits_json, output_file)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L205)

Generate a name-GUID table for all outfits (with gendered labels) and save it to the specified file.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L237)

Main function to process XML files, generate JSON, and create articles.



[Previous Folder](../objects/attachment.md) | [Previous File](movable_definitions_parser.md) | [Next File](radio_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
