from scripts.objects.item import Item
from scripts.core.file_loading import write_file

def generate_table(data):
    content = []

    for item_type in sorted(data.keys()):
        content.append(f"=={item_type}==")
        content.append('{| class="wikitable theme-red sortable" style="text-align: center;"')
        content.append("! Icon")
        content.append("! Name")
        content.append("! Burn time")
        content.append("! Item ID")

        for item in data[item_type]:
            content.append("|-")
            content.append("| " + item.get('icon'))
            content.append("| " + item.get('link'))
            content.append("| " + item.get('burn_time'))
            content.append("| " + item.get('item_id'))

        content.append("|}\n")

    return content


def generate_data():
    items_data = {}

    for item_id in Item.keys():
        item = Item(item_id)
        if item.get_burn_time():

            item_type = item.get("Type")

            if item_type not in items_data:
                items_data[item_type] = []

            processed_item = {
                "name": item.get_name(),
                "icon": item.get_icon(),
                "link": item.get_link(),
                "burn_time": item.get_burn_time(),
                "item_id": item_id
            }

            items_data[item_type].append(processed_item)

    for item_type in items_data:
        items_data[item_type] = sorted(items_data[item_type], key=lambda x: x["name"] or "")

    return items_data


def main():
    data = generate_data()
    content = generate_table(data)
    write_file(content)

if __name__ == "__main__":
    main()