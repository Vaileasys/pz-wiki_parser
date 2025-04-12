from pathlib import Path
from tqdm import tqdm
from scripts.parser import item_parser, distribution_container_parser
from scripts.core.language import Language
from scripts.core.constants import (PBAR_FORMAT, OUTPUT_PATH)
from scripts.utils import utility
from scripts.core.cache import save_cache

TABLE_HEADER = (
    '{{| class="wikitable theme-red sortable mw-collapsible{wiki_class}" id="contents-{item_id}"',
    '! Icon',
    '! Name',
    '! Chance')

TABLE_CAPTION = '|+ style="white-space:nowrap; border:none; font-weight:normal; font-size: 1em;" | '

TABLE_FOOTER = "|}"

distribution_data = distribution_container_parser.get_distribution_data()
language_code = Language.get()
output_dir = Path(OUTPUT_PATH) / language_code.lower() / "container_contents"


def get_probabilities(container_data):

    def calculate_probabilities(items_list, total_rolls, only_one=False):
        """Calculates the probability of each item appearing at least once."""
        item_weights = {}
        total_weight = 0

        # Combine duplicate items, adding weights
        for i in range(0, len(items_list), 2):
            item_name = items_list[i]
            item_weight = items_list[i + 1]

            if item_name in item_weights:
                item_weights[item_name] += item_weight
            else:
                item_weights[item_name] = item_weight

            total_weight += item_weight

        # Calculate probability
        probabilities = {}
        for item_name, item_weight in item_weights.items():
            if total_weight > 0:
                if only_one:
                    # onlyOne = true
                    probability = (item_weight / total_weight) * 100
                    probability = round(probability, 2)
                else:
                    # Normal calculation
                    single_roll_prob = item_weight / total_weight
                    probability = 1 - (1 - single_roll_prob) ** total_rolls
                    probability = round(probability * 100, 2)
            else:
                probability = 0

            probabilities[item_name] = probability

        return probabilities

    # Extract item content data
    rolls = container_data.get("rolls", 1)
    junk_data = container_data.get("junk", {})
    junk_rolls = junk_data.get("rolls", 0)
    junk_items = junk_data.get("items", [])
    item_list = container_data.get("items", [])
    only_one = container_data.get("onlyOne", False)

    # Calculate probabilities
    normal_items = calculate_probabilities(item_list, rolls, only_one)
    junk_items_dict = calculate_probabilities(junk_items, junk_rolls, only_one=False)

    combined_probabilities = {}

    # Combine items and junk
    all_items = set(normal_items.keys()).union(set(junk_items_dict.keys()))

    for item in all_items:
        normal_prob = normal_items.get(item, 0) / 100
        junk_prob = junk_items_dict.get(item, 0) / 100

        combined_prob = normal_prob + junk_prob - (normal_prob * junk_prob) # P(A or B)
        combined_prob = round(combined_prob * 100, 2) # Convert to percentage with 2 decimal places
        combined_prob = min(combined_prob, 100) # Cap at 100%

        combined_probabilities[item] = combined_prob

    return {
        "items": combined_probabilities
#        "junk": junk_prob
        }


def find_distro_key(search_dict, search_key):
    for parent, sub_dict in search_dict.items():
        if search_key in sub_dict:
            return parent
    return None


def process_item(item_type, pbar):
    has_distro = False
    item_probabilities = {}

    distro_key = find_distro_key(distribution_data, item_type)
    if distro_key:
        has_distro = True
        container_contents = distribution_data[distro_key].get(item_type)
        if not container_contents:
            pbar.write(f"{item_type} has no 'items'")
        else:
            item_probabilities = get_probabilities(container_contents)

    return has_distro, item_probabilities


def get_items():
    container_dict = {}
    parsed_item_data = item_parser.get_item_data()

    # Get items
    with tqdm(total=len(parsed_item_data), desc="Processing items", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item_data in parsed_item_data.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")
            if item_data.get("Type") == "Container":
                item_type = item_id.split(".")[1]
                has_distro, item_contents = process_item(item_type, pbar)

                if not has_distro:
                    pbar.update(1)
                    continue

                container_dict[item_id] = item_contents

            pbar.update(1)

        pbar.bar_format = f"Items processed."
           
    return container_dict


def write_to_file(data):
    content_item_cache = {}

    output_dir.mkdir(parents=True, exist_ok=True)
    with tqdm(total=len(data), desc="Writing items", bar_format=PBAR_FORMAT, unit=" items") as pbar:
        for item_id, item_lists in data.items():
            pbar.set_postfix_str(f"Processing: {item_id[:30]}")

            if not item_lists.get("items"):
                pbar.write(f"Skipping '{item_id}': Has no items.")
                continue

            output_file = output_dir / f"contents-{item_id}.txt"

            table = []

            if len(item_lists.get("items")) > 10:
                wiki_class = " mw-collapsed"
            else:
                wiki_class = ""
            table_header_mod = "\n".join(TABLE_HEADER).format(wiki_class=wiki_class, item_id=item_id)

            table.append(table_header_mod)

            table_caption_mod = TABLE_CAPTION + item_id

            table.append(table_caption_mod)

            item_lists["items"] = dict(sorted(item_lists["items"].items(), key=lambda x: x[1], reverse=True))

            for item, chance in item_lists["items"].items():
                # Check if chance is essentially 'zero' and format
                if chance < 0.01:
                    chance = "<0.01"
                else:
                    chance = utility.convert_int(chance)
                
                # Check the cached items first, if it exists, we use that data instead of processing again
                if content_item_cache.get(item):
                    icon = content_item_cache[item]["icon"]
                    name_link = content_item_cache[item]["name_link"]

                else:
                    content_item_id = utility.fix_item_id(item)
                    if content_item_id == item and "." not in content_item_id:
                        pbar.write(f"No item ID found for '{content_item_id}'")
                        icon = "[[File:Question_On.png]]"
                        name_link = item
                        
                    else:
                        icon = utility.get_icon(content_item_id, True, True, True)
                        name = utility.get_name(content_item_id)
                        page = utility.get_page(content_item_id, name)
                        if language_code != "en":
                            name_link = f"[[{page}/{language_code}|{name}]]"
                        elif name != page:
                            name_link = f"[[{page}|{name}]]"
                        else:
                            name_link = f"[[{page}]]"
                    
                    # Add to cache to save time processing the same items
                    if item not in content_item_cache:
                        content_item_cache[item] = {"name_link": name_link, "icon": icon}


                table_entry = f"|-\n| {icon}\n| {name_link}\n| {chance}%"
                table.append(table_entry)
            
            table.append(TABLE_FOOTER)

            with open(output_file, 'w', encoding='utf-8') as file:
                file.write("\n".join(table))

            pbar.update(1)

        pbar.bar_format = f"Item files written to '{output_dir}'."


def main():
    
    items = get_items()
    write_to_file(items)
    save_cache(items, "container_contents.json")




if __name__ == "__main__":
    main()