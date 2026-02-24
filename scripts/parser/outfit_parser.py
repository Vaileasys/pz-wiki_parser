import os
import xml.etree.ElementTree as ET
from scripts.core.file_loading import get_clothing_dir, get_media_dir
from scripts.core import cache
from scripts.utils import echo


def guid_item_mapping(guid_table):
    """Parse the GUID XML table and create a mapping of GUIDs to item names."""
    guid_mapping = {}
    try:
        tree = ET.parse(guid_table)
        root = tree.getroot()
        for file_entry in root.findall("files"):
            path = file_entry.find("path").text
            guid = file_entry.find("guid").text
            filename = os.path.splitext(os.path.basename(path))[0]
            guid_mapping[guid] = filename
    except ET.ParseError as e:
        echo.error(f"Error parsing GUID table XML: {e}")
    return guid_mapping


def parse_outfits(xml_file, guid_mapping):
    """Parse the outfits XML file and return a structured JSON based on GUID mapping."""
    echo.info(f"Parsing outfits from: {xml_file}")
    if not os.path.exists(xml_file):
        echo.error(f"Outfit XML file not found: {xml_file}")
        return {}

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        echo.error(f"Error parsing clothing XML: {e}")
        return {}

    output_json = {"FemaleOutfits": {}, "MaleOutfits": {}}

    # Look for outfit-related elements (case-insensitive search)
    outfit_elements = []
    for elem in root.iter():
        if "outfit" in elem.tag.lower():
            outfit_elements.append(elem.tag)

    for outfit in root.findall(".//m_FemaleOutfits") + root.findall(".//m_MaleOutfits"):
        outfit_type = (
            "FemaleOutfits" if outfit.tag == "m_FemaleOutfits" else "MaleOutfits"
        )
        outfit_name = (
            outfit.find("m_Name").text
            if outfit.find("m_Name") is not None
            else "Unknown Outfit"
        )
        outfit_guid = (
            outfit.find("m_Guid").text
            if outfit.find("m_Guid") is not None
            else "No GUID"
        )

        # Parse all XML parameters
        outfit_params = {}
        for child in outfit:
            if child.tag not in ["m_Name", "m_Guid", "m_items"]:
                # Handle boolean and other parameter types
                if child.text in ["true", "false"]:
                    outfit_params[child.tag] = child.text.lower() == "true"
                else:
                    outfit_params[child.tag] = child.text

        # Parse items with proper main item and sub-item structure
        items_structure = {}

        for item_block in outfit.findall("m_items"):
            probability_tag = item_block.find("probability")
            probability = (
                float(probability_tag.text) * 100
                if probability_tag is not None
                else 100
            )
            probability = int(probability)

            item_guid = (
                item_block.find("itemGUID").text
                if item_block.find("itemGUID") is not None
                else None
            )
            if item_guid:
                item_name = guid_mapping.get(item_guid, item_guid)

                # Initialize main item structure
                items_structure[item_name] = {
                    "probability": probability,
                    "subItems": {},
                }

                # Parse sub-items
                for subitem in item_block.findall(".//subItems/itemGUID"):
                    subitem_guid = subitem.text
                    subitem_name = guid_mapping.get(subitem_guid, subitem_guid)
                    items_structure[item_name]["subItems"][subitem_name] = probability

        if outfit_name:
            output_json[outfit_type][outfit_name] = {
                "GUID": outfit_guid,
                **outfit_params,
                "Items": items_structure,
            }

    return output_json


def get_outfits():
    """
    Get the parsed outfits data from cache, or parse XML files if cache doesn't exist.

    Returns:
        dict: Parsed outfits data with MaleOutfits and FemaleOutfits
    """

    guid_table_path = os.path.join(get_media_dir(), "fileGuidTable.xml")
    outfits_xml_path = os.path.join(get_clothing_dir(), "clothing.xml")

    guid_mapping = guid_item_mapping(guid_table_path)
    outfits_json = parse_outfits(outfits_xml_path, guid_mapping)

    cache.save_cache(outfits_json, "outfits.json")
    return outfits_json


def main():
    get_outfits()
