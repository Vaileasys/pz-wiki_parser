#!/usr/bin/env python3
"""
Project Zomboid Wiki Crafting Recipe Processor

This script processes crafting recipes from Project Zomboid, converting them into
wiki-ready format. It handles both standard crafting recipes and building recipes,
with support for various recipe components and special cases.

The script handles:
- Fluid processing with RGB color values
- Ingredient processing with quantities
- Tool requirements and workstations
- Product outputs and mappers
- Experience gains and skill requirements
- Recipe learning methods
- Item and skill usage documentation
- Lua table generation for templates
"""

import os, json, re
from tqdm import tqdm
from collections import defaultdict
from scripts.core.constants import PBAR_FORMAT, DATA_DIR
from scripts.core.language import Language, Translate
from scripts.core.version import Version
from scripts.core.cache import load_cache
from scripts.parser.script_parser import extract_script_data
from scripts.parser import literature_parser, fluid_parser
from scripts.parser.item_parser import get_item_data
from scripts.utils import utility, util
from scripts.utils import echo
from scripts.items import item_tags

# Cache for unit tool IDs to avoid repeated computation
_unit_tool_ids_cache = None

def get_unit_tool_ids() -> list[str]:
    """
    Get list of item IDs that should be treated as unit tools.
    Finds all items with Type "Drainable" from the item data cache.
    
    Returns:
        list[str]: List of item IDs that are unit tools (drainable items)
    """
    global _unit_tool_ids_cache
    
    if _unit_tool_ids_cache is not None:
        return _unit_tool_ids_cache
        
    item_data = get_item_data()
    unit_tool_ids = []
    
    for item_id, item_info in item_data.items():
        if item_info.get("Type") == "Drainable":
            unit_tool_ids.append(item_id)
    
    _unit_tool_ids_cache = unit_tool_ids
    return unit_tool_ids

def get_use_delta(item_id: str, item_data: dict) -> float:
    """
    Get the UseDelta value for a unit tool item.
    
    Args:
        item_id (str): The item ID to look up
        item_data (dict): Dictionary of parsed item data
        
    Returns:
        float: The UseDelta value as a float, or 0.1 as default if not found
    """
    if not item_id.startswith("Base."):
        item_id = f"Base.{item_id}"
        
    item_info = item_data.get(item_id, {})
    use_delta = item_info.get("UseDelta")
    
    try:
        return float(use_delta) if use_delta else 0.1
    except (ValueError, TypeError):
        return 0.1


def fluid_rgb(fluid_id):
    """
    Get RGB color values for a fluid type.

    Args:
        fluid_id (str): Fluid identifier, can be in form 'categories[Water]'.

    Returns:
        dict: Dictionary containing:
            - name: Display name of the fluid
            - R: Red color value (0-255)
            - G: Green color value (0-255)
            - B: Blue color value (0-255)

    Raises:
        RuntimeError: If there's an error processing the fluid.

    Handles:
    - Category-based fluid IDs
    - Color reference lookups
    - Tainted water special case
    - RGB value normalization
    """
    try:
        # Handle fluid 'categories'
        if isinstance(fluid_id, str):
            match = re.match(r'categories\[(.+?)\]', fluid_id)
            if match:
                fluid_id = match.group(1)

        fluid_metadata = fluid_parser.get_fluid_data().get(fluid_id)
        if not fluid_metadata:
            raise ValueError(f"No fluid found for ID: {fluid_id}")

        with open(os.path.join("resources", "color_reference.json"), "r") as color_reference_file:
            color_reference_data = json.load(color_reference_file)

        fluid_name = utility.get_fluid_name(fluid_metadata)
        if fluid_id == "TaintedWater":
            translated_label = Translate.get("ItemNameTaintedWater", "IGUI")
            fluid_name = translated_label.replace("%1", fluid_name)

        color_reference_key = fluid_metadata.get("ColorReference")
        numeric_rgb_color = fluid_metadata.get("Color", [0.0, 0.0, 0.0])

        if color_reference_key:
            if isinstance(color_reference_key, str):
                rgb_values = color_reference_data["colors"].get(color_reference_key, [0.0, 0.0, 0.0])
            elif isinstance(color_reference_key, list) and len(color_reference_key) == 1 and isinstance(color_reference_key[0], str):
                rgb_values = color_reference_data["colors"].get(color_reference_key[0], [0.0, 0.0, 0.0])
            else:
                rgb_values = numeric_rgb_color
        else:
            rgb_values = numeric_rgb_color

        red_value   = int(float(rgb_values[0]) * 255)
        green_value = int(float(rgb_values[1]) * 255)
        blue_value  = int(float(rgb_values[2]) * 255)

        return {
            "name": fluid_name,
            "R":    red_value,
            "G":    green_value,
            "B":    blue_value
        }

    except Exception as error:
        raise RuntimeError(f"Error processing fluid '{fluid_id}': {error}")


def process_ingredients(recipe: dict, build_data: dict) -> str:
    """
    Process recipe ingredients into wiki markup.

    Args:
        recipe (dict): Recipe data containing ingredients.
        build_data (dict): Additional building recipe data.

    Returns:
        str: Wiki markup for ingredients section.

    Handles:
    - Energy inputs
    - Fluid ingredients with colors
    - Numbered list ingredients
    - Tag-based ingredients
    - Simple item ingredients
    - Proper grouping of "One of" vs "Each of" items
    - Icon integration
    - Unit items with Unit bar template
    """
    input_list = recipe.get("inputs")
    if not isinstance(input_list, list):
        return "''none''"

    # Load item data for UseDelta lookup
    item_data = get_item_data()
    unit_tool_ids = get_unit_tool_ids()
    
    parsed_ingredients = {"ingredients": {}}
    ingredient_counter = 0
    EXCLUDED_ITEM_IDS = {"Base.bobOmb"}

    def safe_name_lookup(item_id: str) -> str:
        if item_id == "Any fluid container":
            return item_id
        try:
            return utility.get_name(item_id)
        except Exception:
            return item_id

    for input_index, input_entry in enumerate(input_list, start=1):
        if any("mapper" in str(value).lower() for value in input_entry.values()):
            continue
        if input_entry.get("mode") == "Keep" and "fluidModifier" not in input_entry:
            continue

        quantity = input_entry.get("count",
                     input_entry.get("amount",
                     input_entry.get("index", 1)))

        ingredient_counter += 1
        key = f"ingredient{ingredient_counter}"
        info: dict = {}

        # Energy
        if input_entry.get("energy"):
            info["energy"] = True
            info["amount"] = quantity
            info["type"] = input_entry.get("type", "")

        # Fluid
        elif "fluidModifier" in input_entry:
            fm = input_entry["fluidModifier"]
            info["fluid"] = True
            info["amount"] = fm.get("amount", quantity)
            info["fluidType"] = fm.get("fluidType", [])
            info["items"] = [
                {"raw": i, "translated": safe_name_lookup(i)}
                for i in input_entry.get("items", [])
            ]

        # Numbered lists
        elif isinstance(input_entry.get("items"), list):
            items = input_entry["items"]
            if all(isinstance(c, str) and ":" in c for c in items):
                parsed = []
                for entry in items:
                    amt_str, rid = entry.split(":",1)
                    try:
                        amt = int(amt_str.strip().split(".")[-1])
                    except:
                        amt = 1
                    rid = rid.strip()
                    if not rid.startswith("Base."):
                        rid = f"Base.{rid}"
                    parsed.append({
                        "raw": rid,
                        "amount": amt,
                        "translated": safe_name_lookup(rid),
                        "is_unit": rid in unit_tool_ids
                    })
                info["numbered_list"] = True
                info["items"] = parsed

        # Structured dict‑list
        if not info and isinstance(input_entry.get("items"), list) \
           and input_entry["items"] \
           and isinstance(input_entry["items"][0], dict):
            struct = input_entry["items"]
            parsed = []
            for ent in struct:
                rid = ent.get("raw_name") or ent.get("raw") or ent.get("item_id","")
                if not rid.startswith("Base."):
                    rid = f"Base.{rid}"
                parsed.append({
                    "raw": rid,
                    "amount": ent.get("amount", quantity),
                    "translated": safe_name_lookup(rid),
                    "is_unit": rid in unit_tool_ids
                })
            info["numbered_list"] = True
            info["items"] = parsed

        # Tags
        if not info and "tags" in input_entry:
            info["tags"] = input_entry["tags"]
            info["amount"] = quantity

        # Simple items
        if not info and "items" in input_entry:
            valid = [c for c in input_entry["items"]
                     if isinstance(c, str) and c not in EXCLUDED_ITEM_IDS]
            
            if valid:
                info["items"] = [
                    {
                        "raw": c, 
                        "translated": safe_name_lookup(c),
                        "is_unit": c in unit_tool_ids
                    }
                    for c in valid
                ]
                info["amount"] = quantity
            else:
                # Skip if no valid items
                continue

        if not info:
            echo.error(f"Unhandled ingredient #{input_index}: {input_entry}")
        
        # Only add to parsed ingredients if we have actual content
        if info:
            parsed_ingredients["ingredients"][key] = info

    # Build string
    formatted = []
    for data in parsed_ingredients["ingredients"].values():
        # Skip empty data entries
        if not data:
            continue
            
        # tags
        if "tags" in data:
            lines = []
            qty = data.get("amount", 1)
            for tag in data["tags"]:
                span = open(os.path.join("output", "en", "tags", "cycle-img", f"{tag}.txt"), "r").read()
                lines.append(f"{span} [[{tag} (tag)]] <small>×{qty}</small>")
            formatted.append(("tag", "<br>".join(lines), "Each of"))

        # Fluids
        elif data.get("fluid"):
            lines = []
            vol = data.get("amount",1)
            for fid in data["fluidType"]:
                cd = fluid_rgb(fid)
                rgb = f"{{{{rgb|{cd['R']},{cd['G']},{cd['B']}}}}}"
                lines.append(f"{rgb} [[{cd['name']} (fluid)|{cd['name']}]] <small>×{int(vol*1000)}mL</small>")
            desc = "One of" if len(data["fluidType"])>1 else "Each of"
            formatted.append(("fluid","<br>".join(lines),desc))

        # Numbered_lists
        elif data.get("numbered_list"):
            lines = []
            for itm in data["items"]:
                icon = utility.get_icon(itm["raw"])
                link = util.link(utility.get_page(itm["raw"], itm["translated"]), itm["translated"])
                if itm.get("is_unit"):
                    # Handle unit items with Unit bar
                    use_delta = get_use_delta(itm["raw"], item_data)
                    unit_bar = f"{{{{#invoke:Unit bar|main|{itm['amount']}|{use_delta}}}}}"

                    lines.append(f"[[File:{icon}|32x32px|class=pixelart]] {link} <br>{unit_bar}")
                else:
                    # Regular items
                    lines.append(f"[[File:{icon}|32x32px|class=pixelart]] {link} <small>×{itm['amount']}</small>")
            formatted.append(("item","<br>".join(lines),"One of"))

        # Simple items
        elif data.get("items"):
            lines = []
            qty = data.get("amount",1)
            for itm in data["items"]:
                icon = utility.get_icon(itm["raw"])
                link = util.link(utility.get_page(itm["raw"], itm["translated"]), itm["translated"])
                if itm.get("is_unit"):
                    # Handle unit items with Unit bar
                    use_delta = get_use_delta(itm["raw"], item_data)
                    unit_bar = f"{{{{#invoke:Unit bar|main|{qty}|{use_delta}}}}}"
                    lines.append(f"[[File:{icon}|32x32px|class=pixelart]] {link} <br>{unit_bar}")
                else:
                    # Regular items
                    lines.append(f"[[File:{icon}|32x32px|class=pixelart]] {link} <small>×{qty}</small>")
            desc = "One of" if len(data["items"])>1 else "Each of"
            formatted.append(("item","<br>".join(lines),desc))

        else:
            formatted.append(("item","Unknown Ingredient","One of"))

    if not formatted:
        return "''none''"

    # Assemble groups
    output = [""]
    last_desc = None

    for _, html, desc in formatted:
        need_heading = (desc == "One of") or (desc != last_desc)
        if need_heading:
            if last_desc is not None:
                output.append("<br>")
            output.append(f"<small>{desc}:</small><br>")
        else:
            output.append("<br>")

        output.append(html)
        last_desc = desc

    return "".join(output)


def process_tools(recipe: dict, build_data: dict) -> str:
    """
    Process tool requirements into wiki markup.

    Args:
        recipe (dict): Recipe data containing tool requirements.
        build_data (dict): Additional building recipe data.

    Returns:
        str: Wiki markup for tools section.

    Handles:
    - Individual tool requirements
    - Tool tag groups
    - Tool condition flags
    - Icon integration
    - Proper grouping of requirements
    - Unit items with Unit bar template
    """
    FLAG_MAP = {
        'IsDamaged':       "damaged",
        'IsNotDull':       "not dull",
        'MayDegrade':      "may degrade",
        'MayDegradeHeavy': "may degrade",
        'MayDegradeLight': "may degrade",
        'NoBrokenItems':   "not broken",
    }
    EXCLUDED = {"Base.bobOmb"}

    groups: list[tuple[str, list[str]]] = []
    
    # Load item data for UseDelta lookup
    item_data = get_item_data()
    unit_tool_ids = get_unit_tool_ids()

    # Process tools
    for inp in recipe.get("inputs", []):
        if inp.get("mode") != "Keep" \
           or "fluidModifier" in inp \
           or any("mapper" in str(v).lower() for v in inp.values()):
            continue

        lines: list[str] = []
        count = inp.get("count", 1)  # Get the count for this input

        # Tags
        if "tags" in inp:
            for tag in inp["tags"]:
                span = open(os.path.join("output", "en", "tags", "cycle-img", f"{tag}.txt"), encoding="utf-8").read()
                lines.append(f"{span} [[{tag} (tag)]] <small>×{count}</small>")

        # Items
        elif "items" in inp:
            for rid in inp["items"]:
                if rid in EXCLUDED or rid.startswith("Base.*"):
                    continue
                    
                name = utility.get_name(rid)
                page = utility.get_page(rid, name)
                icon = utility.get_icon(rid)
                
                # Check if this is a unit tool
                if rid in unit_tool_ids:
                    use_delta = get_use_delta(rid, item_data)
                    unit_bar = f"{{{{#invoke:Unit bar|main|{count}|{use_delta}}}}}"
                    lines.append(f"[[File:{icon}|32x32px|class=pixelart]] {util.link(page, name)} <br>{unit_bar}")
                else:
                    lines.append(f"[[File:{icon}|32x32px|class=pixelart]] {util.link(page, name)} <small>×{count}</small>")

        if not lines:
            continue

        # One flag per tool ingredient
        raw_flags = inp.get("flags", [])
        mapped    = [FLAG_MAP[f] for f in raw_flags if f in FLAG_MAP]
        if mapped:
            lines.append(f"<span style='color:var(--color-pz-subtle)'>({', '.join(dict.fromkeys(mapped))})</span>")

        desc = "One of" if len(lines) - bool(mapped) > 1 else "Each of"
        groups.append((desc, lines))

    if not groups:
        return "''none''"

    # Handle each of
    out, last = [""], None
    
    # Process tools
    for desc, lines in groups:
        if desc == "One of" or desc != last:
            if last is not None:
                out.append("<br>")
            out.append(f"<small>{desc}:</small><br>")
            last = desc
        else:
            out.append("<br>")
        out.append("<br>".join(lines))

    return "".join(out)


def process_workstation(recipe: dict, build_data: dict) -> str:
    """
    Process workstation requirements into wiki markup.

    Args:
        recipe (dict): Recipe data containing workstation info.
        build_data (dict): Additional building recipe data.

    Returns:
        str: Wiki markup for workstation section.

    Handles:
    - Required crafting stations
    - Special location requirements
    - Building-specific workstations
    """
    tag_list = recipe.get("tags")
    if not tag_list:
        return "''none''"

    workstation_mapping = {
        "anysurfacecraft": "Any surface",
        "choppingblock": "Chopping Block",
        "coffeemachine": "Coffee Machine",
        "grindstone": "Grindstone",
        "grinding_slab": "Grinding Slab",
        "weaving": "Simple Loom",
        "stone_mill": "Stone Mill",
        "stone_quern": "Stone Quern",
        "churnbucket": "Butter Churn",
        "dryleatherlarge": "Leather Drying Rack (Large)",
        "dryleathermedium": "Leather Drying Rack (Medium)",
        "dryleathersmall": "Leather Drying Rack (Small)",
        "tanleather": "Tanning Barrel",
        "advancedforge": "Advanced Forge",
        "dryingrackgrain": "Large Plant Drying Rack",
        "dryingrackherb": "Small Plant Drying Rack",
        "forge": "Forge",
        "primitivefurnace": "Primitive Furnace",
        "furnace": "Furnace",
        "advancedfurnace": "Advanced Furnace",
        "metalbandsaw": "Metal Bandsaw",
        "potterywheel": "Pottery Wheel",
        "potterybench": "Pottery Bench",
        "primitiveforge": "Primitive Forge",
        "removeflesh": "Softening Beam",
        "removefur": "Softening Beam",
        "spinningwheel": "Spinning Wheel",
        "standingdrillpress": "Standing Drill Press",
        "whetstone": "Whetstone",
        "toaster": "Toaster",
        "handpress": "Hand Press",
        "domekiln": "Kiln - Dome",
        "kilnlarge": "Advanced Kiln",
        "kilnsmall": "Primitive Kiln",
        "heckling": "Heckle Comb",
        "rippling": "Ripple Comb",
        "scutching": "Scutching Board",
    }

    for tag_identifier in tag_list:
        workstation_name = workstation_mapping.get(tag_identifier.lower())
        if workstation_name:
            return f"[[{workstation_name}]]"

    return "''none''"


def process_output_mapper(recipe: dict, mapper_key: str) -> list[str]:
    """
    Process output mapper strings into item lists.

    Args:
        recipe (dict): Recipe data containing mappers.
        mapper_key (str): Key for the mapper to process.

    Returns:
        list[str]: List of mapped item IDs.

    Handles:
    - Mapper resolution
    - Item ID normalization
    - Multiple mapper types
    """
    item_mappers = recipe.get("itemMappers", {})
    mapper_data = item_mappers.get(mapper_key)
    if not mapper_data or not isinstance(mapper_data, dict):
        echo.warning(f"Mapper '{mapper_key}' not found or invalid in recipe '{recipe.get('name')}'")
        return []

    # Look for the count on the matching output entry; default to 1
    output_amount = 1
    for out in recipe.get("outputs", []):
        if out.get("mapper") == mapper_key:
            output_amount = out.get("count", 1)
            break

    formatted_lines: list[str] = []
    for raw_output_key in mapper_data.keys():
        if raw_output_key.lower() == "default":
            continue

        icon_filename = utility.get_icon(raw_output_key)
        if isinstance(icon_filename, list):
            icon_filename = icon_filename[0] if icon_filename else "Question On.png"

        item_name = utility.get_name(raw_output_key)
        page_url = utility.get_page(raw_output_key, item_name)
        link_html = util.link(page_url, item_name)

        formatted_lines.append(
            f"[[File:{icon_filename}|64x64px|class=pixelart]]<br>{link_html} ×{output_amount}"
        )

    return formatted_lines


def process_products(recipe: dict, build_data: dict) -> str:
    """
    Process recipe products into wiki markup.

    Args:
        recipe (dict): Recipe data containing products.
        build_data (dict): Additional building recipe data.

    Returns:
        str: Wiki markup for products section.

    Handles:
    - Standard product outputs
    - Building recipe outputs
    - Fluid outputs with colors
    - Icon integration
    - Amount formatting
    """
    is_building = "spriteOutputs" in recipe

    first_out = next(iter(recipe.get("outputs", [])), {})
    raw_label = first_out.get("displayName", "")
    raw_name = recipe.get("name", "")
    base_label = raw_label or raw_name

    for key in (base_label.replace(" ", ""),
                base_label.replace(" ", "_")):

        product_name = Translate.get(key)
        if product_name and product_name != key:  # found a real translation?
            break
    else:  # ran through both keys
        product_name = raw_label or raw_name  # final local fallback

    display_name = product_name.replace("_", " ")

    recipe_name = Translate.get(raw_name)
    products_markup = f"products=<small>''{recipe_name}''</small><br>"

    display_name = display_name.replace("Construct ", "")

    if is_building:
        outputs = recipe.get("outputs", [])

        # find first sprite fallback
        sprites = recipe.get("spriteOutputs", {})
        first_sprite = None
        for direction, sprite_list in sprites.items():
            if isinstance(sprite_list, list) and sprite_list:
                first_sprite = sprite_list[0]
                break

        built_entries: list[str] = []
        if outputs:
            for out in outputs:
                icon_ref = out.get("icon")
                label = out.get("displayName", product_name)
                count = out.get("count", 1)

                if icon_ref:
                    img, size = icon_ref, "64x128px"
                    if icon_ref.startswith("Item_"):
                        img = icon_ref[len("Item_"):]
                        size = "64x64px"
                    elif icon_ref.startswith("Build_"):
                        size = "96x96px"
                    built_entries.append(
                        f"[[File:{img}.png|{size}|class=pixelart]]<br>[[{product_name}]] ×{count}"
                    )
                elif first_sprite:
                    sp, size = first_sprite, "64x128px"
                    if first_sprite.startswith("Item_"):
                        sp = first_sprite[len("Item_"):]
                        size = "64x64px"
                    elif first_sprite.startswith("Build_"):
                        size = "96x96px"
                    built_entries.append(
                        f"[[File:{sp}.png|{size}|class=pixelart]]<br>[[{product_name}]] ×{count}"
                    )
        elif first_sprite:
            sp, size = first_sprite, "64x128px"
            if first_sprite.startswith("Item_"):
                sp = first_sprite[len("Item_"):]
                size = "64x64px"
            elif first_sprite.startswith("Build_"):
                size = "96x96px"
            built_entries.append(
                f"[[File:{sp}.png|{size}|class=pixelart]]<br>[[{display_name}]] ×1"
            )

        if not built_entries:
            return products_markup + "''none''"

        if len(built_entries) == 1:
            products_markup += built_entries[0]
        else:
            products_markup += "<small>Each of:</small><br>" + "<br>".join(built_entries)

        return products_markup

    # Crafting
    output_list = recipe.get("outputs", [])
    item_lines:    list[str] = []
    mapper_lines:  list[str] = []
    fluid_lines:   list[str] = []
    energy_lines:  list[str] = []

    for out in output_list:
        # Energy
        if out.get("energy"):
            typ = out.get("type", "Unknown")
            amt = out.get("amount", 0)
            energy_lines.append(f"[[{typ} energy]] ×{amt}")
            continue

        # Mapper‑dependent products
        if "mapper" in out:
            ml = process_output_mapper(recipe, out["mapper"])
            mapper_lines.extend(ml)
            continue

        # Fluid
        fm = out.get("fluidModifier")
        if fm:
            vol = fm.get("amount", 1)
            for fid in fm.get("fluidType", []):
                cd = fluid_rgb(fid)
                rgb = f"{{{{rgb|{cd['R']}, {cd['G']}, {cd['B']}}}}}"
                name = cd["name"]
                fluid_lines.append(f"{rgb} [[{name} (fluid)|{name}]] <small>×{int(vol*1000)}mL</small>")
            continue

        # Item outputs
        if "items" in out:
            qty = out.get("count", out.get("index", 1))
            for rid in out["items"]:
                icon = utility.get_icon(rid)
                if isinstance(icon, list):
                    icon = icon[0] if icon else "Question On.png"
                nm = utility.get_name(rid)
                url = utility.get_page(rid, nm)
                link = util.link(url, nm)
                item_lines.append(f"[[File:{icon}|64x64px|class=pixelart]]<br>{link} ×{qty}")

    # Assemble sections
    if item_lines:
        if len(item_lines) == 1:
            products_markup += item_lines[0]
        else:
            products_markup += "<small>Each of:</small><br>" + "<br>".join(item_lines)

    if mapper_lines:
        if item_lines:
            products_markup += "<br>"
        products_markup += "<small>(Products are dependent on inputs)<br>One of:</small><br>" + "<br>".join(mapper_lines)

    if fluid_lines:
        if item_lines or mapper_lines:
            products_markup += "<br>"
        products_markup += "<small>One of:</small><br>" + "<br>".join(fluid_lines)

    if energy_lines:
        if item_lines or mapper_lines or fluid_lines:
            products_markup += "<br>"
        products_markup += "<br>".join(energy_lines)

    # Fallback
    if products_markup.endswith("<br>") and products_markup.count("<br>") == 1:
        return "products=<small>''none''</small>"

    return products_markup


def process_xp(recipe: dict, build_data: dict) -> str:
    """
    Process experience gains into wiki markup.

    Args:
        recipe (dict): Recipe data containing XP info.
        build_data (dict): Additional building recipe data.

    Returns:
        str: Wiki markup for XP section.

    Handles:
    - XP amounts per skill
    - Multiple skill XP gains
    - Building-specific XP
    """
    xp_award_list = recipe.get("xpAward")
    if not xp_award_list:
        return "''0''"

    skill_mapping = {
        "Woodwork": "Carpentry",
        "MetalWelding": "Welding",
        "FlintKnapping": "Knapping",
        "Blacksmith": "Metalworking",
        "Electricity": "Electrical",
        "LargeBlade": "Long Blade",
    }

    xp_output_parts = []
    for award_entry in xp_award_list:
        for raw_skill_name, xp_amount in award_entry.items():
            display_skill = skill_mapping.get(raw_skill_name, raw_skill_name)
            xp_output_parts.append(f"[[{display_skill}]]: {xp_amount}")

    return "<br>".join(xp_output_parts)


def process_recipes(data: dict) -> str:
    """
    Process recipe learning methods into wiki markup.

    Args:
        data (dict): Recipe data containing learning methods.

    Returns:
        str: Wiki markup for recipe learning section.

    Handles:
    - Skillbook requirements
    - Auto-learn conditions
    - Schematic requirements
    - Trait requirements
    """
    SCHEMATIC = {
        "ExplosiveSchematics": ["Schematic (explosive)"],
        "MeleeWeaponSchematics": ["Schematic (melee weapon)"],
        "BSToolsSchematics":   ["Tools Schematic"],
        "ArmorSchematics":     ["Schematic (armor)"],
        "CookwareSchematic":   ["Cookware Schematic"],
        "FoodRecipes":         ["Recipe"]
    }
    requirements_info = data.get("requirements", {})
    skillbook_list = requirements_info.get("skillbooks", [])
    autolearn_dict = requirements_info.get("autolearn", {})
    autolearn_any_list = requirements_info.get("autolearn_any", [])
    schematic_categories = requirements_info.get("schematics", [])
    trait_list = requirements_info.get("traits", [])

    if not (skillbook_list or autolearn_dict or autolearn_any_list or schematic_categories or trait_list):
        return "''none''"

    formatted_parts = [""]

    for index, skillbook in enumerate(skillbook_list):
        if index > 0:
            formatted_parts.extend(["<br><small>or</small><br>"])
        formatted_parts.append(f"[[{skillbook}]]")

    if schematic_categories:
        formatted_parts.append("<br><small>Schematics:</small><br>")
        for index, schematic_category in enumerate(schematic_categories):
            if index > 0:
                formatted_parts.extend(["<br><small>or</small><br>"])
            for label in SCHEMATIC.get(schematic_category, [schematic_category]):
                formatted_parts.append(f"[[{label}]]")

    if trait_list:
        formatted_parts.append("<br><small>Traits:</small><br>")
        for index, trait_identifier in enumerate(trait_list):
            if index > 0:
                formatted_parts.append("<br>")
            formatted_parts.append(f"[[{trait_identifier}]]")

    if autolearn_dict:
        formatted_parts.append("<br><small>Auto-learnt at:</small><br>")
        for index, (skill_key, level_required) in enumerate(autolearn_dict.items()):
            if index > 0:
                formatted_parts.extend(["<br><small>and</small><br>"])
            formatted_parts.append(f"[[{Translate.get(skill_key, 'Perk')}]] {level_required}")

    # Handle autolearn_any list
    valid_autolearn_entries = []
    for skill_entry in autolearn_any_list:
        if isinstance(skill_entry, str) and ":" in skill_entry:
            sk, lvl = skill_entry.split(":", 1)
            sk = sk.strip()
            lvl = lvl.strip()
            if sk and lvl:  # Only add if both parts are non-empty
                valid_autolearn_entries.append((sk, lvl))

    if valid_autolearn_entries:
        if formatted_parts[-1]:  # If we have previous content, add spacing
            formatted_parts.append("<br>")
        formatted_parts.append("<small>Auto-learnt if any of:</small><br>")
        for index, (skill_key, level) in enumerate(valid_autolearn_entries):
            if index > 0:
                formatted_parts.extend(["<br><small>or</small><br>"])
            formatted_parts.append(f"[[{Translate.get(skill_key, 'Perk')}]] {level}")

    return "".join(formatted_parts)


def process_skills(data: dict) -> str:
    """
    Process skill requirements into wiki markup.

    Args:
        data (dict): Recipe data containing skill requirements.

    Returns:
        str: Wiki markup for skills section.

    Handles:
    - Required skill levels
    - Multiple skill requirements
    - Skill alternatives
    """
    skill_requirements = data.get("requirements", {}).get("skillrequired", {})
    if not skill_requirements:
        return "''none''"

    formatted_skills = []
    for skill_key, required_level in skill_requirements.items():
        formatted_skills.append(f"[[{Translate.get(skill_key, 'Perk')}]] {required_level}")

    return "<br><small>and</small><br>".join(formatted_skills)


def process_requirements(recipe: dict, parsed_item_metadata: dict, literature_data: dict) -> tuple[str, str]:
    """
    Process recipe requirements into wiki markup.

    Args:
        recipe (dict): Recipe data.
        parsed_item_metadata (dict): Item metadata for reference.
        literature_data (dict): Literature data for books/magazines.

    Returns:
        tuple[str, str]: (recipes_markup, skills_markup) for wiki sections.

    Handles:
    - Skill requirements
    - Literature requirements
    - Trait requirements
    - Auto-learn conditions
    """
    requirements_work = {
        "skillrequired": {},
        "skillbooks":   [],
        "autolearn":    {},
        "autolearn_any": [],
        "schematics":   [],
        "traits":       [],
    }

    if recipe.get("needTobeLearn", "").lower() == "true":
        requirements_work["NeedToBeLearn"] = True

    # Explicit skill requirements
    for requirement_entry in recipe.get("SkillRequired", []):
        for sk_key, sk_level in requirement_entry.items():
            requirements_work["skillrequired"][sk_key] = int(sk_level)

    raw_recipe_name = recipe.get("name", "")

    # Skillbooks that teach this recipe
    for item_identifier, item_details in parsed_item_metadata.items():
        if "TeachedRecipes" in item_details and raw_recipe_name in item_details["TeachedRecipes"]:
            book_name = utility.get_name(item_identifier)
            requirements_work["skillbooks"].append(book_name)

    # Schematics from literature spawns
    for category, spawn_list in literature_data.get("SpecialLootSpawns", {}).items():
        if raw_recipe_name in spawn_list:
            requirements_work["schematics"].append(category)

    # Traits parsed from Lua
    try:
        lua_lines = open(os.path.join("resources", "lua", "MainCreationMethods.lua"), encoding="utf-8").read().splitlines()
        translated_recipe_name = Translate.get(raw_recipe_name, property_key="TeachedRecipes")
        for lua_line in lua_lines:
            stripped_line = lua_line.strip()
            if stripped_line.startswith("--"):
                continue
            if re.search(rf'"{re.escape(raw_recipe_name)}"', lua_line) or re.search(rf'"{re.escape(translated_recipe_name)}"', lua_line):
                if ":" in lua_line:
                    trait_identifier = lua_line.split(":", 1)[0].strip()
                    trait_pattern = rf"local\s+{re.escape(trait_identifier)}\s*=\s*TraitFactory\.addTrait\("
                    for lookup_line in lua_lines:
                        if re.search(trait_pattern, lookup_line):
                            match = re.search(r'getText\("([^"]+)"\)', lookup_line)
                            if match and match.group(1).startswith("UI_trait_"):
                                trait_key = match.group(1).replace("UI_trait_", "")
                                trait_name = Translate.get(trait_key, property_key="Trait")
                                if trait_name not in requirements_work["traits"]:
                                    requirements_work["traits"].append(trait_name)
                            break

    except FileNotFoundError:
        echo.error("MainCreationMethods.lua not found for trait parsing")
    except Exception as error:
        echo.error(f"Error parsing traits: {error}")

    # AutoLearnAll
    for autolearn_entry in recipe.get("AutoLearnAll", []):
        for sk_key, sk_level in autolearn_entry.items():
            requirements_work["autolearn"][sk_key] = int(sk_level)

    # AutoLearnAny - handle both string and list formats
    auto_learn_any = recipe.get("AutoLearnAny")
    if auto_learn_any:
        if isinstance(auto_learn_any, str):
            requirements_work["autolearn_any"].append(auto_learn_any)
        elif isinstance(auto_learn_any, list):
            requirements_work["autolearn_any"].extend(auto_learn_any)

    recipes_string = process_recipes({"requirements": requirements_work})
    skills_string  = process_skills({"requirements": requirements_work})
    return recipes_string, skills_string


def build_tag_to_items_map(parsed_item_data: dict) -> dict[str, list[dict[str, str]]]:
    """
    Build mapping of tags to items.

    Args:
        parsed_item_data (dict): Parsed item data.

    Returns:
        dict[str, list[dict[str, str]]]: Mapping of tags to item lists.

    Creates a lookup table for items by their tags.
    """
    full_tag_data = item_tags.get_tag_data()

    tag_map: dict[str, list[dict[str, str]]] = {}
    for tag, entries in full_tag_data.items():
        tag_map[tag] = [{"item_id": entry["item_id"]} for entry in entries]

    return tag_map


def output_item_article_lists(crafting_recipe_map: dict[str, dict], building_recipe_map: dict[str, dict], tag_to_items_map: dict[str, list[dict[str, str]]]) -> None:
    """
    Generate wiki article lists for items.

    Args:
        crafting_recipe_map (dict[str, dict]): Crafting recipe data.
        building_recipe_map (dict[str, dict]): Building recipe data.
        tag_to_items_map (dict[str, list[dict[str, str]]]): Tag to items mapping.

    Creates files documenting how items are used in recipes,
    both as ingredients and as products.
    """

    def is_concrete(item_id: str) -> bool:
        return isinstance(item_id, str) and "*" not in item_id

    def expand_tag(tag: str) -> list[str]:
        return [
            entry["item_id"]
            for entry in tag_to_items_map.get(tag, [])
            if is_concrete(entry["item_id"])
        ]

    def extract_ids(field) -> str: # type: ignore
        for el in field:
            cand = None
            if isinstance(el, str):
                cand = el
            elif isinstance(el, dict):
                cand = (
                    el.get("raw")
                    or el.get("raw_name")
                    or el.get("item_id")
                    or el.get("id")
                )
            if cand and is_concrete(cand):
                yield cand

    usage_by_crafting: dict[str, set[str]] = defaultdict(set)
    usage_by_building: dict[str, set[str]] = defaultdict(set)
    production_by_item: dict[str, set[str]] = defaultdict(set)

    def gather_inputs(recipe: dict, is_building: bool, name: str) -> None:
        seen: set[str] = set()
        target_map = usage_by_building if is_building else usage_by_crafting

        # Items
        for inp in recipe.get("inputs", []):
            for iid in extract_ids(inp.get("items", [])):
                if iid not in seen:
                    seen.add(iid)
                    target_map[iid].add(name)

        # Tags
        for inp in recipe.get("inputs", []):
            for tag in inp.get("tags", []):
                for iid in expand_tag(tag):
                    if iid not in seen:
                        seen.add(iid)
                        target_map[iid].add(name)

        # Tools
        for inp in recipe.get("inputs", []):
            if inp.get("mode") == "Keep" and "items" in inp:
                for iid in extract_ids(inp["items"]):
                    if iid not in seen:
                        seen.add(iid)
                        target_map[iid].add(name)

        # Recipe tags
        for tag in recipe.get("tags", []):
            for iid in expand_tag(tag):
                if iid not in seen:
                    seen.add(iid)
                    target_map[iid].add(name)

    def gather_outputs(recipe: dict, name: str) -> None:
        # Items
        for out in recipe.get("outputs", []):
            if "items" in out:
                for iid in extract_ids(out["items"]):
                    production_by_item[iid].add(name)

            # Mapper outputs
            elif "mapper" in out:
                mapper_key = out["mapper"]
                mapper_data = recipe.get("itemMappers", {}).get(mapper_key, {})
                if isinstance(mapper_data, dict):
                    for raw_output_key in mapper_data.keys():
                        if raw_output_key.lower() == "default":
                            continue
                        production_by_item[raw_output_key].add(name)

    # collect from crafting recipes
    for rname, rdata in crafting_recipe_map.items():
        gather_inputs(rdata, is_building=False, name=rname)
        gather_outputs(rdata, name=rname)

    # collect from building recipes
    for rname, rdata in building_recipe_map.items():
        gather_inputs(rdata, is_building=True, name=rname)

    def render_template(tid: str, names: set[str]) -> str:
        if "construction" in tid:
            header = "Building recipe table"
        else:
            header = "Crafting recipe table"
        lines = [f"{{{{Crafting/sandbox|header={header}|item={tid}"] + [f"|{n}" for n in sorted(names)] + ["}}"]
        return "\n".join(lines)

    def write_file(path: str, content: str) -> None:
        if not content:
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    # whatitcrafts
    for iid, names in usage_by_crafting.items():
        tid = f"{iid}_whatitcrafts"
        write_file(os.path.join("output", "recipes", "crafting", f"{tid}.txt"),
                   render_template(tid, names))

    # howtocraft
    for iid, names in production_by_item.items():
        tid = f"{iid}_howtocraft"
        write_file(os.path.join("output", "recipes", "crafting", f"{tid}.txt"),
                   render_template(tid, names))

    # building
    for iid, names in usage_by_building.items():
        tid = f"{iid}_constructionwhatitcrafts"
        write_file(os.path.join("output", "recipes", "building", f"{tid}.txt"),
                   render_template(tid, names))


def output_skill_usage(recipe_data_map: dict[str, dict]) -> None:
    """
    Generate wiki markup for skill usage.

    Args:
        recipe_data_map (dict[str, dict]): Recipe data.

    Creates files documenting which recipes require each skill
    and what level of skill is needed.
    """
    os.makedirs(os.path.join("output", "recipes", "skills"), exist_ok=True)
    skill_name_mapping = {
        "Woodwork": "Carpentry",
        "MetalWelding": "Welding",
        "FlintKnapping": "Knapping",
        "Blacksmith": "Metalworking",
        "Electricity": "Electrical",
    }

    crafting_skill_usage: defaultdict[str, set[str]] = defaultdict(set)
    building_skill_usage: defaultdict[str, set[str]] = defaultdict(set)

    for recipe_identifier, recipe_data in recipe_data_map.items():
        is_building_recipe = bool(recipe_data.get("construction", False))

        # XP from recipe
        for matched_skill in re.findall(r'\[\[(.*?)\]\]', recipe_data.get("xp", "")):
            display_skill = skill_name_mapping.get(matched_skill, matched_skill)
            target_map = building_skill_usage if is_building_recipe else crafting_skill_usage
            target_map[display_skill].add(recipe_identifier)

        # skill requirements
        for required_skill in recipe_data.get("requirements", {}).get("skillrequired", {}):
            display_skill = skill_name_mapping.get(required_skill, required_skill)
            target_map = building_skill_usage if is_building_recipe else crafting_skill_usage
            target_map[display_skill].add(recipe_identifier)

    # write out templates
    for skill, recipes in crafting_skill_usage.items():
        lines = ["{{Crafting/sandbox|header=Crafting recipe table|ID=" + skill + "_crafting"] + [f"|{r}" for r in sorted(recipes)] + ["}}"]
        with open(os.path.join("output", "recipes", "skills", f"{skill}_crafting.txt"), "w", encoding="utf-8") as file_handle:
            file_handle.write("\n".join(lines))
    for skill, recipes in building_skill_usage.items():
        lines = ["{{Building|header=Building recipe table|ID=" + skill + "_building"] + [f"|{r}" for r in sorted(recipes)] + ["}}"]
        with open(os.path.join("output", "recipes", "skills", f"{skill}_building.txt"), "w", encoding="utf-8") as file_handle:
            file_handle.write("\n".join(lines))


def output_lua_tables(recipe_data_map: dict[str, dict]) -> None:
    """
    Generate Lua tables for recipe data.

    Args:
        recipe_data_map (dict[str, dict]): Recipe data.

    Creates Lua table files that can be used by wiki templates
    to display recipe information.
    """
    base_directory = os.path.join("output", "recipes")
    data_directory = os.path.join(base_directory, "data_files")
    os.makedirs(data_directory, exist_ok=True)

    # split into crafting vs building
    crafting_recipe_map: dict[str, dict] = {}
    building_recipe_map: dict[str, dict] = {}
    for recipe_id, recipe_data in recipe_data_map.items():
        if recipe_data.get("construction", False):
            building_recipe_map[recipe_id] = recipe_data
        else:
            crafting_recipe_map[recipe_id] = recipe_data

    # group crafting by category
    categorized_recipes: dict[str, dict[str, dict]] = defaultdict(dict)
    for recipe_id, recipe_data in crafting_recipe_map.items():
        category_key = (recipe_data.get("category") or "Other").lower()
        categorized_recipes[category_key][recipe_id] = recipe_data

    # write each crafting category file
    for category_key, recipes_in_category in categorized_recipes.items():
        lua_category_path = os.path.join(data_directory, f"{category_key}_data.lua")
        with open(lua_category_path, "w", encoding="utf-8") as writer:
            writer.write(f"-- Module:Crafting/{category_key}_data\n\n")
            writer.write(f"local {category_key} = {{\n")
            for recipe_id, recipe_data in recipes_in_category.items():
                key_name = recipe_id.lower()
                ingredients_markup = recipe_data["ingredients"]
                tools_markup       = recipe_data["tools"]
                recipes_markup     = recipe_data["recipes"]
                skills_markup      = recipe_data["skills"]
                workstation_markup = recipe_data["workstation"]
                xp_markup          = recipe_data["xp"]
                products_markup    = recipe_data["products"]
                if products_markup.startswith("products="):
                    products_markup = products_markup[len("products="):]
                writer.write(
                    f"  {key_name} = {{\n"
                    f"    ingredients = [=[{ingredients_markup}]=],\n"
                    f"    tools       = [=[{tools_markup}]=],\n"
                    f"    recipes     = [=[{recipes_markup}]=],\n"
                    f"    skills      = [=[{skills_markup}]=],\n"
                    f"    workstation = [=[{workstation_markup}]=],\n"
                    f"    xp          = [=[{xp_markup}]=],\n"
                    f"    products    = [=[{products_markup}]=]\n"
                    f"  }},\n"
                )
            writer.write("}\n\n")
            writer.write(f"return {category_key}\n")

    # write building_data.lua
    building_output_path = os.path.join(data_directory, "building_data.lua")
    with open(building_output_path, "w", encoding="utf-8") as writer:
        writer.write("-- Module:Crafting/building_data\n\n")
        writer.write("local buildingList = {\n")
        for recipe_id, recipe_data in building_recipe_map.items():
            key_name = recipe_id.lower()
            ingredients_markup = recipe_data["ingredients"]
            tools_markup       = recipe_data["tools"]
            recipes_markup     = recipe_data["recipes"]
            skills_markup      = recipe_data["skills"]
            workstation_markup = recipe_data["workstation"]
            xp_markup          = recipe_data["xp"]
            products_markup    = recipe_data["products"]
            if products_markup.startswith("products="):
                products_markup = products_markup[len("products="):]
            writer.write(
                f"  {key_name} = {{\n"
                f"    ingredients = [=[{ingredients_markup}]=],\n"
                f"    tools       = [=[{tools_markup}]=],\n"
                f"    recipes     = [=[{recipes_markup}]=],\n"
                f"    skills      = [=[{skills_markup}]=],\n"
                f"    workstation = [=[{workstation_markup}]=],\n"
                f"    xp          = [=[{xp_markup}]=],\n"
                f"    products    = [=[{products_markup}]=]\n"
                f"  }},\n"
            )
        writer.write("}\n\n")
        writer.write("return buildingList\n")

    # write index.lua
    index_path = os.path.join(base_directory, "index.lua")
    with open(index_path, "w", encoding="utf-8") as index_file:
        index_file.write("local index = {\n")

        # crafting categories
        for category_key in sorted(categorized_recipes):
            recipes_in_category = categorized_recipes[category_key]
            names_list = ", ".join(f'"{n}"' for n in sorted(recipes_in_category))
            index_file.write(f"  {category_key} = {{ {names_list} }},\n")

        # building category
        building_names = ", ".join(f'"{n}"' for n in sorted(building_recipe_map))
        index_file.write(f"  building = {{ {building_names} }},\n")
        index_file.write("}\n\n")
        index_file.write("return index\n")


def main():
    """
    Main execution function for recipe processing.

    This function:
    1. Loads necessary data from parsers
    2. Processes all recipes into wiki format
    3. Generates item usage documentation
    4. Creates skill usage documentation
    5. Outputs Lua tables for templates
    """
    language_code = Language.get()
    game_version  = Version.get()

    CRAFT_CACHE_FILE = "parsed_craftRecipe_data.json"
    BUILD_CACHE_FILE = "parsed_entity_data.json"

    craft_cache_path = os.path.join(DATA_DIR, CRAFT_CACHE_FILE)
    build_cache_path = os.path.join(DATA_DIR, BUILD_CACHE_FILE)

    try:
        try:
            echo.info("Building item tags")
            tags_data = item_tags.get_tag_data()
            item_tags.write_tag_image()
        except Exception as exc:
            echo.error(f"Error while building item tags: {exc}")
        else:
            echo.success("Item tags built successfully")

        # Craft cache
        try:
            echo.info("Loading craft cache")
            parsed_craft_data, craft_cache_version = load_cache(
                craft_cache_path, "Craft", get_version=True
            )

            if craft_cache_version != game_version:
                raise ValueError("Craft cache version mismatch")

        except Exception as exc:
            echo.info(f"{exc}; regenerating")

            extract_script_data("craftRecipe")

            parsed_craft_data, craft_cache_version = load_cache(
                craft_cache_path, "Craft", get_version=True
            )
        craft_data = parsed_craft_data
        echo.success("Craft cache ready")

        # Build cache
        try:
            echo.info("Loading build cache")
            parsed_build_data, build_cache_version = load_cache(
                build_cache_path, "Build", get_version=True
            )

            if build_cache_version != game_version:
                raise ValueError("Build cache version mismatch")

        except Exception as exc:
            echo.info(f"{exc}; regenerating")
            extract_script_data("entity")

            parsed_build_data, build_cache_version = load_cache(
                build_cache_path, "Build", get_version=True
            )
        build_data = parsed_build_data
        echo.success("Build cache ready")
        ''
    except Exception as exc:
        echo.error(f"Error while gathering cache: {exc}")
    else:
        echo.success("Cache ready")

    parsed_item_data = get_item_data()
    literature_data  = literature_parser.get_literature_data()
    processed_recipe_map: dict[str, dict] = {}

    total_recipes = len(craft_data) + len(build_data)

    try: #Main processing loop
        with tqdm(total=total_recipes, desc="Processing recipes", bar_format=PBAR_FORMAT, unit=" recipes") as progress_bar:
            # Crafting recipes
            for recipe_id, recipe_data in craft_data.items():
                progress_bar.set_postfix_str(f"Crafting: {recipe_id}")
                try:
                    ingredients_markup   = process_ingredients(recipe_data, build_data)
                    tools_markup         = process_tools(recipe_data, build_data)
                    recipes_markup, skills_markup = process_requirements(recipe_data, parsed_item_data, literature_data)
                    workstation_markup   = process_workstation(recipe_data, build_data)
                    products_markup      = process_products(recipe_data, build_data)
                    xp_markup            = process_xp(recipe_data, build_data)

                    processed_recipe_map[recipe_id] = {
                        "ingredients": ingredients_markup,
                        "tools":        tools_markup,
                        "recipes":      recipes_markup,
                        "skills":       skills_markup,
                        "workstation":  workstation_markup,
                        "products":     products_markup,
                        "xp":           xp_markup,
                        "category":     recipe_data.get("category", "Other"),
                        "construction": False,
                    }
                except Exception as error:
                    echo.error(f"Skipping crafting recipe '{recipe_id}' due to error: {error}")
                finally:
                    progress_bar.update(1)

            # Building recipes
            for recipe_id, recipe_data in build_data.items():
                progress_bar.set_postfix_str(f"Building: {recipe_id}")
                try:
                    ingredients_markup   = process_ingredients(recipe_data, build_data)
                    tools_markup         = process_tools(recipe_data, build_data)
                    recipes_markup, skills_markup = process_requirements(recipe_data, parsed_item_data, literature_data)
                    workstation_markup   = process_workstation(recipe_data, build_data)
                    products_markup      = process_products(recipe_data, build_data)
                    xp_markup            = process_xp(recipe_data, build_data)

                    processed_recipe_map[recipe_id] = {
                        "ingredients": ingredients_markup,
                        "tools":        tools_markup,
                        "recipes":      recipes_markup,
                        "skills":       skills_markup,
                        "workstation":  workstation_markup,
                        "products":     products_markup,
                        "xp":           xp_markup,
                        "category":     recipe_data.get("category", "Other"),
                        "construction": True,
                    }
                except Exception as error:
                    echo.warning(f"Skipping building recipe '{recipe_id}' due to error: {error}")
                finally:
                    progress_bar.update(1)

    except Exception as exc:
        echo.error(f"Error while running main processing loop: {exc}")

    else:
        echo.success("Recipes processed.")

    try: # Begin outputting
        try:
            echo.info("Mapping item tags")
            tag_map = build_tag_to_items_map(parsed_item_data)
        except Exception as exc:
            echo.error(f"Error while mapping item tags: {exc}")
            tag_map = {}
        else:
            echo.success("Item tags mapped")

        try:
            echo.info("Writing skill usage")
            output_skill_usage(processed_recipe_map)
        except Exception as exc:
            echo.error(f"Error while writing skill usage: {exc}")
        else:
            echo.success("Skill usage written")

        try:
            echo.info("Writing lua tables")
            output_lua_tables(processed_recipe_map)
        except Exception as exc:
            echo.error(f"Error while writing lua tables: {exc}")
        else:
            echo.success("Lua tables written")

        try:
            echo.info("Writing per-item article lists")
            output_item_article_lists(craft_data, build_data, tag_map)
        except Exception as exc:
            echo.error(f"Error while writing per-item article lists: {exc}")
        else:
            echo.success("Item article lists written")

    except Exception as exc:
        echo.error(f"Error while writing output: {exc}")

    else:
        echo.success("Recipe output complete")
