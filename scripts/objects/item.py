"""
The `Item` class is a centralised way to access and manipulate data from the parsed script data.
Some properties will return another object, so properties can be strung together.
E.g., `item.blood_location.body_parts.wiki_links` returns a list of body parts as formatted links for an item.

Instances are cached and reused automatically by item ID.
"""

import os
from pathlib import Path
import csv
from scripts.parser import script_parser
from scripts.core.file_loading import get_script_path, get_media_dir
from scripts.core.language import Language, Translate
from scripts.utils import lua_helper, echo
from scripts.core import logger
from scripts.core.constants import RESOURCE_DIR
from scripts.core.cache import load_cache, save_cache
from scripts.core.version import Version
from scripts.utils.util import link
from scripts.core.page_manager import get_pages
from scripts.objects.components import FluidContainer, Durability
from scripts.objects.body_location import BloodLocationList, BloodLocation, BodyLocation
from scripts.objects.clothing_item import ClothingItem
from scripts.objects.skill import Skill, SkillBook
from scripts.objects.craft_recipe import CraftRecipe

class Item:
    """
    Represents a single parsed game item.

    Offers attribute-style access to raw values, translations,
    default handling, icon/model discovery, and logic for derived values
    like burn time or skill books. Also wraps component data
    such as durability or fluid container info.
    """
    _items = None  # Shared cache for all items
    _instances = {}
    _icon_cache_files = None
    _burn_data = None

    # Define property defaults
    _property_defaults = {
        "Type": "Normal",
        "DisplayCategory": "Unknown",
        "AlwaysWelcomeGift": False,
        "Tags": [],
        "IconsForTexture": [],
        "SwingAnim": "Rifle",
        "IdleAnim": "Idle",
        "RunAnim": "Run",
        "StaticModelsByIndex": [],
        "WorldStaticModelsByIndex": [],
        "ScaleWorldIcon": 1.0,
        "UseWorldItem": False,
        "WeaponSpritesByIndex": [],
        "ColorBlue": 255,
        "ColorGreen": 255,
        "ColorRed": 255,
        "SwingSound": "BaseballBatSwing",
        "DoorHitSound": "BaseballBatHit",
        "HitFloorSound": "BatOnFloor",
        "HitSound": "BaseballBatHit",
        "ClickSound": "Stormy9mmClick",
        "ImpactSound": "BaseballBatHit",
        "NPCSoundBoost": 1.0,
        "SoundMap": {},
        "Weight": 1.0,
        "Capacity": 0,
        "WeightReduction": 0,
        "WeightModifier": 0.0,
        "WeaponWeight": 1.0,
        "MaxItemSize": 0.0,
        "WeightEmpty": 0.0,
        "EvolvedRecipe": [],
        "ResearchableRecipes": [],
        "ResearchableRecipe": [],
        "TeachedRecipes": [],
        "Sharpness": 0.0,
        "HeadCondition": 0.0,
        "HeadConditionLowerChanceMultiplier": 1.0,
        "ConditionLowerChanceOneIn": 10,
        "CanAttach": False,
        "CanDetach": False,
        "ConditionMax": 10,
        "UseDelta": 0.03125,
        "UseWhileEquipped": True,
        "UseSelf": False,
        "RemoveOnBroken": True,
        "ticksPerEquipUse": 30,
        "CanBeReused": False,
        "HeadConditionMax": 0.0,
        "DisappearOnUse": True,
        "cantBeConsolided": False,
        "UseWhileUnequipped": False,
        "EquippedNoSprint": False,
        "ProtectFromRainWhenEquipped": False,
        "ReplaceOnCooked": [],
        "CanBarricade": False,
        "KeepOnDeplete": False,
        "ChanceToSpawnDamaged": 0,
        "MetalValue": 0.0,
        "DaysFresh": 1000000000,
        "DaysTotallyRotten": 1000000000,
        "HungerChange": 0.0,
        "ThirstChange": 0.0,
        "Calories": 0.0,
        "Carbohydrates": 0.0,
        "Lipids": 0.0,
        "Proteins": 0.0,
        "IsCookable": False,
        "MinutesToCook": 60,
        "MinutesToBurn": 120,
        "RemoveUnhappinessWhenCooked": False,
        "BadCold": False,
        "BadInMicrowave": False,
        "DangerousUncooked": False,
        "GoodHot": False,
        "CantEat": False,
        "CantBeFrozen": False,
        "Packaged": False,
        "Spice": False,
        "CannedFood": False,
        "EatTime": 0,
        "RemoveNegativeEffectOnCooked": False,
        "UnhappyChange": 0.0,
        "BoredomChange": 0.0,
        "StressChange": 0.0,
        "ReduceFoodSickness": 0,
        "EnduranceChange": 0.0,
        "PoisonPower": 0,
        "Medical": False,
        "Alcoholic": False,
        "BandagePower": 0.0,
        "CanBandage": False,
        "AlcoholPower": 0.0,
        "ReduceInfectionPower": 0.0,
        "FatigueChange": 0.0,
        "FluReduction": 0,
        "PainReduction": 0,
        "ExplosionPower": 0,
        "ExplosionRange": 0,
        "KnockdownMod": 1.0,
        "MaxDamage": 1.5,
        "MaxHitCount": 1000,
        "MaxRange": 1.0,
        "MinDamage": 0.0,
        "MinimumSwingTime": 0.0,
        "SwingAmountBeforeImpact": 0.0,
        "SwingTime": 1.0,
        "TriggerExplosionTimer": 0,
        "CanBePlaced": False,
        "CanBeRemote": False,
        "ExplosionTimer": 0,
        "SensorRange": 0,
        "SoundRadius": 0,
        "ReloadTimeModifier": 0.0,
        "MountOn": [],
        "BaseSpeed": 1.0,
        "Categories": [],
        "CritDmgMultiplier": 0.0,
        "CriticalChance": 20.0,
        "DoorDamage": 1,
        "KnockBackOnNoDeath": True,
        "MinAngle": 1.0,
        "MinRange": 0.0,
        "PushBackMod": 1.0,
        "SplatBloodOnNoDeath": False,
        "SplatNumber": 2,
        "SubCategory": "",
        "TreeDamage": 0,
        "WeaponLength": 0.4,
        "ProjectileSpreadModifier": 0.0,
        "MaxRangeModifier": 0.0,
        "AngleFalloff": False,
        "HaveChamber": True,
        "InsertAllBulletsReload": False,
        "ProjectileSpread": 0.0,
        "ProjectileWeightCenter": 1.0,
        "RackAfterShoot": False,
        "RangeFalloff": False,
        "OtherHandUse": False,
        "FirePower": 0,
        "FireRange": 0,
        "NoiseRange": 0,
        "AimingTimeModifier": 0.0,
        "HitChanceModifier": 0,
        "NoiseDuration": 0,
        "RecoilDelayModifier": 0.0,
        "RemoteController": False,
        "RemoteRange": 0,
        "ManuallyRemoveSpentRounds": False,
        "ExplosionDuration": 0,
        "SmokeRange": 0,
        "TriggerExplosionTimer": 0,
        "Count": 1,
        "CanStack": True,
        "MaxAmmo": 0,
        "AimingPerkCritModifier": 0,
        "AimingPerkHitChanceModifier": 0.0,
        "AimingPerkMinAngleModifier": 0.0,
        "AimingPerkRangeModifier": 0.0,
        "AimingTime": 0,
        "CyclicRateMultiplier": 1.0,
        "HitChance": 0,
        "IsAimedFirearm": False,
        "JamGunChance": 1.0,
        "MinSightRange": 0.0,
        "MaxSightRange": 0.0,
        "MultipleHitConditionAffected": True,
        "PiercingBullets": False,
        "ProjectileCount": 1,
        "Ranged": False,
        "RecoilDelay": 0,
        "ReloadTime": 0,
        "RequiresEquippedBothHands": False,
        "ShareDamage": True,
        "SoundGain": 1.0,
        "SoundVolume": 0,
        "SplatSize": 1.0,
        "StopPower": 5.0,
        "ToHitModifier": 1.0,
        "TwoHandWeapon": False,
        "UseEndurance": True,
        "ClipSize": 0,
        "DamageMakeHole": False,
        "HitAngleMod": 0.0,
        "EnduranceMod": 1.0,
        "LowLightBonus": 0.0,
        "AlwaysKnockdown": False,
        "critDmgMultiplier": 0.0,
        "AimingMod": 1.0,
        "IsAimedHandWeapon": False,
        "CantAttackWithLowestEndurance": False,
        "BodyLocation": "",
        "RunSpeedModifier": 1.0,
        "CanHaveHoles": True,
        "ChanceToFall": 0,
        "Insulation": 0.0,
        "WindResistance": 0.0,
        "ScratchDefense": 0.0,
        "DiscomfortModifier": 0.0,
        "WaterResistance": 0.0,
        "BiteDefense": 0.0,
        "CorpseSicknessDefense": 0.0,
        "HearingModifier": 1.0,
        "NeckProtectionModifier": 1.0,
        "VisualAid": False,
        "VisionModifier": 1.0,
        "AttachmentsProvided": [],
        "CombatSpeedModifier": 1.0,
        "BulletDefense": 0.0,
        "StompPower": 1.0,
        "AcceptMediaType": -1,
        "BaseVolumeRange": 0.0,
        "IsHighTier": False,
        "IsPortable": False,
        "IsTelevision": False,
        "MaxChannel": 108000,
        "MicRange": 0,
        "MinChannel": 88000,
        "NoTransmit": False,
        "TransmitRange": 0,
        "TwoWay": False,
        "UsesBattery": False,
        "RequireInHandOrInventory": [],
        "ActivatedItem": False,
        "LightDistance": 0,
        "LightStrength": 0.0,
        "TorchCone": False,
        "TorchDot": 0.96,
        "brakeForce": 0.0,
        "EngineLoudness": 0.0,
        "ConditionLowerStandard": 0.0,
        "ConditionLowerOffroad": 0.0,
        "SuspensionDamping": 0.0,
        "SuspensionCompression": 0.0,
        "WheelFriction": 0.0,
        "VehicleType": 0,
        "MaxCapacity": -1,
        "MechanicsItem": False,
        "ConditionAffectsCapacity": False,
        "CanBeWrite": False,
        "PageToWrite": 0,
        "LvlSkillTrained": -1,
        "NumLevelsTrained": 1,
        "NumberOfPages": -1,
        "SkillTrained": "",
        "IsDung": False,
        "SurvivalGear": False,
        "FishingLure": False,
        "Trap": False,
        "Padlock": False,
        "DigitalPadlock": False,
        "CanStoreWater": False,
        "IsWaterSource": False,
        "Wet": False,
        "Cosmetic": False,
        "FireFuelRatio": 0.0,
        "RainFactor": 0.0,
        "WetCooldown": 0.0,
        "OriginX": 0.0,
        "OriginY": 0.0,
        "OriginZ": 0.0,
        "ShoutMultiplier": 1.0,
        "OBSOLETE": False,
    }

    # Convert to lowercase
    _property_defaults = {
        k.lower(): v for k, v in _property_defaults.items()
    }

    def __new__(cls, item_id: str):
        """
        Return an existing Item instance if one already exists for the given ID.

        Fixes partial IDs like 'Axe' to 'Base.Axe' before checking or creating the instance.
        """
        if cls._items is None:
            cls._load_items()

        item_id = cls.fix_item_id(item_id)

        if item_id in cls._instances:
            return cls._instances[item_id]

        instance = super().__new__(cls)
        cls._instances[item_id] = instance
        return instance

    def __init__(self, item_id: str):
        """Initialise the Item instance with its data if not already initialised."""
        if hasattr(self, 'item_id'):
            return

        if Item._items is None:
            Item._load_items()

        item_id = self.fix_item_id(item_id)

        self._item_id = item_id
        self.data = Item._items.get(item_id, {})

        id_parts = item_id.split(".", 1)
        self._module = id_parts[0]
        self._id_type = id_parts[1] if len(id_parts) == 2 else None

        self._name = None
        self._name_en = None  # English name
        self._page = None     # Wiki page
        self._wiki_link = None # Wiki link
        self._has_page = None # Page defined (bool)
        self._icon = None     # Primary icon (str)
        self._icons = None    # All icons (list)
    
    def __getitem__(self, key):
        """Allow dictionary-style access to item data (e.g., item["DisplayName"])."""
        return self.data[key]
    
    def __contains__(self, key):
        """Allow 'in' checks for item data keys (e.g., "EvolvedRecipe" in item)."""
        return key in self.data
    
    def __repr__(self):
        """Return a string representation of the Item showing name, ID, type, and source path."""
        return (f'<Item {self._item_id}>')
    
    @staticmethod
    def _lower_keys(data: dict) -> dict:
        """
        Converts the keys of a dictionary to lowercase.

        Args:
            data (dict): Dictionary to normalise.

        Returns:
            dict: Dictionary with all top-level keys lowercased.
        """
        return {k.lower(): v for k, v in data.items()} if isinstance(data, dict) else data

    @classmethod
    def _load_items(cls):
        """
        Loads and normalises item script data into the class-level cache.

        All dictionary keys are lowercased to ensure consistent access.
        """
        raw_data = script_parser.extract_script_data("item")
        cls._items = {k: cls._lower_keys(v) for k, v in raw_data.items()}

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
        """Return all item IDs as a keys view."""
        if cls._items is None:
            cls._load_items()
        return cls._items.keys()

    @classmethod
    def values(cls):
        """Return all Item instances as a generator."""
        if cls._items is None:
            cls._load_items()
        return (cls(item_id) for item_id in cls._items)
    
    @classmethod
    def count(cls):
        """Return the total number of loaded items."""
        if cls._items is None:
            cls._load_items()
        return len(cls._items)
    
    @classmethod
    def get_icon_cache(cls):
        """Return the cached list of item icon filenames."""
        if cls._icon_cache_files is None:
            texture_cache = load_cache(f"{RESOURCE_DIR}/texture_names.json", "texture cache", suppress=True)
            cls._icon_cache_files = texture_cache.get("Item", [])
        return cls._icon_cache_files
    
    @classmethod
    def load_burn_data(cls):
        """Load and cache burn time data from camping_fuel.lua."""
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

    @classmethod
    def exists(cls, item_id: str) -> bool:
        if cls._items is None:
            cls._load_items()

        item_id = cls.fix_item_id(item_id)
        return item_id in cls._items
    
    ## ------------------------- Dict-like Methods ------------------------- ##

    def get(self, key: str, default=None):
        """
        Retrieve the value for a given key from item data.

        Args:
            key (str): The key to look up.
            default (any, optional): Fallback if the key is missing.

        Returns:
            any: The value from data or the provided default.
        """
        return self.data.get(key.lower(), default)
    
    ## ------------------------- Private Methods ------------------------- ##

    def _find_name(self, language: str = None) -> str:
        """
        Determines the display name of the item, handling special cases and translations.

        Args:
            language (str, optional): Language code (e.g., 'en'). If None, uses the active language.

        Returns:
            str: The resolved item name, including special case titles, vehicle part names, or translated display names.
        """
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

    def _find_icon(self):
        """
        Detects and sets the item's icon(s), checking CSV overrides, item properties, and icon variants.
        """
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
                    if row['item_id'] == self.item_id:
                        icon = [row['icon'] + ".png"]
                        break
        else:
            echo.warning(f"File '{icons_csv}' does not exist. Getting icon from item properties.")

        if not icon:
            icon = self.raw_icon

            if icon == "default":
                # Item is a tile, so should get WorldObjectSprite
                icon = self.world_object_sprite or "Flatpack"
            
            elif icon:
                # Use 'Icon' property
                icon_variants = ['Rotten', '_Rotten', 'Spoiled', 'Cooked', 'Burnt', '_Burnt', 'Overdone']
                icons = [icon]
                for variant in icon_variants:
                    variant_icon = f"{icon}{variant}.png"
                    if variant_icon in icon_cache_files:
                        icons.append(variant_icon)
                icon = icons
            
            elif self.icons_for_texture:
                # Use 'IconsForTeture' property
                icon = self.icons_for_texture

            elif self.world_object_sprite:
                # Use 'WorldObjectSprite' property
                icon = self.world_object_sprite
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
        """
        Formats the item's icon(s) for display or wiki markup, with optional cycling or custom names.

        Args:
            format (bool, optional): Whether to return wiki-formatted markup.
            all_icons (bool, optional): Whether to include all icon variants.
            cycling (bool, optional): Whether to wrap icons in a cycling image span.
            custom_name (str, optional): Custom display name for the icon.

        Returns:
            str or list[str]: Formatted wiki markup or raw icon filename(s).
        """
        if not self.data:
            echo.warning(f"Item ID '{self._item_id}' doesn't exist")
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
        if isinstance(icons, str):
            icons = [icons]

        icon_list = [
            f"[[File:{icon}|32x32px|link={self.page}{Language.get_subpage()}|{self.name}]]"
            for icon in icons
        ]

        if cycling and len(icon_list) > 1:
            return f'<span class="cycle-img">{"".join(icon_list)}</span>'
        return ''.join(icon_list)
    
    
    def _calculate_burn_time(self):
        """
        Calculate and store the burn time for this item based on weight, category, tags, and fuel data.
        """
        #TODO: clean up and use should_burn property
        if not self.data:
            self._burn_time = None
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
    
    ## ------------------------- Getter Methods ------------------------- ##

    def get_default(self, key: str, default=None):
        """
        Retrieve the value for a key using the class default if no explicit default is provided.

        Args:
            key (str): The key to look up.
            default (any, optional): Explicit fallback (overrides class default if provided).

        Returns:
            any: The value from data or the determined default.
        """
        key = key.lower()
        if default is None:
            default = self._property_defaults.get(key)
        return self.data.get(key, default)

    def get_component(self, key: str):
        """
        Retrieve a sprecific component dict from the item data.

        Args:
            key (str): The component key to look up.

        Returns:
            dict: The subcomponent data or an empty dict if missing.
        """
        return self.data.get("component", {}).get(key, {})

    def get_icon(self, format: bool = True, all_icons: bool = True, cycling: bool = True, custom_name: str = None) -> str | list[str]:
        """
        Returns the item's icon(s), either as raw filenames or formatted wiki markup.

        Args:
            format (bool, optional): Whether to return wiki-formatted markup. Defaults to True.
            all_icons (bool, optional): Whether to include all icon variants. Defaults to True.
            cycling (bool, optional): Whether to wrap icons in a cycling image span. Defaults to True.
            custom_name (str, optional): Custom display name for the icon. Defaults to None.

        Returns:
            str or list[str]: Formatted wiki markup or raw icon filename(s).
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
    
    def get_skill(self, raw : bool = False, get_all : bool = False):
        """
        Returns the skill(s) associated with the item.

        Args:
            raw (bool): If True, returns the raw skill name(s) as string(s) instead of Skill objects.
            get_all (bool): If True, returns a list of all associated skills. Otherwise returns only the primary one.

        Returns:
            Skill | list[Skill] | str | list[str] | None: A single Skill or skill name, a list of Skills or names,
            or None if no valid skill is found.
        """
        skill_list = self.categories or self.subcategory

        if not skill_list:
            return None
        
        if not isinstance(skill_list, list):
            skill_list = [skill_list]
        
        if "Improvised" in skill_list:
            skill_list = [s for s in skill_list if s != "Improvised"]
            if not skill_list:
                return None

        if not get_all:
            if len(skill_list) > 1:
                echo.warning(f"More than one skill value found for {self.item_id} with a value of: {skill_list}")
                return None

            skill_raw = skill_list[0]
            if skill_raw == "Firearm":
                skill_raw = "Aiming"

            return skill_raw if raw else Skill(skill_raw)

        expanded_skills = []
        for skill_raw in skill_list:
            if skill_raw == "Firearm":
                expanded_skills.extend(["Aiming", "Reloading"])
            else:
                expanded_skills.append(skill_raw)

        return [Skill(s) for s in expanded_skills]
    
    def get_body_parts(self, do_link:bool=True, raw_id:bool=False, default=None) -> list[str]:
        """
        Returns a list of body parts based on the item's `BloodLocation`.

        Args:
            do_link (bool): If True, returns wiki-linked names. Otherwise returns plain names.
            raw_id (bool): If True, returns internal body part ids.
            default (Any): Value to return if no blood location data is found.

        Returns:
            list[str] | Any: A list of body part names or links, or the provided default value if no data is found.
        """
        if not self.blood_location:
            return default
        if raw_id:
            return self.blood_location.body_parts.body_part_ids
        elif do_link:
            return self.blood_location.body_parts.wiki_links
        else:
            return self.blood_location.body_parts.names
    
    def get_recipes(self) -> list[str]:
        if not self.teached_recipes:
            return []
        
        products = []
        for recipe_id in self.teached_recipes:
            recipe = CraftRecipe(recipe_id)
            products.append(recipe.wiki_link)
        
        return products
    
    def get_fabric(self) -> str | None:
        """Returns the item id for the item's fabric type."""
        FABRIC_TYPES = {
            "Cotton": 'Base.RippedSheets',
            "Denim": 'Base.DenimStrips',
            "Leather": 'Base.LeatherStrips',
        }
        return FABRIC_TYPES.get(self.fabric_type)


    ## ------------------------- Misc Methods ------------------------- ##

    def has_tag(self, tag: str) -> bool:
        """
        Check if the item has a specific tag.

        Args:
            tag (str): The tag name to check.

        Returns:
            bool: True if the tag is present, False otherwise.
        """
        return bool(self.tags) and tag in self.tags
    
    ## ------------------------- Properties ------------------------- ##

    # --- Core --- #

    @property
    def valid(self) -> bool:
        return bool(self.data)

    @property
    def script_type(self) -> str:
        return self.data.get("ScriptType")

    @property
    def file(self):
        return self.data.get("SourceFile")

    @property
    def path(self):
        return get_script_path(self.file, prefer="item")

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
        if self._page is None or self._has_page is None:
            pages = get_pages(self.item_id, id_type="item_id")
            if pages:
                self._page = pages[0]
                self._has_page = True
            else:
                self._page = self.name_en
                self._has_page = False
        return self._page
    
    @property
    def has_page(self):
        if self._has_page is None:
            self.name
        return self._has_page

    @property
    def translation_name(self):
        return "ItemName_" + self.item_id

    @property
    def name(self):
        if self._name is None:
            self._name = self._find_name()
        return self._name

    @property
    def name_en(self):
        if self._name_en is None:
            self._name_en = self._find_name(language="en")
        return self._name_en

    @property
    def wiki_link(self):
        if self._wiki_link is None:
            self._wiki_link = link(self.page, self.name)
        return self._wiki_link
    
    @property
    def icon(self): 
        return self.get_icon()
    
    ## ------------------------- Script Properties ------------------------- ##

    # --- Base --- #
    @property
    def type(self) -> str: return self.get_default("Type")
    @property
    def display_category(self) -> str:
        if not hasattr(self, '_display_category'):
            self._display_category = Translate.get("IGUI_ItemCat_" + self.get_default("DisplayCategory"))
        return self._display_category
    @property
    def display_name(self) -> str: return self.get_default("DisplayName")
    @property
    def raw_display_category(self) -> str: return self.get_default("DisplayCategory")
    @property
    def always_welcome_gift(self) -> bool: return bool(self.get_default("AlwaysWelcomeGift"))
    @property
    def tags(self) -> list: return self.get_default("Tags")

    # --- Icon/Model/Animation --- #
    @property
    def raw_icon(self) -> str|None: return self.get_default("Icon")
    @property
    def icons_for_texture(self) -> list: return self.get_default("IconsForTexture")
    @property
    def static_model(self) -> str|None: return self.get_default("StaticModel")
    @property
    def world_static_model(self) -> str|None: return self.get_default("WorldStaticModel")
    @property
    def physics_object(self) -> str|None: return self.get_default("PhysicsObject")
    @property
    def placed_sprite(self) -> str|None: return self.get_default("PlacedSprite")
    @property
    def weapon_sprite(self) -> str|None: return self.get_default("WeaponSprite")
    @property
    def eat_type(self) -> str|None: return self.get_default("EatType")
    @property
    def swing_anim(self) -> str: return self.get_default("SwingAnim")
    @property
    def idle_anim(self) -> str: return self.get_default("IdleAnim")
    @property
    def run_anim(self) -> str: return self.get_default("RunAnim")
    @property
    def static_models_by_index(self) -> list: return self.get_default("StaticModelsByIndex")
    @property
    def world_static_models_by_index(self) -> list: return self.get_default("WorldStaticModelsByIndex")
    @property
    def primary_anim_mask(self) -> str|None: return self.get_default("PrimaryAnimMask")
    @property
    def secondary_anim_mask(self) -> str|None: return self.get_default("SecondaryAnimMask")
    @property
    def world_object_sprite(self) -> str|None: return self.get_default("WorldObjectSprite")
    @property
    def read_type(self) -> str|None: return self.get_default("ReadType")
    @property
    def scale_world_icon(self) -> float: return float(self.get_default("ScaleWorldIcon"))
    @property
    def use_world_item(self) -> bool: return bool(self.get_default("UseWorldItem"))
    @property
    def weapon_sprites_by_index(self) -> list: return self.get_default("WeaponSpritesByIndex")
    @property
    def color_blue(self) -> int: return int(self.get_default("ColorBlue"))
    @property
    def color_green(self) -> int: return int(self.get_default("ColorGreen"))
    @property
    def color_red(self) -> int: return int(self.get_default("ColorRed"))
    @property
    def icon_color_mask(self) -> str|None: return self.get_default("IconColorMask")
    @property
    def icon_fluid_mask(self) -> str|None: return self.get_default("IconFluidMask")
    @property
    def dig_type(self) -> str|None: return self.get_default("DigType")
    @property
    def pour_type(self) -> str|None: return self.get_default("PourType")

    # --- Sound --- #
    @property
    def place_multiple_sound(self) -> str|None: return self.get_default("PlaceMultipleSound")
    @property
    def place_one_sound(self) -> str|None: return self.get_default("PlaceOneSound")
    @property
    def cooking_sound(self) -> str|None: return self.get_default("CookingSound")
    @property
    def swing_sound(self) -> str: return self.get_default("SwingSound")
    @property
    def close_sound(self) -> str|None: return self.get_default("CloseSound")
    @property
    def open_sound(self) -> str|None: return self.get_default("OpenSound")
    @property
    def put_in_sound(self) -> str|None: return self.get_default("PutInSound")
    @property
    def break_sound(self) -> str|None: return self.get_default("BreakSound")
    @property
    def door_hit_sound(self) -> str: return self.get_default("DoorHitSound")
    @property
    def drop_sound(self) -> str|None: return self.get_default("DropSound")
    @property
    def hit_floor_sound(self) -> str: return self.get_default("HitFloorSound")
    @property
    def hit_sound(self) -> str: return self.get_default("HitSound")
    @property
    def aim_release_sound(self) -> str|None: return self.get_default("AimReleaseSound")
    @property
    def bring_to_bear_sound(self) -> str|None: return self.get_default("BringToBearSound")
    @property
    def click_sound(self) -> str: return self.get_default("ClickSound")
    @property
    def eject_ammo_sound(self) -> str|None: return self.get_default("EjectAmmoSound")
    @property
    def eject_ammo_start_sound(self) -> str|None: return self.get_default("EjectAmmoStartSound")
    @property
    def eject_ammo_stop_sound(self) -> str|None: return self.get_default("EjectAmmoStopSound")
    @property
    def equip_sound(self) -> str|None: return self.get_default("EquipSound")
    @property
    def custom_eat_sound(self) -> str|None: return self.get_default("CustomEatSound")
    @property
    def impact_sound(self) -> str: return self.get_default("ImpactSound")
    @property
    def insert_ammo_sound(self) -> str|None: return self.get_default("InsertAmmoSound")
    @property
    def insert_ammo_start_sound(self) -> str|None: return self.get_default("InsertAmmoStartSound")
    @property
    def insert_ammo_stop_sound(self) -> str|None: return self.get_default("InsertAmmoStopSound")
    @property
    def damaged_sound(self) -> str|None: return self.get_default("DamagedSound")
    @property
    def unequip_sound(self) -> str|None: return self.get_default("UnequipSound")
    @property
    def rack_sound(self) -> str|None: return self.get_default("RackSound")
    @property
    def npc_sound_boost(self) -> float: return float(self.get_default("NPCSoundBoost"))
    @property
    def sound_parameter(self) -> str|None: return self.get_default("SoundParameter")
    @property
    def sound_map(self) -> dict: return self.get_default("SoundMap", {})
    @property
    def fill_from_dispenser_sound(self) -> str|None: return self.get_default("FillFromDispenserSound")
    @property
    def fill_from_lake_sound(self) -> str|None: return self.get_default("FillFromLakeSound")
    @property
    def fill_from_tap_sound(self) -> str|None: return self.get_default("FillFromTapSound")
    @property
    def fill_from_toilet_sound(self) -> str|None: return self.get_default("FillFromToiletSound")

    # --- Weight/Container --- #
    @property
    def weight(self) -> float: return float(self.get_default("Weight"))
    @property
    def capacity(self) -> int: return int(self.get_default("Capacity"))
    @property
    def weight_reduction(self) -> int: return int(self.get_default("WeightReduction"))
    @property
    def accept_item_function(self) -> str|None: return self.get_default("AcceptItemFunction")
    @property
    def weight_modifier(self) -> float: return float(self.get_default("WeightModifier"))
    @property
    def weapon_weight(self) -> float: return float(self.get_default("WeaponWeight"))
    @property
    def max_item_size(self) -> float: return float(self.get_default("MaxItemSize"))
    @property
    def weight_empty(self) -> float: return float(self.get_default("WeightEmpty"))

    # --- Recipes/Condition/Replace/Usage --- #
    @property
    def evolved_recipe(self) -> list: return self.get_default("EvolvedRecipe")
    @property
    def evolved_recipe_name(self) -> str|None: return self.get_default("EvolvedRecipeName")
    @property #TODO: should these be CraftRecipe objects?
    def researchable_recipes(self) -> list: return self.get_default("ResearchableRecipes", self.get_default("ResearchableRecipe"))
    @property #TODO: should these be CraftRecipe objects?
    def teached_recipes(self) -> list: return self.get_default("TeachedRecipes")
    @property
    def sharpness(self) -> float: return float(self.get_default("Sharpness"))
    @property
    def head_condition(self) -> float: return float(self.get_default("HeadCondition"))
    @property
    def head_condition_lower_chance_multiplier(self) -> float: return float(self.get_default("HeadConditionLowerChanceMultiplier"))
    @property
    def condition_lower_chance_one_in(self) -> int: return int(self.get_default("ConditionLowerChanceOneIn"))
    @property
    def can_attach(self) -> bool: return bool(self.get_default("CanAttach"))
    @property
    def can_detach(self) -> bool: return bool(self.get_default("CanDetach"))
    @property
    def condition_max(self) -> int: return int(self.get_default("ConditionMax"))
    @property
    def replace_on_use(self) -> str|None: return self.get_default("ReplaceOnUse")
    @property
    def replace_on_use_on(self) -> str|None: return self.get_default("ReplaceOnUseOn")
    @property
    def consolidate_option(self) -> str|None: return self.get_default("ConsolidateOption")
    @property
    def use_delta(self) -> float: return float(self.get_default("UseDelta"))
    @property
    def use_while_equipped(self) -> bool: return bool(self.get_default("UseWhileEquipped"))
    @property
    def use_self(self) -> bool: return bool(self.get_default("UseSelf"))
    @property
    def replace_on_deplete(self) -> str|None: return self.get_default("ReplaceOnDeplete")
    @property
    def remove_on_broken(self) -> bool: return bool(self.get_default("RemoveOnBroken"))
    @property
    def without_drainable(self) -> str|None: return self.get_default("WithoutDrainable")
    @property
    def with_drainable(self) -> str|None: return self.get_default("WithDrainable")
    @property
    def ticks_per_equip_use(self) -> int: return int(self.get_default("ticksPerEquipUse"))
    @property
    def can_be_reused(self) -> bool: return bool(self.get_default("CanBeReused"))
    @property
    def head_condition_max(self) -> float: return float(self.get_default("HeadConditionMax"))
    @property
    def disappear_on_use(self) -> bool: return bool(self.get_default("DisappearOnUse"))
    @property
    def cant_be_consolided(self) -> bool: return bool(self.get_default("cantBeConsolided"))
    @property
    def use_while_unequipped(self) -> bool: return bool(self.get_default("UseWhileUnequipped"))
    @property
    def equipped_no_sprint(self) -> bool: return bool(self.get_default("EquippedNoSprint"))
    @property
    def protect_from_rain_when_equipped(self) -> bool: return bool(self.get_default("ProtectFromRainWhenEquipped"))
    @property
    def replace_on_cooked(self) -> list: return self.get_default("ReplaceOnCooked")
    @property
    def item_after_cleaning(self) -> str|None: return self.get_default("ItemAfterCleaning")
    @property
    def can_barricade(self) -> bool: return bool(self.get_default("CanBarricade"))
    @property
    def keep_on_deplete(self) -> bool: return bool(self.get_default("KeepOnDeplete"))
    @property
    def chance_to_spawn_damaged(self) -> int: return int(self.get_default("ChanceToSpawnDamaged"))
    @property
    def metal_value(self) -> float: return float(self.get_default("MetalValue"))

    # --- Food --- #
    @property
    def food_type(self) -> str|None: return self.get_default("FoodType")
    @property
    def days_fresh(self) -> int: return int(self.get_default("DaysFresh"))
    @property
    def days_totally_rotten(self) -> int: return int(self.get_default("DaysTotallyRotten"))
    @property
    def hunger_change(self) -> float: return float(self.get_default("HungerChange"))
    @property
    def thirst_change(self) -> float: return float(self.get_default("ThirstChange"))
    @property
    def calories(self) -> float: return float(self.get_default("Calories"))
    @property
    def carbohydrates(self) -> float: return float(self.get_default("Carbohydrates"))
    @property
    def lipids(self) -> float: return float(self.get_default("Lipids"))
    @property
    def proteins(self) -> float: return float(self.get_default("Proteins"))
    @property
    def is_cookable(self) -> bool: return bool(self.get_default("IsCookable"))
    @property
    def minutes_to_cook(self) -> int: return int(self.get_default("MinutesToCook"))
    @property
    def minutes_to_burn(self) -> int: return int(self.get_default("MinutesToBurn"))
    @property
    def remove_unhappiness_when_cooked(self) -> bool: return bool(self.get_default("RemoveUnhappinessWhenCooked"))
    @property
    def bad_cold(self) -> bool: return bool(self.get_default("BadCold"))
    @property
    def bad_in_microwave(self) -> bool: return bool(self.get_default("BadInMicrowave"))
    @property
    def dangerous_uncooked(self) -> bool: return bool(self.get_default("DangerousUncooked"))
    @property
    def good_hot(self) -> bool: return bool(self.get_default("GoodHot"))
    @property
    def cant_eat(self) -> bool: return bool(self.get_default("CantEat"))
    @property
    def cant_be_frozen(self) -> bool: return bool(self.get_default("CantBeFrozen"))
    @property
    def animal_feed_type(self) -> str|None: return self.get_default("AnimalFeedType")
    @property
    def packaged(self) -> bool: return bool(self.get_default("Packaged"))
    @property
    def spice(self) -> bool: return bool(self.get_default("Spice"))
    @property
    def canned_food(self) -> bool: return bool(self.get_default("CannedFood"))
    @property
    def replace_on_rotten(self) -> str|None: return self.get_default("ReplaceOnRotten")
    @property
    def eat_time(self) -> int: return int(self.get_default("EatTime"))
    @property
    def remove_negative_effect_on_cooked(self) -> bool: return bool(self.get_default("RemoveNegativeEffectOnCooked"))

    # --- Effects/Medical --- #
    @property
    def unhappy_change(self) -> float: return float(self.get_default("UnhappyChange"))
    @property
    def boredom_change(self) -> float: return float(self.get_default("BoredomChange"))
    @property
    def stress_change(self) -> float: return float(self.get_default("StressChange"))
    @property
    def reduce_food_sickness(self) -> int: return int(self.get_default("ReduceFoodSickness"))
    @property
    def endurance_change(self) -> float: return float(self.get_default("EnduranceChange"))
    @property
    def poison_power(self) -> int: return int(self.get_default("PoisonPower"))
    @property
    def medical(self) -> bool: return bool(self.get_default("Medical"))
    @property
    def alcoholic(self) -> bool: return bool(self.get_default("Alcoholic"))
    @property
    def bandage_power(self) -> float: return float(self.get_default("BandagePower"))
    @property
    def can_bandage(self) -> bool: return bool(self.get_default("CanBandage"))
    @property
    def alcohol_power(self) -> float: return float(self.get_default("AlcoholPower"))
    @property
    def reduce_infection_power(self) -> float: return float(self.get_default("ReduceInfectionPower"))
    @property
    def fatigue_change(self) -> float: return float(self.get_default("FatigueChange"))
    @property
    def flu_reduction(self) -> int: return int(self.get_default("FluReduction"))
    @property
    def herbalist_type(self) -> str|None: return self.get_default("HerbalistType")
    @property
    def pain_reduction(self) -> int: return int(self.get_default("PainReduction"))

    # --- Weapon --- #
    @property
    def explosion_power(self) -> int: return int(self.get_default("ExplosionPower"))
    @property
    def explosion_range(self) -> int: return int(self.get_default("ExplosionRange"))
    @property
    def explosion_sound(self) -> str|None: return self.get_default("ExplosionSound")
    @property
    def knockdown_mod(self) -> float: return float(self.get_default("KnockdownMod"))
    @property
    def max_damage(self) -> float: return float(self.get_default("MaxDamage"))
    @property
    def max_hit_count(self) -> int: return int(self.get_default("MaxHitCount"))
    @property
    def max_range(self) -> float: return float(self.get_default("MaxRange"))
    @property
    def min_damage(self) -> float: return float(self.get_default("MinDamage"))
    @property
    def minimum_swing_time(self) -> float: return float(self.get_default("MinimumSwingTime"))
    @property
    def swing_amount_before_impact(self) -> float: return float(self.get_default("SwingAmountBeforeImpact"))
    @property
    def swing_time(self) -> float: return float(self.get_default("SwingTime"))
    @property
    def trigger_explosion_timer(self) -> int: return int(self.get_default("TriggerExplosionTimer"))
    @property
    def can_be_placed(self) -> bool: return bool(self.get_default("CanBePlaced"))
    @property
    def can_be_remote(self) -> bool: return bool(self.get_default("CanBeRemote"))
    @property
    def explosion_timer(self) -> int: return int(self.get_default("ExplosionTimer"))
    @property
    def sensor_range(self) -> int: return int(self.get_default("SensorRange"))
    @property
    def alarm_sound(self) -> str|None: return self.get_default("AlarmSound")
    @property
    def sound_radius(self) -> int: return int(self.get_default("SoundRadius"))
    @property
    def reload_time_modifier(self) -> float: return float(self.get_default("ReloadTimeModifier"))
    @property
    def mount_on(self) -> list: return self.get_default("MountOn")
    @property
    def part_type(self) -> str|None: return self.get_default("PartType")
    @property
    def attachment_type(self) -> str|None: return self.get_default("AttachmentType")
    @property
    def base_speed(self) -> float: return float(self.get_default("BaseSpeed"))
    @property
    def categories(self) -> list: return self.get_default("Categories")
    @property
    def crit_dmg_multiplier(self) -> float: return float(self.get_default("CritDmgMultiplier"))
    @property
    def critical_chance(self) -> float: return float(self.get_default("CriticalChance"))
    @property
    def door_damage(self) -> int: return int(self.get_default("DoorDamage"))
    @property
    def knock_back_on_no_death(self) -> bool: return bool(self.get_default("KnockBackOnNoDeath"))
    @property
    def min_angle(self) -> float: return float(self.get_default("MinAngle"))
    @property
    def min_range(self) -> float: return float(self.get_default("MinRange"))
    @property
    def push_back_mod(self) -> float: return float(self.get_default("PushBackMod"))
    @property
    def splat_blood_on_no_death(self) -> bool: return bool(self.get_default("SplatBloodOnNoDeath"))
    @property
    def splat_number(self) -> int: return int(self.get_default("SplatNumber"))
    @property
    def subcategory(self) -> str|None: return self.get_default("SubCategory")
    @property
    def tree_damage(self) -> int: return int(self.get_default("TreeDamage"))
    @property
    def weapon_length(self) -> float: return float(self.get_default("WeaponLength"))
    @property
    def projectile_spread_modifier(self) -> float: return float(self.get_default("ProjectileSpreadModifier"))
    @property
    def max_range_modifier(self) -> float: return float(self.get_default("MaxRangeModifier"))
    @property
    def angle_falloff(self) -> bool: return bool(self.get_default("AngleFalloff"))
    @property
    def have_chamber(self) -> bool: return bool(self.get_default("HaveChamber"))
    @property
    def insert_all_bullets_reload(self) -> bool: return bool(self.get_default("InsertAllBulletsReload"))
    @property
    def projectile_spread(self) -> float: return float(self.get_default("ProjectileSpread"))
    @property
    def projectile_weight_center(self) -> float: return float(self.get_default("ProjectileWeightCenter"))
    @property
    def rack_after_shoot(self) -> bool: return bool(self.get_default("RackAfterShoot"))
    @property
    def range_falloff(self) -> bool: return bool(self.get_default("RangeFalloff"))
    @property
    def other_hand_use(self) -> bool: return bool(self.get_default("OtherHandUse"))
    @property
    def other_hand_require(self) -> str|None: return self.get_default("OtherHandRequire")
    @property
    def fire_power(self) -> int: return int(self.get_default("FirePower"))
    @property
    def fire_range(self) -> int: return int(self.get_default("FireRange"))
    @property
    def noise_range(self) -> int: return int(self.get_default("NoiseRange"))
    @property
    def aiming_time_modifier(self) -> float: return float(self.get_default("AimingTimeModifier"))
    @property
    def hit_chance_modifier(self) -> int: return int(self.get_default("HitChanceModifier"))
    @property
    def noise_duration(self) -> int: return int(self.get_default("NoiseDuration"))
    @property
    def recoil_delay_modifier(self) -> float: return float(self.get_default("RecoilDelayModifier"))
    @property
    def remote_controller(self) -> bool: return bool(self.get_default("RemoteController"))
    @property
    def remote_range(self) -> int: return int(self.get_default("RemoteRange"))
    @property
    def manually_remove_spent_rounds(self) -> bool: return bool(self.get_default("ManuallyRemoveSpentRounds"))
    @property
    def explosion_duration(self) -> int: return int(self.get_default("ExplosionDuration"))
    @property
    def smoke_range(self) -> int: return int(self.get_default("SmokeRange"))
    @property
    def count_(self) -> int: return int(self.get_default("Count"))
    @property
    def ammo_type(self) -> str|None: return self.get_default("AmmoType")
    @property
    def can_stack(self) -> bool: return bool(self.get_default("CanStack"))
    @property
    def gun_type(self) -> str|None: return self.get_default("GunType")
    @property
    def max_ammo(self) -> int: return int(self.get_default("MaxAmmo"))
    @property
    def aiming_perk_crit_modifier(self) -> int: return int(self.get_default("AimingPerkCritModifier"))
    @property
    def aiming_perk_hit_chance_modifier(self) -> float: return float(self.get_default("AimingPerkHitChanceModifier"))
    @property
    def aiming_perk_min_angle_modifier(self) -> float: return float(self.get_default("AimingPerkMinAngleModifier"))
    @property
    def aiming_perk_range_modifier(self) -> float: return float(self.get_default("AimingPerkRangeModifier"))
    @property
    def aiming_time(self) -> int: return int(self.get_default("AimingTime"))
    @property
    def ammo_box(self) -> str|None: return self.get_default("AmmoBox")
    @property
    def fire_mode(self) -> str|None: return self.get_default("FireMode")
    @property
    def fire_mode_possibilities(self) -> list: return self.get_default("FireModePossibilities")
    @property
    def cyclic_rate_multiplier(self) -> float: return float(self.get_default("CyclicRateMultiplier"))
    @property
    def hit_chance(self) -> int: return int(self.get_default("HitChance"))
    @property
    def is_aimed_firearm(self) -> bool: return bool(self.get_default("IsAimedFirearm"))
    @property
    def jam_gun_chance(self) -> float: return float(self.get_default("JamGunChance"))
    @property
    def magazine_type(self) -> str|None: return self.get_default("MagazineType")
    @property
    def min_sight_range(self) -> float: return float(self.get_default("MinSightRange"))
    @property
    def max_sight_range(self) -> float: return float(self.get_default("MaxSightRange"))
    @property
    def model_weapon_part(self) -> str|None: return self.get_default("ModelWeaponPart")
    @property
    def multiple_hit_condition_affected(self) -> bool: return bool(self.get_default("MultipleHitConditionAffected"))
    @property
    def piercing_bullets(self) -> bool: return bool(self.get_default("PiercingBullets"))
    @property
    def projectile_count(self) -> int: return int(self.get_default("ProjectileCount"))
    @property
    def ranged(self) -> bool: return bool(self.get_default("Ranged"))
    @property
    def recoil_delay(self) -> int: return int(self.get_default("RecoilDelay"))
    @property
    def reload_time(self) -> int: return int(self.get_default("ReloadTime"))
    @property
    def requires_equipped_both_hands(self) -> bool: return bool(self.get_default("RequiresEquippedBothHands"))
    @property
    def share_damage(self) -> bool: return bool(self.get_default("ShareDamage"))
    @property
    def shell_fall_sound(self) -> str|None: return self.get_default("ShellFallSound")
    @property
    def sound_gain(self) -> float: return float(self.get_default("SoundGain"))
    @property
    def sound_volume(self) -> int: return int(self.get_default("SoundVolume"))
    @property
    def splat_size(self) -> float: return float(self.get_default("SplatSize"))
    @property
    def stop_power(self) -> float: return float(self.get_default("StopPower"))
    @property
    def to_hit_modifier(self) -> float: return float(self.get_default("ToHitModifier"))
    @property
    def two_hand_weapon(self) -> bool: return bool(self.get_default("TwoHandWeapon"))
    @property
    def use_endurance(self) -> bool: return bool(self.get_default("UseEndurance"))
    @property
    def weapon_reload_type(self) -> str|None: return self.get_default("WeaponReloadType")
    @property
    def clip_size(self) -> int: return int(self.get_default("ClipSize"))
    @property
    def damage_category(self) -> str|None: return self.get_default("DamageCategory")
    @property
    def damage_make_hole(self) -> bool: return bool(self.get_default("DamageMakeHole"))
    @property
    def hit_angle_mod(self) -> float: return float(self.get_default("HitAngleMod"))
    @property
    def endurance_mod(self) -> float: return float(self.get_default("EnduranceMod"))
    @property
    def low_light_bonus(self) -> float: return float(self.get_default("LowLightBonus"))
    @property
    def always_knockdown(self) -> bool: return bool(self.get_default("AlwaysKnockdown"))
    @property
    def aiming_mod(self) -> float: return float(self.get_default("AimingMod"))
    @property
    def is_aimed_hand_weapon(self) -> bool: return bool(self.get_default("IsAimedHandWeapon"))
    @property
    def cant_attack_with_lowest_endurance(self) -> bool: return bool(self.get_default("CantAttackWithLowestEndurance"))
    @property
    def close_kill_move(self) -> str|None: return self.get_default("CloseKillMove")

    # --- Clothing --- #
    @property
    def body_location(self) -> BodyLocation | None:
        loc = self.get_default("BodyLocation")
        return BodyLocation(loc) if loc else None
    @property
    def clothing_item(self) -> ClothingItem|None:
        value = self.get_default("ClothingItem")
        if value:
            return ClothingItem(value)
        return None
    @property
    def can_be_equipped(self) -> BodyLocation | None:
        loc = self.get_default("CanBeEquipped")
        return BodyLocation(loc) if loc else None
    @property
    def run_speed_modifier(self) -> float: return float(self.get_default("RunSpeedModifier"))
    @property
    def blood_location(self) -> BloodLocationList|None:
        value = self.get_default("BloodLocation")
        if value:
            locations = [BloodLocation(v) for v in value]
            return BloodLocationList(locations)
        return None
    @property
    def can_have_holes(self) -> bool: return bool(self.get_default("CanHaveHoles"))
    @property
    def chance_to_fall(self) -> int: return int(self.get_default("ChanceToFall"))
    @property
    def insulation(self) -> float: return float(self.get_default("Insulation"))
    @property
    def wind_resistance(self) -> float: return float(self.get_default("WindResistance"))
    @property
    def fabric_type(self) -> str|None: return self.get_default("FabricType")
    @property
    def scratch_defense(self) -> float: return float(self.get_default("ScratchDefense"))
    @property
    def discomfort_modifier(self) -> float: return float(self.get_default("DiscomfortModifier"))
    @property
    def water_resistance(self) -> float: return float(self.get_default("WaterResistance"))
    @property
    def bite_defense(self) -> float: return float(self.get_default("BiteDefense"))
    @property
    def attachment_replacement(self) -> str|None: return self.get_default("AttachmentReplacement")
    @property
    def clothing_item_extra(self) -> str|None: return self.get_default("ClothingItemExtra")
    @property
    def clothing_item_extra_option(self) -> str|None: return self.get_default("ClothingItemExtraOption")
    @property
    def replace_in_second_hand(self) -> str|None: return self.get_default("ReplaceInSecondHand")
    @property
    def replace_in_primary_hand(self) -> str|None: return self.get_default("ReplaceInPrimaryHand")
    @property
    def corpse_sickness_defense(self) -> float: return float(self.get_default("CorpseSicknessDefense"))
    @property
    def hearing_modifier(self) -> float: return float(self.get_default("HearingModifier"))
    @property
    def neck_protection_modifier(self) -> float: return float(self.get_default("NeckProtectionModifier"))
    @property
    def visual_aid(self) -> bool: return bool(self.get_default("VisualAid"))
    @property
    def vision_modifier(self) -> float: return float(self.get_default("VisionModifier"))
    @property
    def attachments_provided(self) -> list: return self.get_default("AttachmentsProvided")
    @property
    def combat_speed_modifier(self) -> float: return float(self.get_default("CombatSpeedModifier"))
    @property
    def bullet_defense(self) -> float: return float(self.get_default("BulletDefense"))
    @property
    def stomp_power(self) -> float: return float(self.get_default("StompPower"))

    # --- Tooltip/Menu --- #
    @property
    def tooltip(self) -> str|None: return self.get_default("Tooltip", self.get_default("ToolTip"))
    @property
    def custom_context_menu(self) -> str|None: return self.get_default("CustomContextMenu")
    @property
    def clothing_extra_submenu(self) -> str|None: return self.get_default("ClothingExtraSubmenu", self.get_default("clothingExtraSubmenu"))

    # --- Lua Functions --- #
    @property
    def on_create(self) -> str|None: return self.get_default("OnCreate")
    @property
    def on_break(self) -> str|None: return self.get_default("OnBreak")
    @property
    def on_cooked(self) -> str|None: return self.get_default("OnCooked")
    @property
    def on_eat(self) -> str|None: return self.get_default("OnEat")

    # --- Electrical/Light --- #
    @property
    def accept_media_type(self) -> int: return int(self.get_default("AcceptMediaType"))
    @property
    def media_category(self) -> str|None: return self.get_default("MediaCategory")
    @property
    def base_volume_range(self) -> float: return float(self.get_default("BaseVolumeRange"))
    @property
    def is_high_tier(self) -> bool: return bool(self.get_default("IsHighTier"))
    @property
    def is_portable(self) -> bool: return bool(self.get_default("IsPortable"))
    @property
    def is_television(self) -> bool: return bool(self.get_default("IsTelevision"))
    @property
    def max_channel(self) -> int: return int(self.get_default("MaxChannel"))
    @property
    def mic_range(self) -> int: return int(self.get_default("MicRange"))
    @property
    def min_channel(self) -> int: return int(self.get_default("MinChannel"))
    @property
    def no_transmit(self) -> bool: return bool(self.get_default("NoTransmit"))
    @property
    def transmit_range(self) -> int: return int(self.get_default("TransmitRange"))
    @property
    def two_way(self) -> bool: return bool(self.get_default("TwoWay"))
    @property
    def uses_battery(self) -> bool: return bool(self.get_default("UsesBattery"))
    @property
    def require_in_hand_or_inventory(self) -> list: return self.get_default("RequireInHandOrInventory")
    @property
    def activated_item(self) -> bool: return bool(self.get_default("ActivatedItem"))
    @property
    def light_distance(self) -> int: return int(self.get_default("LightDistance"))
    @property
    def light_strength(self) -> float: return float(self.get_default("LightStrength"))
    @property
    def torch_cone(self) -> bool: return bool(self.get_default("TorchCone"))
    @property
    def torch_dot(self) -> float: return float(self.get_default("TorchDot"))

    # --- Vehicle Parts --- #
    @property
    def vehicle_part_model(self) -> str|None: return self.get_default("VehiclePartModel")
    @property
    def brake_force(self) -> float: return float(self.get_default("brakeForce"))
    @property
    def engine_loudness(self) -> float: return float(self.get_default("EngineLoudness"))
    @property
    def condition_lower_standard(self) -> float: return float(self.get_default("ConditionLowerStandard"))
    @property
    def condition_lower_offroad(self) -> float: return float(self.get_default("ConditionLowerOffroad"))
    @property
    def suspension_damping(self) -> float: return float(self.get_default("SuspensionDamping"))
    @property
    def suspension_compression(self) -> float: return float(self.get_default("SuspensionCompression"))
    @property
    def wheel_friction(self) -> float: return float(self.get_default("WheelFriction"))
    @property
    def vehicle_type(self) -> int: return int(self.get_default("VehicleType"))
    @property
    def max_capacity(self) -> int: return int(self.get_default("MaxCapacity"))
    @property
    def mechanics_item(self) -> bool: return bool(self.get_default("MechanicsItem"))
    @property
    def condition_affects_capacity(self) -> bool: return bool(self.get_default("ConditionAffectsCapacity"))

    # --- Literature --- #
    @property
    def can_be_write(self) -> bool: return bool(self.get_default("CanBeWrite"))
    @property
    def page_to_write(self) -> int: return int(self.get_default("PageToWrite"))
    @property
    def map(self) -> str|None: return self.get_default("Map")
    @property
    def lvl_skill_trained(self) -> int: return int(self.get_default("LvlSkillTrained"))
    @property
    def num_levels_trained(self) -> int: return int(self.get_default("NumLevelsTrained"))
    @property
    def number_of_pages(self) -> int: return int(self.get_default("NumberOfPages"))
    @property
    def skill_trained(self) -> SkillBook|None:
        if not hasattr(self, "_skill_trained"):
            raw_skill_trained = self.get("SkillTrained")
            self._skill_trained = SkillBook(raw_skill_trained) if raw_skill_trained else None
        return self._skill_trained

    # --- Misc Flags --- #
    @property
    def is_dung(self) -> bool: return bool(self.get_default("IsDung"))
    @property
    def survival_gear(self) -> bool: return bool(self.get_default("SurvivalGear"))
    @property
    def fishing_lure(self) -> bool: return bool(self.get_default("FishingLure"))
    @property
    def trap(self) -> bool: return bool(self.get_default("Trap"))
    @property
    def padlock(self) -> bool: return bool(self.get_default("Padlock"))
    @property
    def digital_padlock(self) -> bool: return bool(self.get_default("DigitalPadlock"))
    @property
    def can_store_water(self) -> bool: return bool(self.get_default("CanStoreWater"))
    @property
    def is_water_source(self) -> bool: return bool(self.get_default("IsWaterSource"))
    @property
    def wet(self) -> bool: return bool(self.get_default("Wet"))
    @property
    def cosmetic(self) -> bool: return bool(self.get_default("Cosmetic"))
    @property
    def obsolete(self) -> bool: return bool(self.get_default("OBSOLETE"))

    # --- Misc --- #
    @property
    def fire_fuel_ratio(self) -> float: return float(self.get_default("FireFuelRatio"))
    @property
    def rain_factor(self) -> float: return float(self.get_default("RainFactor"))
    @property
    def wet_cooldown(self) -> float: return float(self.get_default("WetCooldown"))
    @property
    def origin_x(self) -> float: return float(self.get_default("OriginX"))
    @property
    def origin_y(self) -> float: return float(self.get_default("OriginY"))
    @property
    def origin_z(self) -> float: return float(self.get_default("OriginZ"))
    @property
    def item_when_dry(self) -> str|None: return self.get_default("ItemWhenDry")
    @property
    def spawn_with(self) -> list: return self.get_default("SpawnWith")
    @property
    def make_up_type(self) -> str|None: return self.get_default("MakeUpType")
    @property
    def shout_type(self) -> str|None: return self.get_default("ShoutType")
    @property
    def shout_multiplier(self) -> float: return float(self.get_default("ShoutMultiplier"))

    # --- Components --- #

    @property
    def components(self) -> list:
        """Returns a list of component keys defined for the item."""
        return list(self.data.get("component", {}).keys())

    @property
    def fluid_container(self) -> FluidContainer:
        """Returns the item's FluidContainer component."""
        if not hasattr(self, '_fluid_container'):
            self._fluid_container = FluidContainer(self.get_component("FluidContainer"))
        return self._fluid_container

    @property
    def durability(self) -> Durability:
        """Returns the item's Durability component."""
        if not hasattr(self, '_durability'):
            self._durability = Durability(self.get_component("Durability"))
        return self._durability


    # --- Inferred Properties --- #
    
    @property
    def skill(self) -> Skill|None:
        """
        Returns the primary skill associated with the item, if any.
        """
        if not hasattr(self, "_skill"):
            self._skill = self.get_skill()
        return self._skill

    @property
    def weight_full(self) -> int|float:
        """
        Returns the item's total weight when full, whether with fluids or items.
        Rounded to 2 decimal places, returns an int if no remainder.
        """
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
    def burn_time(self) -> str|None:
        """
        Returns the burn time the item provides.
        """
        if not hasattr(self, "_burn_time"):
            self._calculate_burn_time()
        return self._burn_time

    @property
    def should_burn(self) -> bool:
        """
        Returns True if the item is expected to burn.
        Based on game logic from `ISCampingMenu.shouldBurn()`.
        """
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
    def is_tinder(self) -> bool|None:
        """
        Returns whether the item is valid tinder.
        Based on game logic from `ISCampingMenu.isValidTinder()`.
        Returns None if the item shouldn't burn.
        """
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
    
    @property
    def models(self) -> list[str]:
        """
        Returns a list of model texture filenames for this item.
        Finds the correct model names based on clothing textures or static model values, and formats them as `<Name>_Model.png`.
        """
        if hasattr(self, "_models"):
            return self._models
        textures_dir = Path(get_media_dir()) / "textures"
        models = None


        if self.clothing_item:
            model_path = self.clothing_item.texture_choices
            if not model_path:
                model_path = self.clothing_item.base_textures
            
            # Remove filepath and capitalize
            if model_path:
                if isinstance(model_path, str):
                    model_path = [model_path]

                models = []
                
                # Check the file path and get the correct capitalisation for the model texture
                for model_value in model_path:
                    model_value = os.path.normpath(model_value).replace(os.sep, "/")
                    full_path = textures_dir / f"{model_value}.png"

                    parent_dir = full_path.parent
                    filename_lower = full_path.name.lower()

                    if parent_dir.exists():
                        for file in parent_dir.iterdir():
                            if file.is_file() and file.name.lower() == filename_lower:
                                file_match = file.stem
                                break

                    if file_match:
                        models.append(file_match)
                    else:
                        models.append(model_value)

        elif self.world_static_models_by_index:
            models = self.world_static_models_by_index

        if models is None:
            models = self.world_static_model or self.weapon_sprite or self.static_model

        if models == '':
            self._models = models
            echo.warning(f"{self.item_id} has no model value.")
            return models
        
        if not isinstance(models, list):
            models = [models]
        
        # Remove Ground suffix
        models = [model.replace('_Ground', '').replace('Ground', '') for model in models]
        
        # Add suffix and extension
        models = [f"{value}_Model.png" for value in models]

        self._models = models
        return models
    
    @property
    def skill_multiplier(self) -> float:
        """
        XP multiplier based on the skill book and training level.
        Returns 1 if no skill book is set.
        """
        if not self.skill_trained:
            return 1

        return self.skill_trained.get_multiplier(self.lvl_skill_trained)


if __name__ == "__main__":
    from scripts.utils import util
    item = Item("Base.Necklace_Choker_Bone")
    neck_protection = "-"
    if item.blood_location:
        if "Neck" in item.get_body_parts(do_link=False):
            neck_protection = item.neck_protection_modifier
            neck_protection = util.convert_percentage(neck_protection, True)
    print(neck_protection)