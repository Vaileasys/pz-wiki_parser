from scripts.parser import item_parser
from scripts.utils.utility import find_icon

data = item_parser.get_item_data()

lines = ["Icons = {"]
for item_id in list(data.keys()):
    icons = find_icon(item_id, all_icons=True)
    lua_list = "{" + ", ".join(f'"{icon}"' for icon in icons) + "}"
    lines.append(f'    ["{item_id}"] = {lua_list},')

lines.append("}")

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))