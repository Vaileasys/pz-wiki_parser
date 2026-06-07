[Previous Folder](../misc/item_merger.md) | [Previous File](navbox_outfits.md) | [Next File](navbox_weapons.md) | [Next Folder](../objects/animal.md) | [Back to Index](../../index.md)

# navbox_schema.py

## Classes

### `NavboxSection`

Represents a single navbox section and its items.

#### Object Methods

##### [`add_item(item: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L10)

Add an item to the section if it is valid and not already present.

<ins>**Args:**</ins>
  - **item (str)**:
      - _Page name or formatted navbox item._

##### [`sort_items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L25)

Sort all items in the section alphabetically.

##### [`to_dict() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L29)

Convert the section into a JSON-ready dictionary.

<ins>**Returns:**</ins>
  - **dict**:
      - _Section data containing the section name and item list._

### `NavboxSchema`

Represents the full navbox JSON schema.

#### Object Methods

##### [`add_section(section_name: str) -> NavboxSection`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L48)

Create or retrieve a navbox section.

<ins>**Args:**</ins>
  - **section_name (str)**:
      - _Name of the section._

<ins>**Returns:**</ins>
  - **NavboxSection**:
      - _Existing or newly created section._

##### [`sort_sections()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L68)

Sort all sections alphabetically.

##### [`sort_sections_by_order(section_order: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L72)

Sort sections by a preferred order, then alphabetically.

##### [`sort_items()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L86)

Sort items in every section.

##### [`validate()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L91)

Validate the navbox schema before export.

Raises:
    ValueError: If the navbox contains invalid or missing data.

##### [`to_dict() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox_schema.py#L113)

Convert the navbox schema into a JSON-ready dictionary.

<ins>**Returns:**</ins>
  - **dict**:
      - _Navbox data containing the table name and sections._


[Previous Folder](../misc/item_merger.md) | [Previous File](navbox_outfits.md) | [Next File](navbox_weapons.md) | [Next Folder](../objects/animal.md) | [Back to Index](../../index.md)
