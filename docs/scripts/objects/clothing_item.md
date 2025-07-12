[Previous Folder](../lists/attachment_list.md) | [Previous File](body_location.md) | [Next File](components.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# clothing_item.py

## Classes

### `ClothingDecal`

Represents a single clothing decal, loaded from an XML file.

Includes texture path and placement coordinates.

#### Object Methods
##### [`__new__(decal_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L14)
##### [`__init__(decal_name: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L21)

Args:

decal_name (str): The name of the decal (XML filename without extension).

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L42)
##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L45)
##### [`_parse_decal(path: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L48)

### `ClothingItem`

Represents a clothing item, parsed from XML.

Includes model references, decal group, and texture options.

#### Class Methods
##### [`_load_decal_groups()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L120)

Loads and caches decal group mappings from clothingDecals.xml.

Populates `_decal_group_map` with group name -> decal name list.

#### Object Methods
##### [`__new__(clothing_item: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L70)
##### [`__init__(clothing_item: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L77)

Args:

clothing_item (str): The item ID to load (e.g., 'Tshirt_SpiffoDECAL').

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L111)

Returns a debug representation of the clothing item.

##### [`__str__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L115)

Returns the `ClothingItem` value as a string.

##### [`parse_clothing_xml()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L144)

Parses the XML file for the clothing item and sets all attributes.

Handles decal group loading and decal object creation if applicable.


### `DecalList`

Helper class that wraps a list of ClothingDecal objects with additional properties for convenience.

Supports iteration and indexing.

#### Object Methods
##### [`__init__(decals: list[ClothingDecal])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L199)

Args:

decals (list[ClothingDecal]): A list of ClothingDecal objects.

##### [`__iter__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L206)

Returns an iterator over the decal list.

##### [`__getitem__(index)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L210)

Returns the decal at the given index.

##### [`__len__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L214)

Returns the number of decals in the list.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L218)

Returns a debug representation of the decal list.

#### Properties
##### [`names`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L223)
##### [`textures`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L227)
##### [`coords`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L231)
##### [`dimensions`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/clothing_item.py#L235)


[Previous Folder](../lists/attachment_list.md) | [Previous File](body_location.md) | [Next File](components.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
