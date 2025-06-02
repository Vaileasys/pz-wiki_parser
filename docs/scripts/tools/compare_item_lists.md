[Previous Folder](../tiles/named_furniture_filter.md) | [Next File](item_dict.md) | [Next Folder](../utils/echo.md) | [Back to Index](../../index.md)

# compare_item_lists.py

This script is used to compare 2 txt files for unique item IDs.
The txt files should be in the format of the 'PZwiki:Item_list' article (item_list.py).

## Functions

### [`extract_item_ids(file_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/compare_item_lists.py#L13)

Extracts item IDs from the given file based on the format Base.<item_name>.

### [`get_version(file_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/compare_item_lists.py#L30)

Extracts the version number from the Page version template.

### [`compare_item_ids(file1, file2)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/compare_item_lists.py#L40)

Compares item IDs from two files and returns common and unique item IDs.

### [`write_results(common, unique1, unique2, version1, version2, include_ids)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/compare_item_lists.py#L55)

Writes the comparison results to separate text files with versioned filenames.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/compare_item_lists.py#L80)


[Previous Folder](../tiles/named_furniture_filter.md) | [Next File](item_dict.md) | [Next Folder](../utils/echo.md) | [Back to Index](../../index.md)
