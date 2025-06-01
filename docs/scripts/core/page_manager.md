[Previous Folder](../article_content/hotbar_slots_content.md) | [Previous File](logger.md) | [Next File](setup.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# page_manager.py

## Functions

### [`get_ids(page, id_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L18)

_Returns a list of ids for a given page and id_type._

<ins>**Args:**</ins>
  - **page (str)**:
      - _Page name._
  - **id_type (str)**:
      - _The id type key (default: 'item_id')._

<ins>**Returns:**</ins>
  - **list[str] or None:**
      - List of ids if found.
### [`get_pages(query_id: str, id_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L32)

_Returns a list of pages for a given id._

<ins>**Args:**</ins>
  - **query_id (str)**:
      - _The id to search for._
  - **id_type (str, optional)**:
      - _Restrict search to this id type. Defaults to searching all._

<ins>**Returns:**</ins>
  - **list[str] or None:**
      - List of pages if found, else None.
### [`get_categories(page)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L58)

_Returns the list of categories for the given page._

<ins>**Args:**</ins>
  - **page (str)**:
      - _Wiki page name._

<ins>**Returns:**</ins>
  - **list:**
      - Category names if found, else an empty list.
### [`get_id_categories(script_id, id_type)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L71)

_Returns the list of categories for the given script_id._

<ins>**Args:**</ins>
  - **script_id (str)**:
      - _Full ID like 'Base.Axe'._
  - **id_type (str)**:
      - _Key name to look up IDs (default: 'item_id')._

<ins>**Returns:**</ins>
  - **list:**
      - Category names if found, else an empty list.
### [`get_id_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L90)

_Returns the page dictionary organised with the id as the key._
### [`get_flattened_page_dict()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L98)

_Returns the flattened page dictionary, removing first-level keys (item, tile, vehicle)._
### [`get_raw_page_dict()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L106)

_Returns the raw page dictionary data._
### [`_flatten_page_dict()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L112)

_Flattens the page dictionary into a single-level dict._
### [`_restructure_id_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L121)

_Restructures the flattened page dict so the key is the id, and page is the value._
### [`load(filepath)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L141)

_Load the page dictionary data from file if not already loaded._
### [`init()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/page_manager.py#L148)

_Initialise all data, storing in cache._


[Previous Folder](../article_content/hotbar_slots_content.md) | [Previous File](logger.md) | [Next File](setup.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
