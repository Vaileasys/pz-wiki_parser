import json
from pathlib import Path
from tqdm import tqdm
import concurrent.futures
import scripts.parser.distribution_parser as distribution_parser
from scripts.core import version, translate


def main():
    distribution_parser.main()

    json_path = Path("output/distributions/json/all_items.json")
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    unique_rooms = set()
    for obj_key, obj_value in data.items():
        if "Containers" not in obj_value:
            continue

        containers = obj_value["Containers"]
        for container_entry in containers:
            room_name = container_entry.get("Room")
            if room_name:
                unique_rooms.add(room_name)

    print(f"Found {len(unique_rooms)} unique rooms.")

    room_to_containers = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        with tqdm(total=len(unique_rooms), desc="Processing Rooms", unit="room") as pbar:
            for room in unique_rooms:
                futures[executor.submit(
                    process_single_room, room, data
                )] = room

            for future in concurrent.futures.as_completed(futures):
                room_name = futures[future]
                result_dict = future.result()
                room_to_containers[room_name] = result_dict
                pbar.update(1)

    generate_per_letter_files(room_to_containers)
    generate_main_page(room_to_containers)


def process_single_room(room_name: str, data: dict) -> dict:
    container_map = {}

    for obj_key, obj_value in data.items():
        if "Containers" not in obj_value:
            continue

        containers = obj_value["Containers"]
        for container_entry in containers:
            if container_entry.get("Room") == room_name:
                container_name = container_entry.get("Container", "unknown_container")

                if container_name not in container_map:
                    container_map[container_name] = set()
                container_map[container_name].add(obj_key)

    return container_map


def generate_per_letter_files(room_to_containers: dict):
    game_version = version.get_version()
    language_code = translate.get_language_code()

    rooms_by_letter = {}
    for room_name in room_to_containers:
        first_char = room_name[0].upper() if room_name else 'Other'
        if first_char not in rooms_by_letter:
            rooms_by_letter[first_char] = []
        rooms_by_letter[first_char].append(room_name)

    sorted_letters = sorted(rooms_by_letter.keys())

    for letter in sorted_letters:
        rooms_in_letter = sorted(rooms_by_letter[letter])
        output_dir = Path("output/distributions/roomdef/")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{letter}.txt"

        header_text = (
            "{{Header|Modding}}\n"
            f"{{{{Page version|{game_version}}}}}\n"
            "{{Autogenerated|reason=Any changes to this page will be overwritten automatically."
            "|source=[https://github.com/Vaileasys/pz-wiki_parser/ (Wiki parser)]}}\n\n"
            "All room defines are presented as is, for use in your custom maps. Exact item names have been modified "
            "for increased readability and a greater chance of linking to their respective wiki articles. For a full "
            "list of these items refer to the distribution files in your [[Project Zomboid]] install directory.\n\n"
            "'''Warning: Everything below has been programmatically generated - any changes made will be lost on the next update!'''\n\n"
            "==Room definitions and item spawns==\n"
            '{| class="wikitable theme-blue"\n|-\n\n'
        )

        footer_text = (
            "\n==See also==\n"
            "*{{ll|Mapping}}\n\n"
            "{{Navbox modding}}\n"
        )

        output_lines = [header_text]

        total_items = 0
        for room_name in rooms_in_letter:
            for container in room_to_containers[room_name].values():
                total_items += len(container)

        with tqdm(total=total_items, desc=f"Processing {letter} rooms", unit="item") as pbar:
            for room_name in rooms_in_letter:
                output_lines.append("! colspan=\"2\" |\n")
                output_lines.append(f"<h2 style=\"margin-top:0;\">{room_name}</h2>\n")
                output_lines.append("|-\n! Container !! Items\n|-\n")

                containers_sorted = sorted(room_to_containers[room_name].keys())
                last_container_idx = len(containers_sorted) - 1

                for idx, container_name in enumerate(containers_sorted):
                    output_lines.append(f"| [[{container_name}]] || ")

                    items = sorted(room_to_containers[room_name][container_name])
                    translated_items = []
                    for item in items:
                        translated = translate.get_translation("Base." + item, property_key="DisplayName",
                                                               lang_code=language_code)
                        translated_items.append(f"[[{translated}]]")
                        pbar.update(1)
                    items_line = ", ".join(translated_items)
                    output_lines.append(items_line)

                    output_lines.append("\n|-\n" if idx < last_container_idx else "\n|-\n")

            output_lines.append("|}\n")
            output_lines.append(footer_text)

        final_output = "".join(output_lines)
        print(f"Writing {letter} to {output_file}")
        with output_file.open("w", encoding="utf-8") as f:
            f.write(final_output)


def generate_main_page(room_to_containers: dict):
    game_version = version.get_version()

    output_file = Path("output/distributions/room_definitions_main.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    header_text = (
        "{{Header|Modding}}\n"
        f"{{{{Page version|{game_version}}}}}\n"
        "{{Autogenerated|reason=Any changes to this page will be overwritten automatically."
        "|source=[https://github.com/Vaileasys/pz-wiki_parser/ (Wiki parser)]}}\n\n"
        "This page lists all rooms and their corresponding containers. Each room is linked to its respective letter page where detailed item spawns can be found.\n\n"
        "'''Warning: Everything below has been programmatically generated - any changes made will be lost on the next update!'''\n\n"
        "==Room list==\n"
        '{| class="wikitable theme-blue sortable"\n|-\n'
        '! Room !! Containers\n|-\n'
    )

    footer_text = (
        "\n|}\n"
        "\n==See also==\n"
        "*{{ll|Mapping}}\n\n"
        "{{Navbox modding}}\n"
    )

    output_lines = [header_text]

    all_rooms_sorted = sorted(room_to_containers.keys())

    for room_name in all_rooms_sorted:
        first_letter = room_name[0].upper() if room_name else 'Other'
        room_link = f"[[Room definitions and item spawns/{first_letter}#{room_name}|{room_name}]]"
        containers = sorted(room_to_containers[room_name].keys())
        container_links = [f"[[{container}]]" for container in containers]
        containers_line = ", ".join(container_links)
        output_lines.append(f"| {room_link} || {containers_line}\n|-\n")

    output_lines.append(footer_text)

    final_output = "".join(output_lines)
    with output_file.open("w", encoding="utf-8") as f:
        f.write(final_output)
    print(f"Main page written to {output_file}")


if __name__ == "__main__":
    main()