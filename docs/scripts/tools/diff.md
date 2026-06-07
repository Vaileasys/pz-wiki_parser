[Previous Folder](../tiles/entity_article.md) | [Previous File](batch_processor.md) | [Next File](generate_docs.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)

# diff.py

## Functions

### [`generate_line_diff(old_path: Path, new_path: Path) -> list[dict] | bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L13)

Return grouped diff blocks with full 'old' and 'new' line lists.

### [`compare_dirs(old: dict[str, str], new: dict[str, str], max_workers: int | None = None, use_snapshots: bool = False) -> dict[str, list[str] | dict[str, dict[int, dict[str, str]] | bool]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L40)

Compare two directories and return a dict with added, removed, and changed files.
Includes line-by-line diffs for .lua and .txt files.

### [`save_diff_to_json(diff_data: dict[str, list[str] | dict[str, object]], old: dict[str, str], new: dict[str, str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L113)

Save raw diff to JSON file.

### [`save_diff_to_txt(diff_data: dict[str, list[str] | dict[str, object]], old: dict[str, str], new: dict[str, str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L130)

Save diff as a readable TXT summary.

### [`get_snapshot_file(version: str, name: str = 'media') -> Path`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L180)

### [`scan_game_snapshot(directories: list[Path] = MEDIA_DIRS) -> dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L183)

### [`load_snapshot(version: str, name: str = 'media') -> dict[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L193)

### [`save_snapshot(snapshot: dict[str, str], version: str, name: str = 'media')`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L199)

### [`snapshot_diff(old_version: str, new_version: str, directories: list[Path], name: str = 'media') -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L205)

Loads snapshots and runs a `compare_dirs()` style diff.

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/diff.py#L229)


[Previous Folder](../tiles/entity_article.md) | [Previous File](batch_processor.md) | [Next File](generate_docs.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)
