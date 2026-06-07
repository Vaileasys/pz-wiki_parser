[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_codesnip.md) | [Next File](tiles_infobox.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)

# tiles_container_mapping.py

Project Zomboid Wiki Container Mapping Generator

This script processes the tiles cache to create a mapping of container types to their
associated tile textures. It identifies tiles that have a non-empty "container" property
in their generic properties and groups them by container type.

The output is a JSON file that maps container types to lists of tile textures that
belong to that container type, useful for wiki organization and cross-referencing.

## Functions

### [`generate_container_mapping(tiles_data: Dict, lang_code: str) -> Dict[str, Dict[str, List[str]]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_container_mapping.py#L21)

Generate container mapping from tiles data.

<ins>**Args:**</ins>
  - **tiles_data (Dict)**:
      - _The loaded tiles cache data_
  - **lang_code (str)**:
      - _Language code for output directory_

<ins>**Returns:**</ins>
  - **Dict[str, Dict[str, List[str]]]**:
      - _Mapping of container types to objects with textures lists_

### [`save_container_mapping(container_mapping: Dict[str, Dict[str, List[str]]], lang_code: str) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_container_mapping.py#L61)

Save each container type to a separate JSON file in the container_mapping directory
and generate a batch file for processing.

<ins>**Args:**</ins>
  - **container_mapping (Dict[str, Dict[str, List[str]]])**:
      - _The container mapping data_
  - **lang_code (str)**:
      - _Language code for output directory_

### [`main(tiles_data: Dict = None, lang_code: str = None) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tiles/tiles_container_mapping.py#L117)

Main function to generate container mapping from tiles data.

<ins>**Args:**</ins>
  - **tiles_data (Dict, optional)**:
      - _Pre-loaded tiles data. If None, loads from cache._
  - **lang_code (str, optional)**:
      - _Language code. If None, gets from Language.get()._


[Previous Folder](../recipes/craft_recipes.md) | [Previous File](tiles_codesnip.md) | [Next File](tiles_infobox.md) | [Next Folder](../tools/batch_processor.md) | [Back to Index](../../index.md)
