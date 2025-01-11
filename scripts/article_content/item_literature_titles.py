from pathlib import Path
from scripts.core import translate
from scripts.parser import literature_parser, item_parser

# TODO: parse this dynamically from SpecialLootSpawns.lua
BOOK = {
    "OnCreateAdventureNonFictionBook": "AdventureNonFiction",
    "OnCreateArtBook": "Art",
    "OnCreateBaseballBook": "Baseball",
    "OnCreateBibleBook": "Bible",
    "OnCreateBiographyBook": "Biography",
    "OnCreateBusinessBook": "Business",
    "OnCreateChildsBook": "Childs",
    "OnCreateComputerBook": "Computer",
    "OnCreateConspiracyBook": "Conspiracy",
    "OnCreateCrimeFictionBook": "CrimeFiction",
    "OnCreateCinemaBook": "Cinema",
    "OnCreateClassicBook": "Classic",
    "OnCreateClassicFictionBook": "ClassicFiction",
    "OnCreateClassicNonfictionBook": "Classic",
    "OnCreateDietBook": "Diet",
    "OnCreateFantasyBook": "Fantasy",
    "OnCreateFarmingBook": "Farming",
    "OnCreateFashionBook": "Fashion",
    "OnCreateGeneralReferenceBook": "GeneralReference",
    "OnCreateGolfBook": "Golf",
    "OnCreateHassBook": "Hass",
    "OnCreateHistoryBook": "History",
    "OnCreateHorrorBook": "Horror",
    "OnCreateLegalBook": "Legal",
    "OnCreateLiteraryFictionBook": "GeneralFiction",
    "OnCreateMedicalBook": "Medical",
    "OnCreateMilitaryBook": "Military",
    "OnCreateMilitaryHistoryBook": "MilitaryHistory",
    "OnCreateMusicBook": "Music",
    "OnCreateNatureBook": "Nature",
    "OnCreateNewAgeBook": "NewAge",
    "OnCreateOccultBook": "Occult",
    "OnCreatePhilosophyBook": "Philosophy",
    "OnCreatePlayBook": "Play",
    "OnCreatePolicingBook": "Policing",
    "OnCreatePoliticsBook": "Politics",
    "OnCreateQuackeryBook": "Quackery",
    "OnCreateQuigleyBook": "Quigley",
    "OnCreateRelationshipBook": "Relationship",
    "OnCreateReligionBook": "Religion",
    "OnCreateRomanceBook": "Romance",
    "OnCreateSadNonFictionBook": "SadNonFiction",
    "OnCreateSchoolTextbookBook": "SchoolTextbook",
    "OnCreateScienceBook": "Science",
    "OnCreateSciFiBook": "SciFi",
    "OnCreateSelfHelpBook": "SelfHelp",
    "OnCreateSexyBook": "Sexy",
    "OnCreateSportsBook": "Sports",
    "OnCreateTeensBook": "Teens",
    "OnCreateThrillerBook": "Thriller",
    "OnCreateTravelBook": "Travel",
    "OnCreateTrueCrimeBook": "TrueCrime",
    "OnCreateWesternBook": "Western",
    # Books with randomized subjects
    "OnCreateFictionBook": "BookSubjectsFictionGenres",
    "OnCreateGeneralNonFictionBook": "BookSubjectsNonFiction",
    "OnCreatePoorBook": "BookSubjectsPoor",
    "OnCreateRichBook": "BookSubjectsRich",
    "OnCreateScaryBook": "BookSubjectsScary",
    "OnCreateBook": "BookSubjects",
}

MAGAZINE = {
    "OnCreateMagazine": "Magazines",
    "OnCreateMagazine2": "Magazines",
    "OnCreateMagazine3": "MagazineSubjects",
    "OnCreateArtMagazine": "Art",
    "OnCreateBusinessMagazine": "Business",
    "OnCreateCarMagazine": "Cars",
    "OnCreateChildsMagazine": "Childs",
    "OnCreateCinemaMagazine": "Cinema",
    "OnCreateCrimeMagazine": "Crime",
    "OnCreateFashionMagazine": "Fashion",
    "OnCreateFirearmMagazine": "Firearm",
    "OnCreateGamingMagazine": "Gaming",
    "OnCreateGolfMagazine": "Golf",
    "OnCreateHealthMagazine": "Health",
    "OnCreateHobbyMagazine": "Hobby",
    "OnCreateHorrorMagazine": "Horror",
    "OnCreateHumorMagazine": "Humor",
    "OnCreateMilitaryMagazine": "Military",
    "OnCreateMusicMagazine": "Music",
    "OnCreateOutdoorsMagazine": "Outdoors",
    "OnCreatePoliceMagazine": "Police",
    "OnCreatePopularMagazine": "Popular",
    "OnCreateRichMagazine": "Rich",
    "OnCreateScienceMagazine": "Science",
    "OnCreateSportsMagazine": "Sports",
    "OnCreateTechMagazine": "Tech",
    "OnCreateTeensMagazine": "Teens",
}

# 0: literature type
# 1: multipleChance -- taken from SpecialLootSpawns.lua
SCHEMATIC = {
    "OnCreateExplosivesSchematic": ["ExplosiveSchematics", 40],
    "OnCreateMeleeWeaponSchematic": ["MeleeWeaponSchematics", 30],
    "OnCreateBSToolsSchematic": ["BSToolsSchematics", 50],
    "OnCreateArmorSchematic": ["ArmorSchematics", 30],
    "OnCreateCookwareSchematic": ["CookwareSchematic", 40]
}

SPECIAL = {
    "OnCreateLocket": "Locket",
    "OnCreateDoodleKids": "DoodleKids",
    "OnCreateDoodle": "Doodle",
    "OnCreatePostcard": "Postcards"
}

# 0: literature type
# 1: translation key
GENERIC_LITERATURE = {
    "OnCreateRPGmanual": ["RPGs", "RPG"],
    "OnCreateCatalogue": ["Catalogues", "IGUI"],
    # TODO: may need to look into this one more and determine if the types should be split. One is more common than the others
    "OnCreateStockCertificate": [["StockCertificate1", "StockCertificate2"], "IGUI"],
    "OnCreateGenericMail": ["GenericMail", "IGUI"],
    "OnCreateLetterHandwritten": ["LetterHandwritten", "IGUI"],
    "OnCreateDogTag_Pet": ["DogTags", "IGUI_PetName_"]
}

# TODO: add business cards. These may combine 'BusinessCards' with 'JobTitles'. It also gets a random forename and surname. 

# TODO: Creates the string from various translation strings, only 1 is from OnCreate
# OnCreateLocket: "DisplayName" + "IGUI_LocketText" + "IGUI_Photo_..." + "Locket"
# OnCreateDoodleKids: "DisplayName" + "IGUI_PhotoOf" + "IGUI_Photo_..." + "DoodleKids"
# OnCreateDoodle: "DisplayName" + "IGUI_PhotoOf" + "IGUI_Photo_..." + "Doodle"
# OnCreatePostcards: "DisplayName" + "IGUI_PhotoOf" + "IGUI_Photo_..." + "Postcards"

# Process generic literature
def process_generic(item_id, item_data, on_create):
    literature_data = literature_parser.get_literature_data()
    literature_titles = []

    if on_create in GENERIC_LITERATURE:

        literature = GENERIC_LITERATURE[on_create][0]
        if isinstance(literature, list):
            for value in literature:
                literature_titles.extend(literature_data[value])
        else:
            literature_titles = literature_data[literature]
        translation_str = GENERIC_LITERATURE[on_create][1]

        for i, title in enumerate(literature_titles):
            literature_titles[i] = translate.get_translation(title, translation_str)

        write_to_file(item_id, literature_titles, "generic")


# Process special items
def process_special(item_id, item_data, on_create):
    literature_data = literature_parser.get_literature_data()
    special_titles = []

    if on_create in SPECIAL:
        title_type = SPECIAL[on_create]
        special_titles = literature_data[title_type]

        write_to_file(item_id, special_titles, title_type.lower())


# Process schematic data
def process_schematic(item_id, item_data, on_create):
    literature_data = literature_parser.get_literature_data()
    schematic_recipes = []

    if on_create in SCHEMATIC:

        literature = SCHEMATIC[on_create][0]
        schematic_recipes = literature_data[literature]

        for i, title in enumerate(schematic_recipes):
            schematic_recipes[i] = translate.get_translation(title, None, "en")
            if schematic_recipes[i] == title:
                schematic_recipes[i] = translate.get_translation(title, "TeachedRecipes")
        
        multiple_chance = SCHEMATIC[on_create][1]
        schematic_recipes.append(multiple_chance)

        write_to_file(item_id, schematic_recipes, "schematic")


# Process comic data
def process_comic(item_id, item_data, on_create):
    literature_data = literature_parser.get_literature_data()
    comic_titles = []

    literature = "ComicBooks"
    comic_titles = literature_data[literature]
    
    updated_values = {}
    for title in comic_titles:
        nested_data = literature_data["ComicBookDetails"].get(title, {"issues": "1", "inPrint": False})

        if on_create == "OnCreateComicBookRetail" and not nested_data["inPrint"]:
            continue

        translated_title = translate.get_translation(title, "ComicTitle")
        updated_values[translated_title] = nested_data

        comic_titles = updated_values

    write_to_file(item_id, comic_titles, "comic")


# Process magazine data
def process_magazine(item_id, item_data, on_create):
    literature_data = literature_parser.get_literature_data()
    magazine_titles = {}
    item_tags = item_data.get("Tags", "")
                
    if on_create in ["OnCreateMagazine3"]:
        subjects = literature_data[MAGAZINE[on_create]]
        for subject in subjects:
            magazine_titles[subject] = literature_data["MagazineSubjects"][subject]

    elif on_create in ["OnCreateMagazine", "OnCreateMagazine2"]:
        subject = MAGAZINE[on_create]
        magazine_titles["Default"] = literature_data[subject]

    else:
        subject = MAGAZINE[on_create]
        magazine_titles["Default"] = literature_data["MagazineSubjects"][subject]
    
    for key, values in magazine_titles.items():
        updated_values = {}
        for title in values:
            nested_data = literature_data["MagazineDetails"].get(title, {"firstYear": "1970"})

            # Add firstYear if "New" is in tags
            if "New" in item_tags:
                nested_data["firstYear"] = "1993"

            translated_title = translate.get_translation(title, "MagazineTitle")
            updated_values[translated_title] = nested_data

        magazine_titles[key] = updated_values

    write_to_file(item_id, magazine_titles, "magazine")


# Process book data
def process_book(item_id, item_data, on_create):
    literature_data = literature_parser.get_literature_data()
    book_titles = {}

    if on_create in ["OnCreateFictionBook", "OnCreateGeneralNonFictionBook", "OnCreatePoorBook", "OnCreateRichBook", "OnCreateScaryBook", "OnCreateBook"]:
        subjects = literature_data[BOOK[on_create]]
        for subject in subjects:
            book_titles[subject] = literature_data["BookTitles"][subject]

    else:
        subject = BOOK[on_create]
        book_titles["Default"] = literature_data["BookTitles"][subject]
    
    hardcover = False
    paperback = False
    hardcover_tags = ["Hardcover", "HollowBook", "FancyBook"]
    paperback_tags = ["Softcover"]

    item_tags = item_data.get("Tags", "")

    # Convert str to list, so it can be processed properly
    if isinstance(item_tags, str):
        item_tags = [item_tags]

    for tag in item_tags:
        if tag in hardcover_tags or "Book" in item_id:
            hardcover = True
        if tag in paperback_tags or "Paperback" in item_id:
            paperback = True
    
    # Filter book titles based on cover type
    for subject, titles in book_titles.items():
        filtered_titles = []
        for title in titles:
            details = literature_data["BookDetails"].get(title, {})
            cover = details.get("cover", "both")

            if cover == "both" or (cover == "hardcover" and hardcover) or (cover == "softcover" and paperback):
                filtered_titles.append(translate.get_translation(title, "BookTitle"))

        book_titles[subject] = filtered_titles

        write_to_file(item_id, book_titles, "book")


def write_to_file(item_id, literature_titles, literature_type):
    language_code = translate.get_language_code()
    output_dir = Path("output") / language_code / "literature_lists" / f"{literature_type}_titles"
    output_path = Path(output_dir) / f"{item_id}.txt"

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(f"=={item_id}==\n")
        if literature_type == "book":
            # Determine if the format has multiple dictionaries
            if len(literature_titles) == 1 and "Default" in literature_titles:
                # No subjects
                file.write('<div class="list-columns" style="column-width:450px; max-width:1500px;">\n')
                for title in sorted(literature_titles["Default"]):
                    file.write(f"* {title}\n")
                file.write('</div>\n')
            else:
                # Subjects
                for subject in sorted(literature_titles):  # Sort subjects alphabetically
                    titles = sorted(literature_titles[subject])
                    file.write(f"==={subject}===\n")
                    file.write('<div class="list-columns" style="column-width:450px; max-width:1500px;">\n')
                    for title in titles:
                        file.write(f"* {title}\n")
                    file.write('</div>\n\n')
        
        elif literature_type == "magazine":
            # Determine if the format has multiple dictionaries
            if len(literature_titles) == 1 and "Default" in literature_titles:
                # No subjects
                file.write('{| class="wikitable theme-red mw-collapsible sortable" style="text-align:center;"\n')
                file.write('|+ style="min-width: 300px;" | List of magazine variants\n')
                file.write('! Title !! Earliest year\n')
                for title in sorted(literature_titles["Default"]):
                    first_year = literature_titles["Default"][title].get("firstYear", "1970")
                    year_range = f"{first_year}–1993"
                    if first_year == "1993":
                        year_range = first_year
                    file.write(f"|-\n| {title} || {first_year}\n")
                file.write('|}\n')
            else:
                # Subjects
                for subject in sorted(literature_titles):
                    titles = sorted(literature_titles[subject])
                    file.write(f"==={subject}===\n")
                    file.write('<div class="list-columns" style="column-width:400px; max-width:900px;">\n')
                    for title in titles:
                        file.write(f"* {title}\n")
                    file.write('</div>\n\n')

        elif literature_type == "comic":
            file.write('{| class="wikitable theme-red mw-collapsible mw-collapsed sortable" style="text-align:center;"\n')
            file.write('|+ style="min-width: 300px;" | List of comic book variants\n')
            file.write('! Title !! First available !! Total issues\n')
            for title in sorted(literature_titles):
                issues = literature_titles[title].get("issues", 0) + 1
                issues_start = 1
                if issues > 1:
                    if item_id == "Base.ComicBook_Retail":
                        # Earliest issue will be 4 less than the latest
                        issues_start = max(issues - 4 + 1, 1)
                file.write(f"|-\n| {title} || {issues_start} || {issues}\n")
            file.write('|}\n')

        elif literature_type == "schematic":
            multiple_chance = literature_titles[-1]
            file.write(f"A schematic can be read, teaching the player [[crafting]] recipes.\n\n")
            file.write("===Learned recipes===\n")
            file.write(f"The following are the recipes this schematic can include. Each schematic can contain up to 5 recipes, with a {100 - multiple_chance}% chance of having only 1. Each additional recipe beyond the first has an equal probability.\n")
            file.write('<div class="list-columns" style="column-width:400px; max-width:900px;">\n')
            for title in sorted(literature_titles[:-1]):
                file.write(f"* {title}\n")
            file.write('</div>')

        elif literature_type == "locket":
            file.write('<div class="list-columns" style="column-width:400px; max-width:900px;">\n')
            name = translate.get_translation(item_id)
            locket_text = translate.get_translation("IGUI_LocketText", "IGUI_LocketText")
            for title in sorted(literature_titles):
                photo = translate.get_translation(title, "Photo")
                full_name = f"{name} {locket_text} {photo}"
                file.write(f"* {full_name}\n")
            file.write('</div>')

        elif literature_type == "doodlekids":
            file.write('<div class="list-columns" style="column-width:400px; max-width:900px;">\n')
            name = translate.get_translation(item_id)
            photo_text = translate.get_translation("IGUI_PhotoOf", "IGUI_PhotoOf")
            for title in sorted(literature_titles):
                photo = translate.get_translation(title, "Doodle")
                full_name = f"{name} {photo_text} {photo}"
                file.write(f"* {full_name}\n")
            file.write('</div>')

        elif literature_type == "doodle":
            file.write('<div class="list-columns" style="column-width:400px; max-width:900px;">\n')
            name = translate.get_translation(item_id)
            photo_text = translate.get_translation("IGUI_PhotoOf", "IGUI_PhotoOf")
            for title in sorted(literature_titles):
                photo = translate.get_translation(title, "Photo")
                full_name = f"{name} {photo_text} {photo}"
                file.write(f"* {full_name}\n")
            file.write('</div>')

        elif literature_type == "postcards":
            file.write('<div class="list-columns" style="column-width:400px; max-width:900px;">\n')
            name = translate.get_translation(item_id)
            photo_text = translate.get_translation("IGUI_PhotoOf", "IGUI_PhotoOf")
            for title in sorted(literature_titles):
                photo = translate.get_translation(title, "Photo")
                full_name = f"{name} {photo_text} {photo}"
                file.write(f"* {full_name}\n")
            file.write('</div>')

        else:
            file.write('<div class="list-columns" style="column-width:400px; max-width:900px;">\n')
            for title in sorted(literature_titles):
                file.write(f"* {title}\n")
            file.write('</div>')



def combine_txt_files(type):
    language_code = translate.get_language_code()
    source_dir = Path("output") / language_code / "literature_lists"
    source_path = Path(source_dir) / f"{type}_titles"
    combined_file_path = Path(source_dir) / f"combined_{type}_list.txt"

    combined_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(combined_file_path, 'w', encoding='utf-8') as combined_file:
        for txt_file in sorted(source_path.glob("*.txt")):
            with open(txt_file, 'r', encoding='utf-8') as file:
                combined_file.write(file.read())
                combined_file.write("\n\n")

    print(f"Combined file created at: {combined_file_path}")


def main():
    for item_id, item_data in item_parser.get_item_data().items():
        if "OnCreate" not in item_data:
            continue
        on_create = item_data["OnCreate"]
        # Remove "SpecialLootSpawns." prefix
        on_create = on_create.removeprefix("SpecialLootSpawns.")
        if on_create in BOOK:
            process_book(item_id, item_data, on_create)
        elif on_create in MAGAZINE:
            process_magazine(item_id, item_data, on_create)
        elif on_create in ["OnCreateComicBookRetail", "OnCreateComicBook"]:
            process_comic(item_id, item_data, on_create)
        elif on_create in SCHEMATIC:
            process_schematic(item_id, item_data, on_create)
        elif on_create in SPECIAL:
            process_special(item_id, item_data, on_create)
        elif on_create in GENERIC_LITERATURE:
            process_generic(item_id, item_data, on_create)

    combine_txt_files("book")
    combine_txt_files("magazine")
    combine_txt_files("comic")
    combine_txt_files("schematic")
    combine_txt_files("generic")


if __name__ == "__main__":
    main()