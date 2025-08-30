import re
from typing import List, Dict, Any, Tuple

def parse_recipe_block(recipe_lines: List[str], block_id: str = "Unknown") -> Dict[str, Any]:
    """
    Parse a CraftRecipe block and return a structured dictionary.
    """
    recipe_dict: Dict[str, Any] = {"name": block_id, "inputs": [], "outputs": []}
    block_text: str = "\n".join(recipe_lines)

    item_mapper_pattern = re.compile(
        r"itemMapper\s+(\S+)\s*\{(.*?)\}", re.DOTALL | re.IGNORECASE
    )
    item_mappers: Dict[str, Dict[str, str]] = {}

    def replace_mapper(match_obj: re.Match) -> str:
        mapper_name: str = match_obj.group(1).strip()
        mapper_body: str = match_obj.group(2)
        mapper_dict: Dict[str, str] = {}

        for mapper_body_line in mapper_body.splitlines():
            cleaned_line: str = re.sub(r"/\*.*?\*/", "", mapper_body_line).strip().rstrip(
                ","
            )
            if not cleaned_line or cleaned_line.startswith("//"):
                continue
            if "=" in cleaned_line:
                left_part, right_part = cleaned_line.split("=", 1)
                mapper_dict[left_part.strip()] = right_part.strip().rstrip(",")

        item_mappers[mapper_name] = mapper_dict
        return ""

    block_text = item_mapper_pattern.sub(replace_mapper, block_text)
    if item_mappers:
        recipe_dict["itemMappers"] = item_mappers

    # Inputs / outputs
    inputs_pattern = re.compile(r"inputs\s*\{(.*?)\}", re.DOTALL | re.IGNORECASE)
    outputs_pattern = re.compile(r"outputs\s*\{(.*?)\}", re.DOTALL | re.IGNORECASE)

    input_match = inputs_pattern.search(block_text)
    if input_match:
        recipe_dict["inputs"] = parse_items_block(
            input_match.group(1), is_output=False, recipe_dict=recipe_dict
        )
        block_text = block_text[: input_match.start()] + block_text[input_match.end() :]

    output_match = outputs_pattern.search(block_text)
    if output_match:
        recipe_dict["outputs"] = parse_items_block(
            output_match.group(1), is_output=True, recipe_dict=recipe_dict
        )
        block_text = (
            block_text[: output_match.start()] + block_text[output_match.end() :]
        )

    # key/value lines
    key_value_pattern = re.compile(r"^\s*(\w+)\s*=\s*(.*?)\s*$", re.IGNORECASE)
    for raw_line in block_text.splitlines():
        cleaned_line: str = re.sub(r"/\*.*?\*/", "", raw_line).strip().rstrip(",")
        if not cleaned_line or cleaned_line.startswith("//"):
            continue

        pair_match = key_value_pattern.match(cleaned_line)
        if not pair_match:
            continue

        key: str = pair_match.group(1)
        value: str = pair_match.group(2).strip()
        key_lowercase: str = key.lower()

        # skills / XP / autolearn lists
        if key_lowercase in ("skillrequired", "xpaward", "autolearnall"):
            # fix malformed colon-only separators
            if value.count(":") >= 3 and ";" not in value:
                colon_indices = [idx for idx, ch in enumerate(value) if ch == ":"]
                middle_colon_index = colon_indices[1]
                value = value[:middle_colon_index] + ";" + value[middle_colon_index + 1 :]

            parts: List[str] = [part.strip() for part in value.split(";") if part.strip()]
            skill_entries: List[Dict[str, Any]] = []
            for part in parts:
                if ":" in part:
                    skill_name, skill_level_str = part.split(":", 1)
                    try:
                        skill_level: Any = int(skill_level_str)
                    except ValueError:
                        skill_level = skill_level_str
                    skill_entries.append({skill_name: skill_level})
            recipe_dict[key] = skill_entries
            continue

        # simple scalar / list values
        if key_lowercase == "category":
            recipe_dict["category"] = value
        elif key_lowercase in ("time", "timedaction"):
            recipe_dict[key] = value
        elif key_lowercase == "tags":
            recipe_dict["tags"] = [tag.strip() for tag in value.split(";") if tag.strip()]
        elif ";" in value:
            recipe_dict[key] = [
                element.strip() for element in value.split(";") if element.strip()
            ]
        else:
            recipe_dict[key] = value

    return recipe_dict


def is_any_fluid_container(item_object: Dict[str, Any]) -> bool:
    """
    Detect the legacy “any fluid container” wildcard:  item 1 [*]
    """
    return (
        item_object.get("index") == 1
        and isinstance(item_object.get("items"), list)
        and len(item_object["items"]) == 1
        and item_object["items"][0] == "Base.*"
    )


def parse_items_block(block_text: str, is_output: bool = False, recipe_dict: Dict[str, Any] = None,) -> List[Dict[str, Any]]:
    """
    Parse an inputs/outputs block, preserving legacy behaviour.
    """
    if recipe_dict is None:
        recipe_dict = {}

    parsed_items: List[Dict[str, Any]] = []
    block_lines: List[str] = re.split(r"[\r\n]+", block_text)
    last_parsed_item: Dict[str, Any] = None

    for raw_line in block_lines:
        stripped_line: str = re.sub(r"/\*.*?\*/", "", raw_line).strip().rstrip(",")
        if not stripped_line or stripped_line.startswith("//"):
            continue
        line_lowercase: str = stripped_line.lower()

        # fluid modifiers
        if line_lowercase.startswith("-fluid") or line_lowercase.startswith("+fluid"):
            fluid_info = parse_fluid_line(stripped_line)
            if not fluid_info:
                continue

            if fluid_info["sign"] == "-":
                # attach to previous item
                if last_parsed_item:
                    if is_any_fluid_container(last_parsed_item):
                        last_parsed_item["items"] = ["Any fluid container"]
                    last_parsed_item["fluidModifier"] = {
                        "fluidType": fluid_info["items"],
                        "amount": fluid_info["amount"],
                    }
                else:
                    parsed_items.append(
                        {
                            "fluid": True,
                            "amount": fluid_info["amount"],
                            "items": fluid_info["items"],
                        }
                    )
            else:  # '+fluid'
                if last_parsed_item:
                    copied_item: Dict[str, Any] = dict(last_parsed_item)
                    copied_item["fluidModifier"] = {
                        "fluidType": fluid_info["items"],
                        "amount": fluid_info["amount"],
                    }
                    if is_output:
                        parsed_items.append(copied_item)
                    else:
                        recipe_dict.setdefault("outputs", []).append(copied_item)
            continue

        # energy
        if line_lowercase.startswith("energy"):
            energy_info = parse_energy_line(stripped_line)
            if energy_info:
                parsed_items.append(energy_info)
                last_parsed_item = None
            continue

        # items
        if line_lowercase.startswith("item"):
            item_entry = parse_item_line(stripped_line)
            if not item_entry:
                continue

            item_entry["count"] = item_entry.pop("count", 0)

            # numbered list handling
            if "items" in item_entry and isinstance(item_entry["items"], list):
                if all(":" in element for element in item_entry["items"]):
                    numbered_entries: List[Dict[str, Any]] = []
                    for entry_str in item_entry["items"]:
                        quantity_str, raw_item_id = entry_str.split(":", 1)
                        try:
                            quantity_value = int(quantity_str.split(".")[-1])
                        except ValueError:
                            try:
                                quantity_value = int(float(quantity_str))
                            except ValueError:
                                quantity_value = 1
                        raw_item_id = raw_item_id.strip()
                        if not raw_item_id.startswith("Base."):
                            raw_item_id = f"Base.{raw_item_id}"
                        numbered_entries.append(
                            {"raw_name": raw_item_id, "amount": quantity_value}
                        )
                    item_entry["numbered_list"] = True
                    item_entry["items"] = numbered_entries
                else:
                    normalized_items: List[str] = []
                    for item_identifier in item_entry["items"]:
                        raw_item_id = item_identifier.split(":", 1)[-1].strip()
                        if not raw_item_id.startswith("Base."):
                            raw_item_id = f"Base.{raw_item_id}"
                        normalized_items.append(raw_item_id)
                    item_entry["items"] = normalized_items

            parsed_items.append(item_entry)
            last_parsed_item = item_entry
            continue

    return parsed_items


def parse_fluid_line(line: str) -> Dict[str, Any]:
    pattern = re.compile(r"^([+-])fluid\s+([\d\.]+)\s+(?:\[(.*?)\]|(\S+))", re.IGNORECASE)
    match = pattern.match(line)
    if not match:
        return None
    sign: str = match.group(1)
    amount: float = float(match.group(2))
    bracket_content: str = match.group(3)
    single_identifier: str = match.group(4)
    items_list: List[str] = (
        [element.strip() for element in re.split(r"[;,]", bracket_content) if element.strip()]
        if bracket_content
        else ([single_identifier.strip()] if single_identifier else [])
    )
    return {"sign": sign, "amount": amount, "items": items_list}


def parse_energy_line(line: str) -> Dict[str, Any]:
    pattern = re.compile(r"^energy\s+([\d\.]+)\s+(\S+)\s*(.*)$", re.IGNORECASE)
    match = pattern.match(line)
    if not match:
        return None
    amount: float = float(match.group(1))
    energy_type: str = match.group(2)
    modifiers: str = match.group(3).strip() or None
    energy_entry: Dict[str, Any] = {"energy": True, "amount": amount, "type": energy_type}
    if modifiers:
        energy_entry["modifiers"] = modifiers
    return energy_entry


def parse_item_line(line: str) -> Dict[str, Any]:
    pattern = re.compile(r"^item\s+(\d+)\s+(.*)$", re.IGNORECASE)
    match = pattern.match(line)
    if not match:
        return None
    count_value: int = int(match.group(1))
    remaining_text: str = re.sub(r"/\*.*?\*/", "", match.group(2), flags=re.DOTALL).strip()
    entry_dict: Dict[str, Any] = {"count": count_value}

    remaining_text = re.sub(r"mappers?\[.*?\]", "", remaining_text, flags=re.IGNORECASE).strip()

    mapper_search = re.search(r"mapper\s*:\s*(\S+)", remaining_text, re.IGNORECASE)
    if mapper_search:
        entry_dict["mapper"] = mapper_search.group(1)
        remaining_text = remaining_text[: mapper_search.start()] + remaining_text[mapper_search.end() :]

    mode_search = re.search(r"mode\s*:\s*(\S+)", remaining_text, re.IGNORECASE)
    if mode_search:
        entry_dict["mode"] = mode_search.group(1).capitalize()
        remaining_text = remaining_text[: mode_search.start()] + remaining_text[mode_search.end() :]

    tags_search = re.search(r"tags\[(.*?)\]", remaining_text, re.IGNORECASE)
    if tags_search:
        entry_dict["tags"] = [
            tag.strip() for tag in re.split(r"[;,]", tags_search.group(1)) if tag.strip()
        ]
        remaining_text = remaining_text[: tags_search.start()] + remaining_text[tags_search.end() :]

    flag_list: List[str] = []
    while True:
        flags_search = re.search(r"flags\[(.*?)\]", remaining_text, re.IGNORECASE)
        if not flags_search:
            break
        flag_list.extend(
            [flag.strip() for flag in re.split(r"[;,]", flags_search.group(1)) if flag.strip()]
        )
        remaining_text = remaining_text[: flags_search.start()] + remaining_text[flags_search.end() :]
    if flag_list:
        entry_dict["flags"] = flag_list

    if re.search(r"\bitemcount\b", remaining_text, re.IGNORECASE):
        entry_dict.setdefault("flags", []).append("itemcount")
        remaining_text = re.sub(r"(?i)\bitemcount\b", "", remaining_text).strip()

    item_identifiers: List[str] = []
    while True:
        bracket_search = re.search(r"\[(.*?)\]", remaining_text)
        if not bracket_search:
            break
        for item_identifier in re.split(r"[;,]", bracket_search.group(1)):
            item_identifier = item_identifier.strip()
            if item_identifier:
                item_identifiers.append(
                    item_identifier if item_identifier.startswith("Base.") else f"Base.{item_identifier}"
                )
        remaining_text = (
            remaining_text[: bracket_search.start()] + remaining_text[bracket_search.end() :]
        )

    if item_identifiers:
        entry_dict["items"] = item_identifiers
    else:
        fallback_items = remaining_text.strip()
        if fallback_items:
            entry_dict["items"] = [
                itm if itm.startswith("Base.") else f"Base.{itm}"
                for itm in re.split(r"[;,]", fallback_items)
                if itm.strip()
            ]

    return entry_dict


def extract_block(text: str, start_index: int) -> Tuple[str, int]:
    bracket_count: int = 0
    current_index: int = start_index
    while current_index < len(text):
        if text[current_index] == "{":
            bracket_count += 1
        elif text[current_index] == "}":
            bracket_count -= 1
            if bracket_count == 0:
                return text[start_index : current_index + 1], current_index + 1
        current_index += 1
    return text[start_index:], current_index


def parse_module_block(full_text: str) -> List[Dict[str, str]]:
    module_entries: List[Dict[str, str]] = []
    module_pattern = re.compile(r"module\s+(\w+)\s*\{", re.IGNORECASE)
    search_position: int = 0
    while True:
        module_match = module_pattern.search(full_text, search_position)
        if not module_match:
            break
        block_content, next_position = extract_block(full_text, module_match.end() - 1)
        module_entries.append({"name": module_match.group(1), "block": block_content})
        search_position = next_position
    return module_entries


def parse_module_skin_mapping(module_block: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    skin_mapping: Dict[str, Dict[str, Dict[str, str]]] = {}
    skin_pattern = re.compile(r"xuiSkin\s+(\w+)\s*\{", re.IGNORECASE)
    pattern_position: int = 0
    while True:
        skin_match = skin_pattern.search(module_block, pattern_position)
        if not skin_match:
            break
        skin_name: str = skin_match.group(1)
        skin_block, next_position = extract_block(module_block, skin_match.end() - 1)

        entity_pattern = re.compile(r"entity\s+(\S+)\s*\{", re.IGNORECASE)
        entity_position: int = 0
        entity_entries: Dict[str, Dict[str, str]] = {}
        while True:
            entity_match = entity_pattern.search(skin_block, entity_position)
            if not entity_match:
                break
            entity_style: str = entity_match.group(1)
            entity_block, entity_next_position = extract_block(skin_block, entity_match.end() - 1)

            display_name_match = re.search(r"DisplayName\s*=\s*([^,\n]+)", entity_block, re.IGNORECASE)
            icon_match = re.search(r"Icon\s*=\s*([^,\n]+)", entity_block, re.IGNORECASE)
            entity_entries[entity_style] = {
                "DisplayName": display_name_match.group(1).strip() if display_name_match else None,
                "Icon": icon_match.group(1).strip() if icon_match else None,
            }
            entity_position = entity_next_position

        skin_mapping.setdefault(skin_name, {}).update(entity_entries)
        pattern_position = next_position

    return skin_mapping


def parse_entity_blocks(module_block: str) -> List[Dict[str, Any]]:
    entity_list: List[Dict[str, Any]] = []
    entity_pattern = re.compile(r"entity\s+(\S+)\s*\{", re.IGNORECASE)
    search_position: int = 0
    while True:
        entity_match = entity_pattern.search(module_block, search_position)
        if not entity_match:
            break
        entity_name: str = entity_match.group(1)
        entity_block, next_position = extract_block(module_block, entity_match.end() - 1)

        component_pattern = re.compile(r"component\s+(\S+)\s*\{", re.IGNORECASE)
        component_position: int = 0
        component_blocks: Dict[str, str] = {}
        while True:
            component_match = component_pattern.search(entity_block, component_position)
            if not component_match:
                break
            component_block, component_next_position = extract_block(
                entity_block, component_match.end() - 1
            )
            component_blocks[component_match.group(1)] = component_block
            component_position = component_next_position

        ui_config_block: str = component_blocks.get("UiConfig", "")
        skin_name_match = re.search(r"xuiSkin\s*=\s*(\S+)", ui_config_block, re.IGNORECASE)
        skin_name: str = skin_name_match.group(1).rstrip(",") if skin_name_match else None

        entity_style_match = re.search(r"entityStyle\s*=\s*(\S+)", ui_config_block, re.IGNORECASE)
        entity_style: str = entity_style_match.group(1).rstrip(",") if entity_style_match else None

        entity_list.append(
            {
                "name": entity_name,
                "components": component_blocks,
                "skinName": skin_name,
                "entityStyle": entity_style,
            }
        )
        search_position = next_position

    return entity_list


def parse_sprite_config(block_text: str) -> Tuple[Dict[str, List[str]], float]:
    sprite_mapping: Dict[str, List[str]] = {}
    base_health: float = None

    base_health_match = re.search(r"skillBaseHealth\s*=\s*([\d\.]+)", block_text, re.IGNORECASE)
    if base_health_match:
        try:
            base_health = float(base_health_match.group(1))
        except ValueError:
            pass

    face_pattern = re.compile(r"face\s+(\S+)\s*\{", re.IGNORECASE)
    search_position: int = 0
    while True:
        face_match = face_pattern.search(block_text, search_position)
        if not face_match:
            break
        face_block, next_position = extract_block(block_text, face_match.end() - 1)

        row_matches: List[str] = re.findall(r"row\s*=\s*([^,}\n]+)", face_block, re.IGNORECASE)
        row_entries: List[str] = []
        for row_entry in row_matches:
            row_entries.extend(item.strip() for item in row_entry.split() if item.strip())

        sprite_mapping[face_match.group(1)] = row_entries
        search_position = next_position

    return sprite_mapping, base_health


def parse_construction_recipe(full_text: str) -> List[Dict[str, Any]]:
    """
    Parse every `entity … { component CraftRecipe { … } }` in the source text
    and return a list of normalised recipe dictionaries.

    The routine now:

      1.  Collects a *global* skin‑mapping for **all** modules first.
      2.  Parses each entity and resolves its (skinName, entityStyle) pair
          against that global table so the `outputs` field is always filled
          when the information exists anywhere in the file‑set.
    """
    construction_recipes: List[Dict[str, Any]] = []
    module_blocks = parse_module_block(full_text)

    global_skin_mapping: Dict[str, Dict[str, Dict[str, str]]] = {}
    for module_entry in module_blocks:
        skin_map = parse_module_skin_mapping(module_entry["block"])
        # merge (keeps earlier values if there are duplicates)
        for skin_name, entity_map in skin_map.items():
            global_skin_mapping.setdefault(skin_name, {}).update(entity_map)

    for module_entry in module_blocks:
        entity_blocks = parse_entity_blocks(module_entry["block"])

        for entity_entry in entity_blocks:
            entity_name: str = entity_entry["name"]
            craft_recipe_block = entity_entry["components"].get("CraftRecipe")
            if not craft_recipe_block:
                continue  # entity has no CraftRecipe component

            parsed_recipe_block = parse_recipe_block(
                craft_recipe_block.splitlines(), block_id=entity_name
            )

            recipe_output: Dict[str, Any] = {"name": entity_name}
            recipe_output.update(parsed_recipe_block)

            skin_name: str = entity_entry.get("skinName")
            entity_style: str = entity_entry.get("entityStyle")

            if skin_name and entity_style:
                style_mapping = global_skin_mapping.get(skin_name, {})
                if entity_style in style_mapping:
                    skin_entry_mapping = style_mapping[entity_style]
                    recipe_output["outputs"] = [
                        {
                            "displayName": skin_entry_mapping.get("DisplayName"),
                            "icon":        skin_entry_mapping.get("Icon"),
                        }
                    ]

            sprite_outputs, base_health = parse_sprite_config(
                entity_entry["components"].get("SpriteConfig", "")
            )
            recipe_output["spriteOutputs"] = sprite_outputs
            if base_health is not None:
                recipe_output["skillBaseHealth"] = base_health

            if recipe_output.get("category", "").lower() == "debug":
                continue

            construction_recipes.append(recipe_output)

    return construction_recipes
