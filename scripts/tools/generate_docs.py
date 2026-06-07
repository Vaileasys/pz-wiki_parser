"""Generate Markdown API documentation from the scripts package."""

from __future__ import annotations

import argparse
import ast
import difflib
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
DOCS_DIR = REPO_ROOT / "docs"
GITHUB_BASE_URL = "https://github.com/Vaileasys/pz-wiki_parser/blob/main"


@dataclass(frozen=True)
class DocField:
    name: str
    type_name: str | None = None
    description: str = ""


@dataclass(frozen=True)
class MemberDoc:
    name: str
    kind: str
    signature: str | None
    docstring: str
    line: int
    args: list[DocField] = field(default_factory=list)
    returns: list[DocField] = field(default_factory=list)


@dataclass(frozen=True)
class ClassDoc:
    name: str
    docstring: str
    line: int
    class_methods: list[MemberDoc] = field(default_factory=list)
    static_methods: list[MemberDoc] = field(default_factory=list)
    object_methods: list[MemberDoc] = field(default_factory=list)
    properties: list[MemberDoc] = field(default_factory=list)


@dataclass(frozen=True)
class ModuleDoc:
    source_path: Path
    source_rel: PurePosixPath
    doc_rel: PurePosixPath
    docstring: str
    functions: list[MemberDoc] = field(default_factory=list)
    classes: list[ClassDoc] = field(default_factory=list)


def posix_rel(path: Path, root: Path) -> PurePosixPath:
    """Return a POSIX-style path relative to a root directory."""
    return PurePosixPath(path.relative_to(root).as_posix())


def doc_path_for_source(source_rel: PurePosixPath) -> PurePosixPath:
    """Return the Markdown documentation path for a source file."""
    return source_rel.with_suffix(".md")


def discover_sources(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]:
    """Find Python files that should have generated documentation."""
    return sorted(
        path
        for path in scripts_dir.rglob("*.py")
        if path.name != "__init__.py"
    )


def unparse(node: ast.AST | None) -> str:
    """Convert an AST node back into source-like text."""
    if node is None:
        return ""
    return ast.unparse(node)


def annotation(node: ast.AST | None) -> str | None:
    """Return an annotation as readable text, if one exists."""
    text = unparse(node).strip()
    return text or None


def default_map(args: list[ast.arg], defaults: list[ast.expr]) -> dict[str, ast.expr]:
    """Map positional argument names to their default value nodes."""
    if not defaults:
        return {}
    return {
        arg.arg: default
        for arg, default in zip(args[-len(defaults) :], defaults, strict=False)
    }


def format_arg(arg: ast.arg, default: ast.expr | None = None) -> str:
    """Format one function argument for a generated signature."""
    text = arg.arg
    arg_annotation = annotation(arg.annotation)
    if arg_annotation:
        text += f": {arg_annotation}"
    if default is not None:
        text += f" = {unparse(default)}"
    return text


def function_signature(
    node: ast.FunctionDef | ast.AsyncFunctionDef, *, drop_first_arg: bool = False
) -> str:
    """Build a readable function or method signature."""
    args = node.args
    positional = list(args.posonlyargs) + list(args.args)
    if drop_first_arg and positional:
        positional = positional[1:]

    positional_defaults = default_map(
        list(args.posonlyargs) + list(args.args), list(args.defaults)
    )
    parts: list[str] = []
    for arg in positional:
        parts.append(format_arg(arg, positional_defaults.get(arg.arg)))

    if args.vararg:
        parts.append("*" + format_arg(args.vararg))
    elif args.kwonlyargs:
        parts.append("*")

    for arg, default in zip(args.kwonlyargs, args.kw_defaults, strict=False):
        parts.append(format_arg(arg, default))

    if args.kwarg:
        parts.append("**" + format_arg(args.kwarg))

    signature = f"{node.name}({', '.join(parts)})"
    return_annotation = annotation(node.returns)
    if return_annotation:
        signature += f" -> {return_annotation}"
    return signature


def decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return the simple decorator names used by a function."""
    names = set()
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name):
            names.add(decorator.id)
        elif isinstance(decorator, ast.Attribute):
            names.add(decorator.attr)
        elif isinstance(decorator, ast.Call):
            names.update(decorator_names_from_call(decorator))
    return names


def decorator_names_from_call(node: ast.Call) -> set[str]:
    """Return a decorator name when the decorator is called."""
    func = node.func
    if isinstance(func, ast.Name):
        return {func.id}
    if isinstance(func, ast.Attribute):
        return {func.attr}
    return set()


def clean_docstring(node: ast.AST) -> str:
    """Return a cleaned docstring or an empty string."""
    return ast.get_docstring(node, clean=True) or ""


def parse_field_line(line: str) -> DocField | None:
    """Parse one Args or Returns field from a docstring."""
    stripped = line.strip()
    if not stripped:
        return None
    if ":" in stripped:
        name_part, description = stripped.split(":", 1)
    else:
        name_part, description = stripped, ""

    name_part = name_part.strip()
    description = description.strip()
    type_name = None

    if "(" in name_part and name_part.endswith(")"):
        name, type_part = name_part[:-1].split("(", 1)
        return DocField(name.strip(), type_part.strip(), description)

    return DocField(name_part, type_name, description)


def parse_doc_fields(docstring: str) -> tuple[str, list[DocField], list[DocField]]:
    """Split a docstring into summary, arguments, and returns."""
    lines = docstring.splitlines()
    summary: list[str] = []
    args: list[DocField] = []
    returns: list[DocField] = []
    section: str | None = None
    current_field: DocField | None = None

    for line in lines:
        stripped = line.strip()
        lowered = stripped.lower()
        if lowered in {"args:", "arguments:", "parameters:"}:
            section = "args"
            current_field = None
            continue
        if lowered in {"returns:", "return:"}:
            section = "returns"
            current_field = None
            continue
        if lowered in {"raises:", "yields:", "examples:"}:
            section = None
            current_field = None
            summary.append(line)
            continue

        if section == "args":
            field = parse_field_line(line)
            if field:
                args.append(field)
                current_field = field
            elif current_field and stripped:
                args[-1] = DocField(
                    current_field.name,
                    current_field.type_name,
                    f"{current_field.description} {stripped}".strip(),
                )
                current_field = args[-1]
            continue

        if section == "returns":
            field = parse_field_line(line)
            if field:
                returns.append(field)
                current_field = field
            elif current_field and stripped:
                returns[-1] = DocField(
                    current_field.name,
                    current_field.type_name,
                    f"{current_field.description} {stripped}".strip(),
                )
                current_field = returns[-1]
            continue

        summary.append(line)

    return "\n".join(summary).strip(), args, returns


def member_doc(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    kind: str,
    *,
    drop_first_arg: bool = False,
) -> MemberDoc:
    """Create documentation data for a function-like member."""
    docstring = clean_docstring(node)
    summary, args, returns = parse_doc_fields(docstring)
    return MemberDoc(
        name=node.name,
        kind=kind,
        signature=function_signature(node, drop_first_arg=drop_first_arg),
        docstring=summary,
        line=node.lineno,
        args=args,
        returns=returns,
    )


def parse_module(source_path: Path, repo_root: Path = REPO_ROOT) -> ModuleDoc:
    """Parse one Python file into module documentation data."""
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))
    source_rel = posix_rel(source_path, repo_root)
    functions: list[MemberDoc] = []
    classes: list[ClassDoc] = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(member_doc(node, "function"))
        elif isinstance(node, ast.ClassDef):
            classes.append(parse_class(node))

    return ModuleDoc(
        source_path=source_path,
        source_rel=source_rel,
        doc_rel=doc_path_for_source(source_rel),
        docstring=clean_docstring(tree),
        functions=sorted(functions, key=lambda item: item.line),
        classes=sorted(classes, key=lambda item: item.line),
    )


def parse_class(node: ast.ClassDef) -> ClassDoc:
    """Parse a class and group its documented members."""
    class_methods: list[MemberDoc] = []
    static_methods: list[MemberDoc] = []
    object_methods: list[MemberDoc] = []
    properties: list[MemberDoc] = []

    for child in node.body:
        if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        decorators = decorator_names(child)
        if "property" in decorators:
            summary, args, returns = parse_doc_fields(clean_docstring(child))
            properties.append(
                MemberDoc(
                    name=child.name,
                    kind="property",
                    signature=None,
                    docstring=summary,
                    line=child.lineno,
                    args=args,
                    returns=returns,
                )
            )
        elif "classmethod" in decorators:
            class_methods.append(
                member_doc(child, "class_method", drop_first_arg=True)
            )
        elif "staticmethod" in decorators:
            static_methods.append(member_doc(child, "static_method"))
        else:
            object_methods.append(
                member_doc(child, "object_method", drop_first_arg=True)
            )

    return ClassDoc(
        name=node.name,
        docstring=clean_docstring(node),
        line=node.lineno,
        class_methods=sorted(class_methods, key=lambda item: item.line),
        static_methods=sorted(static_methods, key=lambda item: item.line),
        object_methods=sorted(object_methods, key=lambda item: item.line),
        properties=sorted(properties, key=lambda item: item.line),
    )


def source_url(module: ModuleDoc, line: int) -> str:
    """Build the GitHub source link for a line in a module."""
    return f"{GITHUB_BASE_URL}/{module.source_rel.as_posix()}#L{line}"
    

def relative_link(from_doc: PurePosixPath, to_doc: PurePosixPath) -> str:
    """Build a relative Markdown link between generated docs."""
    from_parts = from_doc.parent.parts
    to_parts = to_doc.parts
    while from_parts and to_parts and from_parts[0] == to_parts[0]:
        from_parts = from_parts[1:]
        to_parts = to_parts[1:]
    return "/".join([".."] * len(from_parts) + list(to_parts))


def index_back_link(doc_rel: PurePosixPath) -> str:
    """Return the relative link from a doc page to the index."""
    return relative_link(doc_rel, PurePosixPath("index.md"))


def nav_line(module: ModuleDoc, modules: list[ModuleDoc]) -> str:
    """Render the navigation links for a module page."""
    folder_groups: dict[PurePosixPath, list[ModuleDoc]] = {}
    for item in modules:
        folder_groups.setdefault(item.doc_rel.parent, []).append(item)
    folders = sorted(folder_groups)
    folder_index = folders.index(module.doc_rel.parent)
    siblings = folder_groups[module.doc_rel.parent]
    sibling_index = siblings.index(module)

    links: list[str] = []
    if folder_index > 0:
        target = folder_groups[folders[folder_index - 1]][0]
        links.append(
            f"[Previous Folder]({relative_link(module.doc_rel, target.doc_rel)})"
        )
    if sibling_index > 0:
        target = siblings[sibling_index - 1]
        links.append(f"[Previous File]({target.doc_rel.name})")
    if sibling_index < len(siblings) - 1:
        target = siblings[sibling_index + 1]
        links.append(f"[Next File]({target.doc_rel.name})")
    if folder_index < len(folders) - 1:
        target = folder_groups[folders[folder_index + 1]][0]
        links.append(f"[Next Folder]({relative_link(module.doc_rel, target.doc_rel)})")
    links.append(f"[Back to Index]({index_back_link(module.doc_rel)})")
    return " | ".join(links)


def render_fields(title: str, fields: list[DocField]) -> list[str]:
    """Render Args or Returns fields as Markdown lines."""
    if not fields:
        return []
    lines = [f"<ins>**{title}:**</ins>"]
    for field in fields:
        type_text = f" ({field.type_name})" if field.type_name else ""
        lines.append(f"  - **{field.name}{type_text}**:")
        if field.description:
            lines.append(f"      - _{field.description}_")
    lines.append("")
    return lines


def render_member(module: ModuleDoc, member: MemberDoc, heading: str) -> list[str]:
    """Render a function, method, or property section."""
    if member.signature:
        label = member.signature
    else:
        label = member.name
    lines = [
        f"{heading} [`{label}`]({source_url(module, member.line)})",
        "",
    ]
    if member.docstring:
        lines.extend([member.docstring, ""])
    lines.extend(render_fields("Args", member.args))
    lines.extend(render_fields("Returns", member.returns))
    return lines


def render_module(module: ModuleDoc, modules: list[ModuleDoc]) -> str:
    """Render one complete module Markdown page."""
    nav = nav_line(module, modules)
    lines = [nav, "", f"# {module.source_rel.name}", ""]
    if module.docstring:
        lines.extend([module.docstring, ""])

    if module.functions:
        lines.extend(["## Functions", ""])
        for function in module.functions:
            lines.extend(render_member(module, function, "###"))

    if module.classes:
        lines.extend(["## Classes", ""])
        for class_doc in module.classes:
            lines.extend(
                [
                    f"### `{class_doc.name}`",
                    "",
                ]
            )
            if class_doc.docstring:
                lines.extend([class_doc.docstring, ""])
            if class_doc.class_methods:
                lines.extend(["#### Class Methods", ""])
                for member in class_doc.class_methods:
                    lines.extend(render_member(module, member, "#####"))
            if class_doc.static_methods:
                lines.extend(["#### Static Methods", ""])
                for member in class_doc.static_methods:
                    lines.extend(render_member(module, member, "#####"))
            if class_doc.object_methods:
                lines.extend(["#### Object Methods", ""])
                for member in class_doc.object_methods:
                    lines.extend(render_member(module, member, "#####"))
            if class_doc.properties:
                lines.extend(["#### Properties", ""])
                for member in class_doc.properties:
                    lines.extend(render_member(module, member, "#####"))

    lines.extend(["", nav, ""])
    return "\n".join(lines)


def render_index(modules: list[ModuleDoc]) -> str:
    """Render the generated documentation index page."""
    lines = ["# Index", "", "## scripts", ""]
    by_folder: dict[PurePosixPath, list[ModuleDoc]] = {}
    for module in modules:
        by_folder.setdefault(module.doc_rel.parent, []).append(module)

    for folder in sorted(by_folder):
        depth = len(folder.parts) - 1
        if depth > 0:
            lines.extend([f"{'#' * (depth + 2)} {folder.name}", ""])
        for module in by_folder[folder]:
            label = module.source_rel.name
            lines.append(f"- [{label}]({module.doc_rel.as_posix()})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_modules(
    scripts_dir: Path = SCRIPTS_DIR, repo_root: Path = REPO_ROOT
) -> list[ModuleDoc]:
    """Parse and sort every source module that should be documented."""
    modules = [parse_module(path, repo_root) for path in discover_sources(scripts_dir)]
    return sorted(modules, key=lambda item: item.doc_rel.as_posix())


def expected_docs(modules: list[ModuleDoc]) -> dict[PurePosixPath, str]:
    """Build the complete set of generated Markdown files."""
    docs = {module.doc_rel: render_module(module, modules) for module in modules}
    docs[PurePosixPath("index.md")] = render_index(modules)
    return docs


def existing_markdown(docs_dir: Path = DOCS_DIR) -> set[PurePosixPath]:
    """Return existing Markdown files under the docs directory."""
    if not docs_dir.exists():
        return set()
    return {
        PurePosixPath(path.relative_to(docs_dir).as_posix())
        for path in docs_dir.rglob("*.md")
    }


def clean_markdown(docs_dir: Path = DOCS_DIR) -> None:
    """Remove generated Markdown files and empty docs folders."""
    if not docs_dir.exists():
        return
    for path in docs_dir.rglob("*.md"):
        path.unlink()
    for directory in sorted(
        [path for path in docs_dir.rglob("*") if path.is_dir()],
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        if not any(directory.iterdir()):
            directory.rmdir()


def write_docs(docs: dict[PurePosixPath, str], docs_dir: Path = DOCS_DIR) -> None:
    """Write all generated docs to disk."""
    clean_markdown(docs_dir)
    docs_dir.mkdir(parents=True, exist_ok=True)
    for rel_path, content in docs.items():
        target = docs_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")


def check_docs(docs: dict[PurePosixPath, str], docs_dir: Path = DOCS_DIR) -> bool:
    """Check whether existing docs match generated output."""
    ok = True
    expected_paths = set(docs)
    existing_paths = existing_markdown(docs_dir)
    stale = sorted(existing_paths - expected_paths)
    missing = sorted(expected_paths - existing_paths)

    for path in stale:
        ok = False
        print(f"Stale doc: {path.as_posix()}")
    for path in missing:
        ok = False
        print(f"Missing doc: {path.as_posix()}")

    for rel_path in sorted(expected_paths & existing_paths):
        current = (docs_dir / rel_path).read_text(encoding="utf-8")
        expected = docs[rel_path]
        if current != expected:
            ok = False
            print(f"Changed doc: {rel_path.as_posix()}")
            diff = difflib.unified_diff(
                current.splitlines(),
                expected.splitlines(),
                fromfile=f"current/{rel_path.as_posix()}",
                tofile=f"expected/{rel_path.as_posix()}",
                lineterm="",
            )
            for index, line in enumerate(diff):
                if index >= 40:
                    print("... diff truncated ...")
                    break
                print(line)
    return ok


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether docs are current without writing files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the documentation generator."""
    args = parse_args(sys.argv[1:] if argv is None else argv)
    modules = build_modules()
    docs = expected_docs(modules)

    if args.check:
        if check_docs(docs):
            print("Docs are current.")
            return 0
        return 1

    write_docs(docs)
    print(f"Generated {len(docs)} Markdown files in {DOCS_DIR}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
