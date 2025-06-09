[Next File](distribution.md) | [Next Folder](core/cache.md) | [Back to Index](../index.md)

# consumables.py

## Functions

### [`get_item()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/consumables.py#L9)
### [`get_icon_variant(item_id: str, variant: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/consumables.py#L18)

Gets an icon for a specific variant. Returns the base icon if there is no variant defined or it doesn't exist.


<ins>**Args:**</ins>
  - **item_id (str)**:
      - _The Item ID to get the icon for._
  - **variant (str, optional)**:
      - _The variant type to find and output if it exists. Defaults to None._

<ins>**Returns:**</ins>
  - **str:**
      - The icon for the defined variant. Will return the base icon if the variant isn't defined or doesn't exist.

### [`is_egg(tags)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/consumables.py#L52)
### [`write_to_output(item_data, item_id, output_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/consumables.py#L62)
### [`process_item(item_data, item_id, output_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/consumables.py#L100)
### [`automatic_extraction(output_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/consumables.py#L104)
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/consumables.py#L113)


[Next File](distribution.md) | [Next Folder](core/cache.md) | [Back to Index](../index.md)
