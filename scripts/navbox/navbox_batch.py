"""Menu and batch runner for the registered PZwiki navbox generators.

Running all modules also builds the page-to-navbox index after the registered navboxes have completed.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType

from scripts.core.constants import NAVBOX_DIR
from scripts.core.language import Language
from scripts.navbox.navbox_page_index import generate_page_navbox_index
from scripts.utils import color, echo


MODULES: dict[str, dict[str, str]] = {
    "1": {
        "module": "scripts.navbox.navbox_outfits",
        "name": "Outfits",
        "description": "navbox for outfit pages.",
        "output_filename": "outfits.json",
    },
    "2": {
        "module": "scripts.navbox.navbox_weapons",
        "name": "Weapons",
        "description": "navbox for weapons, ammunition and weapon-part pages.",
        "output_filename": "weapons.json",
    },
}


def get_output_dir() -> Path:
    """Return the navbox output directory for the active language."""
    return Path(NAVBOX_DIR.format(language_code=Language.get()))


def display_menu(
    start: int = 0,
    page_size: int = 10,
    run_directly: bool = False,
) -> None:
    """Display a paginated menu of registered navbox generators."""
    keys = list(MODULES.keys())
    end = start + page_size

    echo.write("\nSelect a navbox module to run:", color.info)
    print("0: Run all modules and generate the page index")

    for key in keys[start:end]:
        module_data = MODULES[key]
        print(
            f"{key}: {module_data['name']} - "
            f"{module_data['description']}"
        )

    if end < len(keys):
        print("]: Next page")
    if start > 0:
        print("[: Previous page")

    print("Q: Quit" if run_directly else "B: Back")


def _load_module(module_path: str) -> ModuleType:
    """Import a registered navbox module and validate its entry point."""
    module = importlib.import_module(module_path)

    if not callable(getattr(module, "main", None)):
        raise AttributeError(
            f"Navbox module '{module_path}' has no callable main() function."
        )

    return module


def run_module(module_data: dict[str, str]) -> Path:
    """Run one registered navbox module and return its generated file path."""
    module_path = module_data["module"]
    output_filename = module_data["output_filename"]
    output_dir = get_output_dir()
    output_path = output_dir / output_filename

    module = _load_module(module_path)

    # A failed generator must not leave an older file looking current.
    if output_path.exists():
        output_path.unlink()

    module.main()

    if not output_path.is_file():
        raise FileNotFoundError(
            f"Navbox module '{module_path}' completed without creating "
            f"'{output_path}'."
        )

    return output_path


def run_all_modules() -> tuple[list[Path], Path]:
    """Run all registered navboxes, then generate the page-to-navbox index."""
    generated_paths: list[Path] = []
    failures: list[tuple[str, Exception]] = []

    for module_data in MODULES.values():
        echo.write(f"\n[Running] {module_data['name']}", color.warning)

        try:
            generated_paths.append(run_module(module_data))
        except Exception as exc:
            failures.append((module_data["name"], exc))
            echo.error(f"Failed to run '{module_data['module']}': {exc}")

    echo.write("\n[Running] Page navbox index", color.warning)
    index_path = generate_page_navbox_index(navbox_paths=generated_paths)

    if failures:
        failed_names = ", ".join(name for name, _exc in failures)
        raise RuntimeError(
            f"Navbox batch completed with {len(failures)} failure(s): "
            f"{failed_names}. The page index contains only the "
            f"{len(generated_paths)} successful navbox output(s)."
        )

    print("")
    echo.success(
        f"Finished generating navboxes and the page index. "
        f"Files saved to '{get_output_dir()}'"
    )
    return generated_paths, index_path


# Compatibility with the first batch implementation.
run_all_navboxes = run_all_modules


def main(run_directly: bool = False) -> None:
    """Handle menu input for individual or complete navbox generation."""
    page = 0
    page_size = 10

    while True:
        display_menu(
            start=page * page_size,
            page_size=page_size,
            run_directly=run_directly,
        )
        choice = input("> ").strip().lower()

        if choice == ("q" if run_directly else "b"):
            break
        if choice == "]" and (page + 1) * page_size < len(MODULES):
            page += 1
        elif choice == "[" and page > 0:
            page -= 1
        elif choice == "0":
            run_all_modules()
            break
        elif choice in MODULES:
            module_data = MODULES[choice]
            echo.write(f"\n[Running] {module_data['name']}", color.warning)

            try:
                output_path = run_module(module_data)
                echo.success(f"Saved navbox: {output_path}")
            except Exception as exc:
                echo.error(f"Failed to run '{module_data['module']}': {exc}")
        else:
            echo.write("\n[!] Invalid input. Please try again", color.error)


if __name__ == "__main__":
    main(run_directly=True)
