[Previous Folder](../navbox/navbox.md) | [Previous File](outfit_zone.md) | [Next File](recorded_media.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# profession.py

## Functions

### [`parse_main_creation_methods(func: str, expression: str = None, name: str = None, suppress: bool = False) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L10)

## Classes

### `Occupation`

#### Class Methods

##### [`_parse() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L54)

##### [`load() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L60)

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L76)

Return all occupations as a dictionary of Occupation instances.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L83)

Return all occupation keys.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L90)

Yield Occupation instances for all occupations.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L97)

Return the number of defined occupations.

##### [`exists(trait: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L104)

#### Object Methods

##### [`__new__(occupation: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L44)

##### [`__init__(occupation: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L49)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L107)

##### [`__repr__() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L173)

#### Properties

##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L111)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L115)

##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L119)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L123)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L129)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L135)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L139)

##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L143)

##### [`cost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L154)

##### [`is_free`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L158)

##### [`free_traits`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L162)

##### [`xp_boosts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L166)

##### [`recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L170)

### `Trait`

#### Class Methods

##### [`_parse() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L192)

##### [`load() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L198)

##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L214)

Return all traits as a dictionary of Trait instances.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L221)

Return all trait keys.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L228)

Yield Trait instances for all traits.

##### [`count()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L235)

Return the number of defined traits.

##### [`exists(trait: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L242)

#### Object Methods

##### [`__new__(trait: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L182)

##### [`__init__(trait: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L187)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L245)

##### [`__repr__() -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L310)

#### Properties

##### [`id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L249)

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L253)

##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L257)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L261)

##### [`name_en`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L265)

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L271)

##### [`wiki_link`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L275)

##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L279)

##### [`desc`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L287)

##### [`cost`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L291)

##### [`is_free`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L295)

##### [`free_traits`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L299)

##### [`xp_boosts`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L303)

##### [`recipes`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/profession.py#L307)


[Previous Folder](../navbox/navbox.md) | [Previous File](outfit_zone.md) | [Next File](recorded_media.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
