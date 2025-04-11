import re
from pathlib import Path
from scripts.core import config_manager
from scripts.core.version import Version
from scripts.utils import utility

CACHE_FILE = "evolvedrecipe_data.json"

evolvedrecipe_data = {}

def get_evolvedrecipe_data():
    global evolvedrecipe_data
    if not evolvedrecipe_data:
        evolvedrecipe_data = parse_evolved_recipes()
    return evolvedrecipe_data


def remove_comments(content):
    """Removes block and line comments"""
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL) # Block comments
    content = re.sub(r'//.*', '', content) # Line comments
    return content


def parse_evolved_recipes():
    global evolvedrecipe_data

    game_version = Version.get()
    cache_data, cache_version = utility.load_cache(CACHE_FILE, "evolvedrecipe", True)

    # Check if cache is old and should be updated
    if cache_version != game_version:

        game_directory = Path(config_manager.get_config("game_directory"))
        file_path = game_directory / "media" / "scripts" / "evolvedrecipes.txt"

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        content = remove_comments(content)

        # Match all evolvedrecipe blocks
        pattern = re.compile(r"evolvedrecipe\s+(.+?)\s*{(.*?)}", re.DOTALL)
        evolvedrecipe_data = {}

        for match in pattern.finditer(content):
            name = match.group(1).strip()
            body = match.group(2).strip()

            prop_dict = {}
            for line in body.splitlines():
                line = line.strip().rstrip(',')
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    prop_dict[key] = value

            evolvedrecipe_data[name] = prop_dict
        
        utility.save_cache(evolvedrecipe_data, CACHE_FILE)

    else:
        evolvedrecipe_data = cache_data

    return evolvedrecipe_data


if __name__ == "__main__":
    parse_evolved_recipes()
    
    
