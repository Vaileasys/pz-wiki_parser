[Previous Folder](../objects/attachment.md) | [Next File](distribution_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# distribution_container_parser.py

## Functions

### [`get_distribution_data()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_container_parser.py#L13)
### [`convert_list_to_dict(data)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_container_parser.py#L18)

Converts lists with alternating key-value pairs into dicts.

E.g. ["Apple", 8, "Banana", 10] -> {"Apple": 8, "Banana": 10}

### [`sort_proc_list(item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_container_parser.py#L36)

Sorts keys within procList.

### [`sort_keys(data, is_top_level)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_container_parser.py#L49)

Sorts data:

- Top-level: lowercase first keys are first, then uppercase, with each group sorted alphabetically.
- Nested: boolean keys first.
- Special case for procList items.

### [`init()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/distribution_container_parser.py#L86)


[Previous Folder](../objects/attachment.md) | [Next File](distribution_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
