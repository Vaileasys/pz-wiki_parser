[Previous Folder](../objects/animal.md) | [Previous File](item_parser.md) | [Next File](literature_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# java_parser.py

## Functions

### [`parse_game_version() -> list[int, int, int]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/java_parser.py#L11)

Parse game version from Core.java.

### [`parse_static_registry(java_path: Path, java_type: str, *, grouped: bool = False) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/java_parser.py#L36)

Parse static final declarations of a given Java type.

Extracts constant names and their string values from a Java file.

<ins>**Args:**</ins>
  - **java_path (Path)**:
      - _Path to the Java file._
  - **java_type (str)**:
      - _The Java type to parse._
  - **grouped (bool, optional)**:
      - _Whether to group constants by their enclosing class. Defaults to False._

<ins>**Returns:**</ins>
  - **dict**:
      - _A dictionary mapping constant values to their names, optionally grouped by class._

### [`process_registry(java_type: str, java_path: Path, output_path: Path, res_path: Path, *, grouped: bool = False, is_update: bool = False, label: str | None = None, do_flip: bool = False) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/java_parser.py#L76)

### [`update_item_keys(is_update: bool = False) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/java_parser.py#L118)

### [`update_item_body_locations(is_update: bool = False) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/java_parser.py#L130)

### [`main(is_update: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/java_parser.py#L140)


[Previous Folder](../objects/animal.md) | [Previous File](item_parser.md) | [Next File](literature_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
