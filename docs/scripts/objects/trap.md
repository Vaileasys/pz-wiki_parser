[Previous Folder](../lists/attachment_list.md) | [Previous File](skill.md) | [Next File](vehicle.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# trap.py

## Classes

### `Trap`

Subclass of Item for traps. Adds trap-specific data from TrapDefinition.lua.

#### Class Methods
##### [`_load_trap_definitions()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L15)
##### [`from_item(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L42)
#### Object Methods
##### [`__init__(item: Item)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L46)
##### [`__getattr__(name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L50)
##### [`get_sprite(sprite, dim)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L53)
#### Properties
##### [`trap_strength`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L62)
##### [`destroy_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L66)
##### [`sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L71)
##### [`closed_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L75)
##### [`north_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L79)
##### [`north_closed_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L83)
##### [`trap_data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L87)
##### [`animals`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L91)
##### [`animal_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L99)
##### [`animal_chances`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L103)

### `TrapAnimal`
#### Class Methods
##### [`_load_animal_definitions()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L115)
##### [`all()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L142)
#### Object Methods
##### [`__init__(animal_type: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L148)
#### Properties
##### [`animal_data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L153)
##### [`type`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L157)
##### [`item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L161)
##### [`traps`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L165)
##### [`baits`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L169)
##### [`zone`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L173)
##### [`min_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L177)
##### [`max_size`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L181)
##### [`min_hour`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L185)
##### [`max_hour`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L189)
##### [`can_be_alive`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L193)
##### [`alive_animals`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L197)
##### [`alive_breed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L201)
##### [`strength`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/trap.py#L205)


[Previous Folder](../lists/attachment_list.md) | [Previous File](skill.md) | [Next File](vehicle.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
