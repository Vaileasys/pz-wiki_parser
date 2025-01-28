import os, re, json


RECIPES_DIR = "resources/scripts"
OUTPUT_JSON = "output/recipes/recipes.json"
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

# Global dictionary to store the parsed recipe data
parsed_data = {}


def get_recipe_data():
    """Returns the parsed recipe data. Initialises if the parsed data is empty."""
    global parsed_data
    if not parsed_data:
        main()
    return parsed_data


def gather_recipe_lines(directory: str):
    all_lines = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if (
                (filename.lower().startswith("recipes") or
                 filename.lower().startswith("entity") or
                 filename.lower().startswith("craftrecipe"))
                and filename.lower().endswith(".txt")
                and "test" not in filename.lower()
                and "dbg" not in filename.lower()
            ):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    all_lines.extend(f.readlines())
    return all_lines


def extract_recipe_blocks(lines):
    blocks = []
    in_recipe = False
    bracket_level = 0
    current_lines = []
    current_name = None
    craft_recipe_pattern = re.compile(r'^\s*craftRecipe\s+(\S+)', re.IGNORECASE)
    comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)

    for line in lines:
        if not in_recipe:
            match = craft_recipe_pattern.search(line)
            if match:
                in_recipe = True
                current_name = match.group(1).strip()
                bracket_level = line.count('{') - line.count('}')
                current_lines = [line]
        else:
            current_lines.append(line)
            bracket_level += line.count('{')
            bracket_level -= line.count('}')
            if bracket_level <= 0:
                recipe_text = "".join(current_lines)
                recipe_text = re.sub(comment_pattern, "", recipe_text)
                blocks.append((current_name, recipe_text))

                # Reset state for next recipe block
                in_recipe = False
                bracket_level = 0
                current_lines = []
                current_name = None
    return blocks


def parse_recipe_block(recipe_name, recipe_text):
    recipe_dict = {"name": recipe_name, "inputs": [], "outputs": []}
    mapper_pattern = re.compile(r'itemMapper\s+(\S+)\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    mappers = {}

    def mapper_replacer(match):
        mapper_name = match.group(1).strip()
        body = match.group(2).strip()
        mapper_dict = {}
        for ln in body.splitlines():
            ln = re.sub(r'/\*.*?\*/', '', ln.strip().rstrip(','))
            if not ln or ln.startswith('//'):
                continue
            if '=' in ln:
                left, right = ln.split('=', 1)
                mapper_dict[left.strip()] = right.strip().rstrip(',')
        mappers[mapper_name] = mapper_dict
        return ""

    recipe_text = mapper_pattern.sub(mapper_replacer, recipe_text)
    if mappers:
        recipe_dict["itemMappers"] = mappers

    inputs_pattern = re.compile(r'inputs\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    outputs_pattern = re.compile(r'outputs\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)

    # Parse inputs block
    m = inputs_pattern.search(recipe_text)
    if m:
        block_text = m.group(1)
        recipe_dict["inputs"] = parse_items_block(block_text, is_output=False, recipe_dict=recipe_dict)
        s, e = m.span()
        recipe_text = recipe_text[:s] + recipe_text[e:]

    # Parse outputs block
    m = outputs_pattern.search(recipe_text)
    if m:
        block_text = m.group(1)
        new_outputs = parse_items_block(block_text, is_output=True, recipe_dict=recipe_dict)

        existing_outputs = recipe_dict.get("outputs", [])
        recipe_dict["outputs"] = existing_outputs + new_outputs

        s, e = m.span()
        recipe_text = recipe_text[:s] + recipe_text[e:]

    # Parse remaining lines in the recipe text
    leftover = []
    for ln in recipe_text.splitlines():
        ln = re.sub(r'/\*.*?\*/', '', ln.strip().rstrip(','))
        if ln and not ln.startswith('//'):
            leftover.append(ln)

    # Handle leftover key-value pairs
    pair_pattern = re.compile(r'^\s*(\w+)\s*=\s*(.*?)\s*$', re.IGNORECASE)
    for ln in leftover:
        m2 = pair_pattern.match(ln)
        if not m2:
            continue
        k, v = m2.group(1), m2.group(2)
        if ";" in v:
            recipe_dict[k] = [x.strip() for x in v.split(";") if x.strip()]
        else:
            recipe_dict[k] = v

    return recipe_dict


def parse_items_block(block_text, is_output=False, recipe_dict=None):
    if recipe_dict is None:
        recipe_dict = {}
    results = []
    lines = re.split(r'[\r\n]+', block_text)
    last_item = None
    for line in lines:
        line = line.strip().rstrip(',')
        if not line or line.startswith('//'):
            continue

        # Handle fluid lines:
        if line.lower().startswith('-fluid') or line.lower().startswith('+fluid'):
            fl = parse_fluid_line(line)
            if not fl:
                continue

            # If it's a '-' fluid line
            if fl["sign"] == '-':
                if last_item:
                    if is_any_fluid_container(last_item):
                        last_item["items"] = ["Any fluid container"]
                    last_item["fluidModifier"] = {
                        "fluidType": fl["items"],
                        "amount": fl["amount"]
                    }
                else:
                    results.append({
                        "fluid": True,
                        "amount": fl["amount"],
                        "items": fl["items"]
                    })

            # If it's a '+' fluid line
            else:
                if last_item:
                    copy_item = dict(last_item)
                    copy_item["fluidModifier"] = {
                        "fluidType": fl["items"],
                        "amount": fl["amount"]
                    }
                    if not is_output:
                        outputs = recipe_dict.setdefault("outputs", [])
                        outputs.append(copy_item)
                    else:
                        results.append(copy_item)

            continue

        # Handle energy lines
        if line.lower().startswith('energy'):
            ei = parse_energy_line(line)
            if ei:
                results.append(ei)
                last_item = None
            continue

        # Handle item lines
        elif line.lower().startswith('item'):
            it = parse_item_line(line)
            if it:
                results.append(it)
                last_item = it
            continue

    return results


def is_any_fluid_container(item_obj):
    if (item_obj.get("index") == 1 and item_obj.get("items") and
        len(item_obj["items"]) == 1 and item_obj["items"][0] == "Base.*"):
        return True
    return False


def parse_fluid_line(line):
    pattern = re.compile(r'^([+-])fluid\s+([\d\.]+)\s+(?:\[(.*?)\]|(\S+))', re.IGNORECASE)
    m = pattern.match(line)
    if not m:
        return None
    sign = m.group(1)
    amount = float(m.group(2))
    bracket = m.group(3)
    single = m.group(4)
    items = []
    if bracket:
        items = [x.strip() for x in re.split(r'[;,]', bracket) if x.strip()]
    elif single:
        items = [single.strip()]
    return {"sign": sign, "amount": amount, "items": items}


def parse_energy_line(line):
    pattern = re.compile(r'^energy\s+([\d\.]+)\s+(\S+)\s*(.*)$', re.IGNORECASE)
    m = pattern.match(line)
    if not m:
        return None
    amt = float(m.group(1).strip())
    t = m.group(2).strip()
    mod = m.group(3).strip() if m.group(3) else None
    r = {"energy": True, "amount": amt, "type": t}
    if mod:
        r["modifiers"] = mod
    return r


def parse_item_line(line):
    pattern = re.compile(r'^item\s+(\d+)\s+(.*)$', re.IGNORECASE)
    m = pattern.match(line)
    if not m:
        return None

    index = int(m.group(1))
    rest = m.group(2).strip()
    result = {"index": index}

    mpsec = re.compile(r'mappers?\[.*?\]', re.IGNORECASE)
    rest = mpsec.sub("", rest).strip()

    tags_pat = re.compile(r'tags\[(.*?)\]', re.IGNORECASE)
    flags_pat = re.compile(r'flags\[(.*?)\]', re.IGNORECASE)
    br_items = re.compile(r'\[(.*?)\]')
    mode_pat = re.compile(r'mode\s*:\s*(\S+)', re.IGNORECASE)
    mapr_pat = re.compile(r'mapper\s*:\s*(\S+)', re.IGNORECASE)

    # Extract mapper
    mp = mapr_pat.search(rest)
    if mp:
        result["mapper"] = mp.group(1)
        rest = mapr_pat.sub("", rest)

    # Extract mode
    mo = mode_pat.search(rest)
    if mo:
        result["mode"] = mo.group(1).capitalize()  # e.g., "Destroy"
        rest = mode_pat.sub("", rest)

    # Extract tags
    tg = tags_pat.search(rest)
    if tg:
        tstr = tg.group(1)
        spl = [x.strip() for x in re.split(r'[;,]', tstr) if x.strip()]
        result["tags"] = spl
        rest = tags_pat.sub("", rest)

    flags_found = []
    while True:
        fl = flags_pat.search(rest)
        if not fl:
            break
        spl = [x.strip() for x in re.split(r'[;,]', fl.group(1)) if x.strip()]
        flags_found.extend(spl)
        rest = flags_pat.sub("", rest, count=1)
    if flags_found:
        result["flags"] = flags_found

    if re.search(r'\bitemcount\b', rest, re.IGNORECASE):
        flags_list = result.setdefault("flags", [])
        flags_list.append("itemcount")
        rest = re.sub(r'(?i)\bitemcount\b', '', rest).strip()

    items_found = []
    while True:
        br = br_items.search(rest)
        if not br:
            break
        inside = br.group(1).strip()
        spl = [x.strip() for x in re.split(r'[;,]', inside) if x.strip()]
        pref = [f"Base.{x}" if not x.startswith("Base.") else x for x in spl]
        items_found.extend(pref)
        rest = br_items.sub("", rest, count=1)

    if items_found:
        result["items"] = items_found
    else:
        lf = rest.strip()
        if lf:
            spl = [x.strip() for x in re.split(r'[;,]', lf) if x.strip()]
            pref = [f"Base.{x}" if not x.startswith("Base.") else x for x in spl]
            if pref:
                result["items"] = pref

    return result


def main():
    global parsed_data
    lines = gather_recipe_lines(RECIPES_DIR)
    recipe_blocks = extract_recipe_blocks(lines)
    recipes = []
    for recipe_name, recipe_text in recipe_blocks:
        parsed = parse_recipe_block(recipe_name, recipe_text)
        recipes.append(parsed)
    parsed_data = {"recipes": recipes}
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4)
    print(f"{len(recipes)} recipes written to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
