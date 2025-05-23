import os
import re
from scripts.core.constants import DATA_DIR
from scripts.core.version import Version
from scripts.core.language import Language
from scripts.core.cache import load_cache
from scripts.utils.echo import echo_error
from scripts.tiles.tiles_infobox import extract_tile_stats, prepare_tile_list, build_misc_params
from scripts.core.page_manager import init as init_pages, get_pages_from_id

MOVABLE_DEFINITIONS_CACHE_FILE = "movable_definitions.json"

_BED_QUALITY_MAP = {
    "badBed": "Bad",
    "averageBed": "Average",
    "goodBed": "Good",
}

BASE_TABLE_HEADER = """{| class="wikitable theme-red sortable" style="text-align: center;"
|-
! class="unsortable" rowspan=2 | Object
! class="sortable" rowspan=2 | Encumbrance
! class="sortable" rowspan=2 | Size<br>(tiles)
! class="unsortable" rowspan=2 | Crafting surface?
! class="unsortable" colspan=2 | Pick up
! class="unsortable" colspan=2 | Disassemble
|-
! class="sortable" | Skill
! class="sortable" | Tool(s)
! class="sortable" | Skill
! class="sortable" | Tool(s)
"""

STORAGE_TABLE_HEADER = """{| class="wikitable theme-red sortable" style="text-align: center;"
|-
! class="unsortable" rowspan=2 | Object
! class="sortable" rowspan=2 | Encumbrance
! class="sortable" rowspan=2 | Size<br>(tiles)
! class="unsortable" rowspan=2 | Crafting surface?
! class="sortable" rowspan=2 | Capacity
! class="unsortable" colspan=2 | Pick up
! class="unsortable" colspan=2 | Disassemble
|-
! class="sortable" | Skill
! class="sortable" | Tool(s)
! class="sortable" | Skill
! class="sortable" | Tool(s)
"""

COMFORT_TABLE_HEADER = """{| class="wikitable theme-red sortable" style="text-align: center;"
|-
! class="unsortable" rowspan=2 | Object
! class="sortable" rowspan=2 | Encumbrance
! class="sortable" rowspan=2 | Size<br>(tiles)
! class="unsortable" rowspan=2 | Crafting surface?
! class="sortable" rowspan=2 | Bed type
! class="unsortable" colspan=2 | Pick up
! class="unsortable" colspan=2 | Disassemble
|-
! class="sortable" | Skill
! class="sortable" | Tool(s)
! class="sortable" | Skill
! class="sortable" | Tool(s)
"""

CATEGORIES = {
    'Appliances': {
        'Communication': [
            {'key': 'signal', 'mode': 'exists', 'sort': ['signal', 'CustomName']},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Computer'},
        ],
        'Cooking appliances': [
            {'key': 'IsoType', 'mode': 'equals', 'value': 'IsoStove'},
            {'key': 'IsoType', 'mode': 'equals', 'value': 'IsoFireplace'},
            {'key': 'IsoType', 'mode': 'equals', 'value': 'IsoBarbecue'},
        ],
        'Fridges': [
            {'key': 'container', 'mode': 'equals', 'value': 'fridge'},
            {'key': 'CustomName', 'mode': 'in_list', 'values': ['Fridge', 'Freezer']},
            {'key': 'container', 'mode': 'equals', 'value': 'displaycasebutcher'},
        ],
        'Washing machines': [
            {'key': 'IsoType', 'mode': 'equals', 'value': 'IsoClothingDryer'},
            {'key': 'IsoType', 'mode': 'equals', 'value': 'IsoClothingWasher'},
            {'key': 'container', 'mode': 'equals', 'value': 'clothingwasher'},
        ],
        #'Lights': [ Commented out
        #    {'key': 'HasLightOnSprite', 'mode': 'exists', 'sort': ['CustomName']},
        #],
        'Other': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Projector'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Microphone'},
            {'key': 'GroupName', 'mode': 'equals', 'value': 'Extractor'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Terminal'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'HK533p'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Dish'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Clock'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Microscope'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Conditioner'},
            {'key': 'GroupName', 'mode': 'equals', 'value': 'Kaboom Arcade'},
            {'key': 'GroupName', 'mode': 'equals', 'value': 'Dr. Oids Arcade'},
            {'key': 'GroupName', 'mode': 'equals', 'value': 'PAWS Pinball'},
        ],
    },
    'Plumbing': {
        'Sinks': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Sink'},
        ],
        'Baths and showers': [
            {'key': 'CustomName', 'mode': 'in_list', 'values': ['Shower', 'Bath']},
        ],
        'Toilets': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Toilet'},
        ],
        'Other': [
            {'key': 'waterPiped', 'mode': 'exists'},
            {'key': 'CustomName', 'mode': 'in_list', 'values': ['Rain Collector Barrel',]},
            {'key': 'Material2', 'mode': 'equals', 'value': 'WaterContainer'},
            {'key': 'GroupName', 'mode': 'equals', 'value': 'Empty Water'},
        ],
    },
    'Comfort': {
        'Beds': [],      # Handled specially
        'Couches': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Couch'},
        ],
        'Chairs': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Chair'},
        ],
        'Benches': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Bench'},
            {'key': 'GroupName', 'mode': 'equals', 'value': 'Low Bench'},
        ],
        'Stools': [
            {'key': 'CustomName', 'mode': 'in_list', 'values': [
                '50s Barstool', 'Bar Stool', 'Blue Bar Stool',
                'Drum Stool', 'Medical Stool', 'Stool'
            ]},
        ],
        'Seats': [
            {'key': 'CustomName', 'mode': 'in_list', 'values': ['Seating', 'Seat']},
        ],
        'Camping': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Sleeping Bag'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Tent'},
        ],
        'Other': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Pew'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Ottoman'},
        ],
    },
    'Tables': [
        {'key': 'CustomName', 'mode': 'in_list', 'values': [
            'Table', 'Shoddy Table', 'Round Table', 'Poor Quality Table',
            'Picknic Table', 'Oak Round Table', 'Low Table',
            'Light Round Table', 'Fancy Table', 'Fancy Dark Table',
            'Exceptional Table', 'Dark Round Table'
        ]},
        {'key': 'container', 'mode': 'equals', 'value': 'counter'},
    ],
    'Storage': {
        'Counters': [
            {'key': 'container', 'mode': 'equals', 'value': 'counter'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Counter'},
        ],
        'Shelves': [
            {'key': 'container', 'mode': 'in_list', 'values': ['shelves', 'metal_shelves', 'clothingrack', 'shelvesmag']},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'shelves'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Rack'},
        ],
        'Cabinets': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Cabinet'},
        ],
        'Desks': [
            # {'key': 'CustomName', 'mode': 'contains', 'equals': 'Desk'}, This breaks everything?
            {'key': 'container', 'mode': 'contains', 'value': 'desk'},
        ],
        'Dressers': [
            {'key': 'container', 'mode': 'equals', 'value': 'dresser'},
            {'key': 'container', 'mode': 'equals', 'value': 'Wardrobe'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Wardrobe'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Drawers'},
        ],
        'Lockers': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Locker'},
        ],
        'Crates': [
            {'key': 'container', 'mode': 'in_list', 'values': ['cardboardbox', 'militarycrate', 'crate', 'smallbox']},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Crate'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Small crate'},
        ],
        'Displays': [
            {'key': 'container', 'mode': 'in_list', 'values': [
                'restaurantdisplay', 'displaycase', 'displaycasebakery', 'grocerstand'
            ]},
        ],
        'Mail boxes': [
            {'key': 'container', 'mode': 'equals', 'value': 'postbox'},
        ],
        'Mannequins': [
            {'key': 'IsoType', 'mode': 'equals', 'value': 'IsoMannequin'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Mannequin Stand'},
        ],
        'Bins': [
            {'key': 'IsTrashCan', 'mode': 'exists'},
            {'key': 'container', 'mode': 'equals', 'value': 'bin'},
        ],
        'Other': [
            {'key': 'container', 'mode': 'equals', 'value': 'composter'},
            {'key': 'container', 'mode': 'equals', 'value': 'cashregister'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Soda Machine'},
            {'key': 'container', 'mode': 'equals', 'value': 'vendingsnack'},
            {'key': 'GroupName', 'mode': 'equals', 'value': 'Fossoil Candy'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Chest'},
        ],
    },
    'Workstations': [
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Grinder'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Duplicator'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Tannin Barrel'},
        {'key': 'GroupName', 'mode': 'equals', 'value': 'Softening'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Butter Churn'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Workbench'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Loom'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Comb'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Distaff'},
        {'key': 'GroupName', 'mode': 'equals', 'value': 'Scutching'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Quern'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Wheel'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Grinstone'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Grinding Slab'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Bellows'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Pottery Wheel'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Press'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Grindstone'},
        {'key': 'CustomName', 'mode': 'contains', 'value': 'Distaff'},
        {'key': 'CustomName', 'mode': 'contains', 'value': 'Drying Rack'},
        {'key': 'GroupName', 'mode': 'equals', 'value': 'Electric Blower'},
    ],
    'Floors': {
        'Tiles': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Tiles'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Mall Tile'},
        ],
        'Carpets': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'carpet'},
        ],
        'Rugs': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'rug'},
        ],
        'Other': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Floor'},
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Grey Squares'},
        ],
    },
    'Decorations': {
        'Mirrors': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Mirror'},
        ],
        'Paintings': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Painting'},
        ],
        'Sculptures': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Bust'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Statue'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Gallery Toilet'},
            {'key': 'GroupName', 'mode': 'equals', 'value': 'Gallery'},
        ],
        'Posters': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Poster'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Picture'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Notices'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Drawing'},
        ],
        'Flags': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Flag'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Banner'},
        ],
        'Curtains': [
            {'key': 'CustomName', 'mode': 'equals', 'value': 'Curtain'},
        ],
        'Windows': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Window'},
            {'key': 'GroupName', 'mode': 'contains', 'value': 'Window'},
        ],
        'Phones': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Phone'},
        ],
        'Other': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Bird Bath'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Gnome'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Flamingo'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Map'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Noteboard'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Certificate'},
        ],
    },
    'Signs': [
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Sign'},
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Road Sign'},
    ],
    'Trash': [
        {'key': 'CustomName', 'mode': 'equals', 'value': 'Trash'},
    ],
    'Plants': {
        'Plants': [
            {'key': 'CustomName', 'mode': 'contains', 'value': 'tree'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'plant'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'ficus'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'evergreen'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'roses'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Flowers'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Venus Fly Trap'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Cactus'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'roses'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Hay'},
            {'key': 'CustomName', 'mode': 'contains', 'value': 'Flowerbed'},
            {'key': 'vegitation', 'mode': 'exists'},
        ],
    },
}

BLACKLIST = {
    'type': [
        'lightswitch',
    ],
    'sprite': [
        'Carpentry 02 104',
        'crafted_05_18',
        'fixtures_counters_01_16',
        'fixtures_counters_01_24',
        'location_community_medical_01',
        'Location_community_medical_01_107',
        'rooftop_furniture_21',
        'carpentry_02_104',
        # Medical desk blacklisted for now
        'Location_community_medical_01_96',
        'location_community_medical_01_97',
        'location_community_medical_01_98',
        'location_community_medical_01_99',
        'location_community_medical_01_100',
        'location_community_medical_01_101',
        'location_community_medical_01_102',
        'location_community_medical_01_103',
        'location_community_medical_01_104',
        'location_community_medical_01_105',
        'location_community_medical_01_106',
        'location_community_medical_01_107',
        'location_community_medical_01_108',
        'location_community_medical_01_109',
        # Odd-numbered window sprites
        'fixtures_windows_01_3',
        'fixtures_windows_01_5',
        'fixtures_windows_01_7',
        'fixtures_windows_01_11',
        'fixtures_windows_01_13',
        'fixtures_windows_01_15',
        'fixtures_windows_01_19',
        'fixtures_windows_01_21',
        'fixtures_windows_01_23',
        'fixtures_windows_01_27',
        'fixtures_windows_01_29',
        'fixtures_windows_01_31',
        'fixtures_windows_01_35',
        'fixtures_windows_01_37',
        'fixtures_windows_01_39',
        'fixtures_windows_01_59',
        'fixtures_windows_01_61',
        'fixtures_windows_01_63',
    ],
    'CustomName': [
        'Tent',
    ],
    'GroupName': [
        'Floating Trailer',
        'Grey',
        'Large Dark Oak',
        'Random',
    ],
}

def _is_blacklisted(tile: dict) -> bool:
    sprite    = tile.get('sprite', '').lower()
    tile_type = tile.get('type', '').lower()
    generic   = tile.get('properties', {}).get('generic', {})
    custom    = str(generic.get('CustomName', '')).lower()
    group     = str(generic.get('GroupName', '')).lower()

    # prepare lowercase blacklists
    forbidden_sprites     = [s.lower() for s in BLACKLIST.get('sprite', [])]
    forbidden_types       = {t.lower() for t in BLACKLIST.get('type', [])}
    forbidden_customs     = {c.lower() for c in BLACKLIST.get('CustomName', [])}
    forbidden_groups      = {g.lower() for g in BLACKLIST.get('GroupName', [])}

    # sprite exact or prefix match
    for fs in forbidden_sprites:
        if sprite == fs or sprite.startswith(fs + '_'):
            return True

    # type match
    if tile_type in forbidden_types:
        return True

    # CustomName match
    if custom in forbidden_customs:
        return True

    # GroupName match
    if group in forbidden_groups:
        return True

    return False


def _matches(tile: dict, rule: dict) -> bool:
    generic = tile.get("properties", {}).get("generic", {})
    key_name, mode = rule["key"], rule["mode"]
    raw = generic.get(key_name)
    if mode == "exists":
        return raw is not None
    if raw is None:
        return False
    val = str(raw).lower()
    if mode == "equals":
        return val == str(rule.get("value", "")).lower()
    if mode == "in_list":
        return val in (str(x).lower() for x in rule["values"])
    if mode == "contains":
        return str(rule.get("value", "")).lower() in val
    return False


def _flatten_with_parent(named_tiles_data: dict) -> tuple[list[dict], dict]:
    reps, sprite_map = [], {}
    for group_name, variants in named_tiles_data.items():
        if isinstance(variants, dict) and variants:
            first = next(iter(variants.values()))
            reps.append(first)
            sprite_map[first["sprite"]] = group_name
    return reps, sprite_map


def _parse_grid(grid_string: str) -> tuple[int, int]:
    try:
        row, col = map(int, grid_string.split(","))
        return col, row
    except Exception:
        return 0, 0


def generate_furniture_lists(named_tiles_data: dict) -> None:
    init_pages()
    definitions_data, _ = load_cache(
        os.path.join(DATA_DIR, MOVABLE_DEFINITIONS_CACHE_FILE),
        "Movable Definitions",
        get_version=True
    )

    reps, sprite_to_group_map = _flatten_with_parent(named_tiles_data)
    reps = [t for t in reps if not _is_blacklisted(t)]
    matched_sprite_identifiers: set[str] = set()

    current_version = Version.get()
    current_language = Language.get()

    output_dir = os.path.join(os.getcwd(), "output", current_language, "tiles", "lists")
    os.makedirs(output_dir, exist_ok=True)

    header = (
        "{{Header|Project Zomboid|Tiles}}\n"
        f"{{{{Page version|{current_version}}}}}\n"
        "{{Note|Some tiles have been intentionally removed from this list during [[Build 42]] unstable.}}\n"
        "{{toc|right}}\n"
        "{{Tiles nav}}\n\n"
    )

    def write_rows(section_tiles: list[dict], buffer: str, category: str) -> str:
        nonlocal matched_sprite_identifiers

        for tile_data in section_tiles:
            rep_sprite = tile_data["sprite"]
            group_name = sprite_to_group_map.get(rep_sprite)
            page_name = group_name or rep_sprite

            vm = re.match(r'^(?P<b>.*)_(?P<n>\d{1,3}|1000)$', page_name)
            if vm:
                page_name = f"{vm.group('b')} (variant {vm.group('n')})"

            tile_group = named_tiles_data.get(group_name, {}) or {}
            enc, size, p_skill, p_tool, d_skill, _ = extract_tile_stats(
                tile_group, definitions_data, current_language
            )

            # Build sprite candidates & ordering
            candidates = []
            for key, var in tile_group.items():
                gen = var.get("properties", {}).get("generic", {})
                pos = _parse_grid(gen.get("SpriteGridPos", "0,0"))
                facing = gen.get("Facing")
                candidates.append((key, pos, facing))
            south = [(k,p) for k,p,f in candidates if f=="S"]
            east  = [(k,p) for k,p,f in candidates if f=="E"]
            sel   = south or east or [(k,p) for k,p,_ in candidates]
            sel.sort(key=lambda x: (x[1][1], x[1][0]))
            order = [k for k,_ in sel]

            found = None
            for vk in order:
                try:
                    pages = get_pages_from_id(vk, id_type="sprite_id")
                except KeyError:
                    pages = None
                if pages:
                    found = pages[0]
                    break

            if found:
                page_link = f"[[{found}|{page_name}]]"
                img_ref    = found
            else:
                page_link = f"[[{page_name}]]"
                img_ref    = page_name

            if size >= 2 and len(order) >= 2:
                first_key = order[0]
                suffixes = [key.rsplit("_", 1)[-1] for key in order[1:]]
                file_stem = first_key + "".join("+" + s for s in suffixes)
            else:
                file_stem = order[0] if order else rep_sprite

            file_link = f"[[File:{file_stem}.png|link={img_ref}]]"

            # Disassembly tools
            tile_list, _ = prepare_tile_list(tile_group)
            misc = build_misc_params(tile_list, definitions_data, current_language)
            dis_tools = [p.split("=", 1)[1] for p in misc if p.startswith("|disassemble_tool")]
            dis_cell = re.sub(r'[\r\n]+', '', "<br>".join(dis_tools)).strip() or "[[File:UI Cross.png|link=|No tool required]]"

            buffer += "|-\n"
            buffer += f"| {file_link}<br>{page_link}\n"
            buffer += f"| {enc}\n"
            buffer += f"| {size}\n"

            gen0 = tile_data.get("properties", {}).get("generic", {})

            # Crafting surface
            cs = "[[File:UI Tick.png|link=|Can be used as a surface]]" \
                 if str(gen0.get("GenericCraftingSurface","")).lower() == "true" \
                 else "[[File:UI Cross.png|link=|Not a crafting surface]]"
            buffer += f"| {cs}\n"

            # Capacity or Bed type
            if category == "Storage":
                cap = gen0.get("ContainerCapacity")
                if cap is not None:
                    cap_str = cap
                elif gen0.get("container") is not None:
                    cap_str = 50
                else:
                    cap_str = "N/A"
                buffer += f"| {cap_str}\n"
            elif category == "Comfort":
                bt = gen0.get("BedType")
                buffer += f"| {_BED_QUALITY_MAP.get(bt, 'N/A')}\n"

            buffer += f"| {p_skill}\n"
            buffer += f"| {p_tool}\n"

            if "CanScrap" not in next(iter(tile_group.values()), {}).get("properties", {}).get("generic", {}):
                buffer += (
                    "| colspan=\"2\" | [[File:UI Cross.png|link=|Can't be disassembled]]"
                    "<br>Can't be disassembled\n"
                )
            else:
                buffer += f"| {d_skill}\n"
                buffer += f"| {dis_cell}\n"

            matched_sprite_identifiers.add(rep_sprite)

        return buffer

    # Generate each category’s file
    for category, subs in CATEGORIES.items():
        if category == "Storage":
            header_line = STORAGE_TABLE_HEADER
        elif category == "Comfort":
            header_line = COMFORT_TABLE_HEADER
        else:
            header_line = BASE_TABLE_HEADER

        text = header
        remaining = reps.copy()

        if isinstance(subs, dict):
            for sub_name, rules in subs.items():
                text += f"=={sub_name}==\n" + header_line

                # Special Comfort → Beds
                if category == "Comfort" and sub_name == "Beds":
                    beds = []
                    for t in remaining:
                        g = t.get("properties", {}).get("generic", {})
                        nm = str(g.get("CustomName","")).lower()
                        if g.get("BedType") is not None and ("bed" in nm or "mattress" in nm):
                            beds.append(t)
                    text = write_rows(beds, text, category) + "|}\n\n"
                    for b in beds:
                        remaining.remove(b)
                    continue

                matches = []
                for rule in rules:
                    matched = [t for t in remaining if _matches(t, rule)]
                    if rule.get("sort"):
                        matched.sort(key=lambda t: tuple(
                            t.get("properties", {}).get("generic", {}).get(sk, "").lower()
                            for sk in rule["sort"]
                        ))
                    matches.extend(matched)
                    for m in matched:
                        remaining.remove(m)

                text = write_rows(matches, text, category) + "|}\n\n"

        else:
            text += header_line
            matches = []
            for rule in subs:
                matched = [t for t in remaining if _matches(t, rule)]
                matches.extend(matched)
                for m in matched:
                    remaining.remove(m)
            text = write_rows(matches, text, category) + "|}\n\n"

        try:
            with open(os.path.join(output_dir, f"{category}.txt"), "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as err:
            echo_error(f"Failed writing '{category}': {err}")

    leftovers = [t for t in reps if t["sprite"] not in matched_sprite_identifiers]
    if leftovers:
        text = header + BASE_TABLE_HEADER
        text = write_rows(leftovers, text, "") + "|}\n"
        try:
            with open(os.path.join(output_dir, "Miscellaneous.txt"), "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as err:
            echo_error(f"Failed writing 'Other': {err}")