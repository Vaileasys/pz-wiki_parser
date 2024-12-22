from scripts.parser import recipe_parser
from scripts.core import version, translate

def main():
    language_code = translate.get_language_code()
    game_version = version.get_version()
    recipe_parser.main()


if __name__ == "__main__":
    main()