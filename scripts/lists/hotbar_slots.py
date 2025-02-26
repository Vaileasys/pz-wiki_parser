from pathlib import Path
from scripts.core import lua_helper, utility, translate
from scripts.parser import item_parser
from scripts.core.constants import OUTPUT_PATH

language_code = translate.get_language_code()
output_dir = Path(OUTPUT_PATH) / language_code.lower()

hotbar_data = {}
all_item_data = {}
# Items that use a slot
attached_item_data = {}
# Items that provide a slot
attachment_item_data = {}
# Hotbar slots with the 'attachments', 'name', 'animset' and 'items'
hotbar_slots = {}
# attachment types with the 'name' and 'items'
attachment_types = {}


def generate_hotbar_slots():
    global hotbar_slots
    global attachment_types
    hotbar_slots = hotbar_data
    for slot, slot_data in hotbar_data.items():
        hotbar_slots[slot]["items"] = []
        for item_id, item_data in attachment_item_data.items():
            if slot in item_data.get("AttachmentsProvided"):
                hotbar_slots[slot]["items"].append(item_id)

        for attachment, attachment_name in slot_data.get("attachments", {}).items():
            
            if attachment not in attachment_types:
                attachment_types[attachment] = {}
                attachment_types[attachment]["name"] = attachment_name

                attachment_types[attachment]["items"] = []
                for item_id, item_data in attached_item_data.items():
                    if attachment in item_data.get("AttachmentType"):
                        attachment_types[attachment]["items"].append(item_id)

    utility.save_cache(hotbar_slots, "hotbar_slots.json")        
    utility.save_cache(attachment_types, "attachment_types.json")


def clean_hotbar_data():
    """Cleans up the hotbar data making its structure consistent."""
    global hotbar_data
    hotbar_data = hotbar_data.get("ISHotbarAttachDefinition", {})

    # Remove 'replacements' key and promote its contents
    if isinstance(hotbar_data.get("replacements"), list):
        replacements = hotbar_data.pop("replacements")

        for item in replacements:
            if isinstance(item, dict) and "type" in item:
                new_key = item.pop("type")
                hotbar_data[new_key] = item

    new_hotbar_data = {}
    # Change the key to 'type' and remove 'type' from the value
    for key, value in hotbar_data.items():
        new_key = value.get("type", key)
        if "type" in value:
            value.pop("type")
        
        new_hotbar_data[new_key] = value

    return new_hotbar_data


def get_items():
    """Modifies item data to include only items that have AttachmentType and AttachmentsProvided"""
    global attached_item_data
    global attachment_item_data

    for item_id, item_data in all_item_data.items():
        # Item has 'AttachmentType'
        if item_data.get("AttachmentType"):
            attached_item_data[item_id] = item_data

        # Item has 'AttachmentsProvided'
        if item_data.get("AttachmentsProvided"):
            attachment_item_data[item_id] = item_data


def write_table():
    # Intialise table and add headings
    table = [
        '{| class="wikitable theme-blue sortable"',
        '! name',
        '! type',
        '! animset',
        '! attachments',
        '! Items',
    ]

    for slot, slot_data in hotbar_slots.items():
        if not slot_data.get("attachments"):
            continue
        
        # name
        name = slot_data.get("name", "-")

        # animset
        animset = slot_data.get("animset", "-")
        
        # Attachment type
        attachments_list = list(slot_data.get("attachments", {}).keys())
        if attachments_list:
            attachments = "| " + "<br>".join(attachments_list)
        else:
            attachments = '| style="text-align:center;" | -'
        
        # Items with slot
        slot_items_list = slot_data.get("items")
        items = []
        if slot_items_list:
            for item_id in slot_items_list:
                item_name = utility.get_name(item_id)
                item_page = utility.get_page(item_id, item_name)
                item_link = utility.format_link(item_name, item_page)
                item_icon = utility.get_icon(item_id, True, True, True)

                items.append(f"{item_icon} {item_link}")
            items = '| style="white-space:nowrap;" | ' + "<br>".join(items)
        else:
            items = '| style="text-align:center;" | -'


        slot_row = [
            "|-",
            "| " + name,
            "| " + slot,
            "| " + animset,
            attachments,
            items
        ]
        table.append("\n".join(slot_row))
    
    # Close table
    table.append("|}")

    # Write table
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = "hotbar_table.txt"
    output_path = output_dir / output_file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(table))
    print(f"File saved to {output_path}")


def main():
    # Parse ISHotbarAttachDefnition
    global hotbar_data
    global all_item_data
    all_item_data = item_parser.get_item_data()
    lua_runtime = lua_helper.load_lua_file("ISHotbarAttachDefinition.lua")
    hotbar_data = lua_helper.parse_lua_tables(lua_runtime)

    hotbar_data = clean_hotbar_data()
    get_items()
    generate_hotbar_slots()
    utility.save_cache(hotbar_data, "hotbar_attach_definitions.json")
    write_table()


if __name__ == "__main__":
    main()