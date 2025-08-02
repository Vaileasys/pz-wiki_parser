"""
This module contains classes for handling skills and skill books in Project Zomboid.

Skill data is loaded from `skills.json`, based on values from the game's Java class `PerkFactory.init()`.
Skill book data is parsed from `XPSystem_SkillBook.lua`.
"""
import os
from scripts.core.constants import RESOURCE_DIR
from scripts.core.language import Translate
from scripts.core import file_loading
from scripts.utils.util import link
from scripts.utils.lua_helper import load_lua_file, parse_lua_tables
from scripts.utils import echo

PERK_XP_REQ_MULTIPLIER = 1.5

class Skill:
    """
    Represents a game skill (perk), including XP thresholds and translation data.
    """
    _skills = None
    _instances = {}

    def __new__(cls, perk_id: str):
        if cls._skills is None:
            cls._load_skills()

        if perk_id in cls._instances:
            return cls._instances[perk_id]

        instance = super().__new__(cls)
        cls._instances[perk_id] = instance
        return instance

    def __init__(self, perk_id: str):
        if hasattr(self, "perk_id"):
            return

        if Skill._skills is None:
            Skill._load_skills()

        self.perk_id = perk_id
        self.data: dict = Skill._skills.get(perk_id, {})

        self.translation = self.data.get("translation", "")
        self.parent = self.data.get("parent")
        self.passive = self.data.get("passive", False)
        self.xp = [int(val * PERK_XP_REQ_MULTIPLIER) for val in self.data.get("xp", [])]
        self.name = Translate.get(f"IGUI_perks_{self.translation}")
        self.name_en = Translate.get(f"IGUI_perks_{self.translation}", lang_code="en")
        self.page = self.data.get("page", self.name_en)
        self.wiki_link = link(self.page, self.name)

    def __getitem__(self, key):
        """Allow dict-like access to raw skill data."""
        return self.data[key]

    def __contains__(self, key):
        """Check if a key exists in the raw skill data."""
        return key in self.data
    
    def __bool__(self):
        """Return True if the skill has valid data."""
        return bool(self.data)

    def __repr__(self):
        """Return a string representation of the skill."""
        return f"<Skill: {self.perk_id}>"

    @classmethod
    def _load_skills(cls):
        """Load skill data from skills.json."""
        cls._skills = file_loading.load_json(os.path.join(RESOURCE_DIR, "skills.json"))

    @classmethod
    def all(cls):
        """Return all skills as a dictionary of Skill instances."""
        if cls._skills is None:
            cls._load_skills()
        return {perk_id: cls(perk_id) for perk_id in cls._skills}

    @classmethod
    def keys(cls):
        """Return all skill keys."""
        if cls._skills is None:
            cls._load_skills()
        return cls._skills.keys()

    @classmethod
    def values(cls):
        """Yield Skill instances for all skills."""
        if cls._skills is None:
            cls._load_skills()
        return (cls(perk_id) for perk_id in cls._skills)

    @classmethod
    def count(cls):
        """Return the number of defined skills."""
        if cls._skills is None:
            cls._load_skills()
        return len(cls._skills)
    
    def get(self, key: str, default=None):
        """Return a value from the raw data with an optional default."""
        return self.data.get(key, default)
    
    def get_xp(self, level: int) -> int:
        """Return the XP required to reach the given level."""
        if not self.xp or level < 1 or level > len(self.xp):
            return 0
        return self.xp[level - 1]


class SkillBook:
    """
    Represents a skill book with XP multipliers for specific levels.
    """
    _books = None
    _instances = {}

    def __new__(cls, name: str):
        if cls._books is None:
            cls._load_books()

        if name in cls._instances:
            return cls._instances[name]

        data = cls._books.get(name)
        instance = super().__new__(cls)
        cls._instances[name] = instance
        instance._init(name, data)
        return instance

    def _init(self, skill_book: str, data: dict):
        self.skill_book = skill_book
        self.perk = data.get("perk") if data else None
        self.skill = Skill(self.perk) if self.perk else None
        self.multipliers = {
            level: data.get(f"maxMultiplier{level}", 1)
            for level in range(1, 6)
        } if data else {}

    def __bool__(self):
        """Return True if the book has a valid associated skill."""
        return bool(self.skill)

    def __repr__(self):
        """Return a string representation of the skill book."""
        return f"<SkillBook: {self.skill_book} → {self.perk}>"

    @classmethod
    def _load_books(cls):
        """Parse SkillBook data from XPSystem_SkillBook.lua."""
        runtime = load_lua_file("XPSystem_SkillBook.lua", inject_lua="""
            Perks = setmetatable({}, {
                __index = function(_, k) return tostring(k) end
            })
        """)
        parsed = parse_lua_tables(runtime, tables=["SkillBook"])
        cls._books = parsed.get("SkillBook", {})

    @classmethod
    def all(cls):
        """Return all skill books as a dictionary of SkillBook instances."""
        if cls._books is None:
            cls._load_books()
        return {name: cls(name) for name in cls._books}

    def get_multiplier(self, level: int) -> float:
        """Return the XP multiplier for a given skill level."""
        if level == 1:
            return self.multipliers.get(1, 1)
        elif level == 3:
            return self.multipliers.get(2, 1)
        elif level == 5:
            return self.multipliers.get(3, 1)
        elif level == 7:
            return self.multipliers.get(4, 1)
        elif level == 9:
            return self.multipliers.get(5, 1)
        else:
            echo.warning(f"Unhandled skill level {level} for skill book '{self.skill_book}'")
            return 1

    @property
    def name(self):
        """Localised name of the associated skill."""
        return self.skill.name if self.skill else self.skill_book

    @property
    def name_en(self):
        """English name of the associated skill."""
        return self.skill.name_en if self.skill else self.skill_book

    @property
    def wiki_link(self):
        """Wiki link for the associated skill."""
        return self.skill.wiki_link if self.skill else None