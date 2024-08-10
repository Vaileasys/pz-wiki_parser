import os
import re
import sys


def build_header(category, skill_type):
    # Define the category dictionary
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
        "Appearance": "{{Header|Project Zomboid|Items|Miscellaneous items|Appearance}}"
    }

    # Define the skill type dictionary
    skill_type_dict = {
        "Long Blade": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Long blade weapons}}",
        "Short Blade": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Short blade weapons}}",
        "Long Blunt": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Long blunt weapons}}",
        "Short Blunt": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Short blunt weapons}}",
        "Spear": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Spears}}",
        "Axe": "{{Header|Project Zomboid|Items|Weapons|Melee weapons|Axes}}",
        "Aiming": "{{Header|Project Zomboid|Items|Weapons|Firearms}}",
        "Firearm": "{{Header|Project Zomboid|Items|Weapons|Firearms}}"
    }

    # Strip square brackets and anything inside them from skill type
    skill_type = re.sub(r'\[\[(?:[^\|\]]*\|)?([^\|\]]+)\]\]', r'\1', skill_type).strip()

    # Check if category matches
    if category in category_dict:
        if category_dict[category] == "use_skill_type":
            # Check if skill type matches
            if skill_type in skill_type_dict:
                return skill_type_dict[skill_type]
            else:
                return "{{Header|Project Zomboid|Items|Weapons}}"
        else:
            return category_dict[category]
    else:
        return "{{Header|Project Zomboid|Items}}"  # Default header


def process_file(file_path, output_dir):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    # Find the infobox
    infobox_match = re.search(r'(\{\{Infobox item.*?\}\})', content, re.DOTALL)
    if not infobox_match:
        print(f"Infobox not found in {file_path}")
        return

    infobox = infobox_match.group(1)

    # Extract infobox version
    version_match = re.search(r'\|infobox_version\s*=\s*([\d\.]+)', infobox)
    if not version_match:
        print(f"Infobox version not found in {file_path}")
        return

    infobox_version = version_match.group(1)

    # Extract item_id
    item_id_match = re.search(r'\|item_id\s*=\s*(.+)', infobox)
    if not item_id_match:
        print(f"Item ID not found in {file_path}")
        return

    item_id = item_id_match.group(1).strip()

    # Extract name
    name_match = re.search(r'\|name\s*=\s*(.+)', infobox)
    if not name_match:
        print(f"Name not found in {file_path}")
        return

    name = name_match.group(1).strip()
    lowercase_name = name.lower()

    # Extract category
    category_match = re.search(r'\|category\s*=\s*(.+)', infobox)
    category = category_match.group(1).strip() if category_match else ""

    # Extract skill type
    skill_type_match = re.search(r'\|skill_type\s*=\s*(.+)', infobox)
    skill_type = skill_type_match.group(1).strip() if skill_type_match else ""

    # Determine if 'A' should be 'An'
    article = 'An' if lowercase_name[0] in 'aeiou' else 'A'

    # Build the header
    header = build_header(category, skill_type)

    # Create the output content
    body_content = assemble_body(lowercase_name, os.path.basename(file_path), name, item_id, category, skill_type, infobox)

    new_content = f"""
{header}
{{{{Page version|{infobox_version}}}}}
{{{{Autogenerated|B42}}}}
{infobox}
{article} '''{lowercase_name}''' is an [[item]] in [[Project Zomboid]].

{body_content}
"""

    # Sanitize the item_id to create a valid filename
    safe_item_id = re.sub(r'[^\w\-_\. ]', '_', item_id) + '.txt'

    # Determine the new file path
    new_file_path = os.path.join(output_dir, safe_item_id)

    # Write the new content to the output file
    try:
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(new_content.strip())
        print(f"Processed and created {new_file_path}")
    except Exception as e:
        print(f"Error writing to {new_file_path}: {e}")


def assemble_body(name, original_filename, infobox_name, item_id, category, skill_type, infobox):
    sections = {
        'Condition': generate_condition(name, category, skill_type, infobox),
        'Location': generate_location(original_filename, infobox_name, item_id),
        'Code': generate_code(item_id),
        'See also': generate_see_also(name, category)
    }

    body_content = "\n==Usage==\n"  # Start with an empty Usage section

    for section, content in sections.items():
        if content.strip():
            body_content += f"\n=={section}==\n{content}\n"

    return body_content.strip()


def generate_condition(name, category, skill_type, infobox):
    if category not in ['Weapon', 'ToolWeapon']:
        return ""

    condition_max_match = re.search(r'\|condition_max\s*=\s*(\d+)', infobox)
    condition_lower_chance_match = re.search(r'\|condition_lower_chance\s*=\s*(\d+)', infobox)

    if not condition_max_match or not condition_lower_chance_match:
        return ""

    condition_max = condition_max_match.group(1)
    condition_lower_chance = condition_lower_chance_match.group(1)

    return f"""The {name} has a maximum condition of {condition_max}. Its rate of degradation is influenced by the {skill_type} and [[maintenance]] [[skill]]s. The chance of losing [[durability]] can be simplified to the following formula: <code>1 in (35 + maintenanceMod &times; 2)</code>. Where "maintenanceMod" is calculated using the {skill_type} and maintenance skills.<br>

{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"""


def generate_location(original_filename, infobox_name, item_id):
    distribution_dir = 'resources/distribution'

    if not os.path.exists(distribution_dir):
        return ""

    # Generate possible filenames to check
    possible_filenames = [
        original_filename,
        infobox_name,
        re.sub(r'.*\.', '', item_id)
    ]

    for filename in possible_filenames:
        file_path = os.path.join(distribution_dir, filename + '.txt')
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read().strip()
            except Exception as e:

                print(f"Error reading {file_path}: {e}")
    return ""


def generate_code(item_id):
    code_dir = 'resources/code'

    if not os.path.exists(code_dir):
        return ""

    # Generate the filename to check
    filename = re.sub(r'.*\.', '', item_id) + '.txt'
    file_path = os.path.join(code_dir, filename)

    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read().strip()
                return f"""{{{{CodeBox|
{contents}
}}}}"""
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return ""


def generate_see_also(name, category):
    see_also_list = "*{{ll|Placeholder}}\n*{{ll|Placeholder}}\n*{{ll|Placeholder}}"
    category_list = ["Weapon", "Tool", "Clothing", "Food"]

    if category in category_list:
        navbox_param = category.lower()
        navbox = f"{{{{Navbox items|{navbox_param}}}}}"
    else:
        navbox = "{{Navbox items}}"

    return f"{see_also_list}\n\n{navbox}"


def main():
    input_dir = 'output/infoboxes'
    output_dir = 'output/articles'

    if not os.path.exists(input_dir):
        print("Infoboxes directory not found")
        sys.exit(1)

    text_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    if not text_files:
        print("Infoboxes not found")
        sys.exit(1)

    print(f"{len(text_files)} files found")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for text_file in text_files:
        file_path = os.path.join(input_dir, text_file)
        process_file(file_path, output_dir)


if __name__ == "__main__":
    main()
