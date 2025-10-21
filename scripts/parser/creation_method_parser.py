#!/usr/bin/env python3
"""
Parser for MainCreationMethods.lua file to extract traits and occupations data with translation support.
"""

import os
import re
from scripts.core.cache import save_cache
from scripts.core import file_loading
from scripts.core.language import Translate, Language
from scripts.core import page_manager
from scripts.utils import echo


def determine_trait_type(cost: int) -> str:
    """Determine if a trait is positive or negative based on cost."""
    if cost > 0:
        return "Positive"
    elif cost < 0:
        return "Negative"
    else:
        return "Neutral"


def determine_occupation_points_type(cost: int) -> str:
    """Determine if an occupation cost is positive or negative."""
    if cost > 0:
        return "Positive"
    elif cost < 0:
        return "Negative"
    else:
        return "Neutral"


def generate_trait_infobox(trait_data: dict) -> str:
    """Generate a trait infobox in the specified format."""
    name = trait_data.get("display_name", trait_data.get("name", "Unknown"))
    cost = trait_data.get("cost", 0)
    description = trait_data.get("description", "")
    trait_id = trait_data.get("name", "Unknown")

    # Determine type based on cost
    trait_type = determine_trait_type(cost)

    # Handle mutual exclusions
    mutual_exclusions = trait_data.get("mutual_exclusions", [])
    exclusive_fields = []
    for i, exclusion in enumerate(
        mutual_exclusions[:7], 1
    ):  # Limit to 7 as per template
        trait_name = exclusion.get("name", "")
        translated_name = exclusion.get("translated", trait_name)

        # Get the page name for this trait using the page dictionary
        trait_pages = page_manager.get_pages(trait_name, id_type="trait_id")
        if trait_pages and len(trait_pages) > 0:
            page_name = trait_pages[0]
            # Create a wiki link - use simple format if name and page are the same
            if page_name == translated_name:
                wiki_link = f"[[{page_name}]]"
            else:
                wiki_link = f"[[{page_name}|{translated_name}]]"
        else:
            # Fallback to just the trait name if no page found
            wiki_link = f"[[{trait_name}]]"

        exclusive_fields.append(f"|exclusive{i}={wiki_link}")

    infobox = f"""{{{{Infobox trait
|name={name}
|icon=trait_{trait_id}.png
|effect={description}
|type={trait_type}
|points={abs(cost)}
{chr(10).join(exclusive_fields)}
|trait_id={trait_id}
}}}}"""

    return infobox


def generate_occupation_infobox(occupation_data: dict) -> str:
    """Generate an occupation infobox in the specified format."""
    name = occupation_data.get("display_name", occupation_data.get("name", "Unknown"))
    icon = occupation_data.get("icon", "")
    cost = occupation_data.get("cost", 0)
    occupation_id = occupation_data.get("name", "Unknown")

    # Determine points type based on cost
    points_type = determine_occupation_points_type(cost)

    # Generate effect from XP boosts and free traits
    effects = []

    # Add XP boosts
    xp_boosts = occupation_data.get("xp_boosts", {})
    for perk, level in xp_boosts.items():
        if level > 0:
            # Replace PlantScavenging with Foraging
            perk_name = "Foraging" if perk == "PlantScavenging" else perk
            # Get translated perk name
            translated_perk = (
                Translate.get(f"IGUI_perks_{perk_name}")
                or Translate.get(perk_name, property_key="Perk")
                or perk_name
            )
            effects.append(f"+{level} [[{translated_perk}]]")

    # Add free traits
    free_traits = occupation_data.get("free_traits", [])
    for trait in free_traits:
        if isinstance(trait, dict):
            trait_id = trait.get("id", "")
            trait_name = trait.get("translated", trait_id)
        else:
            # Fallback for old format
            trait_id = trait
            trait_name = trait

        # Get the page name for this trait using the page dictionary
        trait_pages = page_manager.get_pages(trait_id, id_type="trait_id")
        if trait_pages and len(trait_pages) > 0:
            page_name = trait_pages[0]
            # Create a wiki link - use simple format if name and page are the same
            if page_name == trait_name:
                wiki_link = f"[[{page_name}]]"
            else:
                wiki_link = f"[[{page_name}|{trait_name}]]"
        else:
            # Fallback to just the trait name if no page found
            wiki_link = f"[[{trait_name}]]"

        effects.append(wiki_link)

    effect_text = "<br>".join(effects) if effects else ""

    infobox = f"""{{{{Infobox occupation
|name={name}
|icon={icon}.png
|effect={effect_text}
|points_type={points_type}
|points={abs(cost)}
|occupation_id={occupation_id}
}}}}"""

    return infobox


def output_trait_files(traits_data: dict):
    """Output trait infobox files to the output directory."""
    output_dir = os.path.join("output", "en", "traits", "infoboxes")
    os.makedirs(output_dir, exist_ok=True)

    for trait_name, trait_data in traits_data.items():
        # Get the page name for this trait using the page dictionary
        trait_pages = page_manager.get_pages(trait_name, id_type="trait_id")
        if trait_pages and len(trait_pages) > 0:
            filename = f"{trait_pages[0]}.txt"
        else:
            # Fallback to raw trait name if no page found
            filename = f"{trait_name}.txt"

        infobox_content = generate_trait_infobox(trait_data)
        filepath = os.path.join(output_dir, filename)

        try:
            # Remove empty lines and clean up the content
            cleaned_content = "\n".join(
                line for line in infobox_content.split("\n") if line.strip()
            )
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
            echo.info(f"Generated trait file: {filename}")
        except Exception as e:
            echo.error(f"Failed to write trait file {filename}: {e}")


def output_occupation_files(occupations_data: dict):
    """Output occupation infobox files to the output directory."""
    output_dir = os.path.join("output", "en", "occupations", "infoboxes")
    os.makedirs(output_dir, exist_ok=True)

    for occupation_name, occupation_data in occupations_data.items():
        # Get the page name for this occupation using the page dictionary
        occupation_pages = page_manager.get_pages(
            occupation_name, id_type="occupation_id"
        )
        if occupation_pages and len(occupation_pages) > 0:
            filename = f"{occupation_pages[0]}.txt"
        else:
            # Fallback to raw occupation name if no page found
            filename = f"{occupation_name}.txt"

        infobox_content = generate_occupation_infobox(occupation_data)
        filepath = os.path.join(output_dir, filename)

        try:
            # Remove empty lines and clean up the content
            cleaned_content = "\n".join(
                line for line in infobox_content.split("\n") if line.strip()
            )
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
            echo.info(f"Generated occupation file: {filename}")
        except Exception as e:
            echo.error(f"Failed to write occupation file {filename}: {e}")


def output_recipe_files(data: dict):
    """Output recipe files for traits and occupations to the output directory."""
    traits_data = data.get("traits", {})
    occupations_data = data.get("occupations", {})

    # Create recipe files for traits
    trait_recipe_dir = os.path.join("output", "en", "traits", "recipes")
    os.makedirs(trait_recipe_dir, exist_ok=True)

    for trait_name, trait_data in traits_data.items():
        # Get the page name for this trait using the page dictionary
        trait_pages = page_manager.get_pages(trait_name, id_type="trait_id")
        if trait_pages and len(trait_pages) > 0:
            filename = f"{trait_pages[0]}.txt"
        else:
            # Fallback to raw trait name if no page found
            filename = f"{trait_name}.txt"

        # Get free recipes for this trait
        free_recipes = trait_data.get("free_recipes", [])

        if free_recipes:
            # Format recipes with * prefix
            recipe_content = "\n".join(f"* {recipe}" for recipe in free_recipes)

            filepath = os.path.join(trait_recipe_dir, filename)

            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(recipe_content)
                echo.info(f"Generated trait recipe file: {filename}")
            except Exception as e:
                echo.error(f"Failed to write trait recipe file {filename}: {e}")

    # Create recipe files for occupations
    occupation_recipe_dir = os.path.join("output", "en", "occupations", "recipes")
    os.makedirs(occupation_recipe_dir, exist_ok=True)

    for occupation_name, occupation_data in occupations_data.items():
        # Get the page name for this occupation using the page dictionary
        occupation_pages = page_manager.get_pages(
            occupation_name, id_type="occupation_id"
        )
        if occupation_pages and len(occupation_pages) > 0:
            filename = f"{occupation_pages[0]}.txt"
        else:
            # Fallback to raw occupation name if no page found
            filename = f"{occupation_name}.txt"

        # Get free recipes for this occupation
        free_recipes = occupation_data.get("free_recipes", [])

        if free_recipes:
            # Format recipes with * prefix
            recipe_content = "\n".join(f"* {recipe}" for recipe in free_recipes)

            filepath = os.path.join(occupation_recipe_dir, filename)

            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(recipe_content)
                echo.info(f"Generated occupation recipe file: {filename}")
            except Exception as e:
                echo.error(f"Failed to write occupation recipe file {filename}: {e}")


def remove_comments(lua_content: str) -> str:
    """
    Remove both single-line and multi-line comments from Lua code.

    Args:
        lua_content (str): Raw Lua file content

    Returns:
        str: Lua content with comments removed
    """
    # Remove single-line comments (--)
    # This regex matches -- followed by anything until end of line
    lua_content = re.sub(r"--.*$", "", lua_content, flags=re.MULTILINE)

    # Remove multi-line comments ([[ ... ]] and --[[ ... ]])
    # Handle [[ ... ]] style comments first
    lua_content = re.sub(r"\[\[.*?\]\]", "", lua_content, flags=re.DOTALL)

    # Handle --[[ ... ]] style comments
    lua_content = re.sub(r"--\[\[.*?\]\]", "", lua_content, flags=re.DOTALL)

    return lua_content


def parse_trait_factory_calls(lua_content: str) -> dict:
    """
    Parse TraitFactory.addTrait calls to extract trait data.

    Args:
        lua_content (str): Lua content with comments removed

    Returns:
        dict: Structured traits data
    """
    traits = {}

    # Pattern to match TraitFactory.addTrait calls
    # Captures: trait_name, display_name, cost, description, is_profession_trait
    trait_pattern = r'TraitFactory\.addTrait\("([^"]+)",\s*getText\("([^"]+)"\),\s*([^,]+),\s*getText\("([^"]+)"\),\s*([^)]+)\)'

    # Find all trait definitions
    trait_matches = re.findall(trait_pattern, lua_content)

    for match in trait_matches:
        trait_name, display_name_key, cost, description_key, is_profession = match

        # Get translations for display name and description
        # Try using the full keys directly first, then fall back to processed keys
        display_name = (
            Translate.get(display_name_key)
            or Translate.get(
                display_name_key.replace("UI_trait_", ""), property_key="Trait"
            )
            or display_name_key.replace("UI_trait_", "")
        )
        description = (
            Translate.get(description_key)
            or Translate.get(
                description_key.replace("UI_trait_", ""), property_key="Trait"
            )
            or description_key.replace("UI_trait_", "Desc").replace("desc", "Desc")
        )

        traits[trait_name] = {
            "name": trait_name,
            "display_name": display_name,
            "display_name_key": display_name_key,
            "cost": int(cost.strip()),
            "description": description,
            "description_key": description_key,
            "is_profession_trait": is_profession.strip().lower() == "true",
            "xp_boosts": {},
            "free_recipes": [],
            "mutual_exclusions": [],
        }

    return traits


def parse_trait_xp_boosts(lua_content: str, traits: dict) -> None:
    """
    Parse XP boost assignments for traits.

    Args:
        lua_content (str): Lua content with comments removed
        traits (dict): Traits dictionary to update
    """
    # Pattern to match handy:addXPBoost(Perks.Xxx, level) calls
    xp_pattern = r"(\w+):addXPBoost\(Perks\.([^,]+),\s*([^)]+)\)"

    xp_matches = re.findall(xp_pattern, lua_content)

    for trait_var, perk_name, level in xp_matches:
        # Find which trait this variable refers to by looking for the trait assignment
        # Look for patterns like: local handy = TraitFactory.addTrait(...)
        trait_var_pattern = (
            rf'local\s+{trait_var}\s*=\s*TraitFactory\.addTrait\("([^"]+)"'
        )

        trait_match = re.search(trait_var_pattern, lua_content)
        if trait_match:
            trait_name = trait_match.group(1)
            if trait_name in traits:
                # Convert perk name from CamelCase to proper format
                perk_name_clean = perk_name.strip()
                try:
                    level_int = int(level.strip())
                    traits[trait_name]["xp_boosts"][perk_name_clean] = level_int
                except ValueError:
                    echo.warning(f"Could not parse XP boost level: {level}")


def parse_trait_free_recipes(lua_content: str, traits: dict) -> None:
    """
    Parse free recipe assignments for traits.

    Args:
        lua_content (str): Lua content with comments removed
        traits (dict): Traits dictionary to update
    """
    # Pattern to match getFreeRecipes():add("recipe") calls
    recipe_pattern = r'(\w+):getFreeRecipes\(\):add\("([^"]+)"\)'

    recipe_matches = re.findall(recipe_pattern, lua_content)

    for trait_var, recipe_name in recipe_matches:
        # Find which trait this variable refers to
        trait_var_pattern = (
            rf'local\s+{trait_var}\s*=\s*TraitFactory\.addTrait\("([^"]+)"'
        )

        trait_match = re.search(trait_var_pattern, lua_content)
        if trait_match:
            trait_name = trait_match.group(1)
            if trait_name in traits:
                # Get recipe translation
                translated_recipe = (
                    Translate.get(recipe_name, property_key="TeachedRecipes")
                    or recipe_name
                )
                traits[trait_name]["free_recipes"].append(translated_recipe)


def parse_mutual_exclusions(lua_content: str, traits: dict) -> None:
    """
    Parse mutual exclusion rules for traits.

    Args:
        lua_content (str): Lua content with comments removed
        traits (dict): Traits dictionary to update
    """
    # Pattern to match TraitFactory.setMutualExclusive calls
    exclusion_pattern = r'TraitFactory\.setMutualExclusive\("([^"]+)",\s*"([^"]+)"\)'

    exclusion_matches = re.findall(exclusion_pattern, lua_content)

    for trait1, trait2 in exclusion_matches:
        if trait1 in traits:
            # Get translation for mutual exclusion - use trait name without UI_trait_ prefix
            translated_trait2 = Translate.get(trait2, property_key="Trait") or trait2
            traits[trait1]["mutual_exclusions"].append(
                {"name": trait2, "translated": translated_trait2}
            )
        if trait2 in traits:
            # Get translation for mutual exclusion - use trait name without UI_trait_ prefix
            translated_trait1 = Translate.get(trait1, property_key="Trait") or trait1
            traits[trait2]["mutual_exclusions"].append(
                {"name": trait1, "translated": translated_trait1}
            )


def parse_profession_factory_calls(lua_content: str) -> dict:
    """
    Parse ProfessionFactory.addProfession calls to extract profession data.

    Args:
        lua_content (str): Lua content with comments removed

    Returns:
        dict: Structured professions data
    """
    professions = {}

    # Pattern to match ProfessionFactory.addProfession calls
    prof_pattern = r'ProfessionFactory\.addProfession\("([^"]+)",\s*getText\("([^"]+)"\),\s*"([^"]+)",\s*([^)]+)\)'

    prof_matches = re.findall(prof_pattern, lua_content)

    for match in prof_matches:
        prof_name, display_name_key, icon, cost = match

        # Get translation for profession display name
        # Try using the full keys directly first, then fall back to processed keys
        display_name = (
            Translate.get(display_name_key)
            or Translate.get(display_name_key.replace("UI_prof_", ""))
            or display_name_key.replace("UI_prof_", "")
        )

        professions[prof_name] = {
            "name": prof_name,
            "display_name": display_name,
            "display_name_key": display_name_key,
            "icon": icon,
            "cost": int(cost.strip()),
            "xp_boosts": {},
            "free_traits": [],
            "free_recipes": [],
        }

    return professions


def parse_profession_xp_boosts(lua_content: str, professions: dict) -> None:
    """
    Parse XP boost assignments for professions.

    Args:
        lua_content (str): Lua content with comments removed
        professions (dict): Professions dictionary to update
    """
    # Pattern to match prof:addXPBoost(Perks.Xxx, level) calls
    prof_xp_pattern = r"(\w+):addXPBoost\(Perks\.([^,]+),\s*([^)]+)\)"

    xp_matches = re.findall(prof_xp_pattern, lua_content)

    for prof_var, perk_name, level in xp_matches:
        # Find which profession this variable refers to
        prof_var_pattern = (
            rf'local\s+{prof_var}\s*=\s*ProfessionFactory\.addProfession\("([^"]+)"'
        )

        prof_match = re.search(prof_var_pattern, lua_content)
        if prof_match:
            prof_name = prof_match.group(1)
            if prof_name in professions:
                perk_name_clean = perk_name.strip()
                try:
                    level_int = int(level.strip())
                    professions[prof_name]["xp_boosts"][perk_name_clean] = level_int
                except ValueError:
                    echo.warning(f"Could not parse profession XP boost level: {level}")


def parse_profession_free_traits(lua_content: str, professions: dict) -> None:
    """
    Parse free trait assignments for professions.

    Args:
        lua_content (str): Lua content with comments removed
        professions (dict): Professions dictionary to update
    """
    # Pattern to match prof:addFreeTrait("trait") calls
    trait_pattern = r'(\w+):addFreeTrait\("([^"]+)"\)'

    trait_matches = re.findall(trait_pattern, lua_content)

    for prof_var, trait_name in trait_matches:
        # Find which profession this variable refers to
        prof_var_pattern = (
            rf'local\s+{prof_var}\s*=\s*ProfessionFactory\.addProfession\("([^"]+)"'
        )

        prof_match = re.search(prof_var_pattern, lua_content)
        if prof_match:
            prof_name = prof_match.group(1)
            if prof_name in professions:
                # Get trait translation
                translated_trait = (
                    Translate.get(trait_name, property_key="Trait") or trait_name
                )
                professions[prof_name]["free_traits"].append(
                    {"id": trait_name, "translated": translated_trait}
                )


def parse_profession_free_recipes(lua_content: str, professions: dict) -> None:
    """
    Parse free recipe assignments for professions.

    Args:
        lua_content (str): Lua content with comments removed
        professions (dict): Professions dictionary to update
    """
    # Pattern to match prof:getFreeRecipes():add("recipe") calls
    recipe_pattern = r'(\w+):getFreeRecipes\(\):add\("([^"]+)"\)'

    recipe_matches = re.findall(recipe_pattern, lua_content)

    for prof_var, recipe_name in recipe_matches:
        # Find which profession this variable refers to
        prof_var_pattern = (
            rf'local\s+{prof_var}\s*=\s*ProfessionFactory\.addProfession\("([^"]+)"'
        )

        prof_match = re.search(prof_var_pattern, lua_content)
        if prof_match:
            prof_name = prof_match.group(1)
            if prof_name in professions:
                # Get recipe translation
                translated_recipe = (
                    Translate.get(recipe_name, property_key="TeachedRecipes")
                    or recipe_name
                )
                professions[prof_name]["free_recipes"].append(translated_recipe)


def parse_lua_file() -> dict:
    """
    Main function to parse the Lua file and extract traits and occupations data.

    Returns:
        dict: Complete parsed data with traits and occupations
    """
    # Initialize language system for translations
    Language.init()

    # Path to the Lua file (assuming it's in the expected location)
    lua_file_path = os.path.join("resources", "lua", "MainCreationMethods.lua")

    if not os.path.exists(lua_file_path):
        echo.error(f"Lua file not found: {lua_file_path}")
        return {}

    # Read and parse the Lua file
    try:
        with open(lua_file_path, "r", encoding="utf-8") as f:
            lua_content = f.read()

        # Remove comments
        lua_content = remove_comments(lua_content)

        # Parse traits
        traits = parse_trait_factory_calls(lua_content)
        parse_trait_xp_boosts(lua_content, traits)
        parse_trait_free_recipes(lua_content, traits)
        parse_mutual_exclusions(lua_content, traits)

        # Parse professions
        professions = parse_profession_factory_calls(lua_content)
        parse_profession_xp_boosts(lua_content, professions)
        parse_profession_free_traits(lua_content, professions)
        parse_profession_free_recipes(lua_content, professions)

        # Combine into final result
        result = {"traits": traits, "occupations": professions}

        echo.success(
            f"Parsed {len(traits)} traits and {len(professions)} occupations from {lua_file_path}"
        )
        return result

    except Exception as e:
        echo.error(f"Error parsing Lua file: {e}")
        return {}


def main():
    """Main function to run the parser and save the cache."""
    echo.info("Starting MainCreationMethods.lua parser...")

    # Parse the Lua file
    data = parse_lua_file()

    if not data:
        echo.error("No data parsed from Lua file")
        return

    # Save to cache
    cache_file = "creation_methods"
    save_cache(data, cache_file, suppress=False)

    # Output trait and occupation files
    traits_data = data.get("traits", {})
    occupations_data = data.get("occupations", {})

    echo.info("Generating trait and occupation infobox files...")
    output_trait_files(traits_data)
    output_occupation_files(occupations_data)

    echo.info("Generating recipe files...")
    output_recipe_files(data)

    echo.success(f"Successfully parsed and cached creation methods data")
