import os
import xml.etree.ElementTree as ET
from scripts.core import logger
from scripts.core.file_loading import get_clothing_dir
from scripts.utils import echo

class ClothingDecal:
    """
    Represents a single clothing decal, loaded from an XML file.
    Includes texture path and placement coordinates.
    """
    _instances: dict[str, "ClothingDecal"] = {}

    def __new__(cls, decal_name: str):
        if decal_name in cls._instances:
            return cls._instances[decal_name]
        instance = super().__new__(cls)
        cls._instances[decal_name] = instance
        return instance

    def __init__(self, decal_name: str):
        """
        Args:
            decal_name (str): The name of the decal (XML filename without extension).
        """
        if hasattr(self, "name"):
            return

        self.name = decal_name
        self.texture = None
        self.x = None
        self.y = None
        self.width = None
        self.height = None

        path = os.path.join(get_clothing_dir(), "clothingDecals", f"{decal_name}.xml")
        if os.path.exists(path):
            self._parse_decal(path)
        else:
            logger.write(f"Decal file not found: {decal_name}.xml")

    def __repr__(self):
        return f"<ClothingDecal: {self.name}>"

    def __str__(self):
        return self.name

    def _parse_decal(self, path: str):
        try:
            tree = ET.parse(path)
            root = tree.getroot()

            self.texture = root.findtext("texture")
            self.x = int(root.findtext("x") or 0)
            self.y = int(root.findtext("y") or 0)
            self.width = int(root.findtext("width") or 0)
            self.height = int(root.findtext("height") or 0)

        except ET.ParseError as e:
            echo.error(f"Failed to parse decal '{self.name}': {e}")

class ClothingItem:
    """
    Represents a clothing item, parsed from XML.
    Includes model references, decal group, and texture options.
    """
    _decal_group_map = None
    _instances: dict[str, "ClothingItem"] = {}

    def __new__(cls, clothing_item: str):
        if clothing_item in cls._instances:
            return cls._instances[clothing_item]
        instance = super().__new__(cls)
        cls._instances[clothing_item] = instance
        return instance

    def __init__(self, clothing_item: str):
        """
        Args:
            clothing_item (str): The item ID to load (e.g., 'Tshirt_SpiffoDECAL').
        """
        if hasattr(self, "clothing_item"):
            return
        
        self.clothing_item = clothing_item
        self.file_path = os.path.join(get_clothing_dir(), "clothingItems", f"{self.clothing_item}.xml")

        self.guid = None  # str
        self.male_model = None  # str
        self.female_model = None  # str
        self.alt_male_model = None  # str
        self.alt_female_model = None  # str
        self.is_static = False  # bool
        self.allow_random_hue = False  # bool
        self.allow_random_tint = False  # bool
        self.attach_bone = None # str
        self.decal_group = None # str
        self.decals = [] # list[ClothingDecal]
        self.masks = [] # list[str]
        self.masks_folder = None # str
        self.underlay_masks_folder = None # str
        self.base_textures = [] # list[str]
        self.texture_choices = [] # list[str]
        self.spawn_with = None # str

        if os.path.exists(self.file_path):
            self.parse_clothing_xml()
        else:
            logger.write(f"No XML file found for ClothingItem '{self.clothing_item}'.")

    def __repr__(self):
        """Returns a debug representation of the clothing item."""
        return f"<ClothingItem: {self.clothing_item}>"

    def __str__(self):
        """Returns the `ClothingItem` value as a string."""
        return self.clothing_item

    @classmethod
    def _load_decal_groups(cls):
        """
        Loads and caches decal group mappings from clothingDecals.xml.
        Populates `_decal_group_map` with group name -> decal name list.
        """
        if cls._decal_group_map is not None:
            return

        path = os.path.join(get_clothing_dir(), "clothingDecals.xml")
        cls._decal_group_map = {}

        if not os.path.exists(path):
            logger.write("clothingDecals.xml not found.")
            return

        try:
            tree = ET.parse(path)
            for group in tree.findall(".//group"):
                name = group.findtext("name")
                if name:
                    cls._decal_group_map[name] = [d.text for d in group.findall("decal") if d.text]
        except ET.ParseError as e:
            echo.error(f"Error parsing decal groups: {e}")

    def parse_clothing_xml(self):
        """
        Parses the XML file for the clothing item and sets all attributes.
        Handles decal group loading and decal object creation if applicable.
        """
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()

            def get_value(tag):
                """Returns the text value of the first tag match or None."""
                elem = root.find(tag)
                return elem.text if elem is not None else None

            def get_list(tag):
                """Returns a list of text values for all matching tags."""
                return [elem.text for elem in root.findall(tag) if elem.text]

            def get_bool(tag):
                """Returns True if the tag value is 'true' (case-insensitive), else False."""
                text = get_value(tag)
                return text.lower() == "true" if text else False

            self.guid = get_value("m_GUID")
            self.male_model = get_value("m_MaleModel")
            self.female_model = get_value("m_FemaleModel")
            self.alt_male_model = get_value("m_AltMaleModel")
            self.alt_female_model = get_value("m_AltFemaleModel")
            self.is_static = get_bool("m_Static")
            self.allow_random_hue = get_bool("m_AllowRandomHue")
            self.allow_random_tint = get_bool("m_AllowRandomTint")
            self.attach_bone = get_value("m_AttachBone")

            self._load_decal_groups()

            self.decal_group = get_value("m_DecalGroup")
            if self.decal_group:
                raw_decals = self._decal_group_map.get(self.decal_group, [])
                self.decals = DecalList([ClothingDecal(name) for name in raw_decals])

            self.masks = get_list("m_Masks")
            self.masks_folder = get_value("m_MasksFolder")
            self.underlay_masks_folder = get_value("m_UnderlayMasksFolder")
            self.base_textures = get_list("m_BaseTextures")
            self.texture_choices = get_list("textureChoices")
            self.spawn_with = get_value("m_SpawnWith")

        except ET.ParseError as e:
            echo.error(f"Failed parsing XML file: {self.file_path}\n{e}")

class DecalList:
    """
    Helper class that wraps a list of ClothingDecal objects with additional properties for convenience.
    Supports iteration and indexing.
    """
    def __init__(self, decals: list[ClothingDecal]):
        """
        Args:
            decals (list[ClothingDecal]): A list of ClothingDecal objects.
        """
        self._decals = decals

    def __iter__(self):
        """Returns an iterator over the decal list."""
        return iter(self._decals)

    def __getitem__(self, index):
        """Returns the decal at the given index."""
        return self._decals[index]

    def __len__(self):
        """Returns the number of decals in the list."""
        return len(self._decals)

    def __repr__(self):
        """Returns a debug representation of the decal list."""
        return repr(self._decals)

    @property
    def names(self) -> list[str]:
        return [d.name for d in self._decals]

    @property
    def textures(self) -> list[str]:
        return [d.texture for d in self._decals if d.texture]

    @property
    def coords(self) -> list[tuple[int, int]]:
        return [(d.x, d.y) for d in self._decals if d.x is not None and d.y is not None]

    @property
    def dimensions(self) -> list[tuple[int, int]]:
        return [(d.width, d.height) for d in self._decals if d.width is not None and d.height is not None]