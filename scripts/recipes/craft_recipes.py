import os, json, re
from tqdm import tqdm
from collections import defaultdict
from scripts.core.constants import PBAR_FORMAT, DATA_PATH
from scripts.core.language import Language, Translate
from scripts.core.version import Version
from scripts.core.cache import load_cache
from scripts.parser.script_parser import extract_script_data
from scripts.parser import literature_parser, fluid_parser
from scripts.parser.item_parser import get_item_data
from scripts.utils import utility, util
from scripts.utils.echo import echo_success, echo_warning, echo_info, echo_error
from scripts.items import item_tags


def fluid_rgb(fluid_id):
    """
    Retrieve the name and RGB values of a fluid based on its ID.
    """
    try:
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

        red_value = int(float(rgb_values[0]) * 255)
        green_value = int(float(rgb_values[1]) * 255)
        blue_value = int(float(rgb_values[2]) * 255)

        return {
            "name": fluid_name,
            "R": red_value,
            "G": green_value,
            "B": blue_value
        }
    except Exception as error:
        raise RuntimeError(f"Error processing fluid '{fluid_id}': {error}")


def process_ingredients(recipe: dict, build_data: dict) -> str:
    """
    Parses recipe['inputs'] into ingredients, then formats them into
    the wiki‑markup string with “Each of:” / “One of:” grouping.
    Uses 'count' if present (for building recipes), otherwise falls back
    to 'amount' or 'index' for crafting recipes.
    """
    input_list = recipe.get("inputs")
    if not isinstance(input_list, list):
        return "''none''"

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
                        "translated": safe_name_lookup(rid)
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
                    "translated": safe_name_lookup(rid)
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
            info["items"] = [
                {"raw": c, "translated": safe_name_lookup(c)}
                for c in valid
            ]
            info["amount"] = quantity

        if not info:
            echo_error(f"Unhandled ingredient #{input_index}: {input_entry}")

        parsed_ingredients["ingredients"][key] = info

    # Build string
    formatted = []
    for data in parsed_ingredients["ingredients"].values():
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
                link = util.format_link(itm["translated"], utility.get_page(itm["raw"], itm["translated"]))
                lines.append(f"[[File:{icon}|32x32px|class=pixelart]] {link} <small>×{itm['amount']}</small>")
            formatted.append(("item","<br>".join(lines),"One of"))

        # Simple items
        elif data.get("items"):
            lines = []
            qty = data.get("amount",1)
            for itm in data["items"]:
                icon = utility.get_icon(itm["raw"])
                link = util.format_link(itm["translated"], utility.get_page(itm["raw"], itm["translated"]))
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
    Build the wiki‑markup for the “tools” column.

    • One group per Keep‑mode input.
    • “One of:” if that input offers >1 option, otherwise “Each of:”.
    • Consecutive single‑option inputs share one “Each of:” heading.
    • Flags (may degrade, damaged, …) are written **once per group**,
      after the list of options, never after every option.
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

    for inp in recipe.get("inputs", []):
        if inp.get("mode") != "Keep" \
           or "fluidModifier" in inp \
           or any("mapper" in str(v).lower() for v in inp.values()):
            continue

        lines: list[str] = []

        # Tags
        if "tags" in inp:
            for tag in inp["tags"]:
                span = open(os.path.join("output", "en", "tags", "cycle-img", f"{tag}.txt"), encoding="utf-8").read()
                lines.append(f"{span} [[{tag} (tag)]]")

        # Items
        elif "items" in inp:
            for rid in inp["items"]:
                if rid in EXCLUDED or rid.startswith("Base.*"):
                    continue
                name  = utility.get_name(rid)
                page  = utility.get_page(rid, name)
                icon  = utility.get_icon(rid)
                lines.append(f"[[File:{icon}|32x32px|class=pixelart]] {util.format_link(name, page)}")

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
    Determines the crafting workstation required by the recipe.
    """
    tag_list = recipe.get("tags")
    if not tag_list:
        return "''none''"

    workstation_mapping = {
        "anysurfacecraft": "Any surface",
        "choppingblock": "Chopping block",
        "grindstone": "Grindstone",
        "grinding_slab": "Grinding Slab",
        "weaving": "Loom",
        "stone_mill": "Stone Mill",
        "stone_quern": "Stone Quern",
        "churnbucket": "Butter Churn",
        "dryleatherlarge": "Large Drying Rack",
        "dryleathermedium": "Medium Drying Rack",
        "dryleathersmall": "Small Drying Rack",
        "tanleather": "Tanning Barrel",
        "advancedforge": "Advanced Forge",
        "dryingrackgrain": "Drying Rack (Grain)",
        "dryingrackherb": "Drying Rack (Herb)",
        "forge": "Forge",
        "furnace": "Furnace",
        "metalbandsaw": "Metal Bandsaw",
        "potterywheel": "Pottery Wheel",
        "potterybench": "Pottery Bench",
        "primitiveforge": "Primitive Forge",
        "primitivefurnace": "Primitive Furnace",
        "removeflesh": "Softening Beam",
        "removefur": "Softening Beam",
        "spinningwheel": "Spinning Wheel",
        "standingdrillpress": "Standing Drill Press",
        "whetstone": "Whetstone",
        "toaster": "Toaster"
    }

    for tag_identifier in tag_list:
        workstation_name = workstation_mapping.get(tag_identifier.lower())
        if workstation_name:
            return f"[[{workstation_name}]]"

    return "''none''"


def process_output_mapper(recipe: dict, mapper_key: str) -> list[str]:
    """
    Given a recipe and a mapper key, return formatted product lines for that mapper.
    Always uses the 'count' field on the output entry (defaulting to 1).
    """
    item_mappers = recipe.get("itemMappers", {})
    mapper_data = item_mappers.get(mapper_key)
    if not mapper_data or not isinstance(mapper_data, dict):
        echo_warning(f"Mapper '{mapper_key}' not found or invalid in recipe '{recipe.get('name')}'")
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
        link_html = util.format_link(item_name, page_url)

        formatted_lines.append(
            f"[[File:{icon_filename}|64x64px|class=pixelart]]<br>{link_html} ×{output_amount}"
        )

    return formatted_lines


def process_products(recipe: dict, build_data: dict) -> str:
    """
    Processes recipe['outputs'] into a wiki‑markup string listing products.

    For building recipes (identified by the presence of "spriteOutputs"):
      - If an "icon" field exists on an output entry, that image is used.
      - Otherwise, falls back to the first available sprite in "spriteOutputs".
      - Icons beginning with "Item_" drop the prefix and render at 64×64px.
      - Icons beginning with "Build_" render at 96×96px.
      - All others render at 64×128px.
      - If the recipe has no "outputs" entries at all, still use the first sprite.

    For crafting recipes (no "spriteOutputs" key), the standard item/mapper/fluid/energy
    handling is applied.
    """
    is_building = "spriteOutputs" in recipe

    # Header with the recipe's display name
    raw_name = recipe.get("name", "")
    display_name = Translate.get(raw_name, "Recipe")
    products_markup = f"products=<small>''{display_name}''</small><br>"

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
                label = out.get("displayName", display_name)
                count = out.get("count", 1)

                if icon_ref:
                    img, size = icon_ref, "64x128px"
                    if icon_ref.startswith("Item_"):
                        img = icon_ref[len("Item_"):]
                        size = "64x64px"
                    elif icon_ref.startswith("Build_"):
                        size = "96x96px"
                    built_entries.append(
                        f"[[File:{img}.png|{size}|class=pixelart]]<br>[[{label}]] ×{count}"
                    )
                elif first_sprite:
                    sp, size = first_sprite, "64x128px"
                    if first_sprite.startswith("Item_"):
                        sp = first_sprite[len("Item_"):]
                        size = "64x64px"
                    elif first_sprite.startswith("Build_"):
                        size = "96x96px"
                    built_entries.append(
                        f"[[File:{sp}.png|{size}|class=pixelart]]<br>[[{label}]] ×{count}"
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
                link = util.format_link(nm, url)
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
    Processes recipe['xpAward'] into a formatted XP string.
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
    Formats recipe requirements (skillbooks, schematics, traits, autolearn).
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
    schematic_categories = requirements_info.get("schematics", [])
    trait_list = requirements_info.get("traits", [])

    if not (skillbook_list or autolearn_dict or schematic_categories or trait_list):
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

    return "".join(formatted_parts)


def process_skills(data: dict) -> str:
    """
    Formats recipe skill requirements.
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
    Aggregates all requirement data and returns two formatted strings:
      (recipes_string, skills_string)
    """
    requirements_work = {
        "skillrequired": {},
        "skillbooks":   [],
        "autolearn":    {},
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
        echo_error("MainCreationMethods.lua not found for trait parsing")
    except Exception as error:
        echo_error(f"Error parsing traits: {error}")

    # AutoLearnAll
    for autolearn_entry in recipe.get("AutoLearnAll", []):
        for sk_key, sk_level in autolearn_entry.items():
            requirements_work["autolearn"][sk_key] = int(sk_level)

    recipes_string = process_recipes({"requirements": requirements_work})
    skills_string  = process_skills({"requirements": requirements_work})
    return recipes_string, skills_string


def build_tag_to_items_map(parsed_item_data: dict) -> dict[str, list[dict[str, str]]]:
    """
    Reverse lookup: tag → list of item_ids that carry it.
    Instead of relying on the limited 'Tags' field in parsed_item_data,
    we pull the complete tag→items mapping from item_tags.get_tag_data(),
    so that we include *every* item registered under each tag.
    """
    full_tag_data = item_tags.get_tag_data()

    tag_map: dict[str, list[dict[str, str]]] = {}
    for tag, entries in full_tag_data.items():
        tag_map[tag] = [{"item_id": entry["item_id"]} for entry in entries]

    return tag_map


def output_item_article_lists(crafting_recipe_map: dict[str, dict], building_recipe_map: dict[str, dict], tag_to_items_map: dict[str, list[dict[str, str]]]) -> None:
    """
    Creates per‑item templates and combined helpers, skipping wildcards.
    Generates:
      • crafting/<item>_whatitcrafts.txt
      • building/<item>_constructionwhatitcrafts.txt
      • crafting/<item>_howtomake.txt
      • crafting_combined/<item>.txt   (crafting only)
    """

    def is_concrete(item_id: str) -> bool:
        return isinstance(item_id, str) and "*" not in item_id

    def expand_tag(tag: str) -> list[str]:
        return [
            entry["item_id"]
            for entry in tag_to_items_map.get(tag, [])
            if is_concrete(entry["item_id"])
        ]

    def extract_ids(field) -> str:
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
        lines = [f"{{{{Crafting/sandbox|item={tid}"] + [f"|{n}" for n in sorted(names)] + ["}}"]
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

    # Combine crafting
    os.makedirs(os.path.join("output", "recipes", "crafting_combined"), exist_ok=True)
    all_items = set(usage_by_crafting) | set(production_by_item)
    for iid in all_items:
        sections: list[str] = []
        if iid in production_by_item:
            sections.append("===How it's made===")
            sections.append(render_template(f"{iid}_howtomake", production_by_item[iid]))
        if iid in usage_by_crafting:
            sections.append("")  # blank line before next header
            sections.append("===What it makes===")
            sections.append(render_template(f"{iid}_whatitcrafts", usage_by_crafting[iid]))

        write_file(os.path.join("output", "recipes", "crafting_combined", f"{iid}.txt"),
                   "\n".join(sections))


def output_skill_usage(recipe_data_map: dict[str, dict]) -> None:
    """
    For each skill, lists which recipes grant XP or require it.
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
        lines = ["{{Crafting/sandbox|ID=" + skill + "_crafting"] + [f"|{r}" for r in sorted(recipes)] + ["}}"]
        with open(os.path.join("output", "recipes", "skills", f"{skill}_crafting.txt"), "w", encoding="utf-8") as file_handle:
            file_handle.write("\n".join(lines))
    for skill, recipes in building_skill_usage.items():
        lines = ["{{Building|ID=" + skill + "_building"] + [f"|{r}" for r in sorted(recipes)] + ["}}"]
        with open(os.path.join("output", "recipes", "skills", f"{skill}_building.txt"), "w", encoding="utf-8") as file_handle:
            file_handle.write("\n".join(lines))


def output_lua_tables(recipe_data_map: dict[str, dict]) -> None:
    """
    Emit Lua data files for crafting categories, building recipes, and an index.
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
    language_code = Language.get()
    game_version  = Version.get()

    CRAFT_CACHE_FILE = "parsed_craftRecipe_data.json"
    BUILD_CACHE_FILE = "parsed_entity_data.json"

    craft_cache_path = os.path.join(DATA_PATH, CRAFT_CACHE_FILE)
    build_cache_path = os.path.join(DATA_PATH, BUILD_CACHE_FILE)

    try:
        try:
            echo_info("Building item tags")
            tags_data = item_tags.get_tag_data()
            item_tags.write_tag_image()
        except Exception as exc:
            echo_error(f"Error while building item tags: {exc}")
        else:
            echo_success("Item tags built successfully")

        try:
            echo_info("Attempting to load craft cache")
            parsed_craft_data, craft_cache_version = load_cache(
                craft_cache_path, "Craft", get_version=True
            )
        except Exception as exc:
            echo_error(f"Error while loading craft cache: {exc}")
            parsed_craft_data, craft_cache_version = {}, None
        else:
            echo_success("Craft cache loaded successfully")

        try:
            if craft_cache_version != game_version:
                echo_info("Generating craft cache")
                parsed_craft_data = extract_script_data("craftRecipe")
            craft_data = parsed_craft_data
        except Exception as exc:
            echo_error(f"Error while generating craft cache: {exc}")
            craft_data = {}
        else:
            echo_success("Craft cache ready")

        try:
            echo_info("Attempting to load build cache")
            parsed_build_data, build_cache_version = load_cache(
                build_cache_path, "Build", get_version=True
            )
        except Exception as exc:
            echo_error(f"Error while loading build cache: {exc}")
            parsed_build_data, build_cache_version = {}, None
        else:
            echo_success("Build cache loaded successfully")

        try:
            if build_cache_version != game_version:
                echo_info("Generating build cache")
                parsed_build_data = extract_script_data("entity")
            build_data = parsed_build_data
        except Exception as exc:
            echo_error(f"Error while generating build cache: {exc}")
            build_data = {}
        else:
            echo_success("Build cache ready")
    except Exception as exc:
        echo_error(f"Error while gathering cache: {exc}")
    else:
        echo_success("Cache ready")

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
                    echo_warning(f"Skipping crafting recipe '{recipe_id}' due to error: {error}")
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
                    echo_warning(f"Skipping building recipe '{recipe_id}' due to error: {error}")
                finally:
                    progress_bar.update(1)

    except Exception as exc:
        echo_error(f"Error while running main processing loop: {exc}")

    else:
        echo_success("Recipes processed.")

    try: # Begin outputting
        try:
            echo_info("Mapping item tags")
            tag_map = build_tag_to_items_map(parsed_item_data)
        except Exception as exc:
            echo_error(f"Error while mapping item tags: {exc}")
            tag_map = {}
        else:
            echo_success("Item tags mapped")

        try:
            echo_info("Writing skill usage")
            output_skill_usage(processed_recipe_map)
        except Exception as exc:
            echo_error(f"Error while writing skill usage: {exc}")
        else:
            echo_success("Skill usage written")

        try:
            echo_info("Writing lua tables")
            output_lua_tables(processed_recipe_map)
        except Exception as exc:
            echo_error(f"Error while writing lua tables: {exc}")
        else:
            echo_success("Lua tables written")

        try:
            echo_info("Writing per-item article lists")
            output_item_article_lists(craft_data, build_data, tag_map)
        except Exception as exc:
            echo_error(f"Error while writing per-item article lists: {exc}")
        else:
            echo_success("Item article lists written")

    except Exception as exc:
        echo_error(f"Error while writing output: {exc}")

    else:
        echo_success("Recipe output complete")
