import os
from tqdm import tqdm
from scripts.objects.fluid import Fluid
from scripts.core.constants import PBAR_FORMAT, FLUID_DIR
from scripts.core.file_loading import write_file
from scripts.utils import echo
from scripts.core import logger
from scripts.core.language import Language, Translate


def are_fluids_compatible(fluid1: Fluid, fluid2: Fluid) -> bool:
    """
    Check if two fluids are compatible for mixing.

    Rules:
    1. All fluids are compatible with themselves
    2. If neither fluid has a whitelist, they are compatible
    3. If a fluid has a whitelist, it only allows fluids with categories in its whitelist
    4. Both fluids must allow each other (if they have whitelists)
    """
    # All fluids are compatible with themselves
    if fluid1.fluid_id == fluid2.fluid_id:
        return True

    # Check if either fluid has a whitelist
    fluid1_has_whitelist = fluid1.blend_whitelist.whitelist
    fluid2_has_whitelist = fluid2.blend_whitelist.whitelist

    # If neither has a whitelist, they are compatible
    if not fluid1_has_whitelist and not fluid2_has_whitelist:
        return True

    # Check if fluid1 allows fluid2 (if fluid1 has a whitelist)
    fluid1_allows_fluid2 = True
    if fluid1_has_whitelist:
        # If whitelist is empty, it doesn't allow anything
        if not fluid1.blend_whitelist.categories:
            fluid1_allows_fluid2 = False
        else:
            fluid2_categories = set(fluid2.categories)
            fluid1_allows_fluid2 = any(
                cat in fluid1.blend_whitelist.categories for cat in fluid2_categories
            )

    # Check if fluid2 allows fluid1 (if fluid2 has a whitelist)
    fluid2_allows_fluid1 = True
    if fluid2_has_whitelist:
        # If whitelist is empty, it doesn't allow anything
        if not fluid2.blend_whitelist.categories:
            fluid2_allows_fluid1 = False
        else:
            fluid1_categories = set(fluid1.categories)
            fluid2_allows_fluid1 = any(
                cat in fluid2.blend_whitelist.categories for cat in fluid1_categories
            )

    # Both fluids must allow each other
    return fluid1_allows_fluid2 and fluid2_allows_fluid1


def sort_fluids(fluids):
    """Sort fluids by first category, then alphabetically, with water fluids first"""
    water_fluids = ["Base.Water", "Base.TaintedWater", "Base.CarbonatedWater"]

    def get_sort_key(fluid):
        # Water fluids get highest priority
        if fluid.fluid_id in water_fluids:
            return (0, water_fluids.index(fluid.fluid_id))

        # Get first category, default to empty string if no categories
        first_category = fluid.categories[0] if fluid.categories else ""

        # Sort by category priority, then alphabetically
        category_priority = {
            "Beverage": 1,
            "Water": 2,
            "Acid": 3,
            "Hazardous": 4,
            "Fuel": 5,
            "Medical": 6,
            "Food": 7,
            "Chemical": 8,
            "Paint": 9,
            "Oil": 10,
            "Alcohol": 11,
            "Poison": 12,
            "Cleaning": 13,
            "Industrial": 14,
            "Agricultural": 15,
            "Construction": 16,
            "Automotive": 17,
            "Household": 18,
            "Personal": 19,
            "Entertainment": 20,
            "Communication": 21,
            "Security": 22,
            "Recreation": 23,
            "Transportation": 24,
            "Utility": 25,
            "Miscellaneous": 26,
            "": 999,  # No category gets lowest priority
        }

        priority = category_priority.get(first_category, 999)
        return (priority, fluid.fluid_id)

    return sorted(fluids, key=get_sort_key)


def generate_compatibility_table():
    """Generate the compatibility table content"""
    fluids = sort_fluids(list(Fluid.values()))

    # Generate table header
    content = []
    content.append(
        '{| class="wikitable theme-red sortable sticky-column" style="text-align: center;"'
    )
    content.append("|-")
    content.append("! Fluid")

    # Add column headers
    header_line = "! " + " || ".join(fluid.wiki_link for fluid in fluids)
    content.append(header_line)

    # Generate table rows
    for fluid1 in tqdm(
        fluids,
        desc="Generating compatibility table",
        unit=" fluids",
        bar_format=PBAR_FORMAT,
    ):
        content.append("|-")
        content.append(f"! {fluid1.wiki_link}")

        # Check compatibility with each other fluid
        compatibility_cells = []
        for fluid2 in fluids:
            if are_fluids_compatible(fluid1, fluid2):
                compatibility_cells.append("[[File:UI_Tick.png|20px]]")
            else:
                compatibility_cells.append("[[File:UI_Cross.png|20px]]")

        # Join all compatibility cells with ||
        row_line = "| " + " || ".join(compatibility_cells)
        content.append(row_line)

    content.append("|}")

    return content


def main():
    """Main function to generate the fluid compatibility table"""
    echo.write("Generating fluid compatibility table...")

    OUTPUT_DIR = os.path.join(FLUID_DIR.format(language_code=Language.get()),)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        content = generate_compatibility_table()

        # Write to file
        filename = "fluid_compatibility_table.txt"
        write_file(content, rel_path=filename, root_path=OUTPUT_DIR, suppress=True)

        echo.success(f"Fluid compatibility table generated successfully!")
        echo.write(f"Output saved to: {os.path.join(OUTPUT_DIR, filename)}")

    except Exception as e:
        logger.write(
            "Error generating fluid compatibility table",
            True,
            exception=e,
            category="error",
        )
        echo.error(f"Failed to generate compatibility table: {e}")


if __name__ == "__main__":
    main()
