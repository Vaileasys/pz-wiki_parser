import os, re, sys, csv
from tqdm import tqdm
from scripts.core.language import Language
from scripts.core.constants import PBAR_FORMAT, DATA_DIR, ITEM_DIR
from scripts.core.cache import save_cache, load_cache
from scripts.utils import echo

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
        echo.error(f"Error reading {dictionary_dir}: {e}")

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

    skill_type = re.sub(r'\[\[(?:[^\|\]]*\|)?([^\|\]]+)\]\]', r'\1', skill_type).strip()

    # Determine the correct header based on the category and skill type
    if category in category_dict:
        if category_dict[category] == "use_skill_type":
            header = skill_type_dict.get(skill_type, "{{Header|Project Zomboid|Items|Weapons}}")
        else:
            header = category_dict[category]
    else:
        header = "{{Header|Project Zomboid|Items}}"

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
    filename = re.sub(r'[^\w\-_\. ]', '_', item_id) + '.txt'
    file_path = os.path.join(consumables_dir, filename)

    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            echo.error(f"Error reading {file_path}: {e}")

    return ""


def generate_condition(name, category, skill_type, infobox, fixing_dir, language_code):
    language_data = LANGUAGE_DATA.get(language_code, LANGUAGE_DATA["en"])
    m_max = re.search(r'\|condition_max\s*=\s*(\d+)', infobox)
    m_low = re.search(r'\|condition_lower_chance\s*=\s*(\d+)', infobox)

    if not m_max or not m_low:
        return ""
    condition_max = m_max.group(1)
    condition_lower_chance = m_low.group(1)
    skill_type_lower = skill_type.lower().split('|')[-1]
    text = language_data["condition_text"].format(
        name=name,
        condition_max=condition_max,
        skill_type=skill_type,
        skill_type_lower=skill_type_lower,
        condition_lower_chance=condition_lower_chance
    )
    text = text[0].upper() + text[1:]
    repairing_header = language_data["headers"]["Repairing"]
    token = f"|item_id={re.search(r'\|item_id\s*=\s*(.+)', infobox).group(1).strip()}"
    if os.path.isdir(fixing_dir):
        for fname in os.listdir(fixing_dir):
            path = os.path.join(fixing_dir, fname)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                if token in content:
                    text += f"\n\n==={repairing_header}===\n{content.strip()}"
                    break
            except Exception as e:
                echo.error(f"Error reading {path}: {e}")
    return text


def generate_crafting(item_id, crafting_dir, teachedrecipes_dir, language_code):
    if language_code != "en":
        return ""

    parts = []

    # What it crafts
    what_fp = os.path.join(crafting_dir, f"{item_id}_whatitcrafts.txt")
    if os.path.isfile(what_fp):
        try:
            with open(what_fp, 'r', encoding='utf-8') as fh:
                parts.append(fh.read().strip())
        except Exception as e:
            echo.error(f"Error reading {what_fp}: {e}")

    # Researchable recipes
    research_fp = os.path.join(crafting_dir, f"{item_id}_research.txt")
    if os.path.isfile(research_fp):
        try:
            with open(research_fp, 'r', encoding='utf-8') as fh:
                research = fh.read().strip()
            parts.append(
                "====Researchable recipes====\n"
                f"{research}"
            )
        except Exception as e:
            echo.error(f"Error reading {research_fp}: {e}")

    # Learned recipes
    learned_fp = os.path.join(teachedrecipes_dir, f"{item_id}_Teached.txt")
    if os.path.isfile(learned_fp):
        try:
            with open(learned_fp, 'r', encoding='utf-8') as fh:
                learned = fh.read().strip()
            parts.append(
                "====Learned recipes====\n"
                f"{learned}"
            )
        except Exception as e:
            echo.error(f"Error reading {learned_fp}: {e}")

    if not parts:
        return ""
    return "\n\n".join(parts)


def generate_building(item_id, building_dir):
    path = os.path.join(building_dir, f"{item_id}_constructionwhatitcrafts.txt")
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                return fh.read().strip()
        except Exception as e:
            echo.error(f"Error reading {path}: {e}")
    return ""


def generate_learned_recipes(item_id, teached_dir):
    path = os.path.join(teached_dir, f"{item_id}_Teached.txt")
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                return fh.read().strip()
        except Exception as e:
            echo.error(f"Error reading {path}: {e}")
    return ""


def generate_body_part(item_id, body_parts_dir):
    path = os.path.join(body_parts_dir, f"{item_id}.txt")
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read().strip()
            return (
                "{{Main|BodyLocation{{!}}Body location}}\n"
                "{| style=\"text-align:center;\"\n"
                f"|'''{item_id}'''<br>{content}\n"
                "|}"
            )
        except Exception as e:
            echo.error(f"Error reading {path}: {e}")
    return ""


def generate_location(original_filename, infobox_name, item_id, distribution_dir):
    if not os.path.isdir(distribution_dir):
        return ""
    for name in (original_filename, infobox_name, re.sub(r'.*\.', '', item_id)):
        path = os.path.join(distribution_dir, name + '.txt')
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    return fh.read().strip()
            except Exception as e:
                echo.error(f"Error reading {path}: {e}")
    return ""


def generate_obtaining(item_id, crafting_dir, original_filename, infobox_name, distribution_dir):
    parts = []
    # Recipes
    howto = os.path.join(crafting_dir, f"{item_id}_howtocraft.txt")
    if os.path.isfile(howto):
        try:
            with open(howto, 'r', encoding='utf-8') as fh:
                parts.append(f"===Recipes===\n{fh.read().strip()}")
        except Exception as e:
            echo.error(f"Error reading {howto}: {e}")

    # Loot
    loot = generate_location(original_filename, infobox_name, item_id, distribution_dir)
    if loot:
        parts.append(f"===Loot===\n{loot}")
    return "\n\n".join(parts)


def generate_history(item_id, history_dir, language_code):
    if language_code != "en":
        return ""
    path = os.path.join(history_dir, f"{item_id}.txt")
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                return fh.read().strip()
        except Exception as e:
            echo.error(f"Error reading {path}: {e}")
    return f"{{{{HistoryTable|\n|item_id={item_id}\n}}}}"


def generate_code(item_id, code_dir):
    if not os.path.isdir(code_dir):
        return ""
    filename = re.sub(r'.*\.', '', item_id) + '.txt'
    path = os.path.join(code_dir, filename)
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                return f"{{{{CodeBox|\n{fh.read().strip()}\n}}}}"
        except Exception as e:
            echo.error(f"Error reading {path}: {e}")
    return ""


def load_infoboxes(infobox_dir):
    infobox_data = []
    for fname in os.listdir(infobox_dir):
        if not fname.endswith('.txt'):
            continue
        path = os.path.join(infobox_dir, fname)
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                txt = fh.read()
        except Exception as e:
            echo.error(f"Error reading {path}: {e}")
            continue
        infobox_data.append({
            'name': re.search(r'\|name\s*=\s*(.+)', txt).group(1).strip() if re.search(r'\|name\s*=\s*(.+)', txt) else "",
            'category': re.search(r'\|category\s*=\s*(.+)', txt).group(1).strip() if re.search(r'\|category\s*=\s*(.+)', txt) else "",
            'skill_type': re.search(r'\|skill_type\s*=\s*(.+)', txt).group(1).strip() if re.search(r'\|skill_type\s*=\s*(.+)', txt) else "",
            'tags': [t.strip() for t in re.findall(r'\|tag\d?\s*=\s*(.+)', txt)],
            'item_id': re.search(r'\|item_id\s*=\s*(.+)', txt).group(1).strip() if re.search(r'\|item_id\s*=\s*(.+)', txt) else ""
        })
    return infobox_data


def assemble_body(name, original_filename, infobox_name, item_id, category, skill_type,
                  infobox, consumables_dir, fixing_dir, code_dir, distribution_dir,
                  history_dir, crafting_dir, building_dir, teachedrecipes_dir,
                  body_parts_dir, language_code,
                  ):
    language_data = LANGUAGE_DATA.get(language_code, LANGUAGE_DATA["en"])
    headers       = language_data["headers"]
    help_text     = language_data["help_text"]

    body = f"\n=={headers['Usage']}==\n{help_text}\n"

    # Crafting
    crafting_inner = generate_crafting(item_id, crafting_dir, teachedrecipes_dir, language_code)
    if crafting_inner:
        body += f"\n===Crafting===\n{crafting_inner}\n"

    # Building
    build_txt = generate_building(item_id, building_dir)
    if build_txt:
        body += f"\n===Building===\n{build_txt}\n"

    # Body part
    bp = generate_body_part(item_id, body_parts_dir)
    if bp:
        body += f"\n===Body part===\n{bp}\n"

    # Consumable properties
    cons = generate_consumable_properties(item_id, consumables_dir)
    if cons:
        body += f"\n==={headers['Consumable properties']}===\n{cons}\n"

    # Condition
    cond = generate_condition(name, category, skill_type, infobox, fixing_dir, language_code)
    if cond:
        body += f"\n===Condition===\n{cond}\n"



    sections = {
        "Obtaining": generate_obtaining(item_id, crafting_dir, original_filename, infobox_name, distribution_dir),
        "History":    generate_history(item_id, history_dir, language_code),
        headers['Code']: generate_code(item_id, code_dir) + "\n\n==Navigation==\n{{Navbox items}}",
    }
    for title, content in sections.items():
        if content and content.strip():
            body += f"\n=={title}==\n{content}\n"

    return body.strip()


def process_files(file_path,
                  output_dir,
                  consumables_dir,
                  item_id_dict,
                  generate_all,
                  fixing_dir,
                  code_dir,
                  distribution_dir,
                  history_dir,
                  crafting_dir,
                  building_dir,
                  teached_dir,
                  body_parts_dir,
                  language_code,
                  pbar):
    try:
        with open(file_path, 'r', encoding='utf-8') as fh:
            content = fh.read()
    except Exception as e:
        echo.error(f"Error reading {file_path}: {e}")
        return

    infobox_match = re.search(r'(\{\{Infobox item.*?\}\})', content, re.DOTALL)
    if not infobox_match:
        echo.warning(f"Infobox not found in {file_path}")
        return
    infobox = infobox_match.group(1)

    item_id_match = re.search(r'\|item_id\s*=\s*(.+)', infobox)
    if not item_id_match:
        echo.warning(f"Item ID not found in {file_path}")
        return
    item_id = item_id_match.group(1).strip()

    if not generate_all and item_id in item_id_dict:
        return

    version_match = re.search(r'\|infobox_version\s*=\s*([\d\.]+)', infobox)
    infobox_version = version_match.group(1) if version_match else ""
    name_match = re.search(r'\|name\s*=\s*(.+)', infobox)
    name = name_match.group(1).strip() if name_match else ""
    lowercase_name = name.lower()
    category_match = re.search(r'\|category\s*=\s*(.+)', infobox)
    category = category_match.group(1).strip() if category_match else ""
    skill_type_match = re.search(r'\|skill_type\s*=\s*(.+)', infobox)
    skill_type = skill_type_match.group(1).strip() if skill_type_match else ""

    header = generate_header(category, skill_type, infobox_version, language_code, name)
    body_content = assemble_body(
        name,
        os.path.basename(file_path),
        name,
        item_id,
        category,
        skill_type,
        infobox,
        consumables_dir,
        fixing_dir,
        code_dir,
        distribution_dir,
        history_dir,
        crafting_dir,
        building_dir,
        teached_dir,
        body_parts_dir,
        language_code,
    )
    intro = generate_intro(lowercase_name, language_code)

    new_content = f"{header}\n{infobox}\n{intro}\n\n{body_content}"
    safe_id = re.sub(r'[^\w\-_\. ]', '_', item_id) + '.txt'
    new_path = os.path.join(output_dir, safe_id)
    try:
        with open(new_path, 'w', encoding='utf-8') as fh:
            fh.write(new_content.strip())
    except Exception as e:
        echo.error(f"Error writing {new_path}: {e}")


def main(run_directly=False):
    if not run_directly:
        Language.init()
    language_code = Language.get()

    cache_file = "item_see_also_data.json"
    see_also_cache = load_cache(os.path.join(DATA_DIR, cache_file), "see also")

    output_item_dir = ITEM_DIR.format(language_code=language_code)
    infobox_dir = os.path.join(output_item_dir, "infoboxes")
    output_dir = os.path.join(output_item_dir, "articles")
    consumables_dir = os.path.join("output", language_code, "consumables")
    fixing_dir = os.path.join("output", language_code, "fixing")
    dictionary_dir = os.path.join("resources", "item_id_dictionary.csv")
    distribution_dir = os.path.join("output", "distributions", "complete")
    history_dir = os.path.join("resources", "history")
    code_dir = os.path.join("output", "codesnips")
    crafting_dir = os.path.join("output", "recipes", "crafting")
    building_dir = os.path.join("output", "recipes", "building")
    teached_dir = os.path.join("output", "recipes", "teachedrecipes")
    body_parts_dir = os.path.join("output", language_code, "body_parts")

    if not os.path.isdir(infobox_dir):
        echo.warning("Infoboxes directory not found")
        sys.exit(1)
    text_files = [f for f in os.listdir(infobox_dir) if f.endswith('.txt')]
    if not text_files:
        echo.warning("Infoboxes not found")
        sys.exit(1)

    echo.info(f"{len(text_files)} files found")
    os.makedirs(output_dir, exist_ok=True)

    while True:
        choice = input("Do you want to generate:\n1: All items\n2: New items\nQ: Quit\n> ").strip().lower()
        if choice in ('1', '2', 'q'):
            break
        echo.write("Invalid input. Please enter 1, 2, or Q.")
    if choice == 'q':
        return
    generate_all = (choice == '1')

    item_id_dict = load_item_id_dictionary(dictionary_dir)

    with tqdm(total=len(text_files), desc="Generating articles", bar_format=PBAR_FORMAT, unit=" files") as pbar:
        for fname in text_files:
            pbar.set_postfix_str(f"Processing: {fname[:-4]}")
            process_files(
                os.path.join(infobox_dir, fname),
                output_dir,
                consumables_dir,
                item_id_dict,
                generate_all,
                fixing_dir,
                code_dir,
                distribution_dir,
                history_dir,
                crafting_dir,
                building_dir,
                teached_dir,
                body_parts_dir,
                language_code,
                pbar
            )
            pbar.update(1)
        pbar.bar_format = f"Item articles written to '{output_dir}'."

    save_cache(see_also_cache, cache_file, suppress=True)


if __name__ == "__main__":
    main(run_directly=True)