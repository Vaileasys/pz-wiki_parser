[Previous Folder](../lists/attachment_list.md) | [Previous File](profession.md) | [Next File](trap.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# skill.py

This module contains classes for handling skills and skill books in Project Zomboid.

Skill data is loaded from `skills.json`, based on values from the game's Java class `PerkFactory.init()`.
Skill book data is parsed from `XPSystem_SkillBook.lua`.

## Classes

### `Skill`

Represents a game skill (perk), including XP thresholds and translation data.

#### Class Methods
##### [`_load_skills()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L71)

Load skill data from skills.json.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L76)

Return all skills as a dictionary of Skill instances.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L83)

Return all skill keys.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L90)

Yield Skill instances for all skills.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L97)

Return the number of defined skills.

#### Object Methods
##### [`__new__(perk_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L24)
##### [`__init__(perk_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L35)
##### [`__getitem__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L54)

Allow dict-like access to raw skill data.

##### [`__contains__(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L58)

Check if a key exists in the raw skill data.

##### [`__bool__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L62)

Return True if the skill has valid data.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L66)

Return a string representation of the skill.

##### [`get(key: str, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L103)

Return a value from the raw data with an optional default.

##### [`get_xp(level: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L107)

Return the XP required to reach the given level.


### `SkillBook`

Represents a skill book with XP multipliers for specific levels.

#### Class Methods
##### [`_load_books()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L152)

Parse SkillBook data from XPSystem_SkillBook.lua.

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L163)

Return all skill books as a dictionary of SkillBook instances.

#### Object Methods
##### [`__new__(name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L121)
##### [`_init(skill_book: str, data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L134)
##### [`__bool__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L143)

Return True if the book has a valid associated skill.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L147)

Return a string representation of the skill book.

##### [`get_multiplier(level: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L169)

Return the XP multiplier for a given skill level.

#### Properties
##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L186)

Localised name of the associated skill.

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L191)

English name of the associated skill.

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/skill.py#L196)

Wiki link for the associated skill.



[Previous Folder](../lists/attachment_list.md) | [Previous File](profession.md) | [Next File](trap.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
