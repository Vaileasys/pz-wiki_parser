from scripts.utils import lua_helper, utility, table_helper
from scripts.parser import item_parser
from scripts.core import translate
from scripts.utils.util import echo, format_positive
from scripts.core.constants import RESOURCE_PATH
from scripts.utils.media_helper import CODES, parse_code_effects

TABLE_HEADER = '{| class="wikitable theme-red sortable""'
TABLE_PATH = f"{RESOURCE_PATH}/tables/recmedia_table.json"
recmedia_data = {}
table_map = {}

def generate_data(guid, rm_data):
    """Generates all data for the recmedia item, for table generation."""
    table_type = rm_data.get("TableType")
    media_category = rm_data.get("category")
    columns = table_map.get(table_type) if table_map.get(table_type) is not None else table_map.get("default")

    item = {}

    item_name = rm_data.get("itemDisplayName")
    page = item_name.split(":")[1].strip().replace("#", "") # Special case for #012
    title = rm_data.get("title")
    subtitle = rm_data.get("subtitle")

    full_title = title + " " + subtitle if subtitle and rm_data.get("category") != "Home-VHS" else title
    lines = rm_data.get("lines")

    merged_effects = {}

    for line_data in lines.values():
        effects = line_data.get("effects", {})
        for key, value in effects.items():
            if CODES.get(key, {}).get("type") == "recipe":
                merged_effects[key] = value
            else:
                try:
                    numeric_value = float(value)
                except (ValueError, TypeError):
                    continue
                merged_effects[key] = merged_effects.get(key, 0.0) + numeric_value
    
    style_center = "style=\"text-align: center;\" | "
    style_nowrap = "style=\"white-space: nowrap;\" | "
    empty_string = style_center + "-"

    moodles = {}
    moodle_list = []
    skills = []
    recipes = []
    for code, value in merged_effects.items():
        code_id = CODES.get(code, {}).get("id", code)
        if code_id is None:
            echo(f"Warning: code_id for '{code}' doesn't exist.")
            continue
        code_title = translate.get_translation(CODES.get(code, {}).get("title", code))
        code_type = CODES.get(code, {}).get("type", "moodle")
        if code_type == "skill":
            skills.append(f"{utility.format_link(code_title)}: {format_positive(value)}")
        if code_type == "recipe":
#            recipes.append(f"{code_title.replace('%1', value)}")
            recipes.append(value)
        elif code_type == "moodle":
            moodle_list.append(f"{code_title}: {format_positive(value)}")
            moodles[code_id] = format_positive(value)
    
    moodle_list = None if not moodle_list else "<br>".join(moodle_list)
    skills = None if not skills else "<br>".join(skills)
    recipes = None if not recipes else "<br>".join(recipes)

    item["title"] = utility.format_link(full_title, page) if "title" in columns else None
    item["author"] = rm_data.get("author", empty_string) if "author" in columns else None
    item["production"] = rm_data.get("extra", empty_string) if "production" in columns else None
    if "cover" in columns:
        item["cover"] = rm_data.get("extra") if rm_data.get("extra") else empty_string
    item["lines"] = style_center + str(len(lines)) if "lines" in columns else None
    if "effect" in columns:
        item["effect"] = style_nowrap + moodle_list if moodle_list else empty_string
    for moodle, value in moodles.items():
        if moodle in columns:
            item[moodle] = style_center + str(value)
        else:
            echo(f"Note: Unused '{moodle}' moodle was found for '{guid}' ({table_type}). Should it be added to the table map?")
    for code, code_data in CODES.items():
        if code_data.get("type") == "moodle":
            code_id = code_data.get("id")
            if code_id not in item and code_id in columns:
                item[code_id] = empty_string
    if "recipe" in columns:
        item["recipe"] = style_nowrap + recipes if recipes else empty_string
    if "skill" in columns:
        item["skill"] = style_nowrap + skills if skills else empty_string
    item["guid"] = guid if "guid" in columns else None
    item["item_id"] = find_item_id(media_category) if "item_id" in columns else None
    
    # Remove any values that are None
    item = {k: v for k, v in item.items() if v is not None}

    # Ensure column order is correct
    item = {key: item[key] for key in columns if key in item}

    # Add item_name for sorting
    item["item_name"] = full_title

    return item


def find_table_type(rm_data):
    category = rm_data.get("category")
    if category == "Retail-VHS":
        if rm_data.get("extra"):
            table_type = "vhs_movie"
        else:
            table_type = "vhs_show"
    elif category == "Home-VHS":
        table_type = "vhs_home"
    elif category == "CDs":
        table_type = "cd"
    else:
        table_type = "default"
    
    rm_data["TableType"] = table_type
    return rm_data


def process_items():
    global table_map
    table_map, column_headings = table_helper.get_table_data(TABLE_PATH)
    all_rm_data = get_recmedia_data()
    items = {}
    for guid, rm_data in all_rm_data.items():
        rm_data = find_table_type(rm_data)
        table_type = rm_data.get("TableType")

        if table_type not in items:
            items[table_type] = []

        items[table_type].append(generate_data(guid, rm_data))

    table_helper.create_tables("recmedia", items, table_map=table_map, columns=column_headings, table_header=TABLE_HEADER, suppress=True)


## -------------------- PARSER -------------------- ##

def get_recmedia_data():
    if not recmedia_data:
        main()
    return recmedia_data


def find_item_id(media_category):
    for item_id, item_data in item_parser.get_item_data().items():
        if item_data.get("MediaCategory") == media_category:
            return item_id
        
    echo("Warning: Unable to find media category.")
    return "style=\"text-align: center;\" | -"


def translate_rm_strings(data):
    if isinstance(data, dict):
        return {
            key: translate_rm_strings(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [translate_rm_strings(item) for item in data]
    elif isinstance(data, str) and data.startswith("RM_"):
        return translate.get_translation(data).replace('[img=music]', '♪')
    else:
        return data


def organise_lines(data):
    """Changes data from a list of dicts, to a nested dict with the line id ('text') as the key."""
    raw_lines = data.get("lines")
    lines = {}
    for line in raw_lines:
        lines[line.get("text")] = line
    return lines


def parse_rm_data():
    """Parses lua file converting tables to Python."""
    lua_runtime = lua_helper.load_lua_file("recorded_media.lua")
    parsed_data = lua_helper.parse_lua_tables(lua_runtime)["RecMedia"]
#    utility.save_cache(parsed_data, "recorded_media_raw.json")

    return parsed_data


def main():
    global recmedia_data
    parsed_data = parse_rm_data()

    for id, data in parsed_data.items():
        for line in data.get("lines", []):
            if line.get("codes"):
                effects = parse_code_effects(line["codes"])
                line["effects"] = effects
                line.pop("codes")
        data["lines"] = organise_lines(data)
        parsed_data[id] = data

    recmedia_data = translate_rm_strings(parsed_data)
#    utility.save_cache(recmedia_data, "recorded_media.json")

    process_items()


if __name__ == "__main__":
    main()