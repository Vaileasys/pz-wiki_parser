import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core import page_manager, file_loading
from scripts.core.constants import RESOURCE_DIR, PBAR_FORMAT, DATA_DIR
from scripts.utils import echo
from scripts.objects.item import Item

# Global variables to store loaded data
_translation_data = None
_page_dictionary = None
_history_cache: dict[str, str] = {}
_codesnips_cache: dict[str, str] = {}
_crafting_cache: dict[str, str] = {}
_body_parts_cache: dict[str, str] = {}
_consumable_properties_cache: dict[str, str] = {}
_container_contents_cache: dict[str, str] = {}
_fixing_cache: dict[str, str] = {}
_infoboxes_cache: dict[str, str] = {}
_evolved_recipes_cache: dict[str, str] = {}
_researchrecipes_cache: dict[str, str] = {}
_teachedrecipes_cache: dict[str, str] = {}
_building_cache: dict[str, str] = {}
_all_items_data = None

# Usage section caches
_usage_weapon_cache: dict[str, str] = {}
_usage_clothing_cache: dict[str, str] = {}
_usage_container_cache: dict[str, str] = {}
_usage_fluid_container_cache: dict[str, str] = {}
_usage_food_cache: dict[str, str] = {}
_usage_crafting_cache: dict[str, str] = {}
_usage_building_cache: dict[str, str] = {}


def load_translations(language_code):
    """
    Load translation data from JSON file for the specified language.

    Args:
        language_code (str): The language code to load translations for

    Returns:
        dict: Translation data for the specified language
    """
    global _translation_data

    if _translation_data is None:
        translation_file = os.path.join(RESOURCE_DIR, "article_translations.json")
        try:
            _translation_data = file_loading.load_json(translation_file)
            echo.info(f"Loaded article translations from {translation_file}")
        except Exception as translation_error:
            echo.error(f"Failed to load article translations: {translation_error}")
            return {}

    return _translation_data.get(language_code, _translation_data.get("en", {}))


def load_page_dictionary():
    """
    Load the page dictionary from page_manager and store it in memory.

    Returns:
        dict: The flattened page dictionary
    """
    global _page_dictionary

    if _page_dictionary is None:
        try:
            page_manager.init()
            _page_dictionary = page_manager.get_flattened_page_dict()
            echo.info("Loaded page dictionary.")
        except Exception as dict_error:
            echo.error(f"Failed to load page dictionary: {dict_error}")
            _page_dictionary = {}

    return _page_dictionary


def load_cache():
    """
    Load frequently accessed content into memory for fast lookups.

    Caches:
    - History entries: resources/history/{id or id_type}.txt
    - Code snippets: output/en/item/codesnips/{id_type or id}.txt
    - Body parts: output/en/item/body_parts/{id_type or id}.txt
    - Consumable properties: output/en/item/consumable_properties/{id_type or id}.txt
    - Container contents: output/en/item/container_contents/{id_type or id}.txt
    - Fixing: output/en/item/fixing/{id_type or id}.txt
    - Infoboxes: output/en/item/infoboxes/{id_type or id}.txt
    - Crafting recipes: output/recipes/crafting/id/*.txt
    - Evolved recipes: output/recipes/evolved_recipes/template/*.txt
    - Research recipes: output/recipes/researchrecipes/id/*.txt
    - Teached recipes: output/recipes/teachedrecipes/id/*.txt
    - Building recipes: output/recipes/building/id/*.txt
    - Distribution data: data/cache/distributions/all_items.json
    - Usage sections:
      - Weapon: output/en/item/usage/weapon/{id_type or id}.txt
      - Clothing: output/en/item/usage/clothing/{id_type or id}.txt
      - Container: output/en/item/usage/container/{id_type or id}.txt
      - Fluid container: output/en/item/usage/fluid_container/{id_type or id}.txt
      - Food: output/en/item/usage/food/{id_type or id}.txt
      - Crafting: output/en/item/usage/crafting/{id_type or id}.txt
      - Building: output/en/item/usage/building/{id_type or id}.txt
    """
    global _history_cache, _codesnips_cache, _crafting_cache, _body_parts_cache
    global _consumable_properties_cache, _container_contents_cache, _fixing_cache
    global _infoboxes_cache, _evolved_recipes_cache, _researchrecipes_cache
    global _teachedrecipes_cache, _building_cache, _all_items_data
    global _usage_weapon_cache, _usage_clothing_cache, _usage_container_cache
    global _usage_fluid_container_cache, _usage_food_cache, _usage_crafting_cache
    global _usage_building_cache

    start_time = time.time()
    echo.info("Starting cache loading with concurrent processing...")

    def collect_files_to_read():
        """
        Collect all files that need to be read into cache.

        Returns:
            list: List of (file_path, base_name, cache_type) tuples
        """
        collected_files = []

        # Cache configuration
        cache_configs = [
            (os.path.join(RESOURCE_DIR, "history"), "history", False),
            (os.path.join("output", "en", "item", "codesnips"), "codesnips", False),
            (os.path.join("output", "recipes", "crafting", "id"), "crafting", True),
            (os.path.join("output", "en", "item", "body_parts"), "body_parts", False),
            (
                os.path.join("output", "en", "item", "consumable_properties"),
                "consumable_properties",
                False,
            ),
            (
                os.path.join("output", "en", "item", "container_contents"),
                "container_contents",
                False,
            ),
            (os.path.join("output", "en", "item", "fixing"), "fixing", False),
            (os.path.join("output", "en", "item", "infoboxes"), "infoboxes", False),
            (
                os.path.join("output", "recipes", "evolved_recipes", "template"),
                "evolved_recipes",
                False,
            ),
            (
                os.path.join("output", "recipes", "researchrecipes", "id"),
                "researchrecipes",
                False,
            ),
            (
                os.path.join("output", "recipes", "teachedrecipes", "id"),
                "teachedrecipes",
                False,
            ),
            (os.path.join("output", "recipes", "building", "id"), "building", False),
        ]

        for directory_path, cache_type, use_full_name in cache_configs:
            if not os.path.isdir(directory_path):
                echo.warning(
                    f"{cache_type.title()} directory '{directory_path}' does not exist"
                )
                continue

            files = [f for f in os.listdir(directory_path) if f.endswith(".txt")]
            if not files:
                echo.warning(
                    f"{cache_type.title()} directory '{directory_path}' is empty"
                )
                continue

            for fname in files:
                source_file_path = os.path.join(directory_path, fname)
                file_base_name = (
                    fname.replace(".txt", "")
                    if use_full_name
                    else os.path.splitext(fname)[0]
                )
                collected_files.append((source_file_path, file_base_name, cache_type))

        return collected_files

    def read_file_worker(file_info):
        """
        Worker function to read a single file.

        Args:
            file_info (tuple): (file_path, base_name, cache_type)

        Returns:
            tuple: (content, base_name, cache_type, success, error_msg)
        """
        worker_file_path, worker_base_name, worker_cache_type = file_info
        try:
            with open(worker_file_path, "r", encoding="utf-8") as fh:
                file_content = fh.read().strip()
            return file_content, worker_base_name, worker_cache_type, True, None
        except Exception as read_error:
            return None, worker_base_name, worker_cache_type, False, str(read_error)

    def get_cache_keys(input_base_name):
        """
        Generate cache keys for a given base name.
        Normalizes Base. prefixes by removing them if present.

        Args:
            input_base_name (str): The base filename without extension

        Returns:
            set: Set of cache keys
        """
        # Removing module and normalize
        normalized_name = input_base_name
        if input_base_name.startswith("Base."):
            normalized_name = input_base_name[5:]
        cache_key_set = {normalized_name}
        cache_key_set.add(f"Base.{normalized_name}")

        return cache_key_set

    # Collect all files to read
    files_to_read = collect_files_to_read()
    total_files = len(files_to_read)

    if total_files == 0:
        echo.warning("No cache files found to load")
        return

    echo.info(f"Found {total_files} files to load into cache")

    # Map cache types to their dictionaries
    cache_maps = {
        "history": _history_cache,
        "codesnips": _codesnips_cache,
        "crafting": _crafting_cache,
        "body_parts": _body_parts_cache,
        "consumable_properties": _consumable_properties_cache,
        "container_contents": _container_contents_cache,
        "fixing": _fixing_cache,
        "infoboxes": _infoboxes_cache,
        "evolved_recipes": _evolved_recipes_cache,
        "researchrecipes": _researchrecipes_cache,
        "teachedrecipes": _teachedrecipes_cache,
        "building": _building_cache,
        # Usage sections
        "usage_weapon": _usage_weapon_cache,
        "usage_clothing": _usage_clothing_cache,
        "usage_container": _usage_container_cache,
        "usage_fluid_container": _usage_fluid_container_cache,
        "usage_food": _usage_food_cache,
        "usage_crafting": _usage_crafting_cache,
        "usage_building": _usage_building_cache,
    }

    # Counters for each cache type
    cache_counters = {cache_type: 0 for cache_type in cache_maps.keys()}
    total_loaded = 0
    total_errors = 0
    max_workers = min(32, (os.cpu_count() or 1) + 4)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all file reading tasks
        future_to_info = {
            executor.submit(read_file_worker, file_info): file_info
            for file_info in files_to_read
        }

        with tqdm(
            total=total_files,
            desc="Loading cache files",
            bar_format=PBAR_FORMAT,
            unit=" files",
        ) as pbar:
            for future in as_completed(future_to_info):
                (
                    result_content,
                    result_base_name,
                    result_cache_type,
                    success,
                    error_msg,
                ) = future.result()

                if success:
                    cache_dict = cache_maps[result_cache_type]
                    if result_cache_type == "crafting":
                        normalized_base_name = result_base_name
                        if result_base_name.startswith("Base."):
                            normalized_base_name = result_base_name[5:]
                        cache_dict[normalized_base_name] = result_content
                    else:
                        cache_keys = get_cache_keys(result_base_name)
                        for key in cache_keys:
                            cache_dict[key] = result_content

                    cache_counters[result_cache_type] += 1
                    total_loaded += 1
                else:
                    error_file_path = future_to_info[future][0]
                    echo.error(
                        f"Failed reading {result_cache_type} file '{error_file_path}': {error_msg}"
                    )
                    total_errors += 1

                pbar.update(1)
    all_items_path = os.path.join(DATA_DIR, "cache", "distributions", "all_items.json")

    try:
        _all_items_data = file_loading.load_json(all_items_path)
        echo.info(f"Loaded distribution data from {all_items_path}")
    except Exception as dist_error:
        echo.error(f"Failed to load distribution data: {dist_error}")
        _all_items_data = {}

    # Report results
    elapsed = time.time() - start_time
    echo.info(f"Cache loading completed in {elapsed:.2f}s")
    echo.info(f"Successfully loaded {total_loaded} files, {total_errors} errors")
    for cache_type, count in cache_counters.items():
        if count > 0:
            echo.info(f"  {cache_type.title()}: {count} files")


def get_article_for_item(item_name, language_code="en"):
    """
    Determine the correct article for an item name.

    Args:
        item_name (str): The item name
        language_code (str): Language code

    Returns:
        str: The appropriate article ("A", "An", or "")
    """
    if language_code != "en":
        return ""

    lowercase_name = item_name.lower()
    words = lowercase_name.split()
    first_word = words[0] if words else ""

    has_of = " of " in lowercase_name
    head_phrase = lowercase_name.split(" of ", 1)[0] if has_of else lowercase_name
    head_words = head_phrase.split()
    head_last_word = head_words[-1] if head_words else ""
    last_word = words[-1] if words else ""

    candidate_plural_word = head_last_word if has_of else last_word
    is_plural = (
        candidate_plural_word.endswith("s")
        and not candidate_plural_word.endswith("ss")
        and len(candidate_plural_word) > 1
    )

    if is_plural:
        return ""

    check_word = head_words[0] if has_of and head_words else first_word
    vowel_starters = ["a", "e", "i", "o", "u"]
    starts_with_vowel = check_word[:1].lower() in vowel_starters

    return "An" if starts_with_vowel else "A"


def create_header(item, translation_data, language_code="en"):
    """
    Create the header markup using logic adapted from the legacy generator.

    Args:
        item (Item): Item instance
        translation_data (dict): Translation data
        language_code (str): Language code

    Returns:
        str: Header markup
    """

    # Mapping adapted from legacy generate_header
    category_dict = {
        "Weapon": "use_skill_type",
        "Tool/Weapon": "use_skill_type",
        "Tool / Weapon": "use_skill_type",
        "Weapon - Crafted": "use_skill_type",
        "Explosives": "{{Header|Project Zomboid|Items|Weapons|Explosives}}",
        "Ammo": "{{Header|Project Zomboid|Items|Weapons|Firearms|Ammo}}",
        "Material": "{{Header|Project Zomboid|Items|Materials}}",
        "Materials": "{{Header|Project Zomboid|Items|Materials}}",
        "Accessory": "{{Header|Project Zomboid|Items|Clothing}}",
        "Clothing": "{{Header|Project Zomboid|Items|Clothing}}",
        "Tool": "{{Header|Project Zomboid|Items|Equipment|Tools}}",
        "Tools": "{{Header|Project Zomboid|Items|Equipment|Tools}}",
        "Junk": "{{Header|Project Zomboid|Items|Miscellaneous items|Junk}}",
        "Mole": "{{Header|Project Zomboid|Items|Miscellaneous items|Plush toys}}",
        "Raccoon": "{{Header|Project Zomboid|Items|Miscellaneous items|Plush toys}}",
        "Squirrel": "{{Header|Project Zomboid|Items|Miscellaneous items|Plush toys}}",
        "Fox": "{{Header|Project Zomboid|Items|Miscellaneous items|Plush toys}}",
        "Badger": "{{Header|Project Zomboid|Items|Miscellaneous items|Plush toys}}",
        "Beaver": "{{Header|Project Zomboid|Items|Miscellaneous items|Plush toys}}",
        "Bunny": "{{Header|Project Zomboid|Items|Miscellaneous items|Plush toys}}",
        "Hedgehog": "{{Header|Project Zomboid|Items|Miscellaneous items|Plush toys}}",
        "Electronics": "{{Header|Project Zomboid|Items|Electronics}}",
        "Weapon Part": "{{Header|Project Zomboid|Items|Weapons|Firearms|Weapon parts}}",
        "WeaponPart": "{{Header|Project Zomboid|Items|Weapons|Firearms|Weapon parts}}",
        "Light Source": "{{Header|Project Zomboid|Items|Equipment|Light sources}}",
        "LightSource": "{{Header|Project Zomboid|Items|Equipment|Light sources}}",
        "Literature": "{{Header|Project Zomboid|Items|Literature}}",
        "Paint": "{{Header|Project Zomboid|Items|Materials}}",
        "First Aid": "{{Header|Project Zomboid|Items|Medical items}}",
        "FirstAid": "{{Header|Project Zomboid|Items|Medical items}}",
        "Fishing": "{{Header|Project Zomboid|Game mechanics|Character|Skills|Fishing}}",
        "Communication": "{{Header|Project Zomboid|Items|Electronics|Communications}}",
        "Communications": "{{Header|Project Zomboid|Items|Electronics|Communications}}",
        "Camping": "{{Header|Project Zomboid|Items|Equipment|Camping}}",
        "Cartography": "{{Header|Project Zomboid|Items|Literature|Cartography}}",
        "Cooking": "{{Header|Project Zomboid|Game mechanics|Crafting|Cooking}}",
        "Entertainment": "{{Header|Project Zomboid|Items|Electronics|Entertainment}}",
        "Food": "{{Header|Project Zomboid|Items|Food}}",
        "Household": "{{Header|Project Zomboid|Items|Miscellaneous items|Household}}",
        "Appearance": "{{Header|Project Zomboid|Items|Miscellaneous items|Appearance}}",
        "AnimalPart": "{{Header|Project Zomboid|Items|Miscellaneous items|Animal parts}}",
        "AnimalPartWeapon": "{{Header|Project Zomboid|Items|Miscellaneous items|Animal parts}}",
    }

    skill_type_dict = {
        "Long Blade": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Long blade weapons}}",
        "Short Blade": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Short blade weapons}}",
        "Long Blunt": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Long blunt weapons}}",
        "Short Blunt": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Short blunt weapons}}",
        "Spear": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Spears}}",
        "Axe": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Axes}}",
        "Aiming": "{{Header|Project Zomboid|Items|Weapons|Firearms}}",
        "Firearm": "{{Header|Project Zomboid|Items|Weapons|Firearms}}",
    }

    item_categories = item.item_categories or []
    header = None

    # Create lowercase mapping for case-insensitive lookups
    lower_key_map: dict[str, str] = {k.lower(): k for k in category_dict.keys()}

    for cat in item_categories:
        if not isinstance(cat, str):
            continue
        normalized = cat.strip()
        key = lower_key_map.get(normalized.lower())
        if key:
            category_value = category_dict[key]
            if category_value == "use_skill_type":
                # Determine skill type
                skill_type = item.get_skill(raw=True) or ""
                skill_type = re.sub(
                    r"\[\[(?:[^\|\]]*\|)?([^\|\]]+)\]\]", r"\1", skill_type
                ).strip()
                header = skill_type_dict.get(
                    skill_type, "{{Header|Project Zomboid|Items|Weapons}}"
                )
            else:
                header = category_value
            break

    if header is None:
        header = "{{Header|Project Zomboid|Items}}"

    translate_reason = translation_data.get("translate_reason", "")

    # Get the current version from Version class
    from scripts.core.version import Version

    version_number = Version.get()

    if language_code == "en":
        full_header = f"{header}\n{{{{Page version|{version_number}}}}}\n{{{{Autogenerated|B42}}}}"
    else:
        full_header = (
            f"{{{{Title|{item.name}}}}}\n"
            f"{header}\n"
            f"{{{{Page version|{version_number}}}}}\n"
            f"{{{{Autogenerated|B42}}}}\n"
            f"{{{{AutoT|{translate_reason}}}}}"
        )

    return full_header


def create_intro(item_data, translation_data, language_code="en"):
    """
    Creates the introduction section for an item article.

    Args:
        item_data (dict): Data about the item including name and other properties
        translation_data (dict): Translation data for the current language
        language_code (str): The language code (default: "en")

    Returns:
        str: The formatted introduction text
    """

    # Extract the name from item_data
    name = item_data.get("name", "")
    if not name:
        echo.warning("No name found for item, cannot create introduction")
        return ""
    lowercase_name = name.lower()

    # Get the appropriate template
    intro_template = translation_data.get(
        "intro_template",
        "{article} '''{lowercase_name}''' {verb} {subsequent_article} [[item]].",
    )
    plural_template = translation_data.get(
        "plural_intro_template",
        "'''{lowercase_name}''' {verb} {subsequent_article} [[item]]s.",
    )

    is_plural = False
    needs_article = True
    words = lowercase_name.split()
    first_word = words[0] if words else ""
    has_of = " of " in lowercase_name
    head_phrase = lowercase_name.split(" of ", 1)[0] if has_of else lowercase_name
    head_words = head_phrase.split()
    head_first_word = head_words[0] if head_words else first_word
    head_last_word = head_words[-1] if head_words else (words[-1] if words else "")
    last_word = words[-1] if words else ""
    subsequent_article = "an"
    verb = "is"

    if language_code == "en":
        # Determine if the item is plural
        candidate_plural_word = head_last_word if has_of else last_word
        if (
            candidate_plural_word.endswith("s")
            and not candidate_plural_word.endswith("ss")
            and len(candidate_plural_word) > 1
        ):
            is_plural = True
            needs_article = False
            verb = "are"

        # Article selection
        article = ""
        if needs_article and not is_plural:
            check_word = head_first_word or first_word
            vowel_starters = ["a", "e", "i", "o", "u"]
            starts_with_vowel = check_word[:1].lower() in vowel_starters

            if starts_with_vowel:
                article = "An"
            else:
                article = "A"
    else:
        article = translation_data.get("article", "")
        if not article:
            needs_article = False
        verb = (
            translation_data.get("verb_singular", "is")
            if not is_plural
            else translation_data.get("verb_plural", "are")
        )

    if is_plural:
        intro = plural_template.format(
            lowercase_name=lowercase_name,
            subsequent_article="",
            verb=verb,
        )
    else:
        intro = intro_template.format(
            article=article if needs_article else "",
            lowercase_name=lowercase_name,
            subsequent_article=subsequent_article,
            verb=verb,
        )

    if intro:
        first_alpha_index = None
        for i, c in enumerate(intro):
            if c.isalpha():
                first_alpha_index = i
                break

        if first_alpha_index is not None:
            intro = (
                intro[:first_alpha_index]
                + intro[first_alpha_index].upper()
                + intro[first_alpha_index + 1 :]
            )

    return intro


def create_infobox(item):
    """
    Get the infobox for an item from the cache.

    Args:
        item (Item): Item instance

    Returns:
        str: Infobox markup
    """

    item_id_full = item.item_id
    item_id_type = item.id_type

    infobox = None
    if item_id_full:
        infobox = _infoboxes_cache.get(item_id_full)
    if not infobox and item_id_type:
        infobox = _infoboxes_cache.get(item_id_type)

    return infobox or ""


def create_usage(item_data, translation_data):
    """
    Creates the usage section for an item article with a call to action.

    Args:
        item_data (dict): Data about the item
        translation_data (dict): Translation data for the current language

    Returns:
        str: The formatted usage section
    """

    def create_usage_weapon():
        """
        Create the weapon subsection for the usage section.

        Returns:
            str or None: The formatted weapon usage section, or None if no data found
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        item = Item(item_id_full or item_id_type)

        if not item.get("MaxDamage"):
            return None

        usage_headers = translation_data.get("Usage_headers", {})
        weapon_header = usage_headers.get("Weapon", "Weapon")
        condition_header = usage_headers.get("Condition", "Condition")
        weapon_text_template = translation_data.get("weapon_usage_text", "")
        condition_text_template = translation_data.get("condition_text", "")

        if not weapon_text_template:
            return None

        translated_name = item.name.lower()
        skill = item.get_skill(raw=True) or "Unknown"
        skill_lower = skill.lower()
        max_hit_count = item.max_hit_count or 1

        weapon_text = weapon_text_template.format(
            translated_name=translated_name,
            skill=skill,
            skill_lower=skill_lower,
            max_hit_count=max_hit_count,
        )

        weapon_section = f"==={weapon_header}===\n{weapon_text}"

        if item.condition_max and item.condition_max > 0 and condition_text_template:
            condition_lower_chance_one_in = item.condition_lower_chance_one_in or 10
            condition_max = item.condition_max

            condition_text = condition_text_template.format(
                translated_name=translated_name,
                condition_max=condition_max,
                skill=skill,
                skill_lower=skill_lower,
                condition_lower_chance_one_in=condition_lower_chance_one_in,
            )

            weapon_section += f"\n\n===={condition_header}====\n{condition_text}"

        return weapon_section

    def create_usage_tool():
        """
        Create the tool subsection for the usage section.

        Returns:
            str or None: The formatted tool usage section, or None if no tool tags found
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        item = Item(item_id_full or item_id_type)

        tool_tags = ["ChopTree", "CutPlant", "RemoveBarricade", "ButcherAnimal"]
        has_tool_tags = [tag for tag in tool_tags if item.has_tag(tag)]

        if not has_tool_tags:
            return None

        usage_headers = translation_data.get("Usage_headers", {})
        tool_header = usage_headers.get("Tool", "Tool")
        tool_base_template = translation_data.get("tool_usage_base", "")
        tool_texts = translation_data.get("tool_usage_texts", {})

        if not tool_base_template:
            return None

        translated_name = item.name.lower()
        tool_text = tool_base_template.format(translated_name=translated_name)

        for tag in has_tool_tags:
            if tag in tool_texts:
                tool_text += " " + tool_texts[tag]

        return f"==={tool_header}===\n{tool_text}"

    def create_usage_fuel():
        """
        Create the fuel subsection for the usage section.

        Returns:
            str or None: The formatted fuel usage section, or None if item cannot be used as fuel
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        item = Item(item_id_full or item_id_type)
        burn_time = item.burn_time
        if not burn_time:
            return None

        usage_headers = translation_data.get("Usage_headers", {})
        fuel_header = usage_headers.get("Fuel", "Fuel")

        fuel_text_template = translation_data.get("fuel_usage_text", "")

        if not fuel_text_template:
            return None

        translated_name = item.name.lower()
        fuel_text = fuel_text_template.format(
            translated_name=translated_name, burn_time=burn_time
        )

        return f"==={fuel_header}===\n{fuel_text}"

    def create_usage_clothing():
        """
        Create the clothing subsection for the usage section.

        Returns:
            str or None: The formatted clothing usage section, or None if not a clothing item
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        item = Item(item_id_full or item_id_type)

        has_body_location = item.get("BodyLocation") is not None
        is_clothing_type = item.get("ItemType") == "Clothing"

        if not has_body_location and not is_clothing_type:
            return None

        usage_headers = translation_data.get("Usage_headers", {})
        clothing_header = usage_headers.get("Clothing", "Clothing")
        body_part_header = usage_headers.get("Body part", "Body part")

        clothing_text_template = translation_data.get("clothing_usage_text", "")
        body_part_table_template = translation_data.get("body_part_table", "")

        if not clothing_text_template:
            return None

        translated_name = item.name.lower()
        clothing_text = clothing_text_template.format(translated_name=translated_name)

        clothing_section = f"==={clothing_header}===\n{clothing_text}"

        if has_body_location and item.body_location and body_part_table_template:
            body_part_cached = None
            if item_id_full:
                body_part_cached = _body_parts_cache.get(item_id_full)
            if not body_part_cached and item_id_type:
                body_part_cached = _body_parts_cache.get(item_id_type)

            if body_part_cached:
                body_part_text = body_part_table_template.format(
                    item_id=item.item_id, body_part_cached=body_part_cached
                )
                clothing_section += f"\n\n===={body_part_header}====\n{body_part_text}"

        return clothing_section

    def create_usage_food():
        """
        Create the food subsection for the usage section.

        Returns:
            str or None: The formatted food usage section, or None if not a food item
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        item = Item(item_id_full or item_id_type)
        if not item.get("HungerChange"):
            return None

        usage_headers = translation_data.get("Usage_headers", {})
        food_header = usage_headers.get("Food", "Food")
        consumable_properties_header = usage_headers.get(
            "Consumable Properties", "Consumable Properties"
        )

        food_text_template = translation_data.get("food_usage_text", "")

        if not food_text_template:
            return None

        food_section = f"==={food_header}===\n{food_text_template}"

        consumable_properties_content = None
        if item_id_full:
            consumable_properties_content = _consumable_properties_cache.get(
                item_id_full
            )
        if not consumable_properties_content and item_id_type:
            consumable_properties_content = _consumable_properties_cache.get(
                item_id_type
            )

        if consumable_properties_content:
            food_section += f"\n\n===={consumable_properties_header}====\n{consumable_properties_content}"

        return food_section

    def create_usage_container():
        """
        Create the container subsection for the usage section.

        Returns:
            str or None: The formatted container usage section, or None if not a container
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None
        item = Item(item_id_full or item_id_type)

        if item.get("ItemType") != "Container" or item.get("Capacity", 0) <= 0:
            return None

        usage_headers = translation_data.get("Usage_headers", {})
        container_header = usage_headers.get("Container", "Container")
        container_text_template = translation_data.get("container_usage_text", "")

        if not container_text_template:
            return None

        language_code = item_data.get("language_code", "en")
        item_lower = item.name.lower()
        article = get_article_for_item(item.name, language_code)

        container_text = container_text_template.format(
            article=article, item_lower=item_lower
        )

        return f"==={container_header}===\n{container_text}"

    def create_usage_container_contents():
        """
        Create the container contents subsection for the usage section.

        Returns:
            str or None: The formatted container contents section, or None if no contents data found
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        contents_cache = None
        if item_id_full:
            contents_cache = _container_contents_cache.get(item_id_full)
        if not contents_cache and item_id_type:
            contents_cache = _container_contents_cache.get(item_id_type)

        if not contents_cache:
            return None

        usage_headers = translation_data.get("Usage_headers", {})
        contents_header = usage_headers.get("Contents", "Contents")

        contents_text_template = translation_data.get("container_contents_text", "")

        if not contents_text_template:
            return None

        from scripts.objects.item import Item

        item = Item(item_id_full or item_id_type)

        language_code = item_data.get("language_code", "en")
        item_lower = item.name.lower()
        article = get_article_for_item(item.name, language_code)

        contents_text = contents_text_template.format(
            article=article, item_lower=item_lower
        )

        return f"==={contents_header}===\n{contents_text}\n{contents_cache}"

    def create_usage_fluid_container():
        """
        Create the fluid container subsection for the usage section.

        Returns:
            str or None: The formatted fluid container usage section, or None if not a fluid container
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        # Create Item object to check if it's a fluid container
        from scripts.objects.item import Item

        item = Item(item_id_full or item_id_type)

        # Check if item has fluid container component
        has_fluid_container = item.get_component("FluidContainer") is not None

        if not has_fluid_container:
            return None

        # Get fluid container capacity
        capacity = (
            item.fluid_container.capacity if hasattr(item, "fluid_container") else 0
        )

        if capacity <= 0:
            return None

        # Convert capacity from liters to milliliters (round to nearest integer)
        capacity_ml = int(round(capacity * 1000))

        # Get translated headers and text template
        usage_headers = translation_data.get("Usage_headers", {})
        fluid_container_header = usage_headers.get("Fluid container", "Fluid container")

        fluid_container_text_template = translation_data.get("fluid_container_text", "")

        if not fluid_container_text_template:
            return None

        # Get item name and determine article
        language_code = item_data.get("language_code", "en")
        item_lower = item.name.lower()
        article = get_article_for_item(item.name, language_code)

        # Format the fluid container usage text
        fluid_container_text = fluid_container_text_template.format(
            article=article, item_lower=item_lower, capacity=capacity_ml
        )

        return f"==={fluid_container_header}===\n{fluid_container_text}"

    def create_usage_crafting():
        """
        Create the crafting subsection for the usage section.

        Returns:
            str or None: The formatted crafting usage section, or None if no crafting data found
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        crafting_content = None
        teached_recipes_content = None
        researchable_recipes_content = None
        evolved_recipes_content = None

        def normalize_item_id(item_id):
            return item_id[5:] if item_id and item_id.startswith("Base.") else item_id

        normalized_id_full = normalize_item_id(item_id_full)
        normalized_id_type = normalize_item_id(item_id_type)

        # Check crafting cache
        if normalized_id_full:
            crafting_content = _crafting_cache.get(f"{normalized_id_full}_whatitcrafts")
        if not crafting_content and normalized_id_type:
            crafting_content = _crafting_cache.get(f"{normalized_id_type}_whatitcrafts")

        # Check teached recipes cache
        if normalized_id_full:
            teached_recipes_content = _teachedrecipes_cache.get(
                f"{normalized_id_full}_Teached"
            )
        if not teached_recipes_content and normalized_id_type:
            teached_recipes_content = _teachedrecipes_cache.get(
                f"{normalized_id_type}_Teached"
            )

        # Check researchable recipes cache
        if normalized_id_full:
            researchable_recipes_content = _researchrecipes_cache.get(
                f"{normalized_id_full}_research"
            )
        if not researchable_recipes_content and normalized_id_type:
            researchable_recipes_content = _researchrecipes_cache.get(
                f"{normalized_id_type}_research"
            )

        # Check evolved recipes cache
        if normalized_id_full:
            evolved_recipes_content = _evolved_recipes_cache.get(normalized_id_full)
        if not evolved_recipes_content and normalized_id_type:
            evolved_recipes_content = _evolved_recipes_cache.get(normalized_id_type)

        # If no crafting data found in any cache, skip section
        if not any(
            [
                crafting_content,
                teached_recipes_content,
                researchable_recipes_content,
                evolved_recipes_content,
            ]
        ):
            return None

        # Get translated headers and text templates
        usage_headers = translation_data.get("Usage_headers", {})
        crafting_header = usage_headers.get("Crafting", "Crafting")
        learned_recipes_header = usage_headers.get("Learned recipes", "Learned recipes")
        evolved_recipes_header = usage_headers.get("Evolved recipes", "Evolved recipes")
        researchable_recipes_header = usage_headers.get(
            "Researchable recipes", "Researchable recipes"
        )

        crafting_text = translation_data.get("crafting_text", "")
        learned_recipes_text = translation_data.get("learned_recipes_text", "")
        evolved_recipes_text = translation_data.get("evolved_recipes_text", "")
        researchable_recipes_text = translation_data.get(
            "researchable_recipes_text", ""
        )

        # Start with main crafting section
        crafting_content_parts = []

        # If we have crafting content, add header, text and content
        if crafting_content:
            crafting_content_parts.append(f"==={crafting_header}===")
            crafting_content_parts.append(crafting_text)
            crafting_content_parts.append(crafting_content)

        # Otherwise if we have any other recipe content, just add the header
        elif any(
            [
                teached_recipes_content,
                researchable_recipes_content,
                evolved_recipes_content,
            ]
        ):
            crafting_content_parts.append(f"==={crafting_header}===")

        # Add learned recipes if available
        if teached_recipes_content:
            crafting_content_parts.append(f"\n===={learned_recipes_header}====")
            crafting_content_parts.append(learned_recipes_text)
            crafting_content_parts.append(teached_recipes_content)

        # Add evolved recipes if available
        if evolved_recipes_content:
            crafting_content_parts.append(f"\n===={evolved_recipes_header}====")
            crafting_content_parts.append(evolved_recipes_text)
            crafting_content_parts.append(evolved_recipes_content)

        # Add researchable recipes if available
        if researchable_recipes_content:
            crafting_content_parts.append(f"\n===={researchable_recipes_header}====")
            # Don't add the text template since it's already included in the content
            crafting_content_parts.append(researchable_recipes_content)

        return "\n".join(crafting_content_parts)

    def create_usage_building():
        """
        Create the building subsection for the usage section.

        Returns:
            str or None: The formatted building usage section, or None if no data found
        """
        item_id_full = item_data.get("id") or ""
        item_id_type = item_data.get("id_type") or ""

        if not item_id_full and not item_id_type:
            return None

        def normalize_item_id(item_id):
            return item_id[5:] if item_id and item_id.startswith("Base.") else item_id

        normalized_id_full = normalize_item_id(item_id_full)
        normalized_id_type = normalize_item_id(item_id_type)

        building_content = None
        if normalized_id_full:
            building_content = _building_cache.get(
                f"{normalized_id_full}_constructionwhatitcrafts"
            )
        if not building_content and normalized_id_type:
            building_content = _building_cache.get(
                f"{normalized_id_type}_constructionwhatitcrafts"
            )

        if building_content:
            usage_headers = translation_data.get("Usage_headers", {})
            building_header = usage_headers.get("Building", "Building")
            building_text = translation_data.get(
                "building_text",
                "It is used as an ingredient in the following building recipes.",
            )

            return f"==={building_header}===\n{building_text}\n{building_content}"

        return None

    # Build usage
    headers = translation_data.get("headers", {})
    usage_header = headers.get("Usage", "Usage")
    call_to_action = translation_data.get("call_to_action", "")

    tool = create_usage_tool()
    weapon = create_usage_weapon()
    fuel = create_usage_fuel()
    clothing = create_usage_clothing()
    food = create_usage_food()
    container = create_usage_container()
    container_contents = create_usage_container_contents()
    fluid_container = create_usage_fluid_container()
    crafting = create_usage_crafting()
    building = create_usage_building()

    sections = [
        section
        for section in [
            tool,
            weapon,
            fuel,
            clothing,
            food,
            container,
            container_contents,
            fluid_container,
            crafting,
            building,
        ]
        if section is not None
    ]

    content = [f"=={usage_header}==\n{call_to_action}"]

    if sections:
        content.extend(sections)

    return "\n\n".join(content)


def create_obtaining(item_data, translation_data):
    """
    Creates the obtaining section.

    Args:
        item_data (dict): Data about the item
        translation_data (dict): Translation data for the current language

    Returns:
        str: The formatted obtaining section, or empty string if no data
    """

    def create_obtaining_recipes():
        """
        Create the recipes subsection for the obtaining section.

        Returns:
            str or None: The formatted recipes section, or None if no recipes found
        """
        item_id = item_data.get("id") or ""
        if not item_id:
            return None

        obtaining_headers = translation_data.get("Obtaining_headers", {})
        recipes_header = obtaining_headers.get("Recipes", "Recipes")
        cache_key = f"{item_id}_howtocraft"
        if cache_key in _crafting_cache:
            content = _crafting_cache[cache_key]
            return f"==={recipes_header}===\n{content}"

        return None

    def create_obtaining_loot():
        """
        Create the loot subsection for the obtaining section.

        Returns:
            str or None: The formatted loot section, or None if no loot distribution found
        """
        item_id_type = item_data.get("id_type") or ""
        if not item_id_type:
            return None

        # Get translated "Loot" header
        obtaining_headers = translation_data.get("Obtaining_headers", {})
        loot_header = obtaining_headers.get("Loot", "Loot")

        if _all_items_data and item_id_type in _all_items_data:
            return f"==={loot_header}===\n{{{{Loot|{item_id_type}}}}}"

        return None

    recipes = create_obtaining_recipes()
    loot = create_obtaining_loot()

    sections = [section for section in [recipes, loot] if section is not None]

    if not sections:
        return ""

    headers = translation_data.get("headers", {})
    obtaining_header = headers.get("Obtaining", "Obtaining")
    content = "\n\n".join(sections)

    return f"=={obtaining_header}==\n{content}"


def create_history(item_data, translation_data):
    """
    Creates the history section.

    Args:
        item_data (dict): Data about the item
        translation_data (dict): Translation data for the current language

    Returns:
        str: The formatted history section
    """
    language_code = item_data.get("language_code", "en")
    headers = translation_data.get("headers", {})
    history_header = headers.get("History", "History")

    item_id_full = item_data.get("id") or ""
    item_id_type = item_data.get("id_type") or ""
    if not item_id_full and not item_id_type:
        return ""

    if language_code != "en":
        return ""

    content = None
    if item_id_full:
        content = _history_cache.get(item_id_full)
    if not content and item_id_type:
        content = _history_cache.get(item_id_type)
    if not content:
        fallback_id = item_id_full or item_id_type
        content = f"{{{{HistoryTable|\n|item_id={fallback_id}\n}}}}"

    return f"=={history_header}==\n{content}"


def create_code(item_data, translation_data):
    """
    Creates the code section.

    Args:
        item_data (dict): Data about the item
        translation_data (dict): Translation data for the current language

    Returns:
        str: The formatted code section
    """
    headers = translation_data.get("headers", {})
    code_header = headers.get("Code", "Code")

    item_id_full = item_data.get("id") or ""
    item_id_type = item_data.get("id_type") or ""
    if not item_id_full and not item_id_type:
        return ""

    inner = None
    if item_id_full:
        inner = _codesnips_cache.get(item_id_full)
    if not inner and item_id_type:
        inner = _codesnips_cache.get(item_id_type)
    if not inner:
        return ""

    code_box = f"{{{{CodeBox|\n{inner}\n}}}}"
    return f"=={code_header}==\n{code_box}"


def create_navigation(translation_data):
    """
    Creates the navigation section.

    Args:
        translation_data (dict): Translation data for the current language

    Returns:
        str: The formatted navigation section
    """
    headers = translation_data.get("headers", {})
    navigation_header = headers.get("Navigation", "Navigation")
    return f"=={navigation_header}==\n{{{{Navbox items}}}}"


def create_articles():
    language_code = Language.get()
    translation_data = load_translations(language_code)

    if not translation_data:
        echo.error(f"No translation data found for language: {language_code}")
        return

    articles_by_id: dict[str, str] = {}

    total_items = Item.count()
    with tqdm(
        total=total_items,
        desc="Generating item articles",
        bar_format=PBAR_FORMAT,
        unit=" items",
    ) as pbar:
        for item in Item.values():
            if not item.valid:
                pbar.update(1)
                continue

            item_data = {
                "name": item.name,
                "id": item.item_id,
                "id_type": item.id_type,
                "language_code": language_code,
            }

            # Sections
            header = create_header(item, translation_data, language_code)
            infobox = create_infobox(item)
            intro = create_intro(item_data, translation_data, language_code)
            usage = create_usage(item_data, translation_data)
            obtaining = create_obtaining(item_data, translation_data)
            history = create_history(item_data, translation_data)
            code = create_code(item_data, translation_data)
            navigation = create_navigation(translation_data)

            # Assemble content
            special_parts = []
            if header:
                special_parts.append(header)
            if infobox:
                special_parts.append(infobox)
            if intro:
                special_parts.append(intro)

            special_section = "\n".join(special_parts) if special_parts else ""

            # Rest of the sections with double newlines
            regular_parts = [
                section
                for section in [
                    usage,
                    obtaining,
                    history,
                    code,
                    navigation,
                ]
                if section
            ]

            # Join everything together
            if special_section and regular_parts:
                content = special_section + "\n\n" + "\n\n".join(regular_parts)
            else:
                content = special_section or "\n\n".join(regular_parts)

            content = content.strip()

            # Use id without module (e.g., remove "Base.")
            file_id = item.id_type
            articles_by_id[file_id] = content

            pbar.set_postfix_str(f"Processing: {file_id}")
            pbar.update(1)

    # Save all generated articles to disk
    output_dir = os.path.join("output", language_code, "item", "articles")
    os.makedirs(output_dir, exist_ok=True)

    for article_id, article_content in articles_by_id.items():
        filename = f"{article_id}.txt"
        path = os.path.join(output_dir, filename)
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(article_content)
        except Exception as e:
            echo.error(f"Error writing '{path}': {e}")


def main():
    Language.init()
    language_code = Language.get()
    echo.info(f"Using language: {language_code}")

    # Load the JSON translation file
    translation_data = load_translations(language_code)
    if not translation_data:
        echo.error("Failed to load translation data. Exiting.")
        return

    # Load page dictionary
    page_dictionary = load_page_dictionary()
    if not page_dictionary:
        echo.error("Failed to load page dictionary. Exiting.")
        return

    load_cache()
    create_articles()

    echo.info("Item article generation completed.")
