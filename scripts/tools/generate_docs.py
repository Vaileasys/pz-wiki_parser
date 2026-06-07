"""Generate HTML API documentation from the scripts package."""

from __future__ import annotations

import argparse
import ast
import difflib
import html
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
DOCS_DIR = REPO_ROOT / "docs"
GITHUB_BASE_URL = "https://github.com/Vaileasys/pz-wiki_parser/blob/main"
CSS_PATH = PurePosixPath("assets/docs.css")
NAV_ICONS = {
    "Home": "icon_home.png",
    "Parent Folder": "icon_skip_backward.png",
    "Previous Folder": "icon_skip_backward.png",
    "Previous File": "icon_previous.png",
    "Next File": "icon_next.png",
    "Next Folder": "icon_skip_forward.png",
}


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


@dataclass(frozen=True)
class PackageDoc:
    source_path: Path
    source_rel: PurePosixPath
    doc_rel: PurePosixPath
    name: str
    summary: str
    description: str


def posix_rel(path: Path, root: Path) -> PurePosixPath:
    """Return a POSIX-style path relative to a root directory."""
    return PurePosixPath(path.relative_to(root).as_posix())


def doc_path_for_source(source_rel: PurePosixPath) -> PurePosixPath:
    """Return the HTML documentation path for a source file."""
    return source_rel.with_suffix(".html")


def doc_path_for_package(source_rel: PurePosixPath) -> PurePosixPath:
    """Return the HTML index path for a package folder."""
    return source_rel.parent / "index.html"


def discover_sources(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]:
    """Find Python files that should have generated documentation."""
    return sorted(
        path
        for path in scripts_dir.rglob("*.py")
        if path.name != "__init__.py"
    )


def discover_packages(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]:
    """Find package marker files that can describe generated folders."""
    return sorted(scripts_dir.rglob("__init__.py"))


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


def split_package_docstring(docstring: str) -> tuple[str, str]:
    """Split a package docstring into short summary and detailed description."""
    parts = [part.strip() for part in docstring.split("\n\n") if part.strip()]
    if not parts:
        return "", ""
    return parts[0], "\n\n".join(parts[1:]).strip()


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


def parse_package(source_path: Path, repo_root: Path = REPO_ROOT) -> PackageDoc:
    """Parse a package __init__.py into folder documentation data."""
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))
    source_rel = posix_rel(source_path, repo_root)
    folder_rel = source_rel.parent
    summary, description = split_package_docstring(clean_docstring(tree))
    return PackageDoc(
        source_path=source_path,
        source_rel=source_rel,
        doc_rel=doc_path_for_package(source_rel),
        name=folder_rel.name,
        summary=summary,
        description=description,
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
    """Build a relative link between generated docs."""
    from_parts = from_doc.parent.parts
    to_parts = to_doc.parts
    while from_parts and to_parts and from_parts[0] == to_parts[0]:
        from_parts = from_parts[1:]
        to_parts = to_parts[1:]
    return "/".join([".."] * len(from_parts) + list(to_parts))


def html_index_back_link(doc_rel: PurePosixPath) -> str:
    """Return the relative link from an HTML page to the HTML index."""
    return relative_link(doc_rel, PurePosixPath("index.html"))


def html_escape(value: str) -> str:
    """Escape text for HTML output."""
    return html.escape(value, quote=True)


def render_html_text(text: str) -> str:
    """Render simple multiline text as HTML paragraphs."""
    paragraphs = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        paragraphs.append(f"<p>{'<br>'.join(html_escape(line) for line in block.splitlines())}</p>")
    return "\n".join(paragraphs)


def slug(value: str) -> str:
    """Return a simple stable id for generated headings."""
    result = []
    for char in value.lower():
        if char.isalnum():
            result.append(char)
        elif result and result[-1] != "-":
            result.append("-")
    return "".join(result).strip("-") or "section"


def render_html_fields(title: str, fields: list[DocField]) -> str:
    """Render Args or Returns fields as an HTML definition list."""
    if not fields:
        return ""
    lines = [f'<h5>{html_escape(title)}</h5>', '<dl class="fields">']
    for field in fields:
        type_text = f" ({field.type_name})" if field.type_name else ""
        lines.append(f"<dt>{html_escape(field.name + type_text)}</dt>")
        description = field.description or "No description."
        lines.append(f"<dd>{html_escape(description)}</dd>")
    lines.append("</dl>")
    return "\n".join(lines)


def render_html_member(module: ModuleDoc, member: MemberDoc) -> str:
    """Render one member block for an HTML module page."""
    label = member.signature or member.name
    lines = ['<section class="member">']
    lines.append(f'<code class="signature">{html_escape(label)}</code>')
    lines.append(
        f'<a class="source" href="{html_escape(source_url(module, member.line))}">source</a>'
    )
    if member.docstring:
        lines.append(render_html_text(member.docstring))
    lines.append(render_html_fields("Args", member.args))
    lines.append(render_html_fields("Returns", member.returns))
    lines.append("</section>")
    return "\n".join(line for line in lines if line)


def render_folder_link(module: ModuleDoc, packages: dict[PurePosixPath, PackageDoc]) -> str:
    """Render a link from a file page back to its folder index."""
    package = packages.get(module.doc_rel.parent)
    if not package:
        return ""
    href = relative_link(module.doc_rel, package.doc_rel)
    folder_name = module.doc_rel.parent.as_posix()
    return (
        '<p class="folder-link">Folder: '
        f'<a href="{html_escape(href)}">{html_escape(folder_name)}</a>'
        "</p>"
    )


def render_parent_back_link(package: PackageDoc, parent_package: PackageDoc) -> str:
    """Render a compact back link above a folder title."""
    href = relative_link(package.doc_rel, parent_package.doc_rel)
    icon_path = relative_link(package.doc_rel, CSS_PATH.parent / NAV_ICONS["Previous File"])
    label = package.doc_rel.parent.parent.as_posix()
    return (
        '<a class="back-link" href="{href}">'
        '<img class="back-icon" src="{icon}" alt="" aria-hidden="true">'
        '<span>{label}</span>'
        '</a>'
    ).format(
        href=html_escape(href),
        icon=html_escape(icon_path),
        label=html_escape(label),
    )


def html_nav_line(module: ModuleDoc, modules: list[ModuleDoc]) -> str:
    """Render navigation links for an HTML module page."""
    folder_groups: dict[PurePosixPath, list[ModuleDoc]] = {}
    for item in modules:
        folder_groups.setdefault(item.doc_rel.parent, []).append(item)
    folders = sorted(folder_groups)
    folder_index = folders.index(module.doc_rel.parent)
    siblings = folder_groups[module.doc_rel.parent]
    sibling_index = siblings.index(module)
    current_html = module.doc_rel

    links: list[tuple[str, PurePosixPath]] = [
        ("Home", PurePosixPath("index.html")),
    ]
    if folder_index > 0:
        links.append(("Previous Folder", folders[folder_index - 1] / "index.html"))
    if sibling_index > 0:
        links.append(("Previous File", siblings[sibling_index - 1].doc_rel))
    if sibling_index < len(siblings) - 1:
        links.append(("Next File", siblings[sibling_index + 1].doc_rel))
    if folder_index < len(folders) - 1:
        links.append(("Next Folder", folders[folder_index + 1] / "index.html"))

    rendered = []
    for label, target in links:
        icon_path = relative_link(current_html, CSS_PATH.parent / NAV_ICONS[label])
        href = html_index_back_link(module.doc_rel) if label == "Home" else relative_link(current_html, target)
        rendered.append(
            '<a class="nav-link" href="{href}">'
            '<img class="nav-icon" src="{icon}" alt="" aria-hidden="true">'
            '<span>{label}</span>'
            '</a>'.format(
                href=html_escape(href),
                icon=html_escape(icon_path),
                label=html_escape(label),
            )
        )
    return f'<nav class="nav">{"".join(rendered)}</nav>'


def render_nav_links(
    current_path: PurePosixPath,
    links: list[tuple[str, PurePosixPath]],
) -> str:
    """Render nav links with icons for a generated page."""
    rendered = []
    for label, target in links:
        icon_path = relative_link(current_path, CSS_PATH.parent / NAV_ICONS[label])
        rendered.append(
            '<a class="nav-link" href="{href}">'
            '<img class="nav-icon" src="{icon}" alt="" aria-hidden="true">'
            '<span>{label}</span>'
            '</a>'.format(
                href=html_escape(relative_link(current_path, target)),
                icon=html_escape(icon_path),
                label=html_escape(label),
            )
        )
    return f'<nav class="nav">{"".join(rendered)}</nav>'


def render_link_list(
    current_path: PurePosixPath,
    title: str,
    links: list[tuple[str, PurePosixPath]],
) -> str:
    """Render a sidebar card with links relative to the current page."""
    lines = ['<aside class="sidebar-card">', f"<h2>{html_escape(title)}</h2>"]
    lines.append('<nav class="sidebar-nav">')
    for label, target in links:
        href = relative_link(current_path, target)
        lines.append(f'<a href="{html_escape(href)}">{html_escape(label)}</a>')
    lines.extend(["</nav>", "</aside>"])
    return "\n".join(lines)


def render_anchor_list(title: str, links: list[tuple[str, str, int]]) -> str:
    """Render a sidebar card with in-page anchor links."""
    lines = ['<aside class="sidebar-card">', f"<h2>{html_escape(title)}</h2>"]
    lines.append('<nav class="sidebar-nav">')
    for label, target, depth in links:
        class_name = "sidebar-parent" if depth == 0 else "sidebar-child"
        lines.append(
            f'<a class="{class_name}" href="#{html_escape(target)}">{html_escape(label)}</a>'
        )
    lines.extend(["</nav>", "</aside>"])
    return "\n".join(lines)


def render_page_layout(nav: str, left: str, content: str, right: str = "") -> str:
    """Render the shared sticky-header and three-column page layout."""
    return "\n".join(
        [
            f'<header class="navbar">{nav}</header>',
            '<div class="doc-layout">',
            f'<div class="doc-sidebar doc-sidebar-left">{left}</div>',
            f'<div class="doc-main">{content}</div>',
            f'<div class="doc-sidebar doc-sidebar-right">{right}</div>',
            "</div>",
        ]
    )


def folder_nav_line(
    package: PackageDoc,
    packages: dict[PurePosixPath, PackageDoc],
) -> str:
    """Render navigation links for a folder index page."""
    links: list[tuple[str, PurePosixPath]] = [("Home", PurePosixPath("index.html"))]
    parent_package = packages.get(package.doc_rel.parent.parent)
    if parent_package and parent_package.doc_rel != package.doc_rel:
        links.append(("Parent Folder", parent_package.doc_rel))
    return render_nav_links(package.doc_rel, links)


def render_module_left_sidebar(
    module: ModuleDoc,
    modules: list[ModuleDoc],
    packages: dict[PurePosixPath, PackageDoc],
) -> str:
    """Render file-page folder navigation."""
    links: list[tuple[str, PurePosixPath]] = []
    package = packages.get(module.doc_rel.parent)
    if package:
        links.append(("Folder Index", package.doc_rel))
    for sibling in modules:
        if sibling.doc_rel.parent == module.doc_rel.parent:
            links.append((sibling.source_rel.name, sibling.doc_rel))
    return render_link_list(module.doc_rel, "Folder", links)


def render_module_right_sidebar(module: ModuleDoc) -> str:
    """Render file-page in-page navigation."""
    links: list[tuple[str, str, int]] = []
    if module.functions:
        links.append(("Functions", "functions", 0))
    if module.classes:
        links.append(("Classes", "classes", 0))
        for class_doc in module.classes:
            links.append((class_doc.name, slug(f"class-{class_doc.name}"), 1))
    return render_anchor_list("On This Page", links)


def render_folder_left_sidebar(
    package: PackageDoc,
    packages: dict[PurePosixPath, PackageDoc],
) -> str:
    """Render folder-page parent and child navigation."""
    folder = package.doc_rel.parent
    links: list[tuple[str, PurePosixPath]] = [("Home", PurePosixPath("index.html"))]
    parent_package = packages.get(folder.parent)
    if parent_package and parent_package.doc_rel != package.doc_rel:
        links.append(("Parent Folder", parent_package.doc_rel))
    child_packages = [
        child
        for child in packages.values()
        if child.doc_rel.parent.parent == folder
    ]
    for child in sorted(child_packages, key=lambda item: item.doc_rel.as_posix()):
        links.append((child.doc_rel.parent.name, child.doc_rel))
    return render_link_list(package.doc_rel, "Folders", links)


def render_folder_right_sidebar(has_folders: bool, has_files: bool) -> str:
    """Render folder-page in-page navigation."""
    links: list[tuple[str, str, int]] = []
    if has_folders:
        links.append(("Folders", "folders", 0))
    if has_files:
        links.append(("Files", "files", 0))
    return render_anchor_list("On This Page", links)


def html_page(title: str, body: str, current_path: PurePosixPath) -> str:
    """Wrap HTML page content with the shared document shell."""
    css_href = relative_link(current_path, CSS_PATH)
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{html_escape(title)} - PZwiki Parser Docs</title>",
            f'<link rel="stylesheet" href="{html_escape(css_href)}">',
            "</head>",
            "<body>",
            '<main class="page">',
            body,
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def render_html_module(
    module: ModuleDoc,
    modules: list[ModuleDoc],
    packages: dict[PurePosixPath, PackageDoc],
) -> str:
    """Render one complete HTML module page."""
    current_path = module.doc_rel
    nav = html_nav_line(module, modules)
    lines = [
        '<article class="content">',
        f"<h1>{html_escape(module.source_rel.name)}</h1>",
    ]
    folder_link = render_folder_link(module, packages)
    if folder_link:
        lines.append(folder_link)
    if module.docstring:
        lines.append(f'<div class="summary">{render_html_text(module.docstring)}</div>')

    if module.functions:
        lines.append('<h2 id="functions">Functions</h2>')
        for function in module.functions:
            lines.append(render_html_member(module, function))

    if module.classes:
        lines.append('<h2 id="classes">Classes</h2>')
        for class_doc in module.classes:
            lines.append(
                f'<h3 id="{html_escape(slug(f"class-{class_doc.name}"))}">{html_escape(class_doc.name)}</h3>'
            )
            if class_doc.docstring:
                lines.append(f'<div class="summary">{render_html_text(class_doc.docstring)}</div>')
            groups = [
                ("Class Methods", class_doc.class_methods),
                ("Static Methods", class_doc.static_methods),
                ("Object Methods", class_doc.object_methods),
                ("Properties", class_doc.properties),
            ]
            for title, members in groups:
                if members:
                    lines.append(f"<h4>{html_escape(title)}</h4>")
                    for member in members:
                        lines.append(render_html_member(module, member))

    lines.append("</article>")
    body = render_page_layout(
        nav,
        render_module_left_sidebar(module, modules, packages),
        "\n".join(lines),
        render_module_right_sidebar(module),
    )
    return html_page(module.source_rel.name, body, current_path)


def render_folder_index(
    package: PackageDoc,
    modules: list[ModuleDoc],
    packages: dict[PurePosixPath, PackageDoc],
) -> str:
    """Render one folder-level index page."""
    folder = package.doc_rel.parent
    nav = folder_nav_line(package, packages)
    files = [module for module in modules if module.doc_rel.parent == folder]
    child_packages = [
        child
        for child in packages.values()
        if child.doc_rel.parent.parent == folder
    ]

    lines = [
        '<article class="content folder-index">',
    ]
    parent_package = packages.get(folder.parent)
    if parent_package and parent_package.doc_rel != package.doc_rel:
        lines.append(render_parent_back_link(package, parent_package))
    lines.append(f'<h1 id="top">{html_escape(folder.as_posix())}</h1>')
    folder_description = package.description or package.summary
    if folder_description:
        lines.append(f'<div class="summary">{render_html_text(folder_description)}</div>')

    if child_packages:
        lines.append('<h2 id="folders">Folders</h2>')
        lines.append('<ul class="index-list">')
        for child in sorted(child_packages, key=lambda item: item.doc_rel.as_posix()):
            href = relative_link(package.doc_rel, child.doc_rel)
            label = child.doc_rel.parent.name
            lines.append(f'<li><a href="{html_escape(href)}">{html_escape(label)}</a></li>')
        lines.append("</ul>")

    if files:
        lines.append('<h2 id="files">Files</h2>')
        lines.append('<ul class="index-list">')
        for module in files:
            href = relative_link(package.doc_rel, module.doc_rel)
            lines.append(
                f'<li><a href="{html_escape(href)}">{html_escape(module.source_rel.name)}</a></li>'
            )
        lines.append("</ul>")

    lines.append("</article>")
    body = render_page_layout(
        nav,
        render_folder_left_sidebar(package, packages),
        "\n".join(lines),
        render_folder_right_sidebar(bool(child_packages), bool(files)),
    )
    return html_page(folder.as_posix(), body, package.doc_rel)


def render_html_index(
    modules: list[ModuleDoc],
    packages: dict[PurePosixPath, PackageDoc],
) -> str:
    """Render the generated HTML index page."""
    by_parent: dict[str, dict[PurePosixPath, list[ModuleDoc]]] = {}
    for module in modules:
        parent = module.doc_rel.parts[0]
        by_parent.setdefault(parent, {}).setdefault(module.doc_rel.parent, []).append(module)

    section_links: list[tuple[str, str, int]] = []
    for parent in sorted(by_parent):
        section_links.append((parent, slug(parent), 0))
        for folder in sorted(by_parent[parent]):
            folder_name = "Root" if folder == PurePosixPath(parent) else folder.relative_to(parent).as_posix()
            section_links.append((folder_name, slug(f"{parent}-{folder_name}"), 1))

    right_sidebar = render_anchor_list("Jump To", section_links)
    left_links = [
        ("Home", PurePosixPath("index.html")),
    ]
    for parent in sorted(by_parent):
        parent_package = packages.get(PurePosixPath(parent))
        if parent_package:
            left_links.append((parent, parent_package.doc_rel))
    left_sidebar = render_link_list(PurePosixPath("index.html"), "Documentation", left_links)

    lines = [
        '<article class="content index-hero">',
        '<h1 id="top">PZwiki Parser Documentation</h1>',
        '<p class="summary">Generated API documentation for the scripts package.</p>',
        "</article>",
    ]

    for parent in sorted(by_parent):
        lines.append('<section class="content index-section">')
        parent_package = packages.get(PurePosixPath(parent))
        if parent_package:
            parent_href = relative_link(PurePosixPath("index.html"), parent_package.doc_rel)
            lines.append(
                f'<h2 id="{html_escape(slug(parent))}"><a href="{html_escape(parent_href)}">{html_escape(parent)}</a></h2>'
            )
            if parent_package.summary:
                lines.append(f'<div class="summary">{render_html_text(parent_package.summary)}</div>')
        else:
            lines.append(f'<h2 id="{html_escape(slug(parent))}">{html_escape(parent)}</h2>')
        for folder in sorted(by_parent[parent]):
            folder_name = "Root" if folder == PurePosixPath(parent) else folder.relative_to(parent).as_posix()
            folder_id = slug(f"{parent}-{folder_name}")
            folder_package = packages.get(folder)
            if folder_package:
                folder_href = relative_link(PurePosixPath("index.html"), folder_package.doc_rel)
                lines.append(
                    f'<h3 id="{html_escape(folder_id)}"><a href="{html_escape(folder_href)}">{html_escape(folder_name)}</a></h3>'
                )
                if folder_package.summary and folder != PurePosixPath(parent):
                    lines.append(f'<div class="summary folder-summary">{render_html_text(folder_package.summary)}</div>')
            else:
                lines.append(f'<h3 id="{html_escape(folder_id)}">{html_escape(folder_name)}</h3>')
            lines.append('<ul class="index-list">')
            for module in by_parent[parent][folder]:
                target = module.doc_rel
                lines.append(
                    f'<li><a href="{html_escape(target.as_posix())}">{html_escape(module.source_rel.name)}</a></li>'
                )
            lines.append("</ul>")
        lines.append("</section>")
    content = "\n".join(lines)
    nav = render_nav_links(PurePosixPath("index.html"), [("Home", PurePosixPath("index.html"))])
    body = render_page_layout(nav, left_sidebar, content, right_sidebar)
    return html_page("Index", body, PurePosixPath("index.html"))


def build_modules(
    scripts_dir: Path = SCRIPTS_DIR, repo_root: Path = REPO_ROOT
) -> list[ModuleDoc]:
    """Parse and sort every source module that should be documented."""
    modules = [parse_module(path, repo_root) for path in discover_sources(scripts_dir)]
    return sorted(modules, key=lambda item: item.doc_rel.as_posix())


def build_packages(
    scripts_dir: Path = SCRIPTS_DIR, repo_root: Path = REPO_ROOT
) -> dict[PurePosixPath, PackageDoc]:
    """Parse and index package folder summaries."""
    packages = [parse_package(path, repo_root) for path in discover_packages(scripts_dir)]
    return {package.doc_rel.parent: package for package in packages}


def expected_html_docs(
    modules: list[ModuleDoc],
    packages: dict[PurePosixPath, PackageDoc],
) -> dict[PurePosixPath, str]:
    """Build the complete set of generated HTML files."""
    docs = {
        module.doc_rel: render_html_module(module, modules, packages)
        for module in modules
    }
    for package in packages.values():
        docs[package.doc_rel] = render_folder_index(package, modules, packages)
    docs[PurePosixPath("index.html")] = render_html_index(modules, packages)
    return docs


def is_generated_doc_path(path: PurePosixPath, suffix: str) -> bool:
    """Return whether a path belongs to generated docs for this format."""
    if path == PurePosixPath(f"index{suffix}"):
        return True
    return path.suffix == suffix and path.parts[:1] == ("scripts",)


def existing_markdown(docs_dir: Path = DOCS_DIR) -> set[PurePosixPath]:
    """Return existing generated Markdown files."""
    if not docs_dir.exists():
        return set()
    return {
        rel_path
        for path in docs_dir.rglob("*.md")
        for rel_path in [PurePosixPath(path.relative_to(docs_dir).as_posix())]
        if is_generated_doc_path(rel_path, ".md")
    }


def existing_html(docs_dir: Path = DOCS_DIR) -> set[PurePosixPath]:
    """Return existing generated HTML files."""
    if not docs_dir.exists():
        return set()
    return {
        rel_path
        for path in docs_dir.rglob("*.html")
        for rel_path in [PurePosixPath(path.relative_to(docs_dir).as_posix())]
        if is_generated_doc_path(rel_path, ".html")
    }


def clean_markdown(docs_dir: Path = DOCS_DIR) -> None:
    """Remove generated Markdown files."""
    if not docs_dir.exists():
        return
    for path in docs_dir.rglob("*.md"):
        rel_path = PurePosixPath(path.relative_to(docs_dir).as_posix())
        if is_generated_doc_path(rel_path, ".md"):
            path.unlink()


def clean_html(docs_dir: Path = DOCS_DIR) -> None:
    """Remove generated HTML files."""
    if not docs_dir.exists():
        return
    for path in docs_dir.rglob("*.html"):
        rel_path = PurePosixPath(path.relative_to(docs_dir).as_posix())
        if is_generated_doc_path(rel_path, ".html"):
            path.unlink()


def prune_empty_dirs(docs_dir: Path = DOCS_DIR) -> None:
    """Remove empty directories left behind by generated docs."""
    if not docs_dir.exists():
        return
    assets_dir = docs_dir / "assets"
    for directory in sorted(
        [path for path in docs_dir.rglob("*") if path.is_dir()],
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        if directory == assets_dir or assets_dir in directory.parents:
            continue
        if not any(directory.iterdir()):
            directory.rmdir()


def write_file_set(docs: dict[PurePosixPath, str], docs_dir: Path = DOCS_DIR) -> None:
    """Write a set of generated files below docs."""
    docs_dir.mkdir(parents=True, exist_ok=True)
    for rel_path, content in docs.items():
        target = docs_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")


def write_docs(html_docs: dict[PurePosixPath, str], docs_dir: Path = DOCS_DIR) -> None:
    """Write generated HTML docs to disk."""
    clean_markdown(docs_dir)
    clean_html(docs_dir)
    prune_empty_dirs(docs_dir)
    write_file_set(html_docs, docs_dir)


def check_file_set(
    docs: dict[PurePosixPath, str],
    existing_paths: set[PurePosixPath],
    docs_dir: Path,
) -> bool:
    """Check whether one generated file set matches disk."""
    ok = True
    expected_paths = set(docs)
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


def check_docs(html_docs: dict[PurePosixPath, str], docs_dir: Path = DOCS_DIR) -> bool:
    """Check whether existing docs match generated HTML output."""
    existing_generated_docs = existing_html(docs_dir) | existing_markdown(docs_dir)
    return check_file_set(html_docs, existing_generated_docs, docs_dir)


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
    packages = build_packages()
    html_docs = expected_html_docs(modules, packages)

    if args.check:
        if check_docs(html_docs):
            print("Docs are current.")
            return 0
        return 1

    write_docs(html_docs)
    print(f"Generated {len(html_docs)} HTML documentation files in {DOCS_DIR}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
