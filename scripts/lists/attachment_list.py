"""
Generates wikitable output for the modding pages `AttachmentType` and `AttachmentsProvided`
on the PZwiki.

This script extracts data from hotbar slot definitions and attachment types,
formats it into MediaWiki tables, and writes them to output files.
"""

from scripts.objects.attachment import HotbarSlot, AttachmentType
from scripts.objects.item import Item
from scripts.core.file_loading import write_file
from scripts.core.constants import BOT_FLAG, BOT_FLAG_END

def build_hotbar_table():
    """
    Write table for `AttachmentsProvided` using hotbar slot data.
    Skips slots with replacements.
    """
    flag_type = "table"
    flag_id = "AttachmentsProvided"

    content = []
    content.append(BOT_FLAG.format(type=flag_type, id=flag_id))
    content.extend([
        '{| class="wikitable theme-blue sortable"',
        '! type',
        '! name',
        '! animset',
        '! attachments',
        '! Items'
    ])
    slots = HotbarSlot.all()
    for slot_id, slot in sorted(slots.items(), key=lambda x: x[1].slot_id.lower()):

        if slot.replacement:
            continue

        attachments = []
        for attachment_id in slot.attachments:
            attachment = AttachmentType(attachment_id)
            attachments.append(attachment.wiki_link_id)
        
        items = []
        for item_id in slot.items.provided:
            item = Item(item_id)
            items.append(f"{item.icon} {item.wiki_link}")
        
        center = 'style="text-align:center;"'

        content.extend([
            f'|- id="{slot_id}"',
            f'| {slot_id}',
            f'| {slot.name}',
            f'| {slot.animset}',
            f'| {"<br>".join(attachments) if attachments else f"{center} | -"}',
            f'| {"<br>".join(items) if items else f"{center} | -"}'
        ])
    content.append('|}')
    content.append(BOT_FLAG_END.format(type=flag_type, id=flag_id))

    write_file(content, rel_path="hotbar_table.txt")

def build_attachment_table():
    """Write table for `AttachmentType` with `AttachedLocation`, hotbar slots, and item icons."""
    flag_type = "table"
    flag_id = "AttachmentType"

    content = []
    content.append(BOT_FLAG.format(type=flag_type, id=flag_id))
    content.extend([
        '{| class="wikitable theme-blue sortable"',
        '! AttachmentType',
        '! style="white-space: nowrap;" | AttachedLocation group',
        '! style="white-space: nowrap;" | Hotbar slots',
        '! Items',
    ])
    attachments = AttachmentType.all()
    for attachment_id, attachment in sorted(attachments.items(), key=lambda x: x[1].attachment_id.lower()):

        hotbar_slots = []
        for slot_id in attachment.slots:
            hotbar_slots.append(HotbarSlot(slot_id).wiki_link_id)

        items = []
        for item_id in attachment.items:
            items.append(Item(item_id).icon)

        center = 'style="text-align:center;"'

        content.extend([
            f'|- id="{attachment_id}"',
            f'| {attachment_id}',
            f'| {attachment.name}',
            f'| {"<br>".join(hotbar_slots) if hotbar_slots else f"{center} | -"}',
            f'| {"".join(items) if items else f"{center} | -"}'
        ])
    content.append('|}')
    content.append(BOT_FLAG_END.format(type=flag_type, id=flag_id))

    write_file(content, rel_path="attachment_table.txt")


def main():
    """Run both hotbar and attachment table builders."""
    build_hotbar_table()
    build_attachment_table()
    


if __name__ == "__main__":
    main()