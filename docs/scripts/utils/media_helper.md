[Previous Folder](../tools/batch_processor.md) | [Previous File](lua_helper.md) | [Next File](table_helper.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)

# media_helper.py

## Functions

### [`parse_code_effects(full_code: str) -> dict[str, str | int | float]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/media_helper.py#L64)

### [`get_code_name(code: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/media_helper.py#L94)

Returns the translated name of a code based on its title ID.

<ins>**Args:**</ins>
  - **code (str)**:
      - _The short effect code, e.g., "BOR", "CRP", "RCP"_

<ins>**Returns:**</ins>
  - **str**:
      - _Translated name if available, or the raw code if not found._

### [`get_icon(code: str, value: int | float = None, size: str = '32px') -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/utils/media_helper.py#L115)

Returns a wiki image for the code's icon, or None if there isn't one.
If it's a recipe (i.e. RCP), this returns None so text can be displayed instead.


[Previous Folder](../tools/batch_processor.md) | [Previous File](lua_helper.md) | [Next File](table_helper.md) | [Next Folder](../vehicles/vehicle_article.md) | [Back to Index](../../index.md)
