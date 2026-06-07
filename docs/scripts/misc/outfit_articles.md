[Previous Folder](../lists/attachment_list.md) | [Previous File](item_merger.md) | [Next File](room_define.md) | [Next Folder](../navbox/navbox.md) | [Back to Index](../../index.md)

# outfit_articles.py

Generates wiki-formatted outfit article output.

Builds outfit pages from Outfit data, including infoboxes, overviews, item tables, 
code sections, and navigation. Story and zone spawn data are pulled from
OutfitStory and OutfitZone, while list output is handled separately.

## Functions

### [`_build_clothing_name_mapping()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L38)

Build a reverse mapping from clothing item names to game item IDs.
This uses cached item data (not reparsing) and caches the mapping itself.

For example: "Belt" -> "Base.Belt2", "Bag_HikingBag" -> "Base.Bag_HikingBag"

<ins>**Returns:**</ins>
  - **dict**:
      - _Mapping of clothing item name to game item ID_

### [`format_display_name(story_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L72)

Format a story ID for display by removing prefix and converting camel case to spaced words

<ins>**Args:**</ins>
  - **story_id (str)**:
      - _The story ID (e.g., "RBBurntFireman")_

<ins>**Returns:**</ins>
  - **str**:
      - _Formatted display name (e.g., "Burnt Fireman")_

### [`format_story_link(story_type, story_id)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L97)

Format a story link based on the story type

<ins>**Args:**</ins>
  - **story_type (str)**:
      - _The type of story (e.g., "random_building", "random_vehicle")_
  - **story_id (str)**:
      - _The story ID (e.g., "RBBurntFireman")_

<ins>**Returns:**</ins>
  - **str**:
      - _Formatted wiki link_

### [`process_stories(outfit_id: str) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L124)

Process story-related spawn locations for the outfit

<ins>**Args:**</ins>
  - **outfit_id (str)**:
      - _The outfit ID_

<ins>**Returns:**</ins>
  - **str**:
      - _Story-related spawn information_

### [`process_zones(outfit_id: str) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L160)

Process zone-related spawn locations for the outfit

<ins>**Args:**</ins>
  - **outfit_id (str)**:
      - _The outfit ID_

<ins>**Returns:**</ins>
  - **list[str]**:
      - _Zone-related spawn information_

### [`create_header()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L217)

Create the header section of the article

### [`create_infobox(outfit: Outfit)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L226)

Create the infobox section for a specific outfit

<ins>**Args:**</ins>
  - **outfit (Outfit)**:
      - _The outfit object_

<ins>**Returns:**</ins>
  - **str**:
      - _Complete infobox template_

### [`create_intro(outfit: Outfit)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L283)

Create the introduction section of the article

<ins>**Args:**</ins>
  - **outfit (Outfit)**:
      - _The outfit object_

<ins>**Returns:**</ins>
  - **str**:
      - _Complete introduction section_

### [`create_overview(outfit: Outfit) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L303)

Create the overview section of the article

<ins>**Args:**</ins>
  - **outfit (Outfit)**:
      - _The outfit object_

<ins>**Returns:**</ins>
  - **dict**:
      - _Contains 'content' (for article) and 'bot_flagged' (for individual files)_

### [`create_items(outfit: Outfit, clothing_to_item_mapping: dict) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L343)

Create the items section of the article

<ins>**Args:**</ins>
  - **outfit (Outfit)**:
      - _The outfit object_
  - **clothing_to_item_mapping (dict)**:
      - _Mapping of clothing item names to game item IDs_

<ins>**Returns:**</ins>
  - **dict**:
      - _Contains 'content' (complete items section) and 'tables_data' (individual table data)_

### [`create_items_table(outfit: Outfit, items_dict: dict, guid: str, sex_label: str, clothing_to_item_mapping: dict) -> dict[str, list[str]] | None`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L416)

Create a wikitable for items with sub-items support

<ins>**Returns:**</ins>
  - **dict**:
      - _Contains 'table_only' (just the bot-flagged table) and_
  - **'full_section' (header + table for article)**:

### [`create_code(outfit: Outfit)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L553)

Create the code section with outfit data

<ins>**Args:**</ins>
  - **outfit (Outfit)**:
      - _The outfit object_

<ins>**Returns:**</ins>
  - **str**:
      - _Complete code section_

### [`create_navigation(sex_type: str) -> list[str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L612)

Create the navigation section of the article

### [`build_article(outfit: Outfit, clothing_to_item_mapping: dict) -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L635)

Build a complete article for a specific outfit

<ins>**Args:**</ins>
  - **outfit (Outfit)**:
      - _The outfit object_
  - **clothing_to_item_mapping (dict)**:
      - _Mapping of clothing item names to game item IDs_

<ins>**Returns:**</ins>
  - **dict**:
      - _Dictionary containing all sections and the complete article_

### [`write_article_files(article_data: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L700)

### [`create_articles()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L736)

Create outfit articles using nested functions to build each section

### [`run_decompiler()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L776)

Ensure the ZomboidDecompiler has been run.
If not, run it now.

<ins>**Returns:**</ins>
  - **bool**:
      - _True if decompiler output exists or was successfully created, False otherwise_

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/misc/outfit_articles.py#L827)


[Previous Folder](../lists/attachment_list.md) | [Previous File](item_merger.md) | [Next File](room_define.md) | [Next Folder](../navbox/navbox.md) | [Back to Index](../../index.md)
