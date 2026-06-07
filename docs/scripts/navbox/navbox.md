[Previous Folder](../misc/item_merger.md) | [Next File](navbox_outfits.md) | [Next Folder](../objects/animal.md) | [Back to Index](../../index.md)

# navbox.py

## Classes

### `Navbox`

Builds and exports navbox JSON data.

#### Object Methods

##### [`__init__(table_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox.py#L11)

Initialise the navbox builder.

<ins>**Args:**</ins>
  - **table_name (str)**:
      - _Display name of the navbox table._

##### [`add_section(section_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox.py#L20)

Create or retrieve a navbox section.

<ins>**Args:**</ins>
  - **section_name (str)**:
      - _Name of the section._

<ins>**Returns:**</ins>
  - **NavboxSection**:
      - _Existing or newly created section._

##### [`add_item(section_name: str, page_name: str, label: str | None = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox.py#L32)

Add an item to a navbox section.

<ins>**Args:**</ins>
  - **section_name (str)**:
      - _Name of the section._
  - **page_name (str)**:
      - _Target page name._
  - **label (str | None, optional)**:
      - _Custom display label._

##### [`sort(*, sections: bool = True, items: bool = True)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox.py#L50)

Sort navbox sections and items.

<ins>**Args:**</ins>
  - **sections (bool, optional)**:
      - _Sort sections alphabetically._
  - **items (bool, optional)**:
      - _Sort items alphabetically._

##### [`sort_sections_by_order(section_order: list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox.py#L64)

Sort sections by a preferred order.

<ins>**Args:**</ins>
  - **section_order (list[str])**:
      - _Preferred section name order._

##### [`to_dict() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox.py#L73)

Convert the navbox into a JSON-ready dictionary.

<ins>**Returns:**</ins>
  - **dict**:
      - _Navbox data._

##### [`to_json() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox.py#L82)

Convert the navbox into formatted JSON.

<ins>**Returns:**</ins>
  - **str**:
      - _Formatted JSON string._

##### [`save(filename: str, output_dir: str | Path | None = None) -> Path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/navbox/navbox.py#L91)

Save the navbox JSON file.

<ins>**Args:**</ins>
  - **filename (str)**:
      - _Output filename._
  - **output_dir (str | Path | None, optional)**:
      - _Output directory path._

<ins>**Returns:**</ins>
  - **Path**:
      - _Path to the saved JSON file._


[Previous Folder](../misc/item_merger.md) | [Next File](navbox_outfits.md) | [Next Folder](../objects/animal.md) | [Back to Index](../../index.md)
