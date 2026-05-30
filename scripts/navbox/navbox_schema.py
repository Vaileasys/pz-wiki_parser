from dataclasses import dataclass, field

@dataclass
class NavboxSection:
    """Represents a single navbox section and its items."""
    
    section_name: str
    item_list: list[str] = field(default_factory=list)

    def add_item(self, item: str):
        """
        Add an item to the section if it is valid and not already present.

        Args:
            item (str): Page name or formatted navbox item.
        """
        item = str(item).strip()

        if not item:
            return

        if item not in self.item_list:
            self.item_list.append(item)

    def sort_items(self):
        """Sort all items in the section alphabetically."""
        self.item_list.sort(key=str.casefold)

    def to_dict(self) -> dict:
        """
        Convert the section into a JSON-ready dictionary.

        Returns:
            dict: Section data containing the section name and item list.
        """
        return {
            "section_name": self.section_name,
            "item_list": self.item_list,
        }


@dataclass
class NavboxSchema:
    """Represents the full navbox JSON schema."""
    table_name: str
    sections: list[NavboxSection] = field(default_factory=list)

    def add_section(self, section_name: str) -> NavboxSection:
        """
        Create or retrieve a navbox section.

        Args:
            section_name (str): Name of the section.

        Returns:
            NavboxSection: Existing or newly created section.
        """
        section_name = str(section_name).strip()

        for section in self.sections:
            if section.section_name == section_name:
                return section

        section = NavboxSection(section_name)
        self.sections.append(section)
        return section

    def sort_sections(self):
        """Sort all sections alphabetically."""
        self.sections.sort(key=lambda section: section.section_name.casefold())

    def sort_sections_by_order(self, section_order: list[str]):
        """Sort sections by a preferred order, then alphabetically."""
        order_map = {
            section_name: index
            for index, section_name in enumerate(section_order)
        }

        self.sections.sort(
            key=lambda section: (
                order_map.get(section.section_name, len(order_map)),
                section.section_name.casefold(),
            )
        )

    def sort_items(self):
        """Sort items in every section."""
        for section in self.sections:
            section.sort_items()

    def validate(self):
        """
        Validate the navbox schema before export.

        Raises:
            ValueError: If the navbox contains invalid or missing data.
        """
        if not self.table_name.strip():
            raise ValueError("Navbox table_name cannot be blank.")

        if not self.sections:
            raise ValueError(f"Navbox '{self.table_name}' has no sections.")

        for section in self.sections:
            if not section.section_name.strip():
                raise ValueError(f"Navbox '{self.table_name}' has a blank section name.")

            if not section.item_list:
                raise ValueError(
                    f"Navbox '{self.table_name}' section '{section.section_name}' has no items."
                )

    def to_dict(self) -> dict:
        """
        Convert the navbox schema into a JSON-ready dictionary.

        Returns:
            dict: Navbox data containing the table name and sections.
        """
        self.validate()

        return {
            "table_name": self.table_name,
            "sections": [section.to_dict() for section in self.sections],
        }