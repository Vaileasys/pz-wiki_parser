import os
import re
from scripts.core.language import Language

# Regex patterns for function calls
set_exclusive_pattern = re.compile(r'setExclusive\s*\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)')
get_location_pattern  = re.compile(r'getOrCreateLocation\s*\(\s*"([^"]+)"\s*\)')
set_multi_pattern     = re.compile(r'setMultiItem\s*\(\s*"([^"]+)"\s*,\s*(true|false)\s*\)', re.IGNORECASE)
set_hide_model_pattern = re.compile(r'setHideModel\s*\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)')

LUA_FILE_PATH = "resources/lua/BodyLocations.lua"
output_file_path = "output/{language_code}/bodylocations_exclusives.txt"


# Parses BodyLocations.lua to get body locations and exclusive locations
def parse_bodylocations(file_path):
    exclusives_dict = {}
    locations = set()
    multi_locs = set()
    hide_locs = {}

    # Helper to record exclusives in a dictionary of sets
    def add_exclusive(a, b):
        # Repeat for 'a' and 'b' to add them both as exclusives to their dict
        exclusives_dict.setdefault(a, set()).add(b)
        exclusives_dict.setdefault(b, set()).add(a)

    # Helper to record hidden models in a dictionary of lists
    def add_hide_model(a, b):
        hide_locs.setdefault(a, set()).add(b)

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # setExclusive("A","B")
            match_excl = set_exclusive_pattern.search(line)
            if match_excl:
                locA, locB = match_excl.groups()
                add_exclusive(locA, locB)
                continue

            # getOrCreateLocation("X")
            match_loc = get_location_pattern.search(line)
            if match_loc:
                loc = match_loc.group(1)
                locations.add(loc)
                continue

            # setMultiItem("Y", true/false)
            match_multi = set_multi_pattern.search(line)
            if match_multi:
                locName, boolVal = match_multi.groups()
                if boolVal.lower() == 'true':
                    multi_locs.add(locName)
                continue

            # setHideModel("A", "B")
            match_hide = set_hide_model_pattern.search(line)
            if match_hide:
                locA, locB = match_hide.groups()
                add_hide_model(locA, locB)
                continue

    return exclusives_dict, locations, multi_locs, hide_locs


# Builds the wiki table and writes to a txt file
def build_table(lua_file_path, output_file_path):
    exclusives_dict, locations, multi_locs, hide_locs = parse_bodylocations(lua_file_path)

    wikilines = [
        '{| class="wikitable theme-blue"',
        '! Location !! Exclusive locations !! Hidden locations'
    ]

    # Filter out any multi locations from 'locations' (these are "Bandage", "Wound", "ZedDmg")
    locations = sorted(loc for loc in locations if loc not in multi_locs)

    # Builds the wiki table and stores each line in the 'wikilines' list
    for location in locations:
        # Filter out any multi locations from 'exclusives' for a 'location'
        exclusives = sorted(excls for excls in exclusives_dict.get(location, []) if excls not in multi_locs)
        hidden_locs = sorted(hide_locs.get(location, []))

        exclusives_str = ", ".join(f"[[#{excl}|{excl}]]" for excl in exclusives)
        hidden_locs_str = ", ".join(f"[[#{hidden}|{hidden}]]" for hidden in hidden_locs)

        wikilines.append(f'|- id="{location}"')
        wikilines.append(f'| {location} || {exclusives_str} || {hidden_locs_str}')

    wikilines.append('|}')

    # Build the table, joining each line into a single string
    table_str = '\n'.join(wikilines)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(table_str)


def main():
    global output_file_path
    language_code = Language.get()
    output_file_path = output_file_path.format(language_code=language_code)
    build_table(LUA_FILE_PATH, output_file_path)
    print(f"Output saved to '{output_file_path}'")


if __name__ == "__main__":
    main()
