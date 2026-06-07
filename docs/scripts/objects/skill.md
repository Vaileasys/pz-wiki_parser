[Previous Folder](../navbox/navbox.md) | [Previous File](recorded_media.md) | [Next File](trap.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# skill.py

This module contains classes for handling skills and skill books in Project Zomboid.

Skill data is loaded from `skills.json`, based on values from the game's Java class `PerkFactory.init()`.
Skill book data is parsed from `XPSystem_SkillBook.lua`.

## Classes

### `Skill`

Represents a game skill (perk), including XP thresholds and translation data.

#### Class Methods

##### [`_load_skills()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L69)

Load skill data from skills.json.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L74)

Return all skills as a dictionary of Skill instances.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L81)

Return all skill keys.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L88)

Yield Skill instances for all skills.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L95)

Return the number of defined skills.

#### Object Methods

##### [`__new__(perk_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L24)

##### [`__init__(perk_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L35)

##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L52)

Allow dict-like access to raw skill data.

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L56)

Check if a key exists in the raw skill data.

##### [`__bool__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L60)

Return True if the skill has valid data.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L64)

Return a string representation of the skill.

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L101)

Return a value from the raw data with an optional default.

##### [`get_xp(level: int) -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L105)

Return the XP required to reach the given level.

#### Properties

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L112)

Localised name of the skill.

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L123)

English name of the skill.

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L133)

Page name for the skill.

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L140)

Wiki link for the skill.

### `SkillBook`

Represents a skill book with XP multipliers for specific levels.

#### Class Methods

##### [`_load_books()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L186)

Parse SkillBook data from XPSystem_SkillBook.lua.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L197)

Return all skill books as a dictionary of SkillBook instances.

#### Object Methods

##### [`__new__(name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L155)

##### [`_init(skill_book: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L168)

##### [`__bool__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L177)

Return True if the book has a valid associated skill.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L181)

Return a string representation of the skill book.

##### [`get_multiplier(level: int) -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L203)

Return the XP multiplier for a given skill level.

#### Properties

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L220)

Localised name of the associated skill.

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L225)

English name of the associated skill.

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L230)

Wiki link for the associated skill.


[Previous Folder](../navbox/navbox.md) | [Previous File](recorded_media.md) | [Next File](trap.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
