[Previous Folder](../items/lists/item_list_animal_part.md) | [Next File](body_locations_list.md) | [Next Folder](../misc/item_merger.md) | [Back to Index](../../index.md)

# attachment_list.py

Generates wikitable output for the modding pages `AttachmentType` and `AttachmentsProvided`
on the PZwiki.

This script extracts data from hotbar slot definitions and attachment types,
formats it into MediaWiki tables, and writes them to output files.

## Functions

### [`build_hotbar_table()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/attachment_list.py#L15)

Write table for `AttachmentsProvided` using hotbar slot data.
Skips slots with replacements.

### [`build_attachment_table()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/attachment_list.py#L66)

Write table for `AttachmentType` with `AttachedLocation`, hotbar slots, and item icons.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/attachment_list.py#L108)

Run both hotbar and attachment table builders.


[Previous Folder](../items/lists/item_list_animal_part.md) | [Next File](body_locations_list.md) | [Next Folder](../misc/item_merger.md) | [Back to Index](../../index.md)
