from pathlib import Path
from scripts.core import translate, version
from scripts.parser import item_parser
from scripts.core.constants import OUTPUT_PATH
from scripts.utils import utility, lua_helper, util

language_code = translate.get_language_code()
output_dir = Path(OUTPUT_PATH) / language_code.lower()

hotbar_data = {}
# All items from item_parser
all_item_data = {}
# Cache items
attachment_items_def = {
    "AttachmentsProvided": {},
    "AttachmentType": {}
}
attachment_items = {}
# Items that use a slot
attached_item_data = {}
# Items that provide a slot
attachment_item_data = {}
# Hotbar slots with the 'attachments', 'name', 'animset' and 'items'
hotbar_slots = {}
# attachment types with the 'name' and 'items'
attachment_types = {}
# Suppress print statements
_suppress = False


def get_hotbar_slots(suppress=None):
    global _suppress
    if suppress is None:
        suppress = False
    suppress = _suppress

    if not hotbar_slots:
        generate_data()
    return hotbar_slots


def get_attachment_types(suppress=None):
    global _suppress
    if suppress is None:
        suppress = False
    suppress = _suppress

    if not attachment_types:
        generate_data()
    return attachment_types


def get_attachment_items(suppress=None):
    global _suppress
    if suppress is None:
        suppress = False
    suppress = _suppress

    if not attachment_items:
        generate_data()
    return attachment_items


def generate_hotbar_slots():
    global hotbar_slots
    global attachment_types
    global attachment_items
    hotbar_slots = hotbar_data
    for slot, slot_data in hotbar_data.items():
        slot_name = hotbar_slots[slot].get("name")
        if slot_name:
            slot_name = translate.get_translation("IGUI_HotbarAttachment_" + slot, "")
            hotbar_slots[slot]["name"] = slot_name
        hotbar_slots[slot]["items"] = []
        for item_id, item_data in attachment_item_data.items():
            if isinstance(item_data["AttachmentsProvided"], str):
                item_data["AttachmentsProvided"] = [item_data["AttachmentsProvided"]]
            if slot in item_data["AttachmentsProvided"]:
                hotbar_slots[slot]["items"].append(item_id)
                # Get and store item data
                if item_id not in attachment_items["AttachmentsProvided"]:
                    name = utility.get_name(item_id, item_data)
                    page = utility.get_page(item_id, name)
                    icon = utility.get_icon(item_id, True, True, True)
                    new_item_data = {
                        "name": name,
                        "page": page,
                        "icon": icon,
                    }
                    attachment_items["AttachmentsProvided"][item_id] = new_item_data
        # Sort items by 'name'
        attachment_items["AttachmentsProvided"] = dict(sorted(attachment_items["AttachmentsProvided"].items(), key=lambda item: item[1]["name"]))
        
        for attachment, attachment_name in slot_data.get("attachments", {}).items():
            if attachment not in attachment_types:
                attachment_types[attachment] = {}
                attachment_types[attachment]["group"] = attachment_name
                attachment_types[attachment]["items"] = []
                for item_id, item_data in attached_item_data.items():
                    if attachment in item_data.get("AttachmentType"):
                        attachment_types[attachment]["items"].append(item_id)
                        # Get and store item data
                        if item_id not in attachment_items["AttachmentType"]:
                            name = utility.get_name(item_id, item_data)
                            page = utility.get_page(item_id, name)
                            icon = utility.get_icon(item_id, True, True, True)
                            new_item_data = {
                                "name": name,
                                "page": page,
                                "icon": icon,
                            }
                            attachment_items["AttachmentType"][item_id] = new_item_data
        # Sort items by 'name'
        attachment_items["AttachmentType"] = dict(sorted(attachment_items["AttachmentType"].items(), key=lambda item: item[1]["name"]))
        # Sort attachment types by key
        attachment_types = {key: attachment_types[key] for key in sorted(attachment_types)}

    # Sort slots by 'name'
    hotbar_slots = dict(sorted(hotbar_slots.items(), key=lambda item: item[1]["name"]))

    utility.save_cache(attachment_items, "attachment_items.json", suppress=_suppress)
    utility.save_cache(hotbar_slots, "hotbar_slots.json", suppress=_suppress)
    utility.save_cache(attachment_types, "attachment_types.json", suppress=_suppress)


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


def write_attachment_table():
    # Intialise table and add headings
    table = [
        '{| class="wikitable theme-blue sortable"',
        '! style="white-space:nowrap;" | AttachmentType',
        '! style="white-space:nowrap;" | AttachedLocation group',
        '! style="white-space:nowrap;" | Hotbar slots',
        '! style="white-space:nowrap;" | Items',
    ]

    for attachment, attachment_data in attachment_types.items():
        # name
        group = attachment_data.get("group", "-")

        # Items using slot
        slot_items_list = attachment_data.get("items")
        items = []
        if slot_items_list:
            for item_id in slot_items_list:
                item_name = attachment_items["AttachmentType"][item_id]["name"]
                item_page = attachment_items["AttachmentType"][item_id]["page"]
                item_link = util.format_link(item_name, item_page)

                items.append(item_link)

            items = '| ' + " &bull; ".join(items)
        else:
            items = '| style="text-align:center;" | -'
        
        slots = []
        for slot, slot_data in hotbar_slots.items():
            slot_attachments = slot_data.get("attachments", {})
            if attachment in slot_attachments:
                slot = f"[[AttachmentsProvided#{slot}|{slot}]]"
                slots.append(slot)
        slots = "<br>".join(slots)

        slot_row = [
            f'|- id="{attachment}"',
            '| ' + attachment,
            '| style="white-space:nowrap;" | ' + group,
            '| ' + slots,
            items
        ]
        table.append("\n".join(slot_row))

    # Close table
    table.append("|}")

    # Write table
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = "attachment_table.txt"
    output_path = output_dir / output_file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(table))
    if not _suppress:
        print(f"File saved to {output_path}")


def write_hotbar_table():
    # Intialise table and add headings
    table = [
        '{| class="wikitable theme-blue sortable"',
        '! style="white-space:nowrap;" | type',
        '! style="white-space:nowrap;" | name',
        '! style="white-space:nowrap;" | animset',
        '! style="white-space:nowrap;" | attachments',
        '! style="white-space:nowrap;" | Items',
    ]

    for slot, slot_data in hotbar_slots.items():
        if not slot_data.get("attachments"):
            continue
        
        # name
        name = slot_data.get("name", "-")

        # animset
        animset = slot_data.get("animset", "-")
        
        # attachments
        attachments_list = list(slot_data.get("attachments", {}).keys())
        new_attachments_list = []
        for attachment in attachments_list:
            attachment = f"[[AttachmentType#{attachment}|{attachment}]]"
            new_attachments_list.append(attachment)
        if new_attachments_list:
            attachments = '| ' + "<br>".join(new_attachments_list)
        else:
            attachments = '| style="text-align:center;" | -'
        
        # Items with slot
        slot_items_list = slot_data.get("items")
        items = []
        if slot_items_list:
            for item_id in slot_items_list:
                item_name = attachment_items["AttachmentsProvided"][item_id]["name"]
                item_page = attachment_items["AttachmentsProvided"][item_id]["page"]
                item_link = util.format_link(item_name, item_page)
                item_icon = attachment_items["AttachmentsProvided"][item_id]["icon"]

                items.append(f"{item_icon} {item_link}")
            items = '| style="white-space:nowrap;" | ' + "<br>".join(items)
        else:
            items = '| style="text-align:center;" | -'

        slot_row = [
            f'|- id="{slot}"',
            '| ' + slot,
            '| ' + name,
            '| ' + animset,
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
    if not _suppress:
        print(f"File saved to {output_path}")


def clean_attached_locations_data(data):
    """ Clean data parsed from AttachedLocations.lua """
    # Remove keys with lua function values
    if isinstance(data, dict):
        keys_to_pop = [key for key, value in data.items() if isinstance(value, str) and value.startswith("<Lua function")]
        for key in keys_to_pop:
            data.pop(key)
        for value in data.values():
            clean_attached_locations_data(value)
    elif isinstance(data, list):
        for item in data:
            clean_attached_locations_data(item)
    
    # Removed "AttachedLocations" and "groups" keys
    if isinstance(data, dict) and "AttachedLocations" in data:
        attached_locations = data.pop("AttachedLocations")
        if isinstance(attached_locations, dict) and "groups" in attached_locations:
            groups = attached_locations.pop("groups")
            if isinstance(groups, dict):
                data.update(groups)

    return data


def parse_data():
    # Parse ISHotbarAttachDefinition
    global hotbar_data
    global all_item_data
    all_item_data = item_parser.get_item_data()
    lua_runtime = lua_helper.load_lua_file("ISHotbarAttachDefinition.lua")
    hotbar_data = lua_helper.parse_lua_tables(lua_runtime)

    hotbar_data = clean_hotbar_data()

    LUA_ATTACHED_LOCATIONS = ("""
        getDebug = function() return false end

        AttachedLocations = AttachedLocations or {
            groups = {},
            getGroup = function(groupName)
                AttachedLocations.groups[groupName] = AttachedLocations.groups[groupName] or {
                    locations = {},
                    getOrCreateLocation = function(self, locationName)
                        self.locations[locationName] = self.locations[locationName] or {
                            setAttachmentName = function(_, attachmentName)
                                self.locations[locationName] = attachmentName
                            end
                        }
                        return self.locations[locationName]
                    end
                }
                return AttachedLocations.groups[groupName]
            end
        }
    """)
#    lua_runtime = lua_helper.load_lua_file("AttachedLocations.lua", inject_lua=LUA_ATTACHED_LOCATIONS)
#    attached_locations_data = lua_helper.parse_lua_tables(lua_runtime)
#    clean_attached_locations_data(attached_locations_data)
#    utility.save_cache(attached_locations_data, "attached_locations.json", suppress=_suppress)


def generate_data():
    """Generates data by parsing data and modifying it."""
    # Separated from main() so we can get data without generating an output
    global hotbar_slots
    global attachment_types
    global attachment_items

    game_version = version.get_version()
    
    hotbar_slots, hotbar_slots_version = utility.load_cache("hotbar_slots.json", "hotbar slots", get_version=True)
    attachment_types, attachment_types_version = utility.load_cache("attachment_types.json", "attachment types", get_version=True)
    attachment_items, attachment_items_version = utility.load_cache("attachment_items.json", "attachment types", get_version=True)

    if (hotbar_slots_version != game_version or 
        attachment_types_version != game_version or 
        attachment_items_version != game_version or
        hotbar_slots_version == {} or 
        attachment_types_version == {} or 
        attachment_items_version == {}):

        hotbar_slots = {}
        attachment_types = {}
        attachment_items = attachment_items_def

        parse_data()
        get_items()
        generate_hotbar_slots()


def main():
    generate_data()
    write_hotbar_table()
    write_attachment_table()


if __name__ == "__main__":
    main()