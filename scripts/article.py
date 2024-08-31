import os
import re
import sys
import csv
from difflib import SequenceMatcher
from tqdm import tqdm
from core import translate

# Language dictionary
LANGUAGE_DATA = {
    "en": {
        "intro_template": "{article} '''{lowercase_name}''' is an [[item]] in [[Project Zomboid]].",
        "article": lambda lowercase_name: 'An' if lowercase_name[0] in 'aeiou' else 'A',
        "headers": {
            "Usage": "Usage",
            "Condition": "Condition",
            "Location": "Location",
            "Code": "Code",
            "See also": "See also",
            "Consumable properties": "Consumable properties",
        },
        "help_text": "Help PZwiki by adding information to this section.",
        "translate_reason": "Translated using game translation files.",
    },
    "pl": {
        "intro_template": "'''{lowercase_name}''' to [[przedmiot]] w [[Project Zomboid/pl]].",
        "headers": {
            "Usage": "Zastosowanie",
            "Condition": "Stan",
            "Location": "Lokalizacja",
            "Code": "Kod",
            "See also": "Zobacz także",
            "Consumable properties": "Właściwości konsumpcyjne",
        },
        "help_text": "Pomóż PZwiki, dodając informacje do tej sekcji.",
        "translate_reason": "Przetłumaczone za pomocą plików tłumaczeń gry.",
    },
    "fr": {
        "intro_template": "'''{lowercase_name}''' est {{{{ll|item}}}} dans {{{{ll|Project Zomboid}}}}.",
        "headers": {
            "Usage": "Utilisation",
            "Condition": "Condition",
            "Location": "Emplacement",
            "Code": "Code",
            "See also": "Voir aussi",
            "Consumable properties": "Propriétés consommables",
        },
        "help_text": "Aidez PZwiki en ajoutant des informations à cette section.",
        "translate_reason": "Traduit à l'aide des fichiers de traduction du jeu.",
    },
    "it": {
        "intro_template": "'''{lowercase_name}''' è {{{{ll|item}}}} in {{{{ll|Project Zomboid}}}}.",
        "headers": {
            "Usage": "Utilizzo",
            "Condition": "Condizione",
            "Location": "Posizione",
            "Code": "Codice",
            "See also": "Vedi anche",
            "Consumable properties": "Proprietà consumabili",
        },
        "help_text": "Aiuta PZwiki aggiungendo informazioni a questa sezione.",
        "translate_reason": "Tradotto utilizzando i file di traduzione del gioco.",
    },
    "es": {
        "intro_template": "'''{lowercase_name}''' es {{{{ll|item}}}} en {{{{ll|Project Zomboid}}}}.",
        "headers": {
            "Usage": "Uso",
            "Condition": "Condición",
            "Location": "Ubicación",
            "Code": "Código",
            "See also": "Ver también",
            "Consumable properties": "Propiedades consumibles",
        },
        "help_text": "Ayuda a PZwiki añadiendo información a esta sección.",
        "translate_reason": "Traducido usando los archivos de traducción del juego.",
    },
    "pt": {
        "intro_template": "'''{lowercase_name}''' é {{{{ll|item}}}} em {{{{ll|Project Zomboid}}}}.",
        "headers": {
            "Usage": "Uso",
            "Condition": "Condição",
            "Location": "Localização",
            "Code": "Código",
            "See also": "Veja também",
            "Consumable properties": "Propriedades consumíveis",
        },
        "help_text": "Ajude PZwiki adicionando informações a esta seção.",
        "translate_reason": "Traduzido usando os arquivos de tradução do jogo.",
    },
    "ptbr": {
        "intro_template": "'''{lowercase_name}''' é {{{{ll|item}}}} em {{{{ll|Project Zomboid}}}}.",
        "headers": {
            "Usage": "Uso",
            "Condition": "Condição",
            "Location": "Localização",
            "Code": "Código",
            "See also": "Veja também",
            "Consumable properties": "Propriedades consumíveis",
        },
        "help_text": "Ajude PZwiki adicionando informações a esta seção.",
        "translate_reason": "Traduzido usando os arquivos de tradução do jogo.",
    },
    "ru": {
        "intro_template": "'''{lowercase_name}''' — это {{{{ll|item}}}} в {{{{ll|Project Zomboid}}}}.",
        "headers": {
            "Usage": "Использование",
            "Condition": "Состояние",
            "Location": "Расположение",
            "Code": "Код",
            "See also": "См. также",
            "Consumable properties": "Потребляемые свойства",
        },
        "help_text": "Помогите PZwiki, добавив информацию в этот раздел.",
        "translate_reason": "Переведено с использованием файлов перевода игры.",
    },
    "tr": {
        "intro_template": "'''{lowercase_name}''' {{{{ll|Project Zomboid}}}}'da bir {{{{ll|item}}}}.",
        "headers": {
            "Usage": "Kullanım",
            "Condition": "Durum",
            "Location": "Konum",
            "Code": "Kod",
            "See also": "Ayrıca bakınız",
            "Consumable properties": "Tüketilebilir özellikler",
        },
        "help_text": "Bu bölüme bilgi ekleyerek PZwiki'ye yardım edin.",
        "translate_reason": "Oyun çeviri dosyaları kullanılarak çevrilmiştir.",
    },
    "jp": {
        "intro_template": "'''{lowercase_name}'''は{{{{ll|Project Zomboid}}}}の{{{{ll|item}}}}です。",
        "headers": {
            "Usage": "使用方法",
            "Condition": "状態",
            "Location": "場所",
            "Code": "コード",
            "See also": "参照",
            "Consumable properties": "消費可能な特性",
        },
        "help_text": "このセクションに情報を追加してPZwikiを支援してください。",
        "translate_reason": "ゲームの翻訳ファイルを使用して翻訳されました。",
    },
    "ko": {
        "intro_template": "'''{lowercase_name}'''은(는) {{{{ll|Project Zomboid}}}}의 {{{{ll|item}}}}입니다.",
        "headers": {
            "Usage": "사용",
            "Condition": "상태",
            "Location": "위치",
            "Code": "코드",
            "See also": "또한 참조하십시오",
            "Consumable properties": "소모 가능한 속성",
        },
        "help_text": "이 섹션에 정보를 추가하여 PZwiki를 도와주세요.",
        "translate_reason": "게임 번역 파일을 사용하여 번역되었습니다.",
    },
}


def load_item_id_dictionary(dictionary_dir):
    item_id_dict = {}
    try:
        with open(dictionary_dir, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                article_name = row[0].strip()

                for item_id in row[1:15]:
                    item_id = item_id.strip()
                    if item_id:  # Ensure item_id is not empty
                        item_id_dict[item_id] = article_name

    except Exception as e:
        print(f"Error reading {dictionary_dir}: {e}")

    return item_id_dict


def generate_intro(lowercase_name, language_code):
    language_data = LANGUAGE_DATA.get(language_code, LANGUAGE_DATA["en"])
    intro_template = language_data["intro_template"]
    article = language_data.get("article", lambda _: "")(lowercase_name).lower()

    intro = intro_template.format(article=article, lowercase_name=lowercase_name)
    intro = intro[0].upper() + intro[1:]

    return intro


def process_file(file_path, output_dir, consumables_dir, infobox_data_list, item_id_dict, generate_all, fixing_dir,
                 code_dir, distribution_dir, language_code):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    infobox_match = re.search(r'(\{\{Infobox item.*?\}\})', content, re.DOTALL)
    if not infobox_match:
        print(f"Infobox not found in {file_path}")
        return
    infobox = infobox_match.group(1)

    item_id_match = re.search(r'\|item_id\s*=\s*(.+)', infobox)
    if not item_id_match:
        print(f"Item ID not found in {file_path}")
        return

    item_id = item_id_match.group(1).strip()

    # Check if we should skip this item_id
    if not generate_all and item_id in item_id_dict:
        return

    version_match = re.search(r'\|infobox_version\s*=\s*([\d\.]+)', infobox)
    if not version_match:
        print(f"Infobox version not found in {file_path}")
        return
    infobox_version = version_match.group(1)

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

    # Build the article
    header = generate_header(category, skill_type, infobox_version, language_code, lowercase_name)
    body_content = assemble_body(lowercase_name, os.path.basename(file_path), name, item_id, category, skill_type,
                                 infobox, consumables_dir, infobox_data_list, item_id_dict, fixing_dir, code_dir,
                                 distribution_dir, language_code)

    intro = generate_intro(lowercase_name, language_code)

    new_content = f"""
{header}
{infobox}
{intro}

{body_content}
"""

    # Sanitize the item_id to create a valid filename
    safe_item_id = re.sub(r'[^\w\-_\. ]', '_', item_id) + '.txt'
    new_file_path = os.path.join(output_dir, safe_item_id)

    # Write the content to the output file
    try:
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(new_content.strip())
    except Exception as e:
        print(f"Error writing to {new_file_path}: {e}")


def generate_header(category, skill_type, infobox_version, language_code, lowercase_name):
    language_data = LANGUAGE_DATA.get(language_code, LANGUAGE_DATA["en"])
    translate_reason = language_data["translate_reason"]

    # Determine header based on category and skill type
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

    # Remove link markup from skill type for comparison
    skill_type = re.sub(r'\[\[(?:[^\|\]]*\|)?([^\|\]]+)\]\]', r'\1', skill_type).strip()

    # Determine the correct header based on the category and skill type
    if category in category_dict:
        if category_dict[category] == "use_skill_type":
            header = skill_type_dict.get(skill_type, "{{Header|Project Zomboid|Items|Weapons}}")
        else:
            header = category_dict[category]
    else:
        header = "{{Header|Project Zomboid|Items}}"

    name = lowercase_name.capitalize()

    if language_code == "en":
        full_header = f"""{header}
{{{{Page version|{infobox_version}}}}}
{{{{Autogenerated|B42}}}}"""
    else:
        full_header = f"""{{{{Title|{name}}}}}
{header}
{{{{Autogenerated}}}}
{{{{AutoT|{translate_reason}}}}}"""

    return full_header


def generate_consumable_properties(item_id, consumables_dir):
    if not os.path.exists(consumables_dir):
        return ""

    # Generate the filename to check
    filename = re.sub(r'[^\w\-_\. ]', '_', item_id) + '.txt'
    file_path = os.path.join(consumables_dir, filename)

    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return ""


def generate_condition(name, category, skill_type, infobox, fixing_dir):
    if category not in ['Weapon', 'Tool / Weapon']:
        return ""

    condition_max_match = re.search(r'\|condition_max\s*=\s*(\d+)', infobox)
    condition_lower_chance_match = re.search(r'\|condition_lower_chance\s*=\s*(\d+)', infobox)

    if not condition_max_match or not condition_lower_chance_match:
        return ""

    condition_max = condition_max_match.group(1)
    condition_lower_chance = condition_lower_chance_match.group(1)

    condition_text = f"""The {name} has a maximum condition of {condition_max}. Its rate of degradation is influenced by the {skill_type} and [[maintenance]] [[skill]]s. The chance of losing [[durability]] can be simplified to the following formula: <code>1 in (35 + maintenanceMod &times; 2)</code>. Where "maintenanceMod" is calculated using the {skill_type} and maintenance skills.<br>

{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"""

    if os.path.exists(fixing_dir):
        fixing_files = os.listdir(fixing_dir)

        item_id = re.search(r'\|item_id\s*=\s*(.+)', infobox).group(1).strip()
        item_id_search = f"|item_id={item_id}"

        if fixing_files:
            for file_name in fixing_files:
                file_path = os.path.join(fixing_dir, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                        if item_id_search in file_content:
                            fixing_content = file_content.strip()
                            condition_text += f"\n\n===Repairing===\n{fixing_content}"
                            break
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return condition_text


def generate_location(original_filename, infobox_name, item_id, distribution_dir):
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


def generate_code(item_id, code_dir):
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


def load_infoboxes(infobox_dir):
    # Store extracted infoboxes in memory for efficiency
    infobox_data_list = []
    infobox_files = [f for f in os.listdir(infobox_dir) if f.endswith('.txt')]

    for file_name in infobox_files:
        file_path = os.path.join(infobox_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        infobox_data = {
            'name': re.search(r'\|name\s*=\s*(.+)', content).group(1).strip() if re.search(r'\|name\s*=\s*(.+)',
                                                                                           content) else "",
            'category': re.search(r'\|category\s*=\s*(.+)', content).group(1).strip() if re.search(
                r'\|category\s*=\s*(.+)', content) else "",
            'skill_type': re.search(r'\|skill_type\s*=\s*(.+)', content).group(1).strip() if re.search(
                r'\|skill_type\s*=\s*(.+)', content) else "",
            'tags': [tag.strip() for tag in re.findall(r'\|tag\d?\s*=\s*(.+)', content)],
            'item_id': re.search(r'\|item_id\s*=\s*(.+)', content).group(1).strip() if re.search(
                r'\|item_id\s*=\s*(.+)', content) else ""
        }

        infobox_data_list.append(infobox_data)

    return infobox_data_list


def calculate_relevance(current_item, other_item):
    category_match = current_item.get('category') == other_item.get('category')
    tag_similarity = len(set(current_item.get('tags', [])).intersection(set(other_item.get('tags', []))))
    name_similarity = SequenceMatcher(None, current_item.get('name', ''), other_item.get('name', '')).ratio()
    skill_type_match = current_item.get('skill_type') == other_item.get('skill_type')

    # Weight scores
    relevance_score = (
            name_similarity * 8 +
            category_match * 8 +
            tag_similarity * 5 +
            skill_type_match * 3
    )
    return relevance_score


def find_most_relevant_items(current_item, all_items_infoboxes, item_id_dict):
    relevance_scores = []
    current_item_name = current_item.get('name', '').lower()

    for item in all_items_infoboxes:
        other_item_name = item.get('name', '').lower()
        if other_item_name == current_item_name:
            continue
        current_item_id = current_item.get('item_id', '')
        other_item_id = item.get('item_id', '')

        # Check if item_id is in the dictionary and skip
        if current_item_id in item_id_dict and other_item_id in item_id_dict:
            if item_id_dict[current_item_id] == item_id_dict[other_item_id]:
                continue

        relevance = calculate_relevance(current_item, item)
        relevance_scores.append((relevance, item['name']))

    top_relevant_items = sorted(relevance_scores, reverse=True, key=lambda x: x[0])[:3]

    # Ensure no items with the same name as the current item are included
    filtered_relevant_items = [item_name for score, item_name in top_relevant_items if
                               item_name.lower() != current_item_name]
    filtered_relevant_items.sort()

    return filtered_relevant_items


def generate_see_also(current_item, infobox_data_list, item_id_dict):
    # Find the most relevant items
    relevant_items = find_most_relevant_items(current_item, infobox_data_list, item_id_dict)

    # Use the English name for each relevant item
    english_names = []
    for item_name in relevant_items:
        item_infobox = next((infobox for infobox in infobox_data_list if infobox['name'].lower() == item_name.lower()), None)
        if item_infobox:
            english_name = item_id_dict.get(item_infobox['item_id'], item_name)
            english_names.append(english_name)

    see_also_list = '\n'.join([f"*{{{{ll|{name}}}}}" for name in english_names])

    category_list = ["Weapon", "Tool", "Clothing", "Food"]

    if current_item.get('category') in category_list:
        navbox_param = current_item.get('category', '').lower()
        navbox = f"{{{{Navbox items|{navbox_param}}}}}"
    else:
        navbox = "{{Navbox items}}"

    return f"{see_also_list}\n\n{navbox}"


def assemble_body(name, original_filename, infobox_name, item_id, category, skill_type, infobox, consumables_dir,
                  infobox_data_list, item_id_dict, fixing_dir, code_dir, distribution_dir, language_code):
    language_data = LANGUAGE_DATA.get(language_code, LANGUAGE_DATA["en"])
    headers = language_data["headers"]
    help_text = language_data["help_text"]

    body_content = f"\n=={headers['Usage']}==\n{help_text}\n"

    # Example of using the consumable properties, condition, etc.
    consumable_properties = generate_consumable_properties(item_id, consumables_dir)
    if consumable_properties:
        body_content += f"\n==={headers['Consumable properties']}===\n{consumable_properties}\n"

    # Add other sections
    sections = {
        headers['Condition']: generate_condition(name, category, skill_type, infobox, fixing_dir),
        headers['Location']: generate_location(original_filename, infobox_name, item_id, distribution_dir),
        headers['Code']: generate_code(item_id, code_dir),
        headers['See also']: generate_see_also({
            'name': name,
            'category': category,
            'skill_type': skill_type,
            'tags': re.findall(r'\|tag\d?\s*=\s*(.+)', infobox),
            'item_id': item_id
        }, infobox_data_list, item_id_dict)
    }

    for section, content in sections.items():
        if content.strip():
            body_content += f"\n=={section}==\n{content}\n"

    return body_content.strip()


def main():
    # Set language code in case it hasn't been set already.
    translate.change_language()
    language_code = translate.get_language_code()

    infobox_dir = f'output/{language_code}/infoboxes'
    output_dir = f'output/{language_code}/articles'
    consumables_dir = f'output/{language_code}/consumables'
    fixing_dir = f'output/{language_code}/fixing'
    dictionary_dir = 'resources/item_id_dictionary.csv'
    distribution_dir = 'output/distributions/complete'
    code_dir = 'output/codesnips'

    warnings = []

    if not os.path.exists(infobox_dir):
        print("Infoboxes directory not found")
        sys.exit(1)

    text_files = [f for f in os.listdir(infobox_dir) if f.endswith('.txt')]

    if not text_files:
        print("Infoboxes not found")
        sys.exit(1)

    print(f"{len(text_files)} files found")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(consumables_dir) or not os.listdir(consumables_dir):
        warnings.append("WARNING: Consumables not found, please run consumables.py first")
    if not os.path.exists(fixing_dir) or not os.listdir(fixing_dir):
        warnings.append("WARNING: Fixing not found, please run fixing.py first")

    while True:
        user_choice = input(
            "Do you want to generate:\n1: All items\n2: New items (Don't exist on the wiki currently)\nQ: Quit\n> ").strip().lower()
        if user_choice == 'q':
            return
        if user_choice in ['1', '2']:
            break
        print("Invalid input. Please enter 1 or 2.")
    generate_all = user_choice == '1'

    infobox_data_list = load_infoboxes(infobox_dir)
    item_id_dict = load_item_id_dictionary(dictionary_dir)

    for text_file in tqdm(text_files, desc="Generating articles", unit="file"):
        file_path = os.path.join(infobox_dir, text_file)
        process_file(file_path, output_dir, consumables_dir, infobox_data_list, item_id_dict, generate_all, fixing_dir,
                     code_dir, distribution_dir, language_code)

    if warnings:
        print("\n".join(warnings))


if __name__ == "__main__":
    main()
