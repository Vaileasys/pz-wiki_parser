import os
import csv
from scripts.parser import script_parser
from scripts.core.file_loading import get_script_path
from scripts.core.language import Language, Translate
from scripts.utils import utility, lua_helper
from scripts.core import logger
from scripts.core.constants import RESOURCE_DIR
from scripts.utils.echo import echo_warning, ignore_warnings
from scripts.core.cache import load_cache, save_cache
from scripts.core.version import Version
from scripts.utils.util import link
from scripts.core.page_manager import get_pages
from scripts.objects.components import FluidContainer, Durability

class Item:
    _items = None  # Shared cache for all items
    _instances = {}
    _icon_cache_files = None
    _burn_data = None

    def __new__(cls, item_id: str):
        """Returns an existing Item instance if one already exists for the given ID.
        
        Fixes partial IDs like 'Axe' to 'Base.Axe' before checking or creating the instance."""
        if cls._items is None:
            cls._load_items()

        item_id = cls.fix_item_id(item_id)

        if item_id in cls._instances:
            return cls._instances[item_id]

        instance = super().__new__(cls)
        cls._instances[item_id] = instance
        return instance

    def __init__(self, item_id: str):
        """Sets up the item's data if it hasn’t been initialised yet."""
        if hasattr(self, 'item_id'):
            return

        if Item._items is None:
            Item._load_items()

        item_id = self.fix_item_id(item_id)

        self._item_id = item_id
        self.data = Item._items.get(item_id, {})

        self._module, self._id_type = item_id.split(".", 1)

        self._name = None
        self._name_en = None  # English name
        self._page = None     # Wiki page
        self._wiki_link = None # Wiki link
        self._has_page = None # Page defined (bool)
        self._icon = None     # Primary icon (str)
        self._icons = None    # All icons (list)
    
    # Allows 'item["DisplayName"]'
    def __getitem__(self, key):
        return self.data[key]
    
    # Allows 'in' checks. e.g. '"EvolvedRecipe" in item'
    def __contains__(self, key):
        return key in self.data
    
    # Overview of the item when called directly: Item(item_id)
    def __repr__(self):
        name = self.get("DisplayName", "Unnamed")
        item_type = self.get("Type", "Unknown")
        source = fr"{self.get_path()}"

        return (f'<Item {name} ({self._item_id}) — {item_type}, "{source}">')

    @classmethod
    def _load_items(cls):
        """Load item data only once and store in class-level cache."""
        cls._items = script_parser.extract_script_data("item")

    @classmethod
    def fix_item_id(cls, item_id: str) -> str:
        """
        Attempts to fix a partial item_id by assuming the 'Base' module first,
        then falling back to a full search through parsed item data.

        Args:
            item_id (str): Either a full item_id ('Module.Item') or just an item name.

        Returns:
            str: The best-guess full item_id.
        """
        if '.' in item_id:
            return item_id

        base_guess = f"Base.{item_id}"
        if cls._items is None:
            cls._load_items()

        if base_guess in cls._items:
            return base_guess

        # Fallback: full search
        for full_id in cls._items:
            if full_id.endswith(f".{item_id}"):
                return full_id

        logger.write(f"No Item ID found for '{item_id}'")
        return item_id

    @classmethod
    def all(cls):
        """Return all items as a dictionary of {item_id: Item}."""
        if cls._items is None:
            cls._load_items()
        return {item_id: cls(item_id) for item_id in cls._items}
    
    @classmethod
    def keys(cls):
        if cls._items is None:
            cls._load_items()
        return cls._items.keys()

    @classmethod
    def values(cls):
        if cls._items is None:
            cls._load_items()
        return (cls(item_id) for item_id in cls._items)
    
    @classmethod
    def count(cls):
        if cls._items is None:
            cls._load_items()
        return len(cls._items)
    
    @classmethod
    def get_icon_cache(cls):
        if cls._icon_cache_files is None:
            texture_cache = load_cache(f"{RESOURCE_DIR}/texture_names.json", "texture cache", suppress=True)
            cls._icon_cache_files = texture_cache.get("Item", [])
        return cls._icon_cache_files
    
    @classmethod
    def load_burn_data(cls):
        """Loads and caches burn time data from camping_fuel.lua."""
        if cls._burn_data is None:
            TABLES = [
                "campingFuelType",
                "campingFuelCategory",
                "campingLightFireType",
                "campingLightFireCategory"
            ]
            CACHE_FILE = "burn_data.json"

            parsed_burn_data, cache_version = load_cache(CACHE_FILE, "burn", True, suppress=True)

            if cache_version != Version.get():
                lua_runtime = lua_helper.load_lua_file("camping_fuel.lua")
                parsed_burn_data = lua_helper.parse_lua_tables(lua_runtime, TABLES)
                save_cache(parsed_burn_data, CACHE_FILE)

            cls._burn_data = parsed_burn_data

    ## ------------------------- Dict-like Methods ------------------------- ##

    def get(self, key: str, default=None):
        return self.data.get(key, default)
    
    ## ------------------------- Misc Methods ------------------------- ##

    def page_exists(self) -> bool:
        if self._has_page is None:
            self.find_page()
        return self._has_page
    
    ## ------------------------- Property Methods ------------------------- ##

    def get_component(self, key: str):
        return self.data.get("component", {}).get(key, {})
    
    def get_file(self):
        return self.data.get("SourceFile")
    
    def get_path(self):
        return get_script_path(self.get_file(), prefer="item")

    def get_module(self):
        return self._module

    def get_id_type(self):
        return self._id_type

    def get_page(self, fallback: str = None) -> str:
        """Returns the page name for this item, calling find_page() if needed."""
        if self._page is None:
            if fallback is None:
                fallback = self.get_name()
            self.find_page(fallback)
        return self._page

    def find_page(self, fallback: str = "Unknown") -> str:
        """Finds and sets the wiki page name this item belongs to."""
        item_id_data = utility.get_item_id_data(True) #TODO: move this function to a class method

        self._has_page = False
        for page_name, item_ids in item_id_data.items():
            if self._item_id in item_ids:
                self._page = page_name
                self._has_page = True
                return self._page

        logger.write(f"Couldn't find a page for '{self._item_id}'")
        self._page = fallback
        return self._page

    def get_name(self, language: str = None) -> str:
        """Returns the item name for the current language"""
        language_code = language or Language.get()

        if language_code == "en":
            if self._name is None:
                self.find_name("en")
            return self._name

        return self.find_name(language_code)

    def find_name(self, language: str = None) -> str:
        """Finds an item name if it has a special case, otherwise translates the DisplayName."""
        item_id = self._item_id
        language_code = language or Language.get()
        is_english = (language_code == "en")

        ITEM_NAMES = {
            "bible": {
                "item_id": ["Base.Book_Bible", "Base.BookFancy_Bible", "Base.Paperback_Bible"],
                "suffix": f": {Translate.get('TheBible', 'BookTitle', language_code)}"
            },
            "Newspaper_Dispatch_New": {
                "item_id": ["Base.Newspaper_Dispatch_New"],
                "suffix": f": {Translate.get('NationalDispatch', 'NewspaperTitle', language_code)}"
            },
            "Newspaper_Herald_New": {
                "item_id": ["Base.Newspaper_Herald_New"],
                "suffix": f": {Translate.get('KentuckyHerald', 'NewspaperTitle', language_code)}"
            },
            "Newspaper_Knews_New": {
                "item_id": ["Base.Newspaper_Knews_New"],
                "suffix": f": {Translate.get('KnoxKnews', 'NewspaperTitle', language_code)}"
            },
            "Newspaper_Times_New": {
                "item_id": ["Base.Newspaper_Times_New"],
                "suffix": f": {Translate.get('LouisvilleSunTimes', 'NewspaperTitle', language_code)}"
            },
            "BusinessCard_Nolans": {
                "item_id": ["Base.BusinessCard_Nolans"],
                "suffix": f": {Translate.get('NolansUsedCars', 'IGUI', language_code)}"
            },
            "Flier_Nolans": {
                "item_id": ["Base.Flier_Nolans"],
                "suffix": f": {Translate.get('NolansUsedCars_title', 'PrintMedia', language_code)}"
            }
        }

        for key, value in ITEM_NAMES.items():
            if item_id in value["item_id"]:
                suffix = value.get("suffix", "")
                prefix = value.get("prefix", "")
                infix = value.get("infix", "")
                if not infix:
                    infix = Translate.get(item_id, "DisplayName", "en" if is_english else language_code)

                name = f"{prefix}{infix}{suffix}"
                if is_english:
                    self._name = name
                return name
        
        display_name = Translate.get(item_id, "DisplayName", "en" if is_english else language_code)
        # Vehicle parts
        if self.get("VehicleType", 0) > 0:
            self._name = Translate.get("IGUI_ItemNameMechanicalType").replace("%1", display_name).replace("%2", Translate.get("IGUI_VehicleType_" + str(self.get("VehicleType"))))
            return self._name

        # Default fallback
        if display_name == item_id:
            display_name = self.get("DisplayName", item_id)

        if is_english:
            self._name = display_name
        return display_name
    
    def get_link(self) -> str:
        """Return the wiki link for this item."""
        if self._wiki_link is None:
            self._wiki_link = link(self.get_page(), self.get_name())
        return self._wiki_link
    
    def get_icon(self, format: bool = True, all_icons: bool = True, cycling: bool = True, custom_name: str = None) -> str | list[str]:
        """
        Main interface for getting icons.

        By default, returns a cycling formatted wiki icon (format=True).
        If format=False, returns raw icon filenames (str or list).
        """
        # Return raw icons if formatting is disabled
        if not format:
            if all_icons:
                if self._icons is None:
                    self._find_icon()
                return self._icons
            else:
                if self._icon is None:
                    self._find_icon()
                return self._icon

        # Otherwise return formatted wiki link
        return self._format_icon(format=True, all_icons=all_icons, cycling=cycling, custom_name=custom_name)

    def _find_icon(self):
        icon_default = "Question_On"
        icon = None

        icon_cache_files = Item.get_icon_cache()

        def check_icon_exists(icon_name):
            if isinstance(icon_name, str):
                icon_name = [icon_name]

            updated_icons = []
            for name in icon_name:
                for file in icon_cache_files:
                    if file.lower() == name.lower():
                        updated_icons.append(file)
                        break
            
            if not updated_icons:
                return icon_name

            return updated_icons

        icons_csv = os.path.join('resources', 'icons.csv')
        if os.path.exists(icons_csv):
            with open(icons_csv, newline='', encoding='UTF-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if row['item_id'] == self._item_id:
                        icon = [row['icon'] + ".png"]
                        break
        else:
            echo_warning(f"File '{icons_csv}' does not exist. Getting icon from item properties.")

        if not icon:
            icon = self.data.get("Icon")

            if icon == "default":
                # Item is a tile, so should get WorldObjectSprite
                icon = self.data.get("WorldObjectSprite", "Flatpack")
            
            elif icon:
                # Use 'Icon' property
                icon_variants = ['Rotten', '_Rotten', 'Spoiled', 'Cooked', 'Burnt', '_Burnt', 'Overdone']
                icons = [icon]
                for variant in icon_variants:
                    variant_icon = f"{icon}{variant}.png"
                    if variant_icon in icon_cache_files:
                        icons.append(variant_icon)
                icon = icons
            
            elif any(k.lower() == "iconsfortexture" for k in self.data):
                # Use 'IconsForTeture' property
                icon = next(v for k, v in self.data.items() if k.lower() == "iconsfortexture")

            elif "WorldObjectSprite" in self.data:
                # Use 'WorldObjectSprite' property
                icon = self.data["WorldObjectSprite"]
            else:
                icon = icon_default

            # Remove 'Item_' prefix if it's present, for both str and list
            if isinstance(icon, str):
                icon = icon.removeprefix("Item_")
            elif isinstance(icon, list):
                icon = [i.removeprefix("Item_") for i in icon]
        
        # Bundle all_icons as a list, and ensure endswith .png
        if isinstance(icon, str):
            all_icons = [icon]
        else:
            all_icons = icon
        all_icons = [i if i.endswith('.png') else f"{i}.png" for i in all_icons]

        checked = check_icon_exists(all_icons)
        if checked and checked != all_icons:
            logger.write(f"Icon was modified for {self._item_id} with icon: {all_icons}", False, "log_modified_icons.txt")
        elif not checked:
            logger.write(f"Missing icon for '{self._item_id}' with icon: {all_icons}", False, "log_missing_icons.txt")

        all_icons = checked or all_icons
        self._icons = all_icons
        self._icon = all_icons[0]

    def _format_icon(self, format: bool = False, all_icons: bool = False, cycling: bool = False, custom_name: str = None) -> str | list[str]:
        """Returns the icon or formatted wiki markup based on given options. Supports cycling image formatting and translations."""
        if not self.data:
            echo_warning(f"Item ID '{self._item_id}' doesn't exist")
            return self._item_id

        # Force all_icons if cycling is True
        if cycling:
            all_icons = True
            format = True

        # Use cached icons or fetch them
        if all_icons:
            if self._icons is None:
                self._find_icon()
            icons = self._icons
        else:
            if self._icon is None:
                self._find_icon()
            icons = self._icon

        if not format:
            return icons

        # Formatting
        language_code = Language.get()
        lang_suffix = f"/{language_code}" if language_code != "en" else ""

        name = custom_name or self.get_name()
        page = self.get_page()

        if isinstance(icons, str):
            icons = [icons]

        icon_list = [
            f"[[File:{icon}|32x32px|link={page}{lang_suffix}|{name}]]"
            for icon in icons
        ]

        if cycling and len(icon_list) > 1:
            return f'<span class="cycle-img">{"".join(icon_list)}</span>'
        return ''.join(icon_list)
    
    def has_tag(self, tag: str) -> bool:
        return tag in self.get("Tags", [])


    def get_burn_time(self):
        if not hasattr(self, "_burn_time"):
            self.calculate_burn_time()
        return self._burn_time
    
    def calculate_burn_time(self):
        """Calculates and stores burn time for this item."""
        #TODO: clean up and use should_burn property
        if not self.data:
            self._burn_time = ""
            return

        if Item._burn_data is None:
            Item.load_burn_data()

        valid_fuel = False
        id_type = self._id_type
        category = self.get("Type", "")
        weight = float(self.get("Weight", 1))
        tags = self.get("Tags", [])
        fabric_type = self.get("FabricType", "")
        fire_fuel_ratio = float(self.get("FireFuelRatio", 0))

        fuel_data = Item._burn_data
        campingFuelType = fuel_data["campingFuelType"]
        campingFuelCategory = fuel_data["campingFuelCategory"]
        campingLightFireType = fuel_data["campingLightFireType"]
        campingLightFireCategory = fuel_data["campingLightFireCategory"]

        # Logic copied from `ISCampingMenu.shouldBurn()` and `ISCampingMenu.isValidFuel()`
        if "IsFireFuel" in tags or fire_fuel_ratio > 0: valid_fuel = True
        if campingFuelType.get(id_type) or campingFuelCategory.get(category): valid_fuel = True
        if campingFuelType.get(id_type) == 0 or campingFuelCategory.get(category) == 0: valid_fuel = False
        if "NotFireFuel" in tags:  valid_fuel = False
        if category.lower() == "clothing" and (fabric_type == "" or fabric_type.lower() == "leather"): valid_fuel = False

        if not valid_fuel:
            self._burn_time = ""
            return

        # Fuel duration logic
        value = None
        if campingFuelType.get(id_type): value = campingFuelType[id_type]
        elif campingLightFireType.get(id_type): value = campingLightFireType[id_type]
        elif campingFuelCategory.get(category): value = campingFuelCategory[category]
        elif campingLightFireCategory.get(category): value = campingLightFireCategory[category]

        burn_ratio = 2 / 3
        if category.lower() in ["clothing", "container", "literature", "map"]:
            burn_ratio = 1 / 4
        if fire_fuel_ratio > 0:
            burn_ratio = fire_fuel_ratio

        weight_value = weight * burn_ratio
        value = min(value, weight_value) if value else weight_value

        # Process value, changing to 'hours, minutes'
        hours = int(value)
        minutes = (value - hours) * 60

        # Translate units
        hours_unit = Translate.get("IGUI_Gametime_hour") if hours == 1 else Translate.get("IGUI_Gametime_hours")
        minutes_unit = Translate.get("IGUI_Gametime_minute") if int(minutes) == 1 else Translate.get("IGUI_Gametime_minutes")

        # Remove decimal where appropriate
        if minutes % 1 == 0:
            minutes = int(minutes)
        else:
            minutes = f"{minutes:.1f}".removesuffix(".0")

        # Convert to appropriate string layout
        if hours > 0:
            self._burn_time = f"{hours} {hours_unit}, {minutes} {minutes_unit}" if minutes else f"{hours} {hours_unit}"
        else:
            self._burn_time = f"{minutes} {minutes_unit}"
    
    ## ------------------------- Properties ------------------------- ##

    # --- Base Properties --- #

    @property
    def file(self):
        return self.data.get("SourceFile")

    @property
    def path(self):
        return get_script_path(self.file, prefer="fluid")

    @property
    def item_id(self):
        return self._item_id

    @property
    def module(self):
        return self._module

    @property
    def id_type(self):
        return self._id_type
    
    @property
    def page(self):
        if self._page is None:
            pages = get_pages(self.item_id, id_type="item_id")
            self._page = pages[0] if pages else self.name_en
        return self._page

    @property
    def display_name(self):
        return "ItemName_" + self.item_id

    @property
    def name(self):
        if self._name is None:
            self._name = Translate.get(self.display_name)
        return self._name

    @property
    def name_en(self):
        if self._name_en is None:
            self._name_en = Translate.get(self.display_name, lang_code="en")
        return self._name_en

    @property
    def wiki_link(self):
        if self._wiki_link is None:
            self._wiki_link = link(self.page, self.name)
        return self._wiki_link
    
    @property
    def icon(self):
        return self.get_icon()
    
    # --- Script Properties --- #

    @property
    def type(self):
        return self.data.get("Type", "Normal")

    @property
    def weight(self):
        return self.data.get("Weight", 1)
    
    @property
    def capacity(self):
        return self.data.get("Capacity", 0)
    
    @property
    def weight_reduction(self):
        return self.data.get("WeightReduction", 0)

    # --- Components --- #

    @property
    def components(self):
        return list(self.data.get("component", {}).keys())

    @property
    def fluid_container(self):
        if not hasattr(self, '_fluid_container'):
            self._fluid_container = FluidContainer(self.get_component("FluidContainer"))
        return self._fluid_container

    @property
    def durability(self):
        if not hasattr(self, '_durability'):
            self._durability = Durability(self.get_component("Durability"))
        return self._durability

    # --- Inferred Properties --- #

    @property
    def weight_full(self):
        total_weight = self.weight

        if self.fluid_container:
            total_weight = self.weight + self.fluid_container.capacity
        else:
            total_weight = self.weight + self.capacity

        total_weight = round(total_weight, 2)

        if total_weight.is_integer():
            return int(total_weight)
        else:
            return total_weight
        
    
    @property
    def burn_time(self):
        if not hasattr(self, "_burn_time"):
            self.calculate_burn_time()
        return self._burn_time
        

    @property
    def should_burn(self):
        """Checks if an item 'should burn', not that it 'can burn'."""
        if hasattr(self, "_should_burn"):
            return self._should_burn
        
        self._should_burn = True
        # Logic copied from 'ISCampingMenu.shouldBurn()'
        is_clothing = self.get("Type", "").lower() == "clothing"
        fabric_type = self.get("FabricType")
        if is_clothing and not fabric_type: self._should_burn = False
        if is_clothing and fabric_type == "Leather": self._should_burn = False
        return self._should_burn

    @property
    def is_tinder(self):
        if hasattr(self, "_is_tinder"):
            return self._is_tinder
        
        if not self.should_burn: return

        fuel_data = Item._burn_data
        campingLightFireType = fuel_data["campingLightFireType"]
        campingLightFireCategory = fuel_data["campingLightFireCategory"]

        # Logic copied from 'ISCampingMenu.isValidTinder()'
        category = self.get("Type")
        id_type = self._id_type

        self._is_tinder = self.has_tag("IsFireTinder")
        if campingLightFireType.get(id_type) or campingLightFireCategory.get(category): self._is_tinder = True
        if campingLightFireType.get(id_type) and campingLightFireType.get(id_type) == 0: self._is_tinder = False
        if campingLightFireCategory.get(category) and campingLightFireCategory.get(category) == 0: self._is_tinder = False
        if self.has_tag("NotFireTinder"): self._is_tinder = False

        return self._is_tinder
    
    #TODO: get_model
    #TODO: get_body_parts
    #TODO: get_guid


if __name__ == "__main__":
    ignore_warnings(1)
    print(Item("Base.Twigs").get_burn_time())