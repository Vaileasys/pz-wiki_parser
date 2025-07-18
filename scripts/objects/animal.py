import os
from scripts.utils import lua_helper, util
from scripts.core.cache import save_cache, load_cache
from scripts.core.language import Translate
from scripts.core.constants import DATA_DIR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.objects.item import Item

class Animal:
    """Represents a single animal entry."""
    _animal_data: dict = None
    _stage_animals: dict[str, set[str]] = {}
    _instances = {}
    _data_file = "parsed_animal_data.json"

    def __new__(cls, animal_id: str):
        """Ensures only one Animal instance exists per animal ID."""
        if not cls._animal_data:
            cls.load()

        if animal_id in cls._instances:
            return cls._instances[animal_id]

        instance = super().__new__(cls)
        cls._instances[animal_id] = instance
        return instance

    def __init__(self, animal_id: str):
        """Initialise the Animal instance with its data if not already initialised."""
        if hasattr(self, 'animal_id'):
            return

        if Animal._animal_data is None:
           Animal.load()

        self.animal_id = animal_id
        self._data = self._animal_data.get(animal_id, {})

    @classmethod
    def _parse(cls):
        """
        Parses Animal data from the provided Lua file and caches it.
        """
        lua_copy_table = ("""
            function copyTable(tbl)
                local copy = {}
                for k, v in pairs(tbl) do
                    if type(v) == "table" then
                        copy[k] = copyTable(v)  -- Recursively copy nested tables
                    else
                        copy[k] = v
                    end
                end
                return copy
            end
        """)
        animal_files = [
            'ChickenDefinitions.lua',
            'CowDefinitions.lua',
            'DeerDefinitions.lua',
            'MouseDefinitions.lua',
            'PigDefinitions.lua',
            'RabbitDefinitions.lua',
            'RaccoonDefinitions.lua',
            'RatDefinitions.lua',
            'SheepDefinitions.lua',
            'TurkeyDefinitions.lua',
        ]
        lua_runtime = lua_helper.load_lua_file(animal_files, inject_lua=lua_copy_table)
        parsed_data = lua_helper.parse_lua_tables(lua_runtime, tables="AnimalDefinitions")

        cls._animal_data:dict = parsed_data.get("AnimalDefinitions", {}).get("animals")

        save_cache(cls._animal_data, cls._data_file)

        return cls._animal_data
    
    @classmethod
    def _init_stages(cls):
        """Builds and caches sets of baby, male, and female animal IDs."""
        cls._stage_animals = {
            "baby": set(),
            "male": set(),
            "female": set()
        }

        if not cls._animal_data:
            return

        for animal_id, data in cls._animal_data.items():
            baby_type = data.get("babyType")
            stages = data.get("stages", {})

            if not baby_type or baby_type not in stages:
                continue

            cls._stage_animals["baby"].add(baby_type)

            stage_data = stages[baby_type]
            next_female = stage_data.get("nextStage")
            next_male = stage_data.get("nextStageMale")

            if next_female:
                cls._stage_animals["female"].add(next_female)
            if next_male:
                cls._stage_animals["male"].add(next_male)



    @classmethod
    def load(cls):
        """
        Loads Animal data from the cache, re-parsing the Lua file if the data is outdated.

        Returns:
            dict: Raw Animal data.
        """
        from scripts.core.version import Version
        if cls._animal_data is None:
            path = os.path.join(DATA_DIR, cls._data_file)

            data, version = load_cache(path, cache_name="animal", get_version=True)

            # Re-parse if outdated
            if version != Version.get():
                data = cls._parse()

            cls._animal_data = data

        if not cls._stage_animals:
            cls._init_stages()

        return cls._animal_data
    
    @classmethod
    def all(cls) -> dict[str, "Animal"]:
        """
        Returns all known Animal instances.

        Returns:
            dict[str, Animal]: Mapping of item ID to Animal instance.
        """
        if not cls._animal_data:
            cls.load()
        return {id: cls(id) for id in cls._animal_data}
    
    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of Animal types parsed.

        Returns:
            int: Number of unique Animal types.
        """
        if not cls._animal_data:
            cls.load()
        return len(cls._animal_data)
    
    @classmethod
    def exists(cls, animal_id: str) -> bool:
        """
        Checks if a Animal with the given id exists in the parsed data.

        Returns:
            bool: True if found, False otherwise.
        """
        if not cls._animal_data:
            cls.load()
        return animal_id in cls._animal_data
    
    def get(self, key: str, default=None):
        """
        Returns a raw value from the animal data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)

    @property
    def is_valid(self) -> bool:
        return self.animal_id in self._animal_data
    
    @property
    def data(self) -> dict:
        return self._data
    
    @property
    def item(self) -> "Item":
        from scripts.objects.item import Item
        return Item(self.animal_id)
    
    @property
    def name(self) -> str:
        return Translate.get("IGUI_AnimalType_" + self.animal_id, default=self.animal_id)
    
    @property
    def name_en(self) -> str:
        return Translate.get("IGUI_AnimalType_" + self.animal_id, lang_code="en", default=self.animal_id)
    
    @property
    def corpse_name(self) -> str:
        return Translate.get("IGUI_Item_AnimalCorpse").replace("%1", self.name)
    
    @property
    def corpse_name_en(self) -> str:
        return Translate.get("IGUI_Item_AnimalCorpse", lang_code="en").replace("%1", self.name_en)
    
    @property
    def skeleton_name(self) -> str:
        return Translate.get("IGUI_Item_AnimalSkeleton").replace("%1", self.name)
    
    @property
    def skeleton_name_en(self) -> str:
        return Translate.get("IGUI_Item_AnimalSkeleton", lang_code="en").replace("%1", self.name_en)
    
    @property
    def page(self) -> str: # TODO: get from page dict
        return self.group_name_en
    
    @property
    def wiki_link(self) -> str:
        return util.link(self.page, self.name)
    
    # --- Base --- #
    @property
    def group(self) -> str: return self.get("group")
    @property
    def group_name(self) -> str: return Translate.get("IGUI_Animal_Group_" + self.group, default=self.group)
    @property
    def group_name_en(self) -> str: return Translate.get("IGUI_Animal_Group_" + self.group, lang_code="en", default=self.group)
    @property
    def group_link(self) -> str: return util.link(self.page, self.group_name)
    @property
    def base_encumbrance(self) -> float | None: return self.get("baseEncumbrance")
    @property
    def trailer_base_size(self) -> float | None: return self.get("trailerBaseSize")
    @property
    def carcass_item(self) -> "Item | None":
        from scripts.objects.item import Item
        if not hasattr(self, "_carcass_item"):
            carcass_item = self.get("carcassItem")
            if Item.exists(carcass_item):
                self._carcass_item = Item(carcass_item)
            else:
                self._carcass_item = None
        return self._carcass_item
    @property
    def min_weight(self) -> float | None: return self.get("minWeight")
    @property
    def max_weight(self) -> float | None: return self.get("maxWeight")
    @property
    def min_size(self) -> float | None: return self.get("minSize")
    @property
    def max_size(self) -> float | None: return self.get("maxSize")
    @property
    def animal_size(self) -> float | None: return self.get("animalSize")
    @property
    def corpse_size(self) -> float | None: return self.get("corpseSize")
    @property
    def collision_size(self) -> float | None: return self.get("collisionSize")
    @property
    def texture_skeleton_bloody(self) -> str | None: return self.get("textureSkeletonBloody")
    @property
    def is_baby(self) -> bool:
        return self.animal_id in self._stage_animals.get("baby")
    @property
    def is_male(self) -> bool:
        return self.animal_id in self._stage_animals.get("male")
    @property
    def is_female(self) -> bool:
        return self.animal_id in self._stage_animals.get("female")


    # --- Physiology and stats --- #
    @property
    def hunger_multiplier(self) -> float | None: return self.get("hungerMultiplier")
    @property
    def thirst_multiplier(self) -> float | None: return self.get("thirstMultiplier")
    @property
    def hunger_boost(self) -> float | None: return self.get("hungerBoost")
    @property
    def thirst_boost(self) -> float | None: return self.get("thirstBoost")
    @property
    def health_loss_multiplier(self) -> float | None: return self.get("healthLossMultiplier")
    @property
    def max_blood(self) -> int | None: return self.get("maxBlood")
    @property
    def min_blood(self) -> int | None: return self.get("minBlood")

    # --- Behaviour and AI --- #
    @property
    def can_be_pet(self) -> bool: return self.get("canBePet", False)
    @property
    def can_thump(self) -> bool: return self.get("canThump", False)
    @property
    def can_be_picked(self) -> bool: return self.get("canBePicked", False)
    @property
    def always_flee_humans(self) -> bool: return self.get("alwaysFleeHumans", False)
    @property
    def stress_under_rain(self) -> bool: return self.get("stressUnderRain", False)
    @property
    def stress_above_ground(self) -> bool: return self.get("stressAboveGround", False)
    @property
    def sit_randomly(self) -> bool: return self.get("sitRandomly", False)
    @property
    def dont_attack_other_male(self) -> bool: return self.get("dontAttackOtherMale", False)
    @property
    def knockdown_attack(self) -> bool: return self.get("knockdownAttack", False)
    @property
    def eat_grass(self) -> bool: return self.get("eatGrass", False)
    @property
    def can_do_laceration(self) -> bool: return self.get("canDoLaceration", False)
    @property
    def can_be_attached(self) -> bool: return self.get("canBeAttached", False)
    @property
    def attack_dist(self) -> float | None: return self.get("attackDist")
    @property
    def attack_timer(self) -> int | None: return self.get("attackTimer")
    @property
    def attack_if_stressed(self) -> bool: return self.get("attackIfStressed", False)
    @property
    def attack_back(self) -> bool: return self.get("attackBack", False)
    @property
    def base_dmg(self) -> float | None: return self.get("baseDmg")
    @property
    def thirst_hunger_trigger(self) -> float | None: return self.get("thirstHungerTrigger")
    @property
    def exit_hutch_time(self) -> int | None: return self.get("exitHutchTime")
    @property
    def enter_hutch_time(self) -> int | None: return self.get("enterHutchTime")
    @property
    def idle_type_nbr(self) -> int | None: return self.get("idleTypeNbr")
    @property
    def periodic_run(self) -> bool: return self.get("periodicRun", False)
    @property
    def male(self) -> bool: return self.get("male", False)
    @property
    def female(self) -> bool: return self.get("female", False)
    @property
    def udder(self) -> bool: return self.get("udder", False)
    @property
    def wild(self) -> bool: return self.get("wild", False)
    @property
    def eat_from_mother(self) -> bool: return self.get("eatFromMother", False)
    @property
    def need_mom(self) -> bool: return self.get("needMom", False)
    @property
    def can_climb_stairs(self) -> bool: return self.get("canClimbStairs", False)
    @property
    def add_tracking_xp(self) -> bool: return self.get("addTrackingXp", False)
    @property
    def wild_flee_time_until_dead_timer(self) -> int | None: return self.get("wildFleeTimeUntilDeadTimer")
    @property
    def spotting_dist(self) -> float | None: return self.get("spottingDist")

    # --- Genetics and breeding --- #
    @property
    def genes(self) -> dict:
        return self.get("genes", {})
    @property
    def stages(self) -> dict:
        return self.get("stages", {})
    @property
    def breeds(self) -> "list[AnimalBreed]":
        if not hasattr(self, "_breeds"):
            breed_data = self.get("breeds", {})
            self._breeds = [
                AnimalBreed(breed_id, data, self)
                for breed_id, data in breed_data.items()
            ]
        return self._breeds
    @property
    def mating_period(self) -> tuple[int | None, int | None]: return (self.get("matingPeriodStart"), self.get("matingPeriodEnd"))
    @property
    def min_age(self) -> int | None: return self.get("minAge")
    @property
    def max_age_geriatric(self) -> int | None: return self.get("maxAgeGeriatric")
    @property
    def min_age_for_baby(self) -> int | None: return self.get("minAgeForBaby")
    @property
    def baby_type(self) -> str | None: return self.get("babyType")
    @property
    def mate(self) -> str | None: return self.get("mate")
    @property
    def baby_nbr(self) -> str | None: return self.get("babyNbr")
    @property
    def pregnant_period(self) -> int | None: return self.get("pregnantPeriod")
    @property
    def time_before_next_pregnancy(self) -> int | None: return self.get("timeBeforeNextPregnancy")

    # --- Animation and visuals --- #
    @property
    def inv_icon(self) -> str | None: return self.get("invIcon")
    @property
    def inv_icon_male(self) -> str | None: return self.get("invIconMale")
    @property
    def inv_icon_female(self) -> str | None: return self.get("invIconFemale")
    @property
    def inv_icon_corpse(self) -> str | None: return self.get("invIconCorpse")
    @property
    def inv_icon_skeleton(self) -> str | None: return self.get("invIconSkeleton")
    @property
    def model_script(self) -> str | None: return self.get("modelscript")
    @property
    def anim_set(self) -> str | None: return self.get("animset")
    @property
    def texture_skeleton(self) -> str | None: return self.get("textureSkeleton")
    @property
    def texture_skinned(self) -> str | None: return self.get("textureSkinned")
    @property
    def body_model(self) -> str | None: return self.get("bodyModel")
    @property
    def body_model_skel(self) -> str | None: return self.get("bodyModelSkel")
    @property
    def body_model_skel_no_head(self) -> str | None: return self.get("bodyModelSkelNoHead")
    @property
    def body_model_headless(self) -> str | None: return self.get("bodyModelHeadless")
    @property
    def rope_bone(self) -> str | None: return self.get("ropeBone")
    @property
    def shadow_w(self) -> float | None: return self.get("shadoww")
    @property
    def shadow_fm(self) -> float | None: return self.get("shadowfm")
    @property
    def shadow_bm(self) -> float | None: return self.get("shadowbm")
    @property
    def sitting_type_nbr(self) -> int | None: return self.get("sittingTypeNbr")
    @property
    def idle_emote_chance(self) -> int | None: return self.get("idleEmoteChance")

    # --- Sound --- #
    @property
    def sounds(self) -> dict: return self.get("sounds", {})
    @property
    def idle_sound_radius(self) -> int | None: return self.get("idleSoundRadius")
    @property
    def idle_sound_volume(self) -> int | None: return self.get("idleSoundVolume")

    # --- Misc --- #
    @property
    def dung(self) -> "Item | None":
        from scripts.objects.item import Item
        if not hasattr(self, "_dung"):
            dung = self.get("dung")
            if Item.exists(dung):
                self._dung = Item(dung)
            else:
                self._dung = None
        return self._dung
    @property
    def dung_chance_per_day(self) -> float | None: return self.get("dungChancePerDay")
    @property
    def enclosure_size(self) -> float | None: return self.get("minEnclosureSize")
    @property
    def eat_type_trough(self) -> str | None: return self.get("eatTypeTrough")
    @property
    def hutches(self) -> str | None: return self.get("hutches")
    @property
    def wander_mul(self) -> float | None: return self.get("wanderMul")
    @property
    def lured_possible_items(self) -> list: return self.get("luredPossibleItems", [])

    def __repr__(self):
        return f"<Animal {self.animal_id}>"


class AnimalBreed:

    def __init__(self, breed: str, breed_data: dict, animal: Animal):
        """Initialise the breed instance."""
        self.breed_id = breed
        self.animal = animal
        self._data = breed_data
    
    def get(self, key: str, default=None):
        """
        Returns a raw value from the animal breed data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)
    
    def build_icon(self, icon: str, page: str, name: str, default: str = None) -> str:
        if not icon:
            icon = default
        return f"[[File:{icon.removeprefix("Item_").removesuffix(".png")}.png|32x32px|link={page}|{name}]]"
    
    def get_name(self, stage: str = None) -> str:
        text = self.name
        if stage == "dead":
            text = Translate.get("IGUI_Item_AnimalCorpse").replace("%1", text)
        elif stage == "skeleton":
            text = Translate.get("IGUI_Item_AnimalSkeleton").replace("%1", text)
        return text
    
    def get_link(self, stage: str = None) -> str:
        name = self.get_name(stage)
        return util.link(self.page, name)
    
    @property
    def data(self) -> dict:
        return self._data
    
    @property
    def name(self) -> str:
        return self.breed_name + " " + self.animal.name
    
    @property
    def breed_name(self) -> str:
        return Translate.get("IGUI_Breed_" + self.breed_id, default=self.breed_id)
    
    @property
    def breed_name_en(self) -> str:
        return Translate.get("IGUI_Breed_" + self.breed_id, lang_code="en", default=self.breed_id)
    
    @property
    def page(self) -> str: #TODO: get from page dict?
        return self.animal.page
    
    @property
    def wiki_link(self) -> str:
        return self.get_link()
    
    @property
    def icons(self) -> str:
        if self.animal.is_baby:
            return self.build_icon(self.inv_icon_baby, self.page, self.name)
        if self.animal.is_male:
            return self.build_icon(self.inv_icon_male, self.page, self.name)
        if self.animal.is_female:
            return self.build_icon(self.inv_icon_female, self.page, self.name)
    
    @property
    def dead_icons(self) -> str:
        if self.animal.is_baby:
            return self.build_icon(self.inv_icon_baby_dead, self.page, self.name, default=self.inv_icon_baby)
        if self.animal.is_male:
            return self.build_icon(self.inv_icon_male_dead, self.page, self.name, default=self.inv_icon_male)
        if self.animal.is_female:
            return self.build_icon(self.inv_icon_female_dead, self.page, self.name, default=self.inv_icon_female)
    
    @property
    def skeleton_icons(self) -> str:
        if self.animal.is_baby:
            return self.build_icon(self.inv_icon_baby_skel, self.page, self.name, default=self.inv_icon_baby_dead or self.inv_icon_baby)
        if self.animal.is_male:
            return self.build_icon(self.inv_icon_male_skel, self.page, self.name, default=self.inv_icon_male_dead or self.inv_icon_male)
        if self.animal.is_female:
            return self.build_icon(self.inv_icon_female_skel, self.page, self.name, default=self.inv_icon_female_dead or self.inv_icon_female)
    
    @property
    def inv_icon_male(self) -> str:
        return self.get("invIconMale")
    
    @property
    def inv_icon_female(self) -> str:
        return self.get("invIconFemale")
    
    @property
    def inv_icon_baby(self) -> str:
        return self.get("invIconBaby")
    
    @property
    def inv_icon_male_dead(self) -> str:
        return self.get("invIconMaleDead")
    
    @property
    def inv_icon_female_dead(self) -> str:
        return self.get("invIconFemaleDead")
    
    @property
    def inv_icon_baby_dead(self) -> str:
        return self.get("invIconBabyDead")
    
    @property
    def inv_icon_male_skel(self) -> str:
        return self.get("invIconMaleSkel")
    
    @property
    def inv_icon_female_skel(self) -> str:
        return self.get("invIconFemaleSkel")
    
    @property
    def inv_icon_baby_skel(self) -> str:
        return self.get("invIconBabySkel")

    def __repr__(self):
        return f"<AnimalBreed {self.animal.animal_id}:{self.breed_id}>"

if __name__ == "__main__":
#    animal = Animal("cow")
#    print(animal.wiki_link)
#    dung = animal.dung
#    print(f"{dung.icon} {dung.name}")
    from scripts.core.file_loading import write_file

    animals = {}

    for animal_id, animal in Animal.all().items():
        if animal.group_name not in animals:
            animals[animal.group_name] = []

        animals[animal.group_name].append(f"==={animal.name}===")
        breeds = animal.breeds
        for breed in breeds:
            animals[animal.group_name].append(f"===={breed.breed_name}====")
            animals[animal.group_name].append(f"*{breed.icons} {breed.wiki_link}")
            animals[animal.group_name].append(f"*{breed.dead_icons} {breed.get_link("dead")}")
            animals[animal.group_name].append(f"*{breed.skeleton_icons} {breed.get_link("skeleton")}")
    
    content = []
    for group, breed in animals.items():
        content.append(f"=={group}==")
        content.extend(breed)
    
    write_file(content)