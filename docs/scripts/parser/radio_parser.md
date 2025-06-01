[Previous Folder](../objects/components.md) | [Previous File](outfit_parser.md) | [Next File](recipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)

# radio_parser.py

## Functions

### [`timestamp_to_datetime(timestamp: Union[int, str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L41)

_Convert a timestamp to time and date strings._

<ins>**Args:**</ins>
  - **timestamp (int or str)**:
      - _The timestamp in minutes since EPOCH._

<ins>**Returns:**</ins>
  - **Tuple[str, str]:**
      - A tuple containing the time in 24-hour format and date in ISO format.
### [`replace_cat(cat: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L58)

_Replace category with its replacement if available._

<ins>**Args:**</ins>
  - **cat (str)**:
      - _The category to replace._

<ins>**Returns:**</ins>
  - **str:**
      - The replaced category.
### [`replace_codes(code_part: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L70)

_Replace code part with its replacement if available._

<ins>**Args:**</ins>
  - **code_part (str)**:
      - _The code part to replace._

<ins>**Returns:**</ins>
  - **str:**
      - The replaced code part.
### [`get_person(color: dict, person_map: dict)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L82)

_Get person identifier based on color._

<ins>**Args:**</ins>
  - **color (dict)**:
      - _A dictionary with 'r', 'g', 'b' keys._
  - **person_map (dict)**:
      - _A mapping of color keys to person identifiers._

<ins>**Returns:**</ins>
  - **str:**
      - The person identifier.
### [`get_channel_cat(channel_entry: Union[ET.Element, None])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L100)

_Get channel category from channel entry._

<ins>**Args:**</ins>

<ins>**Returns:**</ins>
  - **str:**
      - The channel category.
### [`process_broadcast_entries(entries: List[ET.Element], output_file, channel_entry: Union[ET.Element, None], log_file, broadcast_entry_count: int)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L118)

_Process broadcast entries and write to output file._

<ins>**Args:**</ins>
  - **output_file (file object)**:
      - _The output file to write to._
      - _channel_entry (ET.Element or None): The channel entry._
  - **log_file (file object)**:
      - _The log file to write to._
  - **broadcast_entry_count (int)**:
      - _The current broadcast entry count._

<ins>**Returns:**</ins>
  - **int:**
      - The updated broadcast entry count.
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/parser/radio_parser.py#L203)

_Main function to process the RadioData.xml and generate output._


[Previous Folder](../objects/components.md) | [Previous File](outfit_parser.md) | [Next File](recipe_parser.md) | [Next Folder](../recipes/craft_recipes.md) | [Back to Index](../../index.md)
