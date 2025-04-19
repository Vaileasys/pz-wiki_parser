from scripts.parser.script_parser import extract_script_data
from scripts.utils.echo import echo, echo_info, echo_warning, echo_error,  echo_success


def main():
    try:
        echo_info("Extracting recipes")
        extract_script_data("craftRecipe")
        extract_script_data("entity")
        echo_success("Recipes extracted")
    except Exception:
        echo_error("An error occurred while extracting recipes")

