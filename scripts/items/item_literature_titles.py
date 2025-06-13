from pathlib import Path
from scripts.parser import literature_parser
from scripts.core.language import Language, Translate
from scripts.objects.item import Item
from scripts.objects.craft_recipe import CraftRecipe

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
    "OnCreateCookwareSchematic": ["CookwareSchematic", 40],
    "OnCreateSurvivalSchematic": ["SurvivalSchematics", 40],
    "OnCreateRecipeClipping": ["FoodRecipes", None] # Special case
}

SPECIAL = {
    "OnCreateLocket": "Locket",
    "OnCreateDoodleKids": "DoodleKids",
    "OnCreateDoodle": "Doodle",
    "OnCreatePostcard": "Postcards",
    "OnCreatePhoto": "OldPhotos",
    "OnCreatePhoto_Secret": "SecretPhotos",
    "OnCreatePhoto_Racy": "RacyPhotos",
    "OnCreateBusinessCard": ["BusinessCards", "JobTitles"]
}

LOCATION_LITERATURE = {
    "OnCreateFlier": "Fliers",
    "OnCreateBrochure": "Brochures",
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


# Location litearture, e.g. flier & brochure
def process_location_literature(item: Item, on_create):
    literature_data = literature_parser.get_literature_data()
    literature_data = literature_data["PrintMediaDefinitions"]
    business_titles = []

    literature_key = LOCATION_LITERATURE[on_create]
    business_list = literature_data[literature_key]
    businesses = {key: literature_data["MiscDetails"].get(key, None) for key in business_list}
    for business, business_data in businesses.items():
        for location in business_data["location1"]:
            x1 = location["x1"]
            x2 = location["x2"]
            y1 = location["y1"]
            y2 = location["y2"]

            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)

            business_string = business + "_title"
            business_name = Translate.get(business + "_title", "PrintMedia")
            if business_name == business_string:
                business_name = Translate.get(business + "_title", "PrintText")

            business_titles.append({
                "name": business_name,
                "center": f"{x_center}x{y_center}",
                "coord1": f"{x1}x{y1}",
                "coord2": f"{x2}x{y2}"
            })

    write_to_file(item.item_id, business_titles, "flier")


def process_generic(item: Item, on_create):
    literature_data = literature_parser.get_literature_data()
    literature_titles = []

    if on_create in GENERIC_LITERATURE:
        literature = GENERIC_LITERATURE[on_create][0]
        if isinstance(literature, list):
            for value in literature:
                literature_titles.extend(literature_data["SpecialLootSpawns"][value])
        else:
            literature_titles = literature_data["SpecialLootSpawns"][literature]

        translation_str = GENERIC_LITERATURE[on_create][1]

        for i, title in enumerate(literature_titles):
            literature_titles[i] = Translate.get(title, translation_str)

        write_to_file(item.item_id, literature_titles, "generic")


def process_special(item: Item, on_create):
    """Process special items"""
    literature_data = literature_parser.get_literature_data()
    special_titles = []

    if on_create in SPECIAL:
        title_type = SPECIAL[on_create]
        if isinstance(title_type, list):
            for id in title_type:
                special_titles = literature_data["SpecialLootSpawns"][id]
                write_to_file(item.item_id, special_titles, id.lower())
        else:
            special_titles = literature_data["SpecialLootSpawns"][title_type]
            
            if "Photo" in on_create:
                title_type = "photo"

            write_to_file(item.item_id, special_titles, title_type.lower())


def process_schematic(item: Item, on_create):
    """Process schematic data"""

    literature_data = literature_parser.get_literature_data()
    schematic_recipes = []

    if on_create in SCHEMATIC:

        literature = SCHEMATIC[on_create][0]
        schematic_recipes = literature_data["SpecialLootSpawns"][literature]

        for i, title in enumerate(schematic_recipes):
            schematic_recipes[i] = CraftRecipe(title).wiki_link
        
        multiple_chance = SCHEMATIC[on_create][1]
        schematic_recipes.append(multiple_chance)

        if not multiple_chance:
            literature_type = "recipe"
        else:
            literature_type = "schematic"

        write_to_file(item.item_id, schematic_recipes, literature_type)


def process_comic(item: Item, on_create):
    """Process comic data"""
    literature_data = literature_parser.get_literature_data()
    comic_titles = []

    literature = "ComicBooks"
    comic_titles = literature_data["SpecialLootSpawns"][literature]
    
    updated_values = {}
    for title in comic_titles:
        nested_data = literature_data["SpecialLootSpawns"]["ComicBookDetails"].get(title, {"issues": "1", "inPrint": False})

        if on_create == "OnCreateComicBookRetail" and not nested_data["inPrint"]:
            continue

        translated_title = Translate.get(title, "ComicTitle")
        updated_values[translated_title] = nested_data

        comic_titles = updated_values

    write_to_file(item.item_id, comic_titles, "comic")


def process_magazine(item: Item, on_create):
    """Process magazine data"""
    literature_data = literature_parser.get_literature_data()
    magazine_titles = {}
    
    if on_create in ["OnCreateMagazine3"]:
        subjects = literature_data["SpecialLootSpawns"][MAGAZINE[on_create]]
        for subject in subjects:
            magazine_titles[subject] = literature_data["SpecialLootSpawns"]["MagazineSubjects"][subject]

    elif on_create in ["OnCreateMagazine", "OnCreateMagazine2"]:
        subject = MAGAZINE[on_create]
        magazine_titles["Default"] = literature_data["SpecialLootSpawns"][subject]

    else:
        subject = MAGAZINE[on_create]
        magazine_titles["Default"] = literature_data["SpecialLootSpawns"]["MagazineSubjects"][subject]
    
    for key, values in magazine_titles.items():
        updated_values = {}
        for title in values:
            nested_data = literature_data["SpecialLootSpawns"]["MagazineDetails"].get(title, {"firstYear": "1970"})

            # Add firstYear if "New" is in tags
            if item.has_tag("New"):
                nested_data["firstYear"] = "1993"

            translated_title = Translate.get(title, "MagazineTitle")
            updated_values[translated_title] = nested_data

        magazine_titles[key] = updated_values

    write_to_file(item.item_id, magazine_titles, "magazine")


def process_book(item: Item, on_create):
    """Process book data"""
    literature_data = literature_parser.get_literature_data()
    book_titles = {}

    on_create_books = [
        "OnCreateFictionBook",
        "OnCreateGeneralNonFictionBook",
        "OnCreatePoorBook",
        "OnCreateRichBook",
        "OnCreateScaryBook",
        "OnCreateBook"
    ]

    if on_create in on_create_books:
        subjects = literature_data["SpecialLootSpawns"][BOOK[on_create]]
        for subject in subjects:
            book_titles[subject] = literature_data["SpecialLootSpawns"]["BookTitles"][subject]

    else:
        subject = BOOK[on_create]
        book_titles["Default"] = literature_data["SpecialLootSpawns"]["BookTitles"][subject]
    
    hardcover = False
    paperback = False
    hardcover_tags = ["Hardcover", "HollowBook", "FancyBook"]
    paperback_tags = ["Softcover"]

    for tag in item.tags:
        if tag in hardcover_tags or "Book" in item.item_id:
            hardcover = True
        if tag in paperback_tags or "Paperback" in item.item_id:
            paperback = True
    
    # Filter book titles based on cover type
    for subject, titles in book_titles.items():
        filtered_titles = []
        for title in titles:
            details = literature_data["SpecialLootSpawns"]["BookDetails"].get(title, {})
            cover = details.get("cover", "both")

            if cover == "both" or (cover == "hardcover" and hardcover) or (cover == "softcover" and paperback):
                filtered_titles.append(Translate.get(title, "BookTitle"))

        book_titles[subject] = filtered_titles

        write_to_file(item.item_id, book_titles, "book")


def write_to_file(item_id, literature_titles, literature_type):
    language_code = Language.get()
    output_dir = Path("output") / language_code / "literature_lists" / f"{literature_type}_titles"
    output_path = Path(output_dir) / f"{item_id}.txt"

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(f"=={item_id}==\n")
        if literature_type == "book":
            # No subjects
            if len(literature_titles) == 1 and "Default" in literature_titles:
                file.write('<div class="list-columns" style="column-width: 450px; max-width: 1500px;">\n')
                for title in sorted(literature_titles["Default"]):
                    file.write(f"* {title}\n")
                file.write('</div>\n')
            else:
                # Subjects
                for subject in sorted(literature_titles):
                    titles = sorted(literature_titles[subject])
                    file.write(f"==={subject}===\n")
                    file.write('<div class="list-columns" style="column-width: 450px; max-width: 1500px;">\n')
                    for title in titles:
                        file.write(f"* {title}\n")
                    file.write('</div>\n\n')

        elif literature_type == "magazine":
            # Determine if the format has multiple dictionaries
            if len(literature_titles) == 1 and "Default" in literature_titles:
                # No subjects
                file.write('{| class="wikitable theme-red mw-collapsible sortable" style="text-align: center;"\n')
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
                    file.write('<div class="list-columns" style="column-width: 400px; max-width: 900px;">\n')
                    for title in titles:
                        file.write(f"* {title}\n")
                    file.write('</div>\n\n')

        elif literature_type == "comic":
            file.write('{| class="wikitable theme-red mw-collapsible mw-collapsed sortable" style="text-align: center;"\n')
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
            file.write("A schematic can be read, teaching the player [[crafting]] recipes.\n\n")
            file.write("===Learned recipes===\n")
            file.write(
                f"The following are the recipes this schematic can include. Each schematic can contain up to 5 recipes, "
                f"with a {100 - multiple_chance}% chance of having only 1. Each additional recipe beyond the first has an equal probability.\n"
            )
            file.write('<div class="list-columns" style="column-width: 400px; max-width: 900px;">\n')
            for title in sorted(literature_titles[:-1]):
                file.write(f"* {title}\n")
            file.write('</div>')
        
        elif literature_type == "recipe":
            content = []
            content.append("A recipe can be read, teaching the player a [[Crafting|cooking]] recipe.\n")
            content.append("===Learned recipes===")
            content.append("The following are the recipes that this can include. Only 1 recipe will be included.")
            content.append('<div class="list-columns" style="column-width: 400px; max-width: 900px;">')
            for title in sorted(literature_titles[:-1]):
                content.append(f"* {title}")
            content.append("</div>")
            file.write("\n".join(content))

        elif literature_type == "locket":
            file.write('<div class="list-columns" style="column-width: 400px; max-width: 900px;">\n')
            name = Translate.get(item_id, "DisplayName")
            locket_text = Translate.get("IGUI_LocketText", "IGUI_LocketText")
            for title in sorted(literature_titles):
                photo = Translate.get(title, "Photo")
                full_name = f"{name} {locket_text} {photo}"
                file.write(f"* {full_name}\n")
            file.write('</div>')

        elif literature_type == "doodlekids":
            file.write('<div class="list-columns" style="column-width: 400px; max-width: 900px;">\n')
            name = Translate.get(item_id, "DisplayName")
            photo_text = Translate.get("IGUI_PhotoOf", "IGUI_PhotoOf")
            for title in sorted(literature_titles):
                photo = Translate.get(title, "Doodle")
                full_name = f"{name} {photo_text} {photo}"
                file.write(f"* {full_name}\n")
            file.write('</div>')

        # postcards, doodles and photos are generated the same
        elif literature_type in ["postcards", "doodle", "photo"]:
            file.write('<div class="list-columns" style="column-width: 400px; max-width: 900px;">\n')
            name = Translate.get(item_id, "DisplayName")
            photo_text = Translate.get("IGUI_PhotoOf", "IGUI_PhotoOf")
            for title in sorted(literature_titles):
                photo = Translate.get(title, "Photo")
                full_name = f"{name} {photo_text} {photo}"
                file.write(f"* {full_name}\n")
            file.write('</div>')

        elif literature_type in ["businesscards", "jobtitles"]:
            file.write('<div class="list-columns" style="column-width:300px; max-width:1300px;">\n')
            for title in sorted(literature_titles):
                file.write(f'* {Translate.get(title, "IGUI")}\n')
            file.write('</div>')

        elif literature_type == "flier":
            item_name = Item(item_id).name
            file.write('{| class="wikitable theme-red mw-collapsible mw-collapsed sortable"\n')
            file.write(f'|+ style="min-width: 300px;" | List of {item_name.lower()} titles\n')
            file.write('! Business !! Center !! Coord1 !! Coord2\n')
            literature_titles = sorted(literature_titles, key=lambda x: x["name"])
            for business in literature_titles:
                file.write(f"|-\n| {business["name"]} || {{{{Coordinates|{business["center"]}}}}} || {{{{Coordinates|{business["coord1"]}}}}} || {{{{Coordinates|{business["coord2"]}}}}}\n")
            file.write('|}')

        else:
            file.write('<div class="list-columns" style="column-width: 400px; max-width: 900px;">\n')
            for title in sorted(literature_titles):
                file.write(f"* {title}\n")
            file.write('</div>')


def combine_txt_files(type):
    language_code = Language.get()
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
    for item_id in Item.all():
        item = Item(item_id)
        if "OnCreate" not in item.data:
            continue

        # Remove "SpecialLootSpawns." prefix
        on_create = item.on_create

        if not on_create.startswith("SpecialLootSpawns."):
            continue

        on_create = on_create.removeprefix("SpecialLootSpawns.")
        if on_create in BOOK:
            process_book(item, on_create)
        elif on_create in MAGAZINE:
            process_magazine(item, on_create)
        elif on_create in ["OnCreateComicBookRetail", "OnCreateComicBook"]:
            process_comic(item, on_create)
        elif on_create in SCHEMATIC:
            process_schematic(item, on_create)
        elif on_create in SPECIAL:
            process_special(item, on_create)
        elif on_create in LOCATION_LITERATURE:
            process_location_literature(item, on_create)
        elif on_create in GENERIC_LITERATURE:
            process_generic(item, on_create)

    # 'types' that will be combined into a single file, by 'type'.
    file_types = ["book", "magazine", "comic", "schematic", "generic"]

    for ftype in file_types:
        combine_txt_files(ftype)


if __name__ == "__main__":
    main()
