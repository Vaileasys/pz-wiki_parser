[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_infobox_legacy.md) | [Next File](item_literature_titles.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)

# item_lists.py

Menu-based helper module to run item list generators for the PZwiki.

Allows running individual or all item list scripts, each of which generates
wiki-ready tables for specific item categories in Project Zomboid.

## Functions

### [`display_menu(start, page_size, run_directly)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_lists.py#L50)

Displays a page menu of item list modules to choose from.


<ins>**Args:**</ins>
  - **start (int)**:
      - _Index of the first module to display._
  - **page_size (int)**:
      - _Number of modules to display per page._
  - **run_directly (bool)**:
      - _If True, shows 'Quit' instead of 'Back'._

### [`run_module(module_path: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_lists.py#L74)

Dynamically imports and runs a module's main() function.


<ins>**Args:**</ins>
  - **module_path (str)**:
      - _The full import path to the module._

### [`main(run_directly)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_lists.py#L91)

Handles input and navigation for the item list module menu.


<ins>**Args:**</ins>
  - **run_directly (bool)**:
      - _If True, enables quitting directly from the menu._



[Previous Folder](../foraging/foraging_category_infobox.md) | [Previous File](item_infobox_legacy.md) | [Next File](item_literature_titles.md) | [Next Folder](lists/item_list.md) | [Back to Index](../../index.md)
