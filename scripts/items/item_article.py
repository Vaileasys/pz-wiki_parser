import os
import re
import sys
import csv
from difflib import SequenceMatcher
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import (PBAR_FORMAT, DATA_DIR)
from scripts.core.cache import save_cache, load_cache
from scripts.utils.echo import echo, echo_info, echo_warning, echo_error

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
            "Repairing": "Repairing",
        },
        "help_text": "Help PZwiki by adding information to this section.",
        "translate_reason": "Translated using game translation files.",
        "condition_categories": ["Weapon", "Tool / Weapon"],
        "condition_text": (
            "The {name} has a maximum condition of {condition_max}. Its rate of degradation is influenced by the {skill_type_lower} and [[maintenance]] [[skill]]s. The chance of losing [[durability]] can be simplified to the following formula: "
            "<code>1 in (35 + maintenanceMod &times; 2)</code>. Where \"maintenanceMod\" is calculated using the {skill_type_lower} and maintenance skills.<br>"
            "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
        ),
    },
    "pl": {
        "intro_template": "'''{lowercase_name}''' to [[Item/pl|przedmiot]] w [[Project Zomboid/pl|Project Zomboid]].",
        "headers": {
            "Usage": "Zastosowanie",
            "Condition": "Stan",
            "Location": "Lokalizacja",
            "Code": "Kod",
            "See also": "Zobacz też",
            "Consumable properties": "Właściwości konsumpcyjne",
            "Repairing": "Naprawa",
        },
        "help_text": "Pomóż PZwiki, dodając informacje do tej sekcji.",
        "translate_reason": "Przetłumaczone za pomocą plików tłumaczeń gry.",
        "condition_categories": ["Broń", "Narzędzia/broń"],
        "condition_text": (
            "{name} ma maksymalny stan {condition_max}. Na szybkość degradacji mają  wpływ [[Skill/pl|umiejętności]] {skill_type_lower} i umiejętność [[Maintenance/pl|konserwacja]]. Szansa na zmniejszenie  [[Condition/pl|stanu]] może być uproszczona do następującej formuły: "
            "<code>1 na (35 + maintenanceMod &times; 2)</code>. Gdzie \"maintenanceMod\" jest obliczony używając {skill_type_lower} i umiejętności konserwacji.<br>"
            "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
        ),
    },
    "tr": {
        "intro_template": "'''{lowercase_name}''' [[Project Zomboid/tr|Project Zomboid]]'de bir [[Item/tr|eşyadır]].",
        "headers": {
            "Usage": "Kullanım",
            "Condition": "Sağlamlık",
            "Location": "Dağılım",
            "Code": "Kod",
            "See also": "Ayrıca bakınız",
            "Consumable properties": "Tüketilebilir nitelikler",
            "Repairing": "Onarma",
        },
        "help_text": "Bu bölüme bilgi ekleyerek PZviki'ye destek olun.",
        "translate_reason": "Oyunun çeviri dosyalaranı kullanarak çevrildi.",
        "condition_categories": ["Silah", "Alet / Silah"],
        "condition_text": (
            "{name}, {condition_max} azami sağlamlığa sahiptir. Bozulma oranı {skill_type_lower} ve [[maintenance/tr|onarım]] [[skill/tr|becerilerine]] bağlıdır. [[durability/tr|Sağlamlığın]] düşme ihtimali şu formülü kullanarak basitleştirilebilir: "
            "<code>1/(35 + maintenanceMod &times; 2)</code>. Buradaki \"maintenanceMod\", {skill_type_lower} ve onarım becerilerini kullanarak hesaplanır.<br>"
            "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
        ),
    },
    "ru": {
        "intro_template": "'''{lowercase_name}''' это [[Item/ru|предмет]] в [[Project Zomboid/ru|Project Zomboid]].",
        "headers": {
            "Usage": "Использование",
            "Condition": "Состояние",
            "Location": "Локация",
            "Code": "Код",
            "See also": "Смотрите также",
            "Consumable properties": "Свойства",
            "Repairing": "Починка",
        },
        "help_text": "Помогите PZwiki добавив информацию в этот раздел.",
        "translate_reason": "Использован перевод из файлов игры.",
        "condition_categories": ["Оружие", "Инструмент / Оружие"],
        "condition_text": (
            "{name} имеет максимальное состояние {condition_max}. Скорость поломки оружия зависит от уровня [[Skill/ru|навыков]] {skill_type_lower} и [[починки]]. Шанс потери одного очка [[состояния]] можно упростить до следующей формулы: <code>1 in (35 + maintenanceMod &times; 2)</code>. "
            "В которой \"maintenanceMod\" вычислен используя навыки владения {skill_type_lower} и прочности.<br>"
            "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
        ),
    },
    "it": {
        "intro_template": "Il/la '''{lowercase_name}''' è un [[Item/it|Oggetto]] in [[Project Zomboid/it|Project Zomboid]].",
        "headers": {
            "Usage": "Utilizzo",
            "Condition": "Condizione",
            "Location": "Posizione",
            "Code": "Codice",
            "See also": "Vedi anche",
            "Consumable properties": "Proprietà del consumabile",
            "Repairing": "Riparazione",
        },
        "help_text": "Aiuta PZwiki aggiungendo informazioni a questa sezione.",
        "translate_reason": "Tradotto usando file di traduzione del gioco.",
        "condition_categories": ["Arma", "Attrezzo / Arma"],
        "condition_text": (
            "Il/la {name} ha una durabilità che arriva ad un massimo di :{condition_max}. Il ritmo a cui si degrada, dipende dall'abilità : {skill_type_lower} e [[maintenance/it|manutenzione]] [[skill/it|abilità]]. La probabilità di perdere [[durability/it|durabilità]] può essere semplificata nella seguente formula: <code>1 in (35 + maintenanceMod &times; 2)</code>. "
            "Dove \"maintenanceMod\" è calcolata usando il livello di abilità in {skill_type_lower} e il livello di abilità in manutenzione.<br>"
        "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
        ),
    },
    "es": {
        "intro_template": "'''{lowercase_name}''' es un [[item/es|artículo]] en [[Project Zomboid/es|Project Zomboid]].",
        "headers": {
            "Usage": "Uso",
            "Condition": "Estado",
            "Location": "Localización",
            "Code": "Código",
            "See also": "Ver también",
            "Consumable properties": "Propiedades de los consumibles",
            "Repairing": "Reparación",
        },
        "help_text": "Ayuda a PZwiki añadiendo información en esta sección",
        "translate_reason": "Traducido con archivos de traducción del juego.",
        "condition_categories": ["Arma", "Herramienta / Arma"],
        "condition_text": (
            "El {name} tiene una condición máxima de {condition_max}. Su tasa de degradación está influenciada por la {skill_type_lower} y [[maintenance/es|mantenimiento]] [[skill/es|habilidad]]. La probabilidad de perderlo [[durability/es|durabilidad]] se puede resumir con la siguiente fórmula: "
            "<code>1 en (35 + maintenanceMod &times; 2)</code>. Donde \"maintenanceMod\" se calcula utilizando el {skill_type_lower} y las habilidades de mantenimiento.<br>"
            "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
        ),
    },
    "pt-br": {
        "intro_template": "'''{lowercase_name}''' é um [[item/pt-br|item]] em [[Project Zomboid/pt-br|Project Zomboid]].",
        "headers": {
            "Usage": "Utilidade",
            "Condition": "Condição",
            "Location": "Local",
            "Code": "Código",
            "See also": "Veja também",
            "Consumable properties": "Propriedades consumíveis",
            "Repairing": "Consertando",
        },
        "help_text": "Ajude a PZwiki adicionando mais informações a essa seção.",
        "translate_reason": "Traduzido utilizando os arquivos de tradução do jogo.",
        "condition_categories": ["Arma", "Ferramenta / Arma"],
        "condition_text": (
            "O/A {name} tem uma condição máxima de {condition_max}. Sua taxa de degradação é influenciada pelas [[skill/pt-br|habilidades]] de {skill_type_lower} and [[maintenance/pt-br|manutenção]]. A chance de perder [[durability/pt-br|durabilidade]] pode ser siplificada utilizando a seguinte fórmula: "
            "<code>1 em (35 + maintenanceMod &times; 2)</code>. Onde \"maintenanceMod\" é calculado utilizando o nível das duas habilidades.<br>"
            "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
        ),
    },
    "uk": {
        "intro_template": "'''{lowercase_name}''' це [[Item/uk|предмет]] в [[Project Zomboid/uk|Project Zomboid]].",
        "headers": {
            "Usage": "Застосування",
            "Condition": "Стан",
            "Location": "Локація",
            "Code": "Код",
            "See also": "Дивіться також",
            "Consumable properties": "Витратні властивості",
            "Repairing": "Ремонт",
        },
        "help_text": "Допоможіть PZ-Wiki, додавши інформацію до цього розділу.",
        "translate_reason": "Перекладено за допомогою файлів перекладу гри.",
        "condition_categories": ["Інструмент", "Інструмент / Зброя"],
        "condition_text": (
            "{name} має максимальний стан {condition_max}. Його швидкість зносу залежить від {skill_type} і [[skill/uk|навички]] [[maintenance/uk|технічного обслуговування]]. Ймовірність втрати [[durability/uk|міцності]] можна спростити до наступної формули: "
            "<code>1 із (35 + maintenanceMod &times; 2)</code>. Де \"maintenanceMod\" розраховується за допомогою {skill_type} та навички технічного обслуговування.<br>"
            "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
        ),
    },
    "th": {
        "intro_template": "'''{lowercase_name}''' คือ[[item/th|ไอเท็ม]]ใน [[Project Zomboid/th|Project Zomboid]]",
        "headers": {
            "Usage": "การใช้งาน",
            "Condition": "สภาพความทนทาน",
            "Location": "ตำแหน่ง",
            "Code": "โค้ด",
            "See also": "ดูเพิ่มเติม",
            "Consumable properties": "คุณสมบัติของที่ใช้แล้วหมดไป",
            "Repairing": "การซ่อมแซม",
        },
        "help_text": "ช่วย PZwiki  โดยการเพิ่มข้อมูลในส่วนนี้",
        "translate_reason": "แปลโดยใช้ไฟล์แปลของเกม",
        "condition_categories": ["อาวุธ", "อุปกรณ์ / อาวุธ"],
        "condition_text": (
            "{name}มีสภาพสูงสุด {condition_max} อัตราการเสื่อมสภาพของได้รับผลจาก[[skill/th|ทักษะ]]{skill_type_lower}และ[[maintenance/th|การดูแลรักษาอาวุธ]]สามารถสรุปโอกาสในการเสื่อม[[durability/th|สภาพความทนทาน]]ได้ด้วยสูตรดังต่อไปนี้:"
            "<code>1 ใน (35 + maintenanceMod &times; 2)</code> โดยที่ \"maintenanceMod\" จะถูกคำนวณโดยรวมเลเวลทักษะ{skill_type_lower}บวกกับทักษะการดูแลรักษาอาวุธ<br>"
            "\n\n{{{{Durability weapon|{condition_lower_chance}|{condition_max}|skill={skill_type}}}}}"
            ),
    },
}


def load_item_id_dictionary(dictionary_dir):
    """
    Loads the item_id dictionary from a given CSV file.

    The dictionary is expected to have the following format:
        article_name, item_id1, item_id2, ...

    The function will return a dictionary with the item_id as the key and the
    article_name as the value.

    Args:
        dictionary_dir (str): The path to the CSV file containing the item_id
            dictionary.

    Returns:
        dict: A dictionary with the item_id as the key and the article_name as
            the value.
    """
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
        echo_error(f"Error reading {dictionary_dir}: {e}")

    return item_id_dict


def generate_intro(lowercase_name, language_code):
    language_data = LANGUAGE_DATA.get(language_code, LANGUAGE_DATA["en"])
    intro_template = language_data["intro_template"]
    article = language_data.get("article", lambda _: "")(lowercase_name).lower()

    intro = intro_template.format(article=article, lowercase_name=lowercase_name)

    first_alpha_index = next((i for i, c in enumerate(intro) if c.isalpha()), None)
    if first_alpha_index is not None:
        intro = intro[:first_alpha_index] + intro[first_alpha_index].upper() + intro[first_alpha_index + 1:]

    return intro



def process_file(file_path, output_dir, consumables_dir, infobox_data_list, item_id_dict, generate_all, fixing_dir,
                 code_dir, distribution_dir, history_dir, crafting_dir, language_code, pbar):
    """
        Processes a single file and generates the corresponding article content.

        This function reads the file, extracts the item_id, name, and category from the
        infobox, and builds the article content using the generate_header,
        assemble_body, and generate_intro functions. The content is then written to a
        new file in the output directory.

        Args:
            file_path (str): The path to the file to process.
            output_dir (str): The path to the directory where the output file should
                be written.
            consumables_dir (str): The path to the directory containing the
                consumable data.
            infobox_data_list (list): A list of infobox data dictionaries.
            item_id_dict (dict): A dictionary mapping item_id to article_name.
            generate_all (bool): Whether to generate all articles or only those that
                don't already have an article.
            fixing_dir (str): The path to the directory containing the fixing data.
            code_dir (str): The path to the directory containing the code data.
            distribution_dir (str): The path to the directory containing the
                distribution data.
            language_code (str): The language code to use for the generated content.
            pbar (tqdm object): The tqdm progress bar object.

        Returns:
            None
        """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        echo_error(f"Error reading {file_path}: {e}")
        return

    infobox_match = re.search(r'(\{\{Infobox item.*?\}\})', content, re.DOTALL)
    if not infobox_match:
        echo_warning(f"Infobox not found in {file_path}")
        return
    infobox = infobox_match.group(1)

    item_id_match = re.search(r'\|item_id\s*=\s*(.+)', infobox)
    if not item_id_match:
        echo_warning(f"Item ID not found in {file_path}")
        return

    item_id = item_id_match.group(1).strip()

    if not generate_all and item_id in item_id_dict:
        return

    version_match = re.search(r'\|infobox_version\s*=\s*([\d\.]+)', infobox)
    if not version_match:
        echo_warning(f"Infobox version not found in {file_path}")
        return
    infobox_version = version_match.group(1)

    name_match = re.search(r'\|name\s*=\s*(.+)', infobox)
    if not name_match:
        echo_warning(f"Name not found in {file_path}")
        return

    name = name_match.group(1).strip()
    lowercase_name = name.lower()

    category_match = re.search(r'\|category\s*=\s*(.+)', infobox)
    category = category_match.group(1).strip() if category_match else ""

    skill_type_match = re.search(r'\|skill_type\s*=\s*(.+)', infobox)
    skill_type = skill_type_match.group(1).strip() if skill_type_match else ""

    header = generate_header(category, skill_type, infobox_version, language_code, name)
    body_content = assemble_body(lowercase_name, os.path.basename(file_path), name, item_id, category, skill_type,
                                 infobox, consumables_dir, infobox_data_list, item_id_dict, fixing_dir, code_dir,
                                 distribution_dir, history_dir, crafting_dir, language_code, pbar)

    intro = generate_intro(lowercase_name, language_code)

    new_content = f"""
{header}
{infobox}
{intro}

{body_content}
"""

    safe_item_id = re.sub(r'[^\w\-_\. ]', '_', item_id) + '.txt'
    new_file_path = os.path.join(output_dir, safe_item_id)

    try:
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(new_content.strip())
    except Exception as e:
        echo_error(f"Error writing to {new_file_path}: {e}")


def generate_header(category, skill_type, infobox_version, language_code, name):
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

    # Use the original name directly for the Title template
    if language_code == "en":
        full_header = f"""{header}
{{{{Page version|{infobox_version}}}}}
{{{{Autogenerated|B42}}}}"""
    else:
        full_header = f"""{{{{Title|{name}}}}}
{header}
{{{{Autogenerated|B41}}}}
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
            echo_error(f"Error reading {file_path}: {e}")

    return ""


def generate_condition(name, category, skill_type, infobox, fixing_dir, language_code):
    """
    Generates a condition section for an item page based on the item's infobox and fixing files.

    Args:
        name (str): The name of the item.
        category (str): The category of the item.  # (no longer used for condition logic)
        skill_type (str): The skill type of the item.
        infobox (str): The contents of the item's infobox.
        fixing_dir (str): The directory containing the fixing files.
        language_code (str): The language code to use for the condition text.

    Returns:
        str: The condition section for the item page, or empty string if
             either condition_max or condition_lower_chance is missing.
    """
    language_data = LANGUAGE_DATA.get(language_code, LANGUAGE_DATA["en"])

    # Look for both fields in the infobox
    condition_max_match = re.search(r'\|condition_max\s*=\s*(\d+)', infobox)
    condition_lower_chance_match = re.search(r'\|condition_lower_chance\s*=\s*(\d+)', infobox)

    # If either is missing, skip the section entirely
    if not condition_max_match or not condition_lower_chance_match:
        return ""

    condition_max = condition_max_match.group(1)
    condition_lower_chance = condition_lower_chance_match.group(1)

    # Format the skill_type_lower for insertion
    if '|' in skill_type:
        part0, part1 = skill_type.split('|', 1)
        skill_type_lower = f"{part0}|{part1.lower()}"
    else:
        skill_type_lower = skill_type.lower()

    # Build the condition text from the template
    condition_text = language_data["condition_text"].format(
        name=name,
        condition_max=condition_max,
        skill_type=skill_type,
        skill_type_lower=skill_type_lower,
        condition_lower_chance=condition_lower_chance
    )

    # Capitalize first letter
    condition_text = condition_text[0].upper() + condition_text[1:]

    # Append a Repairing subsection if there's a matching fixing file
    repairing_header = language_data["headers"]["Repairing"]
    if os.path.isdir(fixing_dir):
        item_id_match = re.search(r'\|item_id\s*=\s*(.+)', infobox)
        if item_id_match:
            item_id = item_id_match.group(1).strip()
            token = f"|item_id={item_id}"
            for fname in os.listdir(fixing_dir):
                path = os.path.join(fixing_dir, fname)
                try:
                    with open(path, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                        if token in content:
                            fixing_content = content.strip()
                            condition_text += f"\n\n==={repairing_header}===\n{fixing_content}"
                            break
                except Exception as e:
                    echo_error(f"Error reading {path}: {e}")

    return condition_text


def generate_crafting(item_id, crafting_dir, language_code):
    if language_code != "en":
        return ""

    if not os.path.exists(crafting_dir):
        return ""

    filename = f"{item_id}.txt"
    file_path = os.path.join(crafting_dir, filename)

    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            echo_error(f"Error reading {file_path}: {e}")

    return ""


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
                echo_error(f"Error reading {file_path}: {e}")
    return ""


def generate_history(item_id, history_dir, language_code):
    if language_code != "en":
        return ""

    history_file_name = f"{item_id}.txt"
    history_file_path = os.path.join(history_dir, history_file_name)

    if os.path.isfile(history_file_path):
        try:
            with open(history_file_path, 'r', encoding='utf-8') as file:
                contents = file.read().strip()
                content = f"{contents}"
        except Exception as e:
            echo_error(f"Error reading {history_file_path}: {e}")
            content = f"{{{{HistoryTable|\n|item_id={item_id}\n}}}}"
        return content


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
            echo_error(f"Error reading {file_path}: {e}")

    return ""


def load_infoboxes(infobox_dir):
    # Store extracted infoboxes in memory for efficiency
    """
    Loads infobox data from a directory of text files.

    The function opens each file in the given directory, reads its content,
    extracts the infobox data using regular expressions, and stores it in a
    list of dictionaries. The returned list contains dictionaries with the
    keys 'name', 'category', 'skill_type', 'tags', and 'item_id'.

    Args:
        infobox_dir (str): The path to the directory containing the infobox
            data.

    Returns:
        list: A list of dictionaries containing the extracted infobox data.
    """
    infobox_data_list = []
    infobox_files = [f for f in os.listdir(infobox_dir) if f.endswith('.txt')]

    for file_name in infobox_files:
        file_path = os.path.join(infobox_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            echo_error(f"Error reading {file_path}: {e}")
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

        # Skip items without an item ID
        other_item_id = item.get('item_id', '').strip()
        if not other_item_id:
            continue

        # Ensure the other item has an English name
        english_name = item_id_dict.get(other_item_id)
        if not english_name:
            continue

        # Calculate the relevance score
        relevance = calculate_relevance(current_item, item)
        relevance_scores.append((relevance, english_name))

    # Sort by relevance score in descending order and pick the top 3 English names
    top_relevant_items = sorted(relevance_scores, reverse=True, key=lambda x: x[0])[:3]

    # Extract the names from the top relevant items
    relevant_english_names = [item_name for score, item_name in top_relevant_items]

    return relevant_english_names

"""
see_also_cache = {}

def generate_see_also(language_code, current_item, infobox_data_list, item_id_dict):
    global see_also_cache

    item_id = current_item.get("item_id")

    if item_id in see_also_cache:
        relevant_items = see_also_cache[item_id]
    else:
        # Find the most relevant items, ensuring they have English names
        relevant_items = find_most_relevant_items(current_item, infobox_data_list, item_id_dict)
        see_also_cache[item_id] = relevant_items

    # Create a 'See also' list formatted for a wiki page, ensuring all names are in English
    see_also_list = '\n'.join([f"*{{{{ll|{name}}}}}" for name in relevant_items])

    # Determine the appropriate Navbox template based on the item's category and language code
    category_list = ["Weapon", "Tool", "Clothing", "Food"]
    if current_item.get('category') in category_list:
        navbox_param = current_item.get('category', '').lower()
        if language_code == "en":
            navbox = f"{{{{Navbox items|{navbox_param}}}}}"
        else:
            navbox = f"{{{{Navbox items/{language_code}|{navbox_param}}}}}"
    else:
        if language_code == "en":
            navbox = f"{{{{Navbox items}}}}"
        else:
            navbox = f"{{{{Navbox items/{language_code}}}}}"

    # Return the formatted 'See also' section along with the Navbox template
    return f"{see_also_list}\n\n{navbox}"
"""

def assemble_body(name, original_filename, infobox_name, item_id, category, skill_type, infobox, consumables_dir,
                  infobox_data_list, item_id_dict, fixing_dir, code_dir, distribution_dir, history_dir, crafting_dir,
                  language_code, pbar):
    """
        Assembles the body content for an item's article.

        Args:
            name (str): The name of the item.
            original_filename (str): The original filename of the item.
            infobox_name (str): The name of the infobox.
            item_id (str): The unique ID of the item.
            category (str): The category of the item.
            skill_type (str): The skill type of the item.
            infobox (str): The contents of the item's infobox.
            consumables_dir (str): The directory containing consumables data.
            infobox_data_list (list): A list of dictionaries containing extracted infobox data.
            item_id_dict (dict): A dictionary mapping item IDs to names.
            fixing_dir (str): The directory containing fixing data.
            code_dir (str): The directory containing code data.
            distribution_dir (str): The directory containing distribution data.
            history_dir (str): The directory containing history files.
            language_code (str): The language code to use for the generated content.

        Returns:
            str: The assembled body content for the item's article.
        """

    language_data = LANGUAGE_DATA.get(language_code, LANGUAGE_DATA["en"])
    headers = language_data["headers"]
    help_text = language_data["help_text"]

    body_content = f"\n=={headers['Usage']}==\n{help_text}\n"

    consumable_properties = generate_consumable_properties(item_id, consumables_dir)
    if consumable_properties:
        body_content += f"\n==={headers['Consumable properties']}===\n{consumable_properties}\n"

    sections = {
        headers['Condition']: generate_condition(name, category, skill_type, infobox, fixing_dir, language_code),
        "Crafting": generate_crafting(item_id, crafting_dir, language_code),
        headers['Location']: generate_location(original_filename, infobox_name, item_id, distribution_dir),
        "History": generate_history(item_id, history_dir, language_code),
        headers['Code']: generate_code(item_id, code_dir) + "\n\n{{Navbox items}}",
        # COMMENTED OUT FOR EFFICIENCY # headers['See also']: generate_see_also(language_code, {
#            'name': name,
#            'category': category,
#            'skill_type': skill_type,
#            'tags': re.findall(r'\|tag\d?\s*=\s*(.+)', infobox),
#            'item_id': item_id
#        }, infobox_data_list, item_id_dict)
    }

    for section, content in sections.items():
        if content is None:
            echo_warning(f"{item_id} has no content for '{section}'")
            continue
        if content.strip():
            body_content += f"\n=={section}==\n{content}\n"
        else:
            continue

    return body_content.strip()


def main(run_directly=False):
    # 'run_directly' is used to determine if the script was run directly, or called from another module, such as main.py.
    if not run_directly:
        # Only change the language if the script wasn't run directly - this is already done by get_language_code() if it's undefined.
        Language.init()
    language_code = Language.get()

    global see_also_cache
    CACHE_FILE = "item_see_also_data.json"
    see_also_cache_file = os.path.join(DATA_DIR, CACHE_FILE)
    see_also_cache = load_cache(see_also_cache_file, "see also")

    infobox_dir = os.path.join("output", language_code, "infoboxes")
    output_dir = os.path.join("output", language_code, "articles")
    consumables_dir = os.path.join("output", language_code, "consumables")
    fixing_dir = os.path.join("output", language_code, "fixing")
    dictionary_dir = os.path.join("resources", "item_id_dictionary.csv")
    distribution_dir = os.path.join("output", "distributions", "complete")
    history_dir = os.path.join("resources", "history")
    code_dir = os.path.join("output", "codesnips")
    crafting_dir = os.path.join("output", "recipes", "crafting_combined")

    warnings = []

    if not os.path.exists(infobox_dir):
        echo_warning("Infoboxes directory not found")
        sys.exit(1)

    text_files = [f for f in os.listdir(infobox_dir) if f.endswith('.txt')]

    if not text_files:
        echo_warning("Infoboxes not found")
        sys.exit(1)

    echo_info(f"{len(text_files)} files found")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while True:
        user_choice = input(
            "Do you want to generate:\n1: All items\n2: New items (Don't exist on the wiki currently)\nQ: Quit\n> ").strip().lower()
        if user_choice == 'q':
            return
        if user_choice in ['1', '2']:
            break
        echo("Invalid input. Please enter 1 or 2.")
    generate_all = user_choice == '1'

    infobox_data_list = load_infoboxes(infobox_dir)
    item_id_dict = load_item_id_dictionary(dictionary_dir)

    with tqdm(total=len(text_files), desc="Generating articles", bar_format=PBAR_FORMAT, unit=" files") as pbar:
        for text_file in text_files:
            pbar.set_postfix_str(f"Processing: {text_file[:60].rstrip('.txt')}")
            file_path = os.path.join(infobox_dir, text_file)
            process_file(file_path, output_dir, consumables_dir, infobox_data_list, item_id_dict, generate_all, fixing_dir,
                        code_dir, distribution_dir, history_dir, crafting_dir, language_code, pbar=pbar)
            
            pbar.update(1)
        pbar.bar_format = f"Item articles written to '{output_dir}'."

    if warnings:
        echo_warning("\n".join(warnings))
    
    save_cache(see_also_cache, CACHE_FILE, suppress=True)


if __name__ == "__main__":
    main(run_directly=True)
