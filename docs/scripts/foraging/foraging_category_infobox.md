[Previous Folder](../fluids/fluid_article.md) | [Next File](foraging_category_profession_list.md) | [Next Folder](../items/item_article.md) | [Back to Index](../../index.md)

# foraging_category_infobox.py

## Functions

### [`generate_data(category: ForageCategory) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/foraging/foraging_category_infobox.py#L12)

Generates an infobox for a foraging category.

:param category: The ForageCategory object to generate the infobox for.
:return: A string containing the formatted infobox.

### [`build_infobox(infobox_data: dict) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/foraging/foraging_category_infobox.py#L61)

Builds an infobox template from the provided parameters.

<ins>**Args:**</ins>
  - **infobox_data (dict)**:
      - _Dictionary of key-value infobox fields._

<ins>**Returns:**</ins>
  - **list[str]**:
      - _A list of lines forming the infobox template._

### [`process_categories() -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/foraging/foraging_category_infobox.py#L79)

Generates infoboxes for a list of specific category IDs and writes output files.

### [`main(lang_code: str = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/foraging/foraging_category_infobox.py#L95)


[Previous Folder](../fluids/fluid_article.md) | [Next File](foraging_category_profession_list.md) | [Next Folder](../items/item_article.md) | [Back to Index](../../index.md)
