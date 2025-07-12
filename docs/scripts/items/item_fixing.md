[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_distribution.md) | [Next File](item_infobox.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)

# item_fixing.py

Processes and generates [Fixing](https://pzwiki.net/wiki/Template:Fixing) templates for items.

This script extracts fixing data, formats it into wiki templates, and saves individual
.txt files for each item-fixing combination under the `items/fixing/` directory.

The output is in the following MediaWiki format:

Example:
    {{Fixing
    |name=JS-2000 Shotgun
    |item_id=Base.Shotgun
    |fixer1=[[JS-2000 Shotgun]]
    |fixer1_value=1
    |fixer1_skill=2 [[Aiming]]
    |fixer2=[[Sawed-off JS-2000 Shotgun]]
    |fixer2_value=1
    |fixer2_skill=2 [[Aiming]]
    }}

    {{Fixing
    |name=Hood (Standard Vehicle)
    |item_id=Base.EngineDoor1
    |global_item=[[Welding Torch]]
    |global_item_value=2
    |fixer1=[[Steel Sheet]]
    |fixer1_value=1
    |fixer1_skill=1 [[Welding]]<br>2 [[Mechanics]]
    |fixer2=[[Steel Sheet - Small]]
    |fixer2_value=2
    |fixer2_skill=1 [[Welding]]<br>2 [[Mechanics]]
    |condition_modifier=120%
    }}

## Functions

### [`process_fixers(fixers: list[Fixer])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_fixing.py#L47)

Process a list of Fixer objects into a dictionary of wiki template values.


<ins>**Args:**</ins>
  - **fixers (list[Fixer])**:
      - _List of fixer items used for a single fixing entry._

<ins>**Returns:**</ins>
  - **dict:**
      - A dictionary with fixer names, quantities, and skill requirements, formatted for wiki template usage.

### [`generate_data(item: Item, fixing: Fixing)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_fixing.py#L74)

Generate the base data dictionary for a fixing wiki template.


<ins>**Args:**</ins>
  - **item (Item)**:
      - _The item this fixing applies to._
  - **fixing (Fixing)**:
      - _The corresponding fixing object._

<ins>**Returns:**</ins>
  - **dict:**
      - A dictionary of all relevant wiki template keys and values.

### [`generate_template(data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_fixing.py#L103)

Convert a fixing data dictionary into a list of lines representing a wiki template.


<ins>**Args:**</ins>
  - **data (dict)**:
      - _The fixing data to embed in the template._

<ins>**Returns:**</ins>
  - **list[str]:**
      - Lines forming the complete {{Fixing}} wiki template.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_fixing.py#L125)

Generate and save {{Fixing}} templates for all items with fixings.



[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_distribution.md) | [Next File](item_infobox.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)
