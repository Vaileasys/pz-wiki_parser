[Previous Folder](../navbox/navbox.md) | [Previous File](item.md) | [Next File](outfit_story.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# outfit.py

Provides cached access to parsed Project Zomboid outfit data.

The Outfit class wraps male/female outfit definitions, resolves wiki page names,
and exposes common outfit properties such as GUIDs, item lists, sex availability,
and navbox grouping.

## Classes

### `Outfit`

Represents a single outfit definition from the parsed outfit cache.

#### Class Methods

##### [`load(force: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L52)

Load outfit data from cache, regenerating if outdated.

<ins>**Args:**</ins>
  - **force**:
      - _Reload data even if already loaded._

##### [`load_pages(force: bool = False)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L80)

Load flattened page data used for outfit page lookup.

<ins>**Args:**</ins>
  - **force**:
      - _Reload page data even if already loaded._

##### [`all() -> dict[str, 'Outfit']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L95)

Return all outfits keyed by outfit ID.

##### [`values()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L110)

Return all outfit instances.

##### [`keys()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L115)

Return all outfit IDs.

#### Object Methods

##### [`__new__(outfit_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L22)

Create or reuse an Outfit instance.

<ins>**Args:**</ins>
  - **outfit_id**:
      - _Outfit ID._

##### [`__init__(outfit_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L39)

Initialise the outfit instance.

<ins>**Args:**</ins>
  - **outfit_id**:
      - _Outfit ID._

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L229)

Return debug representation.

#### Properties

##### [`outfit_id`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L120)

Outfit ID.

##### [`male_data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L125)

Male outfit data.

##### [`female_data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L130)

Female outfit data.

##### [`has_male`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L135)

Whether the outfit has a male definition.

##### [`has_female`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L140)

Whether the outfit has a female definition.

##### [`sex`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L145)

Sex availability: Both, Male, Female, or blank.

##### [`navbox_section`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L159)

Navbox section name for this outfit.

##### [`page`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L173)

Wiki page name for this outfit, falling back to outfit ID.

##### [`guids`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L192)

All GUIDs for this outfit.

##### [`male_guid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L205)

Male outfit GUID.

##### [`female_guid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L210)

Female outfit GUID.

##### [`male_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L215)

Items used by the male outfit definition.

##### [`female_items`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L220)

Items used by the female outfit definition.

##### [`valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/outfit.py#L225)

Whether the outfit has male or female data.


[Previous Folder](../navbox/navbox.md) | [Previous File](item.md) | [Next File](outfit_story.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
