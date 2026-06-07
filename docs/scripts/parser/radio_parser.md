[Previous Folder](../objects/animal.md) | [Previous File](outfit_zone_parser.md) | [Next File](recipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# radio_parser.py

## Functions

### [`timestamp_to_datetime(timestamp: Union[int, str]) -> Tuple[str, str]`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L48)

Convert a timestamp to time and date strings.

<ins>**Args:**</ins>
  - **timestamp (int or str)**:
      - _The timestamp in minutes since EPOCH._

<ins>**Returns:**</ins>
  - **Tuple[str, str]**:
      - _A tuple containing the time in 24-hour format and date in ISO format._

### [`replace_cat(cat: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L65)

Replace category with its replacement if available.

<ins>**Args:**</ins>
  - **cat (str)**:
      - _The category to replace._

<ins>**Returns:**</ins>
  - **str**:
      - _The replaced category._

### [`replace_codes(code_part: str) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L77)

Replace code part with its replacement if available.

<ins>**Args:**</ins>
  - **code_part (str)**:
      - _The code part to replace._

<ins>**Returns:**</ins>
  - **str**:
      - _The replaced code part._

### [`get_person(color: dict, person_map: dict) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L89)

Get person identifier based on color.

<ins>**Args:**</ins>
  - **color (dict)**:
      - _A dictionary with 'r', 'g', 'b' keys._
  - **person_map (dict)**:
      - _A mapping of color keys to person identifiers._

<ins>**Returns:**</ins>
  - **str**:
      - _The person identifier._

### [`get_channel_cat(channel_entry: Union[ET.Element, None]) -> str`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L107)

Get channel category from channel entry.

<ins>**Args:**</ins>
  - **channel_entry (ET.Element or None)**:
      - _The channel entry element._

<ins>**Returns:**</ins>
  - **str**:
      - _The channel category._

### [`process_broadcast_entries(entries: List[ET.Element], output_file, channel_entry: Union[ET.Element, None], log_file, broadcast_entry_count: int) -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L125)

Process broadcast entries and write to output file.

<ins>**Args:**</ins>
  - **entries (List[ET.Element])**:
      - _List of broadcast entries._
  - **output_file (file object)**:
      - _The output file to write to._
  - **channel_entry (ET.Element or None)**:
      - _The channel entry._
  - **log_file (file object)**:
      - _The log file to write to._
  - **broadcast_entry_count (int)**:
      - _The current broadcast entry count._

<ins>**Returns:**</ins>
  - **int**:
      - _The updated broadcast entry count._

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L210)

Main function to process the RadioData.xml and generate output.


[Previous Folder](../objects/animal.md) | [Previous File](outfit_zone_parser.md) | [Next File](recipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
