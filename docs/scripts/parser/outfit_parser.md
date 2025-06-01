[Previous Folder](../objects/components.md) | [Previous File](movable_definitions_parser.md) | [Next File](radio_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# outfit_parser.py

## Functions

### [`get_outfits()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L12)

_Returns the generated outfit data._
### [`translate_outfit_name(outfit_label)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L18)
### [`generate_translated_names(outfits_json)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L27)

_Generate a dictionary of translated names based on outfit labels._
### [`guid_item_mapping(guid_table)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L33)

_Parse the GUID XML table and create a mapping of GUIDs to item names._
### [`parse_outfits(xml_file, guid_mapping)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L49)

_Parse the outfits XML file and return a structured JSON based on GUID mapping._
### [`generate_articles(outfits_json, output_dir, translated_names)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L96)
### [`generate_name_guid_table(translated_names, outfits_json, output_file)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L206)

_Generate a name-GUID table for all outfits (with gendered labels) and save it to the specified file._
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/outfit_parser.py#L238)

_Main function to process XML files, generate JSON, and create articles._


[Previous Folder](../objects/components.md) | [Previous File](movable_definitions_parser.md) | [Next File](radio_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
