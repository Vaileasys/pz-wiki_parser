import os
import json
import re
from scripts.core.constants import DATA_DIR
from scripts.core import config_manager as config
from scripts.utils import echo

suppress_warnings = False

LANGUAGE_CODES = {
    'ar': {"language": "Arabic"},
    'ca': {"language": "Catalan"},
    'zh-hant': {"language": "Traditional Chinese (zh-Hant)", "code": "CH"},
    'zh-hans': {"language": "Simplified Chinese (zh-Hans)", "code": "CN"},
    'cs': {"language": "Czech"},
    'da': {"language": "Danish"},
    'de': {"language": "German"},
    'en': {"language": "English"},
    'es': {"language": "Spanish"},
    'fi': {"language": "Finnish"},
    'fr': {"language": "French"},
    'hu': {"language": "Hungarian"},
    'id': {"language": "Indonesian"},
    'it': {"language": "Italian"},
    'ja': {"language": "Japanese", "code": "JP"},
    'ko': {"language": "Korean"},
    'nl': {"language": "Dutch"},
    'no': {"language": "Norwegian"},
    'ph': {"language": "Filipino"},
    'pl': {"language": "Polish"},
    'pt': {"language": "Portuguese"},
    'pt-br': {"language": "Portuguese (Brazilian)", "code": "PTBR"},
    'ro': {"language": "Romanian"},
    'ru': {"language": "Russian"},
    'th': {"language": "Thai"},
    'tr': {"language": "Turkish"},
    'uk': {"language": "Ukrainian", "code": "UA"}
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
        'DisplayName': "", # Obsolete for JSON translations
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
        "ItemName", "IG_UI", "Recipes", "Tooltip",
        "EvolvedRecipeName", "Fluids", "Wiki", "UI",
        "Print_Text", "Print_Media", "Recorded_Media", "Stash",
        "ContextMenu", "Farming", "Sandbox"
    )


    ## ------------------------- Public Methods ------------------------- ##

    @classmethod
    def get(cls, property_value, property_key=None, lang_code=None, default=None) -> str:
        """Get a translation for a given value, using optional prefix logic."""
        if not property_value:
            return property_value

        cls._ensure_loaded()

        lang_code = lang_code or Language.get()
        if lang_code not in cls._translations:
            if not suppress_warnings:
                echo.warning("No translations loaded for language code:", lang_code)
            return default or property_value

        translations = cls._translations[lang_code]
        key = cls._PROPERTY_PREFIXES.get(property_key, "") + property_value
        
        # Check if key exists
        if key in translations:
            return translations[key].strip()
        
        # Fallback for TeachedRecipes: try without Recipe_ prefix
        if property_key == "TeachedRecipes":
            # Try without prefix
            if property_value in translations:
                return translations[property_value].strip()

            # Try without prefix and without underscores
            value_no_underscore = property_value.replace("_", "")
            if value_no_underscore in translations:
                return translations[value_no_underscore].strip()

        if not suppress_warnings:
            echo.debug(f"Missing translation for key '{key}' or '{property_value}' in language '{lang_code}'")
        
        return (default or property_value).strip()

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
        from scripts.core.version import Version
        from scripts.core.cache import save_cache, load_cache

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
        from scripts.core.file_loading import get_lua_dir
        base_dirs = [
            os.path.join(get_lua_dir(), "shared", "Translate", game_code.upper()),
            os.path.join("resources", "Translate", game_code.upper())
        ]
        if not any(os.path.exists(d) for d in base_dirs):
            raise FileNotFoundError(f"No translation folder: {base_dirs}")

        parsed = {}

        for base_dir in base_dirs:
            for root, _, files in os.walk(base_dir):
                for name in files:
                    if not any(name.startswith(prefix) for prefix in cls._FILE_WHITELIST):
                        continue
                    if not name.endswith(".json"):
                        continue

                    path = os.path.join(root, name)
                    try:
                        with open(path, 'r', encoding="UTF-8") as f:
                            parsed.update(json.load(f))
                    except Exception as e:
                        echo.error(f"JSON error in {name}: {e}")

        return parsed


def main():
    Language.init()