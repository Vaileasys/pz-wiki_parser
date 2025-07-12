[Previous Folder](../items/lists/item_list.md) | [Previous File](body_locations_list.md) | [Next File](fluid_list.md) | [Next Folder](../objects/attachment.md) | [Back to Index](../../index.md)

# body_parts_list.py

Generates a wiki-formatted table of all BloodLocation values for the modding article.

This script outputs a MediaWiki table showing each BloodLocation name, the associated body parts,
and an image reference. The data is sourced directly from the BloodLocation and BodyPart classes,
and is intended for use in the PZWiki modding documentation.

## Functions

### [`build_links(location: BloodLocation)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/body_parts_list.py#L41)

Builds a single string of internal anchor links for all body parts in a BloodLocation.


<ins>**Args:**</ins>
  - **location (BloodLocation)**:
      - _The location to extract links from._

<ins>**Returns:**</ins>
  - **str:**
      - A string of wiki-formatted anchor links joined with <br> tags.

### [`get_image(blood_location: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/body_parts_list.py#L57)

Returns the appropriate image tag for a given BloodLocation.


<ins>**Args:**</ins>
  - **blood_location (str)**:
      - _The name of the BloodLocation._

<ins>**Returns:**</ins>
  - **str:**
      - A wiki-formatted image link.

### [`generate_content()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/body_parts_list.py#L71)

Builds the full wiki table content for all BloodLocations.


<ins>**Returns:**</ins>
  - **list[str]:**
      - A list of strings representing lines of the wiki table.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/lists/body_parts_list.py#L90)

Entry point for the script. Generates the table and writes it to the output file.



[Previous Folder](../items/lists/item_list.md) | [Previous File](body_locations_list.md) | [Next File](fluid_list.md) | [Next Folder](../objects/attachment.md) | [Back to Index](../../index.md)
