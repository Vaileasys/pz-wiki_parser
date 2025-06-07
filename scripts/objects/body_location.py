import re
from scripts.core.language import Translate, Language
from scripts.core.cache import save_cache
from scripts.core.file_loading import get_lua_files, read_file
from scripts.utils.util import to_bool

class BodyLocation:
    _raw_data = None
    _all_data = None
    _items = None
    _instances = {}

    ## --------------- Class Methods --------------- ##

    @classmethod
    def _load_data(cls):
        cls._parse_locations()
        cls._parse_items()
        cls._rearrange_data()

    @classmethod
    def _parse_locations(cls):
        file_path = get_lua_files("BodyLocations.lua", prefer="NPCs")[0]

        group_name = None
        locations = []
        exclusives = {}
        hide_models = {}
        alt_models = {}
        aliases = {}
        multi_items = {}

        file = read_file(file_path).splitlines()
        for line in file:
            line = line.strip()
            if line.startswith("--") or not line:
                continue

            m = re.match(r'local\s+group\s*=\s*BodyLocations\.getGroup\("([^"]+)"\)', line)
            if m:
                group_name = m.group(1)
                continue

            m = re.match(r'group:getOrCreateLocation\("([^"]+)"\)', line)
            if m:
                locations.append(m.group(1))
                continue

            m = re.match(r'group:setExclusive\("([^"]+)",\s*"([^"]+)"\)', line)
            if m:
                key, value = m.group(1), m.group(2)
                exclusives.setdefault(key, []).append(value)
                continue

            m = re.match(r'group:setHideModel\("([^"]+)",\s*"([^"]+)"\)', line)
            if m:
                key, value = m.group(1), m.group(2)
                hide_models.setdefault(key, []).append(value)
                continue

            m = re.match(r'group:setAltModel\("([^"]+)",\s*"([^"]+)"\)', line)
            if m:
                key, value = m.group(1), m.group(2)
                alt_models.setdefault(key, []).append(value)
                continue

            m = re.match(r'group:setMultiItem\("([^"]+)",\s*(true|false)\)', line)
            if m:
                key, value = m.group(1), m.group(2)
                multi_items[key] = to_bool(value)
                continue

            m = re.match(r'group:getLocation\("([^"]+)"\):addAlias\("([^"]+)"\)', line)
            if m:
                key, value = m.group(1), m.group(2)
                aliases.setdefault(key, []).append(value)
                continue

        cls._raw_data = {
            group_name: {
                "Location": locations,
                "Exclusive": exclusives,
                "HideModel": hide_models,
                "AltModel": alt_models,
                "Alias": aliases,
                "MultiItem": multi_items,
            }
        }

    @classmethod
    def _parse_items(cls) -> dict:
        from scripts.parser import script_parser

        item_data = script_parser.extract_script_data("item")
        location_items = {}

        for item_id, data in item_data.items():
            for key in ("CanBeEquipped", "BodyLocation"):
                loc = data.get(key)
                if loc:
                    if isinstance(loc, list):
                        for l in loc:
                            location_items.setdefault(l, []).append(item_id)
                    else:
                        location_items.setdefault(loc, []).append(item_id)

        cls._items = location_items

    @classmethod
    def _rearrange_data(cls) -> dict:
        if cls._raw_data is None:
            cls._load_data()

        rearranged = {}

        for group, group_data in cls._raw_data.items():
            locations = group_data.get("Location", [])
            for loc_id in locations:
                if loc_id not in rearranged:
                    rearranged[loc_id] = {
                        "Group": group,
                        "Exclusive": [],
                        "HideModel": [],
                        "AltModel": [],
                        "Alias": [],
                        "MultiItem": False,
                        "Items": []  # <-- Add this
                    }

                if loc_id in group_data.get("Exclusive", {}):
                    rearranged[loc_id]["Exclusive"].extend(group_data["Exclusive"][loc_id])
                if loc_id in group_data.get("HideModel", {}):
                    rearranged[loc_id]["HideModel"].extend(group_data["HideModel"][loc_id])
                if loc_id in group_data.get("AltModel", {}):
                    rearranged[loc_id]["AltModel"].extend(group_data["AltModel"][loc_id])
                if loc_id in group_data.get("Alias", {}):
                    rearranged[loc_id]["Alias"].extend(group_data["Alias"][loc_id])
                if loc_id in group_data.get("MultiItem", {}):
                    rearranged[loc_id]["MultiItem"] = group_data["MultiItem"][loc_id]

                if cls._items and loc_id in cls._items:
                    rearranged[loc_id]["Items"].extend(cls._items[loc_id])

        cls._all_data = rearranged
        save_cache(cls._all_data, "body_locations_data.json")

    @classmethod
    def all(cls) -> dict:
        if cls._all_data is None:
            cls._load_data()
        return cls._all_data
    
    ## --------------- Object Methods --------------- ##

    ## --------------- Initialise Methods --------------- ##
    
    def __new__(cls, location_id: str):
        if cls._all_data is None:
            cls._rearrange_data()

        if location_id in cls._instances:
            return cls._instances[location_id]

        instance = super().__new__(cls)
        cls._instances[location_id] = instance
        return instance

    def __init__(self, location_id: str):
        if hasattr(self, "location_id"):
            return

        self.location_id: str = location_id
        self.name: str = self.location_id
        self.data: dict = self._all_data.get(location_id, {})

    def __repr__(self) -> str:
        return f"<BodyLocation '{self.location_id}'>"
    
    ## --------------- Object Properties --------------- ##

    @property
    def group(self) -> str:
        return self.data.get("Group", "")

    @property
    def alias(self) -> list[str]:
        return self.data.get("Alias", [])

    @property
    def multi_item(self) -> bool:
        return self.data.get("MultiItem", False)

    @property
    def exclusive(self) -> list["BodyLocation"]:
        return [BodyLocation(x) for x in self.data.get("Exclusive", [])]

    @property
    def hide_model(self) -> list["BodyLocation"]:
        return [BodyLocation(x) for x in self.data.get("HideModel", [])]

    @property
    def alt_model(self) -> list["BodyLocation"]:
        return [BodyLocation(x) for x in self.data.get("AltModel", [])]
    
    @property
    def items(self) -> list[str]:
        return self.data.get("Items", [])


class BodyPart:
    """Static reference for body part display names."""
    _display_names = {
        "Hand_L": "IGUI_health_Left_Hand",
        "Hand_R": "IGUI_health_Right_Hand",
        "ForeArm_L": "IGUI_health_Left_Forearm",
        "ForeArm_R": "IGUI_health_Right_Forearm",
        "UpperArm_L": "IGUI_health_Left_Upper_Arm",
        "UpperArm_R": "IGUI_health_Right_Upper_Arm",
        "Torso_Upper": "IGUI_health_Upper_Torso",
        "Torso_Lower": "IGUI_health_Lower_Torso",
        "Head": "IGUI_health_Head",
        "Neck": "IGUI_health_Neck",
        "Groin": "IGUI_health_Groin",
        "UpperLeg_L": "IGUI_health_Left_Thigh",
        "UpperLeg_R": "IGUI_health_Right_Thigh",
        "LowerLeg_L": "IGUI_health_Left_Shin",
        "LowerLeg_R": "IGUI_health_Right_Shin",
        "Foot_L": "IGUI_health_Left_Foot",
        "Foot_R": "IGUI_health_Right_Foot",
        "Back": "IGUI_health_Back",
    }

    _instances: dict[str, "BodyPart"] = {}

    def __new__(cls, body_part_id: str):
        if body_part_id in cls._instances:
            return cls._instances[body_part_id]
        
        if body_part_id not in cls._display_names:
            raise ValueError(f"Unknown BodyPart: {body_part_id}")
        
        instance = super().__new__(cls)
        cls._instances[body_part_id] = instance
        return instance

    def __init__(self, body_part: str):
        self.body_part_id = body_part

    def __str__(self):
        return self.body_part_id

    def __repr__(self):
        return f"<BodyPart {self.name}>"

    @property
    def display_name(self) -> str:
        return self._display_names[self.body_part_id]
    @property
    def name(self) -> str:
        if not hasattr(self, "_name"):
            self._name = Translate.get(self.display_name)
        return self._name
    @property
    def name_en(self) -> str:
        if not hasattr(self, "_name"):
            self._name_en = Translate.get(self.display_name, lang_code="en")
        return self._name_en
    @property
    def wiki_link(self) -> str:
        if not hasattr(self, "_wiki_link"):
            self._wiki_link = f"[[BloodLocation{Language.get_subpage()}#{self.name_en}|{self.name}]]"
        return self._wiki_link

class BodyPartList:
    """
    Helper class that wraps a list of BodyPart objects with additional properties for convenience.
    Supports iteration and indexing.
    """
    def __init__(self, body_parts: list[BodyPart]):
        """
        Args:
            body_parts (list[BodyPart]): A list of BodyPart objects.
        """
        self._body_parts = body_parts

    def __iter__(self):
        """Returns an iterator over the body parts."""
        return iter(self._body_parts)

    def __getitem__(self, index):
        """Returns the body part at the given index."""
        return self._body_parts[index]

    def __len__(self):
        """Returns the number of body parts."""
        return len(self._body_parts)

    def __repr__(self):
        """Returns a debug representation of the body part list."""
        return repr(self._body_parts)
    
    @property
    def body_part_ids(self) -> list[str]:
        """Returns the internal names of each body part."""
        return [bp.body_part_id for bp in self._body_parts]

    @property
    def names(self) -> list[str]:
        """Returns the translated names of each body part."""
        return [bp.name for bp in self._body_parts]

    @property
    def wiki_links(self) -> list[str]:
        """Returns the internal names of each body part."""
        return [bp.wiki_link for bp in self._body_parts]

    @property
    def display_names(self) -> list[str]:
        """Returns the display name keys of each body part."""
        return [bp.display_name for bp in self._body_parts]

class BloodLocation:
    """Maps a named blood location to a set of body parts."""
    _blood_locations = {
        "Apron": ["Torso_Upper", "Torso_Lower", "UpperLeg_L", "UpperLeg_R"],
        "ShirtNoSleeves": ["Torso_Upper", "Torso_Lower", "Back"],
        "JumperNoSleeves": ["Torso_Upper", "Torso_Lower", "Back"],
        "Shirt": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R"],
        "ShirtLongSleeves": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R"],
        "Jumper": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R"],
        "Jacket": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R", "Neck"],
        "LongJacket": ["Torso_Upper", "Torso_Lower", "Back", "UpperArm_L", "UpperArm_R", "ForeArm_L", "ForeArm_R", "Neck", "Groin", "UpperLeg_L", "UpperLeg_R"],
        "ShortsShort": ["Groin", "UpperLeg_L", "UpperLeg_R"],
        "Trousers": ["Groin", "UpperLeg_L", "UpperLeg_R", "LowerLeg_L", "LowerLeg_R"],
        "Shoes": ["Foot_L", "Foot_R"],
        "FullHelmet": ["Head"],
        "Bag": ["Back"],
        "Hands": ["Hand_L", "Hand_R"],
        "Head": ["Head"],
        "Neck": ["Neck"],
        "Groin": ["Groin"],
        "UpperBody": ["Torso_Upper"],
        "LowerBody": ["Torso_Lower"],
        "LowerLegs": ["LowerLeg_L", "LowerLeg_R"],
        "UpperLegs": ["UpperLeg_L", "UpperLeg_R"],
        "LowerArms": ["ForeArm_L", "ForeArm_R"],
        "UpperArms": ["UpperArm_L", "UpperArm_R"],
        "Hand_L": ["Hand_L"],
        "Hand_R": ["Hand_R"],
        "ForeArm_L": ["ForeArm_L"],
        "ForeArm_R": ["ForeArm_R"],
        "UpperArm_L": ["UpperArm_L"],
        "UpperArm_R": ["UpperArm_R"],
        "UpperLeg_L": ["UpperLeg_L"],
        "UpperLeg_R": ["UpperLeg_R"],
        "LowerLeg_L": ["LowerLeg_L"],
        "LowerLeg_R": ["LowerLeg_R"],
        "Foot_L": ["Foot_L"],
        "Foot_R": ["Foot_R"],
    }

    _instances: dict[str, "BloodLocation"] = {}

    def __new__(cls, blood_location: str):
        if blood_location in cls._instances:
            return cls._instances[blood_location]
        
        if blood_location not in cls._blood_locations:
            raise ValueError(f"Unknown BloodLocation: {blood_location}")
        
        instance = super().__new__(cls)
        cls._instances[blood_location] = instance
        return instance

    def __init__(self, blood_location: str):
        self.blood_location = blood_location
        self._body_parts = [BodyPart(bp) for bp in self._blood_locations[blood_location]]

    def __str__(self):
        return self.blood_location

    def __repr__(self):
        return f"<BloodLocation {self.blood_location}>"

    @property
    def body_parts(self) -> BodyPartList:
        """Returns a list-like wrapper of BodyPart instances for this blood location."""
        return BodyPartList(self._body_parts)
    

class BloodLocationList:
    """
    Helper class that wraps a list of BloodLocation objects with additional properties for convenience.
    Supports iteration and indexing.
    """
    def __init__(self, locations: list[BloodLocation]):
        """
        Args:
            locations (list[BloodLocation]): A list of BloodLocation objects.
        """
        self._locations = locations

    def __iter__(self):
        """Returns an iterator over the blood locations."""
        return iter(self._locations)

    def __getitem__(self, index):
        """Returns the blood location at the given index."""
        return self._locations[index]

    def __len__(self):
        """Returns the number of blood locations."""
        return len(self._locations)

    def __repr__(self):
        """Returns a debug representation of the blood location list."""
        return repr(self._locations)

    @property
    def names(self) -> list[str]:
        """Returns the names of all blood locations."""
        return [loc.blood_location for loc in self._locations]

    @property
    def body_parts(self) -> BodyPartList:
        all_parts = [bp for loc in self._locations for bp in loc.body_parts]
        return BodyPartList(all_parts)