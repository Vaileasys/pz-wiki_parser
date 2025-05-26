import os
from scripts.core.cache import load_json
from scripts.core.constants import RESOURCE_DIR

class PageDict:
    _data = None

    @classmethod
    def load(cls, filepath=os.path.join(RESOURCE_DIR, "page_dictionary.json")):
        if cls._data is None:
            cls._data = load_json(filepath)

    @classmethod
    def get_page(cls, script_id, type_="item", id_key=None):
        """
        Returns the wiki page name for the given script_id.

        Args:
            script_id (str): Full ID like 'Base.Axe'.
            type_ (str): Script type ('item', 'fluid', etc.).
            id_key (str, optional): Key name to look up IDs. Defaults to '{type_}_id'.

        Returns:
            str or None: Page name if found, else None.
        """
        cls.load()
        id_key = id_key or f"{type_}_id"
        entries = cls._data.get(type_, {})
        for page_name, entry in entries.items():
            if script_id in entry.get(id_key, []):
                return page_name
        return None

    @classmethod
    def get_categories(cls, script_id, type_="item", id_key=None):
        """
        Returns the list of categories for the given script_id.

        Args:
            script_id (str): Full ID like 'Base.Axe'.
            type_ (str): Script type ('item', 'fluid', etc.).
            id_key (str, optional): Key name to look up IDs. Defaults to '{type_}_id'.

        Returns:
            list: Category names if found, else an empty list.
        """
        cls.load()
        id_key = id_key or f"{type_}_id"
        entries = cls._data.get(type_, {})
        for entry in entries.values():
            if script_id in entry.get(id_key, []):
                return entry.get("categories", [])
        return []


if __name__ == "__main__":
    item_id = "Base.Axe"
    item_page = PageDict.get_page(item_id, type_="item")
    item_categories = PageDict.get_categories(item_id, type_="item")
    print(f"Item Page: {item_page}")
    print(f"Item Categories: {item_categories}")