[Previous Folder](../tiles/entity_article.md) | [Previous File](diff.md) | [Next File](manual_tile_stitcher.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)

# generate_docs.py

Generate Markdown API documentation from the scripts package.

## Functions

### [`posix_rel(path: Path, root: Path) -> PurePosixPath`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L58)

Return a POSIX-style path relative to a root directory.

### [`doc_path_for_source(source_rel: PurePosixPath) -> PurePosixPath`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L63)

Return the Markdown documentation path for a source file.

### [`discover_sources(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L68)

Find Python files that should have generated documentation.

### [`unparse(node: ast.AST | None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L77)

Convert an AST node back into source-like text.

### [`annotation(node: ast.AST | None) -> str | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L84)

Return an annotation as readable text, if one exists.

### [`default_map(args: list[ast.arg], defaults: list[ast.expr]) -> dict[str, ast.expr]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L90)

Map positional argument names to their default value nodes.

### [`format_arg(arg: ast.arg, default: ast.expr | None = None) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L100)

Format one function argument for a generated signature.

### [`function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef, *, drop_first_arg: bool = False) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L111)

Build a readable function or method signature.

### [`decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L145)

Return the simple decorator names used by a function.

### [`decorator_names_from_call(node: ast.Call) -> set[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L158)

Return a decorator name when the decorator is called.

### [`clean_docstring(node: ast.AST) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L168)

Return a cleaned docstring or an empty string.

### [`parse_field_line(line: str) -> DocField | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L173)

Parse one Args or Returns field from a docstring.

### [`parse_doc_fields(docstring: str) -> tuple[str, list[DocField], list[DocField]]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L194)

Split a docstring into summary, arguments, and returns.

### [`member_doc(node: ast.FunctionDef | ast.AsyncFunctionDef, kind: str, *, drop_first_arg: bool = False) -> MemberDoc`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L253)

Create documentation data for a function-like member.

### [`parse_module(source_path: Path, repo_root: Path = REPO_ROOT) -> ModuleDoc`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L273)

Parse one Python file into module documentation data.

### [`parse_class(node: ast.ClassDef) -> ClassDoc`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L297)

Parse a class and group its documented members.

### [`source_url(module: ModuleDoc, line: int) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L343)

Build the GitHub source link for a line in a module.

### [`relative_link(from_doc: PurePosixPath, to_doc: PurePosixPath) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L348)

Build a relative Markdown link between generated docs.

### [`index_back_link(doc_rel: PurePosixPath) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L358)

Return the relative link from a doc page to the index.

### [`nav_line(module: ModuleDoc, modules: list[ModuleDoc]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L363)

Render the navigation links for a module page.

### [`render_fields(title: str, fields: list[DocField]) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L392)

Render Args or Returns fields as Markdown lines.

### [`render_member(module: ModuleDoc, member: MemberDoc, heading: str) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L406)

Render a function, method, or property section.

### [`render_module(module: ModuleDoc, modules: list[ModuleDoc]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L423)

Render one complete module Markdown page.

### [`render_index(modules: list[ModuleDoc]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L467)

Render the generated documentation index page.

### [`build_modules(scripts_dir: Path = SCRIPTS_DIR, repo_root: Path = REPO_ROOT) -> list[ModuleDoc]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L486)

Parse and sort every source module that should be documented.

### [`expected_docs(modules: list[ModuleDoc]) -> dict[PurePosixPath, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L494)

Build the complete set of generated Markdown files.

### [`existing_markdown(docs_dir: Path = DOCS_DIR) -> set[PurePosixPath]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L501)

Return existing Markdown files under the docs directory.

### [`clean_markdown(docs_dir: Path = DOCS_DIR) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L511)

Remove generated Markdown files and empty docs folders.

### [`write_docs(docs: dict[PurePosixPath, str], docs_dir: Path = DOCS_DIR) -> None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L526)

Write all generated docs to disk.

### [`check_docs(docs: dict[PurePosixPath, str], docs_dir: Path = DOCS_DIR) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L536)

Check whether existing docs match generated output.

### [`parse_args(argv: list[str]) -> argparse.Namespace`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L572)

Parse command line arguments.

### [`main(argv: list[str] | None = None) -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/generate_docs.py#L583)

Run the documentation generator.

## Classes

### `DocField`

### `MemberDoc`

### `ClassDoc`

### `ModuleDoc`


[Previous Folder](../tiles/entity_article.md) | [Previous File](diff.md) | [Next File](manual_tile_stitcher.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)
