import json
from pathlib import Path

from scripts.core.language import Language
from scripts.core.constants import NAVBOX_DIR
from scripts.navbox.navbox_schema import NavboxSchema


class Navbox:
    """Builds and exports navbox JSON data."""
    def __init__(self, table_name: str):
        """
        Initialise the navbox builder.

        Args:
            table_name (str): Display name of the navbox table.
        """
        self.schema = NavboxSchema(table_name=table_name)

    def add_section(self, section_name: str):
        """
        Create or retrieve a navbox section.

        Args:
            section_name (str): Name of the section.

        Returns:
            NavboxSection: Existing or newly created section.
        """
        return self.schema.add_section(section_name)

    def add_item(self, section_name: str, page_name: str, label: str | None = None):
        """
        Add an item to a navbox section.

        Args:
            section_name (str): Name of the section.
            page_name (str): Target page name.
            label (str | None, optional): Custom display label.
        """
        section = self.add_section(section_name)

        if label:
            item = f"{page_name}|{label}"
        else:
            item = page_name

        section.add_item(item)

    def sort(self, *, sections: bool = True, items: bool = True):
        """
        Sort navbox sections and items.

        Args:
            sections (bool, optional): Sort sections alphabetically.
            items (bool, optional): Sort items alphabetically.
        """
        if sections:
            self.schema.sort_sections()

        if items:
            self.schema.sort_items()

    def sort_sections_by_order(self, section_order: list[str]):
        """
        Sort sections by a preferred order.

        Args:
            section_order (list[str]): Preferred section name order.
        """
        self.schema.sort_sections_by_order(section_order)

    def to_dict(self) -> dict:
        """
        Convert the navbox into a JSON-ready dictionary.

        Returns:
            dict: Navbox data.
        """
        return self.schema.to_dict()

    def to_json(self) -> str:
        """
        Convert the navbox into formatted JSON.

        Returns:
            str: Formatted JSON string.
        """
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def save(self, filename: str, output_dir: str | Path | None = None) -> Path:
        """
        Save the navbox JSON file.

        Args:
            filename (str): Output filename.
            output_dir (str | Path | None, optional): Output directory path.

        Returns:
            Path: Path to the saved JSON file.
        """
        output_dir = Path(output_dir or NAVBOX_DIR.format(language_code=Language.get()))
        output_dir.mkdir(parents=True, exist_ok=True)

        if not filename.endswith(".json"):
            filename += ".json"

        path = output_dir / filename

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())
            f.write("\n")

        return path