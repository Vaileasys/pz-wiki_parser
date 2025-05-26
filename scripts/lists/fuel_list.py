import os
from scripts.objects.item import Item
from scripts.core.file_loading import write_file
from scripts.utils.util import convert_int
from scripts.core.constants import ITEM_DIR

def generate_table(data):
    content = []

    for item_type in sorted(data.keys()):
        content.append(f"=={item_type}==")
        content.append(f'<!--BOT_FLAG-start-{item_type}. DO NOT REMOVE--><div class="scroll-x">')
        content.append('{| class="wikitable theme-red sortable" style="text-align: center;"')
        content.append("! Icon")
        content.append("! Name")
        content.append("! [[File:Status_HeavyLoad_32.png|32px|link=|Encumbrance]]")
        content.append("! Burn time")
        content.append("! Tinder")
        content.append("! Item ID")

        for item in data[item_type]:
            content.append("|-")
            content.append("| " + item.get('icon'))
            content.append("| " + item.get('link'))
            content.append("| " + item.get('weight'))
            content.append("| " + item.get('burn_time'))
            content.append("| " + item.get('tinder'))
            content.append("| " + item.get('item_id'))

        content.append("|}")
        content.append(f'</div><!--BOT_FLAG-end-{item_type}. DO NOT REMOVE-->\n')

    return content


def update_item_type(item_type):
    if item_type == "Map":
        return "Literature"
    elif item_type in ("Food", "Drainable", "Normal", "Moveable"):
        return "Miscellaneous"
    return item_type


def generate_data():
    items_data = {}

    for item_id in Item.keys():
        item = Item(item_id)
        if item.get_burn_time():

            item_type = item.get("Type")
            item_type = update_item_type(item_type)

            if item_type not in items_data:
                items_data[item_type] = []
            
            if item.is_tinder:
                tinder = "[[File:UI_Tick.png|link=|Can be used to start a fire]]"
            else:
                tinder = "[[File:UI_Cross.png|link=|Cannot be used to start a fire]]"
            processed_item = {
                "name": item.get_name(),
                "icon": item.get_icon(),
                "link": item.get_link(),
                "weight": str(convert_int(item.get("Weight", 1))),
                "burn_time": item.get_burn_time(),
                "tinder": tinder,
                "item_id": item_id
            }

            items_data[item_type].append(processed_item)

    for item_type in items_data:
        items_data[item_type] = sorted(items_data[item_type], key=lambda x: x["name"] or "")

    return items_data


def main():
    data = generate_data()
    content = generate_table(data)
    root_path = os.path.join(ITEM_DIR, "lists")
    write_file(content, root_path=root_path, rel_path="fuel.txt")

if __name__ == "__main__":
    main()