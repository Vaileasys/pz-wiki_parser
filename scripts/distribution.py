import re
import os
import csv
import shutil
from tqdm import tqdm
from core import utility


def main():
    root_path = os.getcwd()
    resources_path = os.path.join(root_path, 'resources/lua')
    output_path = os.path.join(root_path, 'output/distributions')
    csv_output_path = os.path.join(output_path, 'csv')
    file_names = ['distributions.lua', 'proceduraldistributions.lua', 'VehicleDistributions.lua']
    forage_file_name = 'foragedefinitions.lua'

    # Extract unique items
    unique_items = sorted(unique_items_extract(resources_path, file_names, forage_file_name))
    write_unique_names(unique_items, output_path)
    item_processing(unique_items, resources_path, csv_output_path, file_names)
    attached_weapon_processing(resources_path, output_path)
    formatting(unique_items, output_path)


def unique_items_extract(resources_path, file_names, forage_file_name):
    unique_items = set()
    # Regex to look for 'items = {' or 'junk = {'
    item_regex = re.compile(r'\b(items|junk)\s*=\s*\{')
    # Regex for matching 'type' entries in foragedefinitions.lua
    type_regex = re.compile(r'^\s*type\s*=\s*"([^"]+)",\s*$')

    # Process distribution and vehicle files
    for file_name in file_names:
        with open(os.path.join(resources_path, file_name), 'r') as file:
            recording = False
            for line in file:
                if line.strip().startswith('--'):
                    continue
                if recording:
                    if '}' in line:
                        recording = False
                    else:
                        items = re.findall(r'"([^"]+)"', line)
                        cleaned_items = [re.sub(r'.*\.', '', item) for item in items]
                        unique_items.update(cleaned_items)
                elif item_regex.search(line):
                    recording = True

    # Process foragedefinitions.lua for 'type' entries and items blocks
    path = os.path.join(resources_path, forage_file_name)
    with open(path, 'r') as file:
        recording = False
        for line in file:
            if line.strip().startswith('--'):
                continue
            if recording:
                if '}' in line:
                    recording = False
                else:
                    if type_regex.match(line):
                        match = type_regex.match(line)
                        full_item = match.group(1)
                        item_name = full_item.split('.')[-1]
                        unique_items.add(item_name)
                    else:
                        items = re.findall(r'"([^"]+)"', line)
                        cleaned_items = [re.sub(r'.*\.', '', item) for item in items]
                        unique_items.update(cleaned_items)
            elif item_regex.search(line):
                recording = True

    return unique_items


def write_unique_names(unique_items, output_path):
    # Create the full path for the unique names file
    file_path = os.path.join(output_path, 'unique_names.txt')
    os.makedirs(output_path, exist_ok=True)
    with open(file_path, 'w') as file:
        for item in sorted(unique_items):
            file.write(item + '\n')


def item_processing(unique_items, resources_path, output_path, file_names):
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    for item in tqdm(unique_items, desc="Processing items"):
        processed_entries = item_processing_container(item, resources_path)
        processed_entries = process_distribution_items(item, resources_path, processed_entries)
        write_container_csv(item, output_path, processed_entries)
        item_processing_vehicle(item, resources_path, output_path)
        item_processing_foraging(item, resources_path, output_path)


def item_processing_container(item, resources_path):
    procedural_data = os.path.join(resources_path, 'proceduraldistributions.lua')
    distribution_data = os.path.join(resources_path, 'distributions.lua')

    processed_entries = []

    with open(procedural_data, 'r') as file:
        proc_lines = file.readlines()
    with open(distribution_data, 'r') as file:
        dist_lines = file.readlines()

    item_value_pattern = re.compile(r'(?:[."]){}"\s*,\s*([0-9]+(?:\.[0-9]+)?)'.format(re.escape(item)), re.IGNORECASE)
    id_pattern = re.compile(r'^\s{4}(\w+)\s')
    container_pattern_primary = re.compile(r'^\s{8}(\w+)\s')
    container_pattern_fallback = re.compile(r'^\s{4}(\w+)\s')
    ignore_line_pattern = re.compile(r'(items|junk|rolls)', re.IGNORECASE)
    room_pattern = re.compile(r'^\s{4}(\w+)\s')
    rolls_pattern = re.compile(r'rolls\s*=\s*(\d+)', re.IGNORECASE)

    for index, line in enumerate(proc_lines):
        if item_value_pattern.search(line):
            value_match = item_value_pattern.search(line)
            quantity = float(value_match.group(1))

            proc_id = None
            rolls = None
            checked_lines = []

            # Find proc_id
            for j in range(index, -1, -1):
                id_match = id_pattern.match(proc_lines[j])
                if id_match:
                    proc_id = id_match.group(1)
                    break

            # Find rolls starting from the line where the item ID was found
            for j in range(index, -1, -1):
                rolls_match = rolls_pattern.search(proc_lines[j])
                checked_lines.append(proc_lines[j].strip())  # Collect checked lines for debug
                if rolls_match:
                    rolls = int(rolls_match.group(1))
                    break

            if not proc_id:
                continue

            search_id_pattern = re.compile(r'"{}"'.format(re.escape(proc_id)), re.IGNORECASE)

            for k, dist_line in enumerate(dist_lines):
                if search_id_pattern.search(dist_line):
                    # Search for container
                    container = None
                    for back_index in range(k - 1, -1, -1):
                        if not ignore_line_pattern.search(dist_lines[back_index]):
                            if container_pattern_primary.match(dist_lines[back_index]):
                                container = container_pattern_primary.match(dist_lines[back_index]).group(1).strip()
                                break
                            elif container_pattern_fallback.match(dist_lines[back_index]):
                                container = container_pattern_fallback.match(dist_lines[back_index]).group(1).strip()
                                break

                    # Search for room
                    room = None
                    for back_index in range(k - 1, -1, -1):
                        if room_pattern.match(dist_lines[back_index]):
                            room = room_pattern.match(dist_lines[back_index]).group(1).strip()
                            break

                    if rolls is None or rolls == 0:
                        print(f"Debug: No valid rolls found for Item '{item}' - Proc ID: {proc_id}. Checked lines: {checked_lines}")

                    # Add entry to processed entries if all components are found
                    if room and container and rolls:
                        processed_entries.append((room, container, rolls, quantity))

    return processed_entries


def process_distribution_items(item, resources_path, processed_entries):
    distribution_data = os.path.join(resources_path, 'distributions.lua')

    with open(distribution_data, 'r') as file:
        lines = file.readlines()

    # Update item_pattern to correctly format and match item names followed by a comma and a number
    item_pattern = re.compile(r'"{}"\s*,\s*([0-9]+)'.format(re.escape(item)), re.IGNORECASE)
    quantity_pattern = re.compile(r'(?<=,)\s*([0-9]+(?:\.[0-9]+)?)\s*,')  # Matches the number immediately after the first comma
    room_pattern = re.compile(r'^\s{4}(\w+)\s')

    matches = []  # List to store item matches

    for line_number, line in enumerate(lines, start=1):
        item_match = item_pattern.search(line)
        if item_match:
            matches.append((item_match.group(1), line, line_number))

    debug_processed = []  # List to store debug messages for processed matches
    for match_index, (matched_item, line, line_number) in enumerate(matches, start=1):

        quantity_match = quantity_pattern.search(line)
        if quantity_match:
            quantity = float(quantity_match.group(1))
            room, container, rolls_value = None, None, None

            # Check previous lines for room information
            for prev_line_number in range(line_number - 1, 0, -1):
                prev_line = lines[prev_line_number - 1]
                room_match = room_pattern.match(prev_line)
                if room_match:
                    room = room_match.group(1).strip()
                    break

            for j in range(line_number - 1, -1, -1):
                if not container and 'rolls' in lines[j]:
                    rolls_match = re.search(r'rolls\s*=\s*(\d+)', lines[j])
                    if rolls_match:
                        rolls_value = rolls_match.group(1)
                        container_match = re.match(r'^\s*(\w+)\s*=\s*\{', lines[j - 1])
                        if container_match:
                            container = container_match.group(1).strip()
                            entry = (room or "all", container, rolls_value, quantity)
                            if entry not in processed_entries:
                                processed_entries.append(entry)

    return processed_entries


def write_container_csv(item, output_path, processed_entries):
    if processed_entries:
        csv_file_path = os.path.join(output_path, f'{item}_container.csv')
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        unique_entries = set()  # Set to store unique entries
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for entry in sorted(processed_entries):
                if entry not in unique_entries:  # Check if entry is unique
                    unique_entries.add(entry)  # Add entry to set of unique entries
                    entry_list = list(entry)
                    rolls = float(entry_list[2])
                    chance = float(entry_list[3])
                    effective_chance = (1 + ((100 * chance * 0.6) + (10 * 4))) / 10000
                    final_chance = round((1 - (1 - effective_chance) ** rolls) * 100, 2)
                    entry_list.append(final_chance)
                    # Write the modified list back to the CSV
                    writer.writerow(entry_list)


def item_processing_vehicle(item, resources_path, output_path):
    vehicle_data_path = os.path.join(resources_path, 'VehicleDistributions.lua')
    vehicle_entries = set()
    item_pattern = re.compile(r'"{}"\s*,\s*(\d+(?:\.\d+)?)'.format(re.escape(item)), re.IGNORECASE)

    with open(vehicle_data_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if item_pattern.search(line):
            # Find the first word of the line that defines vehicle type
            for j in range(i, -1, -1):
                if re.match(r'VehicleDistributions\.[^\s]+ = \{', lines[j]):
                    vehicle_type = re.match(r'VehicleDistributions\.([^\s]+) = \{', lines[j]).group(1)
                    break
            # Find the 'rolls' value
            rolls_value = None
            for k in range(i, -1, -1):
                if 'rolls' in lines[k]:
                    rolls_value = re.search(r'rolls\s*=\s*(\d+)', lines[k]).group(1)
                    break
            # Extract the quantity
            quantity = item_pattern.search(line).group(1)

            vehicle_entries.add((vehicle_type, rolls_value, quantity))

    # Write results to CSV only if there are entries
    if vehicle_entries:
        csv_file_path = os.path.join(output_path, f'{item}_vehicle.csv')
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for entry in sorted(vehicle_entries):
                # Convert tuple entry to a list to modify it
                entry_list = list(entry)
                rolls = float(entry_list[1])
                chance = float(entry_list[2])
                effective_chance = (1 + ((100 * chance * 0.6) + (10 * 4))) / 10000
                final_chance = round((1 - (1 - effective_chance) ** rolls) * 100, 2)
                entry_list.append(final_chance)
                # Write the modified list back to the CSV
                writer.writerow(entry_list)


def clean_foraging_file(resources_path):
    forage_file_path = os.path.join(resources_path, 'forageDefinitions.lua')
    output_path = os.path.join(resources_path, 'foraging_clean.lua')

    with open(forage_file_path, 'r') as file:
        content = file.readlines()

    start_index = next((i for i, line in enumerate(content) if "======== forageDefs ========" in line), None)
    if start_index is not None:
        content = content[start_index + 1:]

    clean_content = []
    in_comment_block = False
    for line in content:
        original_line = line
        line = line.strip()
        if line.startswith('--[[') or ('--[[ ' in line):
            in_comment_block = True
        elif line.endswith(']]') or (' ]]--' in line):
            in_comment_block = False
            continue
        if not in_comment_block and not line.startswith('--'):
            clean_content.append(original_line)

    with open(output_path, 'w') as file:
        file.writelines(clean_content)

    return output_path


def item_processing_foraging(item, resources_path, output_path):
    clean_file_path = clean_foraging_file(resources_path)
    with open(clean_file_path, 'r') as file:
        content = file.readlines()

    details_type1 = process_type1_foraging(item, content)
    details_type2 = process_type2_foraging(item, content)

    if details_type1:
        save_to_csv(details_type1, output_path, item, 1)
    if details_type2:
        save_to_csv(details_type2, output_path, item, 2)


def process_type1_foraging(item, content):
    details_type1 = {}
    type1_regex = re.compile(r'type\s*=\s*"[\w\.]*' + re.escape(item) + r'"', re.IGNORECASE)
    record_type1 = False
    block_content = []
    brace_count = 0  # To manage nested braces

    for i, line in enumerate(content):
        line = line.strip()
        if type1_regex.search(line):
            if not record_type1:
                record_type1 = True
                brace_count = 1  # Start counting braces from this line
                block_content = [line]
        elif record_type1:
            block_content.append(line)
            if '{' in line:
                brace_count += line.count('{')
            if '}' in line:
                brace_count -= line.count('}')
            if brace_count == 0:  # Only end recording when all opened braces are closed
                record_type1 = False
                block_data = extract_data_from_block(block_content)
                details_type1[item] = block_data

    return details_type1


def process_type2_foraging(item, content):
    details_type2 = {}
    item_pattern = re.compile(r'{} = "Base\.{}"'.format(item, item), re.IGNORECASE)
    context_start_pattern = re.compile(r'^\t\t\w+ = \{')  # To identify the start of a block
    blacklist = set()

    for index, line in enumerate(content):
        line = line.strip()
        if item_pattern.search(line) and line not in blacklist:
            blacklist.add(line)
            context_index = index
            block_data = {'chance': None, 'months': None}

            # First independent search for 'months'
            months_index = context_index
            while months_index > 0 and not block_data['months']:
                months_index -= 1
                current_line = content[months_index].strip()
                if 'months =' in current_line:
                    months = re.findall(r'\{([\s\d,]+)\}', current_line)
                    if months:
                        month_numbers = months[0].replace(' ', '').split(',')
                        block_data['months'] = '|'.join(month_numbers)
                if context_start_pattern.match(current_line):
                    break  # Stop this search upon hitting another block start

            # Second independent search for 'chance'
            chance_index = context_index
            while chance_index > 0 and not block_data['chance']:
                chance_index -= 1
                current_line = content[chance_index].strip()
                if 'chance =' in current_line:
                    chance_match = re.search(r'chance\s*=\s*(\d+)', current_line)
                    if chance_match:
                        block_data['chance'] = chance_match.group(1)
                if context_start_pattern.match(current_line):
                    break  # Stop this search upon hitting another block start

            if block_data['months'] or block_data['chance']:
                details_type2[item] = block_data

    return details_type2


def save_to_csv(details, output_path, item, type_number):
    headers = {
        1: ['minCount', 'maxCount', 'skill', 'snowChance', 'rainChance', 'dayChance', 'nightChance', 'months', 'bonusMonths', 'malusMonths', 'zones'],
        2: ['chance', 'months']
    }

    csv_file_path = os.path.join(output_path, f'{item}_foraging{type_number}.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers[type_number])
        for key, data in details.items():
            row = [data.get(header) for header in headers[type_number]]
            writer.writerow(row)


def extract_data_from_block(block_content):
    block_data = {
        'minCount': None, 'maxCount': None, 'skill': None,
        'xp': None, 'snowChance': None, 'rainChance': None, 'dayChance': None, 'nightChance': None,
        'months': '', 'bonusMonths': '', 'malusMonths': '', 'zones': ''
    }
    for line in block_content:
        line = line.strip()
        if 'minCount' in line:
            block_data['minCount'] = re.findall(r'minCount\s*=\s*(\d+)', line)[0]
        if 'maxCount' in line:
            block_data['maxCount'] = re.findall(r'maxCount\s*=\s*(\d+)', line)[0]
        if 'skill' in line:
            block_data['skill'] = re.findall(r'skill\s*=\s*(\d+)', line)[0]
        if 'xp' in line:
            block_data['xp'] = re.findall(r'xp\s*=\s*(\d+)', line)[0]
        if 'snowChance' in line:
            block_data['snowChance'] = re.findall(r'snowChance\s*=\s*(-?\d+)', line)[0]
        # Include patterns for other fields similarly

        # Handling lists within blocks for zones, months, etc.
        if 'zones' in line and '{' in line:
            zone_data = []
            zone_start_index = block_content.index(line)  # Find the starting index of zones
            for zone_line in block_content[zone_start_index:]:
                if '}' in zone_line:
                    break
                zone_match = re.findall(r'(\w+)\s*=\s*(\d+)', zone_line)
                if zone_match:
                    zone_data.extend(zone_match)
            block_data['zones'] = dict(zone_data)

        # Parsing months, ensuring to capture lists correctly
        if 'bonusMonths' in line:
            bonus_months = re.findall(r'(\d+)', line)
            block_data['bonusMonths'] = '|'.join(bonus_months)
        if 'malusMonths' in line:
            malus_months = re.findall(r'(\d+)', line)
            block_data['malusMonths'] = '|'.join(malus_months)

    return block_data


def attached_weapon_processing(resources_path, output_path):
    output_dir = os.path.join(output_path, 'csv')
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(resources_path, 'AttachedWeaponDefinitions.lua')
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Remove comments indicated by '--'
    content = [re.sub(r'--.*$', '', line) for line in content]
    content = ''.join(content)

    definition_blocks = content.split('AttachedWeaponDefinitions.')
    item_regex = re.compile(r'(\w+)\s*=\s*\{')
    chance_regex = re.compile(r'chance\s*=\s*(\d+)', re.IGNORECASE)
    outfit_regex = re.compile(r'outfit\s*=\s*\{\s*"([^}]+)"\s*\}', re.IGNORECASE)
    day_regex = re.compile(r'daySurvived\s*=\s*(\d+)', re.IGNORECASE)
    weapon_regex = re.compile(r'weapons\s*=\s*\{\s*([^}]+)\}', re.IGNORECASE)

    for index, block in enumerate(definition_blocks[1:], start=1):  # Start index at 1 since we skip the first split part
        item_match = item_regex.search(block)
        if item_match:
            item_name = item_match.group(1)

            chance_match = chance_regex.search(block)
            chance = chance_match.group(1) if chance_match else "Unknown"

            outfit_match = outfit_regex.search(block)
            if outfit_match:
                outfit = outfit_match.group(1).replace('"', '').replace(' ', '').replace(',', '|')
            else:
                outfit = "All"

            day_match = day_regex.search(block)
            days_survived = day_match.group(1) if day_match else "Unknown"

            weapon_match = weapon_regex.search(block)
            weapons = []
            if weapon_match:
                raw_weapons = weapon_match.group(1).split(',')
                for weapon_raw in raw_weapons:
                    weapon_clean = weapon_raw.strip().split('.')[-1].replace('"', '')
                    weapons.append(weapon_clean)

            for weapon in weapons:
                csv_file_path = os.path.join(output_dir, f'{weapon}_zombie.csv')
                file_exists = os.path.exists(csv_file_path)
                with open(csv_file_path, 'a', newline='') as csvfile:  # Append mode
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(['Chance', 'Outfit', 'Days Survived'])  # Header for new file
                    writer.writerow([chance, outfit, days_survived])


def month_lookup(month_number):
    month_dict = {
        '1': 'January', '2': 'February', '3': 'March',
        '4': 'April', '5': 'May', '6': 'June',
        '7': 'July', '8': 'August', '9': 'September',
        '10': 'October', '11': 'November', '12': 'December'
    }
    return month_dict.get(month_number, '-')


def process_container_file(file_path):
    rows_to_add = []
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            effective_chance = f"{row[4]}%"
            formatted_row = f"""
    |-
    | {row[0]}
    | {{{{ll|{row[1]}}}}}
    | {effective_chance}
    """
            if any(cell.strip() for cell in row):
                rows_to_add.append(formatted_row)
    if rows_to_add:
        table_caption = "{{ll|Containers}}"
        container_output = "<div id=\"containers\" style=\"flex-basis: 30%;\">\n"
        container_output += f"    {{| class=\"wikitable theme-red sortable\" style=\"margin-right: 15px; width: 95%;\"\n"
        container_output += f"    |+ {table_caption}\n"
        container_output += "    ! Building/Room\n    ! Container\n    ! Effective chance\n"
        container_output += ''.join(rows_to_add) + "|}\n</div>\n"
        return container_output
    return ""


def process_vehicle_file(file_path):
    vehicle_output = ''
    rows_to_add = []
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            effective_chance = f"{row[3]}%"
            type_parts = re.findall('[A-Z][^A-Z]*', row[0])

            if type_parts[0] == "Mc" and len(type_parts) > 1:
                vehicle_type = type_parts[0] + type_parts[1]
                container = ' '.join(type_parts[2:])
            elif ' '.join(type_parts[:2]) == "Metal Welder" and len(type_parts) > 2:
                vehicle_type = ' '.join(type_parts[:2])
                container = ' '.join(type_parts[2:])
            elif ' '.join(type_parts[:3]) == "Mass Gen Fac" and len(type_parts) > 3:
                vehicle_type = ' '.join(type_parts[:3])
                container = ' '.join(type_parts[3:])
            elif ' '.join(type_parts[:2]) == "Construction Worker" and len(type_parts) > 2:
                vehicle_type = ' '.join(type_parts[:2])
                container = ' '.join(type_parts[2:])
            elif type_parts[0] == "Glove" or ' '.join(type_parts[:2]) == "Glove box":
                vehicle_type = "All"
                container = ' '.join(type_parts)
            elif type_parts[0] == "Trunk":
                vehicle_type = ' '.join(type_parts[1:])
                container = type_parts[0]
            else:
                vehicle_type = type_parts[0]
                container = ' '.join(type_parts[1:])

            formatted_row = f"""
    |-
    | {vehicle_type}
    | {{{{ll|{container}}}}}
    | {effective_chance}
    """
            if any(cell.strip() for cell in row):
                rows_to_add.append(formatted_row)

    if rows_to_add:
        table_caption = "{{ll|Vehicles}}"
        vehicle_output += "<div id=\"vehicles\" style=\"flex-basis: 30%;\">\n"
        vehicle_output += f"    {{| class=\"wikitable theme-red sortable\" style=\"margin-right: 15px; width: 95%;\"\n"
        vehicle_output += f"    |+ {table_caption}\n"
        vehicle_output += "    ! Type\n    ! Container\n    ! Effective chance\n"
        vehicle_output += ''.join(rows_to_add) + "|}\n</div>\n"
    return vehicle_output


def process_zombie_file(file_path):
    zombie_output = ''
    unique_rows = set()
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if any(cell.strip() for cell in row):
                outfit = row[1].replace('|', '<br>')
                days = row[2]
                chance = row[0]
                formatted_row = f"""
    |-
    | {outfit}
    | {days}
    | {chance}
    """
                unique_rows.add(formatted_row)
    if unique_rows:
        table_caption = "{{ll|Zombies}}"
        zombie_output += "<div id=\"zombies\" style=\"flex-basis: 30%;\">\n"
        zombie_output += f"    {{| class=\"wikitable theme-red sortable\" style=\"margin-right: 15px; width: 95%;\"\n"
        zombie_output += f"    |+ {table_caption}\n"
        zombie_output += "    ! Outfit\n    ! Days survived\n    ! Chance\n"
        zombie_output += ''.join(unique_rows) + "|}\n</div>\n"
    return zombie_output


def process_foraging_file(file_paths):
    foraging_table = ''
    rows_to_add = []
    foraging_exists = False

    for file_type, file_path in file_paths.items():
        if file_path:
            with open(file_path, mode='r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                foraging_exists = True

                for row in reader:
                    row = [x.strip() if x else '-' for x in row]
                    if file_type == 'foraging1':
                        zones = re.sub(r"[{}']", "", row[10]).replace(":", " ").replace(",", "<br>")
                        months = "<br>".join([month_lookup(x) for x in row[7].split('|') if x])
                        bonus_months = "<br>".join([month_lookup(x) for x in row[8].split('|') if x])
                        malus_months = "<br>".join([month_lookup(x) for x in row[9].split('|') if x])
                        formatted_row = f"""
    |-
    | {row[0]}-{row[1]}
    | {row[2]}
    | {zones}
    | {row[3]}
    | {row[4]}
    | {row[5]}
    | {row[6]}
    | {months}
    | {bonus_months}
    | {malus_months}
    """
                    elif file_type == 'foraging2':
                        chance_info = f"all with {row[0]} chance"
                        formatted_row = f"""
    |-
    | 1
    | 0
    | {chance_info}
    | -
    | -
    | -
    | -
    | all
    | -
    | -
    """
                    if any(cell.strip() for cell in row):
                        rows_to_add.append(formatted_row)

    if foraging_exists and rows_to_add:
        foraging_table = f"    {{| class=\"wikitable theme-red\" style=\"width: 98%;\"\n"
        foraging_table += "    |+ {{ll|Foraging}}\n"
        foraging_table += "    ! rowspan=\"2\" | Amount\n    ! rowspan=\"2\" | Skill level\n    ! rowspan=\"2\" | Biomes\n    ! colspan=\"4\" style=\"text-align: center;\" | Weather modifiers\n    ! colspan=\"3\" style=\"text-align: center;\" | Month modifiers\n    |-\n"
        foraging_table += "    ! Snow\n    ! Rain\n    ! Day\n    ! Night\n    ! Months available\n    ! Bonus months\n    ! Malus months\n"
        foraging_table += ''.join(rows_to_add)
        foraging_table += "|}\n"

    return foraging_table


def formatting(unique_items, output_path):
    version = utility.version
    complete_output_path = os.path.join(output_path, 'complete')
    csv_output_path = os.path.join(output_path, 'csv')

    if os.path.exists(complete_output_path):
        shutil.rmtree(complete_output_path)
    os.makedirs(complete_output_path)

    # Iterate through each item and process
    for item in tqdm(unique_items, desc="Formatting items"):
        output_data = f"<!--BOT FLAG|{item}|{version}-->\n"
        output_data += "<div class=\"togglebox theme-red\">\n"
        output_data += f"    <div>{item} distribution\n"
        output_data += f"        <span class=\"mw-customtoggle-togglebox-{item}\" title=\"{{{{int:show}}}} / {{{{int:hide}}}}\" style=\"float: right; padding-right: 30px; padding-top: 4px; font-size: 0.7em; font-weight: normal;\">{{{{int:show}}}} / {{{{int:hide}}}}</span></div>\n"
        output_data += f"\n    <div class=\"mw-collapsible mw-collapsed\" id=\"mw-customcollapsible-togglebox-{item}\">\n"
        output_data += f"    Effective chance calculations are based off of default loot settings, and median zombie density. The higher the density of zombies in an area, the higher the effective chance of an item spawning. Chance is also influenced by the [[lucky]] and [[unlucky]] traits."
        output_data += f"    <div class=\"toggle-content\">\n<div class=\"pz-container\">\n"

        # Identify relevant files for the item
        item_files = {file_type: None for file_type in ['container', 'vehicle', 'foraging1', 'foraging2', 'zombie']}
        for filename in os.listdir(csv_output_path):
            for file_type in item_files.keys():
                if filename.startswith(item + '_') and filename.endswith(f'{file_type}.csv'):
                    item_files[file_type] = os.path.join(csv_output_path, filename)

        # Process each identified file using the corresponding functions
        if item_files['container']:
            output_data += process_container_file(item_files['container'])
        if item_files['vehicle']:
            output_data += process_vehicle_file(item_files['vehicle'])
        if item_files['zombie']:
            output_data += process_zombie_file(item_files['zombie'])
        # Ensure both foraging file types are processed
        foraging_data = ''
        for foraging_type in ['foraging1', 'foraging2']:
            if item_files[foraging_type]:
                foraging_data += process_foraging_file({foraging_type: item_files[foraging_type]})
        if foraging_data:
            output_data += f"\n    </div><div style=\"clear: both;\"></div>\n" + foraging_data + f"    </div></div><div class=\"toggle large mw-customtoggle-togglebox-{item}\" title=\"{{{{int:show}}}}/{{{{int:hide}}}}\"></div></div>\n"
        else:
            output_data += f"\n    </div><div style=\"clear: both;\"></div>\n    </div></div><div class=\"toggle large mw-customtoggle-togglebox-{item}\" title=\"{{{{int:show}}}}/{{{{int:hide}}}}\"></div></div>\n"

        output_data += f"<!--END BOT FLAG|{item}|{version}-->\n"
        output_data = '\n'.join(line for line in output_data.split('\n') if line.strip())

        # Write the formatted data to a file
        with open(os.path.join(complete_output_path, f'{item}.txt'), 'w') as output_file:
            output_file.write(output_data)


if __name__ == '__main__':
    main()
