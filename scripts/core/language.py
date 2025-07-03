import os
import json
import re
from scripts.core.constants import DATA_DIR
from scripts.core.version import Version
from scripts.core import config_manager as config
from scripts.utils import echo
from scripts.core.cache import save_cache, load_cache

LANGUAGE_CODES = {
    'ar': {"encoding": "CP1252", "language": "Arabic"},
    'ca': {"encoding": "ISO-8859-15", "language": "Catalan"},
    'zh-hant': {"encoding": "UTF-8", "language": "Traditional Chinese (zh-Hant)", "code": "CH"},
    'zh-hans': {"encoding": "UTF-8", "language": "Simplified Chinese (zh-Hans)", "code": "CN"},
    'cs': {"encoding": "Cp1250", "language": "Czech"},
    'da': {"encoding": "UTF-8", "language": "Danish"},
    'de': {"encoding": "UTF-8", "language": "German"},
    'en': {"encoding": "UTF-8", "language": "English"},
    'es': {"encoding": "UTF-8", "language": "Spanish"},
    'fi': {"encoding": "UTF-8", "language": "Finnish"},
    'fr': {"encoding": "UTF-8", "language": "French"},
    'hu': {"encoding": "UTF-8", "language": "Hungarian"},
    'id': {"encoding": "UTF-8", "language": "Indonesian"},
    'it': {"encoding": "UTF-8", "language": "Italian"},
    'ja': {"encoding": "UTF-8", "language": "Japanese", "code": "JP"},
    'ko': {"encoding": "UTF-16", "language": "Korean"},
    'nl': {"encoding": "UTF-8", "language": "Dutch"},
    'no': {"encoding": "UTF-8", "language": "Norwegian"},
    'ph': {"encoding": "UTF-8", "language": "Filipino"},
    'pl': {"encoding": "UTF-8", "language": "Polish"},
    'pt': {"encoding": "UTF-8", "language": "Portuguese"},
    'pt-br': {"encoding": "UTF-8", "language": "Portuguese (Brazilian)", "code": "PTBR"},
    'ro': {"encoding": "UTF-8", "language": "Romanian"},
    'ru': {"encoding": "UTF-8", "language": "Russian"},
    'th': {"encoding": "UTF-8", "language": "Thai"},
    'tr': {"encoding": "UTF-8", "language": "Turkish"},
    'uk': {"encoding": "UTF-8", "language": "Ukrainian", "code": "UA"}
}

class Language:
    _language_code = None
    _default_language = None
    _language_code_subpage = None


    ## ------------------------- Language Code and Config ------------------------- ##

    @classmethod
    def get(cls):
        if cls._language_code is None:
            cls.init()
        return cls._language_code

    @classmethod
    def set(cls, code):
        cls._language_code = code
        cls._language_code_subpage = None # reset subpage

    @classmethod
    def reset(cls):
        cls._language_code = None
        cls._language_code_subpage = None
        cls.init()

    @classmethod
    def get_default(cls):
        if cls._default_language is None:
            cls.update_default()
        return cls._default_language
    
    @classmethod
    def get_subpage(cls):
        if cls._language_code_subpage is None:
            cls.set_subpage(cls.get())
        return cls._language_code_subpage

    @classmethod
    def set_subpage(cls, code):
        cls._language_code_subpage = f"/{code}" if code != "en" else ""
        return cls._language_code_subpage

    @classmethod
    def set_default(cls, code):
        cls._default_language = code

    @classmethod
    def update_default(cls):
        cls._default_language = config.get_default_language()
        return cls._default_language

    @classmethod
    def init(cls):
        echo.info("Initialising language")
        cls.update_default()
        cls._language_code = cls._prompt()
        cls.set_subpage(cls._language_code)
        Translate.load()

    @classmethod
    def _prompt(cls):
        code = input(f"Enter language code (default '{cls._default_language}')\n> ").strip().lower()
        if code not in LANGUAGE_CODES:
            echo.info(f"Unrecognised language code, defaulting to '{cls._default_language}'")
            code = cls._default_language
        echo.info(f"Language set to '{code}' ({cls.get_language_name(code)})")
        return code

    @staticmethod
    def get_encoding(code):
        return LANGUAGE_CODES.get(code, {}).get("encoding", "UTF-8")

    @staticmethod
    def get_language_name(code):
        return LANGUAGE_CODES.get(code, {}).get("language", "Unknown")

    @staticmethod
    def get_game_code(wiki_code):
        return LANGUAGE_CODES.get(wiki_code, {}).get("code", wiki_code)


class Translate:
    _translations = {}
    _cache_loaded = False
    _CACHE_JSON = "translations_data.json"

    _PROPERTY_PREFIXES = {
        'DisplayName': "ItemName_",
        'DisplayCategory': "IGUI_ItemCat_",
        'Categories': "IGUI_perks_",
        'SubCategory': "IGUI_perks_",
        'SkillTrained': "IGUI_perks_",
        'Perk': 'IGUI_perks_',
        'BodyPart': "IGUI_health_",
        'Photo': "IGUI_Photo_",
        'Doodle': "IGUI_Doodle_",
        'PrintText': "Print_Text_",
        'PrintMedia': "Print_Media_",
        'MagazineTitle': "IGUI_MagazineTitle_",
        'NewspaperTitle': "IGUI_NewspaperTitle_",
        'ComicTitle': "IGUI_ComicTitle_",
        'BookTitle': "IGUI_BookTitle_",
        'RPG': "IGUI_RPG_",
        'IGUI': 'IGUI_',
        'TeachedRecipes': "Recipe_",
        'PartType': "Tooltip_weapon_",
        'EvolvedRecipeName': "EvolvedRecipeName_",
        'FluidID': "Fluid_Name_",
        'ContainerName': 'Fluid_Container_',
        'Wiki': 'Wiki_',
        'Trait': 'UI_trait_'
    }

    _FILE_WHITELIST = (
        "ItemName_", "IG_UI_", "Recipes_", "Tooltip_",
        "EvolvedRecipeName_", "Fluids_", "Wiki_", "UI_",
        "Print_Text_", "Print_Media_", "Recorded_Media_", "Stash_",
        "ContextMenu_", "Farming_", "Sandbox_"
    )


    ## ------------------------- Public Methods ------------------------- ##

    @classmethod
    def get(cls, property_value, property_key=None, lang_code=None, default=None):
        """Get a translation for a given value, using optional prefix logic."""
        if not property_value:
            return property_value

        cls._ensure_loaded()

        lang_code = lang_code or Language.get()
        if lang_code not in cls._translations:
            return default or property_value

        translations = cls._translations[lang_code]
        key = cls._PROPERTY_PREFIXES.get(property_key, "") + property_value
        return translations.get(key, default or property_value).strip()

    @classmethod
    def get_wiki(cls, value: str) -> str:
        """Translate all wiki-style placeholders (<< >>) inside a string."""
        placeholders = re.findall(r'\<\<(.*?)\>\>', value)
        for ph in placeholders:
            translated = cls.get(ph, property_key="Wiki")
            value = value.replace(f'<<{ph}>>', translated)
        return value

    @classmethod
    def load(cls):
        """Force-load all translation data, bypassing lazy init."""
        if not cls._cache_loaded:
            cls._cache()
            cls._cache_loaded = True


    ## ------------------------- Caching Logic ------------------------- ##

    @classmethod
    def _ensure_loaded(cls):
        if not cls._cache_loaded:
            cls.load()

    @classmethod
    def _cache(cls):

        cache_path = os.path.join(DATA_DIR, cls._CACHE_JSON)
        cls._translations, cache_version = load_cache(cache_path, "translation", get_version=True)

        if cache_version != Version.get():
            for wiki_code in LANGUAGE_CODES:
                try:
                    game_code = Language.get_game_code(wiki_code)
                    parsed = cls._parse(wiki_code, game_code)
                    cls._translations[wiki_code] = parsed
                except Exception as e:
                    echo.warning(f"Failed to load {wiki_code}: {e}")

            save_cache(cls._translations, cls._CACHE_JSON, suppress=True)

    @classmethod
    def _parse(cls, wiki_code, game_code):
        base_dir = os.path.join("resources", "Translate", game_code.upper())
        if not os.path.exists(base_dir):
            raise FileNotFoundError(f"No translation folder: {base_dir}")

        parsed = {}
        encoding = Language.get_encoding(wiki_code)

        for root, _, files in os.walk(base_dir):
            for name in files:
                if not any(name.startswith(prefix) for prefix in cls._FILE_WHITELIST):
                    continue

                path = os.path.join(root, name)
                if name.endswith(".json"):
                    try:
                        with open(path, 'r', encoding="UTF-8") as f:
                            parsed.update(json.load(f))
                    except Exception as e:
                        echo.error(f"JSON error in {name}: {e}")
                    continue

                try:
                    with open(path, 'r', encoding=encoding) as f:
                        for line in f:
                            line = cls._remove_comments(line).strip()
                            if '=' not in line or '{' in line or '}' in line:
                                continue
                            key, val = [x.strip() for x in line.split('=', 1)]
                            if val.endswith(','): val = val[:-1].strip()
                            if val.startswith('"'): val = val[1:]
                            if val.endswith('"'): val = val[:-1]
                            parsed[key] = val
                except UnicodeDecodeError as e:
                    echo.error(f"Couldn't decode {name}: {e}")
                except Exception as e:
                    echo.error(f"TXT error in {name}: {e}")

        return parsed


    ## ------------------------- Helpers ------------------------- ##

    @staticmethod
    def _remove_comments(line: str) -> str:
        if line.strip().startswith('--'):
            return ''
        return re.split(r'--', line, maxsplit=1)[0].strip()

def main():
    Language.init()