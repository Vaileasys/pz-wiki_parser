import re
from typing import List, Dict, Any, Tuple

def parse_recipe_block(lines: List[str], block_id: str = "Unknown") -> Dict[str, Any]:
    """
    Parses a CraftRecipe block given as lines of text.
    Returns a dict with:
      - name: block_id
      - inputs: list
      - outputs: list
      - timedAction, time, category, tags (as list), ToolTip
      - SkillRequired, xpAward, AutoLearnAll as lists of { skill: level }
    """
    recipe: Dict[str, Any] = {"name": block_id, "inputs": [], "outputs": []}
    text = "\n".join(lines)

    # item mappers
    mapper_pat = re.compile(r'itemMapper\s+(\S+)\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    mappers: Dict[str, Dict[str, str]] = {}
    def _map_replace(m: re.Match) -> str:
        nm = m.group(1).strip()
        body = m.group(2)
        d: Dict[str, str] = {}
        for ln in body.splitlines():
            ln = re.sub(r'/\*.*?\*/', '', ln).strip().rstrip(',')
            if not ln or ln.startswith('//'):
                continue
            if '=' in ln:
                left, right = ln.split('=', 1)
                d[left.strip()] = right.strip().rstrip(',')
        mappers[nm] = d
        return ""
    text = mapper_pat.sub(_map_replace, text)
    if mappers:
        recipe["itemMappers"] = mappers

    # inputs and outputs
    inp_pat = re.compile(r'inputs\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)
    out_pat = re.compile(r'outputs\s*\{(.*?)\}', re.DOTALL | re.IGNORECASE)

    m = inp_pat.search(text)
    if m:
        recipe["inputs"] = parse_items_block(m.group(1), is_output=False, recipe_dict=recipe)
        text = text[:m.start()] + text[m.end():]

    m = out_pat.search(text)
    if m:
        recipe["outputs"] = parse_items_block(m.group(1), is_output=True, recipe_dict=recipe)
        text = text[:m.start()] + text[m.end():]

    # leftover key value pairs
    pair_re = re.compile(r'^\s*(\w+)\s*=\s*(.*?)\s*$', re.IGNORECASE)
    for raw in text.splitlines():
        ln = re.sub(r'/\*.*?\*/', '', raw).strip().rstrip(',')
        if not ln or ln.startswith('//'):
            continue
        m2 = pair_re.match(ln)
        if not m2:
            continue
        k, v = m2.group(1), m2.group(2).strip()
        kl = k.lower()

        if kl == "category":
            recipe["category"] = v
        elif kl in ("time", "timedaction"):
            recipe[k] = v
        elif kl == "tags":
            recipe["tags"] = [x.strip() for x in v.split(";") if x.strip()]
        elif kl in ("skillrequired", "xpaward", "autolearnall"):
            parts = [e.strip() for e in v.split(";") if e.strip()]
            lst: List[Dict[str, Any]] = []
            for e in parts:
                if ":" in e:
                    sk, lvl = e.split(":", 1)
                    try:
                        lvl_val = int(lvl)
                    except ValueError:
                        lvl_val = lvl
                    lst.append({sk: lvl_val})
            recipe[k] = lst
        elif ";" in v:
            recipe[k] = [x.strip() for x in v.split(";") if x.strip()]
        else:
            recipe[k] = v

    return recipe


def parse_items_block(
    block_text: str,
    is_output: bool = False,
    recipe_dict: Dict[str, Any] = None
) -> List[Dict[str, Any]]:

    results: List[Dict[str, Any]] = []
    lines = re.split(r'[\r\n]+', block_text)
    last_item: Dict[str, Any] = {}

    for raw in lines:
        ln = re.sub(r'/\*.*?\*/', '', raw).strip().rstrip(',')
        if not ln or ln.startswith('//'):
            continue
        low = ln.lower()

        # fluid modifier
        if low.startswith('-fluid') or low.startswith('+fluid'):
            fl = parse_fluid_line(ln)
            if not fl:
                continue
            if fl["sign"] == '-':
                if last_item and is_any_fluid_container(last_item):
                    last_item["items"] = ["Any fluid container"]
                last_item["fluidModifier"] = {"fluidType": fl["items"], "amount": fl["amount"]}
            else:
                copy_item = dict(last_item)
                copy_item["fluidModifier"] = {"fluidType": fl["items"], "amount": fl["amount"]}
                if is_output:
                    results.append(copy_item)
                else:
                    recipe_dict.setdefault("outputs", []).append(copy_item)
            continue

        # energy line
        if low.startswith('energy'):
            ei = parse_energy_line(ln)
            if ei:
                results.append(ei)
                last_item = {}
            continue

        # item line
        if low.startswith('item'):
            it = parse_item_line(ln)
            if it:
                results.append(it)
                last_item = it
            continue

    return results


def is_any_fluid_container(item_obj: Dict[str, Any]) -> bool:
    return (
        item_obj.get("count") == 1 and
        isinstance(item_obj.get("items"), list) and
        len(item_obj["items"]) == 1 and
        item_obj["items"][0] == "Base.*"
    )


def parse_fluid_line(line: str) -> Dict[str, Any]:
    pat = re.compile(r'^([+-])fluid\s+([\d\.]+)\s+(?:\[(.*?)\]|(\S+))', re.IGNORECASE)
    m = pat.match(line)
    if not m:
        return None
    sign, amt, bracket, single = m.group(1), float(m.group(2)), m.group(3), m.group(4)
    items = bracket and [x.strip() for x in re.split(r'[;,]', bracket) if x.strip()] or ([single.strip()] if single else [])
    return {"sign": sign, "amount": amt, "items": items}


def parse_energy_line(line: str) -> Dict[str, Any]:
    pat = re.compile(r'^energy\s+([\d\.]+)\s+(\S+)\s*(.*)$', re.IGNORECASE)
    m = pat.match(line)
    if not m:
        return None
    amt = float(m.group(1))
    etype = m.group(2)
    mod = m.group(3).strip() or None
    entry = {"energy": True, "amount": amt, "type": etype}
    if mod:
        entry["modifiers"] = mod
    return entry


def parse_item_line(line: str) -> Dict[str, Any]:
    pat = re.compile(r'^item\s+(\d+)\s+(.*)$', re.IGNORECASE)
    m = pat.match(line)
    if not m:
        return None
    count = int(m.group(1))
    rest = re.sub(r'/\*.*?\*/', '', m.group(2), flags=re.DOTALL).strip()
    entry: Dict[str, Any] = {"count": count}

    rest = re.sub(r'mappers?\[.*?\]', '', rest, flags=re.IGNORECASE).strip()

    mp = re.search(r'mapper\s*:\s*(\S+)', rest, re.IGNORECASE)
    if mp:
        entry["mapper"] = mp.group(1)
        rest = rest[:mp.start()] + rest[mp.end():]

    mo = re.search(r'mode\s*:\s*(\S+)', rest, re.IGNORECASE)
    if mo:
        entry["mode"] = mo.group(1).capitalize()
        rest = rest[:mo.start()] + rest[mo.end():]

    tg = re.search(r'tags\[(.*?)\]', rest, re.IGNORECASE)
    if tg:
        entry["tags"] = [x.strip() for x in re.split(r'[;,]', tg.group(1)) if x.strip()]
        rest = rest[:tg.start()] + rest[tg.end():]

    flags = []
    while True:
        fl = re.search(r'flags\[(.*?)\]', rest, re.IGNORECASE)
        if not fl:
            break
        flags.extend([x.strip() for x in re.split(r'[;,]', fl.group(1)) if x.strip()])
        rest = rest[:fl.start()] + rest[fl.end():]
    if flags:
        entry["flags"] = flags

    if re.search(r'\bitemcount\b', rest, re.IGNORECASE):
        entry.setdefault("flags", []).append("itemcount")
        rest = re.sub(r'(?i)\bitemcount\b', '', rest).strip()

    items = []
    while True:
        br = re.search(r'\[(.*?)\]', rest)
        if not br:
            break
        for x in re.split(r'[;,]', br.group(1)):
            x = x.strip()
            if x:
                items.append(x if x.startswith("Base.") else f"Base.{x}")
        rest = rest[:br.start()] + rest[br.end():]
    if items:
        entry["items"] = items
    else:
        fb = rest.strip()
        if fb:
            entry["items"] = [
                itm if itm.startswith("Base.") else f"Base.{itm}"
                for itm in re.split(r'[;,]', fb) if itm.strip()
            ]

    return entry


def extract_block(text: str, start: int) -> Tuple[str, int]:
    bracket = 0
    idx = start
    while idx < len(text):
        if text[idx] == "{":
            bracket += 1
        elif text[idx] == "}":
            bracket -= 1
            if bracket == 0:
                return text[start:idx+1], idx+1
        idx += 1
    return text[start:], idx


def parse_module_block(text: str) -> List[Dict[str, str]]:
    modules: List[Dict[str, str]] = []
    pat = re.compile(r'module\s+(\w+)\s*\{', re.IGNORECASE)
    pos = 0
    while True:
        m = pat.search(text, pos)
        if not m:
            break
        blk, np = extract_block(text, m.end()-1)
        modules.append({"name": m.group(1), "block": blk})
        pos = np
    return modules


def parse_module_skin_mapping(module_block: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Extracts xuiSkin blocks,
    returns mapping of skinName -> { entityStyle -> {DisplayName, Icon}, … }
    """
    mapping: Dict[str, Dict[str, Dict[str, str]]] = {}
    skin_pat = re.compile(r'xuiSkin\s+(\w+)\s*\{', re.IGNORECASE)
    pos = 0
    while True:
        m = skin_pat.search(module_block, pos)
        if not m:
            break
        skin_name = m.group(1)
        blk, np = extract_block(module_block, m.end()-1)
        ent_pat = re.compile(r'entity\s+(\S+)\s*\{', re.IGNORECASE)
        spos = 0
        entries: Dict[str, Dict[str, str]] = {}
        while True:
            me = ent_pat.search(blk, spos)
            if not me:
                break
            style = me.group(1)
            eb, enp = extract_block(blk, me.end()-1)
            dn = re.search(r'DisplayName\s*=\s*([^,\n]+)', eb, re.IGNORECASE)
            ic = re.search(r'Icon\s*=\s*([^,\n]+)', eb, re.IGNORECASE)
            entries[style] = {
                "DisplayName": dn.group(1).strip() if dn else None,
                "Icon": ic.group(1).strip() if ic else None
            }
            spos = enp
        mapping[skin_name] = entries
        pos = np
    return mapping


def parse_entity_blocks(module_block: str) -> List[Dict[str, Any]]:
    """
    Extracts each entity block along with its components,
    captures name and entityStyle from UiConfig.
    """
    entities: List[Dict[str, Any]] = []
    ent_pat = re.compile(r'entity\s+(\S+)\s*\{', re.IGNORECASE)
    pos = 0
    while True:
        m = ent_pat.search(module_block, pos)
        if not m:
            break
        name = m.group(1)
        blk, np = extract_block(module_block, m.end()-1)

        comp_pat = re.compile(r'component\s+(\S+)\s*\{', re.IGNORECASE)
        cpos = 0
        comps: Dict[str, str] = {}
        while True:
            cm = comp_pat.search(blk, cpos)
            if not cm:
                break
            cblk, cnp = extract_block(blk, cm.end()-1)
            comps[cm.group(1)] = cblk
            cpos = cnp

        ui = comps.get("UiConfig", "")
        m_skin = re.search(r'xuiSkin\s*=\s*(\S+)', ui, re.IGNORECASE)
        skin_name = m_skin.group(1).rstrip(',') if m_skin else None

        m_es = re.search(r'entityStyle\s*=\s*(\S+)', ui, re.IGNORECASE)
        style = m_es.group(1).rstrip(',') if m_es else None

        entities.append({
            "name": name,
            "components": comps,
            "skinName": skin_name,
            "entityStyle": style
        })
        pos = np

    return entities


def parse_sprite_config(block_text: str) -> Tuple[Dict[str, List[str]], float]:
    sprites: Dict[str, List[str]] = {}
    health: float = None
    mh = re.search(r'skillBaseHealth\s*=\s*([\d\.]+)', block_text, re.IGNORECASE)
    if mh:
        try:
            health = float(mh.group(1))
        except ValueError:
            pass

    face_pat = re.compile(r'face\s+(\S+)\s*\{', re.IGNORECASE)
    pos = 0
    while True:
        mf = face_pat.search(block_text, pos)
        if not mf:
            break
        fb, np = extract_block(block_text, mf.end()-1)
        rows = re.findall(r'row\s*=\s*([^,}\n]+)', fb, re.IGNORECASE)
        entries: List[str] = []
        for r in rows:
            entries.extend(e.strip() for e in r.split() if e.strip())
        sprites[mf.group(1)] = entries
        pos = np

    return sprites, health


def parse_construction_recipe(text: str) -> List[Dict[str, Any]]:
    """
    Parses the entire module text for construction‑style recipes:
    - reads xuiSkin blocks
    - enumerates entities + UiConfig + SpriteConfig
    - for each CraftRecipe sub‑block, calls parse_recipe_block
    - then replaces outputs[] with the correct DisplayName/Icon
    """
    results: List[Dict[str, Any]] = []
    modules = parse_module_block(text)
    for mod in modules:
        skin_map_all = parse_module_skin_mapping(mod["block"])
        entities = parse_entity_blocks(mod["block"])
        for ent in entities:
            name = ent["name"]
            cr_blk = ent["components"].get("CraftRecipe")
            if not cr_blk:
                continue

            parsed = parse_recipe_block(cr_blk.splitlines(), name)
            recipe: Dict[str, Any] = {"name": name}
            recipe.update(parsed)

            skin_name = ent.get("skinName", "")
            style_map = skin_map_all.get(skin_name, {})
            style = ent.get("entityStyle")
            if style and style in style_map:
                skin_entry = style_map[style]
                recipe["outputs"] = [{
                    "displayName": skin_entry.get("DisplayName"),
                    "icon": skin_entry.get("Icon")
                }]

            sp, hp = parse_sprite_config(ent["components"].get("SpriteConfig", ""))
            recipe["spriteOutputs"] = sp
            if hp is not None:
                recipe["skillBaseHealth"] = hp

            results.append(recipe)

    return results
