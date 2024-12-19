import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Tuple, Union, List

EPOCH = datetime(1993, 7, 9)

CAT_REPLACEMENTS = {
    "Television": "tv",
    "Radio": "radio",
    "Amateur": "radio",
    "Military": "radio",
}

CODES_REPLACEMENTS = {
    "BOR": "Boredom",
    "STS": "Stress",
    "UHP": "Unhappiness",
    "PAN": "Panic",
    "FEA": "Fear",
    "FAT": "Fatigue",
    "COO": "Cooking",
    "CRP": "Carpentry",
    "FIS": "Fishing",
    "FRM": "Farming",
    "FOD": "Foraging",
    "TRA": "Trapping",
    "MEC": "Mechanics",
    "TAI": "Tailoring",
    "MTL": "Metalworking",
    "ELC": "Electrical",
    "DOC": "First Aid",
    "LFT": "Lightfooted",
    "AIM": "Aiming",
    "REL": "Reloading",
    "RCP": "RCP",
}


def timestamp_to_datetime(timestamp: Union[int, str]) -> Tuple[str, str]:
    """Convert a timestamp to time and date strings.

    Args:
        timestamp (int or str): The timestamp in minutes since EPOCH.

    Returns:
        Tuple[str, str]: A tuple containing the time in 24-hour format and date in ISO format.
    """
    timestamp = int(timestamp)
    delta = timedelta(minutes=timestamp)
    new_datetime = EPOCH + delta
    date_iso = new_datetime.date().isoformat()
    time_24hr = new_datetime.strftime("%H:%M")
    return time_24hr, date_iso


def replace_cat(cat: str) -> str:
    """Replace category with its replacement if available.

    Args:
        cat (str): The category to replace.

    Returns:
        str: The replaced category.
    """
    return CAT_REPLACEMENTS.get(cat, cat)


def replace_codes(code_part: str) -> str:
    """Replace code part with its replacement if available.

    Args:
        code_part (str): The code part to replace.

    Returns:
        str: The replaced code part.
    """
    return CODES_REPLACEMENTS.get(code_part, code_part)


def get_person(color: dict, person_map: dict) -> str:
    """Get person identifier based on color.

    Args:
        color (dict): A dictionary with 'r', 'g', 'b' keys.
        person_map (dict): A mapping of color keys to person identifiers.

    Returns:
        str: The person identifier.
    """
    key = tuple(color.values())
    if key in person_map:
        return person_map[key]
    person = f"person{len(person_map) + 1}"
    person_map[key] = person
    return person


def get_channel_cat(channel_entry: Union[ET.Element, None]) -> str:
    """Get channel category from channel entry.

    Args:
        channel_entry (ET.Element or None): The channel entry element.

    Returns:
        str: The channel category.
    """
    if (
        channel_entry is not None
        and 'cat' in channel_entry.attrib
        and channel_entry.get('cat').strip() != ""
    ):
        return channel_entry.get('cat')
    return "Radio"


def process_broadcast_entries(
    entries: List[ET.Element],
    output_file,
    channel_entry: Union[ET.Element, None],
    log_file,
    broadcast_entry_count: int,
) -> int:
    """Process broadcast entries and write to output file.

    Args:
        entries (List[ET.Element]): List of broadcast entries.
        output_file (file object): The output file to write to.
        channel_entry (ET.Element or None): The channel entry.
        log_file (file object): The log file to write to.
        broadcast_entry_count (int): The current broadcast entry count.

    Returns:
        int: The updated broadcast entry count.
    """
    channel_cat = get_channel_cat(channel_entry)
    for broadcast_entry in entries:
        broadcast_entry_count += 1
        icon = replace_cat(channel_cat)
        timestamp = broadcast_entry.get('timestamp')
        endstamp = broadcast_entry.get('endstamp')
        output_file.write(f"{{{{Transcript\n|icon={icon}")
        log_file.write(f'BroadcastEntry: ID="{broadcast_entry.get("ID")}"\n')

        if timestamp is not None:
            time_start, date = timestamp_to_datetime(timestamp)
            output_file.write(
                f"\n|timestamp={timestamp}\n|time_start={time_start}\n|date={date}"
            )

            if endstamp is not None:
                time_end, _ = timestamp_to_datetime(endstamp)
                output_file.write(f"\n|endstamp={endstamp}\n|time_end={time_end}")

        output_file.write("\n|text=")
        prev_person = None
        person_map = {}
        for line_entry in broadcast_entry.findall('.//LineEntry'):
            color = {
                'r': line_entry.get('r'),
                'g': line_entry.get('g'),
                'b': line_entry.get('b'),
            }
            person = get_person(color, person_map)
            value = line_entry.text.strip() if line_entry.text else ""
            value = value.replace('[img=music]', '♪')
            codes = line_entry.get('codes')

            if codes:
                code_parts = []
                for code in codes.split(','):
                    code_part = code[:3]
                    code_value = code[3:] if len(code) > 3 else ""
                    code_part = replace_codes(code_part)
                    code_parts.append(f"{code_part} {{{{mood|{code_value}}}}} ")
                code_str = ", ".join(code_parts)

                if person != prev_person:
                    if prev_person is not None:
                        output_file.write("}}\n")
                    output_file.write(
                        f"{{{{Transcript/row|{person}|"
                        f"{{{{tooltip|{value}|{code_str}}}}}<br>\n"
                    )
                else:
                    output_file.write(f"{{{{tooltip|{value}|{code_str}}}}}<br>\n")
            else:
                if person != prev_person:
                    if prev_person is not None:
                        output_file.write("}}\n")
                    output_file.write(f"{{{{Transcript/row|{person}|{value}<br>\n")
                else:
                    output_file.write(f"{value}<br>\n")
            prev_person = person

        if prev_person is not None:
            output_file.write("}}")
        output_file.write("}}<br>\n\n")
    return broadcast_entry_count


def main():
    """Main function to process the RadioData.xml and generate output."""
    channel_entry_lines = 0
    broadcast_entry_count = 0

    # Hardcoded file path for input and output
    file_path = os.path.join('resources', 'radio', 'RadioData.xml')
    output_dir = os.path.join('output', 'radio')
    output_file_path = os.path.join(output_dir, 'radio_output.txt')

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_dir), exist_ok=True)

    # Extract directory of the script
    logging_dir = os.path.join('output', 'logging')
    logging_file_path = os.path.join(logging_dir, 'radio_log.txt')
    os.makedirs(logging_dir, exist_ok=True)

    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(output_file_path, 'w', encoding='utf-8') as output_file, open(logging_file_path, 'w', encoding='utf-8') as log_file:
        for element in root:
            if element.tag == 'Adverts':
                output_file.write("==Adverts==\n")
                log_file.write("Starting Adverts\n")
                broadcast_entry_count = process_broadcast_entries(
                    element.findall('.//BroadcastEntry'),
                    output_file,
                    None,
                    log_file,
                    broadcast_entry_count,
                )
                channel_entry_lines += 1

            elif element.tag == 'Channels':
                output_file.write("==Channels==\n")
                log_file.write("Starting Channels\n")

                for channel_entry in element.findall('ChannelEntry'):
                    channel_id = channel_entry.get('ID')
                    channel_name = channel_entry.get('name')
                    channel_cat = channel_entry.get('cat')
                    channel_freq = channel_entry.get('freq')

                    log_file.write(
                        f'ChannelEntry: ID="{channel_id}" '
                        f'name="{channel_name}" '
                        f'cat="{channel_cat}" '
                        f'freq="{channel_freq}"\n'
                    )
                    output_file.write(f"==={channel_name}===\n")
                    broadcast_entry_count = process_broadcast_entries(
                        channel_entry.findall('.//BroadcastEntry'),
                        output_file,
                        channel_entry,
                        log_file,
                        broadcast_entry_count,
                    )
                    channel_entry_lines += 1

        log_file.write(
            f"Total ChannelEntry: {channel_entry_lines}\n"
            f"Total BroadcastEntry: {broadcast_entry_count}"
        )
        print(f"ChannelEntry: {channel_entry_lines}")
        print(f"BroadcastEntry: {broadcast_entry_count}")
        print(
            f"{os.path.basename(output_file.name)} created in {output_file_path}"
        )
        print("Process completed successfully.")


if __name__ == "__main__":
    main()
