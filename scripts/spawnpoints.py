from pathlib import Path
from scripts.core import lua_helper, utility, translate
from scripts.core.constants import (LUA_PATH, DATA_PATH)

OUTPUT_DIR = Path("output") / "spawnpoints"
LUA_DIR = Path(LUA_PATH) / "spawnpoints"

TABLE_HEADER = '''{| class="wikitable theme-red sortable"
! Building
! Coordinates
! Occupation(s)'''

def format_coordinates(posX, posY):
    """Format coordinates as a wiki template."""
    return f"{{{{Coordinates|{posX}x{posY}}}}}"


def normalise_profession(profession):
    professions = {
        "repairman": "Repairman",
        "doctor": "Doctor",
        "constructionworker": "constructionworker",
        "chef": "Chef",
        "unemployed": "unemployed",
        "parkranger": "parkranger",
        "nurse": "Nurse",
        "policeofficer": "policeoff",
        "fireofficer": "fireoff",
        "securityguard": "securityguard"
    }

    profession = professions.get(profession, profession)
    profession = "UI_prof_" + profession

    return profession


def reorder_spawn_data(normalised_data):
    """Reorder data to be grouped by coordinate instead of profession."""
    coordinate_map = {}

    for profession, coords_list in normalised_data.items():
        profession = normalise_profession(profession)
        profession = translate.get_translation(profession)
        profession = f"[[{profession}]]"

        for coords in coords_list:
            coord_str = format_coordinates(coords["posX"], coords["posY"])

            if coord_str not in coordinate_map:
                coordinate_map[coord_str] = []

            if profession not in coordinate_map[coord_str]:
                coordinate_map[coord_str].append(profession)

    return coordinate_map


def normalise_spawn_data(spawn_data):
    """Normalise world coordinates."""
    normalised_data = {}
    
    for profession, coords_list in spawn_data.items():
        normalised_data[profession] = []
        
        for coords in coords_list:
            worldX = coords.get("worldX", 0)
            worldY = coords.get("worldY", 0)
            posX = 300 * worldX + coords.get("posX", 0)
            posY = 300 * worldY + coords.get("posY", 0)
            posZ = coords.get("posZ", 0)

            normalised_data[profession].append({"posX": posX, "posY": posY, "posZ": posZ})
    
    return normalised_data


def write_to_file(coord_data, output_file):
    content = []
    content.append(TABLE_HEADER)
    for coord, professions in coord_data.items():
        content.append('|-')
        content.append('| style="text-align: center;" | [[File:Image.png|256px]]<br>Placeholder')
        content.append(f'| {coord}')
        prof_str = "<br>".join(professions)
        content.append(f'| {prof_str}')

    content.append("|}")
    output_path = OUTPUT_DIR / output_file
    with open(output_path, "w") as file:
        file.write("\n".join(content))
    print(f"File written to '{output_path}'")


def process_lua_file(lua_file):
    """Processes spawnpoints lua file."""
    try:
        lua_runtime = lua_helper.load_lua_file(str(lua_file.relative_to(LUA_DIR.parent)))
        lua_runtime.execute("spawnpoints = SpawnPoints()")
        parsed_data = lua_helper.parse_lua_tables(lua_runtime)

        # Remove 'spawnpoints' key
        spawnpoints_data = next(iter(parsed_data.values()), {})
#        utility.save_cache(spawnpoints_data, lua_file.stem + "_raw.json", f"{DATA_PATH}/spawnpoints")

        # Check if coordinates use old cell coordinates (300x300)
        is_worldcoord = False
        for key, value in spawnpoints_data.items():
            if not isinstance(value, list):
                is_worldcoord = True
                break

        if is_worldcoord:
            normalised_data = normalise_spawn_data(spawnpoints_data)
        else:
            normalised_data = spawnpoints_data
        utility.save_cache(normalised_data, lua_file.stem + "_noramlised.json", f"{DATA_PATH}/spawnpoints")

        reordered_data = reorder_spawn_data(normalised_data)

        
#        utility.save_cache(reordered_data, lua_file.stem + "_reordered.json", f"{DATA_PATH}/spawnpoints")

        write_to_file(reordered_data, f"{lua_file.stem}.txt")
    except KeyError as e:
        print(f"KeyError: '{lua_file}' has no {e} key")


def main():
    LUA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lua_files = list(LUA_DIR.glob("*.lua"))

    if not lua_files:
        print("No Lua files found in the spawnpoints directory. Try running setup again.")
        return

    for lua_file in lua_files:
        process_lua_file(lua_file)

if __name__ == "__main__":
    main()